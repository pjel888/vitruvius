"""Phase 9 Task 5 — human-readable result renderer."""

from __future__ import annotations

from vitruvius.query.cli_formatter import render_query_result
from vitruvius.query.result import QueryCitation, QueryResult


def _cite(
    *,
    source: str = "law-pd-1096",
    section: str = "sec-301",
    snippet: str = "No person shall erect any building without a permit.",
    confidence: float = 0.92,
) -> QueryCitation:
    return QueryCitation(
        source_id=source,
        source_section_id=section,
        evidence_snippet=snippet,
        confidence=confidence,
        source_title=None,
    )


def test_render_happy_path_contains_all_sections() -> None:
    result = QueryResult(
        question="What governs building permits?",
        answer_entities=("law-pd-1096",),
        answer_display_entities=("PD 1096 - National Building Code",),
        citations=(_cite(source='law-pd-1096'),),
        aggregate_confidence=0.92,
        has_evidence=True,
        query_function="what_governs",
        arguments={"subject": "concept-building-permit"},
    )
    output = render_query_result(result)
    assert "Question: What governs building permits?" in output
    assert "Answer: PD 1096 - National Building Code" in output
    assert "Confidence: 0.92" in output
    assert "Supporting Evidence:" in output
    assert "[1] law-pd-1096 sec-301" in output
    assert "function: what_governs" in output
    assert "arguments: {subject=concept-building-permit}" in output


def test_render_no_evidence_path() -> None:
    result = QueryResult(
        question="What governs nothing?",
        answer_entities=(),
        answer_display_entities=None,
        citations=(),
        aggregate_confidence=0.0,
        has_evidence=False,
        query_function="what_governs",
        arguments={"subject": "concept-nothing"},
    )
    output = render_query_result(result)
    assert "No supporting evidence found" in output
    assert "Confidence: 0.00" in output
    # No "Supporting Evidence:" section when empty.
    assert "Supporting Evidence:" not in output


def test_render_multi_citation_preserves_order() -> None:
    citations = (
        _cite(source="law-a", section="sec-1", snippet="First"),
        _cite(source="law-b", section="sec-2", snippet="Second"),
        _cite(source="law-c", section="sec-3", snippet="Third"),
    )
    result = QueryResult(
        question="q",
        answer_entities=("law-a", "law-b", "law-c"),
        answer_display_entities=None,
        citations=citations,
        aggregate_confidence=0.92,
        has_evidence=True,
        query_function="what_governs",
        arguments={"subject": "concept-x"},
    )
    output = render_query_result(result)
    idx_a = output.find("[1] law-a")
    idx_b = output.find("[2] law-b")
    idx_c = output.find("[3] law-c")
    assert 0 < idx_a < idx_b < idx_c


def test_render_is_deterministic() -> None:
    result = QueryResult(
        question="q",
        answer_entities=("law-a",),
        answer_display_entities=None,
        citations=(_cite(),),
        aggregate_confidence=0.9,
        has_evidence=True,
        query_function="what_governs",
        arguments={"subject": "concept-x"},
    )
    a = render_query_result(result)
    b = render_query_result(result)
    assert a == b
    # Byte-identical over repeated calls.
    assert a.encode("utf-8") == b.encode("utf-8")


def test_render_escapes_newlines_in_question_and_snippet() -> None:
    result = QueryResult(
        question="line1\nline2",
        answer_entities=("law-a",),
        answer_display_entities=None,
        citations=(_cite(snippet="snip\r\nwith\nbreaks"),),
        aggregate_confidence=0.5,
        has_evidence=True,
        query_function="what_governs",
        arguments={"subject": "concept-x"},
    )
    output = render_query_result(result)
    # No raw newlines should appear inside the question/snippet field — we
    # check that the word "line2" and the follow-up are on the SAME line
    # as "line1".
    question_line = next(line for line in output.splitlines() if line.startswith("Question:"))
    assert "line1" in question_line and "line2" in question_line
    # Confirm the snippet line does not split mid-quote.
    snippet_lines = [ln for ln in output.splitlines() if "snip" in ln]
    assert len(snippet_lines) == 1


def test_render_uses_source_title_when_present() -> None:
    result = QueryResult(
        question="q",
        answer_entities=("law-a",),
        answer_display_entities=("Law A",),
        citations=(QueryCitation(source_id="law-a", source_section_id="sec-1", evidence_snippet="snippet", confidence=0.9, source_title="Law A"),),
        aggregate_confidence=0.9,
        has_evidence=True,
        query_function="what_governs",
        arguments={"subject": "concept-x"},
    )
    output = render_query_result(result)
    assert "Answer: Law A" in output
    assert "[1] Law A [law-a] sec-1" in output
