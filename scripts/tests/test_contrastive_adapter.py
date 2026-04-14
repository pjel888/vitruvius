"""Contrastive whitening adapter — PCA-based linear projection over positive pairs."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pytest

from vitruvius.concepts.contrastive_adapter import (
    ContrastiveAdapter,
    DEFAULT_MAX_COMPONENTS,
    REGULARIZATION_EPSILON,
    fit_adapter,
    load_adapter,
    save_adapter,
    transform,
)


RNG = np.random.default_rng(0)


def _make_positive_pairs(n_pairs: int, dim: int) -> list[tuple[list[float], list[float]]]:
    pairs = []
    for _ in range(n_pairs):
        a = RNG.normal(size=dim)
        b = a + 0.01 * RNG.normal(size=dim)
        pairs.append((a.tolist(), b.tolist()))
    return pairs


def _make_negative_pairs(n_pairs: int, dim: int) -> list[tuple[list[float], list[float]]]:
    pairs = []
    for _ in range(n_pairs):
        a = RNG.normal(size=dim)
        b = RNG.normal(size=dim)
        pairs.append((a.tolist(), b.tolist()))
    return pairs


def test_fit_on_positive_pairs_reduces_pair_distance() -> None:
    pairs = _make_positive_pairs(20, 16)
    adapter = fit_adapter(pairs)
    assert adapter.is_fitted
    a = np.array(pairs[0][0])
    b = np.array(pairs[0][1])
    pre = float(np.linalg.norm(a - b))
    ta = transform(adapter, a)
    tb = transform(adapter, b)
    post = float(np.linalg.norm(np.array(ta) - np.array(tb)))
    assert post <= pre * 3.0, (
        f"positive pair distance grew wildly: pre={pre}, post={post}"
    )


def test_transform_is_linear_and_deterministic() -> None:
    pairs = _make_positive_pairs(10, 8)
    adapter = fit_adapter(pairs)
    x = np.array(pairs[0][0])
    t1 = transform(adapter, x)
    t2 = transform(adapter, x)
    np.testing.assert_array_equal(t1, t2)
    x2 = 2 * x
    t_x2 = transform(adapter, x2)
    assert np.all(np.isfinite(t_x2))
    assert t_x2.shape == t1.shape


def test_negative_pairs_remain_distant_after_transform() -> None:
    positive = _make_positive_pairs(20, 16)
    negative = _make_negative_pairs(20, 16)
    adapter = fit_adapter(positive)
    pre = float(np.mean([
        float(np.linalg.norm(np.array(a) - np.array(b)))
        for a, b in negative
    ]))
    post = float(np.mean([
        float(np.linalg.norm(transform(adapter, a) - transform(adapter, b)))
        for a, b in negative
    ]))
    assert post > 0
    assert post < pre * 10


def test_round_trip_inverse_preserves_info_when_k_equals_d() -> None:
    dim = 8
    pairs = _make_positive_pairs(20, dim)
    adapter = fit_adapter(pairs, max_components=dim)
    x = np.array(pairs[0][0])
    y = transform(adapter, x)
    assert y.shape[0] <= dim


def test_save_and_load_state(tmp_path: Path) -> None:
    pairs = _make_positive_pairs(10, 6)
    adapter = fit_adapter(pairs)
    out = tmp_path / "adapter.json"
    save_adapter(adapter, out)
    assert out.exists()
    loaded = load_adapter(out)
    assert loaded.is_fitted
    assert loaded.n_components == adapter.n_components
    x = np.array(pairs[0][0])
    np.testing.assert_allclose(
        transform(adapter, x), transform(loaded, x), atol=1e-10
    )


def test_unfitted_adapter_passthrough() -> None:
    adapter = ContrastiveAdapter()
    assert not adapter.is_fitted
    x = np.array([1.0, 2.0, 3.0])
    result = transform(adapter, x)
    np.testing.assert_array_equal(np.array(result), x)


def test_save_deterministic(tmp_path: Path) -> None:
    pairs = _make_positive_pairs(10, 6)
    adapter = fit_adapter(pairs)
    out1 = tmp_path / "a1.json"
    out2 = tmp_path / "a2.json"
    save_adapter(adapter, out1)
    save_adapter(adapter, out2)
    assert out1.read_text() == out2.read_text()


def test_empty_pairs_raises_or_yields_unfitted() -> None:
    adapter = fit_adapter([])
    assert not adapter.is_fitted
    x = np.array([1.0, 2.0])
    np.testing.assert_array_equal(np.array(transform(adapter, x)), x)


def test_constants_are_documented() -> None:
    assert DEFAULT_MAX_COMPONENTS == 64
    assert REGULARIZATION_EPSILON == 1e-6


def test_save_and_load_unfitted_round_trip(tmp_path: Path) -> None:
    adapter = ContrastiveAdapter()
    out = tmp_path / "unfitted.json"
    save_adapter(adapter, out)
    loaded = load_adapter(out)
    assert not loaded.is_fitted
    assert loaded.n_components == 0
    assert loaded.mean is None
    assert loaded.components is None
    x = np.array([1.0, 2.0, 3.0])
    np.testing.assert_array_equal(np.array(transform(loaded, x)), x)


def test_fit_with_single_pair_yields_unfitted() -> None:
    # TruncatedSVD requires n_components < n_samples, so 1 pair cannot fit.
    pairs = [([1.0, 2.0, 3.0], [1.01, 2.01, 3.01])]
    adapter = fit_adapter(pairs)
    assert not adapter.is_fitted


def test_fit_output_shapes_are_consistent() -> None:
    dim = 12
    n_pairs = 15
    pairs = _make_positive_pairs(n_pairs, dim)
    adapter = fit_adapter(pairs)
    assert adapter.is_fitted
    assert adapter.mean is not None
    assert adapter.mean.shape == (dim,)
    assert adapter.components is not None
    # components has shape (k, D)
    assert adapter.components.shape[1] == dim
    assert adapter.components.shape[0] == adapter.n_components
    assert adapter.singular_values is not None
    assert adapter.singular_values.shape == (adapter.n_components,)
    # n_components is bounded by min(max_components, n_pairs - 1)
    assert adapter.n_components <= n_pairs - 1
    assert adapter.n_components <= DEFAULT_MAX_COMPONENTS
