import { describe, expect, it } from "vitest";
import { buildAABB, distanceAABB, intersectsAABB } from "../src/aabb";
import type { BoundingBox } from "../src/types";

describe("buildAABB", () => {
  it("computes min/max from a flat vertex list", () => {
    const verts = [0, 0, 0, 1, 2, 3, -1, 4, 0.5];
    const box = buildAABB(verts);
    expect(box.min).toEqual([-1, 0, 0]);
    expect(box.max).toEqual([1, 4, 3]);
  });

  it("throws if vertices length is not a multiple of 3", () => {
    expect(() => buildAABB([0, 0])).toThrow();
  });

  it("throws if vertices is empty", () => {
    expect(() => buildAABB([])).toThrow();
  });
});

describe("intersectsAABB", () => {
  it("detects overlap", () => {
    const a: BoundingBox = { min: [0, 0, 0], max: [2, 2, 2] };
    const b: BoundingBox = { min: [1, 1, 1], max: [3, 3, 3] };
    expect(intersectsAABB(a, b)).toBe(true);
  });

  it("detects non-overlap", () => {
    const a: BoundingBox = { min: [0, 0, 0], max: [1, 1, 1] };
    const b: BoundingBox = { min: [2, 2, 2], max: [3, 3, 3] };
    expect(intersectsAABB(a, b)).toBe(false);
  });

  it("treats edge-touching as intersection", () => {
    const a: BoundingBox = { min: [0, 0, 0], max: [1, 1, 1] };
    const b: BoundingBox = { min: [1, 1, 1], max: [2, 2, 2] };
    expect(intersectsAABB(a, b)).toBe(true);
  });
});

describe("distanceAABB", () => {
  it("returns 0 for overlapping boxes", () => {
    const a: BoundingBox = { min: [0, 0, 0], max: [2, 2, 2] };
    const b: BoundingBox = { min: [1, 1, 1], max: [3, 3, 3] };
    expect(distanceAABB(a, b)).toBe(0);
  });

  it("returns separation distance for disjoint boxes along x-axis", () => {
    const a: BoundingBox = { min: [0, 0, 0], max: [1, 1, 1] };
    const b: BoundingBox = { min: [3, 0, 0], max: [4, 1, 1] };
    expect(distanceAABB(a, b)).toBeCloseTo(2);
  });

  it("returns Euclidean separation for diagonally disjoint boxes", () => {
    const a: BoundingBox = { min: [0, 0, 0], max: [1, 1, 1] };
    const b: BoundingBox = { min: [4, 5, 0], max: [5, 6, 1] };
    // nearest corners: (1,1,0) and (4,5,0) → sqrt(9+16) = 5
    expect(distanceAABB(a, b)).toBeCloseTo(5);
  });
});
