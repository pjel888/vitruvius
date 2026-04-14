import { describe, expect, it } from "vitest";
import type { Instance, SpatialContract, SpatialEdge } from "../src/types";

describe("types scaffold", () => {
  it("exposes the SpatialContract interface shape", () => {
    const contract: SpatialContract = {
      schema_version: "1.0.0",
      spatial_context_id: "spatial-test-01",
      generated_at_utc: "2026-04-15T09:00:00Z",
      instances: [],
      spatial_edges: [],
    };
    expect(contract.schema_version).toBe("1.0.0");
  });

  it("enforces Instance id prefix via comment convention", () => {
    const i: Instance = {
      instance_id: "instance-door-01",
      canonical_concept_id: "concept-doors-and-exits",
    };
    expect(i.instance_id.startsWith("instance-")).toBe(true);
    expect(i.canonical_concept_id.startsWith("concept-")).toBe(true);
  });

  it("exposes SpatialEdge with predicate union", () => {
    const e: SpatialEdge = {
      source_instance: "instance-a",
      predicate: "spatial_intersects",
      target_instance: "instance-b",
    };
    expect(e.predicate).toBe("spatial_intersects");
  });
});
