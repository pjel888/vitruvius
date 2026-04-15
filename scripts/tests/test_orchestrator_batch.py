"""Sprint 1B-M2 Task 2 — ParserOrchestrator.process_batch tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from vitruvius.parsers.base_parser import BaseParser, ParseResult, ParserTelemetry
from vitruvius.parsers.document_taxonomy import DocumentClass
from vitruvius.parsers.orchestrator import (
    BatchJob,
    ParserOrchestrator,
    TerminalStatus,
)


class _StubParser(BaseParser):
    parser_id = "stub_parallel"
    parser_version = "stub-2.0"

    def parse(self, source_path: Path, work_dir: Path) -> ParseResult:
        md = (
            "# Batch-mode heading\n\n"
            "This sentence is long enough to pass GATE-002 on its own. "
        ) * 20
        return ParseResult(
            markdown_text=md,
            telemetry=ParserTelemetry(
                parser_id=self.parser_id,
                attempt_index=0,
                duration_ms=1,
                pages_total=1,
                pages_processed=1,
                page_coverage_ratio=1.0,
                text_length=len(md),
                md_length=len(md),
                headers=1,
                tables=0,
                images=0,
                captions=0,
                ocr_applied=False,
                confidence=1.0,
                valid=True,
                error=None,
            ),
            sidecar_metadata={"source": str(source_path)},
        )


def test_process_batch_preserves_order(tmp_path: Path) -> None:
    parser = _StubParser()
    orch = ParserOrchestrator(
        parser_chains={DocumentClass.HYBRID_PDF: [parser]},
    )
    jobs: list[BatchJob] = []
    for i in range(5):
        pdf = tmp_path / f"doc_{i}.pdf"
        pdf.write_bytes(b"%PDF-1.4\n" + b"x" * 1024)
        jobs.append(
            BatchJob(
                source_path=pdf,
                doc_class=DocumentClass.HYBRID_PDF,
                work_dir=tmp_path,
            )
        )

    results = orch.process_batch(jobs=jobs)
    assert len(results) == len(jobs)
    for i, r in enumerate(results):
        assert r.terminal_status == TerminalStatus.AUTO_ACCEPTED
        assert r.final_parse_result is not None
        assert f"doc_{i}.pdf" in r.final_parse_result.sidecar_metadata["source"]


def test_process_batch_empty_list(tmp_path: Path) -> None:
    parser = _StubParser()
    orch = ParserOrchestrator(
        parser_chains={DocumentClass.HYBRID_PDF: [parser]},
    )
    results = orch.process_batch(jobs=[])
    assert results == ()


def test_process_batch_respects_max_workers(tmp_path: Path) -> None:
    """Smoke test that max_workers kwarg is accepted and the batch
    runs through regardless of worker count. We don't assert on the
    actual parallelism (hard to verify without instrumentation) —
    just that the method accepts and honours the kwarg without error.
    """
    parser = _StubParser()
    orch = ParserOrchestrator(
        parser_chains={DocumentClass.HYBRID_PDF: [parser]},
    )
    pdf = tmp_path / "doc.pdf"
    pdf.write_bytes(b"%PDF-1.4\n" + b"x" * 1024)
    job = BatchJob(
        source_path=pdf,
        doc_class=DocumentClass.HYBRID_PDF,
        work_dir=tmp_path,
    )

    results = orch.process_batch(jobs=[job], max_workers=1)
    assert len(results) == 1
    assert results[0].terminal_status == TerminalStatus.AUTO_ACCEPTED
