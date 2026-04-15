// Vitruvius Sprint RUST-MIG-1 Task 5 — S2 weight_by_distance.
//
// Rust port of `scripts/vitruvius/spatial/proximity_jump.py`
// :: `weight_by_distance`. The Python baseline is a dense O(n) loop
// over the seed centroids computing `exp(-lambda_decay * euclidean_distance)`
// for each seed against a single focal point. At n=10 000 the Task 1
// baseline bench (AD-036 §4.2) measured wall ~70 ms — enough to flag
// it as `"hot"` even though it is dwarfed by S1, because the pipeline
// calls it once per GraphRAG chain invocation on every query.
//
// Algorithm (pure O(n), zero allocations beyond the output `Vec`):
//
//   For each seed `(x, y, z)`:
//     dx = x - focal.0
//     dy = y - focal.1
//     dz = z - focal.2
//     d  = sqrt(dx*dx + dy*dy + dz*dz)
//     w  = exp(-lambda_decay * d)
//     push w onto the output vec
//
// No octree, no spatial index, no per-pair bookkeeping. The work is
// linear in the number of seeds and every iteration is independent,
// so this is trivially vectorisable by LLVM's auto-vectoriser on
// AVX2/NEON targets — we stay out of its way by writing the loop as
// `seeds.iter().map(...).collect()` (idiomatic slice-map that the
// compiler is happiest optimising). No ndarray/no BLAS dependency —
// `&[(f64, f64, f64)]` is sufficient because the Python caller
// marshals its `dict[str, tuple[...]]` into tuples once at the ffi
// boundary.
//
// Bug-compatibility contract with the Python baseline:
//
//   * Return type is a `Vec<f64>` in the **same order** as the input
//     slice. The pyo3 shim returns it to Python as a list which the
//     caller zips against the original seed-id key order to rebuild
//     the `dict[str, float]` — order preservation is load-bearing so
//     we MUST NOT reorder.
//   * `d == 0.0` (seed at focal) → `exp(0) == 1.0` exactly. IEEE-754
//     guarantees this; no special-casing needed.
//   * `lambda_decay == 0.0` → `exp(-0.0) == 1.0` for every seed. Also
//     handled by the natural IEEE-754 path.
//   * Empty input → empty output. The `.collect()` of an empty iter
//     produces `Vec::new()` with zero allocation, matching the
//     Python `{}`-returns-`{}` contract at the ffi layer.
//   * NaN/±inf in the seed coordinates is a bug in the Python control
//     plane, not something we defend against. `sqrt` and `exp` will
//     propagate NaN-in-NaN-out if the caller sends garbage, which is
//     byte-identical to the Python `math.sqrt`/`math.exp` behaviour.
//
// Why the formula is written as `(-lambda_decay * d).exp()` and not
// `(-lambda_decay).exp() * d.exp().recip()`:
//
//   The two forms are mathematically equivalent but the former is
//   one `exp` call per seed, the latter is two. LLVM cannot CSE
//   across the multiplication here because the intermediate result
//   depends on the loop index, so writing the naive `exp(-λd)` form
//   is both shortest and fastest.

/// Compute `exp(-lambda_decay * d)` for each seed, where `d` is the
/// Euclidean distance from the seed to `focal`.
///
/// * Input: slice of `(x, y, z)` seed coordinates in any order.
/// * Input: `focal` as an `(x, y, z)` tuple in the same frame.
/// * Input: `lambda_decay` — the exponential-decay coefficient. Must
///   be non-negative in practice but the kernel does not enforce it
///   (a negative lambda yields weights > 1, which is the Python
///   baseline's behaviour as well — we preserve the contract).
/// * Output: `Vec<f64>` in the same order as the input slice, one
///   weight per seed.
///
/// This is the O(n) Rust replacement for the Python loop measured at
/// ~70 ms wall time at n=10 000 in the Task 1 baseline (see
/// `.ai/10_state/audit_rust_migration_baseline_2026-04-15.json`).
#[inline]
pub fn weight_by_distance(
    seeds: &[(f64, f64, f64)],
    focal: (f64, f64, f64),
    lambda_decay: f64,
) -> Vec<f64> {
    let (fx, fy, fz) = focal;
    seeds
        .iter()
        .map(|&(x, y, z)| {
            let dx = x - fx;
            let dy = y - fy;
            let dz = z - fz;
            let d = (dx * dx + dy * dy + dz * dz).sqrt();
            (-lambda_decay * d).exp()
        })
        .collect()
}

// ---------------------------------------------------------------------------
// Unit tests.
// ---------------------------------------------------------------------------

#[cfg(test)]
mod tests {
    use super::*;

    const FOCAL: (f64, f64, f64) = (50.0, 50.0, 50.0);
    const LAMBDA: f64 = 0.05;

    #[test]
    fn weight_by_distance_empty_seeds_returns_empty() {
        let out = weight_by_distance(&[], FOCAL, LAMBDA);
        assert!(out.is_empty());
    }

    #[test]
    fn weight_by_distance_zero_distance_is_one() {
        // A seed sitting AT the focal point must score exactly 1.0
        // (IEEE-754 guarantees `exp(-0.0 * 0.0) == 1.0` exactly).
        let seeds = [FOCAL];
        let out = weight_by_distance(&seeds, FOCAL, LAMBDA);
        assert_eq!(out.len(), 1);
        assert_eq!(out[0], 1.0);
    }

    #[test]
    fn weight_by_distance_monotonically_decreasing() {
        // Farther seeds must produce strictly smaller weights —
        // this is the defining property of the decay function and
        // any regression that breaks it (e.g. losing the sqrt) is
        // caught here.
        let near: (f64, f64, f64) = (50.0, 50.0, 51.0); // d = 1.0
        let mid: (f64, f64, f64) = (50.0, 50.0, 55.0); // d = 5.0
        let far: (f64, f64, f64) = (50.0, 50.0, 100.0); // d = 50.0
        let seeds = [near, mid, far];
        let out = weight_by_distance(&seeds, FOCAL, LAMBDA);
        assert_eq!(out.len(), 3);
        assert!(out[0] > out[1], "near ({}) must exceed mid ({})", out[0], out[1]);
        assert!(out[1] > out[2], "mid ({}) must exceed far ({})", out[1], out[2]);
        // Analytic spot-check: exp(-0.05 * 1.0) ~= 0.9512.
        let expected_near = (-LAMBDA * 1.0_f64).exp();
        assert!((out[0] - expected_near).abs() < 1e-15);
        // All weights must be strictly positive and <= 1.0.
        for w in &out {
            assert!(*w > 0.0);
            assert!(*w <= 1.0);
        }
    }

    #[test]
    fn weight_by_distance_lambda_zero_returns_ones() {
        // λ = 0 means no decay at all → exp(-0 * d) == exp(0) == 1.0
        // for every seed, regardless of distance. This is important
        // for GraphRAG callers that want to disable weighting without
        // a code-path change.
        let seeds = [
            (0.0, 0.0, 0.0),
            (100.0, 100.0, 100.0),
            (-50.0, 73.0, 42.0),
        ];
        let out = weight_by_distance(&seeds, FOCAL, 0.0);
        assert_eq!(out.len(), 3);
        for w in &out {
            assert_eq!(*w, 1.0);
        }
    }

    #[test]
    fn weight_by_distance_order_is_preserved() {
        // The caller re-zips the returned Vec against its original
        // seed-id key order to rebuild the dict, so order preservation
        // is load-bearing. This test catches any future refactor that
        // might try to sort or parallel-reorder the output.
        let seeds = [
            (51.0, 50.0, 50.0), // d = 1.0  -> ~0.9512
            (60.0, 50.0, 50.0), // d = 10.0 -> ~0.6065
            (50.5, 50.0, 50.0), // d = 0.5  -> ~0.9753
        ];
        let out = weight_by_distance(&seeds, FOCAL, LAMBDA);
        assert_eq!(out.len(), 3);
        // Middle seed is the farthest -> smallest weight.
        assert!(out[1] < out[0]);
        assert!(out[1] < out[2]);
        // Third seed is the nearest -> largest weight.
        assert!(out[2] > out[0]);
    }

    #[test]
    fn weight_by_distance_large_distance_is_finite_positive() {
        // exp(-0.05 * 1000) ~= 1.93e-22 — well away from subnormal
        // but the test guards against a regression that accidentally
        // zeros out very small weights or triggers NaN via
        // catastrophic cancellation in the sqrt argument.
        let far = (1050.0, 50.0, 50.0); // d = 1000.0
        let out = weight_by_distance(&[far], FOCAL, LAMBDA);
        assert_eq!(out.len(), 1);
        assert!(out[0] > 0.0);
        assert!(out[0] < 1.0);
        assert!(out[0].is_finite());
        let expected = (-LAMBDA * 1000.0_f64).exp();
        assert!((out[0] - expected).abs() < 1e-30);
    }
}
