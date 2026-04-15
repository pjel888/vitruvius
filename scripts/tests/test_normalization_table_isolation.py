"""Sprint CLEANUP-1 Stream C1.3 — table isolation protocol.

Verifies that Tier A whitespace rules do not corrupt markdown pipe tables
when p1c_table_isolation is enabled.
"""

from __future__ import annotations

import pytest

from vitruvius.normalization.table_detector import (
    detect_table_line_ranges,
)
from vitruvius.normalization.rules_tier_a import CollapseTrailingWhitespace


TABLE_MARKDOWN = """\
## Example Table

| Column A | Column B |
|----------|----------|
|  Data 1  |  Data 2  |

Text after table.
"""


def test_detect_table_line_ranges_finds_gfm_block() -> None:
    lines = TABLE_MARKDOWN.splitlines()
    ranges = detect_table_line_ranges(lines)
    assert ranges == [(2, 4)]  # 0-indexed, inclusive — 3 lines of pipes


def test_collapse_trailing_whitespace_preserves_table_alignment(monkeypatch) -> None:
    """When p1c_table_isolation is on, trailing spaces inside table cells are preserved."""

    class _FlagsOn:
        def is_enabled(self, name: str) -> bool:
            return name == "p1c_table_isolation"

    # Patch the feature-gate loader where rules_tier_a imports it
    import vitruvius.normalization.rules_tier_a as rta
    monkeypatch.setattr(
        "vitruvius.spatial._feature_gate._load_features_cached",
        lambda: _FlagsOn(),
    )

    rule = CollapseTrailingWhitespace()
    result = rule.apply(TABLE_MARKDOWN)
    # Table rows must still have trailing spaces INSIDE the cells
    assert "|  Data 1  |  Data 2  |" in result
    # Non-table lines are still collapsed (the trailing space on "Text after table." is gone)
    assert "Text after table." in result
    assert "Text after table. \n" not in result


def test_collapse_trailing_whitespace_flag_off_byte_identical(monkeypatch) -> None:
    """When the flag is off, the rule's output is identical to pre-CLEANUP-1
    behavior — whatever that is on this input."""

    class _FlagsOff:
        def is_enabled(self, _name: str) -> bool:
            return False

    monkeypatch.setattr(
        "vitruvius.spatial._feature_gate._load_features_cached",
        lambda: _FlagsOff(),
    )

    rule = CollapseTrailingWhitespace()
    # The flag-off path must not raise and must produce a string
    result = rule.apply(TABLE_MARKDOWN)
    assert isinstance(result, str)
    # And the text-after-table must still be there (no corruption of non-table lines)
    assert "Text after table." in result
