"""Phase 8 Task 4 — integrity checks."""

from __future__ import annotations

from vitruvius.graph.contract import GraphEdge, GraphNode, GraphSnapshot
from vitruvius.graph.integrity import (
    IntegrityFinding,
    IntegrityReport,
    check_integrity,
)


def _node(id_: str, type_: str = "concept", trust: str = "derived") -> GraphNode:
    return GraphNode(
        id=id_,
        type=type_,
        slug=id_.split("-", 1)[-1],
        trust_level=trust,
        last_updated_utc="2026-04-14T00:00:00Z",
    )


def _edge(from_id: str, to_id: str, *, type_: str = "governs",
          evidence: str = "rel-x", status: str = "verified") -> GraphEdge:
    return GraphEdge(
        from_id=from_id,
        to_id=to_id,
        type=type_,
        evidence_id=evidence,
        status=status,
    )


def _snapshot(nodes: list[GraphNode], edges: list[GraphEdge]) -> GraphSnapshot:
    return GraphSnapshot(
        schema_version="1.0.0",
        generated_at_utc="2026-04-14T00:00:00Z",
        node_count=len(nodes),
        edge_count=len(edges),
        nodes=nodes,
        edges=edges,
    )


def test_clean_snapshot_zero_findings() -> None:
    nodes = [_node("law-a", "source"), _node("concept-b")]
    edges = [_edge("law-a", "concept-b", evidence="rel-1")]
    report = check_integrity(_snapshot(nodes, edges))
    assert isinstance(report, IntegrityReport)
    assert report.findings == ()
    assert report.warning_count == 0
    assert report.error_count == 0
    assert report.passed


def test_orphan_node_is_warning() -> None:
    nodes = [
        _node("law-a", "source"),
        _node("concept-b"),
        _node("concept-lonely"),
    ]
    edges = [_edge("law-a", "concept-b", evidence="rel-1")]
    report = check_integrity(_snapshot(nodes, edges))
    codes = [f.code for f in report.findings]
    assert "orphan_node" in codes
    orphan = next(f for f in report.findings if f.code == "orphan_node")
    assert orphan.severity == "warning"
    assert orphan.node_id == "concept-lonely"
    assert report.passed  # warnings do not fail the build


def test_dangling_edge_is_error() -> None:
    nodes = [_node("law-a", "source")]
    edges = [_edge("law-a", "concept-missing", evidence="rel-1")]
    report = check_integrity(_snapshot(nodes, edges))
    assert any(f.code == "dangling_edge" for f in report.findings)
    assert report.error_count >= 1
    assert not report.passed


def test_duplicate_node_id_is_error() -> None:
    nodes = [_node("law-a", "source"), _node("law-a", "source")]
    report = check_integrity(_snapshot(nodes, []))
    assert any(f.code == "duplicate_node_id" for f in report.findings)
    assert not report.passed


def test_unknown_predicate_is_error_when_vocab_provided() -> None:
    nodes = [_node("law-a", "source"), _node("concept-b")]
    edges = [_edge("law-a", "concept-b", type_="zzzotron", evidence="rel-1")]
    vocab = frozenset({"governs", "affects"})
    report = check_integrity(_snapshot(nodes, edges), known_predicates=vocab)
    assert any(f.code == "unknown_predicate" for f in report.findings)
    assert not report.passed


def test_unknown_predicate_skipped_when_no_vocab() -> None:
    nodes = [_node("law-a", "source"), _node("concept-b")]
    edges = [_edge("law-a", "concept-b", type_="zzzotron", evidence="rel-1")]
    report = check_integrity(_snapshot(nodes, edges))
    assert all(f.code != "unknown_predicate" for f in report.findings)
    assert report.passed


def test_duplicate_edge_is_warning() -> None:
    nodes = [_node("law-a", "source"), _node("concept-b")]
    e1 = _edge("law-a", "concept-b", evidence="rel-1")
    e2 = _edge("law-a", "concept-b", evidence="rel-1")
    report = check_integrity(_snapshot(nodes, [e1, e2]))
    assert any(f.code == "duplicate_edge" for f in report.findings)
    dup = next(f for f in report.findings if f.code == "duplicate_edge")
    assert dup.severity == "warning"
    assert report.passed


def test_stale_evidence_is_error_when_set_provided() -> None:
    nodes = [_node("law-a", "source"), _node("concept-b")]
    edges = [_edge("law-a", "concept-b", evidence="rel-ghost")]
    report = check_integrity(
        _snapshot(nodes, edges),
        known_evidence_ids=frozenset({"rel-1", "rel-2"}),
    )
    assert any(f.code == "stale_evidence" for f in report.findings)
    assert not report.passed


def test_stale_evidence_skipped_when_no_set() -> None:
    nodes = [_node("law-a", "source"), _node("concept-b")]
    edges = [_edge("law-a", "concept-b", evidence="rel-ghost")]
    report = check_integrity(_snapshot(nodes, edges))
    assert all(f.code != "stale_evidence" for f in report.findings)


def test_finding_is_frozen_dataclass() -> None:
    f = IntegrityFinding(
        code="orphan_node",
        severity="warning",
        node_id="concept-x",
        edge_from=None,
        edge_to=None,
        message="test",
    )
    import dataclasses
    import pytest
    with pytest.raises(dataclasses.FrozenInstanceError):
        f.code = "other"  # type: ignore[misc]


def test_report_passed_reflects_error_count() -> None:
    nodes = [_node("law-a", "source")]
    edges = [_edge("law-a", "concept-missing", evidence="rel-1")]
    report = check_integrity(_snapshot(nodes, edges))
    assert report.passed is False

    nodes = [_node("law-a", "source"), _node("concept-b")]
    edges = [_edge("law-a", "concept-b", evidence="rel-1")]
    clean = check_integrity(_snapshot(nodes, edges))
    assert clean.passed is True
