"""Stream I.4 — HMM pipeline observability."""

from __future__ import annotations

import dataclasses

import pytest

from vitruvius.query.pipeline_hmm import (
    HMMModel,
    PIPELINE_STATES,
    fit_hmm_from_registry,
    predict_next_state,
)


def _history_basic() -> list[tuple[str, str]]:
    return [
        ("scanned", "converted"),
        ("scanned", "converted"),
        ("scanned", "errored"),
        ("converted", "refined"),
        ("refined", "canonicalized"),
        ("canonicalized", "extracted"),
        ("extracted", "reviewed"),
        ("reviewed", "promoted"),
    ]


def test_fit_counts_transitions_and_normalises_rows() -> None:
    model = fit_hmm_from_registry(_history_basic())
    assert model.states == PIPELINE_STATES
    assert len(model.transition_matrix) == len(PIPELINE_STATES)
    for row in model.transition_matrix:
        assert abs(sum(row) - 1.0) < 1e-9


def test_scanned_row_reflects_observed_frequencies() -> None:
    model = fit_hmm_from_registry(_history_basic())
    dist = predict_next_state(model, "scanned")
    # scanned -> converted twice, scanned -> errored once.
    assert abs(dist["converted"] - (2.0 / 3.0)) < 1e-9
    assert abs(dist["errored"] - (1.0 / 3.0)) < 1e-9
    assert dist["refined"] == 0.0


def test_zero_outgoing_state_uses_uniform_recovery() -> None:
    # "errored" never has outgoing transitions in this history.
    model = fit_hmm_from_registry(_history_basic())
    dist = predict_next_state(model, "errored")
    expected = 1.0 / len(PIPELINE_STATES)
    for state in PIPELINE_STATES:
        assert abs(dist[state] - expected) < 1e-9


def test_unknown_state_raises() -> None:
    model = fit_hmm_from_registry(_history_basic())
    with pytest.raises(KeyError):
        predict_next_state(model, "banana")


def test_hmm_is_deterministic() -> None:
    model_a = fit_hmm_from_registry(_history_basic())
    model_b = fit_hmm_from_registry(_history_basic())
    assert model_a.transition_matrix == model_b.transition_matrix
    assert model_a.states == model_b.states


def test_hmm_is_frozen() -> None:
    model = fit_hmm_from_registry([])
    assert dataclasses.is_dataclass(model)
    with pytest.raises(dataclasses.FrozenInstanceError):
        model.states = ()  # type: ignore[misc]


def test_unknown_states_in_history_ignored() -> None:
    history = [
        ("scanned", "converted"),
        ("unknown", "converted"),  # unknown from
        ("scanned", "voodoo"),     # unknown to
    ]
    model = fit_hmm_from_registry(history)
    dist = predict_next_state(model, "scanned")
    assert dist["converted"] == 1.0
    # Ensure no stray keys.
    assert set(dist.keys()) == set(PIPELINE_STATES)


def test_empty_history_all_uniform() -> None:
    model = fit_hmm_from_registry([])
    for state in PIPELINE_STATES:
        dist = predict_next_state(model, state)
        expected = 1.0 / len(PIPELINE_STATES)
        for s in PIPELINE_STATES:
            assert abs(dist[s] - expected) < 1e-9
