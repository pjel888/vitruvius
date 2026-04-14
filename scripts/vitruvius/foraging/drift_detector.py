"""Stream O.2 — source-drift detector reusing the Stream C.4 Mahalanobis
outlier module.

Fits a Mahalanobis model over a baseline set of source-embedding
vectors and checks whether an incoming vector falls outside the
configured threshold. Used by the (future) foraging fetcher to decide
whether a newly discovered document is a legitimate new source or
noise from an unrelated domain.

This is a *scaffold*: it does not perform any HTTP fetches and does
not auto-schedule any work. Callers feed it vectors that are already
computed elsewhere.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from ..normalization.outlier_detector import (
    fit_outlier_model,
    mahalanobis_distance,
)


@dataclass(frozen=True)
class DriftVerdict:
    distance: float
    threshold: float
    is_drifted: bool


def detect_source_drift(
    *,
    baseline_vectors: Sequence[Sequence[float]],
    incoming_vector: Sequence[float],
    threshold: float = 3.0,
) -> DriftVerdict:
    """Check whether ``incoming_vector`` is an outlier against the
    baseline distribution.

    ``baseline_vectors`` must contain at least 2 rows so the
    Mahalanobis fit has a meaningful covariance. A single-row
    baseline collapses to a degenerate distribution (all-zero
    covariance) which is useless for drift detection.
    """
    if len(baseline_vectors) < 2:
        raise ValueError(
            "detect_source_drift requires at least 2 baseline vectors "
            "to fit a meaningful Mahalanobis distribution"
        )
    model = fit_outlier_model(baseline_vectors)
    distance = mahalanobis_distance(incoming_vector, model)
    return DriftVerdict(
        distance=float(distance),
        threshold=float(threshold),
        is_drifted=bool(distance > threshold),
    )
