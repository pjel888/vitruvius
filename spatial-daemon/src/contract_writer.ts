import { createHash } from "crypto";
import { mkdirSync, writeFileSync } from "fs";
import { join } from "path";
import type { SpatialContract } from "./types";

/**
 * Integrity footer marker prepended to the hex digest.
 *
 * The footer is appended AFTER the JSON body as a final `#`-prefixed
 * line so that:
 *
 *   - Naive consumers that strip comments can still parse the JSON.
 *   - The Python-side reader (`scripts/vitruvius/spatial/contract_reader.py`)
 *     splits on the marker, verifies the hash of the body, and raises
 *     IntegrityError on mismatch.
 *
 * This closes the MEDIUM admission-gate gap recorded in the Task 2
 * audit (Sprint AUDIT-1). SHA-256 is used rather than BLAKE3 because
 * the integrity audit benchmarked BLAKE3 at only 0.7x of SHA-256 on
 * Apple Silicon (SHA-256 has ARMv8 crypto extension hardware support).
 */
export const INTEGRITY_FOOTER_PREFIX = "# sha256: ";

const ALLOWED_PREDICATES = new Set([
  "spatial_intersects",
  "spatial_clearance",
  "spatial_adjacent_to",
  "spatial_contains",
]);

function assertContract(contract: SpatialContract): void {
  if (contract.schema_version !== "1.0.0") {
    throw new Error(
      `schema_version must be "1.0.0" (got ${contract.schema_version})`,
    );
  }
  if (!contract.spatial_context_id.startsWith("spatial-")) {
    throw new Error(
      `spatial_context_id must start with 'spatial-' (got ${contract.spatial_context_id})`,
    );
  }
  for (const inst of contract.instances) {
    if (!inst.instance_id.startsWith("instance-")) {
      throw new Error(
        `instance_id must start with 'instance-' (got ${inst.instance_id})`,
      );
    }
    if (!inst.canonical_concept_id.startsWith("concept-")) {
      throw new Error(
        `canonical_concept_id must start with 'concept-' (got ${inst.canonical_concept_id})`,
      );
    }
  }
  for (const edge of contract.spatial_edges) {
    if (!ALLOWED_PREDICATES.has(edge.predicate)) {
      throw new Error(`unknown predicate: ${edge.predicate}`);
    }
    if (!edge.source_instance.startsWith("instance-")) {
      throw new Error(
        `source_instance must start with 'instance-' (got ${edge.source_instance})`,
      );
    }
    if (!edge.target_instance.startsWith("instance-")) {
      throw new Error(
        `target_instance must start with 'instance-' (got ${edge.target_instance})`,
      );
    }
  }
}

/**
 * Compute the SHA-256 hex digest of the JSON body of a contract file.
 *
 * The body is the pretty-printed JSON plus a single trailing newline
 * — the exact bytes committed to disk BEFORE the integrity footer.
 *
 * Exported so the Python reader can share the hashing contract via
 * parity tests.
 */
export function computeContractBodySha256(body: string): string {
  return createHash("sha256").update(body, "utf-8").digest("hex");
}

/**
 * Write a validated `SpatialContract` to `<outputDir>/<spatial_context_id>.json`.
 *
 * The file is a pretty-printed JSON document with a trailing newline
 * followed by an integrity footer of the form
 * `# sha256: <hex>\n`. Missing parent directories are created.
 * Returns the absolute path of the written file.
 *
 * The integrity footer closes the MEDIUM admission-gate gap recorded
 * in the Sprint AUDIT-1 Task 2 audit — Python readers can detect
 * truncation or corruption by recomputing the hash of the JSON body
 * and comparing against the footer.
 */
export function writeContract(contract: SpatialContract, outputDir: string): string {
  assertContract(contract);
  mkdirSync(outputDir, { recursive: true });
  const filename = `${contract.spatial_context_id}.json`;
  const path = join(outputDir, filename);
  const body = JSON.stringify(contract, null, 2) + "\n";
  const digest = computeContractBodySha256(body);
  const payload = body + INTEGRITY_FOOTER_PREFIX + digest + "\n";
  writeFileSync(path, payload, "utf-8");
  return path;
}
