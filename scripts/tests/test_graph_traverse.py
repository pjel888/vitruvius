"""Phase 8 Task 6 — traversal helpers."""

from __future__ import annotations

from vitruvius.graph.contract import GraphEdge, GraphNode, GraphSnapshot
from vitruvius.graph.traverse import (
    evidence_joined_paths,
    neighbors,
    typed_edges,
)


def _n(id_: str) -> GraphNode:
    return GraphNode(
        id=id_,
        type="concept",
        slug=id_.split("-", 1)[-1] or "x",
        trust_level="derived",
        last_updated_utc="2026-04-14T00:00:00Z",
    )


def _e(from_id: str, to_id: str, *, type_: str = "governs",
       evidence: str = "rel-x") -> GraphEdge:
    return GraphEdge(
        from_id=from_id,
        to_id=to_id,
        type=type_,
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


def test_out_neighbors() -> None:
    snap = _snap(
        [_n("concept-a"), _n("concept-b"), _n("concept-c")],
        [
            _e("concept-a", "concept-b", evidence="rel-1"),
            _e("concept-a", "concept-c", evidence="rel-2"),
        ],
    )
    result = neighbors(snap, "concept-a", direction="out")
    assert [n.id for n in result] == ["concept-b", "concept-c"]


def test_in_neighbors() -> None:
    snap = _snap(
        [_n("concept-a"), _n("concept-b"), _n("concept-c")],
        [
            _e("concept-b", "concept-a", evidence="rel-1"),
            _e("concept-c", "concept-a", evidence="rel-2"),
        ],
    )
    result = neighbors(snap, "concept-a", direction="in")
    assert [n.id for n in result] == ["concept-b", "concept-c"]


def test_both_direction_neighbors_deduped() -> None:
    snap = _snap(
        [_n("concept-a"), _n("concept-b")],
        [
            _e("concept-a", "concept-b", evidence="rel-1"),
            _e("concept-b", "concept-a", evidence="rel-2"),
        ],
    )
    result = neighbors(snap, "concept-a", direction="both")
    assert [n.id for n in result] == ["concept-b"]


def test_neighbors_unknown_node_returns_empty() -> None:
    snap = _snap([_n("concept-a")], [])
    assert neighbors(snap, "concept-ghost", direction="out") == []


def test_typed_edges_filters_by_predicate() -> None:
    snap = _snap(
        [_n("concept-a"), _n("concept-b"), _n("concept-c")],
        [
            _e("concept-a", "concept-b", type_="governs", evidence="rel-1"),
            _e("concept-a", "concept-c", type_="affects", evidence="rel-2"),
            _e("concept-c", "concept-a", type_="governs", evidence="rel-3"),
        ],
    )
    result = typed_edges(snap, "concept-a", "governs")
    assert len(result) == 2
    ids = {e.evidence_id for e in result}
    assert ids == {"rel-1", "rel-3"}


def test_evidence_joined_paths_one_hop() -> None:
    snap = _snap(
        [_n("concept-a"), _n("concept-b")],
        [_e("concept-a", "concept-b", evidence="rel-1")],
    )
    paths = evidence_joined_paths(snap, "concept-a", "concept-b")
    assert len(paths) == 1
    assert len(paths[0]) == 1
    assert paths[0][0].evidence_id == "rel-1"


def test_evidence_joined_paths_two_hop() -> None:
    snap = _snap(
        [_n("concept-a"), _n("concept-b"), _n("concept-c")],
        [
            _e("concept-a", "concept-b", evidence="rel-1"),
            _e("concept-b", "concept-c", evidence="rel-2"),
        ],
    )
    paths = evidence_joined_paths(snap, "concept-a", "concept-c")
    assert len(paths) == 1
    assert [e.evidence_id for e in paths[0]] == ["rel-1", "rel-2"]


def test_evidence_joined_paths_no_path() -> None:
    snap = _snap(
        [_n("concept-a"), _n("concept-b")],
        [],
    )
    assert evidence_joined_paths(snap, "concept-a", "concept-b") == []


def test_evidence_joined_paths_max_depth_cap() -> None:
    # a -> b -> c -> d
    snap = _snap(
        [_n("concept-a"), _n("concept-b"), _n("concept-c"), _n("concept-d")],
        [
            _e("concept-a", "concept-b", evidence="rel-1"),
            _e("concept-b", "concept-c", evidence="rel-2"),
            _e("concept-c", "concept-d", evidence="rel-3"),
        ],
    )
    assert evidence_joined_paths(
        snap, "concept-a", "concept-d", max_depth=2
    ) == []
    paths = evidence_joined_paths(snap, "concept-a", "concept-d", max_depth=3)
    assert len(paths) == 1
    assert len(paths[0]) == 3


def test_evidence_joined_paths_self_loop_handled() -> None:
    snap = _snap(
        [_n("concept-a")],
        [_e("concept-a", "concept-a", evidence="rel-self")],
    )
    paths = evidence_joined_paths(snap, "concept-a", "concept-a")
    # from == to is a trivial zero-length path; we return [] (no edges traversed)
    assert paths == []


def test_evidence_joined_paths_deterministic() -> None:
    # diamond: a -> b -> d, a -> c -> d
    snap = _snap(
        [_n("concept-a"), _n("concept-b"), _n("concept-c"), _n("concept-d")],
        [
            _e("concept-a", "concept-c", evidence="rel-ac"),
            _e("concept-a", "concept-b", evidence="rel-ab"),
            _e("concept-b", "concept-d", evidence="rel-bd"),
            _e("concept-c", "concept-d", evidence="rel-cd"),
        ],
    )
    a = evidence_joined_paths(snap, "concept-a", "concept-d")
    b = evidence_joined_paths(snap, "concept-a", "concept-d")
    assert a == b
    assert len(a) == 2
