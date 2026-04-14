/**
 * Minimal GJK intersection test for convex point-clouds in 3D.
 *
 * This is a boolean-only GJK implementation — "do these two convex
 * hulls overlap?" — sized for the Vitruvius spatial daemon. For
 * distance queries, use `distanceAABB` from `aabb.ts` against the
 * hull AABBs.
 *
 * References:
 *  - Van den Bergen, "A Fast and Robust GJK Implementation for
 *    Collision Detection of Convex Objects", JGT 4(2):7–25, 1999.
 *  - Ericson, Real-Time Collision Detection, Chapter 9.
 */

type Vec3 = readonly [number, number, number];

const MAX_ITERS = 32;
const EPSILON = 1e-9;

function sub(a: Vec3, b: Vec3): Vec3 {
  return [a[0] - b[0], a[1] - b[1], a[2] - b[2]];
}

function dot(a: Vec3, b: Vec3): number {
  return a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
}

function cross(a: Vec3, b: Vec3): Vec3 {
  return [
    a[1] * b[2] - a[2] * b[1],
    a[2] * b[0] - a[0] * b[2],
    a[0] * b[1] - a[1] * b[0],
  ];
}

function neg(a: Vec3): Vec3 {
  return [-a[0], -a[1], -a[2]];
}

function support(points: readonly Vec3[], direction: Vec3): Vec3 {
  let best = points[0]!;
  let bestDot = dot(best, direction);
  for (let i = 1; i < points.length; i++) {
    const p = points[i]!;
    const d = dot(p, direction);
    if (d > bestDot) {
      bestDot = d;
      best = p;
    }
  }
  return best;
}

function minkowskiSupport(
  a: readonly Vec3[],
  b: readonly Vec3[],
  direction: Vec3,
): Vec3 {
  return sub(support(a, direction), support(b, neg(direction)));
}

function doSimplex(simplex: Vec3[], _direction: Vec3): Vec3 {
  // Returns the new search direction; mutates `simplex` to keep only
  // the sub-simplex closest to the origin.
  if (simplex.length === 2) {
    const b = simplex[0]!;
    const a = simplex[1]!;
    const ab = sub(b, a);
    const ao = neg(a);
    const newDir = cross(cross(ab, ao), ab);
    if (dot(newDir, newDir) < EPSILON) {
      // Origin lies on the AB segment.
      return [0, 0, 0];
    }
    return newDir;
  }
  if (simplex.length === 3) {
    const c = simplex[0]!;
    const b = simplex[1]!;
    const a = simplex[2]!;
    const ab = sub(b, a);
    const ac = sub(c, a);
    const ao = neg(a);
    const abc = cross(ab, ac);
    if (dot(cross(abc, ac), ao) > 0) {
      simplex.splice(1, 1); // keep [c, a]
      return cross(cross(ac, ao), ac);
    }
    if (dot(cross(ab, abc), ao) > 0) {
      simplex.splice(0, 1); // keep [b, a]
      return cross(cross(ab, ao), ab);
    }
    if (dot(abc, ao) > 0) {
      return abc;
    }
    simplex.reverse();
    return neg(abc);
  }
  // Tetrahedron case
  const d = simplex[0]!;
  const c = simplex[1]!;
  const b = simplex[2]!;
  const a = simplex[3]!;
  const ab = sub(b, a);
  const ac = sub(c, a);
  const ad = sub(d, a);
  const ao = neg(a);
  const abc = cross(ab, ac);
  const acd = cross(ac, ad);
  const adb = cross(ad, ab);
  if (dot(abc, ao) > 0) {
    simplex.splice(0, 1); // drop d
    return abc;
  }
  if (dot(acd, ao) > 0) {
    simplex.splice(2, 1); // drop b
    return acd;
  }
  if (dot(adb, ao) > 0) {
    simplex.splice(1, 1); // drop c
    return adb;
  }
  return [0, 0, 0];
}

/**
 * Boolean GJK: returns `true` iff the two convex hulls overlap.
 *
 * Handles vertex-touching as intersection (consistent with the
 * AABB edge-touching convention in `aabb.ts`) via the
 * `dot(a, direction) < -EPSILON` early exit.
 */
export function gjkIntersect(
  hullA: readonly Vec3[],
  hullB: readonly Vec3[],
): boolean {
  if (hullA.length === 0 || hullB.length === 0) return false;
  let direction: Vec3 = [1, 0, 0];
  const simplex: Vec3[] = [minkowskiSupport(hullA, hullB, direction)];
  direction = neg(simplex[0]!);
  for (let i = 0; i < MAX_ITERS; i++) {
    const a = minkowskiSupport(hullA, hullB, direction);
    if (dot(a, direction) < -EPSILON) {
      return false;
    }
    simplex.push(a);
    const newDir = doSimplex(simplex, direction);
    if (dot(newDir, newDir) < EPSILON) {
      return true; // origin contained
    }
    direction = newDir;
    if (simplex.length === 4) {
      return true;
    }
  }
  return true; // default to "intersects" on non-termination (conservative)
}
