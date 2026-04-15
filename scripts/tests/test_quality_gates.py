from __future__ import annotations

import dataclasses
from typing import Any

import pytest

from vitruvius.parsers.base_parser import ParseResult, ParserTelemetry
from vitruvius.parsers.quality_gates import (
    GateReport,
    GateResult,
    GateStatus,
    run_quality_gates,
)


def _make_telemetry(**overrides: Any) -> ParserTelemetry:
    defaults: dict[str, Any] = dict(
        parser_id="test-parser",
        attempt_index=0,
        duration_ms=100,
        pages_total=1,
        pages_processed=1,
        page_coverage_ratio=1.0,
        text_length=1000,
        md_length=600,
        headers=1,
        tables=0,
        images=0,
        captions=0,
        ocr_applied=False,
        confidence=0.95,
        valid=True,
        error=None,
    )
    defaults.update(overrides)
    return ParserTelemetry(**defaults)


def _make_parse_result(**overrides: Any) -> ParseResult:
    telemetry_overrides: dict[str, Any] = {
        k: overrides.pop(k)
        for k in list(overrides)
        if k in ParserTelemetry.__dataclass_fields__
    }
    telemetry = _make_telemetry(**telemetry_overrides)
    defaults: dict[str, Any] = dict(
        markdown_text="# Hello\n\nThis is clean markdown content.",
        telemetry=telemetry,
        sidecar_metadata={"file_type": "pdf"},
    )
    defaults.update(overrides)
    return ParseResult(**defaults)


# ---------------------------------------------------------------------------
# Gate-001 Integrity
# ---------------------------------------------------------------------------


def test_gate_001_passes_on_clean_markdown() -> None:
    result = _make_parse_result(markdown_text="# Hello\n\nworld")
    from vitruvius.parsers.quality_gates import check_gate_001_integrity
    gr = check_gate_001_integrity(result)
    assert gr.status == GateStatus.PASSED
    assert gr.gate_id == "GATE-001"
    assert gr.gate_name == "integrity"


def test_gate_001_fails_on_null_bytes() -> None:
    result = _make_parse_result(markdown_text="# Hello\x00world")
    from vitruvius.parsers.quality_gates import check_gate_001_integrity
    gr = check_gate_001_integrity(result)
    assert gr.status == GateStatus.FAILED
    assert "null" in gr.reason.lower()


def test_gate_001_fails_on_bom_prefix() -> None:
    result = _make_parse_result(markdown_text="\ufeff# Hello")
    from vitruvius.parsers.quality_gates import check_gate_001_integrity
    gr = check_gate_001_integrity(result)
    assert gr.status == GateStatus.FAILED
    assert "bom" in gr.reason.lower()


# ---------------------------------------------------------------------------
# Gate-002 Volume
# ---------------------------------------------------------------------------


def test_gate_002_passes_when_markdown_above_500_chars() -> None:
    result = _make_parse_result(markdown_text="x" * 600, text_length=10000)
    from vitruvius.parsers.quality_gates import check_gate_002_volume
    gr = check_gate_002_volume(result)
    assert gr.status == GateStatus.PASSED


def test_gate_002_passes_on_10_percent_threshold() -> None:
    result = _make_parse_result(markdown_text="x" * 200, text_length=1500)
    from vitruvius.parsers.quality_gates import check_gate_002_volume
    gr = check_gate_002_volume(result)
    assert gr.status == GateStatus.PASSED


def test_gate_002_fails_when_markdown_too_short() -> None:
    result = _make_parse_result(markdown_text="x" * 100, text_length=10000)
    from vitruvius.parsers.quality_gates import check_gate_002_volume
    gr = check_gate_002_volume(result)
    assert gr.status == GateStatus.FAILED


def test_gate_002_passes_when_text_length_zero_and_md_above_500() -> None:
    result = _make_parse_result(markdown_text="x" * 600, text_length=0)
    from vitruvius.parsers.quality_gates import check_gate_002_volume
    gr = check_gate_002_volume(result)
    assert gr.status == GateStatus.PASSED


def test_gate_002_fails_when_text_length_zero_and_md_below_500() -> None:
    result = _make_parse_result(markdown_text="x" * 100, text_length=0)
    from vitruvius.parsers.quality_gates import check_gate_002_volume
    gr = check_gate_002_volume(result)
    assert gr.status == GateStatus.FAILED


# ---------------------------------------------------------------------------
# Gate-003 Structure
# ---------------------------------------------------------------------------


def test_gate_003_not_applicable_when_pages_le_5() -> None:
    result = _make_parse_result(pages_total=3, markdown_text="plain body")
    from vitruvius.parsers.quality_gates import check_gate_003_structure
    gr = check_gate_003_structure(result)
    assert gr.status == GateStatus.NOT_APPLICABLE


def test_gate_003_passes_when_h1_present_and_pages_gt_5() -> None:
    result = _make_parse_result(markdown_text="# Title\n\nbody", pages_total=10)
    from vitruvius.parsers.quality_gates import check_gate_003_structure
    gr = check_gate_003_structure(result)
    assert gr.status == GateStatus.PASSED


def test_gate_003_passes_when_h2_present_and_pages_gt_5() -> None:
    result = _make_parse_result(markdown_text="body\n## Section\n", pages_total=10)
    from vitruvius.parsers.quality_gates import check_gate_003_structure
    gr = check_gate_003_structure(result)
    assert gr.status == GateStatus.PASSED


def test_gate_003_fails_when_no_header_and_pages_gt_5() -> None:
    result = _make_parse_result(markdown_text="plain body", pages_total=10)
    from vitruvius.parsers.quality_gates import check_gate_003_structure
    gr = check_gate_003_structure(result)
    assert gr.status == GateStatus.FAILED
    assert "header" in gr.reason.lower()


# ---------------------------------------------------------------------------
# Gate-004 Office Sanity
# ---------------------------------------------------------------------------


def test_gate_004_not_applicable_for_pdf() -> None:
    result = _make_parse_result(sidecar_metadata={"file_type": "pdf"})
    from vitruvius.parsers.quality_gates import check_gate_004_office_sanity
    gr = check_gate_004_office_sanity(result)
    assert gr.status == GateStatus.NOT_APPLICABLE


def test_gate_004_passes_exact_page_match_docx() -> None:
    result = _make_parse_result(
        sidecar_metadata={"file_type": "docx"},
        pages_total=10,
        pages_processed=10,
        markdown_text="# Document\n\nbody content",
    )
    from vitruvius.parsers.quality_gates import check_gate_004_office_sanity
    gr = check_gate_004_office_sanity(result)
    assert gr.status == GateStatus.PASSED


def test_gate_004_passes_within_tolerance_pptx() -> None:
    result = _make_parse_result(
        sidecar_metadata={"file_type": "pptx"},
        pages_total=10,
        pages_processed=9,
        markdown_text="# Slide\n\nbody",
    )
    from vitruvius.parsers.quality_gates import check_gate_004_office_sanity
    gr = check_gate_004_office_sanity(result)
    assert gr.status == GateStatus.PASSED


def test_gate_004_fails_when_page_count_mismatch() -> None:
    result = _make_parse_result(
        sidecar_metadata={"file_type": "docx"},
        pages_total=10,
        pages_processed=5,
        markdown_text="# Document\n\nbody content",
    )
    from vitruvius.parsers.quality_gates import check_gate_004_office_sanity
    gr = check_gate_004_office_sanity(result)
    assert gr.status == GateStatus.FAILED
    assert "page" in gr.reason.lower()


def test_gate_004_fails_when_empty_markdown() -> None:
    result = _make_parse_result(
        sidecar_metadata={"file_type": "docx"},
        pages_total=10,
        pages_processed=10,
        markdown_text="",
    )
    from vitruvius.parsers.quality_gates import check_gate_004_office_sanity
    gr = check_gate_004_office_sanity(result)
    assert gr.status == GateStatus.FAILED


# ---------------------------------------------------------------------------
# Orchestrator
# ---------------------------------------------------------------------------


def test_run_quality_gates_all_pass_pdf() -> None:
    result = _make_parse_result(
        markdown_text="# Title\n\n" + "x" * 600,
        text_length=6000,
        pages_total=3,
        pages_processed=3,
        sidecar_metadata={"file_type": "pdf"},
    )
    report = run_quality_gates(result)
    assert report.passed is True
    assert len(report.results) == 4
    assert report.results[0].gate_id == "GATE-001"
    assert report.results[1].gate_id == "GATE-002"
    assert report.results[2].gate_id == "GATE-003"
    assert report.results[3].gate_id == "GATE-004"
    assert report.results[3].status == GateStatus.NOT_APPLICABLE


def test_run_quality_gates_all_pass_docx() -> None:
    result = _make_parse_result(
        markdown_text="# Title\n\n" + "x" * 600,
        text_length=6000,
        pages_total=3,
        pages_processed=3,
        sidecar_metadata={"file_type": "docx"},
    )
    report = run_quality_gates(result)
    assert report.passed is True
    assert report.results[3].status == GateStatus.PASSED


def test_run_quality_gates_composite_failure() -> None:
    result = _make_parse_result(
        markdown_text="plain body\x00",
        text_length=10000,
        pages_total=10,
        pages_processed=10,
        sidecar_metadata={"file_type": "pdf"},
    )
    report = run_quality_gates(result)
    assert report.passed is False
    failed_gates = [r for r in report.results if r.status == GateStatus.FAILED]
    assert len(failed_gates) >= 2


def test_gate_report_results_are_in_canonical_order() -> None:
    result = _make_parse_result()
    report = run_quality_gates(result)
    assert [r.gate_id for r in report.results] == [
        "GATE-001",
        "GATE-002",
        "GATE-003",
        "GATE-004",
    ]


# ---------------------------------------------------------------------------
# Dataclass smoke tests
# ---------------------------------------------------------------------------


def test_gate_report_is_frozen() -> None:
    result = _make_parse_result()
    report = run_quality_gates(result)
    with pytest.raises((dataclasses.FrozenInstanceError, TypeError, AttributeError)):
        report.passed = False  # type: ignore[misc]


def test_gate_result_is_frozen() -> None:
    result = _make_parse_result()
    report = run_quality_gates(result)
    gr = report.results[0]
    with pytest.raises((dataclasses.FrozenInstanceError, TypeError, AttributeError)):
        gr.status = GateStatus.FAILED  # type: ignore[misc]


def test_gate_005_accepts_non_empty_pdf(tmp_path):
    from vitruvius.parsers.quality_gates import check_gate_005_libreoffice_pdf, GateStatus

    pdf = tmp_path / "out.pdf"
    # Minimum-viable payload: 256+ bytes so GATE-005 accepts it
    pdf.write_bytes(b"%PDF-1.4\n" + b"x" * 512)

    result = check_gate_005_libreoffice_pdf(pdf_path=pdf)
    assert result.status == GateStatus.PASSED
    assert result.gate_id == "GATE-005"


def test_gate_005_rejects_missing_pdf(tmp_path):
    from vitruvius.parsers.quality_gates import check_gate_005_libreoffice_pdf, GateStatus

    missing = tmp_path / "missing.pdf"
    result = check_gate_005_libreoffice_pdf(pdf_path=missing)
    assert result.status == GateStatus.FAILED
    assert "does not exist" in result.reason.lower()


def test_gate_005_rejects_empty_pdf(tmp_path):
    from vitruvius.parsers.quality_gates import check_gate_005_libreoffice_pdf, GateStatus

    empty = tmp_path / "empty.pdf"
    empty.write_bytes(b"")
    result = check_gate_005_libreoffice_pdf(pdf_path=empty)
    assert result.status == GateStatus.FAILED
    assert "empty" in result.reason.lower()
