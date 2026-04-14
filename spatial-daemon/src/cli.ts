import { readFileSync } from "fs";
import { buildAABB, distanceAABB, intersectsAABB } from "./aabb";
import { writeContract } from "./contract_writer";
import type { Instance, SpatialContract, SpatialEdge } from "./types";

interface RawEntity {
  instance_id: string;
  canonical_concept_id: string;
  vertices: number[];
}

interface RawInput {
  spatial_context_id: string;
  entities: RawEntity[];
}

export interface AnalyzeResult {
  writtenPath: string;
  contract: SpatialContract;
}

/**
 * Parse a raw vertex-list input file, compute AABBs for each entity,
 * check pairwise intersection + clearance, and write the resulting
 * SpatialContract into `outputDir`.
 *
 * Emitted edges per pair:
 *   * `spatial_intersects` — only when the two AABBs overlap.
 *   * `spatial_clearance` — always; carries the Euclidean separation
 *     in meters rounded to 3 decimals (0 when intersecting).
 */
export function analyzeFromInputFile(
  inputPath: string,
  outputDir: string,
): AnalyzeResult {
  const raw = JSON.parse(readFileSync(inputPath, "utf-8")) as RawInput;

  const instances: Instance[] = raw.entities.map((e) => ({
    instance_id: e.instance_id,
    canonical_concept_id: e.canonical_concept_id,
    bounding_box: buildAABB(e.vertices),
  }));

  const edges: SpatialEdge[] = [];
  for (let i = 0; i < instances.length; i++) {
    for (let j = i + 1; j < instances.length; j++) {
      const a = instances[i]!;
      const b = instances[j]!;
      if (!a.bounding_box || !b.bounding_box) continue;
      if (intersectsAABB(a.bounding_box, b.bounding_box)) {
        edges.push({
          source_instance: a.instance_id,
          predicate: "spatial_intersects",
          target_instance: b.instance_id,
        });
      }
      const distance = distanceAABB(a.bounding_box, b.bounding_box);
      edges.push({
        source_instance: a.instance_id,
        predicate: "spatial_clearance",
        target_instance: b.instance_id,
        value: Math.round(distance * 1000) / 1000,
        unit: "meters",
      });
    }
  }

  const contract: SpatialContract = {
    schema_version: "1.0.0",
    spatial_context_id: raw.spatial_context_id,
    generated_at_utc: new Date().toISOString().replace(/\.\d+Z$/, "Z"),
    source_daemon: "vitruvius-spatial-daemon@0.1.0",
    instances,
    spatial_edges: edges,
  };

  const writtenPath = writeContract(contract, outputDir);
  return { writtenPath, contract };
}

// Node entrypoint — invoked via `npx vitruvius-spatial --input ... --output ...`
if (import.meta.url === `file://${process.argv[1]}`) {
  const args = process.argv.slice(2);
  const inputIdx = args.indexOf("--input");
  const outputIdx = args.indexOf("--output");
  if (inputIdx < 0 || outputIdx < 0) {
    console.error("Usage: vitruvius-spatial --input <file.json> --output <dir>");
    process.exit(2);
  }
  const result = analyzeFromInputFile(args[inputIdx + 1]!, args[outputIdx + 1]!);
  console.log(JSON.stringify({ written: result.writtenPath }, null, 2));
}
