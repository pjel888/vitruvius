"""Phase 9 Task 2 — structured query engine."""

from __future__ import annotations

from vitruvius.graph.contract import GraphEdge, GraphNode, GraphSnapshot
from vitruvius.query.engine import (
    edges_between,
    neighbors_query,
    supersession_chain,
    what_affects,
    what_defines,
    what_depends_on,
    what_governs,
    what_limits,
    what_requires,
)


def _n(id_: str, *, type_: str = "concept", trust: str = "derived") -> GraphNode:
    return GraphNode(
        id=id_,
        type=type_,
        slug=id_.split("-", 1)[-1] or "x",
        trust_level=trust,
        last_updated_utc="2026-04-14T00:00:00Z",
    )


def _e(
    from_id: str,
    to_id: str,
    *,
    type_: str,
    evidence: str,
    status: str = "verified",
    source_id: str | None = None,
    section: str | None = "sec-1",
    snippet: str | None = "Snippet",
    confidence: float | None = 0.92,
) -> GraphEdge:
    return GraphEdge(
        from_id=from_id,
        to_id=to_id,
        type=type_,
        evidence_id=evidence,
        status=status,
        evidence_source_id=source_id or from_id,
        evidence_source_section_id=section,
        evidence_snippet=snippet,
        reviewer_confidence=confidence,
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


def test_what_governs_returns_source_and_citation() -> None:
    snap = _snap(
        [_n("law-pd-1096", type_="source", trust="primary"),
         _n("concept-building-permit")],
        [_e("law-pd-1096", "concept-building-permit", type_="governs",
            evidence="rel-1")],
    )
    result = what_governs("concept-building-permit", snap)
    assert result.has_evidence is True
    assert result.answer_entities == ("law-pd-1096",)
    assert len(result.citations) == 1
    assert result.citations[0].source_id == "law-pd-1096"
    assert result.query_function == "what_governs"
    assert result.arguments == {"subject": "concept-building-permit"}


def test_what_governs_no_evidence_case() -> None:
    snap = _snap(
        [_n("law-x", type_="source", trust="primary"), _n("concept-x")],
        [_e("law-x", "concept-x", type_="governs", evidence="rel-1", section=None, snippet=None, confidence=None)],
    )
    result = what_governs("concept-x", snap)
    assert result.has_evidence is False
    assert result.answer_entities == ("law-x",)
    assert result.citations == ()
    assert result.aggregate_confidence == 0.0


def test_what_requires_direction() -> None:
    snap = _snap(
        [_n("concept-a"), _n("concept-b"), _n("concept-c")],
        [
            _e("concept-a", "concept-b", type_="requires", evidence="rel-1"),
            _e("concept-a", "concept-c", type_="requires", evidence="rel-2"),
            # Reverse direction should not match.
            _e("concept-c", "concept-a", type_="requires", evidence="rel-3"),
        ],
    )
    result = what_requires("concept-a", snap)
    assert result.answer_entities == ("concept-b", "concept-c")
    assert len(result.citations) == 2


def test_what_limits_incoming_edges() -> None:
    snap = _snap(
        [_n("law-x", type_="source", trust="primary"), _n("concept-lot")],
        [_e("law-x", "concept-lot", type_="limits", evidence="rel-1")],
    )
    result = what_limits("concept-lot", snap)
    assert result.answer_entities == ("law-x",)
    assert result.citations[0].confidence == 0.92


def test_what_defines_verified_vs_unverified_confidence() -> None:
    snap = _snap(
        [_n("law-x", type_="source", trust="primary"),
         _n("concept-frc")],
        [_e("law-x", "concept-frc", type_="defines",
            evidence="rel-1", status="unverified")],
    )
    result = what_defines("concept-frc", snap)
    assert result.citations[0].confidence == 0.92
    assert result.aggregate_confidence == 0.92


def test_query_omits_placeholder_citations_without_real_provenance() -> None:
    snap = _snap(
        [_n("law-x", type_="source", trust="primary"), _n("concept-y")],
        [_e("law-x", "concept-y", type_="governs", evidence="rel-1", section="", snippet="", confidence=None)],
    )
    result = what_governs("concept-y", snap)
    assert result.has_evidence is False
    assert result.citations == ()


def test_what_depends_on_from_subject() -> None:
    snap = _snap(
        [_n("concept-a"), _n("concept-b")],
        [_e("concept-a", "concept-b", type_="depends_on", evidence="rel-1")],
    )
    result = what_depends_on("concept-a", snap)
    assert result.answer_entities == ("concept-b",)


def test_what_affects_is_symmetric() -> None:
    snap = _snap(
        [_n("concept-a"), _n("concept-b"), _n("concept-c")],
        [
            _e("concept-a", "concept-b", type_="affects", evidence="rel-1"),
            _e("concept-c", "concept-a", type_="affects", evidence="rel-2"),
        ],
    )
    result = what_affects("concept-a", snap)
    assert set(result.answer_entities) == {"concept-b", "concept-c"}
    assert len(result.citations) == 2


def test_supersession_chain_transitive() -> None:
    snap = _snap(
        [_n("law-a", type_="source", trust="primary"),
         _n("law-b", type_="source", trust="primary"),
         _n("law-c", type_="source", trust="primary")],
        [
            _e("law-a", "law-b", type_="supersedes", evidence="rel-1"),
            _e("law-b", "law-c", type_="supersedes", evidence="rel-2"),
        ],
    )
    result = supersession_chain("law-a", snap)
    assert result.answer_entities == ("law-b", "law-c")
    assert len(result.citations) == 2


def test_supersession_chain_no_chain() -> None:
    snap = _snap(
        [_n("law-a", type_="source", trust="primary")],
        [],
    )
    result = supersession_chain("law-a", snap)
    assert result.has_evidence is False
    assert result.answer_entities == ()


def test_neighbors_query_all_and_filtered() -> None:
    snap = _snap(
        [_n("concept-a"), _n("concept-b"), _n("concept-c")],
        [
            _e("concept-a", "concept-b", type_="requires", evidence="rel-1"),
            _e("concept-c", "concept-a", type_="governs", evidence="rel-2"),
        ],
    )
    all_neighbors = neighbors_query("concept-a", snap)
    assert set(all_neighbors.answer_entities) == {"concept-b", "concept-c"}
    filtered = neighbors_query("concept-a", snap, predicate="requires")
    assert filtered.answer_entities == ("concept-b",)
    assert filtered.arguments == {
        "subject": "concept-a",
        "predicate": "requires",
    }


def test_edges_between_bidirectional() -> None:
    snap = _snap(
        [_n("concept-a"), _n("concept-b")],
        [
            _e("concept-a", "concept-b", type_="requires", evidence="rel-1"),
            _e("concept-b", "concept-a", type_="affects", evidence="rel-2"),
        ],
    )
    result = edges_between("concept-a", "concept-b", snap)
    assert len(result.citations) == 2
    assert set(result.answer_entities) == {"concept-a", "concept-b"}


def test_edges_between_none_returns_empty() -> None:
    snap = _snap([_n("concept-a"), _n("concept-b")], [])
    result = edges_between("concept-a", "concept-b", snap)
    assert result.has_evidence is False
    assert result.citations == ()
