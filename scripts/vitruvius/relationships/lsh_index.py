"""Sprint LSH-1 Task 2 — LSH index over MinHash signatures.

Band-based LSH: divide each ``num_perm``-dimensional signature into
``num_bands`` non-overlapping bands of ``num_perm // num_bands`` values
each. Two signatures collide in a band iff their values in that band
are byte-equal. Two signatures collide in the index iff they share at
least one band — which is a sensitivity/specificity knob: more bands =
more recall, fewer bands = more precision.

For ``num_perm=128, num_bands=4`` the classical rule of thumb
(Rajaraman & Ullman, *Mining of Massive Datasets*, Chapter 3, equation
3.2) gives a collision threshold around Jaccard ≈ 0.75 — signatures
above that similarity almost always collide, signatures below that
similarity almost never collide. Tune ``num_bands`` upward for higher
recall, downward for higher precision.

**Language/runtime choice.** Pure-stdlib + numpy Python per AD-037.
Near-duplicate dedup is a cold path (once per ingestion batch), so
the pyo3 FFI overhead + Rust maintenance cost is not justified.
"""
from __future__ import annotations

import hashlib
from collections import defaultdict
from dataclasses import dataclass, field

import numpy as np


@dataclass
class LSHIndex:
    """Band-based LSH index over MinHash signatures.

    Attributes:
        num_perm: Length of each MinHash signature. Must match the
            ``num_perm`` used when computing signatures for ``add`` /
            ``query_candidates``.
        num_bands: Number of non-overlapping bands to split each
            signature into. Must divide ``num_perm`` exactly.
        _buckets: Internal ``(band_index, band_hash_bytes) -> [original_indices]``
            dict. Not part of the public API; exposed as a dataclass
            field so ``replace`` works for testing.
    """

    num_perm: int = 128
    num_bands: int = 4
    _buckets: dict[tuple[int, bytes], list[int]] = field(
        default_factory=lambda: defaultdict(list)
    )

    def __post_init__(self) -> None:
        if self.num_perm % self.num_bands != 0:
            raise ValueError(
                f"num_perm {self.num_perm} must be divisible by "
                f"num_bands {self.num_bands}"
            )
        self._rows_per_band = self.num_perm // self.num_bands

    def _band_keys(self, signature: np.ndarray) -> list[tuple[int, bytes]]:
        """Return the list of ``(band_index, band_hash_bytes)`` keys
        for a given signature. Uses BLAKE2b-128 on the raw band bytes
        so two different ``num_bands``-value slices can never produce
        the same key (unlike a naive ``tobytes()`` comparison which
        can collide across bands at the same index).
        """
        keys: list[tuple[int, bytes]] = []
        for b in range(self.num_bands):
            start = b * self._rows_per_band
            end = start + self._rows_per_band
            band = signature[start:end].tobytes()
            band_hash = hashlib.blake2b(band, digest_size=16).digest()
            keys.append((b, band_hash))
        return keys

    def add(self, *, original_index: int, signature: np.ndarray) -> None:
        """Insert ``signature`` under ``original_index`` into every band
        bucket it hashes to. ``original_index`` is the caller's handle
        back to the full candidate record — the LSH index never
        materializes the candidate itself, only the integer key.
        """
        if signature.shape != (self.num_perm,):
            raise ValueError(
                f"signature shape {signature.shape} does not match "
                f"index num_perm={self.num_perm}"
            )
        for key in self._band_keys(signature):
            self._buckets[key].append(original_index)

    def query_candidates(self, signature: np.ndarray) -> list[int]:
        """Return the sorted unique list of original indices that share
        at least one band with ``signature``.

        The returned list is the *candidate set* for near-duplicate
        detection — callers must still verify each candidate against
        the query signature (typically via exact Jaccard over the
        feature set, or via delegation to the exact-endpoint dedup as
        in :func:`dedupe_by_endpoints_lsh`).
        """
        if signature.shape != (self.num_perm,):
            raise ValueError(
                f"signature shape {signature.shape} does not match "
                f"index num_perm={self.num_perm}"
            )
        seen: set[int] = set()
        for key in self._band_keys(signature):
            for idx in self._buckets.get(key, ()):
                seen.add(idx)
        return sorted(seen)
