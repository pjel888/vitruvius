// Vitruvius Sprint GT/HP — pure core spatial math crate.
//
// This crate owns the spatial types (SpatialPoint, Aabb, LinearOctree)
// with NO pyo3 dependency, so it compiles to:
//
//   * native (aarch64-apple-darwin / x86_64-unknown-linux-gnu / ...) — consumed
//     as an `rlib` by the sibling `pyo3_shim` crate which wraps each
//     struct in a `#[pyclass]` newtype and re-exports them to Python.
//   * wasm32-unknown-unknown — Sprint HP Stream HP.4 ships a thin
//     `#[no_mangle] extern "C"` surface (see `wasm_api` module below)
//     that the browser / wasmtime can call without bundling CPython.
//
// The split is the TDD-expanded version of statistical plan §S4: keep
// the spatial math pure so it can travel to any compile target, and
// push binding code (pyo3, wasm) out to thin shims.
//
// The narrow HP.4 ship exports ONE wasm function: `aabb_intersects`,
// which proves the Python ↔ Wasm roundtrip end-to-end. Richer octree
// exports (insert / query) can land in a follow-on commit.

mod octree;
mod wasm_api;

pub use octree::{
    Aabb, AabbError, LinearOctree, LinearOctreeError, SpatialPoint, DEFAULT_MAX_DEPTH,
};

// Re-export the wasm entry points at the crate root so downstream
// tooling (wasmtime, wasm-bindgen, etc.) can find them by name.
pub use wasm_api::aabb_intersects;
