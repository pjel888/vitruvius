"""Conformal calibrator — split-conformal prediction sets over label probs (Task F.4)."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Sequence


@dataclass(frozen=True)
class CalibrationItem:
    true_label: str
    model_probs: dict[str, float]


@dataclass(frozen=True)
class ConformalPrediction:
    prediction_set: tuple[str, ...]
    confidence: float
    non_conformity_threshold: float


def _non_conformity(item: CalibrationItem) -> float:
    prob_true = item.model_probs.get(item.true_label, 0.0)
    return 1.0 - prob_true


def fit_calibration_threshold(
    calibration: Sequence[CalibrationItem],
    *,
    alpha: float = 0.05,
) -> float:
    if not calibration:
        raise ValueError("calibration set must be non-empty")
    if not (0.0 < alpha < 1.0):
        raise ValueError(f"alpha must be in (0, 1), got {alpha}")

    scores = sorted(_non_conformity(item) for item in calibration)
    n = len(scores)
    # split-conformal quantile index
    rank = math.ceil((n + 1) * (1 - alpha))
    index = min(max(rank - 1, 0), n - 1)
    return scores[index]


def predict_with_conformal_set(
    model_probs: dict[str, float],
    *,
    threshold: float,
    confidence: float,
) -> ConformalPrediction:
    in_set: list[str] = []
    for label in sorted(model_probs.keys()):
        score = 1.0 - model_probs[label]
        if score <= threshold:
            in_set.append(label)

    return ConformalPrediction(
        prediction_set=tuple(in_set),
        confidence=confidence,
        non_conformity_threshold=threshold,
    )
