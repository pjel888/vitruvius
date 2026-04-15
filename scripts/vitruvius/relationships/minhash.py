"""Sprint LSH-1 Task 1 — MinHash signature computation.

Classical MinHash (Broder 1997) for approximating Jaccard similarity
between feature sets. We hash each feature with ``num_perm`` independent
hash functions and take the minimum per function. Two sets with high
Jaccard similarity will produce signatures that agree on many positions.

Pure stdlib + numpy — no ``datasketch`` install. Hash functions are
synthesized by seeding a SHA-256 hash with ``(seed, perm_index, feature)``
so different permutations produce independent-ish hashes but the same
``(seed, perm_index)`` always produces the same hash for a given feature.

**Language/runtime choice.** Per AD-037 in ``.ai/10_state/decisions.md``
this module stays in Python (not Rust): near-duplicate dedup runs once
per ingestion batch, not in a hot loop, so the per-call pyo3 FFI
overhead + crate maintenance cost outweighs any Rust win. The same
perf-first cost/benefit discipline drove AD-036.
"""
from __future__ import annotations

import hashlib
from typing import Iterable

import numpy as np


def _hash_feature(feature: str, perm_index: int, seed: int) -> np.int64:
    """Deterministic per-permutation hash of a single feature string.

    Uses SHA-256 on ``f"{seed}:{perm_index}:{feature}"``, takes the
    first 8 bytes as a signed big-endian int64. Two different
    ``perm_index`` values produce independent-ish hashes; the same
    ``(seed, perm_index, feature)`` triple always produces the same
    output.
    """
    data = f"{seed}:{perm_index}:{feature}".encode("utf-8")
    digest = hashlib.sha256(data).digest()[:8]
    return np.int64(int.from_bytes(digest, "big", signed=True))


def compute_minhash_signature(
    features: Iterable[str],
    *,
    num_perm: int = 128,
    seed: int = 0,
) -> np.ndarray:
    """Compute an ``(num_perm,)`` int64 MinHash signature for a feature set.

    Empty feature sets return an array filled with ``int64.max`` (the
    "nothing beat the initial sentinel" case), which is a legitimate
    signature — two empty-feature candidates collide in all bands, so
    the LSH layer will treat them as near-duplicates, which is the
    desired behaviour (two candidates with no distinguishing features
    are indeed indistinguishable for near-duplicate detection).

    Args:
        features: An iterable of feature strings. Duplicates are
            collapsed (MinHash operates on sets, not multisets).
        num_perm: Number of independent hash permutations — larger =
            lower variance in the Jaccard estimate, but linear
            increase in compute and memory. 128 is the standard
            textbook setting.
        seed: Seed for the permutation hash family. Changing the seed
            gives a different family but preserves all guarantees.

    Returns:
        A ``(num_perm,)`` int64 numpy array — the MinHash signature.
    """
    signature = np.full(num_perm, np.iinfo(np.int64).max, dtype=np.int64)
    feature_set = set(features)
    if not feature_set:
        return signature

    for perm_index in range(num_perm):
        min_val = np.iinfo(np.int64).max
        for feature in feature_set:
            h = _hash_feature(feature, perm_index, seed)
            if h < min_val:
                min_val = h
        signature[perm_index] = min_val
    return signature
