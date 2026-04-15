"""Sprint RUST-MIG-1 Task 5 — S2 Rust/Python parity test for ``weight_by_distance``.

Verifies that the Rust fast path for ``weight_by_distance`` (behind the
``rust_mig_spatial_kernels`` feature flag) produces elementwise-identical
output to the pure-Python ``math.exp(-lambda_decay * d)`` baseline for a
deterministic synthetic set of 10 000 seeds.

The parity assertion uses ``numpy.testing.assert_allclose(atol=1e-12, rtol=0)``
— the Rust and Python paths both call ``sqrt`` and ``exp`` on the same
``f64`` operands in the same order, so the only way the two can diverge is
ULP-level rounding in ``libm`` vs Rust's ``f64::sqrt``/``f64::exp``
implementations. 1e-12 is several orders of magnitude above realistic
libm-libm drift and still tight enough to catch a genuine bug.

Flag toggling is done via monkey-patching
``vitruvius.spatial.proximity_jump`` (not by editing ``config/vitruvius.yaml``)
so the test is hermetic.
"""
from __future__ import annotations

import math

import pytest

from vitruvius.spatial.proximity_jump import weight_by_distance
from vitruvius.spatial import proximity_jump as _pj_module


_FOCAL: tuple[float, float, float] = (50.0, 50.0, 50.0)
_LAMBDA_DECAY: float = 0.05


def _make_synthetic_seeds(
    n: int, seed: int = 42
) -> dict[str, tuple[float, float, float]]:
    """Generate ``n`` deterministic 3D seeds in a 100-unit cube.

    Matches the audit-spec fixture (``numpy.random.default_rng(42)``,
    100-unit cube, fixed focal (50, 50, 50), lambda 0.05) so the parity
    test is reproducible on any host.
    """
    numpy = pytest.importorskip("numpy")
    rng = numpy.random.default_rng(seed)
    coords = rng.uniform(0.0, 100.0, size=(n, 3))
    return {
        f"seed-{i:06d}": (
            float(coords[i, 0]),
            float(coords[i, 1]),
            float(coords[i, 2]),
        )
        for i in range(n)
    }


def test_rust_weight_matches_python_on_10k_seeds(monkeypatch) -> None:
    """Rust fast path must produce elementwise-identical weights on 10 000 seeds."""
    numpy = pytest.importorskip("numpy")

    rs_func = getattr(_pj_module, "weight_by_distance_rs", None)
    if rs_func is None:
        pytest.fail(
            "weight_by_distance_rs not imported into proximity_jump — "
            "Task 5 Rust wiring is incomplete."
        )

    seeds = _make_synthetic_seeds(10_000)

    # ---- Pure-Python baseline (flag OFF). ----
    class _FlagsOff:
        def is_enabled(self, _name: str) -> bool:
            return False

    monkeypatch.setattr(_pj_module, "_load_features_cached", lambda: _FlagsOff())
    py_weights = weight_by_distance(
        seeds, focal_xyz=_FOCAL, lambda_decay=_LAMBDA_DECAY
    )

    # ---- Rust fast path (flag ON). ----
    class _FlagsOn:
        def is_enabled(self, name: str) -> bool:
            return name == "rust_mig_spatial_kernels"

    monkeypatch.setattr(_pj_module, "_load_features_cached", lambda: _FlagsOn())
    rs_weights = weight_by_distance(
        seeds, focal_xyz=_FOCAL, lambda_decay=_LAMBDA_DECAY
    )

    # Keys must match exactly (same seed ids, same order).
    assert list(py_weights.keys()) == list(rs_weights.keys()), (
        "Rust and Python returned mismatched seed-id key sets"
    )

    py_values = numpy.array([py_weights[k] for k in py_weights], dtype=numpy.float64)
    rs_values = numpy.array([rs_weights[k] for k in py_weights], dtype=numpy.float64)

    # Sanity: non-trivial output (not all zero, not all one).
    assert float(py_values.min()) > 0.0
    assert float(py_values.max()) <= 1.0
    assert float(py_values.max()) > float(py_values.min()), (
        "Synthetic fixture collapsed to a single weight — test is vacuous."
    )

    numpy.testing.assert_allclose(rs_values, py_values, atol=1e-12, rtol=0.0)


def test_rust_weight_empty_seeds(monkeypatch) -> None:
    """Empty input → empty output on both paths."""
    if getattr(_pj_module, "weight_by_distance_rs", None) is None:
        pytest.skip("Rust fast path not built.")

    class _FlagsOn:
        def is_enabled(self, name: str) -> bool:
            return name == "rust_mig_spatial_kernels"

    monkeypatch.setattr(_pj_module, "_load_features_cached", lambda: _FlagsOn())
    out = weight_by_distance({}, focal_xyz=_FOCAL, lambda_decay=_LAMBDA_DECAY)
    assert out == {}


def test_rust_weight_zero_distance_is_one(monkeypatch) -> None:
    """A single seed sitting AT the focal point must score exactly 1.0."""
    if getattr(_pj_module, "weight_by_distance_rs", None) is None:
        pytest.skip("Rust fast path not built.")

    class _FlagsOn:
        def is_enabled(self, name: str) -> bool:
            return name == "rust_mig_spatial_kernels"

    monkeypatch.setattr(_pj_module, "_load_features_cached", lambda: _FlagsOn())
    seeds = {"at-focal": _FOCAL}
    out = weight_by_distance(seeds, focal_xyz=_FOCAL, lambda_decay=_LAMBDA_DECAY)
    assert out == {"at-focal": 1.0}


def test_rust_weight_large_distance_is_small_positive(monkeypatch) -> None:
    """A far seed must score strictly in (0, 1) — not zero, not NaN."""
    if getattr(_pj_module, "weight_by_distance_rs", None) is None:
        pytest.skip("Rust fast path not built.")

    class _FlagsOn:
        def is_enabled(self, name: str) -> bool:
            return name == "rust_mig_spatial_kernels"

    monkeypatch.setattr(_pj_module, "_load_features_cached", lambda: _FlagsOn())
    # 1000 units away from focal; exp(-0.05 * 1000) ~= 1.93e-22, still finite.
    far_seed = (50.0 + 1000.0, 50.0, 50.0)
    seeds = {"far": far_seed}
    out = weight_by_distance(seeds, focal_xyz=_FOCAL, lambda_decay=_LAMBDA_DECAY)
    w = out["far"]
    assert w > 0.0
    assert w < 1.0
    assert not math.isnan(w)
    assert math.isfinite(w)
    # Compare to the analytic expectation; this should be well within 1e-12
    # of the pure-Python path.
    expected = math.exp(-_LAMBDA_DECAY * 1000.0)
    assert abs(w - expected) < 1e-12


def test_rust_fast_path_is_noop_when_flag_off(monkeypatch) -> None:
    """Flag-OFF → the Rust kernel is NOT called, pure-Python path runs.

    Non-breaking contract from AD-036 §Decision 5: ``rust_mig_spatial_kernels=false``
    must be byte-identical to pre-migration behaviour. The test proves this by
    replacing ``weight_by_distance_rs`` with a sentinel that raises
    ``AssertionError`` if invoked.
    """
    if getattr(_pj_module, "weight_by_distance_rs", None) is None:
        pytest.skip("Rust fast path not built — nothing to test flag-off for.")

    class _FlagsOff:
        def is_enabled(self, _name: str) -> bool:
            return False

    monkeypatch.setattr(_pj_module, "_load_features_cached", lambda: _FlagsOff())

    def _must_not_be_called(*_args, **_kwargs):  # pragma: no cover - sentinel
        raise AssertionError(
            "weight_by_distance_rs was invoked with the feature flag OFF — "
            "the Python short-circuit is broken."
        )

    monkeypatch.setattr(_pj_module, "weight_by_distance_rs", _must_not_be_called)

    seeds = _make_synthetic_seeds(50)
    out = weight_by_distance(seeds, focal_xyz=_FOCAL, lambda_decay=_LAMBDA_DECAY)

    # Non-empty — proves the Python baseline actually emitted something.
    assert len(out) == 50
    assert all(0.0 < w <= 1.0 for w in out.values())
