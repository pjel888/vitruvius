// Vitruvius Sprint RUST-MIG-1 Task 4 — S1 build_spatial_adjacency_edges.
//
// Rust port of `scripts/vitruvius/spatial/spatial_edge_builder.py`
// :: `build_spatial_adjacency_edges`. The Python baseline is a
// pairwise O(n^2) AABB intersection loop — at n=2000 the bench
// harness (AD-036 §4.2) measured wall=350 ms on an 8 GB M2, which
// flagged this as the highest wall-time migration candidate in
// Sprint RUST-MIG-1.
//
// Algorithm (O(n log n + k) expected, where k = emitted edges):
//
//   1. Scan the input once to compute the union bounding box across
//      all AABBs. This becomes the octree root.
//   2. Build a `vitruvius_engine_rs_core::LinearOctree` over the
//      union box. For each input node, insert a SpatialPoint at its
//      AABB centroid, tagged with its index (we rebuild the id later
//      from the input slice — the octree's `SpatialPoint::id` is a
//      `String`, so we store `format!("{idx}")`).
//   3. For each node i, query the octree with node i's AABB via
//      `query_aabb`. The octree returns centroids whose owning boxes
//      *might* intersect node i's box — the octree is a coarse
//      filter over centroid containment, so the returned hit set is
//      a superset of the true AABB overlaps.
//   4. For each hit j, re-run the exact closed-interval AABB overlap
//      test to filter out false positives. Emit `(id_i, id_j)`
//      once per pair by requiring the lexicographic ordering
//      `id_i < id_j` as the stable dedup rule (no HashSet required).
//   5. Return the `Vec<(String, String)>` to the pyo3 shim.
//
// Why the centroid trick works (and how the query box must be
// expanded to stay correct):
//
//   LinearOctree::insert only accepts a `SpatialPoint` (a single
//   3-D coordinate). So we insert one centroid per node, tagged
//   with the node's index. `query_aabb(q)` then returns every
//   *centroid* whose (x,y,z) lies inside q.
//
//   But a centroid inside q does NOT tell us the owning AABB
//   overlaps q — the owner's box could stick out far beyond its
//   centroid. More importantly, the owning AABB of a neighbour
//   may *overlap* node i's AABB while the neighbour's centroid
//   is *outside* node i's AABB (e.g. two touching walls whose
//   centroids sit on opposite sides of the shared face).
//
//   The fix is to expand the query box by `max_half_extent`, the
//   largest half-size across all input boxes on each axis. Any
//   neighbour j whose AABB[j] can possibly intersect AABB[i] must
//   have its centroid within `AABB[i] ± max_half_extent`:
//
//       |centroid_j.x - centroid_i.x| <= half_i.x + half_j.x
//
//   So taking `max_half_extent.x = max over j of half_j.x` and
//   expanding node i's query box by `half_i.x + max_half_extent.x`
//   on each axis guarantees every true-overlap neighbour lands in
//   the octree's candidate set. The full AABB re-test then filters
//   out the false positives.
//
//   Even with the false-positive overhead, the octree's spatial
//   pruning collapses the search from O(n) candidates per node to
//   O(log n + hits). For PD 1096 inputs where box sizes are
//   bounded (max_half_extent is a fixed constant, not a function
//   of n), the expected hit set stays small and the AABB re-test
//   is O(1) per hit. Net complexity: O(n log n + k).
//
// Bug-compatibility contract with the Python baseline:
//
//   * Closed-interval AABB overlap (`max_x >= min_x` on every axis).
//     Touching faces count as adjacent — same as the Python code.
//   * Single input node → empty output.
//   * Empty input → empty output.
//   * The input's AABB representation is `[min_x, min_y, min_z,
//     max_x, max_y, max_z]` in that exact order; the pyo3 shim
//     marshals Python's `SpatialPoint.aabb.min_xyz / max_xyz` into
//     this form before calling into Rust.
//   * NaN/±inf in the AABB is a bug in the Python control plane,
//     not something we defend against here — the Python dataclass
//     accepts anything but the upstream graph validator rejects
//     non-finite geometry before it reaches us. Passing non-finite
//     bounds to `LinearOctree::new` would raise a `LinearOctreeError`
//     which we propagate as an empty edge list (safe fallback).
//
// Dedup ordering note:
//
//   The Python baseline walks `for i in 0..n, for j in i+1..n` and
//   emits `(points[i].id, points[j].id)` — so the emitted ordering
//   depends on input position, NOT lexicographic id order. This
//   port uses lexicographic id ordering instead, because the Rust
//   octree hit list is unsorted and the caller's test compares
//   edge sets as canonicalised unordered pairs (see
//   `test_spatial_edge_builder_parity.py::_edge_pair_set`). The
//   Python fast-path wrapper remaps each returned
//   `(id_i, id_j)` pair into `SpatialEdge(from_id=id_i, to_id=id_j)`
//   so the public API shape is unchanged — only the *ordering* of
//   from/to within each pair differs, and that ordering is not
//   load-bearing for any downstream consumer (the predicate is
//   symmetric: physically_adjacent_to(a, b) iff physically_adjacent_to(b, a)).

use vitruvius_engine_rs_core::{LinearOctree, SpatialPoint, DEFAULT_MAX_DEPTH};

/// Closed-interval AABB overlap test. Mirrors
/// `vitruvius.spatial.spatial_edge_builder._aabbs_intersect`
/// byte-for-byte — touching faces count as adjacent.
#[inline]
fn aabbs_overlap(a: &[f64; 6], b: &[f64; 6]) -> bool {
    // a = [min_x, min_y, min_z, max_x, max_y, max_z]
    // Fail fast if any axis is separable.
    !(a[3] < b[0] || b[3] < a[0] || a[4] < b[1] || b[4] < a[1] || a[5] < b[2] || b[5] < a[2])
}

/// Maximum half-extent per axis across every input box. Used to
/// expand node i's query box so every potentially-overlapping
/// neighbour's centroid is guaranteed to lie inside the expanded
/// query region — see the module-level "Why the centroid trick
/// works" section for the correctness argument.
#[inline]
fn compute_max_half_extent(nodes: &[(String, [f64; 6])]) -> [f64; 3] {
    let mut out = [0.0_f64; 3];
    for (_, b) in nodes.iter() {
        let hx = 0.5 * (b[3] - b[0]);
        let hy = 0.5 * (b[4] - b[1]);
        let hz = 0.5 * (b[5] - b[2]);
        if hx > out[0] {
            out[0] = hx;
        }
        if hy > out[1] {
            out[1] = hy;
        }
        if hz > out[2] {
            out[2] = hz;
        }
    }
    out
}

/// Build the union bounding box across every input AABB. Returns
/// `None` for empty input (the octree cannot be constructed without
/// a valid root box).
fn compute_union_bounds(nodes: &[(String, [f64; 6])]) -> Option<[f64; 6]> {
    let mut it = nodes.iter();
    let first = it.next()?;
    let mut min_x = first.1[0];
    let mut min_y = first.1[1];
    let mut min_z = first.1[2];
    let mut max_x = first.1[3];
    let mut max_y = first.1[4];
    let mut max_z = first.1[5];
    for (_, b) in it {
        if b[0] < min_x {
            min_x = b[0];
        }
        if b[1] < min_y {
            min_y = b[1];
        }
        if b[2] < min_z {
            min_z = b[2];
        }
        if b[3] > max_x {
            max_x = b[3];
        }
        if b[4] > max_y {
            max_y = b[4];
        }
        if b[5] > max_z {
            max_z = b[5];
        }
    }
    // Guarantee non-degenerate bounds — a zero-volume root would
    // still work for `contains()`, but we add a 1.0-unit pad so the
    // octree subdivision has room to split when every input is
    // collinear (an edge case from e.g. a single row of PD 1096
    // columns).
    const PAD: f64 = 1.0;
    Some([
        min_x - PAD,
        min_y - PAD,
        min_z - PAD,
        max_x + PAD,
        max_y + PAD,
        max_z + PAD,
    ])
}

/// Port of `build_spatial_adjacency_edges` from the Python baseline.
///
/// * Input: slice of `(id, aabb)` where `aabb` is
///   `[min_x, min_y, min_z, max_x, max_y, max_z]` closed-interval.
/// * Output: `Vec<(id_i, id_j)>` where `id_i < id_j` lexicographically,
///   one entry per intersecting AABB pair. No duplicates.
///
/// Allocations are bounded: one octree, one hit buffer per query
/// (reused via `Vec::clear()` would require exposing an API the
/// core crate does not have, so we accept a fresh allocation per
/// query — on an 8 GB M2 at n=2000 the allocator cost is negligible
/// compared to the query walk). The output `Vec` is the only
/// caller-visible allocation.
pub fn build_spatial_adjacency_edges(nodes: &[(String, [f64; 6])]) -> Vec<(String, String)> {
    if nodes.len() < 2 {
        return Vec::new();
    }

    let Some(root) = compute_union_bounds(nodes) else {
        return Vec::new();
    };

    // Try to build the octree. If the bounds are degenerate
    // (NaN/inf from the Python caller), fall back to an empty
    // result — silent-empty matches the Python dataclass's
    // permissive-on-bad-input contract.
    let Ok(mut tree) = LinearOctree::new(
        root[0],
        root[1],
        root[2],
        root[3],
        root[4],
        root[5],
        DEFAULT_MAX_DEPTH,
    ) else {
        return Vec::new();
    };

    // Insert each node's centroid tagged with its index.
    // We use the index as a stringified tag so we can re-look-up
    // the full id + box in O(1) during the query phase.
    for (idx, (_id, aabb)) in nodes.iter().enumerate() {
        let cx = 0.5 * (aabb[0] + aabb[3]);
        let cy = 0.5 * (aabb[1] + aabb[4]);
        let cz = 0.5 * (aabb[2] + aabb[5]);
        // Safe to ignore insert errors: we just padded the root
        // box so every centroid is strictly inside. If somehow the
        // centroid is NaN, drop the node — it cannot participate
        // in a real adjacency relation anyway.
        if let Ok(point) = SpatialPoint::new(format!("{idx}"), cx, cy, cz) {
            let _ = tree.insert(point);
        }
    }

    // Compute the maximum half-extent across all boxes — the
    // amount we need to pad each query box by so every potentially
    // overlapping neighbour's centroid is inside the candidate
    // region. (See correctness argument in the module doc.)
    let max_half = compute_max_half_extent(nodes);

    // Tiny epsilon to survive IEEE-754 rounding at the exact-touch
    // boundary (two walls sharing x=1.0). The octree uses closed
    // containment so an epsilon of 0 is already theoretically
    // correct — we add 1e-12 as a belt-and-braces guard against
    // float-cancellation in the half-extent sum.
    const EPS: f64 = 1e-12;

    // For each node, query the tree for candidate neighbours and
    // confirm with the exact AABB re-test. Stable dedup via
    // lexicographic id ordering (`id_i < id_j`).
    let mut out: Vec<(String, String)> = Vec::new();
    for (idx_i, (id_i, aabb_i)) in nodes.iter().enumerate() {
        // Expand the query box by (half_i + max_half) on every axis.
        // This guarantees the centroid of every neighbour j whose
        // AABB can possibly overlap AABB[i] lies inside the query.
        let half_ix = 0.5 * (aabb_i[3] - aabb_i[0]);
        let half_iy = 0.5 * (aabb_i[4] - aabb_i[1]);
        let half_iz = 0.5 * (aabb_i[5] - aabb_i[2]);
        let cx = 0.5 * (aabb_i[0] + aabb_i[3]);
        let cy = 0.5 * (aabb_i[1] + aabb_i[4]);
        let cz = 0.5 * (aabb_i[2] + aabb_i[5]);
        let pad_x = half_ix + max_half[0] + EPS;
        let pad_y = half_iy + max_half[1] + EPS;
        let pad_z = half_iz + max_half[2] + EPS;
        let qx0 = cx - pad_x;
        let qy0 = cy - pad_y;
        let qz0 = cz - pad_z;
        let qx1 = cx + pad_x;
        let qy1 = cy + pad_y;
        let qz1 = cz + pad_z;

        let Ok(hits) = tree.query_aabb(qx0, qy0, qz0, qx1, qy1, qz1) else {
            continue;
        };

        for hit in hits {
            // Parse the tag back to an index. Anything that does
            // not parse was not inserted by us — skip defensively.
            let Ok(idx_j) = hit.id.parse::<usize>() else {
                continue;
            };
            if idx_j == idx_i {
                continue;
            }
            let (id_j, aabb_j) = &nodes[idx_j];

            // Exact AABB re-test — the octree is a coarse filter.
            if !aabbs_overlap(aabb_i, aabb_j) {
                continue;
            }

            // Stable dedup: only emit the pair where the first id
            // is lex-less-than the second. Ties on equal ids are
            // silently dropped (cannot happen with unique node
            // ids, defensive otherwise).
            if id_i < id_j {
                out.push((id_i.clone(), id_j.clone()));
            }
        }
    }

    out
}

// ---------------------------------------------------------------------------
// Unit tests.
// ---------------------------------------------------------------------------

#[cfg(test)]
mod tests {
    use super::*;
    use std::collections::HashSet;

    fn node(id: &str, aabb: [f64; 6]) -> (String, [f64; 6]) {
        (id.to_string(), aabb)
    }

    #[test]
    fn empty_input_returns_empty() {
        let edges = build_spatial_adjacency_edges(&[]);
        assert!(edges.is_empty());
    }

    #[test]
    fn single_node_returns_empty() {
        let nodes = vec![node("solo", [0.0, 0.0, 0.0, 1.0, 1.0, 1.0])];
        let edges = build_spatial_adjacency_edges(&nodes);
        assert!(edges.is_empty());
    }

    #[test]
    fn disjoint_boxes_return_empty() {
        let nodes = vec![
            node("a", [0.0, 0.0, 0.0, 1.0, 1.0, 1.0]),
            node("b", [10.0, 10.0, 10.0, 11.0, 11.0, 11.0]),
        ];
        let edges = build_spatial_adjacency_edges(&nodes);
        assert!(edges.is_empty());
    }

    #[test]
    fn touching_faces_count_as_adjacent() {
        // Walls sharing the x=1.0 plane.
        let nodes = vec![
            node("wall-01", [0.0, 0.0, 0.0, 1.0, 1.0, 1.0]),
            node("wall-02", [1.0, 0.0, 0.0, 2.0, 1.0, 1.0]),
        ];
        let edges = build_spatial_adjacency_edges(&nodes);
        assert_eq!(edges.len(), 1);
        assert_eq!(edges[0], ("wall-01".to_string(), "wall-02".to_string()));
    }

    #[test]
    fn adjacency_edges_emits_edges_for_intersecting_boxes() {
        // 3 boxes, 2 intersecting pairs:
        //   A overlaps B (classic overlap)
        //   B touches C on shared face x=2
        //   A and C are disjoint (A ends at 1, C starts at 2).
        let nodes = vec![
            node("a", [0.0, 0.0, 0.0, 1.0, 1.0, 1.0]),
            node("b", [0.5, 0.5, 0.5, 2.0, 2.0, 2.0]),
            node("c", [2.0, 0.0, 0.0, 3.0, 1.0, 1.0]),
        ];
        let edges = build_spatial_adjacency_edges(&nodes);
        let edge_set: HashSet<(String, String)> = edges.into_iter().collect();
        let expected: HashSet<(String, String)> = [
            ("a".to_string(), "b".to_string()),
            ("b".to_string(), "c".to_string()),
        ]
        .into_iter()
        .collect();
        assert_eq!(edge_set, expected, "expected exactly 2 intersecting pairs");
    }

    #[test]
    fn three_mutually_overlapping_produces_three_pairs() {
        // Mirrors the Python test_three_mutually_overlapping_produces_three_pairs
        // fixture — ids a,b,c all pairwise-overlap, so 3 choose 2 = 3 edges.
        let nodes = vec![
            node("a", [0.0, 0.0, 0.0, 1.0, 1.0, 1.0]),
            node("b", [0.5, 0.5, 0.5, 1.5, 1.5, 1.5]),
            node("c", [0.9, 0.9, 0.9, 2.0, 2.0, 2.0]),
        ];
        let edges = build_spatial_adjacency_edges(&nodes);
        let edge_set: HashSet<(String, String)> = edges.into_iter().collect();
        assert_eq!(edge_set.len(), 3);
        assert!(edge_set.contains(&("a".to_string(), "b".to_string())));
        assert!(edge_set.contains(&("a".to_string(), "c".to_string())));
        assert!(edge_set.contains(&("b".to_string(), "c".to_string())));
    }

    #[test]
    fn duplicate_pairs_are_deduped() {
        // If the octree's query_aabb returned both "a found b" and
        // "b found a", our `id_i < id_j` dedup rule must emit only
        // the single canonical pair. This is a regression guard
        // against an earlier draft that used a HashSet.
        let nodes = vec![
            node("a", [0.0, 0.0, 0.0, 1.0, 1.0, 1.0]),
            node("b", [0.5, 0.5, 0.5, 1.5, 1.5, 1.5]),
        ];
        let edges = build_spatial_adjacency_edges(&nodes);
        assert_eq!(edges.len(), 1);
        assert_eq!(edges[0], ("a".to_string(), "b".to_string()));
    }
}
