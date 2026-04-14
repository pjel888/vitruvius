"""Stream PHYS.4 — eigenvector centrality + cascade simulator + impact radius."""
from __future__ import annotations

import pytest

from vitruvius.graph.contract import GraphEdge, GraphNode, GraphSnapshot
from vitruvius.graph.physics import (
    CascadeReport,
    EigenvectorReport,
    compute_eigenvector_centrality,
    find_impact_radius,
    simulate_cascade,
)


def _n(id_: str) -> GraphNode:
    return GraphNode(
        id=id_,
        type="concept",
        slug=id_.split("-", 1)[-1],
        trust_level="derived",
        last_updated_utc="2026-04-15T00:00:00Z",
    )


def _e(from_id: str, to_id: str, evidence_id: str) -> GraphEdge:
    return GraphEdge(
        from_id=from_id,
        to_id=to_id,
        type="governs",
        evidence_id=evidence_id,
        status="verified",
    )


def _snapshot(nodes: list[GraphNode], edges: list[GraphEdge]) -> GraphSnapshot:
    return GraphSnapshot(
        schema_version="1.0.0",
        generated_at_utc="2026-04-15T00:00:00Z",
        node_count=len(nodes),
        edge_count=len(edges),
        nodes=nodes,
        edges=edges,
    )


# ---------------------------------------------------------------------------
# Eigenvector centrality
# ---------------------------------------------------------------------------
def test_empty_snapshot_eigenvector_is_empty() -> None:
    report = compute_eigenvector_centrality(_snapshot([], []))
    assert isinstance(report, EigenvectorReport)
    assert report.scores == {}


def test_load_bearing_node_has_highest_score() -> None:
    """A node connected to every other node is the structural anchor."""
    nodes = [_n("concept-hub")] + [_n(f"concept-c{i}") for i in range(6)]
    edges = []
    for i in range(6):
        edges.append(_e("concept-hub", f"concept-c{i}", evidence_id=f"rel-out-{i}"))
        edges.append(_e(f"concept-c{i}", "concept-hub", evidence_id=f"rel-in-{i}"))
    report = compute_eigenvector_centrality(_snapshot(nodes, edges))
    hub_score = report.scores["concept-hub"]
    for i in range(6):
        assert hub_score >= report.scores[f"concept-c{i}"]


# ---------------------------------------------------------------------------
# Cascade simulator
# ---------------------------------------------------------------------------
def test_cascade_from_isolated_node_is_single_node() -> None:
    nodes = [_n("a"), _n("b")]
    edges: list[GraphEdge] = []
    report = simulate_cascade(_snapshot(nodes, edges), focal_node="a")
    assert isinstance(report, CascadeReport)
    assert report.affected_nodes == {"a"}
    assert report.affected_fraction == pytest.approx(0.5)


def test_cascade_covers_reachable_descendants() -> None:
    nodes = [_n("a"), _n("b"), _n("c"), _n("d")]
    edges = [
        _e("a", "b", evidence_id="rel-1"),
        _e("b", "c", evidence_id="rel-2"),
        # d is not reachable from a
    ]
    report = simulate_cascade(_snapshot(nodes, edges), focal_node="a")
    # undirected cascade: a, b, c are connected; d is isolated
    assert "a" in report.affected_nodes
    assert "b" in report.affected_nodes
    assert "c" in report.affected_nodes
    assert "d" not in report.affected_nodes
    assert report.affected_fraction == pytest.approx(0.75)


# ---------------------------------------------------------------------------
# Impact radius
# ---------------------------------------------------------------------------
def test_impact_radius_returns_top_k_neighbors() -> None:
    nodes = [_n("center")] + [_n(f"c{i}") for i in range(5)]
    edges = [
        _e("center", f"c{i}", evidence_id=f"rel-{i}") for i in range(5)
    ]
    # Extra edges making c0 and c1 higher-influence
    edges.append(_e("c0", "c1", evidence_id="rel-extra-1"))
    edges.append(_e("c1", "c0", evidence_id="rel-extra-2"))

    neighbors = find_impact_radius(
        _snapshot(nodes, edges),
        focal_node="center",
        k=3,
    )
    assert len(neighbors) == 3
    assert "center" not in neighbors  # focal node itself is excluded
