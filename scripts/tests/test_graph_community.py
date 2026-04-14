"""Stream H.3 — Louvain community detection."""

from __future__ import annotations

import dataclasses

import pytest

from vitruvius.graph.community import Community, CommunityReport, detect_communities
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


def test_disconnected_components_become_separate_communities() -> None:
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
    report = detect_communities(snap)
    assert len(report.communities) >= 2
    all_nodes: set[str] = set()
    for c in report.communities:
        all_nodes.update(c.node_ids)
    assert all_nodes == {"concept-a", "concept-b", "concept-c", "concept-d"}


def test_connected_clique_is_one_community() -> None:
    nodes = [_n(f"concept-{c}") for c in "abcd"]
    edges = [
        _e("concept-a", "concept-b", evidence="rel-1"),
        _e("concept-a", "concept-c", evidence="rel-2"),
        _e("concept-a", "concept-d", evidence="rel-3"),
        _e("concept-b", "concept-c", evidence="rel-4"),
        _e("concept-b", "concept-d", evidence="rel-5"),
        _e("concept-c", "concept-d", evidence="rel-6"),
    ]
    snap = _snap(nodes, edges)
    report = detect_communities(snap)
    assert len(report.communities) == 1
    assert set(report.communities[0].node_ids) == {
        "concept-a", "concept-b", "concept-c", "concept-d",
    }


def test_empty_snapshot_returns_empty_report() -> None:
    snap = _snap([], [])
    report = detect_communities(snap)
    assert report.communities == ()
    assert report.modularity == 0.0


def test_modularity_non_negative_for_clustered_graph() -> None:
    nodes = [_n(f"concept-{c}") for c in ["a1", "a2", "a3", "b1", "b2", "b3"]]
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
    report = detect_communities(snap)
    assert report.modularity >= 0.0


def test_deterministic_via_seed() -> None:
    nodes = [_n(f"concept-{c}") for c in "abcdef"]
    edges = [
        _e("concept-a", "concept-b", evidence="rel-1"),
        _e("concept-b", "concept-c", evidence="rel-2"),
        _e("concept-d", "concept-e", evidence="rel-3"),
        _e("concept-e", "concept-f", evidence="rel-4"),
    ]
    snap = _snap(nodes, edges)
    a = detect_communities(snap, random_state=42)
    b = detect_communities(snap, random_state=42)
    assert a == b


def test_community_frozen() -> None:
    snap = _snap([_n("concept-a"), _n("concept-b")],
                 [_e("concept-a", "concept-b", evidence="rel-1")])
    report = detect_communities(snap)
    assert dataclasses.is_dataclass(Community)
    with pytest.raises(dataclasses.FrozenInstanceError):
        report.communities[0].community_id = 999  # type: ignore[misc]


def test_node_ids_sorted() -> None:
    nodes = [_n(f"concept-{c}") for c in "zyxwv"]
    edges = [
        _e("concept-z", "concept-y", evidence="rel-1"),
        _e("concept-y", "concept-x", evidence="rel-2"),
        _e("concept-x", "concept-w", evidence="rel-3"),
        _e("concept-w", "concept-v", evidence="rel-4"),
    ]
    snap = _snap(nodes, edges)
    report = detect_communities(snap)
    for c in report.communities:
        assert list(c.node_ids) == sorted(c.node_ids)


def test_summary_is_string() -> None:
    snap = _snap(
        [_n("concept-a"), _n("concept-b"), _n("concept-c")],
        [
            _e("concept-a", "concept-b", evidence="rel-1"),
            _e("concept-b", "concept-c", evidence="rel-2"),
        ],
    )
    report = detect_communities(snap)
    for c in report.communities:
        assert isinstance(c.summary, str)
        assert c.summary.startswith("Community ")
