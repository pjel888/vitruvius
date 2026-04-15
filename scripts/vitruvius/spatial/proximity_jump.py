"""Sprint GT Stream GT.4 — bridge ``engine_rs`` octree → Phase 8 snapshot.

This module glues two previously-independent layers together:

1. The Rust linear octree shipped in Sprint GT.1/GT.2 at
   ``scripts/vitruvius/engine_rs/`` — a spatial index over every
   ``spatial_instance`` node's centroid. It exposes
   ``query_sphere(cx, cy, cz, radius) -> list[SpatialPoint]`` where
   each ``SpatialPoint`` carries a string ``.id``.
2. The Phase 8 graph contract at ``scripts/vitruvius/graph/contract.py``
   — an immutable ``GraphSnapshot`` whose nodes have ``.id`` fields
   prefixed ``instance-``.

Given a focal xyz and a sphere radius, ``proximity_jump_seed`` returns
the subset of snapshot-node IDs that lie inside the sphere. Stale
octree entries (IDs the snapshot has forgotten) are filtered out so a
lagging index cannot poison the GraphRAG seed set.

``weight_by_distance`` is the geometric-decay helper consumed by the
Sprint GT.4 GraphRAG chain — pure math, no octree dependency. Closer
seeds score near 1.0, distant seeds asymptote to 0.0.

Both helpers are gated upstream by the ``gt_proximity_jump`` feature
flag in ``config/vitruvius.yaml``.
"""
from __future__ import annotations

import math
from typing import Any, Iterable, Mapping, Protocol


class _OctreeLike(Protocol):
    """Duck-typed octree interface.

    Matches the real ``vitruvius.engine_rs.LinearOctree`` signature:
    ``query_sphere(cx, cy, cz, radius)``. The return value may be a
    list of objects with an ``.id`` attribute OR a list of bare
    strings — both shapes are accepted.
    """

    def query_sphere(
        self,
        cx: float,
        cy: float,
        cz: float,
        radius: float,
    ) -> list[Any]:
        ...


def _extract_id(hit: Any) -> str:
    """Return the string ID of an octree hit.

    The real ``engine_rs.SpatialPoint`` exposes ``.id``; the
    original TDD sketch used bare strings. Accept both so the
    helper works against either shape without a shim layer.
    """
    if isinstance(hit, str):
        return hit
    return str(hit.id)


def proximity_jump_seed(
    *,
    octree: _OctreeLike,
    focal_xyz: tuple[float, float, float],
    radius: float,
    snapshot: Any,
) -> list[str]:
    """Return snapshot-node IDs that lie within ``radius`` of ``focal_xyz``.

    Parameters
    ----------
    octree:
        Any object exposing ``query_sphere(cx, cy, cz, radius)``.
        In production this is a ``vitruvius.engine_rs.LinearOctree``;
        tests use an in-memory fake.
    focal_xyz:
        Query centre as an ``(x, y, z)`` tuple in the same coordinate
        frame as the octree points.
    radius:
        Query radius (inclusive, same units as the octree points).
    snapshot:
        Duck-typed ``GraphSnapshot`` — any object exposing ``.nodes``
        (iterable of objects with an ``.id`` attribute).

    Returns
    -------
    list[str]
        Snapshot-node IDs that fell inside the sphere, in the order
        returned by the octree (stable for test assertions that use
        ``sorted(...)``). IDs returned by the octree that are NOT
        present in the snapshot are silently dropped — a stale
        octree entry should not poison the GraphRAG seed set.
    """
    octree_hits = list(octree.query_sphere(*focal_xyz, radius))
    known_ids: set[str] = {node.id for node in snapshot.nodes}
    return [
        hit_id
        for hit_id in (_extract_id(hit) for hit in octree_hits)
        if hit_id in known_ids
    ]


def weight_by_distance(
    seeds: Mapping[str, tuple[float, float, float]],
    *,
    focal_xyz: tuple[float, float, float],
    lambda_decay: float = 0.1,
) -> dict[str, float]:
    """Return ``{seed_id: exp(-lambda_decay * d)}`` for each seed.

    ``d`` is Euclidean distance from ``focal_xyz``. Output values lie
    in ``(0.0, 1.0]`` — the seed AT the focal point scores 1.0, seeds
    far away asymptote to 0.0. Empty input returns an empty dict.

    The helper is deliberately pure math with no dependency on the
    octree — the caller is expected to already have resolved each
    seed ID back to an ``(x, y, z)`` centroid (via a separate
    snapshot lookup or directly from the octree point cloud).
    """
    fx, fy, fz = focal_xyz
    weights: dict[str, float] = {}
    for seed_id, (x, y, z) in seeds.items():
        distance = math.sqrt((x - fx) ** 2 + (y - fy) ** 2 + (z - fz) ** 2)
        weights[seed_id] = math.exp(-lambda_decay * distance)
    return weights


__all__ = ["proximity_jump_seed", "weight_by_distance"]
