"""Tests for RuleExtractor — Phase 2 atomic rule extraction."""

from __future__ import annotations

import pytest

from vitruvius.kg.enums import EdgeType, InferenceType, NodeType, ValidationState
from vitruvius.kg.json_evidence_store import KgV2Snapshot
from vitruvius.kg.rule_extractor import RuleExtractor, _is_source_node, _rule_label_from_evidence
from vitruvius.kg.schemas import (
    CanonicalNode,
    CreatedBy,
    DocumentVersion,
    EvidenceSpan,
    MarkdownRangeSelector,
    RelationshipAssertion,
)


class TestIsSourceNode:
    def test_document_id_is_source(self) -> None:
        snap = KgV2Snapshot()
        snap.document_versions.append(
            DocumentVersion(
                id="docv-pd-1096-v1",
                document_id="doc-pd-1096",
                title="PD 1096",
                source_uri="/sources/pd-1096.pdf",
                sha256="a" * 64,
                created_at="2026-01-01T00:00:00Z",
            )
        )
        assert _is_source_node("doc-pd-1096", snap) is True
        assert _is_source_node("docv-pd-1096-v1", snap) is True

    def test_concept_id_is_not_source(self) -> None:
        snap = KgV2Snapshot()
        assert _is_source_node("concept-building-permit", snap) is False

    def test_taxonomy_id_is_not_source(self) -> None:
        snap = KgV2Snapshot()
        assert _is_source_node("taxonomy-building-code", snap) is False


class TestRuleLabelFromEvidence:
    def test_uses_first_sentence(self) -> None:
        text = "All buildings shall have a permit. This applies to all zones."
        assert _rule_label_from_evidence(text) == "All buildings shall have a permit"

    def test_strips_markdown_artifacts(self) -> None:
        assert _rule_label_from_evidence("###### SECTION 707") == "SECTION 707"
        assert _rule_label_from_evidence("- 2. Exit requirements") == "Exit requirements"
        assert _rule_label_from_evidence("* bullet point") == "bullet point"

    def test_fallback_to_concept_source_names(self) -> None:
        label = _rule_label_from_evidence(
            "Legacy promotion pipeline assertion",
            concept_id="concept-building-permit",
            source_id="handout-pd-1096",
        )
        assert "Building Permit" in label
        assert "Pd 1096" in label

    def test_short_text_expanded(self) -> None:
        assert _rule_label_from_evidence("- a") == "a"

    def test_long_text_is_not_truncated(self) -> None:
        text = (
            "The total exit width required from any storey of a building shall "
            "be determined by using the occupant load of that storey and "
            "applying the required width factors for stairs and other exits."
        )
        label = _rule_label_from_evidence(text)
        assert label == text.removesuffix(".")
        assert "..." not in label
        assert "…" not in label

    def test_generated_summary_and_reasoning_detail_are_not_truncated(self) -> None:
        snap = KgV2Snapshot()
        long_quote = (
            "The total exit width required from any storey of a building shall "
            "be determined by using the occupant load of that storey and "
            "applying the required width factors for stairs and other exits. "
            "This source sentence intentionally continues beyond two hundred "
            "characters so generated graph summaries preserve the complete "
            "evidence text instead of adding a truncation marker."
        )
        snap.document_versions.append(
            DocumentVersion(
                id="docv-pd-1096-v1",
                document_id="doc-pd-1096",
                title="PD 1096",
                source_uri="/sources/pd-1096.pdf",
                sha256="a" * 64,
                created_at="2026-01-01T00:00:00Z",
            )
        )
        snap.canonical_nodes.append(
            CanonicalNode(
                id="concept-exit-width",
                type=NodeType.CONCEPT,
                label="Exit Width",
                slug="exit-width",
                taxonomy_path=["taxonomy-building-code"],
                status=ValidationState.VALIDATED,
                confidence=0.9,
            )
        )
        snap.evidence_spans.append(
            EvidenceSpan(
                id="span-ev-002",
                document_id="doc-pd-1096",
                document_version_id="docv-pd-1096-v1",
                selector=MarkdownRangeSelector(heading_path=["section-1207"]),
                quote=long_quote,
                normalized_text=long_quote,
                deep_link="/viewer/pd-1096?section=section-1207",
                parser="test",
                checksum="c" * 64,
                created_at="2026-01-01T00:00:00Z",
            )
        )
        snap.relationship_assertions.append(
            RelationshipAssertion(
                id="assert-rel-003",
                edge_type=EdgeType.APPLIES_TO,
                from_node_id="doc-pd-1096",
                to_node_id="concept-exit-width",
                reasoning_summary="Source governs concept",
                inference_type=InferenceType.DIRECT_CITATION,
                confidence=0.95,
                validation_status=ValidationState.VALIDATED,
                evidence_ids=["span-ev-002"],
                created_at="2026-01-01T00:00:00Z",
            )
        )

        result = RuleExtractor(snapshot=snap).extract_all()
        rule = next(n for n in result.canonical_nodes if n.type.value == "rule")
        defined_by = next(a for a in result.relationship_assertions if a.edge_type == EdgeType.DEFINED_BY)

        assert rule.summary == long_quote
        assert "..." not in rule.summary
        assert "…" not in rule.summary
        assert any(detail == f"Evidence: {long_quote}" for detail in defined_by.reasoning_detail)

    def test_generated_summary_strips_html_and_blockquote_artifacts(self) -> None:
        snap = KgV2Snapshot()
        quote = "<br><br>NOTES<br><br>|1.1 Project area consultation is required."
        snap.document_versions.append(
            DocumentVersion(
                id="docv-eis-v1",
                document_id="doc-eis",
                title="EIS Guidelines",
                source_uri="/sources/eis.pdf",
                sha256="d" * 64,
                created_at="2026-01-01T00:00:00Z",
            )
        )
        snap.canonical_nodes.append(
            CanonicalNode(
                id="concept-project-area",
                type=NodeType.CONCEPT,
                label="Project Area",
                slug="project-area",
                taxonomy_path=["taxonomy-environmental-planning"],
                status=ValidationState.VALIDATED,
                confidence=0.9,
            )
        )
        snap.evidence_spans.append(
            EvidenceSpan(
                id="span-ev-html",
                document_id="doc-eis",
                document_version_id="docv-eis-v1",
                selector=MarkdownRangeSelector(heading_path=["section-3"]),
                quote=quote,
                normalized_text=quote,
                deep_link="/viewer/eis?section=section-3",
                parser="test",
                checksum="e" * 64,
                created_at="2026-01-01T00:00:00Z",
            )
        )
        snap.relationship_assertions.append(
            RelationshipAssertion(
                id="assert-rel-html",
                edge_type=EdgeType.APPLIES_TO,
                from_node_id="doc-eis",
                to_node_id="concept-project-area",
                reasoning_summary="Source governs concept",
                inference_type=InferenceType.DIRECT_CITATION,
                confidence=0.95,
                validation_status=ValidationState.VALIDATED,
                evidence_ids=["span-ev-html"],
                created_at="2026-01-01T00:00:00Z",
            )
        )

        result = RuleExtractor(snapshot=snap).extract_all()
        rule = next(n for n in result.canonical_nodes if n.type.value == "rule")

        assert rule.label == "NOTES |1.1 Project area consultation is required."
        assert rule.summary == "NOTES |1.1 Project area consultation is required."
        assert "<" not in rule.summary
        assert ">" not in rule.summary


class TestRuleExtractor:
    def test_extracts_rule_from_document_to_concept_assertion(self) -> None:
        snap = KgV2Snapshot()

        # Document version
        snap.document_versions.append(
            DocumentVersion(
                id="docv-pd-1096-v1",
                document_id="doc-pd-1096",
                title="PD 1096",
                source_uri="/sources/pd-1096.pdf",
                sha256="a" * 64,
                created_at="2026-01-01T00:00:00Z",
            )
        )

        # Concept node
        snap.canonical_nodes.append(
            CanonicalNode(
                id="concept-building-permit",
                type=NodeType.CONCEPT,
                label="Building Permit",
                slug="building-permit",
                taxonomy_path=["taxonomy-building-code"],
                status=ValidationState.VALIDATED,
                confidence=0.9,
            )
        )

        # Evidence span
        snap.evidence_spans.append(
            EvidenceSpan(
                id="span-ev-001",
                document_id="doc-pd-1096",
                document_version_id="docv-pd-1096-v1",
                selector=MarkdownRangeSelector(heading_path=["section-1"]),
                quote="A building permit is required for all new construction.",
                normalized_text="A building permit is required for all new construction.",
                deep_link="/viewer/pd-1096?section=section-1",
                parser="test",
                checksum="b" * 64,
                created_at="2026-01-01T00:00:00Z",
            )
        )

        # Original assertion: document → concept
        snap.relationship_assertions.append(
            RelationshipAssertion(
                id="assert-rel-001",
                edge_type=EdgeType.APPLIES_TO,
                from_node_id="doc-pd-1096",
                to_node_id="concept-building-permit",
                reasoning_summary="Source governs concept",
                inference_type=InferenceType.DIRECT_CITATION,
                confidence=0.95,
                validation_status=ValidationState.VALIDATED,
                evidence_ids=["span-ev-001"],
                created_at="2026-01-01T00:00:00Z",
            )
        )

        extractor = RuleExtractor(snapshot=snap)
        result = extractor.extract_all()

        # Should have 1 rule node
        rule_nodes = [n for n in result.canonical_nodes if n.type.value == "rule"]
        assert len(rule_nodes) == 1
        rule = rule_nodes[0]
        assert rule.id.startswith("rule-")
        assert rule.label == "A building permit is required for all new construction"
        assert rule.display_label == "Building Permit Rule — Section 1 — PD 1096"
        assert "permit" in rule.label.lower()
        assert "PD 1096" in rule.display_label
        assert "..." not in rule.label
        assert "…" not in rule.label
        assert "..." not in rule.display_label
        assert "…" not in rule.display_label
        assert rule.summary == "A building permit is required for all new construction."
        assert rule.taxonomy_path == ["taxonomy-building-code"]

        # Should have 2 assertions replacing the original 1
        assert len(result.relationship_assertions) == 2
        defined_by = [a for a in result.relationship_assertions if a.edge_type == EdgeType.DEFINED_BY]
        supported_by = [a for a in result.relationship_assertions if a.edge_type == EdgeType.SUPPORTED_BY]
        assert len(defined_by) == 1
        assert len(supported_by) == 1

        # DEFINED_BY: concept → rule
        assert defined_by[0].from_node_id == "concept-building-permit"
        assert defined_by[0].to_node_id == rule.id

        # SUPPORTED_BY: rule → evidence span
        assert supported_by[0].from_node_id == rule.id
        assert supported_by[0].to_node_id == "span-ev-001"

    def test_preserves_concept_to_concept_assertions(self) -> None:
        snap = KgV2Snapshot()

        snap.canonical_nodes.append(
            CanonicalNode(
                id="concept-a",
                type=NodeType.CONCEPT,
                label="A",
                slug="a",
                taxonomy_path=[],
                status=ValidationState.VALIDATED,
                confidence=0.9,
            )
        )
        snap.canonical_nodes.append(
            CanonicalNode(
                id="concept-b",
                type=NodeType.CONCEPT,
                label="B",
                slug="b",
                taxonomy_path=[],
                status=ValidationState.VALIDATED,
                confidence=0.9,
            )
        )

        snap.relationship_assertions.append(
            RelationshipAssertion(
                id="assert-rel-002",
                edge_type=EdgeType.RELATED_TO,
                from_node_id="concept-a",
                to_node_id="concept-b",
                reasoning_summary="A affects B",
                inference_type=InferenceType.MULTI_HOP_INFERENCE,
                confidence=0.8,
                validation_status=ValidationState.VALIDATED,
                created_at="2026-01-01T00:00:00Z",
            )
        )

        extractor = RuleExtractor(snapshot=snap)
        result = extractor.extract_all()

        # No rules created
        rule_nodes = [n for n in result.canonical_nodes if n.type.value == "rule"]
        assert len(rule_nodes) == 0

        # Original assertion preserved
        assert len(result.relationship_assertions) == 1
        assert result.relationship_assertions[0].id == "assert-rel-002"
