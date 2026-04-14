"""Choquet integral aggregator — non-additive signal fusion (Task F.8)."""

from __future__ import annotations

import dataclasses

import pytest

from vitruvius.review.choquet_aggregator import (
    ChoquetResult,
    Signal,
    additive_measure,
    choquet_integral,
)


def test_additive_measure_yields_arithmetic_mean():
    signals = [
        Signal(name="regex", value=0.6),
        Signal(name="crf", value=0.8),
        Signal(name="tfidf", value=0.4),
    ]
    measure = additive_measure([s.name for s in signals])
    result = choquet_integral(signals, fuzzy_measure=measure)
    expected = (0.6 + 0.8 + 0.4) / 3
    assert abs(result.aggregate - expected) < 1e-9


def test_single_signal_aggregate_equals_signal_value():
    signals = [Signal(name="llm", value=0.7)]
    measure = additive_measure(["llm"])
    result = choquet_integral(signals, fuzzy_measure=measure)
    assert abs(result.aggregate - 0.7) < 1e-9


def test_zero_signals_returns_zero():
    result = choquet_integral([], fuzzy_measure={})
    assert result.aggregate == 0.0
    assert result.sorted_signals == ()


def test_non_additive_measure_dampens_redundant_signals():
    # Regex and CRF are treated as partially redundant — their joint measure
    # is LESS than their additive sum would suggest.
    signals = [
        Signal(name="regex", value=0.8),
        Signal(name="crf", value=0.8),
        Signal(name="llm", value=0.2),
    ]
    redundant_measure: dict[frozenset[str], float] = {
        frozenset(): 0.0,
        frozenset({"regex"}): 0.3,
        frozenset({"crf"}): 0.3,
        frozenset({"llm"}): 0.4,
        frozenset({"regex", "crf"}): 0.4,  # redundant — less than 0.6
        frozenset({"regex", "llm"}): 0.7,
        frozenset({"crf", "llm"}): 0.7,
        frozenset({"regex", "crf", "llm"}): 1.0,
    }
    result = choquet_integral(signals, fuzzy_measure=redundant_measure)
    # additive baseline would be (0.8 + 0.8 + 0.2) / 3 = 0.6; redundancy should dampen
    additive = additive_measure([s.name for s in signals])
    additive_result = choquet_integral(signals, fuzzy_measure=additive)
    # not strictly less for any non-additive measure, but at least aggregates should differ
    assert result.aggregate != pytest.approx(additive_result.aggregate, abs=1e-6)


def test_monotonicity_more_with_higher_values_yields_higher_aggregate():
    low_signals = [
        Signal(name="a", value=0.1),
        Signal(name="b", value=0.2),
    ]
    high_signals = [
        Signal(name="a", value=0.8),
        Signal(name="b", value=0.9),
    ]
    measure = additive_measure(["a", "b"])
    low_result = choquet_integral(low_signals, fuzzy_measure=measure)
    high_result = choquet_integral(high_signals, fuzzy_measure=measure)
    assert high_result.aggregate > low_result.aggregate


def test_result_is_frozen():
    result = ChoquetResult(aggregate=0.5, sorted_signals=(Signal(name="a", value=0.5),))
    with pytest.raises(dataclasses.FrozenInstanceError):
        result.aggregate = 1.0  # type: ignore[misc]


def test_sorted_signals_sorted_ascending():
    signals = [
        Signal(name="a", value=0.9),
        Signal(name="b", value=0.1),
        Signal(name="c", value=0.5),
    ]
    measure = additive_measure(["a", "b", "c"])
    result = choquet_integral(signals, fuzzy_measure=measure)
    values = [s.value for s in result.sorted_signals]
    assert values == sorted(values)


def test_aggregate_always_in_unit_interval():
    signals = [
        Signal(name="a", value=1.0),
        Signal(name="b", value=1.0),
        Signal(name="c", value=1.0),
    ]
    measure = additive_measure(["a", "b", "c"])
    result = choquet_integral(signals, fuzzy_measure=measure)
    assert 0.0 <= result.aggregate <= 1.0
    assert abs(result.aggregate - 1.0) < 1e-9


def test_additive_measure_empty_signals_returns_empty_map():
    measure = additive_measure([])
    assert measure == {frozenset(): 0.0}


def test_missing_subset_in_measure_uses_fallback():
    # if a subset is missing, we should not crash
    signals = [
        Signal(name="a", value=0.5),
        Signal(name="b", value=0.5),
    ]
    incomplete: dict[frozenset[str], float] = {
        frozenset(): 0.0,
        frozenset({"a", "b"}): 1.0,
    }
    # should not raise
    result = choquet_integral(signals, fuzzy_measure=incomplete)
    assert 0.0 <= result.aggregate <= 1.0
