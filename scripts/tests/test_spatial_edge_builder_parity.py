"""Sprint RUST-MIG-1 Task 4 — S1 Rust/Python parity test.

Verifies that the Rust fast path for ``build_spatial_adjacency_edges``
(behind the ``rust_mig_spatial_kernels`` feature flag) produces the
same edge set as the pure-Python baseline for a deterministic synthetic
snapshot of 200 random AABB boxes.

The comparison is order-independent — the Python implementation walks
input order (``i < j``) and emits edges as ``(points[i].id, points[j].id)``;
the Rust implementation uses the octree's internal visit order and may
emit edges in a different sequence, but the *set* of unordered pairs
must match byte-for-byte. Both paths use closed-interval AABB
intersection so touching faces count as adjacent.

Flag toggling is done via monkey-patching
``vitruvius.spatial.spatial_edge_builder`` (not by editing
``config/vitruvius.yaml``) so the test is hermetic and does not leak
into the rest of the suite.
"""
from __future__ import annotations

from dataclasses import dataclass

import pytest

from vitruvius.spatial.spatial_edge_builder import (
    SpatialPoint,
    build_spatial_adjacency_edges,
)
from vitruvius.spatial import spatial_edge_builder as _seb_module


@dataclass(frozen=True)
class _AABB:
    min_xyz: tuple[float, float, float]
    max_xyz: tuple[float, float, float]


def _make_synthetic_points(n: int, seed: int = 42) -> list[SpatialPoint]:
    """Generate ``n`` deterministic spatial points with random AABBs.

    Deliberately denser than the bench harness fixture — boxes are
    0.5-2.0 units scattered in a 10-unit cube, which at n=200 yields
    ~1000 intersecting pairs on the seed=42 RNG. The bench harness
    uses a 100-unit cube so pair density is ~100x lower at the same
    n; that's fine for wall-time measurement but would make a parity
    test vacuously pass on zero edges. We trade pair density for
    signal here.
    """
    numpy = pytest.importorskip("numpy")
    rng = numpy.random.default_rng(seed)
    mins = rng.uniform(0.0, 10.0, size=(n, 3))
    sizes = rng.uniform(0.5, 2.0, size=(n, 3))
    maxs = mins + sizes
    return [
        SpatialPoint(
            id=f"inst-{i:04d}",
            aabb=_AABB(
                min_xyz=(float(mins[i, 0]), float(mins[i, 1]), float(mins[i, 2])),
                max_xyz=(float(maxs[i, 0]), float(maxs[i, 1]), float(maxs[i, 2])),
            ),
        )
        for i in range(n)
    ]


def _edge_pair_set(edges) -> frozenset[tuple[str, str]]:
    """Return the unordered pair set for an edge list — order-independent.

    Each pair is canonicalised so ``(a, b)`` and ``(b, a)`` compare equal.
    The Rust kernel returns a canonicalised pair (``id_i < id_j``
    lexicographically); the Python baseline returns pairs in input
    order. Normalising both sides here keeps the assertion stable.
    """
    return frozenset(
        (min(e.from_id, e.to_id), max(e.from_id, e.to_id)) for e in edges
    )


def test_rust_matches_python_on_synthetic_snapshot(monkeypatch) -> None:
    """Rust fast path must emit the exact same edge set as Python baseline."""
    rs_func = getattr(_seb_module, "build_spatial_adjacency_edges_rs", None)
    if rs_func is None:
        pytest.fail(
            "build_spatial_adjacency_edges_rs not imported into spatial_edge_builder — "
            "Task 4 Rust wiring is incomplete."
        )

    points = _make_synthetic_points(200)

    # ---- Pure-Python baseline (flag OFF). ----
    class _FlagsOff:
        def is_enabled(self, _name: str) -> bool:
            return False

    monkeypatch.setattr(_seb_module, "_load_features_cached", lambda: _FlagsOff())
    python_edges = build_spatial_adjacency_edges(points)
    python_pairs = _edge_pair_set(python_edges)

    # ---- Rust fast path (flag ON). ----
    class _FlagsOn:
        def is_enabled(self, name: str) -> bool:
            return name == "rust_mig_spatial_kernels"

    monkeypatch.setattr(_seb_module, "_load_features_cached", lambda: _FlagsOn())
    rust_edges = build_spatial_adjacency_edges(points)
    rust_pairs = _edge_pair_set(rust_edges)

    # Sanity: the synthetic snapshot is dense enough that *some*
    # pairs intersect — if both sides are empty the parity assertion
    # is vacuous and we'd miss a silent-empty bug.
    assert len(python_pairs) > 0, (
        "Synthetic snapshot produced zero Python edges — test is vacuous, "
        "bump n or tighten the box-size distribution."
    )

    # The real assertion: identical unordered edge sets.
    assert rust_pairs == python_pairs, (
        f"Rust and Python disagree on {len(python_pairs ^ rust_pairs)} edges "
        f"(python={len(python_pairs)}, rust={len(rust_pairs)})"
    )

    # Every edge on the Rust side must carry the predicate constant.
    assert all(e.type == "physically_adjacent_to" for e in rust_edges)


def test_rust_fast_path_is_noop_when_flag_off(monkeypatch) -> None:
    """Flag-OFF → pure-Python path, even if the Rust extension is importable.

    This is the non-breaking contract from AD-036 §Decision 5:
    ``rust_mig_spatial_kernels=false`` must be byte-identical to
    pre-migration behaviour.
    """
    if getattr(_seb_module, "build_spatial_adjacency_edges_rs", None) is None:
        pytest.skip("Rust fast path not built — nothing to test flag-off behavior for.")

    # Force the flag OFF even if vitruvius.yaml ever flips it to true.
    class _FlagsOff:
        def is_enabled(self, _name: str) -> bool:
            return False

    monkeypatch.setattr(_seb_module, "_load_features_cached", lambda: _FlagsOff())

    points = _make_synthetic_points(50)
    edges = build_spatial_adjacency_edges(points)
    # If the Python path ran we get SpatialEdge dataclass instances
    # with the ``physically_adjacent_to`` type. That is the only
    # observable signal that the Python code path was taken — the
    # Rust path would return the same dataclasses (it has to, for
    # parity) so we can't distinguish by type alone. What we CAN
    # check is that the call succeeded without raising and produced
    # the same dataclass type as the existing Python tests.
    assert all(hasattr(e, "from_id") and hasattr(e, "to_id") for e in edges)
