"""Sprint 1B-M3 Task 3 — GATE-006 min-chars-per-page tests."""
from __future__ import annotations

import pytest

from vitruvius.parsers.base_parser import ParseResult, ParserTelemetry
from vitruvius.parsers.quality_gates import (
    GateStatus,
    check_gate_006_min_chars_per_page,
)


def _make_result(*, md_length: int, pages_total: int, parser_id: str = "test") -> ParseResult:
    return ParseResult(
        markdown_text="x" * md_length,
        telemetry=ParserTelemetry(
            parser_id=parser_id,
            attempt_index=0,
            duration_ms=1,
            pages_total=pages_total,
            pages_processed=pages_total,
            page_coverage_ratio=1.0 if pages_total > 0 else 0.0,
            text_length=md_length,
            md_length=md_length,
            headers=0,
            tables=0,
            images=0,
            captions=0,
            ocr_applied=False,
            confidence=1.0,
            valid=True,
            error=None,
        ),
        sidecar_metadata={},
    )


def test_gate_006_accepts_sufficient_char_density() -> None:
    # 100 chars / 1 page = 100 chars/page, above the default 20 threshold
    result = _make_result(md_length=100, pages_total=1)
    gate = check_gate_006_min_chars_per_page(result)
    assert gate.status == GateStatus.PASSED
    assert gate.gate_id == "GATE-006"


def test_gate_006_rejects_insufficient_char_density() -> None:
    # 5 chars / 1 page = 5 chars/page, below the default 20 threshold
    result = _make_result(md_length=5, pages_total=1)
    gate = check_gate_006_min_chars_per_page(result)
    assert gate.status == GateStatus.FAILED
    assert "below threshold" in gate.reason.lower()


def test_gate_006_handles_zero_pages() -> None:
    # Must not divide by zero; must return FAILED with a clear reason
    result = _make_result(md_length=0, pages_total=0)
    gate = check_gate_006_min_chars_per_page(result)
    assert gate.status == GateStatus.FAILED
    assert "zero pages" in gate.reason.lower()
