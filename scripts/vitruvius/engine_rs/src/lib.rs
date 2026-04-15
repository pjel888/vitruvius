// Vitruvius Sprint GT — Streams GT.1 + GT.2
//
// GT.1 — Binary Data Plane (pyo3 Rust/Python bridge): expose `SpatialPoint`
//        and `LinearOctree` as `#[pyclass]` types so the Python control
//        plane can stream geometry into Rust without CFFI glue.
//
// GT.2 — Sparse Linear Octree Engine: cache-friendly recursive octree
//        backed by a flat `Vec<SpatialPoint>` per leaf. The root AABB is
//        split into eight octants at every level until `max_depth` or
//        until a node holds ≤ `LEAF_CAPACITY` points. Point, sphere, and
//        axis-aligned-box queries walk the tree and prune any octant
//        whose bounds do not intersect the query volume — i.e. the
//        O(log n) spatial indexing the plan calls for.
//
// The narrow GT.1 + GT.2 ship deliberately defers FlatBuffers/Arrow/SIMD.
// That optimisation can land in a follow-on commit; the test bar for this
// commit is correctness of the pyo3 bridge and the recursive octree walk.

use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;

mod octree;

pub use octree::{Aabb, LinearOctree, SpatialPoint};

/// Python module entry point. Maturin wires this up via the
/// `#[pymodule]` macro so `import vitruvius_engine_rs` in CPython
/// resolves to this compiled extension.
#[pymodule]
fn vitruvius_engine_rs(py: Python<'_>, m: &Bound<'_, PyModule>) -> PyResult<()> {
    // GT.1 types — exposed so the Python control plane can construct and
    // consume them directly.
    m.add_class::<SpatialPoint>()?;
    m.add_class::<LinearOctree>()?;

    // Module metadata. Users can `print(vitruvius_engine_rs.__version__)`
    // to confirm the ABI matches what Python expects, which helps diagnose
    // stale `.so` files after a rebuild.
    m.add("__version__", env!("CARGO_PKG_VERSION"))?;
    m.add("__doc__", "Vitruvius Sprint GT Rust data plane.")?;

    // Defensive: surface a module-level alias for the sprint codename so
    // downstream tooling can sanity-check they imported the right crate.
    m.add("SPRINT_CODENAME", "GT.1+GT.2")?;

    // Suppress unused-py-arg warning on newer pyo3 without needing a
    // separate `_py` binding in the signature.
    let _ = py;
    Ok(())
}

/// Internal helper for error-path conversion — not exported to Python.
/// Kept here so `lib.rs` owns the conversion policy and `octree.rs`
/// stays free of pyo3 error types except where unavoidable.
pub(crate) fn value_error(msg: impl Into<String>) -> PyErr {
    PyValueError::new_err(msg.into())
}
