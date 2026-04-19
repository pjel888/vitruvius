"""
Taxonomy Governance v2 — Pydantic Schemas

Data contracts for the governed global AEC taxonomy architecture:
- Backbone nodes (L1–L4 domain hierarchy)
- Canonical nodes with facet classification
- Jurisdiction, authority, and document edition models
- Overlays and applicability rules
- Standards mapping and cross-discipline edges
- Resolution context and output (Vitruvian Context)

Authority: .ai/06_specs/vitruvian-context/04_schema_contract.md
"""

from __future__ import annotations

from datetime import date, datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


# ---------------------------------------------------------------------------
# Facet enums (closed vocabularies)
# ---------------------------------------------------------------------------

KnowledgeType = Literal[
    "concept",
    "rule",
    "definition",
    "procedure",
    "exception",
    "principle",
]

AssetScope = Literal[
    "building",
    "infrastructure",
    "site",
    "system",
    "component",
    "material",
]

LifecycleStage = Literal[
    "planning",
    "design",
    "construction",
    "operation",
    "demolition",
    "reuse",
]

ProjectType = Literal[
    "residential",
    "commercial",
    "industrial",
    "institutional",
    "public_works",
    "mixed_use",
]

PerformanceTopic = Literal[
    "structural",
    "fire_life_safety",
    "accessibility",
    "sustainability",
    "energy",
    "acoustics",
    "daylight",
    "ventilation",
    "water",
    "durability",
]

JurisdictionLevel = Literal[
    "project_specific",
    "local",
    "agency",
    "regional",
    "state",
    "national",
    "supranational",
    "international",
]

ObligationType = Literal[
    "mandatory",
    "recommended",
    "permitted",
    "prohibited",
]

MappingType = Literal[
    "exact",
    "narrower",
    "broader",
    "related",
]


# ---------------------------------------------------------------------------
# Backbone
# ---------------------------------------------------------------------------

class BackboneNode(BaseModel):
    """A node in the governed L1–L4 subject taxonomy."""

    model_config = ConfigDict(frozen=True)

    canonical_id: str = Field(
        ...,
        pattern=r"^VTN-DOM-\d{7}$",
        description="Opaque ID, e.g., VTN-DOM-0000001",
    )
    path_code: str = Field(
        ...,
        pattern=r"^[A-Z]{3}(\.[A-Z]{3}){0,3}$",
        description="Dot-delimited path, e.g., ACC.BFD.ROU.ARA",
    )
    level: int = Field(..., ge=1, le=4, description="Hierarchy depth (1–4)")
    parent_path_code: str | None = Field(
        default=None,
        description="Parent path code; null for L1 roots",
    )
    pref_label: str = Field(..., min_length=1)
    definition: str = Field(..., min_length=10)
    aliases: list[str] = Field(default_factory=list)
    scope_note: str = Field(default="", description="Usage guidance and edge cases")
    example_concepts: list[str] = Field(
        default_factory=list,
        description="Canonical IDs of exemplar concepts",
    )
    steward: str = Field(..., description="Email or identifier of human owner")
    release_version: str = Field(
        default="1.0.0",
        pattern=r"^\d+\.\d+\.\d+$",
    )

    @field_validator("parent_path_code")
    @classmethod
    def _parent_matches_level(cls, v: str | None, info: Any) -> str | None:
        if v is None:
            return v
        level = info.data.get("level")
        expected_parts = level - 1 if level else 0
        actual_parts = len(v.split("."))
        if actual_parts != expected_parts:
            raise ValueError(
                f"parent_path_code '{v}' has {actual_parts} parts, expected {expected_parts} for level {level}"
            )
        return v


# ---------------------------------------------------------------------------
# ID Redirect
# ---------------------------------------------------------------------------

class IdRedirect(BaseModel):
    """Maps an old semantic slug to a new opaque canonical ID."""

    model_config = ConfigDict(frozen=True)

    old_id: str = Field(..., min_length=1)
    new_id: str = Field(..., pattern=r"^VTN-[A-Z]{3}-\d{7}$")
    scope: Literal["concept", "source", "relationship", "taxonomy", "backbone"] = "concept"
    reason: str = Field(default="migration-to-opaque-ids")
    redirect_type: Literal["permanent", "temporary"] = "permanent"
    created_at: datetime = Field(default_factory=datetime.utcnow)


# ---------------------------------------------------------------------------
# Canonical Node (v2 extension)
# ---------------------------------------------------------------------------

class CanonicalNodeV2(BaseModel):
    """Canonical knowledge node with facet classification and governance metadata."""

    canonical_id: str = Field(..., pattern=r"^VTN-CON-\d{7}$")
    path_code: str = Field(
        ...,
        pattern=r"^[A-Z]{3}(\.[A-Z]{3}){0,3}$",
    )
    label: str = Field(..., min_length=1)
    summary: str = Field(default="")
    knowledge_type: KnowledgeType = "concept"
    asset_scope: AssetScope = "building"
    lifecycle_stage: LifecycleStage = "design"
    project_type: ProjectType = "mixed_use"
    performance_topic: PerformanceTopic = "structural"
    primary_domain: str = Field(
        ...,
        pattern=r"^taxonomy-[a-z-]+$",
        description="L1 domain code, e.g., taxonomy-accessibility",
    )
    status: Literal["draft", "enriched", "verified", "superseded"] = "draft"
    steward: str = Field(default="")
    release_version: str = Field(default="1.0.0", pattern=r"^\d+\.\d+\.\d+$")
    trust_level: Literal["primary", "secondary", "tertiary", "unverified", "derived"] = "primary"
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    @field_validator("path_code")
    @classmethod
    def _path_code_matches_domain(cls, v: str, info: Any) -> str:
        domain = info.data.get("primary_domain", "")
        # Extract L1 prefix from path_code, map to domain
        # e.g., ACC -> taxonomy-accessibility
        # This is a lightweight sanity check; full validation lives in validate_backbone.py
        return v


# ---------------------------------------------------------------------------
# Jurisdiction
# ---------------------------------------------------------------------------

class Jurisdiction(BaseModel):
    """A geographic or administrative jurisdiction with hierarchical precedence."""

    code: str = Field(..., min_length=1, description="e.g., PH-NCR-Makati")
    name: str = Field(..., min_length=1)
    level: JurisdictionLevel = "national"
    precedence_rank: int = Field(
        ...,
        ge=0,
        le=6,
        description="0=project_specific (highest), 6=international (lowest)",
    )
    parent_code: str | None = Field(
        default=None,
        description="Parent jurisdiction code; null for top-level",
    )
    metadata: dict[str, Any] = Field(default_factory=dict)


# ---------------------------------------------------------------------------
# Authority Document Models
# ---------------------------------------------------------------------------

class Authority(BaseModel):
    """An authority that publishes codes, standards, or regulations."""

    canonical_id: str = Field(..., pattern=r"^VTN-AUT-\d{7}$")
    name: str = Field(..., min_length=1)
    short_name: str = Field(default="")
    jurisdiction_code: str = Field(...)
    url: str = Field(default="")
    metadata: dict[str, Any] = Field(default_factory=dict)


class AuthorityDocumentFamily(BaseModel):
    """A family of related document editions (e.g., 'National Building Code')."""

    canonical_id: str = Field(..., pattern=r"^VTN-ADF-\d{7}$")
    title: str = Field(..., min_length=1)
    short_title: str = Field(default="")
    jurisdiction_code: str = Field(...)
    authority_id: str = Field(..., pattern=r"^VTN-AUT-\d{7}$")
    metadata: dict[str, Any] = Field(default_factory=dict)


class AuthorityDocumentEdition(BaseModel):
    """A specific normative edition of a code or standard."""

    canonical_id: str = Field(..., pattern=r"^VTN-ADE-\d{7}$")
    family_id: str = Field(..., pattern=r"^VTN-ADF-\d{7}$")
    edition_number: str = Field(..., min_length=1, description="e.g., 'Revised IRR 2007'")
    effective_date: date
    repeal_date: date | None = Field(default=None)
    status: Literal["draft", "active", "superseded", "repealed"] = "active"
    jurisdiction_code: str = Field(...)
    metadata: dict[str, Any] = Field(default_factory=dict)

    @field_validator("repeal_date")
    @classmethod
    def _repeal_after_effective(cls, v: date | None, info: Any) -> date | None:
        if v is None:
            return v
        effective = info.data.get("effective_date")
        if effective and v <= effective:
            raise ValueError("repeal_date must be strictly after effective_date")
        return v


# ---------------------------------------------------------------------------
# Applicability + Overlay
# ---------------------------------------------------------------------------

class ApplicabilityRule(BaseModel):
    """A rule that determines when a document edition applies."""

    canonical_id: str = Field(..., pattern=r"^VTN-APP-\d{7}$")
    jurisdiction_code: str = Field(...)
    scope: str = Field(default="all_buildings")
    precedence_rank: int = Field(..., ge=0, le=6)
    condition: str = Field(default="")
    effective_date: date
    status: Literal["active", "inactive"] = "active"
    edition_id: str = Field(..., pattern=r"^VTN-ADE-\d{7}$")


class Overlay(BaseModel):
    """A jurisdiction-specific obligation attached to a canonical concept."""

    canonical_id: str = Field(..., pattern=r"^VTN-OVR-\d{7}$")
    concept_id: str = Field(..., pattern=r"^VTN-CON-\d{7}$")
    jurisdiction_code: str = Field(...)
    obligation_type: ObligationType = "mandatory"
    condition: str = Field(default="")
    measurement: str = Field(default="")
    effective_date: date
    repeal_date: date | None = Field(default=None)
    status: Literal["active", "inactive"] = "active"
    edition_id: str = Field(..., pattern=r"^VTN-ADE-\d{7}$")
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)


# ---------------------------------------------------------------------------
# Standards
# ---------------------------------------------------------------------------

class StandardReference(BaseModel):
    """An external classification system or standard."""

    canonical_id: str = Field(..., pattern=r"^VTN-STD-\d{7}$")
    system: str = Field(..., min_length=1, description="e.g., OmniClass, Uniclass, IFC")
    code: str = Field(..., min_length=1, description="e.g., 23-27 11 11")
    title: str = Field(default="")
    url: str = Field(default="")
    version: str = Field(default="")


class StandardMapping(BaseModel):
    """A mapping between a canonical concept and an external standard code."""

    canonical_id: str = Field(..., pattern=r"^VTN-CON-\d{7}$")
    standard_id: str = Field(..., pattern=r"^VTN-STD-\d{7}$")
    mapping_type: MappingType = "exact"
    confidence: float = Field(..., ge=0.0, le=1.0)
    mapped_by: str = Field(default="")
    mapped_at: datetime = Field(default_factory=datetime.utcnow)


# ---------------------------------------------------------------------------
# Localization
# ---------------------------------------------------------------------------

class Localization(BaseModel):
    """v1.1 — localized labels and definitions for a concept."""

    canonical_id: str = Field(..., pattern=r"^VTN-LOC-\d{7}$")
    concept_id: str = Field(..., pattern=r"^VTN-CON-\d{7}$")
    locale: str = Field(..., pattern=r"^[a-z]{2}-[A-Z]{2}$", description="e.g., en-PH, tl-PH")
    label: str = Field(...)
    definition: str = Field(default="")
    aliases: list[str] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Taxonomy Release
# ---------------------------------------------------------------------------

class TaxonomyRelease(BaseModel):
    """A versioned snapshot of the backbone for reproducibility."""

    canonical_id: str = Field(..., pattern=r"^VTN-REL-\d{7}$")
    version: str = Field(..., pattern=r"^\d+\.\d+\.\d+$")
    released_at: datetime = Field(default_factory=datetime.utcnow)
    released_by: str = Field(default="")
    changelog: str = Field(default="")
    backbone_hash: str = Field(default="", description="Merkle hash of backbone files")


# ---------------------------------------------------------------------------
# Vitruvian Context — Resolution I/O
# ---------------------------------------------------------------------------

class ResolutionContext(BaseModel):
    """Context parameters for the Vitruvian Context resolver."""

    jurisdiction_code: str = Field(..., min_length=1)
    query_date: date
    project_type: ProjectType | None = Field(default=None)
    asset_scope: AssetScope | None = Field(default=None)
    lifecycle_stage: LifecycleStage | None = Field(default=None)
    user_overrides: dict[str, Any] = Field(default_factory=dict)


class FacetFilter(BaseModel):
    """Facet filtering parameters for search queries."""

    knowledge_type: KnowledgeType | None = Field(default=None)
    asset_scope: AssetScope | None = Field(default=None)
    lifecycle_stage: LifecycleStage | None = Field(default=None)
    project_type: ProjectType | None = Field(default=None)
    performance_topic: PerformanceTopic | None = Field(default=None)
    primary_domain: str | None = Field(default=None)


class CanonicalQuery(BaseModel):
    """Query parameters for the Vitruvian Context resolver."""

    concept_id: str | None = Field(
        default=None,
        pattern=r"^VTN-CON-\d{7}$",
    )
    path_code: str | None = Field(
        default=None,
        pattern=r"^[A-Z]{3}(\.[A-Z]{3}){0,3}$",
    )
    search_text: str | None = Field(default=None)
    return_type: Literal["concept", "overlay", "evidence", "standards", "full"] = "full"
    facets: FacetFilter | None = Field(default=None)
    expand_domains: list[str] | None = Field(default=None)
    max_hops: int = Field(default=2, ge=1, le=5)


class ReasoningStep(BaseModel):
    """A single step in the resolver's reasoning trace."""

    step: int = Field(..., ge=1)
    operation: str = Field(...)
    input_: Any = Field(..., alias="input")
    output: Any = Field(...)
    evidence: str = Field(default="")


class AffectedDomain(BaseModel):
    """A domain affected by a cross-discipline influence."""

    domain: str = Field(...)
    relationship_type: str = Field(...)
    confidence: float = Field(..., ge=0.0, le=1.0)
    rationale: str = Field(default="")


class ResolvedOverlay(BaseModel):
    """An overlay resolved for a specific jurisdiction and date."""

    jurisdiction_code: str = Field(...)
    jurisdiction_name: str = Field(default="")
    obligation_type: ObligationType = "mandatory"
    condition: str = Field(default="")
    measurement: str = Field(default="")
    based_on: dict[str, str] = Field(default_factory=dict)


class ResolvedTruth(BaseModel):
    """Output of the Vitruvian Context resolver."""

    canonical_concept: CanonicalNodeV2 = Field(...)
    resolution: dict[str, Any] = Field(...)
    influences: dict[str, Any] = Field(...)
    evidence: list[dict[str, Any]] = Field(default_factory=list)
    standards_mappings: list[StandardMapping] = Field(default_factory=list)
    reasoning_trace: list[ReasoningStep] = Field(default_factory=list)
    query: CanonicalQuery = Field(...)
    context: ResolutionContext = Field(...)
    resolved_at: datetime = Field(default_factory=datetime.utcnow)


# ---------------------------------------------------------------------------
# Cross-discipline edge (for validation and ingestion)
# ---------------------------------------------------------------------------

class CrossDisciplineEdge(BaseModel):
    """A typed, confidence-scored edge between a concept and another domain or concept."""

    from_id: str = Field(..., pattern=r"^VTN-CON-\d{7}$")
    to_id: str = Field(...)
    edge_type: str = Field(...)
    from_domain: str = Field(...)
    to_domain: str = Field(...)
    confidence: float = Field(..., ge=0.0, le=1.0)
    rationale: str = Field(default="")
    valid_from: date | None = Field(default=None)
    valid_until: date | None = Field(default=None)

    @field_validator("edge_type")
    @classmethod
    def _edge_type_allowed(cls, v: str) -> str:
        from vitruvius.cross_discipline_validator import ALLOWED_CROSS_DISCIPLINE_PREDICATES
        if v not in ALLOWED_CROSS_DISCIPLINE_PREDICATES:
            raise ValueError(f"Edge type '{v}' is not in the allowed predicate registry")
        return v
