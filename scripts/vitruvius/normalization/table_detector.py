"""Sprint CLEANUP-1 Stream C1.3 — GFM pipe-table block detector.

A GFM pipe table is a block of contiguous lines where every line starts
with optional whitespace followed by `|`, and at least one of the first
two lines is a divider row (`| --- | --- |`).

Returns a list of (start_idx, end_idx) tuples (inclusive, 0-indexed) for
each detected table block. Used by Tier A whitespace rules to skip
trailing-space collapse inside table cells.

Perf call: pure string scan, above the Rust Line (AD-036).
"""

from __future__ import annotations

import re
from typing import List, Tuple


_PIPE_LINE = re.compile(r"^\s*\|.*\|\s*$")
_DIVIDER_LINE = re.compile(r"^\s*\|(\s*:?-+:?\s*\|)+\s*$")


def detect_table_line_ranges(lines: List[str]) -> List[Tuple[int, int]]:
    """Return (start_idx, end_idx) tuples for every GFM pipe-table block."""
    ranges: List[Tuple[int, int]] = []
    i = 0
    n = len(lines)
    while i < n:
        if _PIPE_LINE.match(lines[i]):
            start = i
            j = i
            saw_divider = False
            while j < n and _PIPE_LINE.match(lines[j]):
                if _DIVIDER_LINE.match(lines[j]):
                    saw_divider = True
                j += 1
            if saw_divider and j - start >= 2:
                ranges.append((start, j - 1))
            i = j
        else:
            i += 1
    return ranges


def is_line_inside_table(lines: List[str], line_idx: int) -> bool:
    """Return True iff `line_idx` falls inside any detected table block."""
    for start, end in detect_table_line_ranges(lines):
        if start <= line_idx <= end:
            return True
    return False
