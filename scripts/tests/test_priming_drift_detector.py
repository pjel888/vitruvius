"""Stream Y1.3 — cosine drift detector tests."""
from __future__ import annotations

import numpy as np
import pytest

pytest.importorskip("sentence_transformers")

from vitruvius.priming.context_vector import SourceIdentity
from vitruvius.priming.drift_detector import (
    DriftReport,
    is_drift_excessive,
    measure_drift,
)


def _id_vec(values: list[float]) -> SourceIdentity:
    arr = np.array(values, dtype=np.float32)
    arr /= np.linalg.norm(arr) + 1e-9
    padded = np.zeros(384, dtype=np.float32)
    padded[: len(arr)] = arr
    return SourceIdentity(fingerprint="x", prose="y", vector=padded)


def test_identical_response_zero_drift() -> None:
    ident = _id_vec([1.0, 0.0, 0.0])
    report = measure_drift(identity=ident, response_vector=ident.vector)
    assert report.cosine_similarity == pytest.approx(1.0, abs=1e-4)
    assert report.drift == pytest.approx(0.0, abs=1e-4)


def test_orthogonal_response_full_drift() -> None:
    a = _id_vec([1.0, 0.0, 0.0])
    b_vec = np.zeros(384, dtype=np.float32)
    b_vec[1] = 1.0
    report = measure_drift(identity=a, response_vector=b_vec)
    assert report.cosine_similarity == pytest.approx(0.0, abs=1e-4)
    assert report.drift == pytest.approx(1.0, abs=1e-4)


def test_drift_threshold_default() -> None:
    a = _id_vec([1.0, 0.0, 0.0])
    b_vec = np.zeros(384, dtype=np.float32)
    b_vec[0] = 0.5
    b_vec[1] = float(np.sqrt(1 - 0.25))
    report = measure_drift(identity=a, response_vector=b_vec)
    # cosine ≈ 0.5, drift ≈ 0.5
    assert is_drift_excessive(report, threshold_cosine=0.45) is False  # 0.5 >= 0.45
    assert is_drift_excessive(report, threshold_cosine=0.55) is True   # 0.5 < 0.55
