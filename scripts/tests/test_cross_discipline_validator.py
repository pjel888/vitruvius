"""
Test harness for the Cross-Discipline Edge Validator.

Covers validation rules defined in:
    .ai/06_specs/vitruvian-context/01_CROSS_DISCIPLINE_RELATIONSHIP_TAXONOMY.md §4

Run with: pytest scripts/tests/test_cross_discipline_validator.py -v
"""

import pytest

from vitruvius.cross_discipline_validator import (
    ALLOWED_CROSS_DISCIPLINE_PREDICATES,
    validate_cross_discipline_graph,
    ValidationResult,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _concept(cid: str, domain: str = "taxonomy-structural") -> dict:
    return {"canonical_id": cid, "primary_domain": domain}


def _edge(frm: str, to: str, etype: str, from_domain: str = "", to_domain: str = "", confidence: float = 0.9) -> dict:
    return {
        "from": frm,
        "to": to,
        "type": etype,
        "from_domain": from_domain or "taxonomy-structural",
        "to_domain": to_domain or "taxonomy-structural",
        "confidence": confidence,
    }


# ---------------------------------------------------------------------------
# primary_domain facet presence
# ---------------------------------------------------------------------------

def test_primary_domain_present_ok():
    concepts = [_concept("VTN-CON-0001", "taxonomy-structural")]
    edges = []
    result = validate_cross_discipline_graph(concepts, edges)
    assert result.passed is True
    assert not any(v.rule == "PRIMARY_DOMAIN_MISSING" for v in result.violations)


def test_primary_domain_missing():
    concepts = [{"canonical_id": "VTN-CON-0001"}]  # no primary_domain facet
    edges = []
    result = validate_cross_discipline_graph(concepts, edges)
    assert result.passed is False
    assert any(v.rule == "PRIMARY_DOMAIN_MISSING" and v.concept_id == "VTN-CON-0001" for v in result.violations)


# ---------------------------------------------------------------------------
# No vague edges
# ---------------------------------------------------------------------------

def test_vague_cross_discipline_edge_detected():
    concepts = [
        _concept("VTN-CON-0001", "taxonomy-structural"),
        _concept("VTN-CON-0002", "taxonomy-architecture"),
    ]
    edges = [
        _edge("VTN-CON-0001", "VTN-CON-0002", "RELATED_TO", "taxonomy-structural", "taxonomy-architecture"),
    ]
    result = validate_cross_discipline_graph(concepts, edges)
    assert any(v.rule == "VAGUE_CROSS_DISCIPLINE_EDGE" for v in result.violations)


def test_related_to_intra_domain_allowed():
    """RELATED_TO within the same domain is not flagged."""
    concepts = [
        _concept("VTN-CON-0001", "taxonomy-structural"),
        _concept("VTN-CON-0002", "taxonomy-structural"),
    ]
    edges = [
        _edge("VTN-CON-0001", "VTN-CON-0002", "RELATED_TO", "taxonomy-structural", "taxonomy-structural"),
    ]
    result = validate_cross_discipline_graph(concepts, edges)
    assert not any(v.rule == "VAGUE_CROSS_DISCIPLINE_EDGE" for v in result.violations)


# ---------------------------------------------------------------------------
# Allowed predicates
# ---------------------------------------------------------------------------

def test_unknown_predicate_rejected():
    concepts = [_concept("VTN-CON-0001")]
    edges = [_edge("VTN-CON-0001", "VTN-CON-0002", "MYSTERY_EDGE")]
    result = validate_cross_discipline_graph(concepts, edges)
    assert any(v.rule == "UNKNOWN_PREDICATE" for v in result.violations)


def test_all_allowed_predicates_exist():
    """Smoke test: ensure the allowed set is non-empty and well-formed."""
    assert "BELONGS_TO_DOMAIN" in ALLOWED_CROSS_DISCIPLINE_PREDICATES
    assert "CONSTRAINS" in ALLOWED_CROSS_DISCIPLINE_PREDICATES
    assert "MAPS_TO_STANDARD" in ALLOWED_CROSS_DISCIPLINE_PREDICATES
    assert "RELATED_TO" not in ALLOWED_CROSS_DISCIPLINE_PREDICATES


# ---------------------------------------------------------------------------
# Domain pair constraints
# ---------------------------------------------------------------------------

def test_allowed_domain_pair_passes():
    concepts = [
        _concept("VTN-CON-0001", "taxonomy-structural"),
    ]
    edges = [
        _edge("VTN-CON-0001", "taxonomy-architecture", "CONSTRAINS", "taxonomy-structural", "taxonomy-architecture"),
    ]
    result = validate_cross_discipline_graph(concepts, edges)
    assert not any(v.rule == "DISALLOWED_DOMAIN_PAIR" for v in result.violations)


def test_disallowed_domain_pair_warns():
    concepts = [
        _concept("VTN-CON-0001", "taxonomy-structural"),
    ]
    edges = [
        _edge("VTN-CON-0001", "taxonomy-regulatory", "CONSTRAINS", "taxonomy-structural", "taxonomy-regulatory"),
    ]
    result = validate_cross_discipline_graph(concepts, edges)
    assert any(v.rule == "DISALLOWED_DOMAIN_PAIR" and v.severity == "warning" for v in result.violations)


# ---------------------------------------------------------------------------
# Confidence thresholds
# ---------------------------------------------------------------------------

def test_confidence_below_threshold_warns():
    concepts = [_concept("VTN-CON-0001")]
    edges = [
        _edge("VTN-CON-0001", "taxonomy-architecture", "CONSTRAINS", confidence=0.50),
    ]
    result = validate_cross_discipline_graph(concepts, edges)
    assert any(
        v.rule == "CONFIDENCE_TOO_LOW"
        and "0.5" in v.detail
        and "0.9" in v.detail
        and v.severity == "warning"
        for v in result.violations
    )


def test_confidence_at_threshold_passes():
    concepts = [_concept("VTN-CON-0001")]
    edges = [
        _edge("VTN-CON-0001", "taxonomy-architecture", "CONSTRAINS", confidence=0.90),
    ]
    result = validate_cross_discipline_graph(concepts, edges)
    assert not any(v.rule == "CONFIDENCE_TOO_LOW" for v in result.violations)


# ---------------------------------------------------------------------------
# Cycle detection
# ---------------------------------------------------------------------------

def test_cycle_detected():
    concepts = [
        _concept("VTN-CON-0001", "taxonomy-structural"),
        _concept("VTN-CON-0002", "taxonomy-structural"),
        _concept("VTN-CON-0003", "taxonomy-structural"),
    ]
    edges = [
        _edge("VTN-CON-0001", "VTN-CON-0002", "REQUIRES"),
        _edge("VTN-CON-0002", "VTN-CON-0003", "REQUIRES"),
        _edge("VTN-CON-0003", "VTN-CON-0001", "REQUIRES"),  # cycle
    ]
    result = validate_cross_discipline_graph(concepts, edges)
    assert any(v.rule == "CYCLE_DETECTED" for v in result.violations)


def test_acyclic_passes():
    concepts = [
        _concept("VTN-CON-0001", "taxonomy-structural"),
        _concept("VTN-CON-0002", "taxonomy-structural"),
        _concept("VTN-CON-0003", "taxonomy-structural"),
    ]
    edges = [
        _edge("VTN-CON-0001", "VTN-CON-0002", "REQUIRES"),
        _edge("VTN-CON-0002", "VTN-CON-0003", "REQUIRES"),
    ]
    result = validate_cross_discipline_graph(concepts, edges)
    assert not any(v.rule == "CYCLE_DETECTED" for v in result.violations)


# ---------------------------------------------------------------------------
# End-to-end valid graph
# ---------------------------------------------------------------------------

def test_valid_graph_passes():
    """A fully conformant graph should pass with zero errors."""
    concepts = [
        _concept("VTN-CON-0001", "taxonomy-structural"),
        _concept("VTN-CON-0002", "taxonomy-architecture"),
        _concept("VTN-CON-0003", "taxonomy-construction"),
    ]
    edges = [
        _edge("VTN-CON-0001", "taxonomy-structural", "BELONGS_TO_DOMAIN", "taxonomy-structural", "taxonomy-structural", 1.0),
        _edge("VTN-CON-0002", "taxonomy-architecture", "BELONGS_TO_DOMAIN", "taxonomy-architecture", "taxonomy-architecture", 1.0),
        _edge("VTN-CON-0003", "taxonomy-construction", "BELONGS_TO_DOMAIN", "taxonomy-construction", "taxonomy-construction", 1.0),
        _edge("VTN-CON-0001", "VTN-CON-0002", "CONSTRAINS", "taxonomy-structural", "taxonomy-architecture", 0.95),
        _edge("VTN-CON-0001", "VTN-CON-0003", "EXECUTED_IN", "taxonomy-structural", "taxonomy-construction", 0.98),
    ]
    result = validate_cross_discipline_graph(concepts, edges)
    assert result.passed is True
    error_violations = [v for v in result.violations if v.severity == "error"]
    assert len(error_violations) == 0
