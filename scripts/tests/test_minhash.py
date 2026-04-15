"""Sprint LSH-1 Task 1 — MinHash signature tests.

Per AD-037 the LSH-1 plan ships a pure-stdlib + numpy MinHash
implementation (NOT ``datasketch``; NOT Rust). These tests lock in the
three load-bearing properties of the MinHash primitive:

1. Determinism — same features + seed always produce the same signature
2. Shape and dtype — ``(num_perm,)`` int64 array
3. Jaccard approximation — signature agreement rate is within ±0.15 of
   the true Jaccard for two sets with known overlap
4. Empty-set sentinel — empty feature set returns ``int64.max`` for
   every permutation position
"""
from __future__ import annotations

import numpy as np

from vitruvius.relationships.minhash import compute_minhash_signature


def test_minhash_determinism() -> None:
    features = {"a", "b", "c", "d"}
    s1 = compute_minhash_signature(features, num_perm=64, seed=42)
    s2 = compute_minhash_signature(features, num_perm=64, seed=42)
    np.testing.assert_array_equal(s1, s2)


def test_minhash_shape_and_dtype() -> None:
    s = compute_minhash_signature({"x", "y", "z"}, num_perm=128, seed=0)
    assert s.shape == (128,)
    assert s.dtype == np.int64


def test_minhash_jaccard_approximation() -> None:
    """Two sets with a known Jaccard similarity should produce MinHash
    signatures whose agreement rate approximates that Jaccard. Not
    exact — MinHash is probabilistic — but within ±0.15 for
    ``num_perm=256``.
    """
    set_a = {f"token_{i}" for i in range(100)}
    set_b = {f"token_{i}" for i in range(50, 150)}
    # True Jaccard = |A intersect B| / |A union B| = 50 / 150 approx 0.333

    sig_a = compute_minhash_signature(set_a, num_perm=256, seed=0)
    sig_b = compute_minhash_signature(set_b, num_perm=256, seed=0)

    agreement = float(np.sum(sig_a == sig_b) / len(sig_a))
    true_jaccard = 50 / 150
    assert abs(agreement - true_jaccard) < 0.15, (
        f"agreement {agreement} too far from true jaccard {true_jaccard}"
    )


def test_minhash_empty_set_returns_sentinel() -> None:
    s = compute_minhash_signature(set(), num_perm=16, seed=0)
    assert s.shape == (16,)
    # Empty set: all positions should be the INT64 max (the "no element
    # beat this" sentinel).
    assert np.all(s == np.iinfo(np.int64).max)


def test_minhash_different_seeds_produce_different_signatures() -> None:
    """Seed participates in the permutation construction so two
    different seeds over the same feature set must not produce
    byte-identical signatures (collisions are possible on a few
    positions but the overall arrays must differ).
    """
    features = {"lot-area", "minimum-lot-area", "requires"}
    s1 = compute_minhash_signature(features, num_perm=64, seed=0)
    s2 = compute_minhash_signature(features, num_perm=64, seed=1)
    assert not np.array_equal(s1, s2)
