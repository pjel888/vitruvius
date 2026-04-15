"""Sprint GT Streams GT.1 + GT.2 — pyo3 Rust linear-octree regression tests.

These tests target the ``vitruvius.engine_rs`` wrapper which, when the
maturin-built crate is installed, re-exports the pyo3 ``SpatialPoint``
and ``LinearOctree`` pyclasses. On hosts that have not yet built the
crate the ``pytest.importorskip`` guard skips the whole module, which
keeps CI green until a follow-on step runs ``maturin build`` / ``pip
install`` in the build container.

The tests cover the correctness contract of the GT.2 octree:

* construction + ``len()`` reporting
* insert paths from both ``SpatialPoint`` and the fast-path 4-tuple
* axis-aligned-box queries (inclusive boundary semantics)
* sphere / point queries (Euclidean distance)
* negative queries (no points returned when the box is empty)
* direct field access on ``SpatialPoint`` to guarantee the pyo3
  ``#[pyo3(get)]`` wiring is right
* validation error paths (non-finite coordinates, out-of-bounds
  insert, bad sphere radius) — these are the guardrails the pure
  Python spatial fallback relies on
* a medium-n smoke benchmark that inserts ~1k points and spot-checks
  query correctness against a brute-force list comprehension; this is
  not a real perf test (no timing assertions) but it catches obvious
  regressions from a split-plane bug
"""

from __future__ import annotations

import math
import random

import pytest

# --------------------------------------------------------------------------- #
# Import guard — must happen before anything from the module is referenced.   #
# --------------------------------------------------------------------------- #
engine_rs = pytest.importorskip(
    "vitruvius.engine_rs",
    reason=(
        "vitruvius_engine_rs native crate not built on this host. "
        "Run `cd scripts/vitruvius/engine_rs && python3.11 -m maturin build "
        "--release && pip install target/wheels/*.whl` to enable."
    ),
)

# A second guard for hosts where the Python wrapper exists but the
# underlying extension failed to load (older macOS, wrong ABI, etc.).
if not getattr(engine_rs, "ENGINE_RS_AVAILABLE", False):
    pytest.skip(
        "vitruvius.engine_rs imported but ENGINE_RS_AVAILABLE is False — "
        "the compiled extension was not found.",
        allow_module_level=True,
    )

SpatialPoint = engine_rs.SpatialPoint
LinearOctree = engine_rs.LinearOctree


# --------------------------------------------------------------------------- #
# Core construction + size-reporting                                          #
# --------------------------------------------------------------------------- #
def test_construct_empty_octree() -> None:
    tree = LinearOctree(0.0, 0.0, 0.0, 100.0, 100.0, 100.0)
    assert tree.len() == 0
    assert len(tree) == 0
    assert tree.live_count() == 0
    assert tree.bounds == (0.0, 0.0, 0.0, 100.0, 100.0, 100.0)
    assert tree.max_depth == 8


def test_construct_with_custom_max_depth() -> None:
    tree = LinearOctree(-10.0, -10.0, -10.0, 10.0, 10.0, 10.0, 4)
    assert tree.max_depth == 4
    assert tree.bounds == (-10.0, -10.0, -10.0, 10.0, 10.0, 10.0)


def test_construct_rejects_inverted_bounds() -> None:
    with pytest.raises(ValueError, match="max must be >= min"):
        LinearOctree(10.0, 0.0, 0.0, 0.0, 100.0, 100.0)


def test_construct_rejects_zero_max_depth() -> None:
    with pytest.raises(ValueError, match="max_depth must be >= 1"):
        LinearOctree(0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0)


def test_construct_rejects_non_finite_bounds() -> None:
    with pytest.raises(ValueError, match="finite"):
        LinearOctree(0.0, 0.0, 0.0, float("inf"), 1.0, 1.0)


# --------------------------------------------------------------------------- #
# Insert paths                                                                #
# --------------------------------------------------------------------------- #
def test_insert_and_len() -> None:
    tree = LinearOctree(0.0, 0.0, 0.0, 100.0, 100.0, 100.0)
    for i in range(5):
        tree.insert(SpatialPoint(f"p{i}", float(i * 10), float(i * 10), float(i * 10)))
    assert tree.len() == 5
    assert len(tree) == 5
    assert tree.live_count() == 5


def test_insert_accepts_tuple_fast_path() -> None:
    """The fast-path 4-tuple API lets bulk ingest skip a per-point
    allocation of the SpatialPoint pyclass. It must be equivalent to
    explicit SpatialPoint insertion."""
    tree = LinearOctree(0.0, 0.0, 0.0, 100.0, 100.0, 100.0)
    tree.insert(("tuple-1", 1.0, 2.0, 3.0))
    tree.insert(SpatialPoint("obj-1", 4.0, 5.0, 6.0))
    assert tree.len() == 2
    hits = tree.query_aabb(0.0, 0.0, 0.0, 10.0, 10.0, 10.0)
    ids = sorted(p.id for p in hits)
    assert ids == ["obj-1", "tuple-1"]


def test_insert_rejects_out_of_bounds_point() -> None:
    tree = LinearOctree(0.0, 0.0, 0.0, 10.0, 10.0, 10.0)
    with pytest.raises(ValueError, match="outside the octree bounds"):
        tree.insert(SpatialPoint("bad", 100.0, 100.0, 100.0))
    assert tree.len() == 0


def test_spatial_point_rejects_non_finite() -> None:
    with pytest.raises(ValueError, match="finite"):
        SpatialPoint("nan-point", float("nan"), 0.0, 0.0)


def test_spatial_point_rejects_empty_id() -> None:
    with pytest.raises(ValueError, match="non-empty"):
        SpatialPoint("", 0.0, 0.0, 0.0)


# --------------------------------------------------------------------------- #
# SpatialPoint field access and equality                                      #
# --------------------------------------------------------------------------- #
def test_spatial_point_field_access() -> None:
    p = SpatialPoint("p1", 1.0, 2.0, 3.0)
    assert p.id == "p1"
    assert p.x == 1.0
    assert p.y == 2.0
    assert p.z == 3.0


def test_spatial_point_equality() -> None:
    a = SpatialPoint("same", 1.0, 2.0, 3.0)
    b = SpatialPoint("same", 1.0, 2.0, 3.0)
    c = SpatialPoint("diff", 1.0, 2.0, 3.0)
    d = SpatialPoint("same", 1.0, 2.0, 4.0)
    assert a == b
    assert a != c
    assert a != d


def test_spatial_point_repr() -> None:
    p = SpatialPoint("id", 1.5, 2.5, 3.5)
    r = repr(p)
    assert "SpatialPoint" in r
    assert "id" in r
    assert "1.5" in r


# --------------------------------------------------------------------------- #
# AABB queries                                                                #
# --------------------------------------------------------------------------- #
def test_query_aabb_returns_only_points_inside() -> None:
    """Insert a 4-point cube clustered near the origin plus 4 far
    outliers, then query a box that only covers the cluster. Must
    return exactly the 4 cluster points."""
    tree = LinearOctree(0.0, 0.0, 0.0, 100.0, 100.0, 100.0)
    cluster = [
        SpatialPoint("c0", 1.0, 1.0, 1.0),
        SpatialPoint("c1", 2.0, 1.0, 1.0),
        SpatialPoint("c2", 1.0, 2.0, 1.0),
        SpatialPoint("c3", 1.0, 1.0, 2.0),
    ]
    outliers = [
        SpatialPoint("o0", 50.0, 50.0, 50.0),
        SpatialPoint("o1", 75.0, 25.0, 25.0),
        SpatialPoint("o2", 25.0, 75.0, 25.0),
        SpatialPoint("o3", 99.0, 99.0, 99.0),
    ]
    for p in cluster + outliers:
        tree.insert(p)

    hits = tree.query_aabb(0.0, 0.0, 0.0, 5.0, 5.0, 5.0)
    assert len(hits) == 4
    assert sorted(p.id for p in hits) == ["c0", "c1", "c2", "c3"]


def test_query_aabb_empty_when_no_points_inside() -> None:
    tree = LinearOctree(0.0, 0.0, 0.0, 100.0, 100.0, 100.0)
    tree.insert(SpatialPoint("a", 5.0, 5.0, 5.0))
    tree.insert(SpatialPoint("b", 50.0, 50.0, 50.0))
    tree.insert(SpatialPoint("c", 95.0, 95.0, 95.0))
    hits = tree.query_aabb(10.0, 10.0, 10.0, 20.0, 20.0, 20.0)
    assert hits == []


def test_query_aabb_boundary_is_inclusive() -> None:
    """A point on the boundary of the query box must be returned —
    this keeps GT downstream consumers from having to care about
    floating-point epsilon."""
    tree = LinearOctree(0.0, 0.0, 0.0, 10.0, 10.0, 10.0)
    tree.insert(SpatialPoint("corner", 5.0, 5.0, 5.0))
    hits = tree.query_aabb(5.0, 5.0, 5.0, 5.0, 5.0, 5.0)
    assert len(hits) == 1
    assert hits[0].id == "corner"


def test_query_aabb_full_bounds_returns_everything() -> None:
    tree = LinearOctree(0.0, 0.0, 0.0, 100.0, 100.0, 100.0)
    for i in range(20):
        tree.insert(SpatialPoint(f"p{i}", float(i * 4), float(i * 4), float(i * 4)))
    hits = tree.query_aabb(0.0, 0.0, 0.0, 100.0, 100.0, 100.0)
    assert len(hits) == 20


# --------------------------------------------------------------------------- #
# Sphere queries                                                              #
# --------------------------------------------------------------------------- #
def test_query_sphere_returns_points_within_radius() -> None:
    tree = LinearOctree(-100.0, -100.0, -100.0, 100.0, 100.0, 100.0)
    tree.insert(SpatialPoint("origin", 0.0, 0.0, 0.0))
    tree.insert(SpatialPoint("near", 1.0, 0.0, 0.0))
    tree.insert(SpatialPoint("far", 10.0, 0.0, 0.0))
    hits = tree.query_sphere(0.0, 0.0, 0.0, 5.0)
    assert len(hits) == 2
    assert sorted(p.id for p in hits) == ["near", "origin"]


def test_query_sphere_zero_radius_returns_coincident_points_only() -> None:
    tree = LinearOctree(-10.0, -10.0, -10.0, 10.0, 10.0, 10.0)
    tree.insert(SpatialPoint("here", 2.0, 3.0, 4.0))
    tree.insert(SpatialPoint("one-unit-away", 3.0, 3.0, 4.0))
    hits = tree.query_sphere(2.0, 3.0, 4.0, 0.0)
    assert len(hits) == 1
    assert hits[0].id == "here"


def test_query_sphere_rejects_negative_radius() -> None:
    tree = LinearOctree(0.0, 0.0, 0.0, 10.0, 10.0, 10.0)
    with pytest.raises(ValueError, match="non-negative"):
        tree.query_sphere(0.0, 0.0, 0.0, -1.0)


def test_query_point_is_alias_for_query_sphere() -> None:
    tree = LinearOctree(-10.0, -10.0, -10.0, 10.0, 10.0, 10.0)
    tree.insert(SpatialPoint("a", 0.0, 0.0, 0.0))
    tree.insert(SpatialPoint("b", 3.0, 0.0, 0.0))
    a = tree.query_point(0.0, 0.0, 0.0, 4.0)
    b = tree.query_sphere(0.0, 0.0, 0.0, 4.0)
    assert sorted(p.id for p in a) == sorted(p.id for p in b)


# --------------------------------------------------------------------------- #
# Medium-n stress — spot-check correctness against brute force                #
# --------------------------------------------------------------------------- #
def test_medium_n_aabb_matches_brute_force() -> None:
    """Insert 1,000 deterministic random points and check that the
    octree returns exactly the same AABB query result as a naive
    Python list filter. This is the load-bearing correctness check —
    it's the only test that will catch a split-plane off-by-one bug."""
    random.seed(20260415)
    bounds = (0.0, 0.0, 0.0, 100.0, 100.0, 100.0)
    tree = LinearOctree(*bounds)

    truth: list[tuple[str, float, float, float]] = []
    for i in range(1000):
        x = random.uniform(0.0, 100.0)
        y = random.uniform(0.0, 100.0)
        z = random.uniform(0.0, 100.0)
        pid = f"pt{i}"
        tree.insert(SpatialPoint(pid, x, y, z))
        truth.append((pid, x, y, z))

    assert tree.len() == 1000

    # Query a specific sub-box and compare against the brute-force set.
    query_box = (25.0, 25.0, 25.0, 75.0, 75.0, 75.0)
    expected = {
        pid
        for pid, x, y, z in truth
        if query_box[0] <= x <= query_box[3]
        and query_box[1] <= y <= query_box[4]
        and query_box[2] <= z <= query_box[5]
    }
    actual = {p.id for p in tree.query_aabb(*query_box)}
    assert actual == expected


def test_medium_n_sphere_matches_brute_force() -> None:
    random.seed(20260415)
    tree = LinearOctree(0.0, 0.0, 0.0, 100.0, 100.0, 100.0)

    truth = []
    for i in range(1000):
        x = random.uniform(0.0, 100.0)
        y = random.uniform(0.0, 100.0)
        z = random.uniform(0.0, 100.0)
        pid = f"pt{i}"
        tree.insert(SpatialPoint(pid, x, y, z))
        truth.append((pid, x, y, z))

    cx, cy, cz, r = 50.0, 50.0, 50.0, 15.0
    expected = {
        pid
        for pid, x, y, z in truth
        if math.sqrt((x - cx) ** 2 + (y - cy) ** 2 + (z - cz) ** 2) <= r
    }
    actual = {p.id for p in tree.query_sphere(cx, cy, cz, r)}
    assert actual == expected


# --------------------------------------------------------------------------- #
# Module metadata                                                             #
# --------------------------------------------------------------------------- #
def test_engine_rs_module_metadata() -> None:
    assert engine_rs.ENGINE_RS_AVAILABLE is True
    assert engine_rs.SPRINT_CODENAME == "GT.1+GT.2"
    assert engine_rs.ENGINE_RS_VERSION == "0.1.0"
