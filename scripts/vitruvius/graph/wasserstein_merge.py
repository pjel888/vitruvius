from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import numpy as np
import ot

# Sprint RUST-MIG-1 Task 7 — DEFER_ALREADY_NATIVE (see AD-038a, 2026-04-15).
#
# The audit plan (.ai/03_plans/2026-04-15-rust-migration-audit-plan.md §2.3
# row N1 + §3) assumed this function was a pure ndarray sort + elementwise
# diff kernel — "sliced Wasserstein-2 via ndarray::sort". It is not. It
# builds a dense squared-Euclidean cost matrix via ot.dist (native BLAS) and
# calls ot.emd2 once (native POT C++ network simplex LP solver). There is
# no projection loop, no Python-level sort, no inner Python-level hot path
# to port — the 3830 ms / 369 MB baseline cost is dominated by the native
# EMD solve and the (n, n) cost matrix allocation, both already in C++.
#
# Per AD-036 §"Why Rust here at all": "we only port what wall-time
# measurement says is worth the Rust tax". A Rust reimplementation would
# either (a) duplicate POT's existing native path for d > 1 (scope creep —
# a full network simplex solver), or (b) ship a d == 1 sort-diff kernel
# that would never fire in production because every real call site passes
# multi-dimensional embeddings (see scripts/tests/test_graph_wasserstein_
# merge.py fixtures: d = 2, 3, 4). Sprint RUST-MIG-1 Task 7 is therefore
# DEFERred with no Rust code written. Task 8 (AD-038) will record the
# closure verdict alongside S1/S2/N4.


MergeVerdict = Literal["merge", "review", "keep_separate"]
DEFAULT_MERGE_THRESHOLD = 0.1
DEFAULT_REVIEW_THRESHOLD = 0.3


@dataclass(frozen=True)
class MergeDecision:
    distance: float
    verdict: MergeVerdict
    reason: str


def _verdict(
    distance: float,
    merge_threshold: float,
    review_threshold: float,
) -> tuple[MergeVerdict, str]:
    if distance < merge_threshold:
        return "merge", (
            f"2-Wasserstein distance {distance:.4f} below merge "
            f"threshold {merge_threshold}"
        )
    if distance < review_threshold:
        return "review", (
            f"2-Wasserstein distance {distance:.4f} in review band "
            f"[{merge_threshold}, {review_threshold})"
        )
    return "keep_separate", (
        f"2-Wasserstein distance {distance:.4f} at or above review "
        f"threshold {review_threshold}"
    )


def wasserstein_merge_decision(
    embeddings_a: np.ndarray,
    embeddings_b: np.ndarray,
    *,
    merge_threshold: float = DEFAULT_MERGE_THRESHOLD,
    review_threshold: float = DEFAULT_REVIEW_THRESHOLD,
) -> MergeDecision:
    if embeddings_a.ndim != 2 or embeddings_b.ndim != 2:
        raise ValueError(
            "embeddings must be 2-D arrays of shape (n, d); got "
            f"{embeddings_a.shape} and {embeddings_b.shape}"
        )
    if embeddings_a.shape[0] == 0 or embeddings_b.shape[0] == 0:
        raise ValueError("embeddings must not be empty")
    if embeddings_a.shape[1] != embeddings_b.shape[1]:
        raise ValueError(
            "embedding dimensions must match; got "
            f"{embeddings_a.shape[1]} and {embeddings_b.shape[1]}"
        )

    a_weights = np.ones(embeddings_a.shape[0]) / embeddings_a.shape[0]
    b_weights = np.ones(embeddings_b.shape[0]) / embeddings_b.shape[0]
    cost = ot.dist(embeddings_a, embeddings_b, metric="sqeuclidean")
    squared = float(ot.emd2(a_weights, b_weights, cost))
    distance = float(np.sqrt(max(squared, 0.0)))

    verdict, reason = _verdict(distance, merge_threshold, review_threshold)
    return MergeDecision(distance=distance, verdict=verdict, reason=reason)
