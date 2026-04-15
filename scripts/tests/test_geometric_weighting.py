"""Sprint GT Stream GT.4.2 — exponential distance weighting.

Pure math: ``w(seed) = exp(-lambda_decay * euclidean_distance)``.
Closer seeds score near 1.0, distant seeds asymptote to 0.0. No
octree dependency here — the caller passes a ``{seed_id: xyz}``
mapping that already came out of ``proximity_jump_seed`` + a
separate AABB lookup.
"""
from __future__ import annotations

import math

import pytest

from vitruvius.spatial.proximity_jump import weight_by_distance


def test_closer_seed_has_higher_weight() -> None:
    """The seed at (0,0,0) should score higher than the seed 5 units out."""
    seeds = {
        "instance-a": (0.0, 0.0, 0.0),
        "instance-b": (5.0, 0.0, 0.0),
    }
    weights = weight_by_distance(
        seeds,
        focal_xyz=(0.0, 0.0, 0.0),
        lambda_decay=0.1,
    )
    assert weights["instance-a"] > weights["instance-b"]


def test_weight_at_origin_is_one() -> None:
    """d = 0 → exp(0) = 1.0 exactly."""
    seeds = {"instance-a": (0.0, 0.0, 0.0)}
    weights = weight_by_distance(
        seeds,
        focal_xyz=(0.0, 0.0, 0.0),
        lambda_decay=0.1,
    )
    assert math.isclose(weights["instance-a"], 1.0, abs_tol=1e-9)


def test_weight_matches_closed_form_exponential() -> None:
    """Pythagorean (3, 4, 0) → distance 5 → exp(-lambda * 5)."""
    seeds = {"instance-a": (3.0, 4.0, 0.0)}
    weights = weight_by_distance(
        seeds,
        focal_xyz=(0.0, 0.0, 0.0),
        lambda_decay=0.2,
    )
    expected = math.exp(-0.2 * 5.0)
    assert math.isclose(weights["instance-a"], expected, abs_tol=1e-9)


def test_empty_seeds_returns_empty_dict() -> None:
    weights = weight_by_distance(
        {},
        focal_xyz=(0.0, 0.0, 0.0),
        lambda_decay=0.1,
    )
    assert weights == {}


def test_larger_lambda_decays_faster() -> None:
    """For a fixed seed, larger lambda_decay → smaller weight."""
    seeds = {"instance-a": (10.0, 0.0, 0.0)}
    slow = weight_by_distance(
        seeds, focal_xyz=(0.0, 0.0, 0.0), lambda_decay=0.05
    )
    fast = weight_by_distance(
        seeds, focal_xyz=(0.0, 0.0, 0.0), lambda_decay=0.5
    )
    assert slow["instance-a"] > fast["instance-a"]
    # Sanity check: both are in (0, 1].
    for w in (slow["instance-a"], fast["instance-a"]):
        assert 0.0 < w <= 1.0


def test_weight_is_bounded_above_by_one() -> None:
    """Every weight must lie in (0, 1] — exp(-lambda * d) <= 1 iff
    lambda * d >= 0 (which holds for non-negative lambda and any
    physical distance)."""
    seeds = {
        "instance-a": (0.0, 0.0, 0.0),
        "instance-b": (1.0, 0.0, 0.0),
        "instance-c": (10.0, 10.0, 10.0),
    }
    weights = weight_by_distance(
        seeds, focal_xyz=(0.0, 0.0, 0.0), lambda_decay=0.1
    )
    for w in weights.values():
        assert 0.0 < w <= 1.0
