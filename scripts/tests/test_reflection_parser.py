"""Reflection parser — LLM thought-block extraction and hedge detection (Task F.6)."""

from __future__ import annotations

import dataclasses

import pytest

from vitruvius.review.reflection_parser import (
    ReflectionVerdict,
    parse_reflection,
)


def test_block_extraction_basic():
    response = """<thought_process>
The candidate looks solid. Confidence: 0.92
</thought_process>
Final: keep"""
    result = parse_reflection(response)
    assert result.thought_block is not None
    assert "Confidence: 0.92" in result.thought_block


def test_confidence_under_threshold_halts():
    response = """<thought_process>
I am not fully certain. confidence: 0.5
</thought_process>"""
    result = parse_reflection(response, min_confidence_to_promote=0.7)
    assert result.halt_auto_promote is True
    assert result.self_confidence == 0.5


def test_confidence_above_threshold_does_not_halt():
    response = """<thought_process>
This looks clean. confidence: 0.85
</thought_process>"""
    result = parse_reflection(response, min_confidence_to_promote=0.7)
    assert result.halt_auto_promote is False
    assert result.self_confidence == 0.85


def test_hedge_word_detection_single():
    response = """<thought_process>
This might be correct, I think.
</thought_process>"""
    result = parse_reflection(response)
    assert "might" in result.hedge_words_found
    # one hedge word alone does not halt
    assert result.halt_auto_promote is False


def test_multiple_hedge_words_halt():
    response = """<thought_process>
This might possibly be unclear.
</thought_process>"""
    result = parse_reflection(response)
    assert len(result.hedge_words_found) >= 2
    assert result.halt_auto_promote is True


def test_no_thought_block_does_not_halt():
    response = "Just a plain answer."
    result = parse_reflection(response)
    assert result.thought_block is None
    assert result.halt_auto_promote is False
    assert "no thought block" in result.reason.lower()


def test_case_insensitive_block_markers():
    response = """<THOUGHT_PROCESS>
Confidence: 0.9
</THOUGHT_PROCESS>"""
    result = parse_reflection(response)
    assert result.thought_block is not None
    assert result.self_confidence == 0.9


def test_verdict_is_frozen():
    verdict = ReflectionVerdict(
        thought_block=None,
        self_confidence=None,
        hedge_words_found=(),
        halt_auto_promote=False,
        reason="no thought block",
    )
    with pytest.raises(dataclasses.FrozenInstanceError):
        verdict.halt_auto_promote = True  # type: ignore[misc]
