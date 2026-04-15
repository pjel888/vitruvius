"""Sprint 1B-M1 Task 4 — Orchestrator preprocessor-integration tests.

Verifies the new `preprocessors` constructor parameter and the
process() flow that runs a preprocessor before the parser chain.
Tests use duck-typed stubs so they don't require soffice or docling
to be installed.
"""
from __future__ import annotations

from pathlib import Path

import pytest

from vitruvius.parsers.base_parser import BaseParser, ParseResult, ParserTelemetry
from vitruvius.parsers.document_taxonomy import DocumentClass
from vitruvius.parsers.libreoffice_preprocessor import PreprocessResult
from vitruvius.parsers.orchestrator import ParserOrchestrator, TerminalStatus


def _make_good_telemetry(parser_id: str, markdown: str) -> ParserTelemetry:
    return ParserTelemetry(
        parser_id=parser_id,
        attempt_index=0,
        duration_ms=1,
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


class _StubParser(BaseParser):
    parser_id = "stub_docling"
    parser_version = "stub-1.0"

    def __init__(self) -> None:
        self.parse_calls: list[Path] = []

    def parse(self, source_path: Path, work_dir: Path) -> ParseResult:
        self.parse_calls.append(source_path)
        # Produce enough markdown content to pass all 4 default quality
        # gates. GATE-002 requires >=500 chars; repeat a sentence enough
        # times to blow past it.
        md = (
            "# Generated heading\n\n"
            "This sentence makes the markdown body long enough to pass GATE-002. "
        ) * 20
        return ParseResult(
            markdown_text=md,
            telemetry=_make_good_telemetry(self.parser_id, md),
            sidecar_metadata={"source": str(source_path)},
        )


class _StubPreprocessor:
    """Duck-typed stub matching LibreOfficePreprocessor's surface.

    Exposes ``preprocessor_id`` + ``preprocess(*, source_path, workdir)``.
    """

    preprocessor_id = "libreoffice_preprocessor"

    def __init__(self, produce_pdf: bool = True) -> None:
        self.produce_pdf = produce_pdf
        self.preprocess_calls: list[Path] = []

    def preprocess(self, *, source_path: Path, workdir: Path) -> PreprocessResult:
        self.preprocess_calls.append(source_path)
        if not self.produce_pdf:
            return PreprocessResult(
                pdf_path=None,
                duration_ms=5,
                error="stub preprocessor forced failure",
            )
        output = Path(workdir) / (Path(source_path).stem + ".pdf")
        output.write_bytes(b"%PDF-1.4\n" + b"x" * 1024)
        return PreprocessResult(
            pdf_path=output,
            duration_ms=5,
            error=None,
        )


def test_office_doc_runs_preprocessor_before_parser(tmp_path: Path) -> None:
    parser = _StubParser()
    pre = _StubPreprocessor(produce_pdf=True)
    orch = ParserOrchestrator(
        parser_chains={DocumentClass.OFFICE_DOC: [parser]},
        preprocessors={DocumentClass.OFFICE_DOC: pre},
    )

    docx = tmp_path / "doc.docx"
    docx.write_text("stub office source")

    result = orch.process(
        source_path=docx,
        doc_class=DocumentClass.OFFICE_DOC,
        work_dir=tmp_path,
    )

    assert pre.preprocess_calls == [docx]
    # Parser was invoked on the preprocessor's output PDF, not the original .docx
    assert len(parser.parse_calls) == 1
    assert parser.parse_calls[0] != docx
    assert parser.parse_calls[0].suffix == ".pdf"
    assert result.terminal_status == TerminalStatus.AUTO_ACCEPTED
    assert result.successful_parser_id == "stub_docling"


def test_preprocessor_failure_short_circuits_to_fallback_exhausted(tmp_path: Path) -> None:
    parser = _StubParser()
    pre = _StubPreprocessor(produce_pdf=False)
    orch = ParserOrchestrator(
        parser_chains={DocumentClass.OFFICE_DOC: [parser]},
        preprocessors={DocumentClass.OFFICE_DOC: pre},
    )

    docx = tmp_path / "doc.docx"
    docx.write_text("stub office source")

    result = orch.process(
        source_path=docx,
        doc_class=DocumentClass.OFFICE_DOC,
        work_dir=tmp_path,
    )

    assert pre.preprocess_calls == [docx]
    # Parser must NOT be invoked when the preprocessor failed
    assert parser.parse_calls == []
    assert result.terminal_status == TerminalStatus.FALLBACK_EXHAUSTED
    assert result.successful_parser_id is None
    # The single attempt record belongs to the preprocessor
    assert len(result.attempts) == 1
    assert result.attempts[0].parser_id == "libreoffice_preprocessor"
    assert "forced failure" in (result.attempts[0].exception or "")


def test_no_preprocessor_registered_backcompat(tmp_path: Path) -> None:
    """With no preprocessor registered for a doc_class, the orchestrator
    behaves exactly as it did before Tranche 1: the parser chain runs
    directly on the source_path."""
    parser = _StubParser()
    orch = ParserOrchestrator(
        parser_chains={DocumentClass.HYBRID_PDF: [parser]},
        # No preprocessors kwarg at all — default is None → empty dict
    )

    pdf = tmp_path / "hybrid.pdf"
    pdf.write_bytes(b"%PDF-1.4\n" + b"x" * 1024)

    result = orch.process(
        source_path=pdf,
        doc_class=DocumentClass.HYBRID_PDF,
        work_dir=tmp_path,
    )

    assert len(parser.parse_calls) == 1
    assert parser.parse_calls[0] == pdf
    assert result.terminal_status == TerminalStatus.AUTO_ACCEPTED
