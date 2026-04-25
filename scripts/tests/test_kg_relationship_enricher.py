"""Tests for deterministic MVP KG relationship enrichment."""

from __future__ import annotations

from pathlib import Path

from vitruvius.kg.enums import EdgeType, InferenceType, NodeType, ValidationState
from vitruvius.kg.json_evidence_store import KgV2Snapshot
from vitruvius.kg.relationship_enricher import enrich_snapshot
from vitruvius.kg.schemas import (
    CanonicalNode,
    DocumentVersion,
    EvidenceSpan,
    RelationshipAssertion,
    TextRangeSelector,
)


def _concept(
    concept_id: str,
    label: str,
    taxonomy_root: str,
    *,
    aliases: list[str] | None = None,
) -> CanonicalNode:
    return CanonicalNode(
        id=concept_id,
        type=NodeType.CONCEPT,
        label=label,
        slug=concept_id.removeprefix("concept-"),
        taxonomy_path=[taxonomy_root, f"topic-{taxonomy_root.removeprefix('taxonomy-')}", f"subtopic-{concept_id.removeprefix('concept-')}"],
        aliases=aliases or [],
        status=ValidationState.VALIDATED,
        confidence=0.9,
    )


def _rule(rule_id: str, label: str) -> CanonicalNode:
    return CanonicalNode(
        id=rule_id,
        type=NodeType.RULE,
        label=label,
        display_label=label,
        slug=rule_id.removeprefix("rule-"),
        taxonomy_path=["taxonomy-spaces-occupancy"],
        status=ValidationState.REVIEW_REQUIRED,
        confidence=0.82,
    )


def _source(path: Path, *, title: str, concepts: list[str], trust_level: str = "primary") -> None:
    path.write_text(
        "\n".join(
            [
                "---",
                f"title: {title}",
                f"trust_level: {trust_level}",
                "canonical_status: draft",
                "---",
                "",
                f"# {title}",
                "",
                "## Referenced Concepts",
                *[f"- {concept}" for concept in concepts],
                "",
            ]
        ),
        encoding="utf-8",
    )


def test_enrichment_adds_reviewable_rule_semantics_and_source_support(tmp_path: Path) -> None:
    snap = KgV2Snapshot()
    snap.canonical_nodes.extend(
        [
            _concept("concept-floor-area", "Floor Area", "taxonomy-spaces-occupancy"),
            _concept("concept-zoning-ordinance", "Zoning Ordinance", "taxonomy-regulatory-permits"),
            _concept("concept-standards-of-professional-practice", "Standards of Professional Practice", "taxonomy-project-practice", aliases=["SPP"]),
            _concept("concept-arbitration", "Arbitration", "taxonomy-project-practice"),
            _rule("rule-floor-area-001", "Floor Area Rule"),
        ]
    )
    snap.evidence_spans.append(
        EvidenceSpan(
            id="span-floor-area",
            document_id="doc-zoning",
            document_version_id="docv-zoning-v1",
            selector=TextRangeSelector(kind="text_range", quote="floor area", char_start=0, char_end=10),
            quote="Floor area shall not exceed the limits established by the zoning ordinance.",
            normalized_text="Floor area shall not exceed the limits established by the zoning ordinance.",
            parser="test",
            checksum="a" * 64,
        )
    )
    snap.relationship_assertions.extend(
        [
            RelationshipAssertion(
                id="assert-floor-area-defined-by",
                edge_type=EdgeType.DEFINED_BY,
                from_node_id="concept-floor-area",
                to_node_id="rule-floor-area-001",
                reasoning_summary="Floor Area defines a rule.",
                inference_type=InferenceType.DIRECT_CITATION,
                confidence=0.9,
                validation_status=ValidationState.VALIDATED,
            ),
            RelationshipAssertion(
                id="assert-floor-area-supported-by",
                edge_type=EdgeType.SUPPORTED_BY,
                from_node_id="rule-floor-area-001",
                to_node_id="span-floor-area",
                reasoning_summary="Rule is supported by evidence.",
                inference_type=InferenceType.DIRECT_CITATION,
                confidence=0.9,
                validation_status=ValidationState.VALIDATED,
                evidence_ids=["span-floor-area"],
            ),
        ]
    )

    source_dir = tmp_path / "sources"
    source_dir.mkdir()
    _source(
        source_dir / "spp-205.md",
        title="SPP DOC. 205",
        concepts=["concept-standards-of-professional-practice"],
    )
    _source(
        source_dir / "practice-1.md",
        title="Professional Practice 1",
        concepts=["concept-standards-of-professional-practice", "concept-arbitration"],
    )
    _source(
        source_dir / "practice-2.md",
        title="Professional Practice 2",
        concepts=["concept-standards-of-professional-practice", "concept-arbitration"],
    )
    _source(
        source_dir / "practice-3.md",
        title="Professional Practice 3",
        concepts=["concept-standards-of-professional-practice"],
    )
    snap.document_versions.extend(
        [
            DocumentVersion(
                id="docv-spp-205-v1",
                document_id="doc-spp-205",
                title="SPP DOC. 205",
                source_uri=str(source_dir / "spp-205.md"),
                sha256="b" * 64,
                created_at="2026-01-01T00:00:00Z",
            ),
            DocumentVersion(
                id="docv-practice-1-v1",
                document_id="doc-practice-1",
                title="Professional Practice 1",
                source_uri=str(source_dir / "practice-1.md"),
                sha256="c" * 64,
                created_at="2026-01-01T00:00:00Z",
            ),
            DocumentVersion(
                id="docv-practice-2-v1",
                document_id="doc-practice-2",
                title="Professional Practice 2",
                source_uri=str(source_dir / "practice-2.md"),
                sha256="d" * 64,
                created_at="2026-01-01T00:00:00Z",
            ),
            DocumentVersion(
                id="docv-practice-3-v1",
                document_id="doc-practice-3",
                title="Professional Practice 3",
                source_uri=str(source_dir / "practice-3.md"),
                sha256="e" * 64,
                created_at="2026-01-01T00:00:00Z",
            ),
        ]
    )

    report = enrich_snapshot(snap, repo_root=tmp_path, max_new_assertions=20)

    assert report.added_source_support_count == 6
    assert report.semantic_assertion_count >= 2
    assert any(
        assertion.edge_type == EdgeType.REGULATED_BY
        and assertion.from_node_id == "concept-floor-area"
        and assertion.to_node_id == "concept-zoning-ordinance"
        and assertion.validation_status == ValidationState.REVIEW_REQUIRED
        for assertion in snap.relationship_assertions
    )
    assert any(
        assertion.edge_type == EdgeType.SUPPORTED_BY
        and assertion.from_node_id == "concept-standards-of-professional-practice"
        and assertion.to_node_id == "docv-spp-205-v1"
        and assertion.document_version_ids == ["docv-spp-205-v1"]
        for assertion in snap.relationship_assertions
    )
    assert any(
        assertion.edge_type == EdgeType.RELATED_TO
        and {assertion.from_node_id, assertion.to_node_id}
        == {"concept-standards-of-professional-practice", "concept-arbitration"}
        and assertion.review_state == "pending"
        for assertion in snap.relationship_assertions
    )


def test_enrichment_does_not_duplicate_existing_semantic_relationship() -> None:
    snap = KgV2Snapshot()
    snap.canonical_nodes.extend(
        [
            _concept("concept-floor-area", "Floor Area", "taxonomy-spaces-occupancy"),
            _concept("concept-zoning-ordinance", "Zoning Ordinance", "taxonomy-regulatory-permits"),
            _rule("rule-floor-area-001", "Floor Area Rule"),
        ]
    )
    snap.evidence_spans.append(
        EvidenceSpan(
            id="span-floor-area",
            document_id="doc-zoning",
            document_version_id="docv-zoning-v1",
            selector=TextRangeSelector(kind="text_range", quote="floor area", char_start=0, char_end=10),
            quote="Floor area shall not exceed the limits established by the zoning ordinance.",
            normalized_text="Floor area shall not exceed the limits established by the zoning ordinance.",
            parser="test",
            checksum="f" * 64,
        )
    )
    snap.relationship_assertions.extend(
        [
            RelationshipAssertion(
                id="assert-existing-floor-area-zoning",
                edge_type=EdgeType.REGULATED_BY,
                from_node_id="concept-floor-area",
                to_node_id="concept-zoning-ordinance",
                reasoning_summary="Existing semantic edge.",
                inference_type=InferenceType.HUMAN_AUTHORED,
                confidence=0.95,
                validation_status=ValidationState.VALIDATED,
            ),
            RelationshipAssertion(
                id="assert-floor-area-defined-by",
                edge_type=EdgeType.DEFINED_BY,
                from_node_id="concept-floor-area",
                to_node_id="rule-floor-area-001",
                reasoning_summary="Floor Area defines a rule.",
                inference_type=InferenceType.DIRECT_CITATION,
                confidence=0.9,
                validation_status=ValidationState.VALIDATED,
            ),
            RelationshipAssertion(
                id="assert-floor-area-supported-by",
                edge_type=EdgeType.SUPPORTED_BY,
                from_node_id="rule-floor-area-001",
                to_node_id="span-floor-area",
                reasoning_summary="Rule is supported by evidence.",
                inference_type=InferenceType.DIRECT_CITATION,
                confidence=0.9,
                validation_status=ValidationState.VALIDATED,
                evidence_ids=["span-floor-area"],
            ),
        ]
    )

    report = enrich_snapshot(snap, max_new_assertions=20)

    regulated_by_edges = [
        assertion
        for assertion in snap.relationship_assertions
        if assertion.edge_type == EdgeType.REGULATED_BY
        and assertion.from_node_id == "concept-floor-area"
        and assertion.to_node_id == "concept-zoning-ordinance"
    ]
    assert len(regulated_by_edges) == 1
    assert report.skipped_existing_count == 1
