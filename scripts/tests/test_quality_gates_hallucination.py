"""Sprint CLEANUP-1 Stream C3.2 — Hallucination Trap quality gate tests.

GATE-007: repetition trap — detects >3 occurrences of the same 20+ char
substring (OCR fallback pattern).

GATE-008: script-mix trap — detects unexpected Unicode block clusters
(e.g., CJK in an English text).
"""

from __future__ import annotations

import pytest

from vitruvius.parsers.quality_gates import (
    GateStatus,
    check_gate_007_repetition_trap,
    check_gate_008_script_mix_trap,
)


def test_gate_007_passes_on_clean_text() -> None:
    text = (
        "Section 1. The building height shall not exceed 10 meters.\n"
        "Section 2. Lot coverage shall not exceed 60%.\n"
        "Section 3. Setbacks shall comply with this chapter.\n"
    )
    result = check_gate_007_repetition_trap(text=text)
    assert result.status == GateStatus.PASSED
    assert result.gate_id == "GATE-007"


def test_gate_007_fails_on_repeated_substring() -> None:
    # Repeat a 25-char sequence many times — classic OCR fallback
    padding = "xxxxxxxxxxxxxxxxxxxxxxxxx"  # 25 chars
    text = (padding + "\n") * 5
    result = check_gate_007_repetition_trap(text=text)
    assert result.status == GateStatus.FAILED
    assert "repetition" in result.reason.lower()


def test_gate_008_passes_on_pure_ascii() -> None:
    text = "All ASCII text like PD 1096 English statutes."
    result = check_gate_008_script_mix_trap(
        text=text,
        expected_scripts={"latin"},
    )
    assert result.status == GateStatus.PASSED


def test_gate_008_fails_on_unexpected_cjk() -> None:
    text = "Section 1 shall mean 節 the first chapter."  # CJK char mixed in
    result = check_gate_008_script_mix_trap(
        text=text,
        expected_scripts={"latin"},
    )
    assert result.status == GateStatus.FAILED
    assert "cjk" in result.reason.lower() or "han" in result.reason.lower() or "script" in result.reason.lower()


def test_gate_008_tolerates_short_accented_latin() -> None:
    """Accented latin (café, niño) should not trip the script-mix gate when
    latin is in expected_scripts."""
    text = "Café niño piñata — all still latin-script."
    result = check_gate_008_script_mix_trap(
        text=text,
        expected_scripts={"latin"},
    )
    assert result.status == GateStatus.PASSED
