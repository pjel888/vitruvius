"""Tests for KG snapshot quality report helpers."""

from __future__ import annotations

from vitruvius.kg.enums import EdgeType, InferenceType, NodeType, ValidationState
from vitruvius.kg.json_evidence_store import KgV2Snapshot
from vitruvius.kg.quality_report import build_kg_quality_report
from vitruvius.kg.schemas import CanonicalNode, EvidenceSpan, RelationshipAssertion, TextRangeSelector


def test_quality_report_flags_missing_supported_by_endpoint() -> None:
    snapshot = KgV2Snapshot()
    snapshot.canonical_nodes.append(
        CanonicalNode(
            id="rule-demo",
            type=NodeType.RULE,
            label="No building shall proceed without a permit",
            display_label="Building Permit Rule",
            slug="demo",
        )
    )
    snapshot.relationship_assertions.append(
        RelationshipAssertion(
            id="assert-rule-demo-supported-by",
            edge_type=EdgeType.SUPPORTED_BY,
            from_node_id="rule-demo",
            to_node_id="source-missing",
            reasoning_summary="Missing source endpoint.",
            inference_type=InferenceType.DIRECT_CITATION,
            confidence=0.9,
            validation_status=ValidationState.VALIDATED,
        )
    )

    report = build_kg_quality_report(snapshot)

    assert report["relationship_endpoint_quality"]["missing_endpoint_count"] == 1
    assert "relationship_assertions_have_missing_endpoints" in report["warnings"]
    assert "supported_by_assertions_do_not_all_target_evidence" in report["warnings"]


def test_quality_report_accepts_supported_by_evidence_span() -> None:
    snapshot = KgV2Snapshot()
    snapshot.canonical_nodes.append(
        CanonicalNode(
            id="rule-demo",
            type=NodeType.RULE,
            label="No building shall proceed without a permit",
            display_label="Building Permit Rule",
            slug="demo",
        )
    )
    snapshot.evidence_spans.append(
        EvidenceSpan(
            id="span-demo",
            document_id="doc-demo",
            document_version_id="docv-demo-v1",
            selector=TextRangeSelector(kind="text_range", quote="permit", char_start=0, char_end=6),
            quote="permit",
            normalized_text="permit",
            parser="test",
            checksum="a" * 64,
        )
    )
    snapshot.relationship_assertions.append(
        RelationshipAssertion(
            id="assert-rule-demo-supported-by",
            edge_type=EdgeType.SUPPORTED_BY,
            from_node_id="rule-demo",
            to_node_id="span-demo",
            reasoning_summary="Rule is supported by evidence.",
            inference_type=InferenceType.DIRECT_CITATION,
            confidence=0.9,
            validation_status=ValidationState.VALIDATED,
            evidence_ids=["span-demo"],
        )
    )

    report = build_kg_quality_report(snapshot)

    assert report["relationship_endpoint_quality"]["missing_endpoint_count"] == 0
    assert report["relationship_endpoint_quality"]["supported_by_to_evidence"] == 1
    assert report["warnings"] == []


def test_quality_report_allows_source_ellipsis_in_source_faithful_label() -> None:
    snapshot = KgV2Snapshot()
    snapshot.canonical_nodes.append(
        CanonicalNode(
            id="rule-source-ellipsis",
            type=NodeType.RULE,
            label="Building height shall follow the National Building Code … subject to zoning.",
            display_label="Building Height Rule — Section 4 — Mandaue CLUP",
            summary="Building height shall follow the National Building Code … subject to zoning.",
            slug="source-ellipsis",
        )
    )

    report = build_kg_quality_report(snapshot)

    assert report["rule_title_quality"]["truncated_rule_label_ids"] == []
    assert "truncated_rule_labels" not in report["warnings"]


def test_quality_report_flags_display_title_truncation() -> None:
    snapshot = KgV2Snapshot()
    snapshot.canonical_nodes.append(
        CanonicalNode(
            id="rule-display-truncated",
            type=NodeType.RULE,
            label="Building height shall follow the National Building Code subject to zoning.",
            display_label="Building Height Rule …",
            summary="Building height shall follow the National Building Code subject to zoning.",
            slug="display-truncated",
        )
    )
    snapshot.canonical_nodes.append(
        CanonicalNode(
            id="rule-source-summary-ellipsis",
            type=NodeType.RULE,
            label="Exit width shall be determined from occupant load.",
            display_label="Exit Width Rule — Section 1207 — PD 1096",
            summary="Exit width shall be determined from occupant load...",
            slug="source-summary-ellipsis",
        )
    )

    report = build_kg_quality_report(snapshot)

    assert report["rule_title_quality"]["truncated_rule_label_ids"] == ["rule-display-truncated"]
    assert "truncated_rule_labels" in report["warnings"]
