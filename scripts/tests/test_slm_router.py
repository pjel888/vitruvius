"""SLM complexity router — deterministic rules engine for model selection (Task F.2)."""

from __future__ import annotations

import dataclasses

import pytest

from vitruvius.review.slm_router import (
    DEFAULT_MODEL_MAP,
    ComplexitySignals,
    RoutingDecision,
    classify_complexity,
    route,
)


def _base_signals(**overrides) -> ComplexitySignals:
    defaults = dict(
        predicate="governs",
        evidence_char_count=100,
        sentence_count=1,
        has_negation=False,
        crf_confidence=0.9,
        regex_pattern_id="P-G-01",
    )
    defaults.update(overrides)
    return ComplexitySignals(**defaults)


def test_complex_path_long_evidence():
    signals = _base_signals(evidence_char_count=2500)
    assert classify_complexity(signals) == "complex"


def test_complex_path_negation():
    signals = _base_signals(has_negation=True)
    assert classify_complexity(signals) == "complex"


def test_complex_path_many_sentences():
    signals = _base_signals(sentence_count=6)
    assert classify_complexity(signals) == "complex"


def test_medium_path_missing_crf_confidence():
    signals = _base_signals(crf_confidence=None)
    assert classify_complexity(signals) == "medium"


def test_medium_path_low_crf_confidence():
    signals = _base_signals(crf_confidence=0.4)
    assert classify_complexity(signals) == "medium"


def test_medium_path_evidence_over_500_chars():
    signals = _base_signals(evidence_char_count=800, crf_confidence=0.95)
    assert classify_complexity(signals) == "medium"


def test_simple_path_short_high_confidence():
    signals = _base_signals(
        evidence_char_count=80,
        crf_confidence=0.95,
        sentence_count=1,
        has_negation=False,
    )
    assert classify_complexity(signals) == "simple"


def test_route_returns_default_model_for_simple():
    signals = _base_signals()
    decision = route(signals)
    assert decision.level == "simple"
    assert decision.model_name == DEFAULT_MODEL_MAP["simple"]
    assert decision.reason  # non-empty


def test_route_custom_model_map_override():
    signals = _base_signals(evidence_char_count=2500)
    custom = {
        "simple": "fast-model",
        "medium": "mid-model",
        "complex": "heavy-model",
    }
    decision = route(signals, model_map=custom)
    assert decision.level == "complex"
    assert decision.model_name == "heavy-model"


def test_routing_decision_is_frozen():
    decision = RoutingDecision(level="simple", model_name="foo", reason="bar")
    with pytest.raises(dataclasses.FrozenInstanceError):
        decision.level = "complex"  # type: ignore[misc]


def test_default_model_map_contains_all_three_levels():
    assert set(DEFAULT_MODEL_MAP.keys()) == {"simple", "medium", "complex"}


def test_route_reason_is_informative():
    signals = _base_signals(has_negation=True)
    decision = route(signals)
    # reason should mention negation or complexity
    assert "negation" in decision.reason.lower() or "complex" in decision.reason.lower()
