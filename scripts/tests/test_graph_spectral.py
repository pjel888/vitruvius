"""Stream H.2 — spectral graph partitioning."""

from __future__ import annotations

import dataclasses

import pytest

from vitruvius.graph.contract import GraphEdge, GraphNode, GraphSnapshot
from vitruvius.graph.spectral import SpectralPartition, compute_spectral_partition


def _n(id_: str) -> GraphNode:
    return GraphNode(
        id=id_,
        type="concept",
        slug=id_.split("-", 1)[-1] or "x",
        trust_level="derived",
        last_updated_utc="2026-04-14T00:00:00Z",
    )


def _e(from_id: str, to_id: str, *, evidence: str = "rel-x") -> GraphEdge:
    return GraphEdge(
        from_id=from_id,
        to_id=to_id,
        type="governs",
        evidence_id=evidence,
        status="verified",
    )


def _snap(nodes: list[GraphNode], edges: list[GraphEdge]) -> GraphSnapshot:
    return GraphSnapshot(
        schema_version="1.0.0",
        generated_at_utc="2026-04-14T00:00:00Z",
        node_count=len(nodes),
        edge_count=len(edges),
        nodes=nodes,
        edges=edges,
    )


def test_two_cluster_graph_partitions_correctly() -> None:
    # Two dense triangles joined by a single bridge edge.
    nodes = [
        _n("concept-a1"), _n("concept-a2"), _n("concept-a3"),
        _n("concept-b1"), _n("concept-b2"), _n("concept-b3"),
    ]
    edges = [
        _e("concept-a1", "concept-a2", evidence="rel-1"),
        _e("concept-a2", "concept-a3", evidence="rel-2"),
        _e("concept-a3", "concept-a1", evidence="rel-3"),
        _e("concept-b1", "concept-b2", evidence="rel-4"),
        _e("concept-b2", "concept-b3", evidence="rel-5"),
        _e("concept-b3", "concept-b1", evidence="rel-6"),
        _e("concept-a1", "concept-b1", evidence="rel-7"),
    ]
    snap = _snap(nodes, edges)
    part = compute_spectral_partition(snap)
    all_a = {"concept-a1", "concept-a2", "concept-a3"}
    all_b = {"concept-b1", "concept-b2", "concept-b3"}
    set_a = set(part.partition_a)
    set_b = set(part.partition_b)
    assert set_a | set_b == all_a | all_b
    # The two triangles should land on opposite signs.
    assert set_a == all_a or set_a == all_b
    assert set_b == all_a or set_b == all_b


def test_fiedler_value_non_negative() -> None:
    snap = _snap(
        [_n("concept-a"), _n("concept-b"), _n("concept-c")],
        [
            _e("concept-a", "concept-b", evidence="rel-1"),
            _e("concept-b", "concept-c", evidence="rel-2"),
        ],
    )
    part = compute_spectral_partition(snap)
    assert part.fiedler_value >= -1e-9


def test_empty_snapshot_raises() -> None:
    snap = _snap([], [])
    with pytest.raises(ValueError):
        compute_spectral_partition(snap)


def test_single_node_raises() -> None:
    snap = _snap([_n("concept-lonely")], [])
    with pytest.raises(ValueError):
        compute_spectral_partition(snap)


def test_disconnected_graph_fiedler_near_zero() -> None:
    snap = _snap(
        [
            _n("concept-a"), _n("concept-b"),
            _n("concept-c"), _n("concept-d"),
        ],
        [
            _e("concept-a", "concept-b", evidence="rel-1"),
            _e("concept-c", "concept-d", evidence="rel-2"),
        ],
    )
    part = compute_spectral_partition(snap)
    assert abs(part.fiedler_value) < 1e-6


def test_deterministic_output() -> None:
    snap = _snap(
        [
            _n("concept-a"), _n("concept-b"),
            _n("concept-c"), _n("concept-d"),
        ],
        [
            _e("concept-a", "concept-b", evidence="rel-1"),
            _e("concept-b", "concept-c", evidence="rel-2"),
            _e("concept-c", "concept-d", evidence="rel-3"),
        ],
    )
    a = compute_spectral_partition(snap)
    b = compute_spectral_partition(snap)
    # Partitions may flip signs on rerun, so compare unordered set pairs.
    assert {a.partition_a, a.partition_b} == {b.partition_a, b.partition_b}
    assert abs(a.fiedler_value - b.fiedler_value) < 1e-9


def test_partition_sizes_sum_to_node_count() -> None:
    snap = _snap(
        [
            _n("concept-a"), _n("concept-b"),
            _n("concept-c"), _n("concept-d"),
        ],
        [
            _e("concept-a", "concept-b", evidence="rel-1"),
            _e("concept-c", "concept-d", evidence="rel-2"),
            _e("concept-b", "concept-c", evidence="rel-3"),
        ],
    )
    part = compute_spectral_partition(snap)
    assert len(part.partition_a) + len(part.partition_b) == 4
    assert dataclasses.is_dataclass(part)
    with pytest.raises(dataclasses.FrozenInstanceError):
        part.fiedler_value = 0.0  # type: ignore[misc]
