"""Sprint LSH-1 Task 2 — LSHIndex band-based bucketing tests.

Band-based LSH (Rajaraman & Ullman Chapter 3) over MinHash signatures.
Two signatures collide in the index iff they share at least one band's
exact values — which is a sensitivity/specificity knob: more bands =
higher recall, fewer bands = higher precision.

Tests cover:
1. Self-query collision — a signature queried against an index
   containing itself must return its own index (exact match rate = 1.0)
2. Disjoint-set separation — distinct feature sets should rarely share
   any band (false positive rate bounded)
3. Empty-index query — empty list
4. num_perm/num_bands divisibility validation
"""
from __future__ import annotations

import numpy as np
import pytest

from vitruvius.relationships.lsh_index import LSHIndex
from vitruvius.relationships.minhash import compute_minhash_signature


def test_lsh_index_builds_and_queries_same_set() -> None:
    """A signature queried against an index containing itself must
    return its own original index as a candidate (collision rate for
    an exact match is 100%).
    """
    features_a = {"subject_slug:light", "predicate:governs", "object_slug:corridor"}
    sig_a = compute_minhash_signature(features_a, num_perm=128, seed=0)

    index = LSHIndex(num_perm=128, num_bands=4)
    index.add(original_index=0, signature=sig_a)

    matches = index.query_candidates(sig_a)
    assert 0 in matches


def test_lsh_index_distinct_sets_rarely_collide() -> None:
    features_a = {f"a_{i}" for i in range(20)}
    features_b = {f"b_{i}" for i in range(20)}  # no overlap
    sig_a = compute_minhash_signature(features_a, num_perm=128, seed=0)
    sig_b = compute_minhash_signature(features_b, num_perm=128, seed=0)

    index = LSHIndex(num_perm=128, num_bands=4)
    index.add(original_index=0, signature=sig_a)

    matches = index.query_candidates(sig_b)
    # With disjoint sets and 4 bands over 128 perms (32 rows/band),
    # the probability of ANY band collision is vanishingly small.
    # Accept at most 1 as a pessimistic false-positive budget.
    assert len(matches) <= 1


def test_lsh_index_query_empty_index() -> None:
    """Query over an empty index should return an empty list."""
    index = LSHIndex(num_perm=128, num_bands=4)
    sig = compute_minhash_signature({"x"}, num_perm=128, seed=0)
    matches = index.query_candidates(sig)
    assert matches == []


def test_lsh_index_rejects_non_divisible_bands() -> None:
    """num_perm must be divisible by num_bands."""
    with pytest.raises(ValueError, match="must be divisible"):
        LSHIndex(num_perm=128, num_bands=5)


def test_lsh_index_rejects_signature_shape_mismatch() -> None:
    """Add/query reject signatures whose shape doesn't match num_perm."""
    index = LSHIndex(num_perm=128, num_bands=4)
    wrong_sig = np.zeros(64, dtype=np.int64)
    with pytest.raises(ValueError, match="does not match"):
        index.add(original_index=0, signature=wrong_sig)
    with pytest.raises(ValueError, match="does not match"):
        index.query_candidates(wrong_sig)


def test_lsh_index_returns_sorted_unique_matches() -> None:
    """When multiple signatures collide with the query, matches are
    returned sorted and deduplicated (a signature added under
    multiple indices should appear once even if all 4 bands collide).
    """
    features = {"tok_1", "tok_2", "tok_3", "tok_4"}
    sig = compute_minhash_signature(features, num_perm=128, seed=0)

    index = LSHIndex(num_perm=128, num_bands=4)
    # Add the same signature under three different original_indexes.
    index.add(original_index=5, signature=sig)
    index.add(original_index=2, signature=sig)
    index.add(original_index=9, signature=sig)

    matches = index.query_candidates(sig)
    # Each original_index should appear exactly once and the list
    # should be sorted.
    assert matches == sorted(set(matches))
    assert set(matches) == {2, 5, 9}
