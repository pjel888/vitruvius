"""Sprint PQ-1 Task 1 — PQCodebook + train_pq_codebook tests."""
from __future__ import annotations

import numpy as np
import pytest

from vitruvius.graph.pq_codebook import PQCodebook, train_pq_codebook


def test_train_pq_codebook_shape() -> None:
    rng = np.random.default_rng(seed=0)
    embeddings = rng.standard_normal((500, 64)).astype(np.float32)
    codebook = train_pq_codebook(embeddings, M=8, k=256, n_iter=10, seed=42)
    assert isinstance(codebook, PQCodebook)
    assert codebook.M == 8
    assert codebook.k == 256
    assert codebook.sub_dim == 8
    assert codebook.centroids.shape == (8, 256, 8)
    assert codebook.centroids.dtype == np.float32


def test_train_pq_codebook_deterministic_under_seed() -> None:
    rng = np.random.default_rng(seed=0)
    embeddings = rng.standard_normal((200, 64)).astype(np.float32)
    a = train_pq_codebook(embeddings, M=8, k=16, n_iter=5, seed=123)
    b = train_pq_codebook(embeddings, M=8, k=16, n_iter=5, seed=123)
    np.testing.assert_array_equal(a.centroids, b.centroids)


def test_train_pq_codebook_rejects_non_divisible_dim() -> None:
    embeddings = np.zeros((10, 63), dtype=np.float32)  # 63 not divisible by 8
    with pytest.raises(ValueError, match="must be divisible"):
        train_pq_codebook(embeddings, M=8, k=4, n_iter=1)


def test_train_pq_codebook_empty_input() -> None:
    empty = np.zeros((0, 64), dtype=np.float32)
    with pytest.raises(ValueError, match="empty"):
        train_pq_codebook(empty, M=8, k=16, n_iter=1)
