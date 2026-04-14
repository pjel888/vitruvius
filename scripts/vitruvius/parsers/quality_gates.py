from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

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
