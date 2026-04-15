"""Sprint GT Stream GT.4.3 — spatial edge generator for adjacent AABBs.

Walks pairs of spatial points and emits one ``physically_adjacent_to``
edge per intersecting (or touching) AABB pair. Behind the
``gt_spatial_edges`` feature flag in ``config/vitruvius.yaml``.
"""
from __future__ import annotations

from dataclasses import dataclass

import pytest

from vitruvius.spatial.spatial_edge_builder import (
    SpatialEdge,
    SpatialPoint,
    build_spatial_adjacency_edges,
)


@dataclass
class AABB:
    min_xyz: tuple[float, float, float]
    max_xyz: tuple[float, float, float]


def test_two_overlapping_points_produce_one_edge() -> None:
    """Classic overlap: (0,0,0)-(1,1,1) vs (0.5,0.5,0.5)-(1.5,1.5,1.5)."""
    points = [
        SpatialPoint(
            id="instance-col-01",
            aabb=AABB(min_xyz=(0.0, 0.0, 0.0), max_xyz=(1.0, 1.0, 1.0)),
        ),
        SpatialPoint(
            id="instance-col-02",
            aabb=AABB(min_xyz=(0.5, 0.5, 0.5), max_xyz=(1.5, 1.5, 1.5)),
        ),
    ]
    edges = build_spatial_adjacency_edges(points)
    assert len(edges) == 1
    assert edges[0].from_id == "instance-col-01"
    assert edges[0].to_id == "instance-col-02"
    assert edges[0].type == "physically_adjacent_to"


def test_two_distant_points_produce_no_edges() -> None:
    """Non-intersecting AABBs → empty edge list."""
    points = [
        SpatialPoint(
            id="instance-col-01",
            aabb=AABB(min_xyz=(0.0, 0.0, 0.0), max_xyz=(1.0, 1.0, 1.0)),
        ),
        SpatialPoint(
            id="instance-col-02",
            aabb=AABB(min_xyz=(10.0, 10.0, 10.0), max_xyz=(11.0, 11.0, 11.0)),
        ),
    ]
    edges = build_spatial_adjacency_edges(points)
    assert edges == []


def test_touching_edges_count_as_adjacent() -> None:
    """Shared face at x=1.0 → walls are physically adjacent."""
    points = [
        SpatialPoint(
            id="instance-wall-01",
            aabb=AABB(min_xyz=(0.0, 0.0, 0.0), max_xyz=(1.0, 1.0, 1.0)),
        ),
        SpatialPoint(
            id="instance-wall-02",
            aabb=AABB(min_xyz=(1.0, 0.0, 0.0), max_xyz=(2.0, 1.0, 1.0)),
        ),
    ]
    edges = build_spatial_adjacency_edges(points)
    assert len(edges) == 1
    assert edges[0].from_id == "instance-wall-01"
    assert edges[0].to_id == "instance-wall-02"


def test_three_mutually_overlapping_produces_three_pairs() -> None:
    """3-choose-2 = 3 unique edges with stable input-order pair ordering."""
    points = [
        SpatialPoint(
            id="instance-a",
            aabb=AABB(min_xyz=(0.0, 0.0, 0.0), max_xyz=(1.0, 1.0, 1.0)),
        ),
        SpatialPoint(
            id="instance-b",
            aabb=AABB(min_xyz=(0.5, 0.5, 0.5), max_xyz=(1.5, 1.5, 1.5)),
        ),
        SpatialPoint(
            id="instance-c",
            aabb=AABB(min_xyz=(0.9, 0.9, 0.9), max_xyz=(2.0, 2.0, 2.0)),
        ),
    ]
    edges = build_spatial_adjacency_edges(points)
    assert len(edges) == 3
    pair_set = {(e.from_id, e.to_id) for e in edges}
    assert pair_set == {
        ("instance-a", "instance-b"),
        ("instance-a", "instance-c"),
        ("instance-b", "instance-c"),
    }
    # Every edge must use the same predicate.
    assert {e.type for e in edges} == {"physically_adjacent_to"}


def test_single_point_produces_no_edges() -> None:
    """One-element input → zero pairs → zero edges."""
    points = [
        SpatialPoint(
            id="instance-solo",
            aabb=AABB(min_xyz=(0.0, 0.0, 0.0), max_xyz=(1.0, 1.0, 1.0)),
        ),
    ]
    assert build_spatial_adjacency_edges(points) == []


def test_empty_input_produces_no_edges() -> None:
    assert build_spatial_adjacency_edges([]) == []
