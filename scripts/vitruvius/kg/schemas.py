"""Knowledge Graph transition — Pydantic v2 schemas.

These models define the data contracts for:
- Evidence graph (DocumentVersion → Section → Chunk → EvidenceSpan)
- Canonical graph (CanonicalNode with taxonomy placement)
- Assertion layer (RelationshipAssertion, PlacementAssertion, MergeAssertion)
- Selectors (deep-links to PDF and Markdown sources)

All models export JSON Schema via ``model_json_schema()`` for structured
LLM output validation.
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field, field_validator

from .enums import EdgeType, InferenceType, NodeType, ValidationState


# ---------------------------------------------------------------------------
# Selectors — deep-linking to source evidence
# ---------------------------------------------------------------------------

class Selector(BaseModel):
    """Abstract base for all evidence selectors."""

    kind: Literal["pdf_bbox", "pdf_page", "markdown_range", "text_range"]
    quote: str = Field(
        default="",
        description="Exact quoted text at the selector location. Survives layout drift.",
    )


class PdfBboxSelector(Selector):
    """PDF page + bounding box selector."""

    kind: Literal["pdf_bbox"] = "pdf_bbox"
    page: int = Field(..., ge=1)
    bbox: list[float] = Field(
        ...,
        min_length=4,
        max_length=4,
        description="[x1, y1, x2, y2] in PDF points",
    )


class PdfPageSelector(Selector):
    """PDF page-only selector (fallback when bbox unavailable)."""

    kind: Literal["pdf_page"] = "pdf_page"
    page: int = Field(..., ge=1)


class MarkdownRangeSelector(Selector):
    """Markdown heading path + line/char range selector."""

    kind: Literal["markdown_range"] = "markdown_range"
    heading_path: list[str] = Field(default_factory=list)
    line_start: int | None = Field(default=None, ge=1)
    line_end: int | None = Field(default=None, ge=1)
    char_start: int | None = Field(default=None, ge=0)
    char_end: int | None = Field(default=None, ge=0)


class TextRangeSelector(Selector):
    """Plain text character range selector."""

    kind: Literal["text_range"] = "text_range"
    char_start: int = Field(..., ge=0)
    char_end: int = Field(..., ge=0)


# Union type for evidence span selectors
EvidenceSelector = PdfBboxSelector | PdfPageSelector | MarkdownRangeSelector | TextRangeSelector


# ---------------------------------------------------------------------------
# Evidence graph entities
# ---------------------------------------------------------------------------

class DocumentVersion(BaseModel):
    """Immutable version of a source document."""

    id: str = Field(..., pattern=r"^docv-[a-z0-9-]+-v\d+$")
    document_id: str = Field(..., pattern=r"^doc-[a-z0-9-]+$")
    title: str
    source_uri: str
    mime_type: str = Field(default="application/pdf")
    sha256: str = Field(..., pattern=r"^[a-f0-9]{64}$")
    created_at: str = Field(..., description="ISO-8601 UTC")
    supersedes: str | None = Field(default=None, pattern=r"^docv-[a-z0-9-]+-v\d+$")


class Section(BaseModel):
    """A logical section within a document version."""

    id: str = Field(..., pattern=r"^sec-[a-z0-9-]+$")
    document_version_id: str
    title: str
    level: int = Field(default=2, ge=1, le=6)
    line_start: int | None = Field(default=None, ge=1)
    line_end: int | None = Field(default=None, ge=1)
    char_start: int | None = Field(default=None, ge=0)
    char_end: int | None = Field(default=None, ge=0)


class Chunk(BaseModel):
    """A semantic chunk within a section."""

    id: str = Field(..., pattern=r"^chk-[a-z0-9-]+$")
    section_id: str
    document_version_id: str
    text: str
    char_start: int = Field(..., ge=0)
    char_end: int = Field(..., ge=0)
    token_count: int | None = Field(default=None, ge=1)


class EvidenceSpan(BaseModel):
    """A citable span of evidence within a document version."""

    id: str = Field(..., pattern=r"^span-[a-z0-9-]+$")
    document_id: str
    document_version_id: str
    selector: EvidenceSelector
    quote: str
    normalized_text: str
    deep_link: str = Field(
        default="",
        description="Internal viewer route, e.g. /viewer/:doc/:docv?page=87&bbox=...",
    )
    parser: str
    parser_version: str | None = None
    ingestion_run_id: str | None = None
    checksum: str = Field(..., pattern=r"^[a-f0-9]{64}$")
    created_at: str = Field(default="", description="ISO-8601 UTC")

    @field_validator("selector", mode="before")
    @classmethod
    def _coerce_selector(cls, v: Any) -> Any:
        if isinstance(v, dict):
            kind = v.get("kind")
            if kind == "pdf_bbox":
                return PdfBboxSelector(**v)
            if kind == "pdf_page":
                return PdfPageSelector(**v)
            if kind == "markdown_range":
                return MarkdownRangeSelector(**v)
            if kind == "text_range":
                return TextRangeSelector(**v)
        return v


# ---------------------------------------------------------------------------
# Canonical graph entities
# ---------------------------------------------------------------------------

class CanonicalNode(BaseModel):
    """A validated knowledge unit in the canonical graph."""

    id: str = Field(..., pattern=r"^(taxonomy|topic|subtopic|concept|term|definition|rule|procedure|exception|constraint|example)-[a-z0-9-]+$")
    type: NodeType
    label: str = Field(..., min_length=1)
    display_label: str | None = Field(
        default=None,
        description="Short presentation label for dense graph and search surfaces.",
    )
    slug: str = Field(..., min_length=1)
    summary: str = Field(default="", description="Definition or concise explanation")
    taxonomy_path: list[str] = Field(default_factory=list)
    aliases: list[str] = Field(default_factory=list)
    status: ValidationState = ValidationState.CANDIDATE
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    version: int = Field(default=1, ge=1)
    created_at: str = Field(default="", description="ISO-8601 UTC")
    updated_at: str = Field(default="", description="ISO-8601 UTC")
    embedding_ref: str | None = None
    primary_assertion_id: str | None = None


class TaxonomyNode(BaseModel):
    """A lightweight taxonomy parent node for placement decisions."""

    id: str = Field(..., min_length=1)
    path: list[str] = Field(default_factory=list)
    label: str = Field(..., min_length=1)
    embedding: list[float] | None = None


# ---------------------------------------------------------------------------
# Assertion layer — reified edges
# ---------------------------------------------------------------------------

class CreatedBy(BaseModel):
    """Provenance for who/what created an assertion."""

    mode: Literal["hybrid", "local_llm", "cloud_llm", "deterministic", "human"]
    model: str | None = None
    pipeline_stage: str | None = None
    run_id: str | None = None


class RelationshipAssertion(BaseModel):
    """A reified claim that node A relates to node B."""

    id: str = Field(..., pattern=r"^assert-[a-z0-9-]+$")
    edge_type: EdgeType
    from_node_id: str
    to_node_id: str
    reasoning_summary: str = Field(..., min_length=1)
    reasoning_detail: list[str] = Field(default_factory=list)
    inference_type: InferenceType
    confidence: float = Field(..., ge=0.0, le=1.0)
    validation_status: ValidationState = ValidationState.CANDIDATE
    created_by: CreatedBy = Field(default_factory=lambda: CreatedBy(mode="hybrid"))
    review_state: Literal["pending", "approved", "rejected", "escalated"] = "pending"
    evidence_ids: list[str] = Field(default_factory=list)
    document_version_ids: list[str] = Field(default_factory=list)
    created_at: str = Field(default="", description="ISO-8601 UTC")
    updated_at: str = Field(default="", description="ISO-8601 UTC")
    version: int = Field(default=1, ge=1)


class PlacementAssertion(BaseModel):
    """A claim that a canonical node belongs under a parent taxonomy node."""

    id: str = Field(..., pattern=r"^assert-placement-[a-z0-9-]+$")
    node_id: str
    parent_node_id: str
    reasoning_summary: str = Field(..., min_length=1)
    confidence: float = Field(..., ge=0.0, le=1.0)
    validation_status: ValidationState = ValidationState.CANDIDATE
    evidence_ids: list[str] = Field(default_factory=list)
    created_at: str = Field(default="", description="ISO-8601 UTC")
    version: int = Field(default=1, ge=1)


class MergeAssertion(BaseModel):
    """A claim that two candidate nodes represent the same canonical unit."""

    id: str = Field(..., pattern=r"^assert-merge-[a-z0-9-]+$")
    from_node_id: str
    to_node_id: str
    reasoning_summary: str = Field(..., min_length=1)
    confidence: float = Field(..., ge=0.0, le=1.0)
    validation_status: ValidationState = ValidationState.CANDIDATE
    evidence_ids: list[str] = Field(default_factory=list)
    created_at: str = Field(default="", description="ISO-8601 UTC")
    version: int = Field(default=1, ge=1)


# ---------------------------------------------------------------------------
# Phase 2 — Atomic knowledge extraction candidates
# ---------------------------------------------------------------------------

class KnowledgeUnitCandidate(BaseModel):
    """A pre-canonical knowledge unit extracted from a chunk by an LLM."""

    id: str = Field(..., pattern=r"^cand-[a-z0-9-]+$")
    unit_type: Literal["concept", "definition", "rule", "procedure", "exception"]
    label: str = Field(..., min_length=1, description="Short name or term")
    text: str = Field(..., min_length=1, description="Full extracted text / definition / rule statement")
    span_ids: list[str] = Field(default_factory=list, description="EvidenceSpan IDs supporting this candidate")
    chunk_id: str = Field(..., description="Source chunk ID")
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    extraction_run_id: str = Field(default="", description="Traceable run ID")
    embedding: list[float] | None = Field(default=None, description="Vector embedding for deduplication")
    created_at: str = Field(default="", description="ISO-8601 UTC")


class ExtractionResult(BaseModel):
    """Output of one extraction call over a single chunk for one unit type."""

    unit_type: Literal["concept", "definition", "rule", "procedure", "exception"]
    candidates: list[KnowledgeUnitCandidate] = Field(default_factory=list)
    chunk_id: str = Field(..., description="Source chunk ID")
    model: str = Field(default="", description="LLM model used")
    prompt_tokens: int | None = Field(default=None)
    response_tokens: int | None = Field(default=None)
    duration_ms: int = Field(default=0)
    error: str | None = Field(default=None)
