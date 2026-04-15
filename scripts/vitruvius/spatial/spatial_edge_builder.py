"""Sprint GT Stream GT.4.3 — ``physically_adjacent_to`` edge generator.

For every pair of spatial points whose AABBs intersect (or touch
on a shared face), this module emits one edge with the predicate
``physically_adjacent_to``. The builder has two implementations:

* **Pure-Python O(n^2)** — the original Sprint GT baseline, a
  nested-pair AABB intersection loop. Still the default path.
* **Rust O(n log n)** — Sprint RUST-MIG-1 Task 4, gated by the
  ``rust_mig_spatial_kernels`` feature flag (default ``false``).
  Delegates the hot work to ``vitruvius_engine_rs`` which reuses
  the `LinearOctree` from Sprint GT.2 as a spatial index over
  AABB centroids, reducing the pair scan from O(n^2) to expected
  O(n log n + k). See the Rust source at
  ``engine_rs/spatial_kernels/src/adjacency_edges.rs`` for the
  full algorithm + correctness argument.

The snapshot builder is expected to call this function only when
``config.features.gt_spatial_edges`` is true. The Rust fast path
is a further opt-in — flag-OFF is byte-identical to the pre-
migration Python-only behaviour.

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

import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any, Iterable

# Sprint RUST-MIG-1 Task 4 — import the Rust fast path lazily.
# The ``vitruvius.engine_rs`` facade returns ``None`` when the
# extension module is not built, so the fast-path guard below is
# a pure attribute check with no ImportError risk at call time.
from vitruvius.engine_rs import build_spatial_adjacency_edges_rs
from vitruvius.features import Features, load_features


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


def _resolve_config_path() -> Path:
    """Mirror of ``vitruvius.spatial.cli._resolve_config_path``.

    Honours ``VITRUVIUS_CONFIG`` for hermetic tests, falls back to
    ``<cwd>/config/vitruvius.yaml``. Kept local to this module so the
    spatial edge builder does not pull in the CLI command stack on
    the hot import path.
    """
    env_path = os.environ.get("VITRUVIUS_CONFIG")
    if env_path:
        return Path(env_path)
    return Path.cwd() / "config" / "vitruvius.yaml"


@lru_cache(maxsize=1)
def _load_features_cached() -> Features:
    """Load the feature-flag block once per process.

    The parity test in ``test_spatial_edge_builder_parity.py``
    monkey-patches this function directly, so keep it as a plain
    module-level attribute — do NOT inline the ``load_features``
    call inside ``build_spatial_adjacency_edges`` or the test's
    flag flip will not take effect.
    """
    return load_features(_resolve_config_path())


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

    Two execution paths:

    * **Rust fast path** (``rust_mig_spatial_kernels=true``): delegate
      to ``vitruvius_engine_rs.build_spatial_adjacency_edges`` which
      runs an octree-backed O(n log n + k) scan over centroids
      followed by an exact AABB re-test per candidate. Each returned
      ``(id_i, id_j)`` pair is wrapped in a ``SpatialEdge`` dataclass
      with the canonical ``physically_adjacent_to`` predicate so the
      return shape is byte-identical to the Python path.
    * **Python baseline** (default): nested O(n^2) pair loop. Edges
      are emitted in input order — if ``points[i]`` precedes
      ``points[j]`` and their AABBs intersect, the edge is
      ``SpatialEdge(from_id=points[i].id, to_id=points[j].id)``.

    The Rust path is order-independent: edges may come back in a
    different sequence than the Python loop would emit, but the
    *set* of unordered ``(from_id, to_id)`` pairs is identical. No
    downstream consumer depends on the emission order of the Python
    path (the predicate is symmetric), so swapping paths via the
    feature flag is a safe behaviour-preserving swap.
    """
    # ---- Sprint RUST-MIG-1 Task 4 — Rust fast path. ----
    # Minimal glue: one flag check, one list-comprehension to marshal
    # nodes. The Python wrapper must NOT pre-compute anything the
    # Rust kernel could do — that would defeat the O(n log n) win.
    # Flag-OFF short-circuits past this block entirely so the Python
    # path below runs unchanged (non-breaking contract from AD-036).
    if (
        build_spatial_adjacency_edges_rs is not None
        and _load_features_cached().is_enabled("rust_mig_spatial_kernels")
    ):
        materialised = list(points)
        nodes_payload = [
            (
                p.id,
                [
                    float(p.aabb.min_xyz[0]),
                    float(p.aabb.min_xyz[1]),
                    float(p.aabb.min_xyz[2]),
                    float(p.aabb.max_xyz[0]),
                    float(p.aabb.max_xyz[1]),
                    float(p.aabb.max_xyz[2]),
                ],
            )
            for p in materialised
        ]
        rust_pairs = build_spatial_adjacency_edges_rs(nodes_payload)
        return [
            SpatialEdge(from_id=from_id, to_id=to_id)
            for from_id, to_id in rust_pairs
        ]

    # ---- Pure-Python baseline (default). ----
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
