"""Stream PHYS.3 — Shannon entropy adaptive sampler + Kolmogorov delta."""
from __future__ import annotations

import math

import pytest

from vitruvius.graph.physics import (
    KolmogorovDelta,
    adaptive_window_overlap,
    compute_shannon_entropy,
    compute_kolmogorov_delta,
)


# ---------------------------------------------------------------------------
# Shannon entropy
# ---------------------------------------------------------------------------
def test_entropy_of_empty_string_is_zero() -> None:
    assert compute_shannon_entropy("") == 0.0


def test_entropy_of_single_char_is_zero() -> None:
    assert compute_shannon_entropy("aaaaaaa") == pytest.approx(0.0, abs=1e-9)


def test_entropy_scales_with_variety() -> None:
    low = compute_shannon_entropy("aaaabbbb")
    high = compute_shannon_entropy("abcdefgh")
    assert high > low
    # "abcdefgh" has 8 equiprobable chars → entropy = log2(8) = 3.0
    assert high == pytest.approx(math.log2(8), abs=1e-9)


def test_entropy_counts_numeric_density() -> None:
    """Legal text with lots of numbers should score higher than prose
    because the digit vocabulary expands the symbol alphabet."""
    prose = "the setback must be met"
    numeric = "the setback must be 3.5 m, 7.2 m, or 15 m"
    # Rough proxy — we just check numeric > prose by at least a bit.
    assert compute_shannon_entropy(numeric) > compute_shannon_entropy(prose)


# ---------------------------------------------------------------------------
# Adaptive sampler
# ---------------------------------------------------------------------------
def test_adaptive_overlap_bounds() -> None:
    """Overlap must sit in [min, max] regardless of entropy."""
    for entropy in [0.0, 1.0, 2.0, 4.0, 8.0]:
        overlap = adaptive_window_overlap(
            entropy=entropy,
            window_size=512,
            min_overlap=16,
            max_overlap=256,
        )
        assert 16 <= overlap <= 256


def test_adaptive_overlap_grows_with_entropy() -> None:
    low = adaptive_window_overlap(
        entropy=1.0, window_size=512, min_overlap=16, max_overlap=256,
    )
    high = adaptive_window_overlap(
        entropy=6.0, window_size=512, min_overlap=16, max_overlap=256,
    )
    assert high > low


# ---------------------------------------------------------------------------
# Kolmogorov delta
# ---------------------------------------------------------------------------
def test_kolmogorov_delta_for_identical_text() -> None:
    delta = compute_kolmogorov_delta("hello world", "hello world")
    assert isinstance(delta, KolmogorovDelta)
    assert delta.edit_ratio == pytest.approx(0.0, abs=1e-9)
    assert delta.is_near_duplicate is True


def test_kolmogorov_delta_for_small_modification() -> None:
    base = "hello world, the setback is 3 meters"
    modified = "hello world, the setback is 4 meters"
    delta = compute_kolmogorov_delta(base, modified)
    # Only 1 char differs out of ~37; edit ratio should be very small.
    assert delta.edit_ratio < 0.1
    assert delta.is_near_duplicate is True


def test_kolmogorov_delta_for_different_text() -> None:
    base = "the setback must be 3 meters"
    modified = "building permits require an application fee of 5000 PHP"
    delta = compute_kolmogorov_delta(base, modified)
    assert delta.edit_ratio > 0.5
    assert delta.is_near_duplicate is False
