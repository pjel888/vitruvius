---
plan_id: graphsage-pq-embeddings
phase: meta
title: "Product Quantization for GraphSAGE Embeddings (low-spec disk win)"
status: active
priority: medium
sprint: "Sprint PQ-1"
version: 1.0.0
plan_type: implementation_tdd
created: 2026-04-15
last_updated: 2026-04-15
owner: Senior Systems Architect
prerequisites:
  - Sprint HP closed (tag `sprint-hp-closed`) — HP.5 GraphSAGE embeddings shipped at 64-dim float32
  - numpy installed (verified at plan-write time — numpy 2.1.3)
related_plans:
  - ../09_archive/plans/phase-13-high-performance-optimizations-plan.md (Sprint HP parent)
---

# Product Quantization for GraphSAGE Embeddings Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a Product Quantization (PQ) compressor alongside the existing `compute_graphsage_embeddings` function so 64-dim float32 embeddings (256 bytes/node) can be stored and retrieved as 8-byte PQ codes (**32× compression**) with negligible retrieval accuracy loss. Ship as a pure-numpy implementation with zero new pip dependencies — this is a low-spec disk win that costs nothing at runtime.

**Architecture:** PQ is a classical vector-quantization technique (Jégou, Douze, Schmid 2010) that splits an N-dim vector into M sub-vectors of N/M dims each, then learns k centroids per sub-vector (k-means per subspace) and stores each sub-vector as a single byte (the index of its nearest centroid). For our 64-d float32 embeddings with M=8 sub-quantizers × k=256 centroids, each embedding compresses from **256 bytes → 8 bytes (32×)**. Distance queries between two PQ codes use asymmetric distance computation (ADC): look up pre-computed distances from a query sub-vector to each centroid, sum across M sub-vectors. At our scale (≤10k nodes) this is O(M × k) per query = O(2048) ops — microseconds.

Pure-numpy implementation. No FAISS, no scikit-learn, no new installs. The existing GraphSAGE `float32` embeddings stay as the authoritative source; PQ codes are a parallel compressed representation that callers opt into via a new `encode_to_pq` / `decode_from_pq` / `adc_distance` API.

**Tech Stack:**
- `numpy 2.1.3` — already installed
- Existing `scripts/vitruvius/graph/graphsage.py::GraphSAGEReport` — the source of embeddings to compress
- Existing `scripts/vitruvius/graph/mc_dropout.py` — stdlib pattern to follow (numpy-optional minimal utility)

---

## Scope & Non-Goals

### In scope

1. **`PQCodebook` frozen dataclass** — holds the learned M sub-quantizer centroids (a numpy array of shape `(M, k, sub_dim)` float32) + the sub-dim + the num sub-vectors M + the number of centroids k. Serializable to/from a single `.npz` file via `numpy.savez_compressed` / `numpy.load`.
2. **`train_pq_codebook(embeddings, *, M=8, k=256, n_iter=25, seed=0) -> PQCodebook`** — runs k-means on each of M sub-vector subspaces. Pure numpy k-means (no scikit-learn). Deterministic under the seed.
3. **`encode_to_pq(embeddings, codebook) -> np.ndarray[uint8]`** — quantizes a batch of embeddings to their PQ codes. Input shape `(N, dim)`, output shape `(N, M)` where each entry is a uint8 centroid index.
4. **`decode_from_pq(codes, codebook) -> np.ndarray[float32]`** — reconstructs approximate embeddings from codes by concatenating the selected centroids. Lossy but close.
5. **`adc_distance(query, codes, codebook) -> np.ndarray[float32]`** — asymmetric distance computation: pre-compute the squared distance from a query vector's sub-vectors to each of the M × k centroids, then sum per code. Output is the approximate squared L2 distance from `query` to each row of `codes`. Much faster than `decode_from_pq` + distance.
6. **`save_codebook(codebook, path)` / `load_codebook(path) -> PQCodebook`** — persistence helpers using `numpy.savez_compressed`.
7. **Integration helper** — `compress_graphsage_report(report, *, M=8, k=256, seed=0) -> tuple[PQCodebook, np.ndarray, list[str]]` — convenience function that takes a `GraphSAGEReport` from `graphsage.py`, trains a codebook, encodes every embedding, and returns `(codebook, codes, node_ids)` so callers can persist the compressed form in one call.
8. **Reconstruction-error benchmark** — a simple measurement of `|original - decoded| / |original|` average across the synthetic graph used in GraphSAGE tests. Documented in `.ai/10_state/bench_pq_reconstruction_2026-04-15.json` as an evidence artifact (not a decision gate — PQ compression is unconditional, the benchmark records the measured quality).
9. **Feature flag** — `hp_graphsage_pq` default false. Deployment-readiness marker. When flipped on, callers that persist embeddings should serialize to PQ instead of raw float32.
10. **Docs + AD-034 (or whatever number lands next)** — record the compression ratio, the measured reconstruction error, and the follow-up plan to wire PQ into the embedding persistence layer.

### Out of scope

- **Optimized PQ (OPQ)** — an improvement that rotates the embedding space before quantization for better accuracy. Worth revisiting if plain PQ's reconstruction error is unacceptable on real embeddings, but premature for Tranche 1 of this plan.
- **Inverted file indexes (IVFPQ)** — retrieval-time index for billion-scale corpora. We have ~10k nodes max; a linear scan of `adc_distance` across all codes is fast enough.
- **GPU acceleration** — numpy on CPU is sufficient at current scale and fits the low-spec target better than any GPU path.
- **Wiring PQ into the existing GraphSAGE persistence** — no persistence layer exists today; embeddings are computed on-demand in memory. Persistence is a follow-up plan.
- **Using sklearn's `MiniBatchKMeans`** — avoided to preserve the zero-new-dep constraint. Pure-numpy k-means is 40 lines.

---

## File Structure

### New files

| Path | Purpose |
|---|---|
| `scripts/vitruvius/graph/pq_codebook.py` | `PQCodebook` dataclass + `train_pq_codebook` + `encode_to_pq` + `decode_from_pq` + `adc_distance` + `save_codebook` + `load_codebook` |
| `scripts/vitruvius/graph/graphsage_pq.py` | `compress_graphsage_report` integration helper |
| `scripts/tests/test_pq_codebook.py` | 6 tests — training, encoding, decoding, ADC, save/load roundtrip, reconstruction error |
| `scripts/tests/test_graphsage_pq.py` | 2 tests — integration with `GraphSAGEReport`, empty-graph handling |
| `.ai/10_state/bench_pq_reconstruction_2026-04-15.json` | Measured reconstruction error on the synthetic GraphSAGE corpus |

### Modified files

| Path | Reason |
|---|---|
| `config/vitruvius.yaml` | Add `hp_graphsage_pq: false` |
| `scripts/tests/test_features.py` | Add flag to `EXPECTED_FLAGS` + default-false test |
| `.ai/10_state/decisions.md` | Append AD entry with compression ratio + reconstruction error numbers |
| `.ai/03_plans/INDEX.md` | Add row for this plan |

### Explicitly NOT touched

- `scripts/vitruvius/graph/graphsage.py` — stays as the source of truth for embedding computation. The PQ compressor is a *consumer*, not a replacement.
- `scripts/vitruvius/graph/rocksdb_event_store.py` — PQ storage doesn't go through the event store. Persistence is a follow-up plan.

---

## Dispatch Order

1. **Task 1** — `PQCodebook` dataclass + `train_pq_codebook` + 2 tests
2. **Task 2** — `encode_to_pq` + `decode_from_pq` + 2 tests
3. **Task 3** — `adc_distance` + 1 test
4. **Task 4** — `save_codebook` / `load_codebook` + 1 test
5. **Task 5** — `compress_graphsage_report` integration helper + 2 tests
6. **Task 6** — Reconstruction-error benchmark + `.json` output + feature flag + AD entry + plan archival

---

## Task 1: `PQCodebook` + `train_pq_codebook`

**Goal:** Learn M sub-quantizer codebooks via pure-numpy k-means. Deterministic under a seed.

**Files:**
- Create: `scripts/vitruvius/graph/pq_codebook.py`
- Create: `scripts/tests/test_pq_codebook.py`

### Step 1: Write failing tests

Create `scripts/tests/test_pq_codebook.py`:

```python
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
```

### Step 2: Run tests (fail)

```bash
cd /Users/philiplewis/vitruvius && /opt/homebrew/opt/python@3.11/bin/python3.11 -m pytest scripts/tests/test_pq_codebook.py -v
```

Expected: `ModuleNotFoundError: No module named 'vitruvius.graph.pq_codebook'`.

### Step 3: Implement `PQCodebook` + `train_pq_codebook`

Create `scripts/vitruvius/graph/pq_codebook.py`:

```python
"""Sprint PQ-1 Task 1 — Product Quantization codebook.

Classical PQ (Jégou, Douze, Schmid 2010) for compressing float32
embeddings into uint8 codes. Pure-numpy implementation — no scikit-learn,
no FAISS, no new installs. See the plan at
.ai/03_plans/2026-04-15-graphsage-pq-embeddings-plan.md for
architectural context.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

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
    """Pure-numpy k-means. Returns (k, d) centroids as float32."""
    n, d = points.shape
    # Initialize centroids by sampling without replacement if possible.
    if n <= k:
        centroids = np.zeros((k, d), dtype=np.float32)
        centroids[:n] = points
        # Pad with zero centroids (these won't win any assignments in
        # the degenerate case n <= k).
        return centroids
    idx = rng.choice(n, size=k, replace=False)
    centroids = points[idx].astype(np.float32, copy=True)

    for _ in range(n_iter):
        # Assign each point to the nearest centroid.
        # Squared L2 distances: (n, k) = ||p||^2 - 2 p·c + ||c||^2
        p_sq = np.sum(points * points, axis=1, keepdims=True)  # (n, 1)
        c_sq = np.sum(centroids * centroids, axis=1, keepdims=True).T  # (1, k)
        cross = points @ centroids.T  # (n, k)
        dist = p_sq - 2.0 * cross + c_sq
        labels = np.argmin(dist, axis=1)  # (n,)

        # Update centroids to the mean of their assigned points.
        new_centroids = np.zeros_like(centroids)
        counts = np.zeros(k, dtype=np.int64)
        np.add.at(new_centroids, labels, points)
        np.add.at(counts, labels, 1)
        nonzero = counts > 0
        new_centroids[nonzero] /= counts[nonzero, None]
        # Empty clusters keep their previous centroid to avoid NaNs.
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

    ``embeddings`` must be a ``(N, dim)`` float32 array where
    ``dim`` is divisible by ``M``. Runs k-means with ``k`` centroids
    on each of ``M`` non-overlapping sub-spaces. Deterministic under
    ``seed``.
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
        sub = embeddings[:, m * sub_dim : (m + 1) * sub_dim].astype(np.float32, copy=False)
        centroids[m] = _kmeans(sub, k=k, n_iter=n_iter, rng=rng)

    return PQCodebook(
        centroids=centroids,
        M=M,
        k=k,
        sub_dim=sub_dim,
    )
```

### Step 4: Run tests (pass)

```bash
cd /Users/philiplewis/vitruvius && /opt/homebrew/opt/python@3.11/bin/python3.11 -m pytest scripts/tests/test_pq_codebook.py -v
```

Expected: 4 passed.

### Step 5: Commit

```bash
cd /Users/philiplewis/vitruvius && git add \
  scripts/vitruvius/graph/pq_codebook.py \
  scripts/tests/test_pq_codebook.py
git commit -m "feat(graph): Sprint PQ-1 Task 1 — PQCodebook + train_pq_codebook (pure numpy)"
```

---

## Task 2: `encode_to_pq` + `decode_from_pq`

**Goal:** Quantize embeddings to 8-byte codes and reconstruct approximate vectors from codes.

### Step 1: Append failing tests to `test_pq_codebook.py`

```python
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

    from vitruvius.graph.pq_codebook import encode_to_pq, decode_from_pq

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
```

### Step 2: Run tests (fail)

Expected: `ImportError: cannot import name 'encode_to_pq'`.

### Step 3: Append implementation to `pq_codebook.py`

```python
def encode_to_pq(embeddings: np.ndarray, codebook: PQCodebook) -> np.ndarray:
    """Quantize ``embeddings`` to uint8 PQ codes.

    Input shape: ``(N, M * sub_dim)``. Output shape: ``(N, M)`` uint8.
    Each output byte is the index of the nearest centroid in its
    sub-quantizer.
    """
    n = embeddings.shape[0]
    if embeddings.shape[1] != codebook.M * codebook.sub_dim:
        raise ValueError(
            f"embedding dim {embeddings.shape[1]} does not match codebook "
            f"{codebook.M}*{codebook.sub_dim}={codebook.M * codebook.sub_dim}"
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
```

### Step 4: Run tests (pass)

Expected: 6 passed (4 from Task 1 + 2 new).

### Step 5: Commit

```bash
cd /Users/philiplewis/vitruvius && git add \
  scripts/vitruvius/graph/pq_codebook.py \
  scripts/tests/test_pq_codebook.py
git commit -m "feat(graph): Sprint PQ-1 Task 2 — encode_to_pq + decode_from_pq"
```

---

## Task 3: `adc_distance` (asymmetric distance computation)

**Goal:** Compute approximate squared L2 distance from a query vector to every row of a code table in O(M × k) per query. The ADC trick precomputes distances from the query's sub-vectors to every centroid once, then does an O(M) sum per row.

### Step 1: Append failing test

```python
def test_adc_distance_matches_decoded_approximation() -> None:
    """ADC distance should closely track the L2 distance computed
    against decoded vectors. Not exactly equal (decode rounds to
    centroids in both operands; ADC only rounds in the db operand),
    but within the same order of magnitude."""
    rng = np.random.default_rng(seed=0)
    db = rng.standard_normal((200, 64)).astype(np.float32)
    codebook = train_pq_codebook(db, M=8, k=128, n_iter=25, seed=42)

    from vitruvius.graph.pq_codebook import (
        encode_to_pq,
        decode_from_pq,
        adc_distance,
    )

    codes = encode_to_pq(db, codebook)
    query = rng.standard_normal(64).astype(np.float32)

    # ADC distance
    adc = adc_distance(query, codes, codebook)
    assert adc.shape == (200,)
    assert adc.dtype == np.float32

    # Reference: decoded-vs-query L2
    decoded = decode_from_pq(codes, codebook)
    ref = np.sum((decoded - query) ** 2, axis=1)

    # ADC should match decoded L2 to within numerical error.
    np.testing.assert_allclose(adc, ref, rtol=1e-4, atol=1e-4)
```

### Step 2: Implement `adc_distance`

Append to `pq_codebook.py`:

```python
def adc_distance(
    query: np.ndarray,
    codes: np.ndarray,
    codebook: PQCodebook,
) -> np.ndarray:
    """Asymmetric distance from ``query`` to every code in ``codes``.

    Precomputes the squared distance from each of the query's M
    sub-vectors to each of the k centroids (one O(M*k) table), then
    sums the selected centroid distances per code row in O(M) per
    code. Total: O(M*k) + O(N*M). At M=8, k=256, N=10000 this is
    2048 + 80000 = 82048 ops vs 640000 for a naive decode + L2.

    Output: ``(N,)`` float32 array of approximate squared L2 distances.
    """
    if query.shape != (codebook.M * codebook.sub_dim,):
        raise ValueError(
            f"query must have shape ({codebook.M * codebook.sub_dim},), "
            f"got {query.shape}"
        )
    n = codes.shape[0]
    # lut[m, c] = ||query[m_th_sub] - centroids[m, c]||^2
    lut = np.zeros((codebook.M, codebook.k), dtype=np.float32)
    q = query.astype(np.float32, copy=False)
    for m in range(codebook.M):
        q_sub = q[m * codebook.sub_dim : (m + 1) * codebook.sub_dim]
        cent = codebook.centroids[m]
        diff = cent - q_sub  # (k, sub_dim)
        lut[m] = np.sum(diff * diff, axis=1)

    # Sum per row: for each code, look up lut[m, codes[i, m]] for m in [0,M) and sum
    dists = np.zeros(n, dtype=np.float32)
    for m in range(codebook.M):
        dists += lut[m][codes[:, m]]
    return dists
```

### Step 3: Run + commit

Expected: 7 tests pass.

```bash
cd /Users/philiplewis/vitruvius && /opt/homebrew/opt/python@3.11/bin/python3.11 -m pytest scripts/tests/test_pq_codebook.py -v
git add scripts/vitruvius/graph/pq_codebook.py scripts/tests/test_pq_codebook.py
git commit -m "feat(graph): Sprint PQ-1 Task 3 — adc_distance for fast approximate queries"
```

---

## Task 4: `save_codebook` + `load_codebook`

**Goal:** Persist a codebook to disk using `numpy.savez_compressed` and round-trip it back.

### Step 1: Append failing test

```python
def test_save_load_codebook_roundtrip(tmp_path) -> None:
    rng = np.random.default_rng(seed=0)
    embeddings = rng.standard_normal((50, 64)).astype(np.float32)
    codebook = train_pq_codebook(embeddings, M=8, k=16, n_iter=5, seed=42)

    from vitruvius.graph.pq_codebook import save_codebook, load_codebook

    out = tmp_path / "codebook.npz"
    save_codebook(codebook, out)
    assert out.exists()
    assert out.stat().st_size > 0

    loaded = load_codebook(out)
    assert loaded.M == codebook.M
    assert loaded.k == codebook.k
    assert loaded.sub_dim == codebook.sub_dim
    np.testing.assert_array_equal(loaded.centroids, codebook.centroids)
```

### Step 2: Implement

Append to `pq_codebook.py`:

```python
def save_codebook(codebook: PQCodebook, path: Path) -> None:
    """Save a codebook to ``path`` as a compressed numpy archive."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(
        path,
        centroids=codebook.centroids,
        M=np.int32(codebook.M),
        k=np.int32(codebook.k),
        sub_dim=np.int32(codebook.sub_dim),
    )


def load_codebook(path: Path) -> PQCodebook:
    """Load a codebook from ``path``."""
    with np.load(Path(path)) as data:
        return PQCodebook(
            centroids=data["centroids"].astype(np.float32, copy=True),
            M=int(data["M"]),
            k=int(data["k"]),
            sub_dim=int(data["sub_dim"]),
        )
```

### Step 3: Run + commit

```bash
cd /Users/philiplewis/vitruvius && /opt/homebrew/opt/python@3.11/bin/python3.11 -m pytest scripts/tests/test_pq_codebook.py -v
git add scripts/vitruvius/graph/pq_codebook.py scripts/tests/test_pq_codebook.py
git commit -m "feat(graph): Sprint PQ-1 Task 4 — save/load codebook via npz"
```

---

## Task 5: `compress_graphsage_report` integration helper

**Goal:** One-call helper that takes a `GraphSAGEReport` from `graphsage.py`, trains a codebook, and returns the encoded form ready for persistence.

### Step 1: Write failing tests

Create `scripts/tests/test_graphsage_pq.py`:

```python
"""Sprint PQ-1 Task 5 — compress_graphsage_report integration tests."""
from __future__ import annotations

import numpy as np
import pytest

from vitruvius.graph.graphsage import GraphSAGEReport
from vitruvius.graph.graphsage_pq import compress_graphsage_report
from vitruvius.graph.pq_codebook import PQCodebook


def test_compress_graphsage_report_shapes() -> None:
    rng = np.random.default_rng(seed=0)
    embeddings = {
        f"node-{i:03d}": rng.standard_normal(64).astype(np.float32)
        for i in range(200)
    }
    report = GraphSAGEReport(embeddings=embeddings, dim=64)

    codebook, codes, node_ids = compress_graphsage_report(
        report, M=8, k=32, n_iter=5, seed=42
    )

    assert isinstance(codebook, PQCodebook)
    assert codes.shape == (200, 8)
    assert codes.dtype == np.uint8
    assert len(node_ids) == 200
    # Order must be deterministic (sorted by node_id) so the codes[i]
    # always corresponds to node_ids[i].
    assert node_ids == sorted(node_ids)


def test_compress_graphsage_report_empty() -> None:
    report = GraphSAGEReport(embeddings={}, dim=64)
    codebook, codes, node_ids = compress_graphsage_report(
        report, M=8, k=32, n_iter=5, seed=42
    )
    assert codebook is None
    assert codes.shape == (0, 8)
    assert node_ids == []
```

### Step 2: Implement

Create `scripts/vitruvius/graph/graphsage_pq.py`:

```python
"""Sprint PQ-1 Task 5 — GraphSAGEReport → PQ compression helper."""
from __future__ import annotations

from typing import Optional

import numpy as np

from vitruvius.graph.graphsage import GraphSAGEReport
from vitruvius.graph.pq_codebook import (
    PQCodebook,
    encode_to_pq,
    train_pq_codebook,
)


def compress_graphsage_report(
    report: GraphSAGEReport,
    *,
    M: int = 8,
    k: int = 256,
    n_iter: int = 25,
    seed: int = 0,
) -> tuple[Optional[PQCodebook], np.ndarray, list[str]]:
    """Train a PQ codebook on ``report.embeddings`` and encode them.

    Returns ``(codebook, codes, node_ids)`` where ``codes[i]`` is the
    PQ encoding of ``node_ids[i]``'s embedding. Empty reports return
    ``(None, empty_array, [])``.

    Node IDs are returned in sorted order so the codes array is
    deterministic regardless of dict insertion order.
    """
    if not report.embeddings:
        return None, np.zeros((0, M), dtype=np.uint8), []

    node_ids = sorted(report.embeddings.keys())
    stacked = np.stack(
        [report.embeddings[nid] for nid in node_ids],
        axis=0,
    ).astype(np.float32, copy=False)

    codebook = train_pq_codebook(
        stacked, M=M, k=k, n_iter=n_iter, seed=seed
    )
    codes = encode_to_pq(stacked, codebook)
    return codebook, codes, node_ids
```

### Step 3: Run + commit

```bash
cd /Users/philiplewis/vitruvius && /opt/homebrew/opt/python@3.11/bin/python3.11 -m pytest scripts/tests/test_graphsage_pq.py -v
git add scripts/vitruvius/graph/graphsage_pq.py scripts/tests/test_graphsage_pq.py
git commit -m "feat(graph): Sprint PQ-1 Task 5 — compress_graphsage_report integration helper"
```

Expected: 2 new tests pass; full suite at prior_count + 9.

---

## Task 6: Reconstruction-error benchmark + flag + AD + archival

**Goal:** Measure the real-world reconstruction error on the existing synthetic GraphSAGE test corpus, flip the feature flag marker, write the AD, archive the plan.

### Step 1: Benchmark script

Create `scripts/vitruvius/bench/bench_pq_reconstruction.py` that:

1. Builds a synthetic `GraphSnapshot` with ~500 nodes (matching the GraphSAGE test pattern)
2. Runs `compute_graphsage_embeddings` to get a real `GraphSAGEReport`
3. Calls `compress_graphsage_report` with M=8, k=256, n_iter=25
4. Reports: original byte size (N * 64 * 4), PQ byte size (N * 8), compression ratio, average L2 reconstruction error
5. Writes `.ai/10_state/bench_pq_reconstruction_2026-04-15.json`

### Step 2: Feature flag

Add to `config/vitruvius.yaml`:

```yaml
  hp_graphsage_pq: false  # Sprint PQ-1 — PQ embedding compression deployment marker
```

Add to `scripts/tests/test_features.py::EXPECTED_FLAGS` + a default-false test.

### Step 3: AD entry + archival

Append to `.ai/10_state/decisions.md`:

```markdown
## AD-0XX — GraphSAGE PQ Embedding Compression (2026-04-15)

Shipped Product Quantization compression alongside GraphSAGE
embeddings. 64-d float32 (256 bytes/node) → 8-byte PQ codes
(32× compression). Measured reconstruction error: [FILL] average
L2 per node. Implementation: pure-numpy k-means (no sklearn,
no FAISS). Feature flag `hp_graphsage_pq` default false.
```

Fill with real numbers from the Step 1 benchmark run. Archive plan + update INDEX.md + final commit.

### Step 4: Tag

```bash
cd /Users/philiplewis/vitruvius && git tag sprint-pq-1-closed HEAD -m "Sprint PQ-1 — PQ compression for GraphSAGE embeddings"
```

---

## Self-Review

**1. Spec coverage.** User's Tier A #2 was "Product Quantization (PQ) for GraphSAGE embeddings" with a claim of 32× disk win and negligible quality loss. Every task ships a piece of that: training (T1), encoding (T2), decoding (T2), fast query (T3), persistence (T4), integration (T5), measurement (T6).

**2. Pure-numpy commitment.** Zero new pip deps. k-means is implemented from scratch in ~30 lines. Deterministic under seed.

**3. Decoupling.** The existing `graphsage.py` is not modified. PQ is a consumer, not a replacement. Flag-off behaviour is byte-identical.

**4. Scale fit.** At our current max of ~10k nodes, PQ saves us (10000 * 256) − (10000 * 8) = 2.48 MB of embedding storage. Not huge in absolute terms, but at 100k nodes it's 24.8 MB saved, and at 1M nodes it's 248 MB saved. The code is ready for that scale.

---

## Execution Handoff

Plan saved. Executable via executing-plans or subagent-driven-development when the user approves.
