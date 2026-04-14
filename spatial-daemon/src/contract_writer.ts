import { mkdirSync, writeFileSync } from "fs";
import { join } from "path";
import type { SpatialContract } from "./types";

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
 * Write a validated `SpatialContract` to `<outputDir>/<spatial_context_id>.json`.
 *
 * The file is a pretty-printed JSON document with a trailing
 * newline. Missing parent directories are created. Returns the
 * absolute path of the written file.
 */
export function writeContract(contract: SpatialContract, outputDir: string): string {
  assertContract(contract);
  mkdirSync(outputDir, { recursive: true });
  const filename = `${contract.spatial_context_id}.json`;
  const path = join(outputDir, filename);
  writeFileSync(path, JSON.stringify(contract, null, 2) + "\n", "utf-8");
  return path;
}
