"""Stream H.7 — causal DAG intervention overlay."""

from __future__ import annotations

import dataclasses

import pytest

from vitruvius.graph.causal_dag import (
    CyclicGraphError,
    InterventionResult,
    assert_is_dag,
    intervention,
)
from vitruvius.graph.contract import GraphEdge, GraphNode, GraphSnapshot


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


def test_dag_with_clear_descendants() -> None:
    # a -> b -> c, a -> d
    snap = _snap(
        [_n("concept-a"), _n("concept-b"), _n("concept-c"), _n("concept-d")],
        [
            _e("concept-a", "concept-b", evidence="rel-1"),
            _e("concept-b", "concept-c", evidence="rel-2"),
            _e("concept-a", "concept-d", evidence="rel-3"),
        ],
    )
    assert_is_dag(snap)
    result = intervention(snap, node_id="concept-a", value=1.0)
    assert set(result.descendants_affected) == {
        "concept-b", "concept-c", "concept-d",
    }


def test_cyclic_graph_raises() -> None:
    snap = _snap(
        [_n("concept-a"), _n("concept-b"), _n("concept-c")],
        [
            _e("concept-a", "concept-b", evidence="rel-1"),
            _e("concept-b", "concept-c", evidence="rel-2"),
            _e("concept-c", "concept-a", evidence="rel-3"),
        ],
    )
    with pytest.raises(CyclicGraphError):
        assert_is_dag(snap)
    with pytest.raises(CyclicGraphError):
        intervention(snap, node_id="concept-a", value=1.0)


def test_unknown_node_raises() -> None:
    snap = _snap([_n("concept-a")], [])
    with pytest.raises(KeyError):
        intervention(snap, node_id="concept-ghost", value=1.0)


def test_leaf_intervention_has_no_descendants() -> None:
    snap = _snap(
        [_n("concept-a"), _n("concept-b"), _n("concept-c")],
        [
            _e("concept-a", "concept-b", evidence="rel-1"),
            _e("concept-b", "concept-c", evidence="rel-2"),
        ],
    )
    result = intervention(snap, node_id="concept-c", value=0.5)
    assert result.descendants_affected == ()


def test_root_intervention_affects_everything() -> None:
    nodes = [_n(f"concept-{c}") for c in "abcd"]
    edges = [
        _e("concept-a", "concept-b", evidence="rel-1"),
        _e("concept-a", "concept-c", evidence="rel-2"),
        _e("concept-b", "concept-d", evidence="rel-3"),
    ]
    snap = _snap(nodes, edges)
    result = intervention(snap, node_id="concept-a", value=1.0)
    assert set(result.descendants_affected) == {
        "concept-b", "concept-c", "concept-d",
    }


def test_frozen_return() -> None:
    snap = _snap(
        [_n("concept-a"), _n("concept-b")],
        [_e("concept-a", "concept-b", evidence="rel-1")],
    )
    result = intervention(snap, node_id="concept-a", value=1.0)
    assert dataclasses.is_dataclass(result)
    with pytest.raises(dataclasses.FrozenInstanceError):
        result.intervention_value = 99.0  # type: ignore[misc]
    assert isinstance(result, InterventionResult)


def test_deterministic_sorted_descendants() -> None:
    nodes = [_n(f"concept-{c}") for c in ["z", "y", "x", "w"]]
    edges = [
        _e("concept-w", "concept-z", evidence="rel-1"),
        _e("concept-w", "concept-y", evidence="rel-2"),
        _e("concept-w", "concept-x", evidence="rel-3"),
    ]
    snap = _snap(nodes, edges)
    result = intervention(snap, node_id="concept-w", value=1.0)
    assert list(result.descendants_affected) == sorted(result.descendants_affected)
    assert list(result.descendants_affected) == ["concept-x", "concept-y", "concept-z"]
