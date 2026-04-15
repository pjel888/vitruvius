"""Sprint PIPELINE-CLI Task 2 — tests for run_convert_parsers_one handler.

Uses monkey-patching on build_default_orchestrator to inject a stub
orchestrator so we never touch real PDF kernels (docling, lopdf,
opendataloader_pdf). The handler's job is:

1. Resolve the relative path against 001_Raw-Source-Layer
2. Classify by extension via document_taxonomy
3. Call orchestrator.process()
4. On AUTO_ACCEPTED / AUTO_REFINED — write markdown to
   002_Raw-Conversion-Layer/<top_category>/refined_markdown/<...>/<stem>.md
   and write telemetry sidecar to
   006_System-Manifests/runs/latest_convert_parsers.json
5. Return 0 on success, 1 on FALLBACK_EXHAUSTED
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from vitruvius.parsers.base_parser import ParseResult, ParserTelemetry
from vitruvius.parsers.document_taxonomy import DocumentClass
from vitruvius.parsers.orchestrator import (
    AttemptRecord,
    OrchestratorResult,
    ParserOrchestrator,
    TerminalStatus,
)
from vitruvius.parsers.quality_gates import GateReport, GateResult, GateStatus


def _good_telemetry(parser_id: str, markdown: str) -> ParserTelemetry:
    return ParserTelemetry(
        parser_id=parser_id,
        attempt_index=0,
        duration_ms=42,
        pages_total=1,
        pages_processed=1,
        page_coverage_ratio=1.0,
        text_length=len(markdown),
        md_length=len(markdown),
        headers=1,
        tables=0,
        images=0,
        captions=0,
        ocr_applied=False,
        confidence=1.0,
        valid=True,
        error=None,
    )


def _good_gate_report() -> GateReport:
    return GateReport(
        results=(
            GateResult(
                gate_id="GATE-001",
                gate_name="integrity",
                status=GateStatus.PASSED,
                reason="",
            ),
        ),
        passed=True,
    )


class _StubOrchestrator:
    """Drop-in replacement for ParserOrchestrator returning a fixed result."""

    def __init__(self, result: OrchestratorResult) -> None:
        self._result = result
        self.process_calls: list[dict] = []

    def process(
        self,
        *,
        source_path: Path,
        doc_class: DocumentClass,
        work_dir: Path,
    ) -> OrchestratorResult:
        self.process_calls.append(
            {
                "source_path": source_path,
                "doc_class": doc_class,
                "work_dir": work_dir,
            }
        )
        return self._result


@pytest.fixture
def fake_repo_root(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    raw = tmp_path / "001_Raw-Source-Layer"
    raw.mkdir(parents=True)
    (raw / "001-Laws").mkdir()
    (raw / "001-Laws" / "PD-1096").mkdir()
    pdf = raw / "001-Laws" / "PD-1096" / "doc.pdf"
    pdf.write_bytes(b"%PDF-1.4\n" + b"x" * 1024)

    monkeypatch.setattr(
        "vitruvius.parsers.cli_handler._get_repo_root",
        lambda: tmp_path,
    )
    return tmp_path


def test_handler_writes_markdown_and_sidecar_on_auto_accepted(
    fake_repo_root: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    md = "# Title\n\n" + ("This is a sentence. " * 50)
    parse_result = ParseResult(
        markdown_text=md,
        telemetry=_good_telemetry("stub_parser", md),
        sidecar_metadata={"source": "stub"},
    )
    orch_result = OrchestratorResult(
        terminal_status=TerminalStatus.AUTO_ACCEPTED,
        successful_parser_id="stub_parser",
        final_parse_result=parse_result,
        attempts=(
            AttemptRecord(
                parser_id="stub_parser",
                attempt_index=0,
                parse_result=parse_result,
                gate_report=_good_gate_report(),
                exception=None,
            ),
        ),
    )
    stub = _StubOrchestrator(orch_result)
    monkeypatch.setattr(
        "vitruvius.parsers.cli_handler.build_default_orchestrator",
        lambda: stub,
    )

    from vitruvius.parsers.cli_handler import run_convert_parsers_one

    rc = run_convert_parsers_one(relative_pdf_path="001-Laws/PD-1096/doc.pdf")
    assert rc == 0

    expected_md = (
        fake_repo_root
        / "002_Raw-Conversion-Layer"
        / "001-Laws"
        / "refined_markdown"
        / "PD-1096"
        / "doc.md"
    )
    assert expected_md.exists()
    assert expected_md.read_text(encoding="utf-8") == md

    sidecar = (
        fake_repo_root
        / "006_System-Manifests"
        / "runs"
        / "latest_convert_parsers.json"
    )
    assert sidecar.exists()
    data = json.loads(sidecar.read_text(encoding="utf-8"))
    assert data["terminal_status"] == "auto_accepted"
    assert data["successful_parser_id"] == "stub_parser"
    assert data["relative_pdf_path"] == "001-Laws/PD-1096/doc.pdf"
    assert data["doc_class"] == "text_pdf_simple"
    assert "attempts" in data
    assert data["attempts"][0]["parser_id"] == "stub_parser"


def test_handler_returns_one_and_logs_attempts_on_fallback_exhausted(
    fake_repo_root: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    orch_result = OrchestratorResult(
        terminal_status=TerminalStatus.FALLBACK_EXHAUSTED,
        successful_parser_id=None,
        final_parse_result=None,
        attempts=(
            AttemptRecord(
                parser_id="primary",
                attempt_index=0,
                parse_result=None,
                gate_report=None,
                exception="primary parser exploded",
            ),
            AttemptRecord(
                parser_id="fallback",
                attempt_index=1,
                parse_result=None,
                gate_report=None,
                exception="fallback parser also exploded",
            ),
        ),
    )
    stub = _StubOrchestrator(orch_result)
    monkeypatch.setattr(
        "vitruvius.parsers.cli_handler.build_default_orchestrator",
        lambda: stub,
    )

    from vitruvius.parsers.cli_handler import run_convert_parsers_one

    rc = run_convert_parsers_one(relative_pdf_path="001-Laws/PD-1096/doc.pdf")
    assert rc == 1

    # No markdown was written.
    md_dir = (
        fake_repo_root
        / "002_Raw-Conversion-Layer"
        / "001-Laws"
        / "refined_markdown"
    )
    assert not md_dir.exists()

    # Sidecar is written even on failure so operators can see the
    # attempt log.
    sidecar = (
        fake_repo_root
        / "006_System-Manifests"
        / "runs"
        / "latest_convert_parsers.json"
    )
    assert sidecar.exists()
    data = json.loads(sidecar.read_text(encoding="utf-8"))
    assert data["terminal_status"] == "fallback_exhausted"
    assert data["successful_parser_id"] is None
    assert len(data["attempts"]) == 2
    assert data["attempts"][0]["exception"] == "primary parser exploded"
    assert data["attempts"][1]["exception"] == "fallback parser also exploded"


def test_handler_errors_when_source_missing(
    fake_repo_root: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A missing source file should print an error and return 1
    without ever calling the orchestrator factory."""
    called = {"factory": False}

    def _raises():
        called["factory"] = True
        raise AssertionError("factory should not be called for missing files")

    monkeypatch.setattr(
        "vitruvius.parsers.cli_handler.build_default_orchestrator",
        _raises,
    )

    from vitruvius.parsers.cli_handler import run_convert_parsers_one

    rc = run_convert_parsers_one(
        relative_pdf_path="001-Laws/PD-1096/does_not_exist.pdf"
    )
    assert rc == 1
    assert called["factory"] is False


def test_handler_classifies_office_doc_by_extension(
    fake_repo_root: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A .docx source path should be classified as OFFICE_DOC and
    routed through that chain."""
    raw = fake_repo_root / "001_Raw-Source-Layer"
    docx = raw / "001-Laws" / "PD-1096" / "doc.docx"
    docx.write_bytes(b"PK\x03\x04stub office bytes")

    md = "# Office heading\n\n" + ("Office body sentence. " * 50)
    parse_result = ParseResult(
        markdown_text=md,
        telemetry=_good_telemetry("office_stub", md),
        sidecar_metadata={"source": "office stub"},
    )
    orch_result = OrchestratorResult(
        terminal_status=TerminalStatus.AUTO_REFINED,
        successful_parser_id="office_stub",
        final_parse_result=parse_result,
        attempts=(
            AttemptRecord(
                parser_id="office_stub",
                attempt_index=1,
                parse_result=parse_result,
                gate_report=_good_gate_report(),
                exception=None,
            ),
        ),
    )
    stub = _StubOrchestrator(orch_result)
    monkeypatch.setattr(
        "vitruvius.parsers.cli_handler.build_default_orchestrator",
        lambda: stub,
    )

    from vitruvius.parsers.cli_handler import run_convert_parsers_one

    rc = run_convert_parsers_one(relative_pdf_path="001-Laws/PD-1096/doc.docx")
    assert rc == 0
    assert len(stub.process_calls) == 1
    assert stub.process_calls[0]["doc_class"] == DocumentClass.OFFICE_DOC
