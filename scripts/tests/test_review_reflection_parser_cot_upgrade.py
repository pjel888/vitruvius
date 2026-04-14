"""Stream Y3.1 — strict CoT parser tests."""
from __future__ import annotations

import pytest

from vitruvius.review.reflection_parser import parse_cot_strict, CotParseError


def test_valid_cot_parses_cleanly() -> None:
    raw = (
        "<think>\n"
        "Step 1: Read the rule. Evidence: 'Section 701: the setback must be at least 3 meters'.\n"
        "Step 2: The candidate predicate 'has_setback' aligns with the rule.\n"
        "Self-confidence: 0.92\n"
        "</think>\n"
        "VERDICT: keep"
    )
    result = parse_cot_strict(raw)
    assert result.verdict == "keep"
    assert result.self_confidence == pytest.approx(0.92)
    assert "Section 701" in result.evidence_citation
    assert len(result.reasoning_steps) == 2


def test_missing_think_block_raises() -> None:
    raw = "VERDICT: keep"
    with pytest.raises(CotParseError, match="no <think> block"):
        parse_cot_strict(raw)


def test_missing_verdict_raises() -> None:
    raw = "<think>step 1: 'cite' here. Self-confidence: 0.8</think>"
    with pytest.raises(CotParseError, match="no VERDICT line"):
        parse_cot_strict(raw)


def test_missing_evidence_citation_raises() -> None:
    raw = "<think>Step 1: I think so. Self-confidence: 0.8</think>\nVERDICT: keep"
    with pytest.raises(CotParseError, match="no evidence citation"):
        parse_cot_strict(raw)


def test_low_self_confidence_flags_escalate() -> None:
    raw = (
        "<think>Step 1: Evidence: 'quoted phrase'. Self-confidence: 0.40</think>\n"
        "VERDICT: keep"
    )
    result = parse_cot_strict(raw, escalate_below=0.70)
    assert result.verdict == "keep"
    assert result.escalate is True
