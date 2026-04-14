import type { BoundingBox } from "./types";

/**
 * Compute an axis-aligned bounding box from a flat vertex array.
 *
 * The input is a flattened sequence of `[x0, y0, z0, x1, y1, z1, ...]`
 * — the format every modern CAD exporter uses for raw vertex buffers.
 * Throws if the input is empty or not a multiple of 3.
 */
export function buildAABB(vertices: readonly number[]): BoundingBox {
  if (vertices.length === 0 || vertices.length % 3 !== 0) {
    throw new Error(
      `vertices must be a non-empty flat array with length divisible by 3 (got ${vertices.length})`,
    );
  }
  let minX = Infinity;
  let minY = Infinity;
  let minZ = Infinity;
  let maxX = -Infinity;
  let maxY = -Infinity;
  let maxZ = -Infinity;
  for (let i = 0; i < vertices.length; i += 3) {
    const x = vertices[i]!;
    const y = vertices[i + 1]!;
    const z = vertices[i + 2]!;
    if (x < minX) minX = x;
    if (y < minY) minY = y;
    if (z < minZ) minZ = z;
    if (x > maxX) maxX = x;
    if (y > maxY) maxY = y;
    if (z > maxZ) maxZ = z;
  }
  return { min: [minX, minY, minZ], max: [maxX, maxY, maxZ] };
}

/** Canonical AABB-AABB overlap test (edge-touching counts as a hit). */
export function intersectsAABB(a: BoundingBox, b: BoundingBox): boolean {
  return (
    a.min[0] <= b.max[0] && a.max[0] >= b.min[0] &&
    a.min[1] <= b.max[1] && a.max[1] >= b.min[1] &&
    a.min[2] <= b.max[2] && a.max[2] >= b.min[2]
  );
}

/**
 * Minimum Euclidean distance between two AABBs. Returns 0 for
 * overlapping or touching boxes.
 */
export function distanceAABB(a: BoundingBox, b: BoundingBox): number {
  const dx = Math.max(0, Math.max(b.min[0] - a.max[0], a.min[0] - b.max[0]));
  const dy = Math.max(0, Math.max(b.min[1] - a.max[1], a.min[1] - b.max[1]));
  const dz = Math.max(0, Math.max(b.min[2] - a.max[2], a.min[2] - b.max[2]));
  return Math.sqrt(dx * dx + dy * dy + dz * dz);
}
