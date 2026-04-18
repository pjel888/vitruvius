"""Tests for ``vitruvius.kg.assertion_validator``."""

from __future__ import annotations

import pytest

from vitruvius.kg.assertion_validator import (
    AssertionValidationResult,
    AssertionValidator,
)
from vitruvius.kg.enums import EdgeType, InferenceType, ValidationState
from vitruvius.kg.schemas import (
    CreatedBy,
    MergeAssertion,
    PlacementAssertion,
    RelationshipAssertion,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _rel(**overrides) -> RelationshipAssertion:
    defaults = {
        "id": "assert-rel-001",
        "edge_type": EdgeType.APPLIES_TO,
        "from_node_id": "concept-fire-resistive-construction",
        "to_node_id": "concept-occupancy-classification",
        "reasoning_summary": "Governs fire resistive requirements per PD 1096.",
        "inference_type": InferenceType.DIRECT_CITATION,
        "confidence": 0.95,
        "evidence_ids": ["span-001"],
    }
    defaults.update(overrides)
    return RelationshipAssertion(**defaults)


def _place(**overrides) -> PlacementAssertion:
    defaults = {
        "id": "assert-placement-001",
        "node_id": "concept-fire-resistive-construction",
        "parent_node_id": "topic-building-codes",
        "reasoning_summary": "Directly under building codes topic.",
        "confidence": 0.92,
        "evidence_ids": ["span-001"],
    }
    defaults.update(overrides)
    return PlacementAssertion(**defaults)


def _merge(**overrides) -> MergeAssertion:
    defaults = {
        "id": "assert-merge-001",
        "from_node_id": "concept-fire-resistive-construction",
        "to_node_id": "concept-fire-resistant-construction",
        "reasoning_summary": "Same concept, different spelling.",
        "confidence": 0.88,
        "evidence_ids": ["span-001"],
    }
    defaults.update(overrides)
    return MergeAssertion(**defaults)


def _make_validator(
    *,
    placement_index: dict[str, str] | None = None,
    merge_index: dict[str, str] | None = None,
    concept_status: str = "candidate",
) -> AssertionValidator:
    canonical_index = {
        "concept-fire-resistive-construction": {
            "type": "concept",
            "status": concept_status,
        },
        "concept-occupancy-classification": {
            "type": "concept",
            "status": concept_status,
        },
        "concept-fire-resistant-construction": {
            "type": "concept",
            "status": concept_status,
        },
        "topic-building-codes": {
            "type": "topic",
            "status": concept_status,
        },
    }
    evidence_index = {
        "span-001": {"id": "span-001"},
    }
    return AssertionValidator(
        canonical_index=canonical_index,
        evidence_index=evidence_index,
        placement_index=placement_index or {},
        merge_index=merge_index or {},
    )


# ---------------------------------------------------------------------------
# RelationshipAssertion — happy path
# ---------------------------------------------------------------------------

def test_relationship_happy_path():
    v = _make_validator()
    assertion = _rel()
    result = v.validate_relationship(assertion)
    assert result.passed
    assert result.errors == []
    assert result.updated_status == ValidationState.VALIDATED
    assert assertion.validation_status == ValidationState.VALIDATED


# ---------------------------------------------------------------------------
# RelationshipAssertion — structural rules
# ---------------------------------------------------------------------------

def test_r3_missing_from_node():
    v = _make_validator()
    result = v.validate_relationship(_rel(from_node_id="concept-missing"))
    assert not result.passed
    assert any("from_node_id" in e for e in result.errors)


def test_r4_missing_to_node():
    v = _make_validator()
    result = v.validate_relationship(_rel(to_node_id="concept-missing"))
    assert not result.passed
    assert any("to_node_id" in e for e in result.errors)


def test_r5_empty_reasoning():
    v = _make_validator()
    assertion = RelationshipAssertion.model_construct(
        id="assert-rel-001",
        edge_type=EdgeType.APPLIES_TO,
        from_node_id="concept-fire-resistive-construction",
        to_node_id="concept-occupancy-classification",
        reasoning_summary="",
        inference_type=InferenceType.DIRECT_CITATION,
        confidence=0.95,
        evidence_ids=["span-001"],
    )
    result = v.validate_relationship(assertion)
    assert not result.passed
    assert any("reasoning_summary" in e for e in result.errors)


def test_r6_confidence_out_of_range():
    v = _make_validator()
    assertion = RelationshipAssertion.model_construct(
        id="assert-rel-001",
        edge_type=EdgeType.APPLIES_TO,
        from_node_id="concept-fire-resistive-construction",
        to_node_id="concept-occupancy-classification",
        reasoning_summary="Valid summary.",
        inference_type=InferenceType.DIRECT_CITATION,
        confidence=1.5,
        evidence_ids=["span-001"],
    )
    result = v.validate_relationship(assertion)
    assert not result.passed
    assert any("confidence" in e for e in result.errors)


def test_r7_unknown_inference_type():
    v = _make_validator()
    assertion = RelationshipAssertion.model_construct(
        id="assert-rel-001",
        edge_type=EdgeType.APPLIES_TO,
        from_node_id="concept-fire-resistive-construction",
        to_node_id="concept-occupancy-classification",
        reasoning_summary="Valid summary.",
        inference_type="bogus",  # type: ignore[arg-type]
        confidence=0.95,
        evidence_ids=["span-001"],
    )
    result = v.validate_relationship(assertion)
    assert not result.passed
    assert any("inference_type" in e for e in result.errors)


def test_r8_empty_evidence():
    v = _make_validator()
    result = v.validate_relationship(_rel(evidence_ids=[]))
    assert not result.passed
    assert any("evidence_ids" in e for e in result.errors)


def test_r9_missing_evidence_span():
    v = _make_validator()
    result = v.validate_relationship(_rel(evidence_ids=["span-missing"]))
    assert not result.passed
    assert any("span-missing" in e for e in result.errors)


def test_r14_rejected_review_state():
    v = _make_validator()
    result = v.validate_relationship(_rel(review_state="rejected"))
    assert not result.passed
    assert any("rejected" in e for e in result.errors)


# ---------------------------------------------------------------------------
# PlacementAssertion
# ---------------------------------------------------------------------------

def test_placement_happy_path():
    v = _make_validator()
    assertion = _place()
    result = v.validate_placement(assertion)
    assert result.passed
    assert assertion.validation_status == ValidationState.VALIDATED


def test_placement_r10_parent_not_taxonomy_container():
    v = _make_validator()
    # Parent is a concept, not a topic/subtopic/taxonomy
    result = v.validate_placement(_place(parent_node_id="concept-occupancy-classification"))
    assert not result.passed
    assert any("R10" in e for e in result.errors)


def test_placement_r11_conflicting_existing():
    v = _make_validator(placement_index={"concept-fire-resistive-construction": "topic-other"})
    result = v.validate_placement(_place())
    assert not result.passed
    assert any("R11" in e for e in result.errors)


# ---------------------------------------------------------------------------
# MergeAssertion
# ---------------------------------------------------------------------------

def test_merge_happy_path():
    v = _make_validator()
    result = v.validate_merge(_merge())
    assert result.passed


def test_merge_r12_type_mismatch():
    v = _make_validator()
    # Change to_node to a topic type (different from from_node concept)
    v2 = AssertionValidator(
        canonical_index={
            "concept-fire-resistive-construction": {"type": "concept"},
            "topic-building-codes": {"type": "topic"},
        },
        evidence_index={"span-001": {"id": "span-001"}},
    )
    result = v2.validate_merge(_merge(to_node_id="topic-building-codes"))
    assert not result.passed
    assert any("R12" in e for e in result.errors)


def test_merge_r13_already_merged():
    v = _make_validator(merge_index={"concept-fire-resistive-construction": "concept-x"})
    result = v.validate_merge(_merge())
    assert not result.passed
    assert any("R13" in e for e in result.errors)


def test_merge_r13_superseded_node():
    v = _make_validator(concept_status="superseded")
    result = v.validate_merge(_merge())
    assert not result.passed
    assert any("R13" in e for e in result.errors)
