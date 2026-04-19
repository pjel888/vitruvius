"""
Vitruvian Context Resolver — Stub Implementation

This module provides the core resolve() interface for the Vitruvian Context.
It is intentionally a stub: it uses in-memory mock data and demonstrates the
contract, precedence logic, and reasoning trace. It will be replaced by a
full Neo4j-backed implementation in PR-17.

Authority: .ai/06_specs/vitruvian-context/02_RESOLVER_ENGINE_SPEC.md
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from datetime import datetime, date
from typing import Any, Optional


# ---------------------------------------------------------------------------
# Data models
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class ResolutionContext:
    jurisdiction_code: str
    query_date: date
    project_type: Optional[str] = None
    asset_scope: Optional[str] = None
    lifecycle_stage: Optional[str] = None
    user_overrides: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class CanonicalQuery:
    concept_id: Optional[str] = None
    path_code: Optional[str] = None
    search_text: Optional[str] = None
    return_type: str = "full"
    facets: Optional[dict[str, str]] = None
    expand_domains: Optional[list[str]] = None
    max_hops: int = 2


@dataclass
class ReasoningStep:
    step: int
    operation: str
    input: Any
    output: Any
    evidence: str


@dataclass
class ResolvedTruth:
    canonical_concept: dict[str, Any]
    resolution: dict[str, Any]
    influences: dict[str, Any]
    evidence: list[dict[str, Any]]
    standards_mappings: list[dict[str, Any]]
    reasoning_trace: list[ReasoningStep]
    query: CanonicalQuery
    context: ResolutionContext
    resolved_at: str


# ---------------------------------------------------------------------------
# Mock data store
# ---------------------------------------------------------------------------

MOCK_CONCEPTS: dict[str, dict[str, Any]] = {
    "VTN-CON-0000042": {
        "canonical_id": "VTN-CON-0000042",
        "path_code": "ACC.BFD.ROU.ARA",
        "label": "Accessible Ramps",
        "knowledge_type": "concept",
        "asset_scope": "building",
        "lifecycle_stage": "design",
        "project_type": "mixed_use",
        "performance_topic": "accessibility",
        "primary_domain": "taxonomy-accessibility",
        "summary": "Ramps provide accessible routes for persons with disabilities.",
    },
    "VTN-CON-0000100": {
        "canonical_id": "VTN-CON-0000100",
        "path_code": "STR.RCD.001",
        "label": "Reinforced Concrete Detailing",
        "knowledge_type": "concept",
        "asset_scope": "building",
        "lifecycle_stage": "design",
        "project_type": "mixed_use",
        "performance_topic": "structural",
        "primary_domain": "taxonomy-structural",
        "summary": "Reinforced concrete detailing for structural elements.",
    },
}

MOCK_JURISDICTIONS: dict[str, dict[str, Any]] = {
    "PH": {"code": "PH", "name": "Philippines", "level": "national", "precedence_rank": 4, "parent": None},
    "PH-NCR": {"code": "PH-NCR", "name": "National Capital Region", "level": "regional", "precedence_rank": 3, "parent": "PH"},
    "PH-NCR-Makati": {"code": "PH-NCR-Makati", "name": "Makati City", "level": "local", "precedence_rank": 1, "parent": "PH-NCR"},
}

MOCK_OVERLAYS: list[dict[str, Any]] = [
    {
        "id": "VTN-OVR-0000001",
        "concept_id": "VTN-CON-0000042",
        "jurisdiction_code": "PH",
        "obligation_type": "mandatory",
        "condition": "slope_max_1_12",
        "measurement": "1:12",
        "effective_date": date(2007, 1, 1),
        "repeal_date": None,
        "precedence_rank": 4,
        "based_on": {"family": "Batas Pambansa Blg. 344", "edition": "Revised IRR 2007", "effective_date": "2007-01-01"},
    },
    {
        "id": "VTN-OVR-0000002",
        "concept_id": "VTN-CON-0000042",
        "jurisdiction_code": "PH-NCR-Makati",
        "obligation_type": "mandatory",
        "condition": "slope_max_1_10",
        "measurement": "1:10",
        "effective_date": date(2015, 1, 1),
        "repeal_date": None,
        "precedence_rank": 1,
        "based_on": {"family": "Makati City Ordinance 2020-001", "edition": "2020", "effective_date": "2020-01-01"},
    },
]

MOCK_EVIDENCE: list[dict[str, Any]] = [
    {
        "id": "VTN-EVS-0000001",
        "concept_id": "VTN-CON-0000042",
        "source_edition": "Revised IRR 2007",
        "section_id": "section-1",
        "snippet": "Ramps shall be provided as an alternative to stairs...",
        "confidence": 0.95,
    },
]

MOCK_STANDARDS: list[dict[str, Any]] = [
    {
        "concept_id": "VTN-CON-0000042",
        "system": "OmniClass",
        "code": "23-27 11 11",
        "title": "Ramps",
        "confidence": 0.92,
    },
]

MOCK_INFLUENCES: list[dict[str, Any]] = [
    {
        "concept_id": "VTN-CON-0000042",
        "target_domain": "taxonomy-architecture",
        "relationship_type": "CONSTRAINS",
        "confidence": 0.95,
        "rationale": "Ramp slope constrains architectural clearances",
    },
    {
        "concept_id": "VTN-CON-0000042",
        "target_domain": "taxonomy-construction",
        "relationship_type": "EXECUTED_IN",
        "confidence": 0.98,
        "rationale": "Ramps are built during construction",
    },
    {
        "concept_id": "VTN-CON-0000100",
        "target_domain": "taxonomy-architecture",
        "relationship_type": "CONSTRAINS",
        "confidence": 0.95,
        "rationale": "Rebar cover determines finish clearance",
    },
]

# ---------------------------------------------------------------------------
# Precedence constants
# ---------------------------------------------------------------------------

PRECEDENCE_ORDER = [
    "project-specific",
    "local",
    "agency",
    "regional",
    "state",
    "national",
    "supranational",
    "international",
]


# ---------------------------------------------------------------------------
# Resolver functions
# ---------------------------------------------------------------------------

def _resolve_jurisdiction_chain(code: str) -> list[dict[str, Any]]:
    """Build jurisdiction chain from most specific to most general."""
    chain = []
    seen = set()
    current = code
    while current and current not in seen:
        seen.add(current)
        jurisdiction = MOCK_JURISDICTIONS.get(current)
        if not jurisdiction:
            break
        chain.append(jurisdiction)
        current = jurisdiction.get("parent")
    return chain


def _find_concept(query: CanonicalQuery) -> Optional[dict[str, Any]]:
    """Identify concept by ID, path code, or search text."""
    if query.concept_id:
        return MOCK_CONCEPTS.get(query.concept_id)
    if query.path_code:
        for concept in MOCK_CONCEPTS.values():
            if concept["path_code"] == query.path_code:
                return concept
    if query.search_text:
        # Simple substring match for stub
        for concept in MOCK_CONCEPTS.values():
            if query.search_text.lower() in concept["label"].lower():
                return concept
    return None


def _select_overlay(
    concept_id: str, jurisdiction_chain: list[dict[str, Any]], query_date: date
) -> Optional[dict[str, Any]]:
    """Select highest-precedence applicable overlay."""
    candidates = []
    for overlay in MOCK_OVERLAYS:
        if overlay["concept_id"] != concept_id:
            continue
        # Check temporal validity
        if overlay["effective_date"] > query_date:
            continue
        if overlay["repeal_date"] and overlay["repeal_date"] <= query_date:
            continue
        # Check jurisdiction match
        for jurisdiction in jurisdiction_chain:
            if overlay["jurisdiction_code"] == jurisdiction["code"]:
                candidates.append(overlay)
                break

    if not candidates:
        return None

    # Sort by precedence rank (lower number = higher precedence)
    candidates.sort(key=lambda o: o["precedence_rank"])
    return candidates[0]


def _gather_evidence(concept_id: str, overlay_id: Optional[str]) -> list[dict[str, Any]]:
    """Gather evidence spans for concept and optional overlay."""
    evidence = [e for e in MOCK_EVIDENCE if e["concept_id"] == concept_id]
    # In full implementation, also gather overlay-specific evidence
    return evidence


def _gather_standards(concept_id: str, threshold: float = 0.70) -> list[dict[str, Any]]:
    """Gather standards mappings above confidence threshold."""
    return [s for s in MOCK_STANDARDS if s["concept_id"] == concept_id and s["confidence"] >= threshold]


def _gather_influences(concept_id: str, expand_domains: Optional[list[str]], max_hops: int) -> dict[str, Any]:
    """Gather cross-discipline influences."""
    primary_domain = MOCK_CONCEPTS.get(concept_id, {}).get("primary_domain", "unknown")
    affected = []
    regulating = []

    for influence in MOCK_INFLUENCES:
        if influence["concept_id"] != concept_id:
            continue
        if expand_domains and influence["target_domain"] not in expand_domains:
            continue
        if influence["relationship_type"] == "REGULATED_BY":
            regulating.append({
                "domain": influence["target_domain"],
                "relationship_type": influence["relationship_type"],
                "confidence": influence["confidence"],
                "rationale": influence["rationale"],
            })
        else:
            affected.append({
                "domain": influence["target_domain"],
                "relationship_type": influence["relationship_type"],
                "confidence": influence["confidence"],
                "rationale": influence["rationale"],
            })

    return {
        "primary_domain": primary_domain,
        "affected_domains": affected,
        "regulating_domains": regulating,
    }


def resolve(query: CanonicalQuery, context: ResolutionContext) -> ResolvedTruth:
    """
    Main Vitruvian Context resolver entrypoint.

    Transforms a canonical query + resolution context into a ResolvedTruth
    with reasoning trace.
    """
    resolved_at = datetime.now().astimezone().isoformat()
    trace: list[ReasoningStep] = []

    # Step 1: Identify concept
    concept = _find_concept(query)
    if not concept:
        raise ResolutionError("CONCEPT_NOT_FOUND", "No concept matches the query")

    trace.append(ReasoningStep(
        step=1,
        operation="IDENTIFY",
        input=query,
        output=concept["canonical_id"],
        evidence=f"Matched concept by {query.concept_id or query.path_code or query.search_text}",
    ))

    # Step 2: Validate context + build jurisdiction chain
    jurisdiction_chain = _resolve_jurisdiction_chain(context.jurisdiction_code)
    if not jurisdiction_chain:
        raise ResolutionError("INVALID_JURISDICTION", f"Unknown jurisdiction code: {context.jurisdiction_code}")

    trace.append(ReasoningStep(
        step=2,
        operation="JURISDICTION",
        input=context.jurisdiction_code,
        output=[j["code"] for j in jurisdiction_chain],
        evidence=f"Resolved {len(jurisdiction_chain)} jurisdictions in chain",
    ))

    # Step 3: Gather and select overlay
    selected_overlay = _select_overlay(concept["canonical_id"], jurisdiction_chain, context.query_date)
    trace.append(ReasoningStep(
        step=3,
        operation="OVERLAY",
        input=len([o for o in MOCK_OVERLAYS if o["concept_id"] == concept["canonical_id"]]),
        output=selected_overlay["id"] if selected_overlay else None,
        evidence="Selected by precedence: local > regional > national",
    ))

    # Step 4: Gather evidence
    evidence = _gather_evidence(concept["canonical_id"], selected_overlay["id"] if selected_overlay else None)
    trace.append(ReasoningStep(
        step=4,
        operation="EVIDENCE",
        input="all_sources",
        output=len(evidence),
        evidence=f"Gathered {len(evidence)} evidence spans",
    ))

    # Step 5: Gather standards mappings
    threshold = context.user_overrides.get("confidence_threshold", 0.70)
    mappings = _gather_standards(concept["canonical_id"], threshold)
    trace.append(ReasoningStep(
        step=5,
        operation="STANDARDS",
        input=f"threshold={threshold}",
        output=len(mappings),
        evidence=f"Found {len(mappings)} standards mappings above threshold",
    ))

    # Step 6: Gather cross-discipline influences
    influences = _gather_influences(
        concept["canonical_id"],
        query.expand_domains,
        query.max_hops,
    )
    trace.append(ReasoningStep(
        step=6,
        operation="INFLUENCES",
        input=influences["primary_domain"],
        output=len(influences["affected_domains"]),
        evidence=f"Primary domain: {influences['primary_domain']}",
    ))

    # Step 7: Assemble resolution metadata
    resolution = {
        "jurisdiction_chain": jurisdiction_chain,
        "applicable_overlays": [selected_overlay] if selected_overlay else [],
        "effective_documents": [selected_overlay["based_on"]] if selected_overlay else [],
        "precedence_applied": ["jurisdiction", "temporal"],
    }

    return ResolvedTruth(
        canonical_concept=concept,
        resolution=resolution,
        influences=influences,
        evidence=evidence,
        standards_mappings=mappings,
        reasoning_trace=trace,
        query=query,
        context=context,
        resolved_at=resolved_at,
    )


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------

class ResolutionError(Exception):
    """Standard error for Vitruvian Context resolution failures."""

    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(f"[{code}] {message}")
