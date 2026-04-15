// Vitruvius Sprint GT Streams GT.1 + GT.2 — pyo3 shim.
//
// Post-HP.4 workspace split: this crate is a thin wrapper around
// `vitruvius_engine_rs_core`, exposing each pure-Rust type as a
// `#[pyclass]` newtype so Python's public surface stays unchanged.
//
// The split lets the `core` crate target wasm32-unknown-unknown for
// Sprint HP Stream HP.4, while this crate keeps the libpython link
// policy that maturin needs.

use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;

use vitruvius_engine_rs_core as core;

// ---------------------------------------------------------------------------
// SpatialPoint — pyo3 newtype wrapper over core::SpatialPoint.
//
// Field access (`.id`, `.x`, `.y`, `.z`) uses `#[getter]` methods to
// copy values out of the inner struct. That keeps the Python-visible
// API identical to the pre-split pyo3 `#[pyo3(get)]` version.
// ---------------------------------------------------------------------------

/// A single point in 3-space with an opaque identifier.
#[pyclass(module = "vitruvius_engine_rs", frozen)]
#[derive(Clone, Debug)]
pub struct SpatialPoint {
    pub(crate) inner: core::SpatialPoint,
}

impl SpatialPoint {
    fn wrap(inner: core::SpatialPoint) -> Self {
        Self { inner }
    }
}

#[pymethods]
impl SpatialPoint {
    #[new]
    #[pyo3(signature = (id, x, y, z))]
    pub fn new(id: String, x: f64, y: f64, z: f64) -> PyResult<Self> {
        core::SpatialPoint::new(id, x, y, z)
            .map(Self::wrap)
            .map_err(PyValueError::new_err)
    }

    #[getter]
    fn id(&self) -> &str {
        &self.inner.id
    }

    #[getter]
    fn x(&self) -> f64 {
        self.inner.x
    }

    #[getter]
    fn y(&self) -> f64 {
        self.inner.y
    }

    #[getter]
    fn z(&self) -> f64 {
        self.inner.z
    }

    fn __repr__(&self) -> String {
        format!(
            "SpatialPoint(id={:?}, x={}, y={}, z={})",
            self.inner.id, self.inner.x, self.inner.y, self.inner.z
        )
    }

    /// Equality check — matches the pre-split Python API.
    fn __eq__(&self, other: &Self) -> bool {
        self.inner == other.inner
    }
}

// ---------------------------------------------------------------------------
// LinearOctree — pyo3 newtype wrapper over core::LinearOctree.
// ---------------------------------------------------------------------------

/// Sparse linear octree over `SpatialPoint` records.
#[pyclass(module = "vitruvius_engine_rs")]
pub struct LinearOctree {
    inner: core::LinearOctree,
}

#[pymethods]
impl LinearOctree {
    #[new]
    #[pyo3(signature = (
        min_x, min_y, min_z, max_x, max_y, max_z,
        max_depth = core::DEFAULT_MAX_DEPTH
    ))]
    pub fn new(
        min_x: f64,
        min_y: f64,
        min_z: f64,
        max_x: f64,
        max_y: f64,
        max_z: f64,
        max_depth: usize,
    ) -> PyResult<Self> {
        core::LinearOctree::new(min_x, min_y, min_z, max_x, max_y, max_z, max_depth)
            .map(|inner| Self { inner })
            .map_err(PyValueError::new_err)
    }

    /// Insert a point into the octree.
    ///
    /// Accepts either a `SpatialPoint` or a 4-tuple `(id, x, y, z)`.
    #[pyo3(signature = (point))]
    pub fn insert(&mut self, point: &Bound<'_, PyAny>) -> PyResult<()> {
        let sp = coerce_spatial_point(point)?;
        self.inner.insert(sp).map_err(PyValueError::new_err)
    }

    pub fn __len__(&self) -> usize {
        self.inner.total()
    }

    pub fn len(&self) -> usize {
        self.inner.total()
    }

    pub fn live_count(&self) -> usize {
        self.inner.live_count()
    }

    #[getter]
    pub fn max_depth(&self) -> usize {
        self.inner.max_depth()
    }

    #[getter]
    pub fn bounds(&self) -> (f64, f64, f64, f64, f64, f64) {
        self.inner.bounds_tuple()
    }

    #[pyo3(signature = (min_x, min_y, min_z, max_x, max_y, max_z))]
    pub fn query_aabb(
        &self,
        min_x: f64,
        min_y: f64,
        min_z: f64,
        max_x: f64,
        max_y: f64,
        max_z: f64,
    ) -> PyResult<Vec<SpatialPoint>> {
        self.inner
            .query_aabb(min_x, min_y, min_z, max_x, max_y, max_z)
            .map(|points| points.into_iter().map(SpatialPoint::wrap).collect())
            .map_err(PyValueError::new_err)
    }

    #[pyo3(signature = (cx, cy, cz, radius))]
    pub fn query_sphere(
        &self,
        cx: f64,
        cy: f64,
        cz: f64,
        radius: f64,
    ) -> PyResult<Vec<SpatialPoint>> {
        self.inner
            .query_sphere(cx, cy, cz, radius)
            .map(|points| points.into_iter().map(SpatialPoint::wrap).collect())
            .map_err(PyValueError::new_err)
    }

    /// Alias for `query_sphere` — plan-spec name for the point-query
    /// entry point.
    #[pyo3(signature = (x, y, z, radius))]
    pub fn query_point(
        &self,
        x: f64,
        y: f64,
        z: f64,
        radius: f64,
    ) -> PyResult<Vec<SpatialPoint>> {
        self.query_sphere(x, y, z, radius)
    }

    fn __repr__(&self) -> String {
        let (a, b, c, d, e, f) = self.bounds();
        format!(
            "LinearOctree(bounds=({a}, {b}, {c}, {d}, {e}, {f}), max_depth={}, len={})",
            self.inner.max_depth(),
            self.inner.total()
        )
    }
}

/// Accept either `SpatialPoint` or `(id, x, y, z)` on the insert path.
fn coerce_spatial_point(value: &Bound<'_, PyAny>) -> PyResult<core::SpatialPoint> {
    if let Ok(sp) = value.extract::<SpatialPoint>() {
        return Ok(sp.inner);
    }
    if let Ok((id, x, y, z)) = value.extract::<(String, f64, f64, f64)>() {
        return core::SpatialPoint::new(id, x, y, z).map_err(PyValueError::new_err);
    }
    Err(PyValueError::new_err(
        "insert() expected a SpatialPoint or (id, x, y, z) tuple",
    ))
}

// ---------------------------------------------------------------------------
// Module entry point.
// ---------------------------------------------------------------------------

#[pymodule]
fn vitruvius_engine_rs(py: Python<'_>, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<SpatialPoint>()?;
    m.add_class::<LinearOctree>()?;

    m.add("__version__", env!("CARGO_PKG_VERSION"))?;
    m.add("__doc__", "Vitruvius Sprint GT Rust data plane.")?;
    m.add("SPRINT_CODENAME", "GT.1+GT.2")?;

    let _ = py;
    Ok(())
}
