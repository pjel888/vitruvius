"""Phase 9 Task 3 — aggregate_confidence helper wired into engine functions."""

from __future__ import annotations

from vitruvius.graph.contract import GraphEdge, GraphNode, GraphSnapshot
from vitruvius.query.engine import (
    what_defines,
    what_governs,
    what_limits,
    what_requires,
)
from vitruvius.query.result import QueryCitation, compute_aggregate_confidence


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
    section: str = "sec-1",
    snippet: str = "Snippet",
    confidence: float | None = None,
) -> GraphEdge:
    return GraphEdge(
        from_id=from_id,
        to_id=to_id,
        type=type_,
        evidence_id=evidence,
        status=status,
        evidence_source_id=from_id,
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


def test_compute_aggregate_confidence_single_citation() -> None:
    cite = QueryCitation(
        source_id="law-x",
        source_section_id="sec-1",
        evidence_snippet="",
        confidence=0.7,
    )
    assert compute_aggregate_confidence((cite,)) == 0.7


def test_compute_aggregate_confidence_picks_minimum() -> None:
    cs = (
        QueryCitation("law-a", "s1", "", 0.95),
        QueryCitation("law-b", "s2", "", 0.30),
        QueryCitation("law-c", "s3", "", 0.60),
    )
    assert compute_aggregate_confidence(cs) == 0.30


def test_compute_aggregate_confidence_empty_returns_zero() -> None:
    assert compute_aggregate_confidence(()) == 0.0


def test_engine_what_governs_aggregate_all_verified() -> None:
    snap = _snap(
        [_n("law-a", type_="source", trust="primary"),
         _n("law-b", type_="source", trust="primary"),
         _n("concept-x")],
        [
            _e("law-a", "concept-x", type_="governs", evidence="rel-1"),
            _e("law-b", "concept-x", type_="governs", evidence="rel-2"),
        ],
    )
    result = what_governs("concept-x", snap)
    assert result.aggregate_confidence == 1.0


def test_engine_what_governs_aggregate_min_mixed_status() -> None:
    snap = _snap(
        [_n("law-a", type_="source", trust="primary"),
         _n("law-b", type_="source", trust="primary"),
         _n("concept-x")],
        [
            _e("law-a", "concept-x", type_="governs", evidence="rel-1",
               status="verified"),
            _e("law-b", "concept-x", type_="governs", evidence="rel-2",
               status="unverified"),
        ],
    )
    result = what_governs("concept-x", snap)
    # One verified (1.0) + one unverified (0.5) => min = 0.5
    assert result.aggregate_confidence == 0.5


def test_engine_empty_result_aggregate_is_zero() -> None:
    snap = _snap([_n("concept-x")], [])
    result = what_limits("concept-x", snap)
    assert result.has_evidence is False
    assert result.aggregate_confidence == 0.0


def test_engine_all_unverified_aggregate_half() -> None:
    snap = _snap(
        [_n("law-a", type_="source", trust="primary"), _n("concept-x")],
        [_e("law-a", "concept-x", type_="defines", evidence="rel-1",
            status="unverified")],
    )
    result = what_defines("concept-x", snap)
    assert result.aggregate_confidence == 0.5


def test_engine_what_requires_uses_aggregate_helper() -> None:
    snap = _snap(
        [_n("concept-a"), _n("concept-b"), _n("concept-c")],
        [
            _e("concept-a", "concept-b", type_="requires", evidence="rel-1",
               status="verified"),
            _e("concept-a", "concept-c", type_="requires", evidence="rel-2",
               status="unverified"),
        ],
    )
    result = what_requires("concept-a", snap)
    assert result.aggregate_confidence == 0.5
