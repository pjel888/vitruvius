import { describe, expect, it } from "vitest";
import { mkdtempSync, readFileSync, rmSync } from "fs";
import { tmpdir } from "os";
import { join } from "path";
import {
  INTEGRITY_FOOTER_PREFIX,
  computeContractBodySha256,
  writeContract,
} from "../src/contract_writer";
import type { SpatialContract } from "../src/types";

function splitBodyAndDigest(raw: string): { body: string; digest: string } {
  const footerIdx = raw.lastIndexOf("\n" + INTEGRITY_FOOTER_PREFIX);
  if (footerIdx < 0) {
    throw new Error("integrity footer missing");
  }
  const body = raw.slice(0, footerIdx + 1); // keep trailing newline of body
  const footerLine = raw.slice(footerIdx + 1).trimEnd();
  const digest = footerLine.slice(INTEGRITY_FOOTER_PREFIX.length);
  return { body, digest };
}

describe("writeContract", () => {
  it("writes a valid JSON file with the schema_version field", () => {
    const dir = mkdtempSync(join(tmpdir(), "vitruvius-daemon-"));
    try {
      const contract: SpatialContract = {
        schema_version: "1.0.0",
        spatial_context_id: "spatial-test-01",
        generated_at_utc: "2026-04-15T09:00:00Z",
        source_daemon: "vitruvius-spatial-daemon@0.1.0",
        instances: [
          {
            instance_id: "instance-door-01",
            canonical_concept_id: "concept-doors-and-exits",
          },
        ],
        spatial_edges: [],
      };
      const path = writeContract(contract, dir);
      const raw = readFileSync(path, "utf-8");
      const { body } = splitBodyAndDigest(raw);
      const onDisk = JSON.parse(body);
      expect(onDisk.schema_version).toBe("1.0.0");
      expect(onDisk.spatial_context_id).toBe("spatial-test-01");
      expect(path.endsWith("spatial-test-01.json")).toBe(true);
    } finally {
      rmSync(dir, { recursive: true, force: true });
    }
  });

  it("appends a SHA-256 integrity footer matching the JSON body", () => {
    const dir = mkdtempSync(join(tmpdir(), "vitruvius-daemon-"));
    try {
      const contract: SpatialContract = {
        schema_version: "1.0.0",
        spatial_context_id: "spatial-integrity-01",
        generated_at_utc: "2026-04-15T09:00:00Z",
        source_daemon: "vitruvius-spatial-daemon@0.1.0",
        instances: [
          {
            instance_id: "instance-door-01",
            canonical_concept_id: "concept-doors-and-exits",
          },
        ],
        spatial_edges: [],
      };
      const path = writeContract(contract, dir);
      const raw = readFileSync(path, "utf-8");
      const { body, digest } = splitBodyAndDigest(raw);
      // Digest in footer must match recomputed body hash.
      expect(digest).toMatch(/^[0-9a-f]{64}$/);
      expect(digest).toBe(computeContractBodySha256(body));
      // Trailing line after footer ends in newline
      expect(raw.endsWith("\n")).toBe(true);
    } finally {
      rmSync(dir, { recursive: true, force: true });
    }
  });

  it("throws when spatial_context_id does not start with 'spatial-'", () => {
    const dir = mkdtempSync(join(tmpdir(), "vitruvius-daemon-"));
    try {
      const contract: SpatialContract = {
        schema_version: "1.0.0",
        spatial_context_id: "bad" as SpatialContract["spatial_context_id"],
        generated_at_utc: "2026-04-15T09:00:00Z",
        instances: [],
        spatial_edges: [],
      };
      expect(() => writeContract(contract, dir)).toThrow();
    } finally {
      rmSync(dir, { recursive: true, force: true });
    }
  });

  it("throws when an instance_id lacks the 'instance-' prefix", () => {
    const dir = mkdtempSync(join(tmpdir(), "vitruvius-daemon-"));
    try {
      const contract: SpatialContract = {
        schema_version: "1.0.0",
        spatial_context_id: "spatial-ok",
        generated_at_utc: "2026-04-15T09:00:00Z",
        instances: [
          // eslint-disable-next-line @typescript-eslint/no-explicit-any
          { instance_id: "door", canonical_concept_id: "concept-door" } as any,
        ],
        spatial_edges: [],
      };
      expect(() => writeContract(contract, dir)).toThrow();
    } finally {
      rmSync(dir, { recursive: true, force: true });
    }
  });
});
