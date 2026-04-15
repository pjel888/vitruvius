// Sprint RUST-MIG-1 spatial kernels crate — AABB-pairwise + distance-decay ports.
//
// Task 4 (this commit): S1 `build_spatial_adjacency_edges` — O(n^2) pairwise
// AABB intersection → O(n log n) octree-backed adjacency builder. Reuses
// `vitruvius_engine_rs_core::LinearOctree` / `query_aabb`.
//
// Task 5 (next): S2 `weight_by_distance` — exponential distance decay
// over seed centroids. Will land in this crate next to `adjacency_edges`.
//
// Both modules are pure Rust (no pyo3 dependency); the pyo3 shim in
// `../pyo3_shim/src/lib.rs` wraps each entry point in a `#[pyfunction]`
// so Python callers see a normal function on the `vitruvius_engine_rs`
// extension module.

pub mod adjacency_edges;

pub use adjacency_edges::build_spatial_adjacency_edges;
