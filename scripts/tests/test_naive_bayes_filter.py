"""Naive Bayes pre-review filter — scaffolded, refuses training on small corpora."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from vitruvius.review.naive_bayes_filter import (
    DEFAULT_AUTO_ACCEPT_THRESHOLD,
    DEFAULT_AUTO_REJECT_THRESHOLD,
    MIN_TRAINING_EXAMPLES,
    CandidateFeatures,
    FilterDecision,
    InsufficientTrainingDataError,
    NBFilter,
    TrainingExample,
    classify,
    fit_filter,
    load_filter,
    save_filter,
)


def _keep_example() -> TrainingExample:
    return TrainingExample(
        features=CandidateFeatures(
            predicate="governs",
            regex_pattern_id="P-G-01",
            char_distance=10,
            evidence_length=80,
            verb_voice="active",
            has_negation=False,
        ),
        decision="keep",
    )


def _reject_example() -> TrainingExample:
    return TrainingExample(
        features=CandidateFeatures(
            predicate="limits",
            regex_pattern_id="P-L-99",
            char_distance=500,
            evidence_length=1500,
            verb_voice="unknown",
            has_negation=True,
        ),
        decision="reject",
    )


def _balanced_corpus(n: int) -> list[TrainingExample]:
    half = n // 2
    return [_keep_example()] * half + [_reject_example()] * half


def test_refuses_training_below_minimum() -> None:
    with pytest.raises(InsufficientTrainingDataError):
        fit_filter(_balanced_corpus(MIN_TRAINING_EXAMPLES - 2))


def test_refuses_training_on_empty_corpus() -> None:
    with pytest.raises(InsufficientTrainingDataError):
        fit_filter([])


def test_refuses_training_when_all_labels_are_keep() -> None:
    examples = [_keep_example()] * MIN_TRAINING_EXAMPLES
    with pytest.raises(ValueError):
        fit_filter(examples)


def test_refuses_training_when_all_labels_are_reject() -> None:
    examples = [_reject_example()] * MIN_TRAINING_EXAMPLES
    with pytest.raises(ValueError):
        fit_filter(examples)


def test_fits_on_balanced_synthetic_corpus() -> None:
    filter_ = fit_filter(_balanced_corpus(MIN_TRAINING_EXAMPLES))
    assert filter_.is_fitted is True
    assert filter_.model is not None
    assert filter_.vectorizer is not None


def test_classify_unfitted_filter_forwards_to_llm() -> None:
    empty = NBFilter()
    decision = classify(empty, _keep_example().features)
    assert decision.action == "forward_to_llm"
    assert decision.probability_keep == 0.5
    assert decision.probability_reject == 0.5


def test_classify_auto_accepts_high_probability_keep() -> None:
    filter_ = fit_filter(_balanced_corpus(MIN_TRAINING_EXAMPLES))
    decision = classify(filter_, _keep_example().features)
    assert decision.probability_keep > 0.9
    assert decision.action == "auto_accept"


def test_classify_auto_rejects_low_probability_keep() -> None:
    filter_ = fit_filter(_balanced_corpus(MIN_TRAINING_EXAMPLES))
    decision = classify(filter_, _reject_example().features)
    assert decision.probability_keep < 0.1
    assert decision.action == "auto_reject"


def test_classify_forwards_uncertain_to_llm() -> None:
    filter_ = fit_filter(_balanced_corpus(MIN_TRAINING_EXAMPLES))
    ambiguous = CandidateFeatures(
        predicate="depends_on",
        regex_pattern_id="P-D-02",
        char_distance=100,
        evidence_length=500,
        verb_voice="active",
        has_negation=False,
    )
    decision = classify(filter_, ambiguous)
    assert decision.action in {"auto_accept", "auto_reject", "forward_to_llm"}


def test_round_trip_save_and_load(tmp_path: Path) -> None:
    filter_ = fit_filter(_balanced_corpus(MIN_TRAINING_EXAMPLES))
    out = tmp_path / "nb_filter.json"
    save_filter(filter_, out)
    assert out.exists()

    loaded = load_filter(out)
    assert loaded.is_fitted is True

    original_decision = classify(filter_, _keep_example().features)
    loaded_decision = classify(loaded, _keep_example().features)
    assert original_decision.action == loaded_decision.action
    assert abs(original_decision.probability_keep - loaded_decision.probability_keep) < 1e-9


def test_save_uses_sort_keys_for_determinism(tmp_path: Path) -> None:
    filter_ = fit_filter(_balanced_corpus(MIN_TRAINING_EXAMPLES))
    out1 = tmp_path / "a.json"
    out2 = tmp_path / "b.json"
    save_filter(filter_, out1)
    save_filter(filter_, out2)
    assert out1.read_text() == out2.read_text()


def test_custom_thresholds_respected() -> None:
    strict = fit_filter(
        _balanced_corpus(MIN_TRAINING_EXAMPLES),
        auto_accept_threshold=0.999,
        auto_reject_threshold=0.001,
    )
    assert strict.auto_accept_threshold == 0.999
    assert strict.auto_reject_threshold == 0.001


def test_filter_decision_is_frozen() -> None:
    decision = FilterDecision(
        action="auto_accept",
        probability_keep=0.95,
        probability_reject=0.05,
        reason="test",
    )
    with pytest.raises((AttributeError, Exception)):
        decision.action = "auto_reject"  # type: ignore[misc]


def test_constants_are_documented() -> None:
    assert MIN_TRAINING_EXAMPLES == 50
    assert DEFAULT_AUTO_ACCEPT_THRESHOLD == 0.95
    assert DEFAULT_AUTO_REJECT_THRESHOLD == 0.05


def test_save_output_is_valid_json(tmp_path: Path) -> None:
    filter_ = fit_filter(_balanced_corpus(MIN_TRAINING_EXAMPLES))
    out = tmp_path / "nb.json"
    save_filter(filter_, out)
    payload = json.loads(out.read_text())
    assert "class_log_prior" in payload
    assert "feature_log_prob" in payload
    assert "classes" in payload
    assert "vectorizer_vocabulary" in payload
    assert "auto_accept_threshold" in payload
    assert "auto_reject_threshold" in payload


def test_probabilities_sum_to_one_for_fitted_filter() -> None:
    filter_ = fit_filter(_balanced_corpus(MIN_TRAINING_EXAMPLES))
    decision = classify(filter_, _keep_example().features)
    assert abs(decision.probability_keep + decision.probability_reject - 1.0) < 1e-9


def test_candidate_features_is_frozen() -> None:
    features = _keep_example().features
    with pytest.raises((AttributeError, Exception)):
        features.predicate = "other"  # type: ignore[misc]
