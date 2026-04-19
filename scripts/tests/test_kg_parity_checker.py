"""Tests for ParityChecker."""

from __future__ import annotations

from vitruvius.graph.contract import GraphEdge, GraphNode, GraphSnapshot
from vitruvius.kg.enums import NodeType, ValidationState
from vitruvius.kg.json_evidence_store import KgV2Snapshot
from vitruvius.kg.parity_checker import ParityChecker
from vitruvius.kg.schemas import CanonicalNode


def _make_v1_snapshot() -> GraphSnapshot:
    return GraphSnapshot(
        schema_version="1.0.0",
        generated_at_utc="2026-04-19T00:00:00Z",
        node_count=2,
        edge_count=1,
        nodes=[
            GraphNode(id="concept-a", type="concept", slug="a", trust_level="primary", last_updated_utc="2026-04-19T00:00:00Z"),
            GraphNode(id="concept-b", type="concept", slug="b", trust_level="primary", last_updated_utc="2026-04-19T00:00:00Z"),
        ],
        edges=[
            GraphEdge(from_id="concept-a", to_id="concept-b", type="RELATED_TO", evidence_id="ev-001", status="verified"),
        ],
    )


def _make_v2_snapshot() -> KgV2Snapshot:
    snap = KgV2Snapshot()
    snap.canonical_nodes.extend([
        CanonicalNode(id="concept-a", type=NodeType.CONCEPT, label="A", slug="a", status=ValidationState.VALIDATED),
        CanonicalNode(id="concept-b", type=NodeType.CONCEPT, label="B", slug="b", status=ValidationState.VALIDATED),
    ])
    snap.fast_edges.append({
        "id": "edge-001",
        "edge_type": "RELATED_TO",
        "from_node_id": "concept-a",
        "to_node_id": "concept-b",
        "assertion_id": "assert-001",
        "confidence": 0.9,
        "validation_status": "validated",
        "evidence_span_count": 1,
        "document_version_count": 0,
    })
    return snap


class TestParityCheck:
    def test_full_match(self) -> None:
        v1 = _make_v1_snapshot()
        v2 = _make_v2_snapshot()
        checker = ParityChecker()
        report = checker.check(v1, v2)
        assert report.v1_node_count == 2
        assert report.v2_node_count == 2
        assert len(report.matched_node_ids) == 2
        assert len(report.missing_in_v2) == 0
        assert report.v1_edge_count == 1
        assert report.v2_edge_count == 1
        assert len(report.matched_edges) == 1
        assert report.coverage_pct == 1.0
        assert checker.is_ready_for_deprecation(report) is True

    def test_missing_node_in_v2(self) -> None:
        v1 = _make_v1_snapshot()
        v2 = _make_v2_snapshot()
        v2.canonical_nodes.pop()  # Remove concept-b
        checker = ParityChecker()
        report = checker.check(v1, v2)
        assert len(report.missing_in_v2) == 1
        assert report.missing_in_v2[0] == "concept-b"
        assert report.coverage_pct == 0.75
        assert checker.is_ready_for_deprecation(report) is False

    def test_missing_edge_in_v2(self) -> None:
        v1 = _make_v1_snapshot()
        v2 = _make_v2_snapshot()
        v2.fast_edges.clear()
        checker = ParityChecker()
        report = checker.check(v1, v2)
        assert len(report.missing_edges_in_v2) == 1
        # node_coverage=1.0, edge_coverage=0.0 → avg=0.5
        assert report.coverage_pct == 0.5

    def test_empty_snapshots(self) -> None:
        v1 = GraphSnapshot(
            schema_version="1.0.0",
            generated_at_utc="2026-04-19T00:00:00Z",
            node_count=0,
            edge_count=0,
            nodes=[],
            edges=[],
        )
        v2 = KgV2Snapshot()
        checker = ParityChecker()
        report = checker.check(v1, v2)
        assert report.coverage_pct == 1.0
