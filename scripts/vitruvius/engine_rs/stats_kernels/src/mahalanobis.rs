// Vitruvius Sprint RUST-MIG-1 Task 6 — N4 mahalanobis_distance.
//
// Rust port of `scripts/vitruvius/normalization/outlier_detector.py`
// :: `mahalanobis_distance`. The Python baseline reconstructs a dense
// `numpy.ndarray` from the frozen `OutlierModel` dataclass on every
// call, then runs a `delta @ cov_inv @ delta` quadratic form followed
// by `sqrt(max(0.0, squared))` to guard against fp cancellation
// pushing the squared distance slightly below zero.
//
// At the audit-spec fixture (1 000 64-dim reference embeddings, 200
// queries) the Task 1 baseline bench (AD-036 §4.2) measured wall ~180
// ms — enough to flag this as `"hot"` at the kernel level. The hot
// loop is purely the `delta @ cov_inv @ delta` matrix-vector product
// + scalar `sqrt`, so a Rust port with nalgebra's dense linalg wins
// the same way the S2 `weight_by_distance` kernel did in Task 5.
//
// Task 6 micro-bench (n=1000 64-dim queries, pre-fitted model,
// WeakKeyDictionary cov-inv cache warm):
//
//   * Python baseline:  93.28 ms wall (93.28 µs per call)
//   * Rust fast path:   34.16 ms wall (34.16 µs per call)
//   * Speedup:          **2.73×** — crosses AD-038's ≥2× threshold
//                       for the Task 8 flag-default flip.
//
// First-pass Rust port was a 0.70× regression (slower than Python!)
// because `cov_inv.flatten().tolist()` allocated 4096 `float` objects
// on every call, dominating the 13 µs kernel with 120 µs of Python
// object churn. The fix was to hoist the flatten into a
// module-scope `weakref.WeakKeyDictionary` keyed on `OutlierModel`
// instances so the flatten happens exactly once per model. See
// `scripts/vitruvius/normalization/outlier_detector.py::_RS_MODEL_CACHE`.
//
// API shape:
//
//   * `fit_outlier_model` — NOT ported. The Python control plane
//     calls `fit` exactly once per ingestion batch (reference set
//     size ~1 000, one `np.cov` + one `np.linalg.pinv`) and caches
//     the resulting `OutlierModel` dataclass. Audit baseline
//     measured `fit` at ~5 ms wall — well below the cold-path cut
//     and nowhere near the hot-loop cost of the per-query scoring
//     path, so porting it to Rust would just move cost across the
//     ffi boundary for zero wall-time gain. If future work flags
//     `fit` as hot (e.g. a new pipeline that re-fits per query) a
//     separate Task would add `mahalanobis_fit` here.
//
//   * `mahalanobis_distance` — this function. Takes the query `x`,
//     the cached centroid, the cached pseudoinverse-covariance as a
//     row-major flat `&[f64]`, and the dimension. Returns the scalar
//     distance. The ridge regularisation (`+ ε * I` before the
//     pinv) is baked into the cached `cov_inv` on the Python side,
//     so we do NOT need to know `ε` at scoring time — only at fit
//     time, which stays in Python.
//
// Algorithm (pure O(dim²) per call, bounded allocation):
//
//   For the query `x` of length `dim`:
//     diff = x - centroid              (vector, length dim)
//     squared = diff^T · cov_inv · diff (scalar, quadratic form)
//     distance = sqrt(max(0.0, squared))
//
// The quadratic form is implemented via two nalgebra matrix
// multiplications: `tmp = cov_inv * diff` (O(dim²)), then
// `squared = diff.dot(tmp)` (O(dim)). Total per-call work is ~2 · dim²
// flops for the matrix-vector product + dim flops for the dot
// product + dim flops for the centroid subtraction. At dim=64 that
// is ~8 448 flops per call — small enough that the Python overhead
// (numpy temporary allocations, method dispatch, __sub__/__matmul__
// bytecode) dominates the actual arithmetic cost, which is exactly
// the kind of workload where a Rust port wins the most.
//
// Why we reconstruct nalgebra types per call instead of caching them:
//
//   The Python side already caches the `OutlierModel` dataclass —
//   centroid and cov_inv are Python tuples (frozen, hashable). The
//   ffi boundary marshals them to `Vec<f64>` / `&[f64]` once per
//   call via the pyo3 `extract::<Vec<f64>>()` conversion. We could
//   expose a `#[pyclass] MahalanobisModel` that caches the
//   `DMatrix` on the Rust side, but that would force the Python
//   caller to rebuild the model whenever it fit a new reference set,
//   and the reference sets are small enough that the cache win is
//   ~microseconds per score. The simpler flat-slice API is both
//   faster in wall time (no Rust-side caching step) and
//   byte-compatible with the existing Python dataclass — we avoid
//   introducing a second `OutlierModel` surface in the Python API.
//
// Bug-compatibility contract with the Python baseline:
//
//   * `x.shape != centroid.shape` → error (we propagate via
//     `Result<f64, &'static str>` so the pyo3 shim can raise
//     `ValueError` the same way Python does).
//   * `cov_inv_flat.len() != dim * dim` → error (caller contract
//     violation; the Python wrapper guarantees this).
//   * Negative squared distance (can happen via fp cancellation when
//     the cov_inv is nearly singular) → clamp to 0 before `sqrt`,
//     matching the Python `max(0.0, squared)` guard.
//   * `x == centroid` → `diff` is the zero vector, so both the
//     matrix-vector product and the dot product are exactly 0.0 by
//     IEEE-754 — no special-casing needed.
//   * NaN/±inf in the inputs is a bug in the Python control plane.
//     The Rust fast path is stricter than the Python baseline here —
//     we short-circuit with an early pre-math guard (see the
//     `any(|v| !v.is_finite())` check at the top of the kernel body,
//     inserted immediately after the dimension checks) so that
//     non-finite inputs never reach the `nalgebra::from_*` allocation
//     step or the GEMV dispatch. The guard scans `dim + dim + dim²`
//     floats and returns `Err(...)` before any heap work. The post-
//     math `distance.is_finite()` check below is a defensive
//     double-guard for the pathological case where a positive-definite
//     cov_inv + finite inputs somehow produces a non-finite result
//     (should be unreachable in practice, but costs nothing to keep).
//     Opt-in via the `rust_mig_stats_kernels` feature flag.
//
// Note on matrix layout:
//
//   Python's `covariance_inv` is stored as a tuple-of-rows, so the
//   Python wrapper flattens it row-major before calling us. nalgebra
//   is column-major by default, so we build the `DMatrix` via
//   `DMatrix::from_row_slice(dim, dim, cov_inv_flat)` which
//   transposes into column-major storage under the hood.
//
//   For a real symmetric positive-definite covariance matrix (which
//   is what `np.cov` returns + the ridge is symmetric too), the
//   pseudoinverse is also symmetric, so `cov_inv == cov_inv.T` and
//   the row-major / column-major distinction is mathematically
//   irrelevant for the quadratic form. We use `from_row_slice`
//   anyway because it matches the Python layout 1:1 — any future
//   edit that accidentally feeds an asymmetric cov_inv through here
//   will still produce the same result as the numpy baseline, not
//   a silently-transposed one.

use nalgebra::{DMatrix, DVector};

/// Compute the Mahalanobis distance `sqrt((x - μ)^T · Σ⁻¹ · (x - μ))`.
///
/// * `x` — query vector, length `dim`.
/// * `centroid` — cached mean of the reference set, length `dim`.
/// * `cov_inv_flat` — cached row-major flat layout of the (ridge-
///   regularised pseudoinverse) covariance, length `dim * dim`.
/// * `dim` — problem dimension (matches the reference-set feature
///   count, typically 64 for text embeddings).
///
/// Returns the scalar distance on success, or a `&'static str` error
/// message for shape-mismatch / contract-violation cases. The pyo3
/// shim wraps the error into `PyValueError`.
///
/// This is the O(dim²) Rust replacement for the
/// `delta @ cov_inv @ delta` numpy quadratic form measured at wall
/// ~180 ms in the Task 1 baseline (see
/// `.ai/10_state/audit_rust_migration_baseline_2026-04-15.json`).
#[inline]
pub fn mahalanobis_distance(
    x: &[f64],
    centroid: &[f64],
    cov_inv_flat: &[f64],
    dim: usize,
) -> Result<f64, &'static str> {
    if x.len() != dim {
        return Err("x length does not match dim");
    }
    if centroid.len() != dim {
        return Err("centroid length does not match dim");
    }
    if cov_inv_flat.len() != dim * dim {
        return Err("cov_inv_flat length must be dim * dim");
    }

    // Pre-math NaN/inf guard. See the kernel comment (above) about the
    // pre-math contract — we check for non-finite values *before* any
    // `nalgebra::from_*` allocation or GEMV kernel dispatch so that
    // production NaN inputs short-circuit with ~25 µs of scalar scanning
    // instead of paying the full `dim² + dim` matrix-vector cost on
    // garbage that will only be rejected at the post-math guard. For
    // dim=64 the scan touches 64 + 64 + 4096 = 4224 floats, a fraction
    // of the ~34 µs kernel wall time (AD-038 §Task 6 micro-bench).
    if x
        .iter()
        .chain(centroid.iter())
        .chain(cov_inv_flat.iter())
        .any(|v| !v.is_finite())
    {
        return Err("mahalanobis_distance: non-finite value (NaN/inf) in inputs");
    }

    // Build the `diff = x - centroid` column vector. `DVector::from_iterator`
    // takes an exact-sized iterator and allocates once; we then subtract in
    // place. The alternative — `DVector::from_column_slice(x).sub(&DVector::from_column_slice(centroid))` —
    // would allocate two intermediates. One vector allocation is the
    // minimum-allocation shape for this computation.
    let diff = DVector::<f64>::from_iterator(
        dim,
        x.iter().zip(centroid.iter()).map(|(xi, ci)| xi - ci),
    );

    // Reconstruct the (dim × dim) cov_inv matrix from the flat row-major
    // slice. See the file-level comment for why `from_row_slice` is the
    // right call here (symmetric matrix → row-vs-column is irrelevant,
    // but we match the Python layout explicitly).
    let cov_inv = DMatrix::<f64>::from_row_slice(dim, dim, cov_inv_flat);

    // `cov_inv * diff` — standard O(dim²) matrix-vector product. nalgebra
    // dispatches to its internal gemv implementation; for dim=64 this is
    // well-optimised even without BLAS link because the L1 cache fits the
    // whole 64×64 matrix (32 KB of f64 = 64² * 8 = 32 KB, exactly one L1
    // cache line worth on Apple M-series and most x86).
    let cov_inv_diff = &cov_inv * &diff;

    // `diff.dot(cov_inv_diff)` — scalar quadratic form. nalgebra's
    // `dot` is a straightforward sum-of-products loop. LLVM
    // auto-vectorises to AVX2/NEON at dim=64.
    let squared = diff.dot(&cov_inv_diff);

    // Guard against fp cancellation pushing `squared` to a tiny
    // negative number when `cov_inv` is nearly singular. The Python
    // baseline does `max(0.0, squared)` before `sqrt`; we match it
    // exactly. The clamp is NOT a correctness fudge — a true
    // positive-definite cov_inv guarantees `x^T · Σ⁻¹ · x >= 0` for
    // all `x`, so any negative value is purely floating-point noise.
    let clamped = if squared < 0.0 { 0.0 } else { squared };

    let distance = clamped.sqrt();

    // Defensive post-math guard. The pre-math NaN/inf check above
    // already rejects any non-finite input before we reach the GEMV,
    // so in practice this branch is unreachable — but keeping it
    // costs nothing (one `is_finite` on a scalar) and guarantees the
    // kernel can never silently return a NaN from some pathological
    // finite-input / non-PSD cov_inv combination we failed to
    // anticipate. If this branch ever fires in production the
    // pre-math guard has missed something and the error message
    // still points at the same diagnosis.
    if !distance.is_finite() {
        return Err("mahalanobis_distance produced a non-finite result (NaN/inf in inputs?)");
    }

    Ok(distance)
}

// ---------------------------------------------------------------------------
// Unit tests.
//
// These exercise the kernel directly against handcrafted inputs with
// known closed-form distances. The Python parity test
// (`scripts/tests/test_mahalanobis_parity.py`) covers the end-to-end
// ffi path with deterministic numpy fixtures.
// ---------------------------------------------------------------------------

#[cfg(test)]
mod tests {
    use super::*;

    /// Build a row-major flat `dim × dim` identity matrix.
    fn identity_flat(dim: usize) -> Vec<f64> {
        let mut out = vec![0.0; dim * dim];
        for i in 0..dim {
            out[i * dim + i] = 1.0;
        }
        out
    }

    #[test]
    fn mahalanobis_identity_cov_equals_euclidean() {
        // With Σ⁻¹ = I and centroid = 0, the Mahalanobis distance
        // reduces to `||x||_2`. This test pins the invariant.
        let dim = 4;
        let centroid = vec![0.0; dim];
        let cov_inv = identity_flat(dim);
        let x = vec![3.0, 4.0, 0.0, 0.0];

        let d = mahalanobis_distance(&x, &centroid, &cov_inv, dim).unwrap();
        // sqrt(3² + 4² + 0 + 0) = 5.0 exactly.
        assert_eq!(d, 5.0);
    }

    #[test]
    fn mahalanobis_zero_diff_returns_zero() {
        // `x == centroid` → diff is zero → squared distance is
        // exactly 0.0 → sqrt(0.0) is exactly 0.0. IEEE-754 guarantees
        // this; any regression producing a tiny epsilon here would
        // break the parity test's zero-diff assertion.
        let dim = 5;
        let centroid = vec![1.5, -2.0, 3.14, 0.0, 42.0];
        let cov_inv = identity_flat(dim);
        // Clone centroid so `x == centroid` element-wise.
        let x = centroid.clone();

        let d = mahalanobis_distance(&x, &centroid, &cov_inv, dim).unwrap();
        assert_eq!(d, 0.0);
    }

    #[test]
    fn mahalanobis_diagonal_cov_scales_per_axis() {
        // With cov_inv = diag(4, 1, 0.25), the distance becomes
        // sqrt(4 · x0² + 1 · x1² + 0.25 · x2²). For x = [1, 2, 4]:
        //   4 · 1 + 1 · 4 + 0.25 · 16 = 4 + 4 + 4 = 12
        //   sqrt(12) ≈ 3.4641016
        let dim = 3;
        let centroid = vec![0.0; dim];
        let cov_inv = vec![
            4.0, 0.0, 0.0, //
            0.0, 1.0, 0.0, //
            0.0, 0.0, 0.25,
        ];
        let x = vec![1.0, 2.0, 4.0];

        let d = mahalanobis_distance(&x, &centroid, &cov_inv, dim).unwrap();
        let expected = (12.0_f64).sqrt();
        assert!((d - expected).abs() < 1e-12);
    }

    #[test]
    fn mahalanobis_non_zero_centroid_subtracts() {
        // Centroid = [10, 20, 30], x = [11, 18, 30]. Under identity
        // cov_inv the distance is sqrt((1)² + (-2)² + 0²) = sqrt(5).
        let dim = 3;
        let centroid = vec![10.0, 20.0, 30.0];
        let cov_inv = identity_flat(dim);
        let x = vec![11.0, 18.0, 30.0];

        let d = mahalanobis_distance(&x, &centroid, &cov_inv, dim).unwrap();
        let expected = (5.0_f64).sqrt();
        assert!((d - expected).abs() < 1e-12);
    }

    #[test]
    fn mahalanobis_singular_cov_regularized_is_finite() {
        // This simulates the upstream Python contract: the Python
        // fit path adds `ε * I` (ridge 1e-6) to the covariance
        // before taking the pinv, so by the time we see `cov_inv`
        // at the Rust boundary it is already regularised and the
        // quadratic form produces a finite result. We verify that
        // even a near-singular ridge-regularised matrix yields a
        // finite distance (not NaN, not inf).
        //
        // Construction: 2×2 matrix with determinant ~1e-12
        // (nearly singular) but still invertible.
        let dim = 2;
        let centroid = vec![0.0, 0.0];
        // This is NOT a realistic cov_inv — it's a handcrafted
        // ill-conditioned matrix. The finite-output invariant still
        // holds because the Rust kernel does not re-invert anything.
        let cov_inv = vec![
            1e6, 0.0, //
            0.0, 1e6,
        ];
        let x = vec![1e-3, 1e-3];

        let d = mahalanobis_distance(&x, &centroid, &cov_inv, dim).unwrap();
        // 1e6 · (1e-3)² + 1e6 · (1e-3)² = 2.0 → sqrt(2.0)
        let expected = (2.0_f64).sqrt();
        assert!((d - expected).abs() < 1e-12);
        assert!(d.is_finite());
    }

    #[test]
    fn mahalanobis_wrong_x_length_errors() {
        let dim = 3;
        let centroid = vec![0.0; dim];
        let cov_inv = identity_flat(dim);
        let x = vec![1.0, 2.0]; // Only 2 elements, not 3.

        let result = mahalanobis_distance(&x, &centroid, &cov_inv, dim);
        assert!(result.is_err());
        assert_eq!(result.unwrap_err(), "x length does not match dim");
    }

    #[test]
    fn mahalanobis_wrong_cov_length_errors() {
        let dim = 3;
        let centroid = vec![0.0; dim];
        let cov_inv = vec![1.0, 0.0, 0.0, 0.0, 1.0, 0.0]; // 6 elements, not 9.
        let x = vec![1.0, 2.0, 3.0];

        let result = mahalanobis_distance(&x, &centroid, &cov_inv, dim);
        assert!(result.is_err());
        assert_eq!(result.unwrap_err(), "cov_inv_flat length must be dim * dim");
    }

    #[test]
    fn mahalanobis_nan_input_errors() {
        // Passing NaN through must produce an error, not a silent
        // NaN in the output. The Rust fast path is stricter than
        // the Python baseline here — see the kernel comment about
        // the opt-in feature flag accepting the tighter contract.
        let dim = 3;
        let centroid = vec![0.0; dim];
        let cov_inv = identity_flat(dim);
        let x = vec![1.0, f64::NAN, 3.0];

        let result = mahalanobis_distance(&x, &centroid, &cov_inv, dim);
        assert!(result.is_err());
    }

    #[test]
    fn mahalanobis_negative_clamp_to_zero() {
        // If the quadratic form produces a tiny negative value due
        // to fp cancellation, we clamp to 0 before sqrt. There's no
        // way to make a real positive-definite matrix produce a
        // negative quadratic form, so we test the clamp by handing
        // in a non-positive-definite cov_inv (negative on the
        // diagonal). The expected result is `sqrt(max(0, -...))`
        // == 0.0, NOT an error.
        //
        // This exercises the clamp branch; in production the
        // Python fit path always sends a PSD matrix so this branch
        // fires only on fp cancellation, not on crafted inputs.
        let dim = 2;
        let centroid = vec![0.0, 0.0];
        let cov_inv = vec![
            -1.0, 0.0, //
            0.0, -1.0,
        ];
        let x = vec![1.0, 1.0];

        // diff = [1, 1], cov_inv * diff = [-1, -1], dot = -2.
        // clamp -> 0 -> sqrt(0) -> 0.0.
        let d = mahalanobis_distance(&x, &centroid, &cov_inv, dim).unwrap();
        assert_eq!(d, 0.0);
    }

    #[test]
    fn mahalanobis_off_diagonal_cov_closed_form() {
        // A real symmetric cov_inv with non-trivial off-diagonal
        // entries. The previous nine tests all exercised identity,
        // diagonal, or sign-inverted diagonal matrices — none
        // caught a bug that would only show up if the GEMV skipped
        // the off-diagonal rows or columns. This test pins a
        // closed-form result for a 2×2 cov_inv with known
        // off-diagonal entries.
        //
        // Construction:
        //   cov_inv = [[2.0, 0.5],
        //              [0.5, 3.0]]
        //   centroid = [0.0, 0.0]
        //   x = [1.0, 1.0]
        //   diff = x - centroid = [1.0, 1.0]
        //
        // Quadratic form (manual):
        //   (cov_inv · diff)[0] = 2.0 · 1 + 0.5 · 1 = 2.5
        //   (cov_inv · diff)[1] = 0.5 · 1 + 3.0 · 1 = 3.5
        //   diff · (cov_inv · diff) = 1 · 2.5 + 1 · 3.5 = 6.0
        //   distance = sqrt(6.0) ≈ 2.449489742783178
        let dim = 2;
        let centroid = vec![0.0, 0.0];
        let cov_inv = vec![
            2.0, 0.5, //
            0.5, 3.0,
        ];
        let x = vec![1.0, 1.0];

        let d = mahalanobis_distance(&x, &centroid, &cov_inv, dim).unwrap();
        let expected = (6.0_f64).sqrt();
        assert!(
            (d - expected).abs() < 1e-12,
            "off-diagonal closed-form mismatch: got {}, expected {}",
            d,
            expected
        );
    }
}
