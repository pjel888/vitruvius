"""Sprint CLEANUP-1 Stream C2.1 — phrase-density definition extractor tests."""

from __future__ import annotations

import pytest

from vitruvius.concepts.density_extractor import (
    DensityCandidate,
    extract_definitions_by_density,
)


def test_dense_paragraph_selected() -> None:
    text = """
Section 1. Yards and setbacks are regulated by this chapter.

Section 2. A yard is the open space between a building and the lot line.
A yard provides light and ventilation. A yard may be front, side, or rear.
The yard depth is measured perpendicular to the lot line.

Section 3. Other definitions follow.
"""
    candidates = extract_definitions_by_density(
        text=text,
        slug="yards",
        aliases=["yard", "yards"],
        min_density=2.0,  # 2 mentions per 500 chars
        window_chars=500,
    )
    assert len(candidates) >= 1
    top = candidates[0]
    assert isinstance(top, DensityCandidate)
    assert "yard" in top.definition.lower()
    assert top.density >= 2.0


def test_no_mentions_returns_empty() -> None:
    text = "Section 1. Only unrelated text here."
    candidates = extract_definitions_by_density(
        text=text,
        slug="yards",
        aliases=["yard", "yards"],
        min_density=2.0,
        window_chars=500,
    )
    assert candidates == []


def test_below_threshold_returns_empty() -> None:
    text = "This paragraph contains yards once. " * 3
    candidates = extract_definitions_by_density(
        text=text,
        slug="yards",
        aliases=["yard", "yards"],
        min_density=10.0,  # unreasonably high threshold
        window_chars=500,
    )
    assert candidates == []
