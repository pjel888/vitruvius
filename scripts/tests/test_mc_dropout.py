"""Sprint GT Stream GT.5.3 — Monte Carlo dropout epistemic uncertainty."""
from __future__ import annotations

import math

import pytest

from vitruvius.graph.mc_dropout import compute_epistemic_uncertainty


def test_identical_predictions_are_zero_uncertainty() -> None:
    preds = [0.8] * 20
    result = compute_epistemic_uncertainty(preds)
    assert math.isclose(result, 0.0, abs_tol=1e-9)


def test_spread_predictions_are_positive_uncertainty() -> None:
    preds = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    result = compute_epistemic_uncertainty(preds)
    assert result > 0.0


def test_uncertainty_increases_with_spread() -> None:
    tight = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.4, 0.6]
    wide = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.0, 1.0]
    assert compute_epistemic_uncertainty(wide) > compute_epistemic_uncertainty(tight)


def test_empty_predictions_raises() -> None:
    with pytest.raises(ValueError):
        compute_epistemic_uncertainty([])


def test_single_prediction_is_zero_uncertainty() -> None:
    result = compute_epistemic_uncertainty([0.7])
    assert math.isclose(result, 0.0, abs_tol=1e-9)


def test_num_samples_caps_the_input() -> None:
    # num_samples=3 → only the first 3 predictions are considered.
    preds = [0.1, 0.1, 0.1, 0.9, 0.9, 0.9]
    result = compute_epistemic_uncertainty(preds, num_samples=3)
    assert math.isclose(result, 0.0, abs_tol=1e-9)
