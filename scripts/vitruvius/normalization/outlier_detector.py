"""Mahalanobis outlier detector — Task C.4.

Fits a (centroid, regularised-pinv-covariance) model on a reference set
of embeddings and scores new chunks by Mahalanobis distance. A ridge
`REGULARIZATION_EPSILON * I` keeps the covariance invertible when the
reference set is small or degenerate.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

import numpy as np

from .embedding_chunker import EmbeddedChunk


DEFAULT_THRESHOLD = 3.0
REGULARIZATION_EPSILON = 1e-6


@dataclass(frozen=True)
class OutlierModel:
    centroid: tuple[float, ...]
    covariance_inv: tuple[tuple[float, ...], ...]
    ridge: float


@dataclass(frozen=True)
class OutlierResult:
    chunk_id: str
    distance: float
    is_outlier: bool


@dataclass(frozen=True)
class OutlierReport:
    threshold: float
    total: int
    outlier_count: int
    results: tuple[OutlierResult, ...]


def fit_outlier_model(embeddings: Sequence[Sequence[float]]) -> OutlierModel:
    if len(embeddings) == 0:
        raise ValueError("fit_outlier_model requires at least one embedding")

    matrix = np.asarray(embeddings, dtype=np.float64)
    if matrix.ndim != 2:
        raise ValueError("embeddings must be a 2-D sequence")

    centroid = np.mean(matrix, axis=0)
    dim = matrix.shape[1]

    if matrix.shape[0] == 1:
        covariance = np.zeros((dim, dim), dtype=np.float64)
    else:
        covariance = np.cov(matrix, rowvar=False)
        covariance = np.atleast_2d(covariance)

    cov_reg = covariance + REGULARIZATION_EPSILON * np.eye(dim, dtype=np.float64)
    cov_inv = np.linalg.pinv(cov_reg)

    return OutlierModel(
        centroid=tuple(float(x) for x in centroid),
        covariance_inv=tuple(
            tuple(float(v) for v in row) for row in cov_inv
        ),
        ridge=REGULARIZATION_EPSILON,
    )


def mahalanobis_distance(
    x: Sequence[float],
    model: OutlierModel,
) -> float:
    vec = np.asarray(x, dtype=np.float64)
    centroid = np.asarray(model.centroid, dtype=np.float64)
    cov_inv = np.asarray(model.covariance_inv, dtype=np.float64)

    if vec.shape != centroid.shape:
        raise ValueError(
            f"embedding dim {vec.shape} does not match model centroid {centroid.shape}"
        )

    delta = vec - centroid
    squared = float(delta @ cov_inv @ delta)
    return float(np.sqrt(max(0.0, squared)))


def score_chunks(
    chunks: Sequence[EmbeddedChunk],
    model: OutlierModel,
    *,
    threshold: float = DEFAULT_THRESHOLD,
) -> OutlierReport:
    results: list[OutlierResult] = []
    for chunk in chunks:
        dist = mahalanobis_distance(chunk.embedding, model)
        results.append(
            OutlierResult(
                chunk_id=chunk.chunk.chunk_id,
                distance=dist,
                is_outlier=dist > threshold,
            )
        )

    results.sort(key=lambda r: (-r.distance, r.chunk_id))

    outlier_count = sum(1 for r in results if r.is_outlier)
    return OutlierReport(
        threshold=threshold,
        total=len(results),
        outlier_count=outlier_count,
        results=tuple(results),
    )


def write_report(report: OutlierReport, out_path: Path) -> None:
    payload = {
        "outlier_count": report.outlier_count,
        "results": [
            {
                "chunk_id": r.chunk_id,
                "distance": r.distance,
                "is_outlier": r.is_outlier,
            }
            for r in report.results
        ],
        "threshold": report.threshold,
        "total": report.total,
    }
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n"
    )
