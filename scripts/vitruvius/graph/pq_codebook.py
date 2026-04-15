"""Sprint PQ-1 — Product Quantization codebook for GraphSAGE embeddings.

Classical PQ (Jegou, Douze, Schmid 2010) for compressing float32
embeddings into uint8 codes. Pure-numpy implementation — no scikit-learn,
no FAISS, no new installs. See the plan at
``.ai/03_plans/2026-04-15-graphsage-pq-embeddings-plan.md`` for
architectural context.

Rust Line note (per AD-036 perf-first directive): every hot loop in
this module is a single numpy call (matrix-multiply, ``np.argmin``,
``np.add.at``, integer-index gather). All are C-backed via numpy's
BLAS/SIMD path, so a Rust port would only orchestrate the same
operations and add FFI overhead. DEFER_ALREADY_NATIVE — Python
remains correct here.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np


@dataclass(frozen=True)
class PQCodebook:
    """Learned centroids for M sub-quantizers.

    ``centroids`` is a ``(M, k, sub_dim)`` float32 array where
    ``centroids[m, c, :]`` is the ``sub_dim``-dimensional centroid
    of the ``c``-th cluster in the ``m``-th sub-quantizer.
    """

    centroids: np.ndarray
    M: int
    k: int
    sub_dim: int


def _kmeans(
    points: np.ndarray,
    *,
    k: int,
    n_iter: int,
    rng: np.random.Generator,
) -> np.ndarray:
    """Pure-numpy k-means. Returns ``(k, d)`` centroids as float32.

    All compute paths use numpy broadcasting / matmul (BLAS-backed).
    """
    n, d = points.shape
    if n <= k:
        # Degenerate: fewer points than clusters. Use the available
        # points as centroids; pad the rest with zeros (they will not
        # win any encoder assignments at runtime if the same points
        # are encoded back).
        centroids = np.zeros((k, d), dtype=np.float32)
        centroids[:n] = points
        return centroids

    idx = rng.choice(n, size=k, replace=False)
    centroids = points[idx].astype(np.float32, copy=True)

    for _ in range(n_iter):
        # Squared L2 distances via the polarisation identity:
        # ||p - c||^2 = ||p||^2 - 2 p . c + ||c||^2
        p_sq = np.sum(points * points, axis=1, keepdims=True)  # (n, 1)
        c_sq = np.sum(centroids * centroids, axis=1, keepdims=True).T  # (1, k)
        cross = points @ centroids.T  # (n, k) — BLAS gemm
        dist = p_sq - 2.0 * cross + c_sq
        labels = np.argmin(dist, axis=1)  # (n,)

        # Update centroids to the mean of their assigned points via
        # vectorised scatter-add.
        new_centroids = np.zeros_like(centroids)
        counts = np.zeros(k, dtype=np.int64)
        np.add.at(new_centroids, labels, points)
        np.add.at(counts, labels, 1)
        nonzero = counts > 0
        new_centroids[nonzero] /= counts[nonzero, None]
        # Empty clusters keep their previous centroid (no-NaN guarantee).
        new_centroids[~nonzero] = centroids[~nonzero]
        centroids = new_centroids

    return centroids


def train_pq_codebook(
    embeddings: np.ndarray,
    *,
    M: int = 8,
    k: int = 256,
    n_iter: int = 25,
    seed: int = 0,
) -> PQCodebook:
    """Train M sub-quantizer codebooks on ``embeddings``.

    ``embeddings`` must be a ``(N, dim)`` float32 array where ``dim``
    is divisible by ``M``. Runs k-means with ``k`` centroids on each of
    ``M`` non-overlapping sub-spaces. Deterministic under ``seed``.

    Raises:
        ValueError: if ``embeddings`` is empty or ``dim`` is not
            divisible by ``M``.
    """
    if embeddings.size == 0 or embeddings.shape[0] == 0:
        raise ValueError("cannot train PQ codebook on empty embeddings")
    n, dim = embeddings.shape
    if dim % M != 0:
        raise ValueError(
            f"embedding dim {dim} must be divisible by M={M}; "
            f"got {dim} % {M} = {dim % M}"
        )
    sub_dim = dim // M

    rng = np.random.default_rng(seed=seed)
    centroids = np.zeros((M, k, sub_dim), dtype=np.float32)
    for m in range(M):
        sub = embeddings[:, m * sub_dim : (m + 1) * sub_dim].astype(
            np.float32, copy=False
        )
        centroids[m] = _kmeans(sub, k=k, n_iter=n_iter, rng=rng)

    return PQCodebook(
        centroids=centroids,
        M=M,
        k=k,
        sub_dim=sub_dim,
    )
