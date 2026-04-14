"""Bayesian evidence fusion — log-odds aggregation of multi-source signals."""

from __future__ import annotations

import math

import pytest

from vitruvius.promotion.bayesian_fusion import (
    DEFAULT_BAYES_FACTORS,
    DEFAULT_PRIOR,
    EvidenceSignal,
    FusionResult,
    fuse_evidence,
)


def _logit(p: float) -> float:
    return math.log(p / (1 - p))


def _sigmoid_value(x: float) -> float:
    if x >= 0:
        return 1.0 / (1.0 + math.exp(-x))
    return math.exp(x) / (1.0 + math.exp(x))


def test_no_signals_returns_prior() -> None:
    result = fuse_evidence([])
    assert result.prior == DEFAULT_PRIOR
    assert math.isclose(result.posterior, DEFAULT_PRIOR, abs_tol=1e-9)
    assert result.applied_signals == ()


def test_single_regex_match_updates_log_odds_correctly() -> None:
    result = fuse_evidence([EvidenceSignal("regex_match", observed=True)])
    expected_log_odds = math.log(0.1 / 0.9) + math.log(6.0)
    assert math.isclose(result.log_odds, expected_log_odds, abs_tol=1e-9)
    expected_posterior = _sigmoid_value(expected_log_odds)
    assert math.isclose(result.posterior, expected_posterior, abs_tol=1e-9)


def test_fired_signals_are_tracked() -> None:
    result = fuse_evidence([
        EvidenceSignal("regex_match", observed=True),
        EvidenceSignal("tfidf_match", observed=False),
        EvidenceSignal("crf_tag", observed=True),
    ])
    assert set(result.applied_signals) == {"regex_match", "crf_tag"}


def test_false_signal_does_not_change_posterior() -> None:
    a = fuse_evidence([EvidenceSignal("regex_match", observed=True)])
    b = fuse_evidence([
        EvidenceSignal("regex_match", observed=True),
        EvidenceSignal("tfidf_match", observed=False),
    ])
    assert math.isclose(a.posterior, b.posterior, abs_tol=1e-9)


def test_adding_positive_signal_does_not_decrease_posterior() -> None:
    base = fuse_evidence([EvidenceSignal("regex_match", observed=True)])
    stacked = fuse_evidence([
        EvidenceSignal("regex_match", observed=True),
        EvidenceSignal("tfidf_match", observed=True),
        EvidenceSignal("crf_tag", observed=True),
        EvidenceSignal("llm_agreement", observed=True),
    ])
    assert stacked.posterior >= base.posterior


def test_order_invariance() -> None:
    signals = [
        EvidenceSignal("regex_match", observed=True),
        EvidenceSignal("tfidf_match", observed=True),
        EvidenceSignal("crf_tag", observed=True),
    ]
    a = fuse_evidence(signals)
    b = fuse_evidence(list(reversed(signals)))
    assert math.isclose(a.posterior, b.posterior, abs_tol=1e-12)


def test_custom_bayes_factor_override() -> None:
    result = fuse_evidence([
        EvidenceSignal("regex_match", observed=True, bayes_factor=100.0),
    ])
    assert result.posterior > 0.9


def test_custom_prior() -> None:
    result = fuse_evidence([], prior=0.5)
    assert math.isclose(result.posterior, 0.5, abs_tol=1e-9)


def test_custom_prior_propagates_through_signals() -> None:
    result = fuse_evidence(
        [EvidenceSignal("regex_match", observed=True)],
        prior=0.5,
    )
    expected = _sigmoid_value(_logit(0.5) + math.log(6.0))
    assert math.isclose(result.posterior, expected, abs_tol=1e-9)


def test_unknown_source_without_override_raises() -> None:
    with pytest.raises(KeyError, match="unknown_source"):
        fuse_evidence([EvidenceSignal("unknown_source", observed=True)])


def test_unknown_source_with_override_works() -> None:
    result = fuse_evidence([
        EvidenceSignal("unknown_source", observed=True, bayes_factor=2.0),
    ])
    expected = _sigmoid_value(_logit(0.1) + math.log(2.0))
    assert math.isclose(result.posterior, expected, abs_tol=1e-9)


def test_unknown_source_not_observed_is_ignored() -> None:
    result = fuse_evidence([
        EvidenceSignal("some_weird_source", observed=False),
    ])
    assert math.isclose(result.posterior, DEFAULT_PRIOR, abs_tol=1e-9)
    assert result.applied_signals == ()


def test_posterior_in_unit_interval_for_extreme_stacks() -> None:
    many = [EvidenceSignal("regex_match", observed=True)] * 20
    result = fuse_evidence(many)
    assert 0 <= result.posterior <= 1
    assert result.posterior > 0.999


def test_fusion_result_is_frozen() -> None:
    result = fuse_evidence([])
    with pytest.raises((AttributeError, Exception)):
        result.posterior = 0.5  # type: ignore[misc]


def test_evidence_signal_is_frozen() -> None:
    sig = EvidenceSignal("regex_match", observed=True)
    with pytest.raises((AttributeError, Exception)):
        sig.observed = False  # type: ignore[misc]


def test_default_constants_documented() -> None:
    assert DEFAULT_PRIOR == 0.10
    assert "regex_match" in DEFAULT_BAYES_FACTORS
    assert DEFAULT_BAYES_FACTORS["regex_match"] == 6.0
    assert DEFAULT_BAYES_FACTORS["tfidf_match"] == 1.4
    assert DEFAULT_BAYES_FACTORS["crf_tag"] == 1.1
    assert DEFAULT_BAYES_FACTORS["llm_agreement"] == 1.06


def test_custom_bayes_factors_dict() -> None:
    custom = {"my_source": 10.0}
    result = fuse_evidence(
        [EvidenceSignal("my_source", observed=True)],
        bayes_factors=custom,
    )
    expected = _sigmoid_value(_logit(0.1) + math.log(10.0))
    assert math.isclose(result.posterior, expected, abs_tol=1e-9)


def test_per_signal_override_beats_source_default() -> None:
    default_result = fuse_evidence([
        EvidenceSignal("regex_match", observed=True),
    ])
    overridden = fuse_evidence([
        EvidenceSignal("regex_match", observed=True, bayes_factor=1.5),
    ])
    assert overridden.posterior < default_result.posterior


def test_fusion_result_type() -> None:
    result = fuse_evidence([EvidenceSignal("regex_match", observed=True)])
    assert isinstance(result, FusionResult)
    assert isinstance(result.prior, float)
    assert isinstance(result.posterior, float)
    assert isinstance(result.log_odds, float)
    assert isinstance(result.applied_signals, tuple)


def test_applied_signals_preserves_input_order() -> None:
    result = fuse_evidence([
        EvidenceSignal("crf_tag", observed=True),
        EvidenceSignal("regex_match", observed=True),
        EvidenceSignal("tfidf_match", observed=True),
    ])
    assert result.applied_signals == ("crf_tag", "regex_match", "tfidf_match")
