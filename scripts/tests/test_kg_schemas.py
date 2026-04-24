"""Tests for Knowledge Graph Pydantic schemas."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from vitruvius.kg.enums import EdgeType, InferenceType, NodeType, ValidationState
from vitruvius.kg.schemas import (
    CanonicalNode,
    Chunk,
    CreatedBy,
    DocumentVersion,
    EvidenceSpan,
    MarkdownRangeSelector,
    MergeAssertion,
    PdfBboxSelector,
    PdfPageSelector,
    PlacementAssertion,
    RelationshipAssertion,
    Section,
    TextRangeSelector,
)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

def test_node_type_enum() -> None:
    assert NodeType.CONCEPT == "concept"
    assert NodeType.RULE == "rule"


def test_edge_type_enum() -> None:
    assert EdgeType.DEPENDS_ON == "DEPENDS_ON"


def test_inference_type_enum() -> None:
    assert InferenceType.DIRECT_CITATION == "direct_citation"


def test_validation_state_enum() -> None:
    assert ValidationState.CANDIDATE == "candidate"


# ---------------------------------------------------------------------------
# Selectors
# ---------------------------------------------------------------------------

def test_pdf_bbox_selector_valid() -> None:
    sel = PdfBboxSelector(page=87, bbox=[72.1, 144.0, 381.4, 175.8], quote="test")
    assert sel.kind == "pdf_bbox"
    assert sel.page == 87


def test_pdf_bbox_selector_invalid_page() -> None:
    with pytest.raises(ValidationError):
        PdfBboxSelector(page=0, bbox=[0, 0, 1, 1], quote="test")


def test_markdown_range_selector_valid() -> None:
    sel = MarkdownRangeSelector(
        heading_path=["Rule VII", "Means of Egress"],
        line_start=120,
        line_end=128,
        quote="Stairways shall form part...",
    )
    assert sel.kind == "markdown_range"


def test_text_range_selector_valid() -> None:
    sel = TextRangeSelector(char_start=3421, char_end=3678, quote="test")
    assert sel.kind == "text_range"


# ---------------------------------------------------------------------------
# Evidence graph entities
# ---------------------------------------------------------------------------

def test_document_version_valid() -> None:
    dv = DocumentVersion(
        id="docv-pd1096-irr-v1",
        document_id="doc-pd1096-irr",
        title="PD 1096 IRR Volume 1",
        source_uri="/docs/pd1096-irr-v1.pdf",
        sha256="a" * 64,
        created_at="2026-04-18T00:00:00Z",
    )
    assert dv.mime_type == "application/pdf"


def test_document_version_invalid_id() -> None:
    with pytest.raises(ValidationError):
        DocumentVersion(
            id="bad-id",
            document_id="doc-test",
            title="Test",
            source_uri="/test.pdf",
            sha256="a" * 64,
        )


def test_section_valid() -> None:
    sec = Section(
        id="sec-pd1096-001",
        document_version_id="docv-pd1096-irr-v1",
        title="Means of Egress",
        level=2,
    )
    assert sec.level == 2


def test_chunk_valid() -> None:
    chk = Chunk(
        id="chk-pd1096-001",
        section_id="sec-pd1096-001",
        document_version_id="docv-pd1096-irr-v1",
        text="Stairways shall...",
        char_start=0,
        char_end=100,
    )
    assert chk.token_count is None


def test_evidence_span_with_pdf_selector() -> None:
    span = EvidenceSpan(
        id="span-pd1096-001",
        document_id="doc-pd1096-irr",
        document_version_id="docv-pd1096-irr-v1",
        selector=PdfBboxSelector(page=87, bbox=[0, 0, 1, 1], quote="test"),
        quote="Stairways shall...",
        normalized_text="Stairways shall...",
        deep_link="/viewer/...",
        parser="pymupdf",
        checksum="a" * 64,
    )
    assert span.selector.kind == "pdf_bbox"


def test_evidence_span_with_markdown_selector() -> None:
    span = EvidenceSpan(
        id="span-md-001",
        document_id="doc-test",
        document_version_id="docv-test-v1",
        selector=MarkdownRangeSelector(heading_path=["H1"], line_start=1, line_end=5, quote="test"),
        quote="Test quote",
        normalized_text="Test quote",
        parser="markdown",
        checksum="b" * 64,
    )
    assert span.selector.kind == "markdown_range"


def test_evidence_span_selector_coercion_from_dict() -> None:
    data = {
        "id": "span-test-001",
        "document_id": "doc-test",
        "document_version_id": "docv-test-v1",
        "selector": {"kind": "pdf_page", "page": 5, "quote": "hello"},
        "quote": "hello",
        "normalized_text": "hello",
        "parser": "test",
        "checksum": "c" * 64,
    }
    span = EvidenceSpan.model_validate(data)
    assert isinstance(span.selector, PdfPageSelector)
    assert span.selector.page == 5


# ---------------------------------------------------------------------------
# Canonical graph entities
# ---------------------------------------------------------------------------

def test_canonical_node_valid() -> None:
    node = CanonicalNode(
        id="concept-means-of-egress",
        type=NodeType.CONCEPT,
        label="Means of Egress",
        display_label="Egress",
        slug="means-of-egress",
        summary="A continuous path of travel...",
        taxonomy_path=["Architecture", "Fire and Life Safety", "Means of Egress"],
        aliases=["egress", "exit path"],
        status=ValidationState.VALIDATED,
        confidence=0.97,
        version=3,
    )
    assert node.type == NodeType.CONCEPT
    assert node.display_label == "Egress"


def test_canonical_node_invalid_type_prefix() -> None:
    with pytest.raises(ValidationError):
        CanonicalNode(
            id="bad-prefix-test",
            type=NodeType.CONCEPT,
            label="Test",
            slug="test",
        )


# ---------------------------------------------------------------------------
# Assertion layer
# ---------------------------------------------------------------------------

def test_relationship_assertion_valid() -> None:
    assertion = RelationshipAssertion(
        id="assert-rule-depends-on-occupant-load-0001",
        edge_type=EdgeType.DEPENDS_ON,
        from_node_id="rule-minimum-corridor-width",
        to_node_id="concept-occupant-load",
        reasoning_summary="Minimum corridor width requirements vary by occupant load.",
        inference_type=InferenceType.DIRECT_CITATION,
        confidence=0.94,
        validation_status=ValidationState.VALIDATED,
        evidence_ids=["span-pd1096-001"],
        document_version_ids=["docv-pd1096-irr-v1"],
        created_by=CreatedBy(mode="hybrid", model="gemma4:31b", pipeline_stage="edge_extraction"),
        review_state="approved",
    )
    assert assertion.edge_type == EdgeType.DEPENDS_ON


def test_placement_assertion_valid() -> None:
    pa = PlacementAssertion(
        id="assert-placement-means-of-egress-001",
        node_id="concept-means-of-egress",
        parent_node_id="taxonomy-fire-and-life-safety",
        reasoning_summary="Means of egress is a fire and life safety topic.",
        confidence=0.95,
        validation_status=ValidationState.VALIDATED,
        evidence_ids=["span-pd1096-001"],
    )
    assert pa.parent_node_id == "taxonomy-fire-and-life-safety"


def test_merge_assertion_valid() -> None:
    ma = MergeAssertion(
        id="assert-merge-egress-001",
        from_node_id="concept-egress",
        to_node_id="concept-means-of-egress",
        reasoning_summary="These two concepts refer to the same idea.",
        confidence=0.91,
        validation_status=ValidationState.REVIEW_REQUIRED,
    )
    assert ma.validation_status == ValidationState.REVIEW_REQUIRED


# ---------------------------------------------------------------------------
# JSON Schema export
# ---------------------------------------------------------------------------

def test_canonical_node_json_schema() -> None:
    schema = CanonicalNode.model_json_schema()
    assert "properties" in schema
    assert "id" in schema["properties"]


def test_relationship_assertion_json_schema() -> None:
    schema = RelationshipAssertion.model_json_schema()
    assert "properties" in schema
    assert "evidence_ids" in schema["properties"]
