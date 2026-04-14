"""Stream PHYS.1 — PageRank statutory authority engine tests."""
from __future__ import annotations

import pytest

from vitruvius.graph.contract import GraphEdge, GraphNode, GraphSnapshot
from vitruvius.graph.physics import (
    PageRankReport,
    compute_pagerank,
    resolve_conflict_by_pagerank,
)


def _n(id_: str, type_: str = "concept") -> GraphNode:
    return GraphNode(
        id=id_,
        type=type_,
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


def test_empty_snapshot_returns_empty_report() -> None:
    report = compute_pagerank(_snapshot([], []))
    assert isinstance(report, PageRankReport)
    assert report.scores == {}
    assert report.alpha == 0.85


def test_single_hub_has_highest_score() -> None:
    """A node that every other node points to should beat every other node."""
    nodes = [_n("law-pd-1096", type_="source")]
    for i in range(5):
        nodes.append(_n(f"concept-c{i}"))
    edges = [
        _e(f"concept-c{i}", "law-pd-1096", evidence_id=f"rel-hub-{i}")
        for i in range(5)
    ]
    report = compute_pagerank(_snapshot(nodes, edges))
    hub_score = report.scores["law-pd-1096"]
    for i in range(5):
        assert hub_score > report.scores[f"concept-c{i}"], (
            f"hub score {hub_score} should beat leaf concept-c{i} "
            f"score {report.scores[f'concept-c{i}']}"
        )


def test_scores_sum_to_one() -> None:
    nodes = [_n("a", type_="concept"), _n("b", type_="concept"), _n("c", type_="concept")]
    edges = [
        _e("a", "b", evidence_id="rel-1"),
        _e("b", "c", evidence_id="rel-2"),
        _e("c", "a", evidence_id="rel-3"),
    ]
    report = compute_pagerank(_snapshot(nodes, edges))
    assert sum(report.scores.values()) == pytest.approx(1.0, abs=1e-6)


def test_custom_alpha_is_respected() -> None:
    nodes = [_n("a"), _n("b")]
    edges = [_e("a", "b", evidence_id="rel-1")]
    report = compute_pagerank(_snapshot(nodes, edges), alpha=0.5)
    assert report.alpha == 0.5


def test_resolve_conflict_picks_higher_pagerank() -> None:
    """Given two edges touching different sources, the one whose source
    has a higher PageRank score wins."""
    nodes = [
        _n("law-pd-1096", type_="source"),
        _n("law-lgu-quezon-city", type_="source"),
        _n("concept-zone-r1"),
    ]
    # PD 1096 is heavily cited; the LGU ordinance is not.
    edges = [
        _e("concept-zone-r1", "law-pd-1096", evidence_id="rel-a"),
        _e("concept-zone-r1", "law-pd-1096", evidence_id="rel-b"),
        _e("concept-zone-r1", "law-pd-1096", evidence_id="rel-c"),
        _e("concept-zone-r1", "law-lgu-quezon-city", evidence_id="rel-d"),
    ]
    snap = _snapshot(nodes, edges)

    winner = resolve_conflict_by_pagerank(
        snap,
        node_a="law-pd-1096",
        node_b="law-lgu-quezon-city",
    )
    assert winner == "law-pd-1096"
