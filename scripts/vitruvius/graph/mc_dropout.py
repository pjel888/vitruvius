"""Sprint GT Stream GT.5.3 — Monte Carlo dropout epistemic uncertainty.

Given the list of per-sample predictions collected from a model
run with dropout ENABLED at inference time (classic Gal & Ghahramani
2016 MC-dropout recipe), this module reports the sample variance
as the epistemic uncertainty estimate. Stdlib-only — no numpy
dependency so it can run on the 8GB M2 boot path.
"""
from __future__ import annotations

import statistics
from typing import Sequence


def compute_epistemic_uncertainty(
    model_predictions: Sequence[float],
    *,
    num_samples: int = 20,
) -> float:
    """Return the sample variance over at most ``num_samples`` MC
    dropout predictions.

    Raises ``ValueError`` if ``model_predictions`` is empty.
    A single prediction returns 0.0 (variance is undefined for
    one sample, but for our API we treat it as "no spread").
    """
    if not model_predictions:
        raise ValueError("model_predictions must be a non-empty sequence")

    window = list(model_predictions)[: max(0, int(num_samples))]
    if len(window) <= 1:
        return 0.0

    return float(statistics.variance(window))
