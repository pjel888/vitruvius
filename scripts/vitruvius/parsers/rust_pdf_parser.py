"""Sprint 1B-M3 Task 2 — RustPdfParser(BaseParser).

Thin adapter around vitruvius_rust_pdf.extract_pdf_text that reshapes
the lopdf output into the Phase 1B BaseParser contract. Emits telemetry
with:

- pages_total from form-feed count in the Rust output
- headers from naive '#'-line parsing (lopdf doesn't detect headings)
- tables = 0 (lopdf can't detect tables)
- ocr_applied = False (lopdf doesn't OCR; scanned PDFs go through
  OCRPreprocessor first per the Tranche 2 design)

Low-spec alignment: AD-033 measured vitruvius_rust_pdf at 13.7 MB
peak RSS vs docling's 659.5 MB on synthetic PDFs. AD-034 quality
spot check showed 0.9925 LCS similarity with pypdf on a real
architecture history PDF. This parser is the primary low-spec
entry point for text_pdf_simple and hybrid_pdf chains when
``features.p1b_rust_pdf_parser`` is on.
"""
from __future__ import annotations

import time
from pathlib import Path
from typing import Any

from vitruvius.parsers.base_parser import BaseParser, ParseResult, ParserTelemetry


class RustPdfParser(BaseParser):
    parser_id = "rust_pdf"
    parser_version = "vitruvius_rust_pdf-0.1.0"

    def parse(self, source_path: Path, work_dir: Path) -> ParseResult:
        start = time.perf_counter()
        source_path = Path(source_path)

        if not source_path.exists():
            return self._failure(
                duration_ms=int((time.perf_counter() - start) * 1000),
                error=f"missing file: {source_path}",
            )

        try:
            pdf_bytes = source_path.read_bytes()
        except OSError as exc:
            return self._failure(
                duration_ms=int((time.perf_counter() - start) * 1000),
                error=f"read error: {exc}",
            )

        if len(pdf_bytes) == 0:
            return self._failure(
                duration_ms=int((time.perf_counter() - start) * 1000),
                error="empty file (0 bytes)",
            )

        try:
            import vitruvius_rust_pdf
        except ImportError as exc:
            return self._failure(
                duration_ms=int((time.perf_counter() - start) * 1000),
                error=f"vitruvius_rust_pdf not installed: {exc}",
            )

        try:
            text = vitruvius_rust_pdf.extract_pdf_text(pdf_bytes)
        except ValueError as exc:
            return self._failure(
                duration_ms=int((time.perf_counter() - start) * 1000),
                error=f"lopdf extraction failed: {exc}",
            )

        duration_ms = int((time.perf_counter() - start) * 1000)
        pages_total = text.count("\x0c") if text else 0
        md_pages = [p for p in text.split("\x0c") if p.strip()]
        markdown = "\n\n".join(md_pages)
        headers = sum(1 for line in markdown.splitlines() if line.startswith("#"))

        telemetry = ParserTelemetry(
            parser_id=self.parser_id,
            attempt_index=0,
            duration_ms=duration_ms,
            pages_total=pages_total,
            pages_processed=pages_total,
            page_coverage_ratio=1.0 if pages_total > 0 else 0.0,
            text_length=len(text),
            md_length=len(markdown),
            headers=headers,
            tables=0,
            images=0,
            captions=0,
            ocr_applied=False,
            confidence=1.0 if markdown else 0.0,
            valid=bool(markdown),
            error=None if markdown else "empty extraction",
        )

        sidecar: dict[str, Any] = {
            "parser_id": self.parser_id,
            "parser_version": self.parser_version,
            "page_count": pages_total,
            "bytes_in": len(pdf_bytes),
        }
        return ParseResult(
            markdown_text=markdown,
            telemetry=telemetry,
            sidecar_metadata=sidecar,
        )

    def _failure(self, *, duration_ms: int, error: str) -> ParseResult:
        return ParseResult(
            markdown_text="",
            telemetry=ParserTelemetry(
                parser_id=self.parser_id,
                attempt_index=0,
                duration_ms=duration_ms,
                pages_total=0,
                pages_processed=0,
                page_coverage_ratio=0.0,
                text_length=0,
                md_length=0,
                headers=0,
                tables=0,
                images=0,
                captions=0,
                ocr_applied=False,
                confidence=0.0,
                valid=False,
                error=error,
            ),
            sidecar_metadata={},
        )
