import { describe, expect, it } from "vitest";
import { gjkIntersect } from "../src/gjk";

// A unit cube at origin
const unitCube: [number, number, number][] = [
  [0, 0, 0], [1, 0, 0], [0, 1, 0], [1, 1, 0],
  [0, 0, 1], [1, 0, 1], [0, 1, 1], [1, 1, 1],
];

// Cube shifted by 2 on x-axis (disjoint)
const disjointCube: [number, number, number][] = unitCube.map(
  ([x, y, z]) => [x + 2, y, z] as [number, number, number],
);

// Cube shifted by 0.5 (overlaps unitCube)
const overlapCube: [number, number, number][] = unitCube.map(
  ([x, y, z]) => [x + 0.5, y, z] as [number, number, number],
);

// Tetrahedron sharing a vertex with unitCube (touches at (1,1,1))
const touchingTet: [number, number, number][] = [
  [1, 1, 1], [2, 1, 1], [1, 2, 1], [1, 1, 2],
];

describe("gjkIntersect", () => {
  it("detects overlap between two overlapping cubes", () => {
    expect(gjkIntersect(unitCube, overlapCube)).toBe(true);
  });

  it("detects non-overlap between two separated cubes", () => {
    expect(gjkIntersect(unitCube, disjointCube)).toBe(false);
  });

  it("detects vertex-touching as intersection", () => {
    expect(gjkIntersect(unitCube, touchingTet)).toBe(true);
  });

  it("returns false for single-point vs far-away single-point", () => {
    expect(gjkIntersect([[0, 0, 0]], [[10, 10, 10]])).toBe(false);
  });
});
