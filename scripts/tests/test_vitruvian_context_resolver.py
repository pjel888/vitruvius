"""
Test harness for the Vitruvian Context resolver.

Covers all 8 test cases defined in:
    .ai/06_specs/vitruvian-context/02_RESOLVER_ENGINE_SPEC.md §8

Run with: pytest scripts/tests/test_vitruvian_context_resolver.py -v
"""

from datetime import date

import pytest

from vitruvius.resolver import (
    CanonicalQuery,
    ResolutionContext,
    ResolutionError,
    resolve,
)


# ---------------------------------------------------------------------------
# TC-01: Philippine Accessible Ramp
# ---------------------------------------------------------------------------

def test_tc01_philippine_accessible_ramp():
    """
    TC-01: Basic resolution for Accessible Ramps in Philippines.
    Expected: concept resolved, PH overlay returned, evidence present,
    standards mapping present, reasoning trace complete.
    """
    query = CanonicalQuery(
        concept_id="VTN-CON-0000042",
        return_type="full",
    )
    context = ResolutionContext(
        jurisdiction_code="PH",
        query_date=date(2026, 4, 19),
    )

    result = resolve(query, context)

    # Canonical concept
    assert result.canonical_concept["canonical_id"] == "VTN-CON-0000042"
    assert result.canonical_concept["label"] == "Accessible Ramps"
    assert result.canonical_concept["primary_domain"] == "taxonomy-accessibility"

    # Jurisdiction resolution
    assert len(result.resolution["jurisdiction_chain"]) == 1
    assert result.resolution["jurisdiction_chain"][0]["code"] == "PH"

    # Overlay
    assert len(result.resolution["applicable_overlays"]) == 1
    overlay = result.resolution["applicable_overlays"][0]
    assert overlay["jurisdiction_code"] == "PH"
    assert overlay["obligation_type"] == "mandatory"
    assert overlay["condition"] == "slope_max_1_12"

    # Evidence
    assert len(result.evidence) >= 1
    assert result.evidence[0]["snippet"].startswith("Ramps shall be provided")

    # Standards
    assert len(result.standards_mappings) == 1
    assert result.standards_mappings[0]["system"] == "OmniClass"
    assert result.standards_mappings[0]["code"] == "23-27 11 11"

    # Reasoning trace
    assert len(result.reasoning_trace) == 6
    assert result.reasoning_trace[0].operation == "IDENTIFY"
    assert result.reasoning_trace[2].operation == "OVERLAY"

    # Non-mutation invariant
    assert result.canonical_concept["label"] == "Accessible Ramps"


# ---------------------------------------------------------------------------
# TC-02: Makati Override
# ---------------------------------------------------------------------------

def test_tc02_makati_override():
    """
    TC-02: Local jurisdiction overrides national.
    Expected: Makati overlay (slope_max_1_10) wins over PH overlay (slope_max_1_12).
    """
    query = CanonicalQuery(
        concept_id="VTN-CON-0000042",
        return_type="full",
    )
    context = ResolutionContext(
        jurisdiction_code="PH-NCR-Makati",
        query_date=date(2026, 4, 19),
    )

    result = resolve(query, context)

    # Jurisdiction chain: Makati → NCR → PH
    chain_codes = [j["code"] for j in result.resolution["jurisdiction_chain"]]
    assert chain_codes == ["PH-NCR-Makati", "PH-NCR", "PH"]

    # Overlay: Makati wins (precedence_rank 1 < 4)
    assert len(result.resolution["applicable_overlays"]) == 1
    overlay = result.resolution["applicable_overlays"][0]
    assert overlay["jurisdiction_code"] == "PH-NCR-Makati"
    assert overlay["condition"] == "slope_max_1_10"

    # Reasoning trace documents precedence decision
    overlay_step = [s for s in result.reasoning_trace if s.operation == "OVERLAY"][0]
    assert "precedence" in overlay_step.evidence.lower()


# ---------------------------------------------------------------------------
# TC-03: Cross-Discipline Query
# ---------------------------------------------------------------------------

def test_tc03_cross_discipline_influences():
    """
    TC-03: Query returns cross-discipline influences.
    Expected: Primary domain = Structural, affected domains include Architecture.
    """
    query = CanonicalQuery(
        concept_id="VTN-CON-0000100",
        expand_domains=["taxonomy-architecture", "taxonomy-construction"],
        max_hops=2,
        return_type="full",
    )
    context = ResolutionContext(
        jurisdiction_code="PH",
        query_date=date(2026, 4, 19),
    )

    result = resolve(query, context)

    # Primary domain
    assert result.influences["primary_domain"] == "taxonomy-structural"

    # Affected domains
    affected_domains = [a["domain"] for a in result.influences["affected_domains"]]
    assert "taxonomy-architecture" in affected_domains

    # Relationship type
    arch_influence = [a for a in result.influences["affected_domains"] if a["domain"] == "taxonomy-architecture"][0]
    assert arch_influence["relationship_type"] == "CONSTRAINS"
    assert arch_influence["confidence"] >= 0.90


# ---------------------------------------------------------------------------
# TC-04: Future Date Warning
# ---------------------------------------------------------------------------

def test_tc04_future_date():
    """
    TC-04: Query with future date should still resolve but may include warnings.
    Stub: we accept future dates without warning since mock data has no future editions.
    Full implementation will add warning to reasoning trace.
    """
    query = CanonicalQuery(
        concept_id="VTN-CON-0000042",
        return_type="full",
    )
    context = ResolutionContext(
        jurisdiction_code="PH",
        query_date=date(2030, 1, 1),
    )

    result = resolve(query, context)

    # Should still resolve
    assert result.canonical_concept["canonical_id"] == "VTN-CON-0000042"

    # Overlay should still be found (effective_date 2007 < 2030)
    assert len(result.resolution["applicable_overlays"]) == 1


# ---------------------------------------------------------------------------
# TC-05: Invalid Jurisdiction
# ---------------------------------------------------------------------------

def test_tc05_invalid_jurisdiction():
    """
    TC-05: Invalid jurisdiction code should raise ResolutionError.
    """
    query = CanonicalQuery(
        concept_id="VTN-CON-0000042",
        return_type="full",
    )
    context = ResolutionContext(
        jurisdiction_code="XX-Invalid",
        query_date=date(2026, 4, 19),
    )

    with pytest.raises(ResolutionError) as exc_info:
        resolve(query, context)

    assert exc_info.value.code == "INVALID_JURISDICTION"


# ---------------------------------------------------------------------------
# TC-06: No Overlay Found
# ---------------------------------------------------------------------------

def test_tc06_no_overlay():
    """
    TC-06: Concept exists but no overlay for requested jurisdiction.
    Expected: Return canonical concept with empty overlays list.
    """
    query = CanonicalQuery(
        concept_id="VTN-CON-0000100",  # Reinforced Concrete — no overlays in mock
        return_type="full",
    )
    context = ResolutionContext(
        jurisdiction_code="PH",
        query_date=date(2026, 4, 19),
    )

    result = resolve(query, context)

    assert result.canonical_concept["canonical_id"] == "VTN-CON-0000100"
    assert result.resolution["applicable_overlays"] == []
    assert result.resolution["effective_documents"] == []


# ---------------------------------------------------------------------------
# TC-07: Search by Text
# ---------------------------------------------------------------------------

def test_tc07_search_by_text():
    """
    TC-07: Resolve by search text instead of concept ID.
    """
    query = CanonicalQuery(
        search_text="ramps",
        return_type="full",
    )
    context = ResolutionContext(
        jurisdiction_code="PH",
        query_date=date(2026, 4, 19),
    )

    result = resolve(query, context)

    assert result.canonical_concept["label"] == "Accessible Ramps"
    assert result.canonical_concept["canonical_id"] == "VTN-CON-0000042"


# ---------------------------------------------------------------------------
# TC-08: Confidence Threshold Filtering
# ---------------------------------------------------------------------------

def test_tc08_confidence_threshold():
    """
    TC-08: User override for confidence threshold.
    Expected: Standards mappings below threshold are filtered out.
    """
    query = CanonicalQuery(
        concept_id="VTN-CON-0000042",
        return_type="full",
    )
    context = ResolutionContext(
        jurisdiction_code="PH",
        query_date=date(2026, 4, 19),
        user_overrides={"confidence_threshold": 0.95},
    )

    result = resolve(query, context)

    # OmniClass mapping has confidence 0.92, which is below 0.95 threshold
    assert len(result.standards_mappings) == 0

    # Verify trace mentions threshold
    standards_step = [s for s in result.reasoning_trace if s.operation == "STANDARDS"][0]
    assert "0.95" in standards_step.input


# ---------------------------------------------------------------------------
# Invariant Tests
# ---------------------------------------------------------------------------

def test_resolver_is_read_only():
    """
    I9: The resolver never mutates canonical nodes.
    """
    query = CanonicalQuery(concept_id="VTN-CON-0000042", return_type="full")
    context = ResolutionContext(jurisdiction_code="PH", query_date=date(2026, 4, 19))

    # Resolve twice
    result1 = resolve(query, context)
    result2 = resolve(query, context)

    # Concept should be unchanged
    assert result1.canonical_concept == result2.canonical_concept


def test_resolver_is_deterministic():
    """
    VC-N02: Same input always produces identical output (modulo resolved_at).
    """
    query = CanonicalQuery(concept_id="VTN-CON-0000042", return_type="full")
    context = ResolutionContext(jurisdiction_code="PH", query_date=date(2026, 4, 19))

    result1 = resolve(query, context)
    result2 = resolve(query, context)

    # Compare everything except resolved_at
    assert result1.canonical_concept == result2.canonical_concept
    assert result1.resolution == result2.resolution
    assert result1.influences == result2.influences
    assert result1.evidence == result2.evidence
    assert result1.standards_mappings == result2.standards_mappings
    assert len(result1.reasoning_trace) == len(result2.reasoning_trace)


# ---------------------------------------------------------------------------
# Performance Benchmarks (informative, not strict gates)
# ---------------------------------------------------------------------------

def test_tc_performance_single_concept():
    """
    VC-P01: Single concept resolution should complete in <100ms.
    This is an informative benchmark; CI may vary.
    """
    import time

    query = CanonicalQuery(concept_id="VTN-CON-0000042", return_type="full")
    context = ResolutionContext(jurisdiction_code="PH", query_date=date(2026, 4, 19))

    start = time.perf_counter()
    for _ in range(100):
        resolve(query, context)
    elapsed = time.perf_counter() - start

    avg_ms = (elapsed / 100) * 1000
    # Informative assertion: log if >100ms but don't fail
    if avg_ms > 100:
        pytest.skip(f"Average latency {avg_ms:.1f}ms exceeds 100ms target (informative only)")
