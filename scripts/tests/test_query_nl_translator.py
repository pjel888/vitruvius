"""Phase 9 Task 4 — baseline NL-to-structured translator."""

from __future__ import annotations

import json

from vitruvius.query.nl_translator import (
    ALLOWED_FUNCTIONS,
    TranslationResult,
    build_llm_prompt,
    translate_question,
)


KNOWN = ("concept-building-permit", "concept-occupancy-classification",
         "concept-fire-resistive-construction", "law-pd-1096",
         "law-ra-9514")


def test_regex_governs() -> None:
    result = translate_question(
        "What governs building permit?",
        known_entities=KNOWN,
    )
    assert result.function == "what_governs"
    assert result.arguments == {"subject": "concept-building-permit"}
    assert result.confidence >= 0.5


def test_regex_requires() -> None:
    result = translate_question(
        "What does building permit require?",
        known_entities=KNOWN,
    )
    assert result.function == "what_requires"
    assert result.arguments["subject"] == "concept-building-permit"


def test_regex_limits() -> None:
    result = translate_question(
        "Which sections limit occupancy classification?",
        known_entities=KNOWN,
    )
    assert result.function == "what_limits"
    assert result.arguments["subject"] == "concept-occupancy-classification"


def test_regex_defines() -> None:
    result = translate_question(
        "What defines fire resistive construction?",
        known_entities=KNOWN,
    )
    assert result.function == "what_defines"
    assert result.arguments["subject"] == "concept-fire-resistive-construction"


def test_regex_depends_on() -> None:
    result = translate_question(
        "What does building permit depend on?",
        known_entities=KNOWN,
    )
    assert result.function == "what_depends_on"


def test_regex_affects() -> None:
    result = translate_question(
        "What affects occupancy classification?",
        known_entities=KNOWN,
    )
    assert result.function == "what_affects"


def test_unknown_question_falls_back_to_neighbors() -> None:
    result = translate_question(
        "Tell me a joke about buildings",
        known_entities=KNOWN,
    )
    assert result.function == "neighbors"
    assert result.confidence < 0.5


def test_empty_known_entities_still_produces_function() -> None:
    result = translate_question(
        "What governs something?",
        known_entities=(),
    )
    assert result.function == "what_governs"
    # No subject could be matched.
    assert "subject" not in result.arguments


def test_llm_caller_happy_path_returns_structured() -> None:
    def fake(_prompt: str) -> str:
        return json.dumps({
            "function": "what_governs",
            "arguments": {"subject": "concept-building-permit"},
            "confidence": 0.92,
        })

    result = translate_question(
        "Anything you want",
        known_entities=KNOWN,
        llm_caller=fake,
    )
    assert result.function == "what_governs"
    assert result.arguments == {"subject": "concept-building-permit"}
    assert result.confidence == 0.92


def test_llm_caller_malformed_response_falls_back_to_regex() -> None:
    def fake(_prompt: str) -> str:
        return "not-json"

    result = translate_question(
        "What governs building permit?",
        known_entities=KNOWN,
        llm_caller=fake,
    )
    # Falls back to regex which should succeed.
    assert result.function == "what_governs"


def test_llm_caller_unknown_function_falls_back() -> None:
    def fake(_prompt: str) -> str:
        return json.dumps({
            "function": "not_a_real_function",
            "arguments": {"subject": "concept-x"},
            "confidence": 0.99,
        })

    result = translate_question(
        "What governs building permit?",
        known_entities=KNOWN,
        llm_caller=fake,
    )
    assert result.function == "what_governs"


def test_build_llm_prompt_caps_entities() -> None:
    big = tuple(f"concept-{i}" for i in range(500))
    prompt = build_llm_prompt("What governs x?", big)
    payload = json.loads(prompt)
    assert len(payload["known_entities"]) == 100
    assert payload["allowed_functions"] == list(ALLOWED_FUNCTIONS)


def test_translation_result_is_frozen_dataclass() -> None:
    tr = TranslationResult(
        function="what_governs",
        arguments={"subject": "x"},
        confidence=0.8,
    )
    import dataclasses
    assert dataclasses.is_dataclass(tr)
    import pytest
    with pytest.raises(dataclasses.FrozenInstanceError):
        tr.function = "neighbors"  # type: ignore[misc]
