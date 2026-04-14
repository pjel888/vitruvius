"""Stream H.1 — centrality overlays."""

from __future__ import annotations

import dataclasses

import pytest

from vitruvius.graph.centrality import CentralityReport, compute_centrality
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


def test_degree_centrality_chain() -> None:
    # a -> b -> c: b is the hub with degree 2, a and c have degree 1
    snap = _snap(
        [_n("concept-a"), _n("concept-b"), _n("concept-c")],
        [
            _e("concept-a", "concept-b", evidence="rel-1"),
            _e("concept-b", "concept-c", evidence="rel-2"),
        ],
    )
    report = compute_centrality(snap, kind="degree")
    assert report.kind == "degree"
    scores = dict(report.scores)
    assert scores["concept-b"] > scores["concept-a"]
    assert scores["concept-b"] > scores["concept-c"]


def test_pagerank_converges_and_sums_to_one() -> None:
    snap = _snap(
        [_n("concept-a"), _n("concept-b"), _n("concept-c")],
        [
            _e("concept-a", "concept-b", evidence="rel-1"),
            _e("concept-b", "concept-c", evidence="rel-2"),
            _e("concept-c", "concept-a", evidence="rel-3"),
        ],
    )
    report = compute_centrality(snap, kind="pagerank")
    assert report.kind == "pagerank"
    total = sum(v for _, v in report.scores)
    assert abs(total - 1.0) < 1e-6


def test_betweenness_bridge_node() -> None:
    # Two triangles joined by a single bridge node b.
    # x - y - b - p - q, with extra edges in each triangle.
    snap = _snap(
        [
            _n("concept-x"),
            _n("concept-y"),
            _n("concept-b"),
            _n("concept-p"),
            _n("concept-q"),
        ],
        [
            _e("concept-x", "concept-y", evidence="rel-1"),
            _e("concept-y", "concept-b", evidence="rel-2"),
            _e("concept-b", "concept-p", evidence="rel-3"),
            _e("concept-p", "concept-q", evidence="rel-4"),
        ],
    )
    report = compute_centrality(snap, kind="betweenness")
    scores = dict(report.scores)
    # Bridge b must have the highest betweenness.
    assert scores["concept-b"] >= max(
        scores["concept-x"],
        scores["concept-y"],
        scores["concept-p"],
        scores["concept-q"],
    )


def test_empty_snapshot_returns_empty_report() -> None:
    snap = _snap([], [])
    report = compute_centrality(snap, kind="pagerank")
    assert report.scores == ()


def test_unknown_kind_raises() -> None:
    snap = _snap([_n("concept-a")], [])
    with pytest.raises(ValueError):
        compute_centrality(snap, kind="banana")  # type: ignore[arg-type]


def test_output_is_deterministic() -> None:
    snap = _snap(
        [_n("concept-a"), _n("concept-b"), _n("concept-c")],
        [
            _e("concept-a", "concept-b", evidence="rel-1"),
            _e("concept-b", "concept-c", evidence="rel-2"),
        ],
    )
    a = compute_centrality(snap, kind="degree")
    b = compute_centrality(snap, kind="degree")
    assert a == b
    assert a.scores == b.scores


def test_centrality_report_frozen() -> None:
    snap = _snap([_n("concept-a")], [])
    report = compute_centrality(snap, kind="degree")
    assert dataclasses.is_dataclass(report)
    with pytest.raises(dataclasses.FrozenInstanceError):
        report.kind = "pagerank"  # type: ignore[misc]


def test_pagerank_alpha_threading() -> None:
    snap = _snap(
        [_n("concept-a"), _n("concept-b"), _n("concept-c")],
        [
            _e("concept-a", "concept-b", evidence="rel-1"),
            _e("concept-b", "concept-c", evidence="rel-2"),
        ],
    )
    low_alpha = compute_centrality(snap, kind="pagerank", alpha=0.1)
    high_alpha = compute_centrality(snap, kind="pagerank", alpha=0.95)
    # Different alphas should yield different distributions.
    assert low_alpha.scores != high_alpha.scores


def test_single_node_snapshot() -> None:
    snap = _snap([_n("concept-lonely")], [])
    report = compute_centrality(snap, kind="pagerank")
    assert len(report.scores) == 1
    assert report.scores[0][0] == "concept-lonely"


def test_stable_tie_break_on_id() -> None:
    # Three isolated nodes → all equal degree 0. Tie-break on id ascending.
    snap = _snap(
        [_n("concept-c"), _n("concept-a"), _n("concept-b")],
        [],
    )
    report = compute_centrality(snap, kind="degree")
    ids = [nid for nid, _ in report.scores]
    assert ids == ["concept-a", "concept-b", "concept-c"]
