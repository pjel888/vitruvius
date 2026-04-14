from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import numpy as np
import ot


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
