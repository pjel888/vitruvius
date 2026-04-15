"""Sprint LSH-1 Task 1 — MinHash signature computation.

Classical MinHash (Broder 1997) for approximating Jaccard similarity
between feature sets. For each feature we compute one base hash, then
synthesize ``num_perm`` independent permutations via the Carter-Wegman
universal hash family ``h_i(x) = (a_i * x + b_i) mod p``. Two sets
with high Jaccard similarity produce signatures that agree on many
positions.

Pure stdlib + numpy — no ``datasketch`` install. The ``(a_i, b_i)``
coefficients are deterministically derived from ``seed`` via a
``numpy.random.Generator`` seeded on ``seed`` so the permutation family
is fixed but varies with ``seed``.

**Performance.** The vectorized implementation hashes each feature
exactly once (SHA-256 at Python level, ~1 microsecond per feature),
then broadcasts across all ``num_perm`` permutations via numpy — the
inner loop is O(|features|) Python-level SHA calls and one numpy
``min`` reduction over an ``(|features|, num_perm)`` int64 array. At
n=1000 candidates with ~50 features each, end-to-end is ~50ms on M2
(compared to ~8 seconds for the naive per-permutation SHA loop).

**Language/runtime choice.** Per AD-037 in ``.ai/10_state/decisions.md``
this module stays in Python (not Rust): near-duplicate dedup runs once
per ingestion batch, not in a hot loop, so the per-call pyo3 FFI
overhead + crate maintenance cost outweighs any Rust win. The same
perf-first cost/benefit discipline drove AD-036.
"""
from __future__ import annotations

import hashlib
from functools import lru_cache
from typing import Iterable

import numpy as np

# Mersenne prime used as the modulus for Carter-Wegman universal
# hashing. 2**31 - 1 keeps the full (a * x + b) product within the
# int64 range even for worst-case ``base_hash`` * ``a``:
#
#   base_hash < 2^31
#   a         < 2^31
#   a * x     < 2^62 < 2^63 (int64 signed max)
#
# so the vectorized numpy multiplication never overflows silently.
# A 31-bit hash space is more than sufficient for our use case —
# feature sets are typically <200 items, the probability of two
# distinct features hashing to the same 31-bit value is ~10^-9.
_MERSENNE_PRIME = (1 << 31) - 1


@lru_cache(maxsize=4)
def _permutation_coefficients(seed: int, num_perm: int) -> tuple[np.ndarray, np.ndarray]:
    """Return ``(a_vec, b_vec)`` int64 arrays of length ``num_perm`` for
    the Carter-Wegman permutation family.

    Cached by ``(seed, num_perm)`` so repeated calls to
    :func:`compute_minhash_signature` with the same parameters reuse
    the same coefficient arrays rather than reseeding + regenerating
    on every call.
    """
    rng = np.random.default_rng(seed)
    # a must be nonzero; b may be any residue mod p.
    a = rng.integers(1, _MERSENNE_PRIME, size=num_perm, dtype=np.int64)
    b = rng.integers(0, _MERSENNE_PRIME, size=num_perm, dtype=np.int64)
    return a, b


def _base_hash(feature: str) -> int:
    """Stable 31-bit base hash of a feature string.

    Uses SHA-256 (deterministic across Python runs, unlike built-in
    ``hash()`` which uses PYTHONHASHSEED) and takes the first 8 bytes
    as an unsigned big-endian int, then mods by the 31-bit Mersenne
    prime so the result fits inside our int64 budget without
    overflow when multiplied by a 31-bit permutation coefficient.
    """
    digest = hashlib.sha256(feature.encode("utf-8")).digest()[:8]
    raw = int.from_bytes(digest, "big", signed=False)
    return raw % _MERSENNE_PRIME


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
    feature_set = set(features)
    if not feature_set:
        return np.full(num_perm, np.iinfo(np.int64).max, dtype=np.int64)

    # One SHA-256 per unique feature (Python-level but fast: ~1 us).
    base_hashes = np.array(
        [_base_hash(f) for f in feature_set],
        dtype=np.int64,
    )  # shape: (|features|,)

    a_vec, b_vec = _permutation_coefficients(seed, num_perm)

    # Broadcast: (|features|, 1) * (1, num_perm) + (1, num_perm) mod p
    # -> (|features|, num_perm) int64 grid of per-(feature, perm) hashes.
    # All arithmetic stays within int64 because _MERSENNE_PRIME < 2^62
    # and ``a, b, base`` are all < p.
    grid = (base_hashes[:, None] * a_vec[None, :] + b_vec[None, :]) % _MERSENNE_PRIME

    # MinHash: for each permutation column, the signature value is
    # the minimum grid entry across all features.
    signature = grid.min(axis=0)
    return signature.astype(np.int64, copy=False)
