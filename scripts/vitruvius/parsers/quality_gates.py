from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from pathlib import Path

from vitruvius.parsers.base_parser import ParseResult

_OFFICE_FILE_TYPES: frozenset[str] = frozenset({"docx", "pptx", "doc", "ppt"})


class GateStatus(str, Enum):
    PASSED = "passed"
    FAILED = "failed"
    NOT_APPLICABLE = "not_applicable"


@dataclass(kw_only=True, frozen=True)
class GateResult:
    gate_id: str
    gate_name: str
    status: GateStatus
    reason: str


@dataclass(kw_only=True, frozen=True)
class GateReport:
    results: tuple[GateResult, ...]
    passed: bool


def check_gate_001_integrity(parse_result: ParseResult) -> GateResult:
    md = parse_result.markdown_text
    if md.startswith("\ufeff"):
        return GateResult(
            gate_id="GATE-001",
            gate_name="integrity",
            status=GateStatus.FAILED,
            reason="markdown_text starts with a BOM (U+FEFF)",
        )
    if "\x00" in md:
        return GateResult(
            gate_id="GATE-001",
            gate_name="integrity",
            status=GateStatus.FAILED,
            reason="markdown_text contains null byte(s) (U+0000)",
        )
    try:
        md.encode("utf-8").decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError) as exc:
        return GateResult(
            gate_id="GATE-001",
            gate_name="integrity",
            status=GateStatus.FAILED,
            reason=f"UTF-8 roundtrip failed: {exc}",
        )
    return GateResult(
        gate_id="GATE-001",
        gate_name="integrity",
        status=GateStatus.PASSED,
        reason="",
    )


def check_gate_002_volume(parse_result: ParseResult) -> GateResult:
    md_len = len(parse_result.markdown_text)
    text_len = parse_result.telemetry.text_length
    if md_len >= 500:
        return GateResult(
            gate_id="GATE-002",
            gate_name="volume",
            status=GateStatus.PASSED,
            reason="",
        )
    if text_len > 0 and md_len >= 0.1 * text_len:
        return GateResult(
            gate_id="GATE-002",
            gate_name="volume",
            status=GateStatus.PASSED,
            reason="",
        )
    return GateResult(
        gate_id="GATE-002",
        gate_name="volume",
        status=GateStatus.FAILED,
        reason=(
            f"markdown_length={md_len} is below 500-char floor and below "
            f"10% of text_length={text_len}"
        ),
    )


def check_gate_003_structure(parse_result: ParseResult) -> GateResult:
    if parse_result.telemetry.pages_total <= 5:
        return GateResult(
            gate_id="GATE-003",
            gate_name="structure",
            status=GateStatus.NOT_APPLICABLE,
            reason="",
        )
    for line in parse_result.markdown_text.splitlines():
        if line.startswith("# ") or line.startswith("## "):
            return GateResult(
                gate_id="GATE-003",
                gate_name="structure",
                status=GateStatus.PASSED,
                reason="",
            )
    return GateResult(
        gate_id="GATE-003",
        gate_name="structure",
        status=GateStatus.FAILED,
        reason=(
            "no ATX header (# or ##) found in document with "
            f"pages_total={parse_result.telemetry.pages_total}"
        ),
    )


def check_gate_004_office_sanity(parse_result: ParseResult) -> GateResult:
    file_type = parse_result.sidecar_metadata.get("file_type", "")
    if file_type not in _OFFICE_FILE_TYPES:
        return GateResult(
            gate_id="GATE-004",
            gate_name="office_sanity",
            status=GateStatus.NOT_APPLICABLE,
            reason="",
        )
    if not parse_result.markdown_text:
        return GateResult(
            gate_id="GATE-004",
            gate_name="office_sanity",
            status=GateStatus.FAILED,
            reason="markdown_text is empty for office file",
        )
    pages_total = parse_result.telemetry.pages_total
    pages_processed = parse_result.telemetry.pages_processed
    if abs(pages_total - pages_processed) > 1:
        return GateResult(
            gate_id="GATE-004",
            gate_name="office_sanity",
            status=GateStatus.FAILED,
            reason=(
                f"page count mismatch: pages_total={pages_total} vs "
                f"pages_processed={pages_processed} (tolerance ±1)"
            ),
        )
    return GateResult(
        gate_id="GATE-004",
        gate_name="office_sanity",
        status=GateStatus.PASSED,
        reason="",
    )


def run_quality_gates(parse_result: ParseResult) -> GateReport:
    results = (
        check_gate_001_integrity(parse_result),
        check_gate_002_volume(parse_result),
        check_gate_003_structure(parse_result),
        check_gate_004_office_sanity(parse_result),
    )
    passed = all(r.status != GateStatus.FAILED for r in results)
    return GateReport(results=results, passed=passed)


def check_gate_005_libreoffice_pdf(*, pdf_path: Path) -> GateResult:
    """GATE-005 — post-LibreOffice PDF sanity check (Sprint 1B-M1 Task 3).

    Verifies the PDF produced by :class:`LibreOfficePreprocessor`:
    - exists on disk
    - has non-zero bytes
    - is at least 256 bytes (empirically: any valid soffice PDF output
      is larger than this; shorter outputs indicate a silent failure)

    Returns a :class:`GateResult` with status PASSED / FAILED.
    """
    pdf_path = Path(pdf_path)
    if not pdf_path.exists():
        return GateResult(
            gate_id="GATE-005",
            gate_name="libreoffice_pdf_sanity",
            status=GateStatus.FAILED,
            reason=f"PDF does not exist: {pdf_path}",
        )
    size_bytes = pdf_path.stat().st_size
    if size_bytes == 0:
        return GateResult(
            gate_id="GATE-005",
            gate_name="libreoffice_pdf_sanity",
            status=GateStatus.FAILED,
            reason=f"PDF is empty (0 bytes): {pdf_path}",
        )
    if size_bytes < 256:
        return GateResult(
            gate_id="GATE-005",
            gate_name="libreoffice_pdf_sanity",
            status=GateStatus.FAILED,
            reason=(
                f"PDF is suspiciously small ({size_bytes} bytes, minimum 256): "
                f"likely a silent soffice failure"
            ),
        )
    return GateResult(
        gate_id="GATE-005",
        gate_name="libreoffice_pdf_sanity",
        status=GateStatus.PASSED,
        reason=f"PDF {pdf_path.name} is {size_bytes} bytes (>=256)",
    )


def check_gate_006_min_chars_per_page(
    parse_result: ParseResult,
    *,
    min_chars_per_page: int = 20,
) -> GateResult:
    """GATE-006 — minimum characters per extracted page.

    Catches silent failures where a parser returns non-error but
    empty (or near-empty) text — typical for encrypted PDFs and
    lopdf decode failures on non-standard font dictionaries.
    Sprint 1B-M3 Task 3.
    """
    telemetry = parse_result.telemetry
    if telemetry.pages_total == 0:
        return GateResult(
            gate_id="GATE-006",
            gate_name="min_chars_per_page",
            status=GateStatus.FAILED,
            reason=f"zero pages extracted; parser_id={telemetry.parser_id!r}",
        )
    avg = telemetry.md_length / telemetry.pages_total
    if avg < min_chars_per_page:
        return GateResult(
            gate_id="GATE-006",
            gate_name="min_chars_per_page",
            status=GateStatus.FAILED,
            reason=(
                f"average chars per page {avg:.1f} below threshold "
                f"{min_chars_per_page} ({telemetry.md_length} chars / "
                f"{telemetry.pages_total} pages)"
            ),
        )
    return GateResult(
        gate_id="GATE-006",
        gate_name="min_chars_per_page",
        status=GateStatus.PASSED,
        reason=f"{avg:.1f} chars/page >= {min_chars_per_page}",
    )
