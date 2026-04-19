"""Tests for ExtractionValidator."""

from __future__ import annotations

import pytest

from vitruvius.kg.extraction_validator import ExtractionValidator
from vitruvius.kg.schemas import ExtractionResult, KnowledgeUnitCandidate


def _make_candidate(**overrides: Any) -> KnowledgeUnitCandidate:
    defaults = {
        "id": "cand-test-001",
        "unit_type": "concept",
        "label": "Building Permit",
        "text": "A building permit is required for construction.",
        "span_ids": ["span-001"],
        "chunk_id": "chk-001",
        "confidence": 0.9,
        "extraction_run_id": "run-001",
    }
    defaults.update(overrides)
    return KnowledgeUnitCandidate(**defaults)


class TestValidCandidate:
    def test_valid_candidate_passes(self) -> None:
        v = ExtractionValidator()
        cand = _make_candidate()
        result = v.validate_candidate(cand)
        assert result.passed is True
        assert result.errors == []


class TestUnitType:
    def test_invalid_unit_type_fails(self) -> None:
        v = ExtractionValidator()
        # Bypass Pydantic validation to test the validator logic
        cand = KnowledgeUnitCandidate.model_construct(
            id="cand-test",
            unit_type="invalid",
            label="Test",
            text="Text",
            span_ids=["span-001"],
            chunk_id="chk-001",
            confidence=0.9,
            extraction_run_id="run-001",
        )
        result = v.validate_candidate(cand)
        assert result.passed is False
        assert any("E1" in e for e in result.errors)

    def test_allowed_unit_types_pass(self) -> None:
        v = ExtractionValidator()
        for ut in ("concept", "definition", "rule", "procedure", "exception"):
            cand = _make_candidate(unit_type=ut)
            result = v.validate_candidate(cand)
            assert result.passed is True, f"unit_type={ut} should pass"


class TestLabel:
    def test_empty_label_fails(self) -> None:
        v = ExtractionValidator()
        cand = _make_candidate(label="  ")
        result = v.validate_candidate(cand)
        assert any("E2" in e for e in result.errors)

    def test_long_label_fails(self) -> None:
        v = ExtractionValidator()
        cand = _make_candidate(label="x" * 201)
        result = v.validate_candidate(cand)
        assert any("E2" in e for e in result.errors)

    def test_generic_filler_fails(self) -> None:
        v = ExtractionValidator()
        for filler in ("undefined", "N/A", "None", "NULL", "unknown"):
            cand = _make_candidate(label=filler)
            result = v.validate_candidate(cand)
            assert any("E7" in e for e in result.errors), f"filler '{filler}' should fail"


class TestText:
    def test_empty_text_fails(self) -> None:
        v = ExtractionValidator()
        cand = _make_candidate(text="  ")
        result = v.validate_candidate(cand)
        assert any("E3" in e for e in result.errors)

    def test_long_text_fails(self) -> None:
        v = ExtractionValidator()
        cand = _make_candidate(text="x" * 4097)
        result = v.validate_candidate(cand)
        assert any("E3" in e for e in result.errors)

    def test_text_same_as_label_fails(self) -> None:
        v = ExtractionValidator()
        cand = _make_candidate(label="Same", text="Same")
        result = v.validate_candidate(cand)
        assert any("E8" in e for e in result.errors)


class TestConfidence:
    def test_negative_confidence_fails(self) -> None:
        v = ExtractionValidator()
        cand = KnowledgeUnitCandidate.model_construct(
            id="cand-test", unit_type="concept", label="Test", text="Text",
            span_ids=["span-001"], chunk_id="chk-001", confidence=-0.1,
            extraction_run_id="run-001",
        )
        result = v.validate_candidate(cand)
        assert any("E4" in e for e in result.errors)

    def test_over_one_confidence_fails(self) -> None:
        v = ExtractionValidator()
        cand = KnowledgeUnitCandidate.model_construct(
            id="cand-test", unit_type="concept", label="Test", text="Text",
            span_ids=["span-001"], chunk_id="chk-001", confidence=1.1,
            extraction_run_id="run-001",
        )
        result = v.validate_candidate(cand)
        assert any("E4" in e for e in result.errors)

    def test_below_minimum_fails(self) -> None:
        v = ExtractionValidator(min_confidence=0.5)
        cand = _make_candidate(confidence=0.3)
        result = v.validate_candidate(cand)
        assert any("E4" in e for e in result.errors)


class TestTraceability:
    def test_empty_span_ids_fails(self) -> None:
        v = ExtractionValidator()
        cand = _make_candidate(span_ids=[])
        result = v.validate_candidate(cand)
        assert any("E5" in e for e in result.errors)

    def test_empty_chunk_id_fails(self) -> None:
        v = ExtractionValidator()
        cand = _make_candidate(chunk_id="")
        result = v.validate_candidate(cand)
        assert any("E6" in e for e in result.errors)

    def test_empty_run_id_fails(self) -> None:
        v = ExtractionValidator()
        cand = _make_candidate(extraction_run_id="")
        result = v.validate_candidate(cand)
        assert any("E9" in e for e in result.errors)


class TestResultValidation:
    def test_validate_result_returns_one_per_candidate(self) -> None:
        v = ExtractionValidator()
        bad_cand = KnowledgeUnitCandidate.model_construct(
            id="cand-bad", unit_type="concept", label="", text="Text",
            span_ids=["span-001"], chunk_id="chk-001", confidence=0.9,
            extraction_run_id="run-001",
        )
        result = ExtractionResult(
            unit_type="concept",
            candidates=[_make_candidate(), bad_cand],
            chunk_id="chk-001",
        )
        results = v.validate_result(result)
        assert len(results) == 2
        assert results[0].passed is True
        assert results[1].passed is False


class TestFilterValid:
    def test_filter_valid_returns_only_passing(self) -> None:
        v = ExtractionValidator()
        bad_cand = KnowledgeUnitCandidate.model_construct(
            id="cand-2", unit_type="concept", label="", text="Text",
            span_ids=["span-001"], chunk_id="chk-001", confidence=0.9,
            extraction_run_id="run-001",
        )
        cands = [
            _make_candidate(id="cand-1"),
            bad_cand,
            _make_candidate(id="cand-3"),
        ]
        valid = v.filter_valid(cands)
        assert len(valid) == 2
        assert {c.id for c in valid} == {"cand-1", "cand-3"}
