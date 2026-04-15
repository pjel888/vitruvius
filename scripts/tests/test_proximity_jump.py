"""Sprint GT Stream GT.4.1 — proximity jump from octree to snapshot IDs.

Bridges the `engine_rs` LinearOctree (Sprint GT.2) to the Phase 8
graph snapshot: given a focal xyz and a sphere radius, return the
set of snapshot-node IDs that fall inside the sphere.

NOTE on the octree API shape: The plan's TDD spec sketches a
``query_sphere(center_tuple, radius) -> list[str]`` test double.
The real ``vitruvius.engine_rs.LinearOctree`` (committed in Sprint
GT.2) exposes ``query_sphere(cx, cy, cz, radius) -> list[SpatialPoint]``.
The production ``proximity_jump_seed`` helper therefore calls
``octree.query_sphere(*focal_xyz, radius)`` and extracts ``.id`` from
each returned point (falling back to the raw value when the result
is already a string, so the test double below keeps working).
"""
from __future__ import annotations

from dataclasses import dataclass, field

import pytest

from vitruvius.spatial.proximity_jump import proximity_jump_seed


@dataclass
class FakePoint:
    """Matches the engine_rs SpatialPoint shape — has .id and xyz."""

    id: str
    x: float
    y: float
    z: float


@dataclass
class FakeOctree:
    """Test double — the real one is ``engine_rs.LinearOctree``.

    Mirrors the real API: ``query_sphere(cx, cy, cz, radius)``
    returning a list of points with ``.id`` / ``.x`` / ``.y`` / ``.z``.
    """

    points: dict[str, tuple[float, float, float]] = field(default_factory=dict)

    def query_sphere(
        self,
        cx: float,
        cy: float,
        cz: float,
        radius: float,
    ) -> list[FakePoint]:
        hits: list[FakePoint] = []
        for pid, (x, y, z) in self.points.items():
            dist_sq = (x - cx) ** 2 + (y - cy) ** 2 + (z - cz) ** 2
            if dist_sq <= radius * radius:
                hits.append(FakePoint(id=pid, x=x, y=y, z=z))
        return hits


@dataclass
class FakeGraphNode:
    id: str


@dataclass
class FakeSnapshot:
    nodes: list[FakeGraphNode]


def test_proximity_jump_returns_points_inside_sphere() -> None:
    """Five points, three within r=1.0 of origin → three IDs returned."""
    octree = FakeOctree(
        points={
            "instance-col-01": (0.0, 0.0, 0.0),
            "instance-col-02": (0.5, 0.5, 0.0),
            "instance-col-03": (10.0, 10.0, 10.0),
            "instance-col-04": (0.8, 0.0, 0.0),
            "instance-col-05": (100.0, 100.0, 100.0),
        }
    )
    snapshot = FakeSnapshot(
        nodes=[
            FakeGraphNode(id="instance-col-01"),
            FakeGraphNode(id="instance-col-02"),
            FakeGraphNode(id="instance-col-03"),
            FakeGraphNode(id="instance-col-04"),
            FakeGraphNode(id="instance-col-05"),
        ]
    )
    seeds = proximity_jump_seed(
        octree=octree,
        focal_xyz=(0.0, 0.0, 0.0),
        radius=1.0,
        snapshot=snapshot,
    )
    assert sorted(seeds) == [
        "instance-col-01",
        "instance-col-02",
        "instance-col-04",
    ]


def test_proximity_jump_filters_unknown_ids() -> None:
    """An octree hit that is NOT in the snapshot must be dropped — a
    stale octree entry must not poison the GraphRAG seed set."""
    octree = FakeOctree(
        points={
            "instance-col-01": (0.0, 0.0, 0.0),
            "instance-ghost-99": (0.1, 0.1, 0.0),  # not in snapshot
        }
    )
    snapshot = FakeSnapshot(nodes=[FakeGraphNode(id="instance-col-01")])
    seeds = proximity_jump_seed(
        octree=octree,
        focal_xyz=(0.0, 0.0, 0.0),
        radius=1.0,
        snapshot=snapshot,
    )
    assert seeds == ["instance-col-01"]


def test_proximity_jump_empty_when_nothing_nearby() -> None:
    """Every octree point is outside the radius → empty seed list."""
    octree = FakeOctree(
        points={"instance-far-01": (1000.0, 1000.0, 1000.0)}
    )
    snapshot = FakeSnapshot(nodes=[FakeGraphNode(id="instance-far-01")])
    seeds = proximity_jump_seed(
        octree=octree,
        focal_xyz=(0.0, 0.0, 0.0),
        radius=1.0,
        snapshot=snapshot,
    )
    assert seeds == []


def test_proximity_jump_accepts_raw_string_ids() -> None:
    """Octrees that already return bare ID strings (plan's original
    sketch) must still work — production code should handle both."""

    @dataclass
    class StringOctree:
        hits: list[str]

        def query_sphere(
            self, cx: float, cy: float, cz: float, radius: float
        ) -> list[str]:
            return list(self.hits)

    snapshot = FakeSnapshot(
        nodes=[
            FakeGraphNode(id="instance-a"),
            FakeGraphNode(id="instance-b"),
        ]
    )
    seeds = proximity_jump_seed(
        octree=StringOctree(hits=["instance-a", "instance-b"]),
        focal_xyz=(0.0, 0.0, 0.0),
        radius=1.0,
        snapshot=snapshot,
    )
    assert sorted(seeds) == ["instance-a", "instance-b"]
