"""Stream O.2 — drift detector reusing the Stream C.4 Mahalanobis module."""
from __future__ import annotations

import pytest

pytest.importorskip("numpy")

from vitruvius.foraging.drift_detector import (
    DriftVerdict,
    detect_source_drift,
)


def test_in_distribution_vector_is_not_drifted() -> None:
    # Baseline: a cluster of vectors near the origin.
    baseline = [
        [0.0, 0.0, 0.0],
        [0.1, 0.0, 0.0],
        [0.0, 0.1, 0.0],
        [0.0, 0.0, 0.1],
        [-0.05, 0.0, 0.0],
        [0.0, -0.05, 0.0],
    ]
    incoming = [0.02, 0.01, 0.0]  # sits inside the cluster
    verdict = detect_source_drift(
        baseline_vectors=baseline,
        incoming_vector=incoming,
        threshold=3.0,
    )
    assert isinstance(verdict, DriftVerdict)
    assert verdict.is_drifted is False
    assert verdict.distance >= 0.0


def test_out_of_distribution_vector_is_drifted() -> None:
    baseline = [
        [0.0, 0.0, 0.0],
        [0.1, 0.0, 0.0],
        [0.0, 0.1, 0.0],
        [0.0, 0.0, 0.1],
        [-0.05, 0.0, 0.0],
        [0.0, -0.05, 0.0],
    ]
    incoming = [50.0, 50.0, 50.0]  # far from the cluster
    verdict = detect_source_drift(
        baseline_vectors=baseline,
        incoming_vector=incoming,
        threshold=3.0,
    )
    assert verdict.is_drifted is True
    assert verdict.distance > 3.0


def test_empty_baseline_raises() -> None:
    with pytest.raises(ValueError, match="at least 2"):
        detect_source_drift(
            baseline_vectors=[],
            incoming_vector=[0.0, 0.0],
            threshold=3.0,
        )
