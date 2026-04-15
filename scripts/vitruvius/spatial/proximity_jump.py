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
import os
from functools import lru_cache
from pathlib import Path
from typing import Any, Iterable, Mapping, Protocol

# Sprint RUST-MIG-1 Task 5 — import the Rust fast path lazily.
# The ``vitruvius.engine_rs`` facade returns ``None`` when the
# extension module is not built, so the fast-path guard below is
# a pure attribute check with no ImportError risk at call time.
from vitruvius.engine_rs import weight_by_distance_rs
from vitruvius.features import Features, load_features


def _resolve_config_path() -> Path:
    """Mirror of ``vitruvius.spatial.cli._resolve_config_path``.

    Honours ``VITRUVIUS_CONFIG`` for hermetic tests, falls back to
    ``<cwd>/config/vitruvius.yaml``. Kept local to this module so the
    proximity-jump helpers do not pull in the CLI command stack on
    the hot import path.
    """
    env_path = os.environ.get("VITRUVIUS_CONFIG")
    if env_path:
        return Path(env_path)
    return Path.cwd() / "config" / "vitruvius.yaml"


@lru_cache(maxsize=1)
def _load_features_cached() -> Features:
    """Load the feature-flag block once per process.

    The parity test in ``test_proximity_jump_weight_parity.py``
    monkey-patches this function directly, so keep it as a plain
    module-level attribute — do NOT inline the ``load_features``
    call inside ``weight_by_distance`` or the test's flag flip will
    not take effect.
    """
    return load_features(_resolve_config_path())


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

    Two execution paths:

    * **Rust fast path** (``rust_mig_spatial_kernels=true``): delegate
      to ``vitruvius_engine_rs.weight_by_distance`` which runs the
      ``exp(-λd)`` loop in Rust. The Python wrapper marshals each
      seed tuple into the ffi once, then re-zips the returned weight
      list against the original key order to rebuild the ``dict[str,
      float]`` so the return shape is byte-identical to the Python
      path.
    * **Python baseline** (default): ``math.sqrt`` + ``math.exp``
      loop in pure Python. Pre-migration byte-for-byte behaviour.

    The helper is deliberately pure math with no dependency on the
    octree — the caller is expected to already have resolved each
    seed ID back to an ``(x, y, z)`` centroid (via a separate
    snapshot lookup or directly from the octree point cloud).
    """
    # ---- Sprint RUST-MIG-1 Task 5 — Rust fast path. ----
    # Minimal glue: one flag check, one list comprehension to marshal
    # seed tuples into a Rust-friendly `list[(f64, f64, f64)]` in the
    # same order as `seeds.items()`. We keep the key order in a
    # separate list and re-zip the returned weight vec back into a
    # dict so the public return type is unchanged.
    #
    # Flag-OFF short-circuits past this block entirely so the Python
    # path below runs unchanged (non-breaking contract from AD-036).
    #
    # Note: we only walk `seeds.items()` once. Any future editor who
    # tries to hoist `list(seeds.items())` above the branch for a
    # putative "clean up" should NOT — the Python baseline path wants
    # the raw mapping (dict.items() is O(1) in Python 3.7+ and the
    # pure-Python loop iterates it directly).
    if (
        weight_by_distance_rs is not None
        and _load_features_cached().is_enabled("rust_mig_spatial_kernels")
    ):
        seed_ids: list[str] = []
        seed_payload: list[tuple[float, float, float]] = []
        for seed_id, (x, y, z) in seeds.items():
            seed_ids.append(seed_id)
            seed_payload.append((float(x), float(y), float(z)))
        focal_tuple = (
            float(focal_xyz[0]),
            float(focal_xyz[1]),
            float(focal_xyz[2]),
        )
        rust_weights = weight_by_distance_rs(
            seed_payload, focal_tuple, float(lambda_decay)
        )
        return dict(zip(seed_ids, rust_weights))

    # ---- Pure-Python baseline (default). ----
    fx, fy, fz = focal_xyz
    weights: dict[str, float] = {}
    for seed_id, (x, y, z) in seeds.items():
        distance = math.sqrt((x - fx) ** 2 + (y - fy) ** 2 + (z - fz) ** 2)
        weights[seed_id] = math.exp(-lambda_decay * distance)
    return weights


__all__ = ["proximity_jump_seed", "weight_by_distance"]
