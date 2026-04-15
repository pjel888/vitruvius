"""Sprint RUST-MIG-1 Task 6 — N4 Rust/Python parity test for ``mahalanobis_distance``.

Verifies that the Rust fast path for ``mahalanobis_distance`` (behind the
``rust_mig_stats_kernels`` feature flag) produces
numerically-identical output to the pure-Python
``float(delta @ cov_inv @ delta)`` baseline for a deterministic synthetic
set of 1 000 reference embeddings + 200 query vectors.

The parity assertion uses
``numpy.testing.assert_allclose(atol=1e-9, rtol=1e-9)`` — Mahalanobis
distance involves a dense matrix-vector product followed by a scalar
square root, so the ULP budget is larger than the O(n) elementwise
``exp`` kernel we tested in Task 5. nalgebra's BLAS-3 dot/quadratic form
in ``cov_inv * delta`` and numpy's equivalent ``delta @ cov_inv`` may
diverge by a handful of f64 ULPs on identical inputs because their loop
ordering and FMA usage differ. 1e-9 is conservative for 64-dim linalg
and still tight enough to catch a genuine bug (e.g. a sign flip, a wrong
ridge, or a transpose error).

Flag toggling is done via monkey-patching
``vitruvius.normalization.outlier_detector`` (not by editing
``config/vitruvius.yaml``) so the test is hermetic.
"""
from __future__ import annotations

import math

import numpy as np
import pytest

from vitruvius.normalization.outlier_detector import (
    OutlierModel,
    fit_outlier_model,
    mahalanobis_distance,
)
from vitruvius.normalization import outlier_detector as _od_module


_DIM: int = 64
_N_REF: int = 1_000
_N_QUERY: int = 200
_SEED: int = 42


def _make_reference_embeddings(n: int = _N_REF, dim: int = _DIM) -> np.ndarray:
    """Deterministic ``(n, dim)`` float64 matrix sampled from N(0, 1).

    ``numpy.random.default_rng(42)`` anchors the test to a fixed stream so
    every host recomputes the same reference set. The Task 1 bench harness
    uses an identical fixture shape, which makes the parity test's
    micro-bench numbers directly comparable to the audit baseline.
    """
    rng = np.random.default_rng(_SEED)
    return rng.standard_normal(size=(n, dim)).astype(np.float64)


def _make_query_batch(n: int = _N_QUERY, dim: int = _DIM, seed: int = _SEED + 1) -> np.ndarray:
    """Deterministic ``(n, dim)`` query batch from a DIFFERENT rng seed.

    Using ``seed + 1`` keeps the reference and query distributions
    independent without forcing the test to maintain two separate fixtures.
    """
    rng = np.random.default_rng(seed)
    return rng.standard_normal(size=(n, dim)).astype(np.float64)


def test_rust_mahalanobis_matches_python_on_1000_embeddings(monkeypatch) -> None:
    """Rust fast path must produce near-identical distances on 1 000 refs + 200 queries.

    The reference set fits a single ``OutlierModel`` once. The 200 query
    vectors are scored twice — once via the pure-Python path (flag OFF)
    and once via the Rust path (flag ON). Both outputs go through the
    same ``numpy.testing.assert_allclose`` tight tolerance check.
    """
    rs_func = getattr(_od_module, "mahalanobis_distance_rs", None)
    if rs_func is None:
        pytest.fail(
            "mahalanobis_distance_rs not imported into outlier_detector — "
            "Task 6 Rust wiring is incomplete."
        )

    reference = _make_reference_embeddings()
    queries = _make_query_batch()

    # Fit once — ``fit_outlier_model`` is the same in both paths (no
    # Rust port of ``fit`` in Task 6; the audit flagged only the
    # scoring loop as hot).
    model = fit_outlier_model(reference.tolist())

    # ---- Pure-Python baseline (flag OFF). ----
    class _FlagsOff:
        def is_enabled(self, _name: str) -> bool:
            return False

    monkeypatch.setattr(_od_module, "_load_features_cached", lambda: _FlagsOff())
    py_distances = np.array(
        [mahalanobis_distance(q.tolist(), model) for q in queries],
        dtype=np.float64,
    )

    # ---- Rust fast path (flag ON). ----
    class _FlagsOn:
        def is_enabled(self, name: str) -> bool:
            return name == "rust_mig_stats_kernels"

    monkeypatch.setattr(_od_module, "_load_features_cached", lambda: _FlagsOn())
    rs_distances = np.array(
        [mahalanobis_distance(q.tolist(), model) for q in queries],
        dtype=np.float64,
    )

    # Sanity: non-trivial output (at 64-dim the mean-scale expected
    # distance for a random Gaussian draw is ~sqrt(dim) ≈ 8).
    assert float(py_distances.min()) > 0.0
    assert float(py_distances.max()) < 100.0  # generous upper bound
    assert float(py_distances.max()) > float(py_distances.min()), (
        "Synthetic fixture collapsed to a single distance — test is vacuous."
    )

    np.testing.assert_allclose(rs_distances, py_distances, atol=1e-9, rtol=1e-9)


def test_rust_mahalanobis_zero_diff_returns_zero(monkeypatch) -> None:
    """``x == model.centroid`` → distance ≈ 0 (not NaN, not negative)."""
    if getattr(_od_module, "mahalanobis_distance_rs", None) is None:
        pytest.skip("Rust fast path not built.")

    class _FlagsOn:
        def is_enabled(self, name: str) -> bool:
            return name == "rust_mig_stats_kernels"

    monkeypatch.setattr(_od_module, "_load_features_cached", lambda: _FlagsOn())

    reference = _make_reference_embeddings()
    model = fit_outlier_model(reference.tolist())

    # Score the centroid itself — ``diff`` vector is exactly zero so
    # ``diff^T @ cov_inv @ diff == 0.0`` deterministically (IEEE-754
    # guarantees 0 * anything = 0).
    centroid_vec = list(model.centroid)
    d = mahalanobis_distance(centroid_vec, model)
    assert d == 0.0
    assert not math.isnan(d)


def test_rust_mahalanobis_identity_cov_equals_euclidean(monkeypatch) -> None:
    """With Σ = I (covariance = identity), Mahalanobis === Euclidean.

    Constructing an exact-identity covariance via fitting is hard
    (requires carefully crafted input), so instead we build a handcrafted
    ``OutlierModel`` with centroid = 0, cov_inv = I. Under that model
    the Mahalanobis distance of any vector ``x`` is exactly ``||x||_2``.
    """
    if getattr(_od_module, "mahalanobis_distance_rs", None) is None:
        pytest.skip("Rust fast path not built.")

    class _FlagsOn:
        def is_enabled(self, name: str) -> bool:
            return name == "rust_mig_stats_kernels"

    monkeypatch.setattr(_od_module, "_load_features_cached", lambda: _FlagsOn())

    dim = 8
    identity_model = OutlierModel(
        centroid=tuple(0.0 for _ in range(dim)),
        covariance_inv=tuple(
            tuple(1.0 if i == j else 0.0 for j in range(dim)) for i in range(dim)
        ),
        ridge=0.0,
    )

    x = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]
    expected = math.sqrt(sum(v * v for v in x))
    got = mahalanobis_distance(x, identity_model)
    assert abs(got - expected) < 1e-12


def test_rust_mahalanobis_diagonal_cov_scales_per_axis(monkeypatch) -> None:
    """With Σ⁻¹ = diag(1/σ²), Mahalanobis === sqrt(sum((x_i/σ_i)²)).

    Same construction trick as the identity test — a handcrafted
    ``OutlierModel`` with a diagonal cov_inv so we can compute the
    expected distance in closed form.
    """
    if getattr(_od_module, "mahalanobis_distance_rs", None) is None:
        pytest.skip("Rust fast path not built.")

    class _FlagsOn:
        def is_enabled(self, name: str) -> bool:
            return name == "rust_mig_stats_kernels"

    monkeypatch.setattr(_od_module, "_load_features_cached", lambda: _FlagsOn())

    # cov_inv diag = [4, 1, 0.25] -> sigma = [0.5, 1.0, 2.0] -> per-axis
    # scale = [2.0, 1.0, 0.5]. For x = [1, 2, 4], expected distance is
    # sqrt((1*2)^2 + (2*1)^2 + (4*0.5)^2) = sqrt(4 + 4 + 4) = sqrt(12).
    model = OutlierModel(
        centroid=(0.0, 0.0, 0.0),
        covariance_inv=(
            (4.0, 0.0, 0.0),
            (0.0, 1.0, 0.0),
            (0.0, 0.0, 0.25),
        ),
        ridge=0.0,
    )

    x = [1.0, 2.0, 4.0]
    expected = math.sqrt(12.0)
    got = mahalanobis_distance(x, model)
    assert abs(got - expected) < 1e-12


def test_rust_fast_path_is_noop_when_flag_off(monkeypatch) -> None:
    """Flag-OFF → Rust kernel is NOT called; pure-Python path runs.

    Non-breaking contract from AD-036 §Decision 5:
    ``rust_mig_stats_kernels=false`` must be byte-identical to
    pre-migration behaviour. The test proves this by replacing
    ``mahalanobis_distance_rs`` with a sentinel that raises if invoked.
    """
    if getattr(_od_module, "mahalanobis_distance_rs", None) is None:
        pytest.skip("Rust fast path not built — nothing to test flag-off for.")

    class _FlagsOff:
        def is_enabled(self, _name: str) -> bool:
            return False

    monkeypatch.setattr(_od_module, "_load_features_cached", lambda: _FlagsOff())

    def _must_not_be_called(*_args, **_kwargs):  # pragma: no cover - sentinel
        raise AssertionError(
            "mahalanobis_distance_rs was invoked with the feature flag OFF — "
            "the Python short-circuit is broken."
        )

    monkeypatch.setattr(_od_module, "mahalanobis_distance_rs", _must_not_be_called)

    reference = _make_reference_embeddings(n=100, dim=16)
    model = fit_outlier_model(reference.tolist())

    # Score a random query — the sentinel will raise if the short-
    # circuit is broken.
    rng = np.random.default_rng(_SEED + 7)
    query = rng.standard_normal(size=16).tolist()
    d = mahalanobis_distance(query, model)
    assert d >= 0.0
    assert math.isfinite(d)
