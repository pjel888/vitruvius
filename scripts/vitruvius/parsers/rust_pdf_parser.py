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
# Sprint CLEANUP-1 C3.1 — imported as a module-level attribute so the
# page-isolation parity test can ``monkeypatch.setattr`` it on this
# module (same pattern as the spatial fast-path callers in
# ``spatial._feature_gate``). Do NOT inline ``load_features`` inside
# ``parse()`` — the monkeypatch would not take effect.
from vitruvius.spatial._feature_gate import _load_features_cached


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

        # Sprint CLEANUP-1 C3.1 — flag-gated per-page error surface.
        # When ``p1b_page_isolation`` is on and the rebuilt wheel
        # exposes ``extract_pdf_text_with_errors``, route through the
        # tuple-returning entry point so we can populate
        # ``ParseResult.failed_pages`` with the 1-indexed page numbers
        # ``lopdf`` could not decode. Flag-off or missing symbol both
        # fall through to the original byte-identical path, preserving
        # the Phase 1B low-spec baseline.
        failed_pages: list[int] = []
        use_error_surface = False
        try:
            _features = _load_features_cached()
        except Exception:
            _features = None
        if _features is not None:
            try:
                use_error_surface = _features.is_enabled("p1b_page_isolation")
            except Exception:
                use_error_surface = False
        if use_error_surface and hasattr(
            vitruvius_rust_pdf, "extract_pdf_text_with_errors"
        ):
            try:
                text, failed_rust = vitruvius_rust_pdf.extract_pdf_text_with_errors(
                    pdf_bytes
                )
                failed_pages = [int(p) for p in failed_rust]
            except ValueError as exc:
                return self._failure(
                    duration_ms=int((time.perf_counter() - start) * 1000),
                    error=f"lopdf extraction failed: {exc}",
                )
        else:
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
            failed_pages=failed_pages,
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
