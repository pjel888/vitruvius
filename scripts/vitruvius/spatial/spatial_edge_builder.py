"""Sprint GT Stream GT.4.3 — ``physically_adjacent_to`` edge generator.

For every pair of spatial points whose AABBs intersect (or touch
on a shared face), this module emits one edge with the predicate
``physically_adjacent_to``. The builder uses Python-native AABB
intersection for an O(n^2) first implementation; when the
``engine_rs`` LinearOctree's neighbour enumerator lands, the
builder can be rewritten to run in O(n log n).

The snapshot builder is expected to call this function only when
``config.features.gt_spatial_edges`` is true.

Note
----
``SpatialPoint`` and ``SpatialEdge`` here are *local* dataclasses —
distinct from ``vitruvius.engine_rs.SpatialPoint`` (which stores a
centroid) and ``vitruvius.graph.contract.GraphEdge`` (which carries
the full Phase-8 edge schema). The snapshot builder is responsible
for mapping these lightweight records onto ``GraphEdge`` instances
downstream — that mapping is deliberately out of scope for this
stream so this module stays pure-python and testable without a
full snapshot fixture.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable


@dataclass(frozen=True)
class SpatialPoint:
    """A spatial instance with an axis-aligned bounding box.

    ``aabb`` is duck-typed: it only needs ``.min_xyz`` and
    ``.max_xyz`` attributes, each a 3-tuple of floats. This keeps
    the module independent of any particular AABB dataclass in the
    rest of the codebase.
    """

    id: str
    aabb: Any


@dataclass(frozen=True)
class SpatialEdge:
    """A ``physically_adjacent_to`` edge between two spatial points."""

    from_id: str
    to_id: str
    type: str = "physically_adjacent_to"


def _aabbs_intersect(a: Any, b: Any) -> bool:
    """Return True if two axis-aligned bounding boxes intersect.

    Uses closed-interval intersection — boxes that merely touch on a
    shared face (e.g. walls sharing the x=1.0 plane) count as
    adjacent, which is the semantics the GraphRAG seed pipeline
    wants for ``physically_adjacent_to``.
    """
    ax0, ay0, az0 = a.min_xyz
    ax1, ay1, az1 = a.max_xyz
    bx0, by0, bz0 = b.min_xyz
    bx1, by1, bz1 = b.max_xyz
    if ax1 < bx0 or bx1 < ax0:
        return False
    if ay1 < by0 or by1 < ay0:
        return False
    if az1 < bz0 or bz1 < az0:
        return False
    return True


def build_spatial_adjacency_edges(
    points: Iterable[SpatialPoint],
) -> list[SpatialEdge]:
    """Return one ``SpatialEdge`` per pair of intersecting AABBs.

    Edges are emitted in input order — if ``points[i]`` precedes
    ``points[j]`` and their AABBs intersect, the edge is
    ``SpatialEdge(from_id=points[i].id, to_id=points[j].id)``.
    The traversal is O(n^2) — fine for the ~10^3-node snapshots
    Sprint GT targets, and the octree-backed rewrite can land when
    GT.5 enables it.
    """
    materialised = list(points)
    edges: list[SpatialEdge] = []
    for i in range(len(materialised)):
        a = materialised[i]
        for j in range(i + 1, len(materialised)):
            b = materialised[j]
            if _aabbs_intersect(a.aabb, b.aabb):
                edges.append(SpatialEdge(from_id=a.id, to_id=b.id))
    return edges


__all__ = [
    "SpatialPoint",
    "SpatialEdge",
    "build_spatial_adjacency_edges",
]
