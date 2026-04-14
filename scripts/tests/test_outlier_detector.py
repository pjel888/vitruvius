"""Mahalanobis outlier detector — fits on reference set, scores new chunks."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pytest

from vitruvius.normalization.ast_chunker import Chunk
from vitruvius.normalization.embedding_chunker import EmbeddedChunk
from vitruvius.normalization.outlier_detector import (
    DEFAULT_THRESHOLD,
    REGULARIZATION_EPSILON,
    OutlierModel,
    OutlierReport,
    OutlierResult,
    fit_outlier_model,
    mahalanobis_distance,
    score_chunks,
    write_report,
)


def _make_embedded_chunk(chunk_id: str, vec: list[float]) -> EmbeddedChunk:
    return EmbeddedChunk(
        chunk=Chunk(
            chunk_id=chunk_id,
            source_path="x.md",
            source_section_id="",
            parent_titles=(),
            heading="",
            body="body",
            token_count=1,
        ),
        embedding=tuple(float(v) for v in vec),
    )


def test_centroid_of_uniform_cluster_is_mean() -> None:
    vecs = [[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]]
    model = fit_outlier_model(vecs)
    assert model.centroid == (3.0, 4.0)


def test_outlier_exceeds_threshold() -> None:
    np.random.seed(42)
    refs = np.random.randn(100, 2).tolist()
    model = fit_outlier_model(refs)
    far = _make_embedded_chunk("far", [10.0, 10.0])
    near = _make_embedded_chunk("near", refs[0])
    report = score_chunks([far, near], model)
    assert report.total == 2
    far_result = next(r for r in report.results if r.chunk_id == "far")
    near_result = next(r for r in report.results if r.chunk_id == "near")
    assert far_result.is_outlier is True
    assert far_result.distance > near_result.distance


def test_cluster_points_below_threshold() -> None:
    np.random.seed(42)
    refs = np.random.randn(100, 2).tolist()
    model = fit_outlier_model(refs)
    chunks = [_make_embedded_chunk(f"r{i}", v) for i, v in enumerate(refs)]
    report = score_chunks(chunks, model)
    assert report.outlier_count <= 5


def test_singular_covariance_uses_pinv() -> None:
    identical = [[1.0, 1.0, 1.0]] * 5
    model = fit_outlier_model(identical)
    assert isinstance(model, OutlierModel)
    dist = mahalanobis_distance([1.0, 1.0, 1.0], model)
    assert dist == pytest.approx(0.0, abs=1e-9)


def test_persists_scoring_to_manifest(tmp_path: Path) -> None:
    vecs = [[1.0, 0.0], [0.0, 1.0], [1.0, 1.0], [0.0, 0.0]]
    model = fit_outlier_model(vecs)
    chunks = [_make_embedded_chunk(f"c{i}", v) for i, v in enumerate(vecs)]
    report = score_chunks(chunks, model)
    out = tmp_path / "outliers.json"
    write_report(report, out)
    assert out.exists()
    data = json.loads(out.read_text())
    assert "threshold" in data
    assert "total" in data
    assert "outlier_count" in data
    assert "results" in data
    assert data["total"] == 4


def test_report_is_sorted_by_distance_descending() -> None:
    np.random.seed(7)
    refs = np.random.randn(50, 3).tolist()
    model = fit_outlier_model(refs)
    chunks = [
        _make_embedded_chunk("near", refs[0]),
        _make_embedded_chunk("far", [10.0, 10.0, 10.0]),
        _make_embedded_chunk("medium", [2.0, 2.0, 2.0]),
    ]
    report = score_chunks(chunks, model)
    distances = [r.distance for r in report.results]
    assert distances == sorted(distances, reverse=True)


def test_mahalanobis_distance_is_non_negative() -> None:
    model = fit_outlier_model([[0.0, 0.0], [1.0, 1.0], [2.0, 2.0]])
    for pt in [[0.5, 0.5], [10.0, 10.0], [-1.0, -1.0]]:
        assert mahalanobis_distance(pt, model) >= 0.0


def test_write_report_is_deterministic(tmp_path: Path) -> None:
    np.random.seed(11)
    refs = np.random.randn(20, 3).tolist()
    model = fit_outlier_model(refs)
    chunks = [_make_embedded_chunk(f"c{i}", v) for i, v in enumerate(refs)]
    report = score_chunks(chunks, model)
    out1 = tmp_path / "r1.json"
    out2 = tmp_path / "r2.json"
    write_report(report, out1)
    write_report(report, out2)
    assert out1.read_text() == out2.read_text()


def test_threshold_is_configurable() -> None:
    vecs = [[0.0, 0.0], [1.0, 0.0], [0.0, 1.0], [1.0, 1.0]]
    model = fit_outlier_model(vecs)
    chunks = [_make_embedded_chunk("pt", [5.0, 5.0])]
    report_high = score_chunks(chunks, model, threshold=1e9)
    assert report_high.outlier_count == 0
    report_low = score_chunks(chunks, model, threshold=1.0)
    assert report_low.outlier_count == 1


def test_fit_rejects_empty_reference_set() -> None:
    with pytest.raises(ValueError):
        fit_outlier_model([])


def test_default_threshold_constant() -> None:
    assert DEFAULT_THRESHOLD == 3.0
    assert REGULARIZATION_EPSILON == 1e-6


def test_report_tie_break_by_chunk_id() -> None:
    # Two chunks at identical distance — order must be stable by chunk_id.
    vecs = [[0.0, 0.0], [1.0, 1.0], [2.0, 2.0]]
    model = fit_outlier_model(vecs)
    chunks = [
        _make_embedded_chunk("bravo", [1.0, 1.0]),
        _make_embedded_chunk("alpha", [1.0, 1.0]),
    ]
    report = score_chunks(chunks, model)
    ids = [r.chunk_id for r in report.results]
    assert ids == ["alpha", "bravo"]


def test_model_is_frozen_and_hashable() -> None:
    model = fit_outlier_model([[0.0, 0.0], [1.0, 1.0]])
    assert isinstance(hash(model), int)
    with pytest.raises(Exception):
        model.centroid = (9.0, 9.0)  # type: ignore[misc]


def test_score_empty_chunks() -> None:
    model = fit_outlier_model([[0.0, 0.0], [1.0, 1.0]])
    report = score_chunks([], model)
    assert report.total == 0
    assert report.outlier_count == 0
    assert report.results == ()


def test_write_report_sort_keys_stable(tmp_path: Path) -> None:
    vecs = [[0.0, 0.0], [1.0, 1.0]]
    model = fit_outlier_model(vecs)
    chunks = [_make_embedded_chunk("c0", [0.0, 0.0])]
    report = score_chunks(chunks, model)
    out = tmp_path / "r.json"
    write_report(report, out)
    text = out.read_text()
    # Deterministic JSON must have keys alphabetised at top level.
    parsed = json.loads(text)
    assert list(parsed.keys()) == sorted(parsed.keys())
