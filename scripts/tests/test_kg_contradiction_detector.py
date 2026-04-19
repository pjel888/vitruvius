"""Tests for ContradictionDetector."""

from __future__ import annotations

import pytest

from vitruvius.kg.contradiction_detector import ContradictionDetector
from vitruvius.kg.enums import EdgeType, InferenceType, ValidationState
from vitruvius.kg.schemas import RelationshipAssertion


def _make_assertion(
    aid: str,
    edge_type: EdgeType,
    from_node: str = "concept-a",
    to_node: str = "concept-b",
    inference: InferenceType = InferenceType.DIRECT_CITATION,
    confidence: float = 0.9,
) -> RelationshipAssertion:
    return RelationshipAssertion(
        id=aid,
        edge_type=edge_type,
        from_node_id=from_node,
        to_node_id=to_node,
        reasoning_summary="Reason",
        inference_type=inference,
        confidence=confidence,
        validation_status=ValidationState.VALIDATED,
        evidence_ids=["span-001"],
    )


class TestOverrideConflict:
    def test_detects_overrides_and_applies_to(self) -> None:
        assertions = [
            _make_assertion("assert-1", EdgeType.OVERRIDES),
            _make_assertion("assert-2", EdgeType.APPLIES_TO),
        ]
        detector = ContradictionDetector()
        issues = detector.detect(assertions)
        assert len(issues) == 1
        assert issues[0].pattern == "override_vs_applies_to"
        assert issues[0].severity == "critical"
        assert "assert-1" in issues[0].assertion_ids
        assert "assert-2" in issues[0].assertion_ids

    def test_no_false_positive_when_only_overrides(self) -> None:
        assertions = [_make_assertion("assert-1", EdgeType.OVERRIDES)]
        detector = ContradictionDetector()
        issues = detector.detect(assertions)
        assert len(issues) == 0


class TestRequirementConflict:
    def test_detects_requires_and_excludes(self) -> None:
        assertions = [
            _make_assertion("assert-1", EdgeType.REQUIRES),
            _make_assertion("assert-2", EdgeType.EXCLUDES),
        ]
        detector = ContradictionDetector()
        issues = detector.detect(assertions)
        assert len(issues) == 1
        assert issues[0].pattern == "requires_vs_excludes"
        assert issues[0].severity == "critical"


class TestInferenceCredibility:
    def test_detects_semantic_shadowing_direct_citation(self) -> None:
        assertions = [
            _make_assertion(
                "assert-direct", EdgeType.RELATED_TO, inference=InferenceType.DIRECT_CITATION, confidence=0.95
            ),
            _make_assertion(
                "assert-semantic", EdgeType.RELATED_TO, inference=InferenceType.SEMANTIC_SIMILARITY, confidence=0.75
            ),
        ]
        detector = ContradictionDetector(min_confidence_delta=0.15)
        issues = detector.detect(assertions)
        assert len(issues) == 1
        assert issues[0].pattern == "semantic_shadows_direct_citation"
        assert issues[0].severity == "warning"

    def test_ignores_small_delta(self) -> None:
        assertions = [
            _make_assertion(
                "assert-direct", EdgeType.RELATED_TO, inference=InferenceType.DIRECT_CITATION, confidence=0.95
            ),
            _make_assertion(
                "assert-semantic", EdgeType.RELATED_TO, inference=InferenceType.SEMANTIC_SIMILARITY, confidence=0.90
            ),
        ]
        detector = ContradictionDetector(min_confidence_delta=0.15)
        issues = detector.detect(assertions)
        assert len(issues) == 0


class TestBidirectionalDependency:
    def test_detects_weak_bidirectional_depends_on(self) -> None:
        assertions = [
            _make_assertion("assert-ab", EdgeType.DEPENDS_ON, from_node="a", to_node="b", confidence=0.7),
            _make_assertion("assert-ba", EdgeType.DEPENDS_ON, from_node="b", to_node="a", confidence=0.6),
        ]
        detector = ContradictionDetector()
        issues = detector.detect(assertions)
        assert len(issues) == 1
        assert issues[0].pattern == "weak_bidirectional_dependency"
        assert issues[0].severity == "warning"

    def test_ignores_strong_bidirectional(self) -> None:
        assertions = [
            _make_assertion("assert-ab", EdgeType.DEPENDS_ON, from_node="a", to_node="b", confidence=0.9),
            _make_assertion("assert-ba", EdgeType.DEPENDS_ON, from_node="b", to_node="a", confidence=0.85),
        ]
        detector = ContradictionDetector()
        issues = detector.detect(assertions)
        assert len(issues) == 0


class TestEmpty:
    def test_no_assertions_returns_empty(self) -> None:
        detector = ContradictionDetector()
        issues = detector.detect([])
        assert issues == []
