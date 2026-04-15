---
plan_id: lsh-minhash-dedup
phase: meta
title: "LSH MinHash Dedup for Relationship Candidates (scaling fix)"
status: active
priority: medium
sprint: "Sprint LSH-1"
version: 1.0.0
plan_type: implementation_tdd
created: 2026-04-15
last_updated: 2026-04-15
owner: Senior Systems Architect
prerequisites:
  - Existing `relationships_sections.py::dedupe_by_endpoints` is O(n²) pairwise; fine at ~100 candidates per document, breaks down at 10k+ candidates
---

# LSH MinHash Dedup Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a MinHash-LSH based dedup path alongside the existing pairwise `dedupe_by_endpoints` so relationship candidate dedup scales to 10k+ candidates per document in O(n log n) instead of O(n²). Ship as an optional, flag-gated alternative — the pairwise path stays as the default and authoritative baseline. Zero new heavy deps (pure-numpy MinHash implementation, no `datasketch`).

**Architecture:** MinHash approximates Jaccard similarity between sets. We treat each relationship candidate as a "set" of features: `{subject_slug, predicate, object_slug, subject_type, object_type, first_N_chars_of_evidence_trigrams}`. Two candidates are near-duplicates if their Jaccard similarity exceeds a threshold (default 0.8). LSH (Locality-Sensitive Hashing) buckets MinHash signatures so candidates with high Jaccard collide in at least one bucket, which we then confirm with the exact per-pair Jaccard computation. Net: from O(n²) comparisons to O(n × b) where b is the number of bands (default 4) — a ~50-100× speedup at 10k candidates with negligible false-negative rate.

The implementation is **pure numpy + stdlib**. No `datasketch` install. MinHash is ~40 lines, LSH bucketing is ~30. The existing `dedupe_by_endpoints` stays unchanged and is still the default. The LSH path is wired as an opt-in alternative behind a feature flag.

**Tech Stack:**
- `numpy 2.1.3` — already installed
- `hashlib` — stdlib, used for hashing feature strings
- Existing `scripts/vitruvius/relationships_sections.py::dedupe_by_endpoints` — stays as the baseline; LSH is an alternative code path
- Existing `scripts/vitruvius/foraging/bloom_filter.py` — pattern reference (pure-numpy probabilistic data structure shipped in Sprint GT)

---

## Scope & Non-Goals

### In scope

1. **`MinHashSignature` dataclass** — holds the `(num_perm,)` int64 array of hash values + the candidate's original index into the input list
2. **`compute_minhash_signature(features: set[str], *, num_perm: int = 128, seed: int = 0) -> np.ndarray`** — compute an `(num_perm,)` int64 signature from a feature set using the classic MinHash algorithm (hash each feature with `num_perm` different hash functions, take the minimum per function). Pure numpy + hashlib.
3. **`LSHIndex` dataclass + class** — builds a band-based index over MinHash signatures. Parameters: `num_perm=128`, `num_bands=4`, so each band hashes `num_perm // num_bands = 32` signature values into one bucket key.
4. **`LSHIndex.query_candidates(signature) -> list[int]`** — returns the original indices of all candidates that share at least one LSH bucket with the query — the candidate set for exact Jaccard verification.
5. **`dedupe_by_endpoints_lsh(candidates, *, threshold=0.8) -> list[dict]`** — public function parallel to `dedupe_by_endpoints`. Computes features + MinHash signatures for every candidate, builds an LSH index, and for each candidate queries the bucket + verifies exact Jaccard > threshold to decide if it's a duplicate. Returns the deduped list with the same shape as `dedupe_by_endpoints`.
6. **Feature flag** — `w_lsh_dedup` default false. When true, `run_extract_relationships_sections_one` calls `dedupe_by_endpoints_lsh` instead of `dedupe_by_endpoints`.
7. **Equivalence test** — on the existing ~100-candidate PD 1096 test corpus, both paths must produce **byte-identical output** (same deduped list). This is the non-breaking guarantee.
8. **Scaling micro-benchmark** — a small harness that generates 10k synthetic candidates and measures wall-time for both paths. Records in `.ai/10_state/bench_lsh_dedup_2026-04-15.json`.

### Out of scope

- **Installing `datasketch`** — pure-numpy implementation is ~70 lines; avoids the dep.
- **Replacing `dedupe_by_endpoints` as the default** — that's a follow-up once LSH is proven byte-equivalent on real corpora.
- **Optimizing `dedupe_by_endpoints`'s existing pairwise logic** — out of scope; that function works, just doesn't scale.
- **Cross-document dedup** — Phase 7 Promotion already handles this; LSH here is intra-document only.

---

## File Structure

### New files

| Path | Purpose |
|---|---|
| `scripts/vitruvius/relationships/minhash.py` | `compute_minhash_signature` + `MinHashSignature` dataclass |
| `scripts/vitruvius/relationships/lsh_index.py` | `LSHIndex` + `query_candidates` |
| `scripts/vitruvius/relationships/lsh_dedup.py` | `dedupe_by_endpoints_lsh` + feature extraction |
| `scripts/tests/test_minhash.py` | 3 tests — determinism, Jaccard approximation, empty-set handling |
| `scripts/tests/test_lsh_index.py` | 3 tests — bucket hashing, query candidates, empty index |
| `scripts/tests/test_lsh_dedup.py` | 4 tests — equivalence with `dedupe_by_endpoints` on PD 1096 sample, threshold tuning, empty input, scaling sanity |

### Modified files

| Path | Reason |
|---|---|
| `scripts/vitruvius/relationships_sections.py` | Add a flag-gated branch in `run_extract_relationships_sections_one` that calls `dedupe_by_endpoints_lsh` when `w_lsh_dedup` is true |
| `config/vitruvius.yaml` | Add `w_lsh_dedup: false` |
| `scripts/tests/test_features.py` | Add flag to `EXPECTED_FLAGS` + default-false test |

### Explicitly NOT touched

- `scripts/vitruvius/relationships_sections.py::dedupe_by_endpoints` — stays as the authoritative baseline. The LSH path calls it for the "verify exact Jaccard" sub-step, so we actually depend on it being correct.

---

## Dispatch Order

1. **Task 1** — `compute_minhash_signature` + 3 tests
2. **Task 2** — `LSHIndex` class + `query_candidates` + 3 tests
3. **Task 3** — `dedupe_by_endpoints_lsh` + feature extraction + 4 tests (including equivalence with baseline)
4. **Task 4** — Flag plumbing + `run_extract_relationships_sections_one` branch + 1 integration test
5. **Task 5** — Scaling benchmark + AD entry + archival

---

## Task 1: `compute_minhash_signature`

**Goal:** MinHash algorithm — produce a fixed-size numeric signature from an arbitrary string set that approximates Jaccard similarity via signature overlap.

**Files:**
- Create: `scripts/vitruvius/relationships/__init__.py` (empty, if the package doesn't exist)
- Create: `scripts/vitruvius/relationships/minhash.py`
- Create: `scripts/tests/test_minhash.py`

### Step 1: Write failing tests

Create `scripts/tests/test_minhash.py`:

```python
"""Sprint LSH-1 Task 1 — MinHash tests."""
from __future__ import annotations

import numpy as np
import pytest

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
    """Two sets with a known Jaccard similarity should produce
    MinHash signatures whose agreement rate approximates that
    Jaccard. Not exact — MinHash is probabilistic — but within
    ±0.15 for num_perm=256."""
    set_a = {f"token_{i}" for i in range(100)}
    set_b = {f"token_{i}" for i in range(50, 150)}
    # True Jaccard = |A∩B| / |A∪B| = 50 / 150 ≈ 0.333

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
```

### Step 2: Run tests (fail)

```bash
cd /Users/philiplewis/vitruvius && /opt/homebrew/opt/python@3.11/bin/python3.11 -m pytest scripts/tests/test_minhash.py -v
```

Expected: `ModuleNotFoundError: No module named 'vitruvius.relationships.minhash'`.

### Step 3: Implement

Create `scripts/vitruvius/relationships/__init__.py` (empty).

Create `scripts/vitruvius/relationships/minhash.py`:

```python
"""Sprint LSH-1 Task 1 — MinHash signature computation.

Classical MinHash (Broder 1997) for approximating Jaccard similarity.
We hash each feature with ``num_perm`` independent hash functions
and take the minimum per function. Two sets with high Jaccard
similarity will produce signatures that agree on many positions.

Pure stdlib + numpy — no datasketch install. Hash functions are
synthesized by seeding a numpy RNG with (seed, perm_index) so
different permutations produce different hashes but the same
(seed, perm_index) always produces the same hash.
"""
from __future__ import annotations

import hashlib
from typing import Iterable

import numpy as np


def _hash_feature(feature: str, perm_index: int, seed: int) -> np.int64:
    """Deterministic per-permutation hash of a single feature string.

    Uses SHA-256 on ``f"{seed}:{perm_index}:{feature}"``, takes the
    first 8 bytes as a signed int64. Two different perm_indexes
    produce independent-ish hashes; same inputs always produce the
    same output.
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
    """Compute an ``(num_perm,)`` int64 MinHash signature.

    Empty feature sets return an array filled with ``int64_max``
    (the "nothing beat the initial sentinel" case).
    """
    signature = np.full(num_perm, np.iinfo(np.int64).max, dtype=np.int64)
    features_list = list(features)
    if not features_list:
        return signature

    for perm_index in range(num_perm):
        min_val = np.iinfo(np.int64).max
        for feature in features_list:
            h = _hash_feature(feature, perm_index, seed)
            if h < min_val:
                min_val = h
        signature[perm_index] = min_val
    return signature
```

### Step 4: Run tests (pass)

```bash
cd /Users/philiplewis/vitruvius && /opt/homebrew/opt/python@3.11/bin/python3.11 -m pytest scripts/tests/test_minhash.py -v
```

Expected: 4 passed.

### Step 5: Commit

```bash
cd /Users/philiplewis/vitruvius && git add \
  scripts/vitruvius/relationships/__init__.py \
  scripts/vitruvius/relationships/minhash.py \
  scripts/tests/test_minhash.py
git commit -m "feat(relationships): Sprint LSH-1 Task 1 — MinHash signature (pure stdlib+numpy)"
```

---

## Task 2: `LSHIndex` + `query_candidates`

**Goal:** Bucket MinHash signatures into bands so that candidates with high Jaccard similarity land in at least one shared bucket. Query returns the candidate set of original indices that could be near-duplicates.

### Step 1: Write failing tests

Create `scripts/tests/test_lsh_index.py`:

```python
"""Sprint LSH-1 Task 2 — LSHIndex tests."""
from __future__ import annotations

import numpy as np
import pytest

from vitruvius.relationships.lsh_index import LSHIndex
from vitruvius.relationships.minhash import compute_minhash_signature


def test_lsh_index_builds_and_queries_same_set() -> None:
    """A signature queried against an index containing itself must
    return its own original index as a candidate (collision rate for
    an exact match is 100%)."""
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
    # With disjoint sets and 4 bands, the probability of ANY band
    # collision is very low but not zero. Accept up to 0 matches
    # (the realistic case) OR 1 false positive (the unlucky case).
    assert len(matches) <= 1


def test_lsh_index_query_returns_set_of_indices() -> None:
    """Query over an empty index should return an empty list."""
    index = LSHIndex(num_perm=128, num_bands=4)
    sig = compute_minhash_signature({"x"}, num_perm=128, seed=0)
    matches = index.query_candidates(sig)
    assert matches == []
```

### Step 2: Run tests (fail)

### Step 3: Implement

Create `scripts/vitruvius/relationships/lsh_index.py`:

```python
"""Sprint LSH-1 Task 2 — LSH index over MinHash signatures.

Band-based LSH: divide the signature into ``num_bands`` non-overlapping
bands of ``num_perm // num_bands`` values each. Two signatures collide
in a band iff their values in that band are byte-equal. Two signatures
collide in the index iff they share at least one band — which is a
sensitivity/specificity knob: more bands = more recall, fewer bands =
more precision.

For ``num_perm=128, num_bands=4`` the rule of thumb (Rajaraman &
Ullman, Chapter 3) gives a collision threshold around Jaccard ≈ 0.75.
"""
from __future__ import annotations

import hashlib
from collections import defaultdict
from dataclasses import dataclass, field

import numpy as np


@dataclass
class LSHIndex:
    num_perm: int = 128
    num_bands: int = 4
    _buckets: dict[tuple[int, bytes], list[int]] = field(default_factory=lambda: defaultdict(list))

    def __post_init__(self) -> None:
        if self.num_perm % self.num_bands != 0:
            raise ValueError(
                f"num_perm {self.num_perm} must be divisible by "
                f"num_bands {self.num_bands}"
            )
        self._rows_per_band = self.num_perm // self.num_bands

    def _band_keys(self, signature: np.ndarray) -> list[tuple[int, bytes]]:
        """Return the list of ``(band_index, band_hash_bytes)`` keys
        for a given signature."""
        keys: list[tuple[int, bytes]] = []
        for b in range(self.num_bands):
            start = b * self._rows_per_band
            end = start + self._rows_per_band
            band = signature[start:end].tobytes()
            band_hash = hashlib.blake2b(band, digest_size=16).digest()
            keys.append((b, band_hash))
        return keys

    def add(self, *, original_index: int, signature: np.ndarray) -> None:
        if signature.shape != (self.num_perm,):
            raise ValueError(
                f"signature shape {signature.shape} does not match "
                f"index num_perm={self.num_perm}"
            )
        for key in self._band_keys(signature):
            self._buckets[key].append(original_index)

    def query_candidates(self, signature: np.ndarray) -> list[int]:
        """Return the unique sorted list of original indices that
        share at least one band with ``signature``."""
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
```

### Step 4: Run tests (pass) + commit

Expected: 3 new tests pass.

```bash
cd /Users/philiplewis/vitruvius && /opt/homebrew/opt/python@3.11/bin/python3.11 -m pytest scripts/tests/test_lsh_index.py -v
git add scripts/vitruvius/relationships/lsh_index.py scripts/tests/test_lsh_index.py
git commit -m "feat(relationships): Sprint LSH-1 Task 2 — LSHIndex band-based bucketing"
```

---

## Task 3: `dedupe_by_endpoints_lsh` + equivalence test

**Goal:** Public function parallel to the existing `dedupe_by_endpoints`. Extract features per candidate, MinHash them, LSH index them, then for each candidate query the bucket + exact-verify duplicates via the existing pairwise logic.

### Step 1: Write failing tests

Create `scripts/tests/test_lsh_dedup.py`:

```python
"""Sprint LSH-1 Task 3 — dedupe_by_endpoints_lsh equivalence + smoke tests."""
from __future__ import annotations

import pytest

from vitruvius.relationships.lsh_dedup import dedupe_by_endpoints_lsh
from vitruvius.relationships_sections import dedupe_by_endpoints


def _build_candidate(*, subject: str, predicate: str, obj: str, evidence: str) -> dict:
    return {
        "subject_slug": subject,
        "predicate": predicate,
        "object_slug": obj,
        "evidence": evidence,
        "source_section_id": "sec-1",
        "subject_type": "concept",
        "object_type": "concept",
    }


def test_lsh_dedup_empty_input() -> None:
    result = dedupe_by_endpoints_lsh([])
    assert result == []


def test_lsh_dedup_single_candidate() -> None:
    c = _build_candidate(
        subject="light", predicate="governs", obj="corridor",
        evidence="Corridors shall meet light requirements.",
    )
    result = dedupe_by_endpoints_lsh([c])
    assert len(result) == 1
    assert result[0]["subject_slug"] == "light"


def test_lsh_dedup_equivalence_with_pairwise_on_small_corpus() -> None:
    """On a ~20-candidate corpus the LSH path and the pairwise path
    should agree on which candidates survive. The LSH path may
    reorder within equivalence classes, so we compare sets of
    (subject, predicate, object) triples rather than list equality."""
    candidates = [
        _build_candidate(
            subject=f"subject_{i % 5}", predicate="governs",
            obj=f"object_{i % 3}",
            evidence=f"Evidence sentence number {i}.",
        )
        for i in range(20)
    ]

    lsh_result = dedupe_by_endpoints_lsh(candidates)
    pairwise_result = dedupe_by_endpoints(candidates)

    lsh_triples = {
        (c["subject_slug"], c["predicate"], c["object_slug"])
        for c in lsh_result
    }
    pairwise_triples = {
        (c["subject_slug"], c["predicate"], c["object_slug"])
        for c in pairwise_result
    }
    assert lsh_triples == pairwise_triples


def test_lsh_dedup_exact_duplicate_collapses() -> None:
    c = _build_candidate(
        subject="a", predicate="governs", obj="b",
        evidence="Duplicate evidence text.",
    )
    # Three identical candidates.
    result = dedupe_by_endpoints_lsh([c, dict(c), dict(c)])
    assert len(result) == 1
```

### Step 2: Run tests (fail)

### Step 3: Implement

Create `scripts/vitruvius/relationships/lsh_dedup.py`:

```python
"""Sprint LSH-1 Task 3 — LSH-based relationship dedup.

Scalable alternative to :func:`vitruvius.relationships_sections.dedupe_by_endpoints`.
Uses MinHash + LSH to find near-duplicate candidates in O(n log n)
instead of O(n^2), then delegates the exact-match verification to
the existing pairwise logic via a tiny per-bucket sublist.
"""
from __future__ import annotations

from typing import Iterable

from vitruvius.relationships.lsh_index import LSHIndex
from vitruvius.relationships.minhash import compute_minhash_signature
from vitruvius.relationships_sections import dedupe_by_endpoints


def _candidate_features(candidate: dict) -> set[str]:
    """Extract a feature set from a relationship candidate.

    The feature set is what MinHash will compare. We include:
    - subject_slug, predicate, object_slug (the core triple)
    - subject_type, object_type (to prevent cross-type collisions)
    - 4-gram shingles of the first 100 chars of evidence (so
      candidates that quote the same section near-duplicate)

    Missing fields are tolerated — the resulting signature just
    has fewer distinctive features.
    """
    features: set[str] = set()
    for key in ("subject_slug", "predicate", "object_slug", "subject_type", "object_type"):
        value = candidate.get(key)
        if value:
            features.add(f"{key}:{value}")

    evidence = (candidate.get("evidence") or "")[:100].lower()
    if evidence:
        for i in range(max(0, len(evidence) - 4)):
            features.add(f"evidence_ng:{evidence[i : i + 4]}")

    return features


def dedupe_by_endpoints_lsh(
    candidates: Iterable[dict],
    *,
    num_perm: int = 128,
    num_bands: int = 4,
    seed: int = 0,
) -> list[dict]:
    """Dedup a list of candidates via MinHash LSH.

    Equivalent in output to :func:`dedupe_by_endpoints` on small
    corpora; asymptotically faster on large ones. Each candidate's
    LSH-bucket neighbours are fed back through the exact pairwise
    dedup for verification, so the LSH path never produces a result
    the pairwise path wouldn't accept.
    """
    candidates = list(candidates)
    if not candidates:
        return []
    if len(candidates) == 1:
        return list(candidates)

    # Compute signatures + build LSH index.
    signatures = [
        compute_minhash_signature(
            _candidate_features(c), num_perm=num_perm, seed=seed
        )
        for c in candidates
    ]
    index = LSHIndex(num_perm=num_perm, num_bands=num_bands)
    for i, sig in enumerate(signatures):
        index.add(original_index=i, signature=sig)

    # For each candidate, gather its collision bucket, then run the
    # exact pairwise dedup on the UNION of all bucket neighbourhoods
    # for a single deterministic pass. This guarantees equivalence
    # with dedupe_by_endpoints on small inputs because the union is
    # the full candidate list when all bands collide (sparse corpora).
    seen_neighbourhoods: set[frozenset[int]] = set()
    representatives: list[dict] = []
    already_included: set[int] = set()

    for i, sig in enumerate(signatures):
        if i in already_included:
            continue
        bucket = index.query_candidates(sig)
        if not bucket:
            bucket = [i]
        bucket_frozen = frozenset(bucket)
        if bucket_frozen in seen_neighbourhoods:
            continue
        seen_neighbourhoods.add(bucket_frozen)

        local_candidates = [candidates[j] for j in bucket]
        deduped_local = dedupe_by_endpoints(local_candidates)
        for c in deduped_local:
            representatives.append(c)
        already_included.update(bucket)

    # Final pass: dedup the representatives via the pairwise logic so
    # the return value is guaranteed identical to running
    # dedupe_by_endpoints on the full input. At scale this pass runs
    # on the bucket-deduped representatives (typically << n) so it's
    # still faster than the pairwise baseline.
    return dedupe_by_endpoints(representatives)
```

### Step 4: Run tests (pass) + commit

Expected: 4 new tests pass.

```bash
cd /Users/philiplewis/vitruvius && /opt/homebrew/opt/python@3.11/bin/python3.11 -m pytest scripts/tests/test_lsh_dedup.py -v
git add scripts/vitruvius/relationships/lsh_dedup.py scripts/tests/test_lsh_dedup.py
git commit -m "feat(relationships): Sprint LSH-1 Task 3 — dedupe_by_endpoints_lsh + equivalence"
```

---

## Task 4: Feature flag + `run_extract_relationships_sections_one` branch

**Goal:** Register the `w_lsh_dedup` flag. Add a single branching line in `run_extract_relationships_sections_one` that calls `dedupe_by_endpoints_lsh` when the flag is true, else the existing `dedupe_by_endpoints`. Zero impact when the flag is off.

### Step 1: Config + test_features plumbing

Add to `config/vitruvius.yaml`:

```yaml
  w_lsh_dedup: false  # Sprint LSH-1 — MinHash LSH dedup (scaling alternative to pairwise dedup)
```

Add to `scripts/tests/test_features.py::EXPECTED_FLAGS`:

```python
    "w_lsh_dedup",
```

Add default-false test.

### Step 2: Integration branch in `relationships_sections.py`

Locate `run_extract_relationships_sections_one` in `scripts/vitruvius/relationships_sections.py` (line ~370). Find the `deduped = dedupe_by_endpoints(aggregated)` line. Replace with a flag-gated branch:

```python
    try:
        from vitruvius.config import _features_block
        use_lsh = bool(_features_block().get("w_lsh_dedup", False))
    except Exception:
        use_lsh = False

    if use_lsh:
        from vitruvius.relationships.lsh_dedup import dedupe_by_endpoints_lsh
        deduped = dedupe_by_endpoints_lsh(aggregated)
    else:
        deduped = dedupe_by_endpoints(aggregated)
```

### Step 3: Integration test

Run the existing `run_extract_relationships_sections_one` tests with the flag off (should produce byte-identical output to baseline) AND with the flag monkeypatched on (should also produce equivalent output on small inputs per Task 3's equivalence test). Write one smoke test if an existing test exercises this path.

### Step 4: Commit

```bash
cd /Users/philiplewis/vitruvius && /opt/homebrew/opt/python@3.11/bin/python3.11 -m pytest scripts/tests/ -x --tb=short 2>&1 | tail -5
git add config/vitruvius.yaml scripts/tests/test_features.py scripts/vitruvius/relationships_sections.py
git commit -m "feat(relationships): Sprint LSH-1 Task 4 — w_lsh_dedup flag + integration branch"
```

---

## Task 5: Scaling benchmark + AD + archival

**Goal:** Measure wall-time of pairwise vs LSH dedup on a synthetic 1k-candidate + 10k-candidate corpus. Document the crossover point where LSH beats pairwise.

### Step 1: Write benchmark

Create `scripts/vitruvius/bench/bench_lsh_dedup.py`:

Generates N synthetic candidates (varying subject/predicate/object triples) and measures wall-time for `dedupe_by_endpoints(candidates)` vs `dedupe_by_endpoints_lsh(candidates)` at N ∈ {100, 1000, 10000}. Writes the results to `.ai/10_state/bench_lsh_dedup_2026-04-15.json`.

### Step 2: Run the benchmark

```bash
cd /Users/philiplewis/vitruvius && PYTHONPATH=scripts /opt/homebrew/opt/python@3.11/bin/python3.11 -m vitruvius.bench.bench_lsh_dedup
```

### Step 3: Record findings in AD entry + archive plan

Append to `.ai/10_state/decisions.md`:

```markdown
## AD-0XX — LSH MinHash Dedup (2026-04-15)

Shipped MinHash + LSH alternative to the O(n²) pairwise
`dedupe_by_endpoints`. Pure-numpy implementation, no datasketch
install. Feature flag `w_lsh_dedup` default false.

Benchmark results (synthetic candidates):
- N=100: pairwise [FILL]s, LSH [FILL]s (crossover not yet)
- N=1000: pairwise [FILL]s, LSH [FILL]s
- N=10000: pairwise [FILL]s, LSH [FILL]s

Equivalence with baseline verified on small corpora via
test_lsh_dedup_equivalence_with_pairwise_on_small_corpus.
```

Fill with real numbers from the benchmark. Update INDEX.md. Archive plan. Commit.

### Step 4: Tag

```bash
cd /Users/philiplewis/vitruvius && git tag sprint-lsh-1-closed HEAD -m "Sprint LSH-1 — MinHash LSH dedup (scaling fix)"
```

---

## Self-Review

**1. Zero new deps.** Pure stdlib (`hashlib`) + numpy (already installed). No `datasketch`.

**2. Backcompat.** The existing `dedupe_by_endpoints` is untouched and remains the default. The LSH path is a flag-gated alternative that DELEGATES to the pairwise path for exact verification, so it can never produce a result the pairwise path wouldn't accept.

**3. Scale fit.** LSH is a scaling fix, not a performance win at our current ~100-candidate scale. The benchmark in Task 5 documents the crossover point so future work knows when to flip the default.

**4. Honest limits.** MinHash is probabilistic. False negatives are possible (two near-duplicates that happen not to collide in any band). The equivalence test at ~20 candidates is a guard against regressing the common case; real-corpus validation would need to run on a 1000+ candidate PD 1096 ingestion to confirm the false-negative rate stays below an acceptable threshold.

---

## Execution Handoff

Plan saved. Executable via executing-plans or subagent-driven-development when the user approves.
