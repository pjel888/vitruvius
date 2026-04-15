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


def encode_to_pq(embeddings: np.ndarray, codebook: PQCodebook) -> np.ndarray:
    """Quantize ``embeddings`` to uint8 PQ codes.

    Input shape: ``(N, M * sub_dim)``. Output shape: ``(N, M)`` uint8.
    Each output byte is the index of the nearest centroid in its
    sub-quantizer.

    Rust Line: hot loop is M iterations of vectorised L2 distance via
    BLAS gemm + ``np.argmin``. C-backed end-to-end.
    DEFER_ALREADY_NATIVE.
    """
    n = embeddings.shape[0]
    expected_dim = codebook.M * codebook.sub_dim
    if embeddings.shape[1] != expected_dim:
        raise ValueError(
            f"embedding dim {embeddings.shape[1]} does not match codebook "
            f"{codebook.M}*{codebook.sub_dim}={expected_dim}"
        )
    codes = np.zeros((n, codebook.M), dtype=np.uint8)
    for m in range(codebook.M):
        sub = embeddings[:, m * codebook.sub_dim : (m + 1) * codebook.sub_dim]
        cent = codebook.centroids[m]  # (k, sub_dim)
        # Squared distances: (n, k)
        sub_sq = np.sum(sub * sub, axis=1, keepdims=True)
        cent_sq = np.sum(cent * cent, axis=1, keepdims=True).T
        cross = sub.astype(np.float32) @ cent.T
        dist = sub_sq - 2.0 * cross + cent_sq
        labels = np.argmin(dist, axis=1)
        codes[:, m] = labels.astype(np.uint8)
    return codes


def decode_from_pq(codes: np.ndarray, codebook: PQCodebook) -> np.ndarray:
    """Reconstruct approximate embeddings from PQ codes.

    Input shape: ``(N, M)`` uint8. Output shape: ``(N, M * sub_dim)``
    float32. Reconstruction is lossy — the returned vectors are the
    concatenated centroids selected by each code byte.
    """
    n = codes.shape[0]
    dim = codebook.M * codebook.sub_dim
    reconstructed = np.zeros((n, dim), dtype=np.float32)
    for m in range(codebook.M):
        reconstructed[:, m * codebook.sub_dim : (m + 1) * codebook.sub_dim] = (
            codebook.centroids[m][codes[:, m]]
        )
    return reconstructed


def adc_distance(
    query: np.ndarray,
    codes: np.ndarray,
    codebook: PQCodebook,
) -> np.ndarray:
    """Asymmetric distance from ``query`` to every code in ``codes``.

    Precomputes the squared distance from each of the query's M
    sub-vectors to each of the k centroids (one O(M*k) lookup table),
    then sums the selected centroid distances per code row in O(M)
    per code. At M=8, k=256, N=10000 this is ~82k flops vs ~640k for a
    naive decode + L2.

    Output: ``(N,)`` float32 array of approximate squared L2 distances.

    Rust Line: M iterations of a vectorised diff + sum + an
    integer-index gather/sum. All numpy primitives.
    DEFER_ALREADY_NATIVE.
    """
    expected_dim = codebook.M * codebook.sub_dim
    if query.shape != (expected_dim,):
        raise ValueError(
            f"query must have shape ({expected_dim},), got {query.shape}"
        )
    n = codes.shape[0]
    lut = np.zeros((codebook.M, codebook.k), dtype=np.float32)
    q = query.astype(np.float32, copy=False)
    for m in range(codebook.M):
        q_sub = q[m * codebook.sub_dim : (m + 1) * codebook.sub_dim]
        cent = codebook.centroids[m]
        diff = cent - q_sub  # (k, sub_dim)
        lut[m] = np.sum(diff * diff, axis=1)

    dists = np.zeros(n, dtype=np.float32)
    for m in range(codebook.M):
        dists += lut[m][codes[:, m]]
    return dists


def save_codebook(codebook: PQCodebook, path: Path | str) -> None:
    """Save a codebook to ``path`` as a compressed numpy archive.

    Rust Line: ``np.savez_compressed`` is C + zlib. Python orchestration
    is fine here. DEFER_ALREADY_NATIVE.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(
        path,
        centroids=codebook.centroids,
        M=np.int32(codebook.M),
        k=np.int32(codebook.k),
        sub_dim=np.int32(codebook.sub_dim),
    )


def load_codebook(path: Path | str) -> PQCodebook:
    """Load a codebook from ``path``."""
    with np.load(Path(path)) as data:
        return PQCodebook(
            centroids=data["centroids"].astype(np.float32, copy=True),
            M=int(data["M"]),
            k=int(data["k"]),
            sub_dim=int(data["sub_dim"]),
        )
