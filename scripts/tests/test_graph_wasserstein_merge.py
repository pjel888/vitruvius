"""Stream H.6 — Wasserstein merge decisions."""

from __future__ import annotations

import dataclasses

import numpy as np
import pytest

from vitruvius.graph.wasserstein_merge import (
    DEFAULT_MERGE_THRESHOLD,
    DEFAULT_REVIEW_THRESHOLD,
    MergeDecision,
    wasserstein_merge_decision,
)


def test_identical_distributions_merge() -> None:
    rng = np.random.default_rng(0)
    pts = rng.normal(size=(8, 4))
    decision = wasserstein_merge_decision(pts, pts.copy())
    assert decision.verdict == "merge"
    assert decision.distance < DEFAULT_MERGE_THRESHOLD


def test_far_distributions_keep_separate() -> None:
    a = np.zeros((10, 3))
    b = np.ones((10, 3)) * 100.0
    decision = wasserstein_merge_decision(a, b)
    assert decision.verdict == "keep_separate"
    assert decision.distance > DEFAULT_REVIEW_THRESHOLD


def test_medium_overlap_review() -> None:
    rng = np.random.default_rng(1)
    a = rng.normal(size=(16, 3))
    b = a + 0.2  # small constant offset → medium Wasserstein
    decision = wasserstein_merge_decision(
        a, b,
        merge_threshold=0.01,
        review_threshold=5.0,
    )
    assert decision.verdict == "review"
    assert 0.01 <= decision.distance < 5.0


def test_empty_input_raises() -> None:
    a = np.zeros((0, 3))
    b = np.zeros((4, 3))
    with pytest.raises(ValueError):
        wasserstein_merge_decision(a, b)


def test_mismatched_dims_raises() -> None:
    a = np.zeros((4, 3))
    b = np.zeros((4, 5))
    with pytest.raises(ValueError):
        wasserstein_merge_decision(a, b)


def test_frozen_return() -> None:
    a = np.zeros((3, 2))
    b = np.zeros((3, 2))
    decision = wasserstein_merge_decision(a, b)
    assert dataclasses.is_dataclass(decision)
    with pytest.raises(dataclasses.FrozenInstanceError):
        decision.verdict = "merge"  # type: ignore[misc]
    assert isinstance(decision, MergeDecision)


def test_thresholds_configurable() -> None:
    rng = np.random.default_rng(2)
    a = rng.normal(size=(8, 3))
    b = a + 0.5
    strict = wasserstein_merge_decision(
        a, b, merge_threshold=0.0, review_threshold=0.0
    )
    assert strict.verdict == "keep_separate"

    generous = wasserstein_merge_decision(
        a, b, merge_threshold=1_000.0, review_threshold=2_000.0
    )
    assert generous.verdict == "merge"
