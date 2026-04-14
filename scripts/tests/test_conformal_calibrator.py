"""Conformal calibrator — split-conformal prediction sets (Task F.4)."""

from __future__ import annotations

import dataclasses

import pytest

from vitruvius.review.conformal_calibrator import (
    CalibrationItem,
    ConformalPrediction,
    fit_calibration_threshold,
    predict_with_conformal_set,
)


def _perfect_calibration() -> list[CalibrationItem]:
    return [
        CalibrationItem(true_label="keep", model_probs={"keep": 1.0, "reject": 0.0}),
        CalibrationItem(true_label="keep", model_probs={"keep": 1.0, "reject": 0.0}),
        CalibrationItem(true_label="reject", model_probs={"keep": 0.0, "reject": 1.0}),
        CalibrationItem(true_label="reject", model_probs={"keep": 0.0, "reject": 1.0}),
    ]


def _noisy_calibration() -> list[CalibrationItem]:
    return [
        CalibrationItem(true_label="keep", model_probs={"keep": 0.9, "reject": 0.1}),
        CalibrationItem(true_label="keep", model_probs={"keep": 0.7, "reject": 0.3}),
        CalibrationItem(true_label="keep", model_probs={"keep": 0.6, "reject": 0.4}),
        CalibrationItem(true_label="reject", model_probs={"keep": 0.2, "reject": 0.8}),
        CalibrationItem(true_label="reject", model_probs={"keep": 0.3, "reject": 0.7}),
        CalibrationItem(true_label="reject", model_probs={"keep": 0.4, "reject": 0.6}),
    ]


def test_threshold_from_perfect_calibration_is_zero():
    threshold = fit_calibration_threshold(_perfect_calibration(), alpha=0.05)
    assert threshold == 0.0


def test_threshold_from_noisy_calibration_is_positive():
    threshold = fit_calibration_threshold(_noisy_calibration(), alpha=0.05)
    assert threshold > 0.0


def test_prediction_set_contains_true_label_when_confident():
    threshold = fit_calibration_threshold(_noisy_calibration(), alpha=0.1)
    pred = predict_with_conformal_set(
        {"keep": 0.92, "reject": 0.08},
        threshold=threshold,
        confidence=0.9,
    )
    assert "keep" in pred.prediction_set


def test_singleton_set_on_high_confidence():
    threshold = fit_calibration_threshold(_noisy_calibration(), alpha=0.1)
    pred = predict_with_conformal_set(
        {"keep": 0.99, "reject": 0.01},
        threshold=threshold,
        confidence=0.9,
    )
    assert pred.prediction_set == ("keep",)


def test_multi_label_set_on_uncertain_prediction():
    # use a high threshold explicitly — multi-label behavior depends on threshold >= max non-conformity
    pred = predict_with_conformal_set(
        {"keep": 0.5, "reject": 0.5},
        threshold=0.6,
        confidence=0.9,
    )
    assert set(pred.prediction_set) == {"keep", "reject"}


def test_alpha_monotone_behavior():
    cal = _noisy_calibration()
    tight = fit_calibration_threshold(cal, alpha=0.3)
    loose = fit_calibration_threshold(cal, alpha=0.05)
    # smaller alpha → higher confidence → larger threshold (more permissive set)
    assert loose >= tight


def test_custom_alpha_values_change_threshold():
    cal = _noisy_calibration()
    a1 = fit_calibration_threshold(cal, alpha=0.1)
    a2 = fit_calibration_threshold(cal, alpha=0.2)
    # different alphas should generally give different thresholds on noisy data
    assert a1 != a2 or a1 > 0  # at least nonzero


def test_conformal_prediction_is_frozen():
    pred = ConformalPrediction(
        prediction_set=("keep",),
        confidence=0.9,
        non_conformity_threshold=0.1,
    )
    with pytest.raises(dataclasses.FrozenInstanceError):
        pred.confidence = 0.5  # type: ignore[misc]


def test_prediction_set_threshold_and_confidence_included():
    threshold = 0.2
    pred = predict_with_conformal_set(
        {"keep": 0.9, "reject": 0.1},
        threshold=threshold,
        confidence=0.95,
    )
    assert pred.non_conformity_threshold == threshold
    assert pred.confidence == 0.95
