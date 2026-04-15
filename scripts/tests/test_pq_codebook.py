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


def test_encode_to_pq_shape_and_dtype() -> None:
    rng = np.random.default_rng(seed=0)
    embeddings = rng.standard_normal((100, 64)).astype(np.float32)
    codebook = train_pq_codebook(embeddings, M=8, k=32, n_iter=5, seed=42)

    from vitruvius.graph.pq_codebook import encode_to_pq

    codes = encode_to_pq(embeddings, codebook)
    assert codes.shape == (100, 8)
    assert codes.dtype == np.uint8
    assert codes.max() < 32  # all centroid indices in range


def test_decode_from_pq_shape_and_reconstruction() -> None:
    rng = np.random.default_rng(seed=0)
    embeddings = rng.standard_normal((50, 64)).astype(np.float32)
    codebook = train_pq_codebook(embeddings, M=8, k=128, n_iter=25, seed=42)

    from vitruvius.graph.pq_codebook import decode_from_pq, encode_to_pq

    codes = encode_to_pq(embeddings, codebook)
    reconstructed = decode_from_pq(codes, codebook)
    assert reconstructed.shape == embeddings.shape
    assert reconstructed.dtype == np.float32

    # Reconstruction error: average L2 norm ratio. At k=128 on
    # random input the error is bounded but non-zero.
    diff_norms = np.linalg.norm(embeddings - reconstructed, axis=1)
    orig_norms = np.linalg.norm(embeddings, axis=1)
    rel_error = (diff_norms / np.maximum(orig_norms, 1e-8)).mean()
    assert rel_error < 1.0  # reconstruction is at least somewhat useful


def test_adc_distance_matches_decoded_approximation() -> None:
    """ADC distance should match the L2 distance computed against
    decoded vectors to within numerical error (both round the database
    operand to centroids; ADC just skips materialising the
    reconstruction)."""
    rng = np.random.default_rng(seed=0)
    db = rng.standard_normal((200, 64)).astype(np.float32)
    codebook = train_pq_codebook(db, M=8, k=128, n_iter=25, seed=42)

    from vitruvius.graph.pq_codebook import (
        adc_distance,
        decode_from_pq,
        encode_to_pq,
    )

    codes = encode_to_pq(db, codebook)
    query = rng.standard_normal(64).astype(np.float32)

    adc = adc_distance(query, codes, codebook)
    assert adc.shape == (200,)
    assert adc.dtype == np.float32

    decoded = decode_from_pq(codes, codebook)
    ref = np.sum((decoded - query) ** 2, axis=1)

    np.testing.assert_allclose(adc, ref, rtol=1e-4, atol=1e-4)
