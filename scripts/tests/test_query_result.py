"""Phase 9 Task 1 — QueryResult + QueryCitation dataclasses."""

from __future__ import annotations

import dataclasses

import pytest

from vitruvius.query.result import (
    QueryCitation,
    QueryResult,
    compute_aggregate_confidence,
)


def _cite(confidence: float, section_id: str = "sec-1") -> QueryCitation:
    return QueryCitation(
        source_id="law-x",
        source_section_id=section_id,
        evidence_snippet="snippet",
        confidence=confidence,
    )


def test_query_citation_construction() -> None:
    c = _cite(0.9)
    assert c.source_id == "law-x"
    assert c.source_section_id == "sec-1"
    assert c.evidence_snippet == "snippet"
    assert c.confidence == 0.9


def test_query_citation_is_frozen() -> None:
    c = _cite(0.9)
    assert dataclasses.is_dataclass(c)
    with pytest.raises(dataclasses.FrozenInstanceError):
        c.confidence = 0.5  # type: ignore[misc]


def test_query_result_construction_with_citations() -> None:
    cites = (_cite(0.9), _cite(0.8, "sec-2"))
    result = QueryResult(
        question="what governs x?",
        answer_entities=("concept-a",),
        citations=cites,
        aggregate_confidence=0.8,
        has_evidence=True,
        query_function="what_governs",
        arguments={"subject": "concept-x"},
    )
    assert result.answer_entities == ("concept-a",)
    assert len(result.citations) == 2
    assert result.has_evidence is True
    assert result.query_function == "what_governs"


def test_query_result_is_frozen() -> None:
    result = QueryResult(
        question="q",
        answer_entities=(),
        citations=(),
        aggregate_confidence=0.0,
        has_evidence=False,
        query_function="neighbors",
        arguments={},
    )
    assert dataclasses.is_dataclass(result)
    with pytest.raises(dataclasses.FrozenInstanceError):
        result.has_evidence = True  # type: ignore[misc]


def test_query_result_empty_citations_has_no_evidence() -> None:
    result = QueryResult(
        question="q",
        answer_entities=(),
        citations=(),
        aggregate_confidence=0.0,
        has_evidence=False,
        query_function="what_governs",
        arguments={"subject": "concept-x"},
    )
    assert result.has_evidence is False
    assert result.aggregate_confidence == 0.0
    assert result.citations == ()


def test_compute_aggregate_confidence_minimum() -> None:
    cites = (_cite(0.9), _cite(0.4), _cite(0.7))
    assert compute_aggregate_confidence(cites) == 0.4


def test_compute_aggregate_confidence_empty() -> None:
    assert compute_aggregate_confidence(()) == 0.0
