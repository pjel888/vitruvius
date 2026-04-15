// Sprint RUST-MIG-1 stats kernels crate — Mahalanobis + sliced Wasserstein.
//
// Task 3 scaffolded this crate with an intentional-red test while
// the gates for Tasks 6 + 7 were still pending. Task 6 (this
// commit) lands N4 `mahalanobis_distance` — a dense quadratic form
// over a cached pseudoinverse covariance — and removes the red
// scaffold test. Task 7 will add `sliced_wasserstein` next to it.
//
// Both modules are pure Rust (no pyo3 dependency); the pyo3 shim in
// `../pyo3_shim/src/lib.rs` wraps each entry point in a
// `#[pyfunction]` so Python callers see a normal function on the
// `vitruvius_engine_rs` extension module.
//
// Dense linalg lives on `nalgebra` (pure Rust, no BLAS link, good
// perf for small-to-medium dims). The 64-dim cov_inv matrix fits
// comfortably in L1 cache on every target we care about, so the
// `DMatrix * DVector` matrix-vector product nalgebra dispatches to
// is already close to the theoretical FMA peak without needing a
// heavier dep like `ndarray-linalg` or BLAS.

pub mod mahalanobis;

pub use mahalanobis::mahalanobis_distance;
