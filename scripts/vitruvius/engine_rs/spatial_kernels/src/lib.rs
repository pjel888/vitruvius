// Sprint RUST-MIG-1 spatial kernels crate — AABB-pairwise + distance-decay ports.
//
// Task 4: S1 `build_spatial_adjacency_edges` — O(n^2) pairwise AABB
// intersection → O(n log n) octree-backed adjacency builder. Reuses
// `vitruvius_engine_rs_core::LinearOctree` / `query_aabb`.
//
// Task 5 (this commit): S2 `weight_by_distance` — pure O(n) exponential
// distance decay over seed centroids. No octree, no heap beyond the
// output `Vec`. Sits next to `adjacency_edges` in the same crate so
// the Python shim has a single `vitruvius_spatial_kernels` dep.
//
// All modules are pure Rust (no pyo3 dependency); the pyo3 shim in
// `../pyo3_shim/src/lib.rs` wraps each entry point in a `#[pyfunction]`
// so Python callers see a normal function on the `vitruvius_engine_rs`
// extension module.

pub mod adjacency_edges;
pub mod distance_weight;

pub use adjacency_edges::build_spatial_adjacency_edges;
pub use distance_weight::weight_by_distance;
