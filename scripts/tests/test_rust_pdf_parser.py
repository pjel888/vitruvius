"""Sprint 1B-M3 Task 2 — RustPdfParser tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from vitruvius.parsers.base_parser import BaseParser, ParseResult
from vitruvius.parsers.rust_pdf_parser import RustPdfParser

vitruvius_rust_pdf = pytest.importorskip("vitruvius_rust_pdf")


def test_rust_pdf_parser_is_base_parser() -> None:
    parser = RustPdfParser()
    assert isinstance(parser, BaseParser)
    assert parser.parser_id == "rust_pdf"
    assert parser.parser_version


def test_rust_pdf_parser_missing_file_returns_failure(tmp_path: Path) -> None:
    parser = RustPdfParser()
    missing = tmp_path / "does_not_exist.pdf"
    result = parser.parse(missing, tmp_path)
    assert isinstance(result, ParseResult)
    assert result.telemetry.valid is False
    assert "missing file" in (result.telemetry.error or "").lower()


def test_rust_pdf_parser_empty_file_returns_failure(tmp_path: Path) -> None:
    parser = RustPdfParser()
    empty = tmp_path / "empty.pdf"
    empty.write_bytes(b"")
    result = parser.parse(empty, tmp_path)
    assert result.telemetry.valid is False
    assert "empty" in (result.telemetry.error or "").lower()


def test_rust_pdf_parser_happy_path_with_pypdf_generated_pdf(tmp_path: Path) -> None:
    pypdf = pytest.importorskip("pypdf")
    writer = pypdf.PdfWriter()
    writer.add_blank_page(width=612, height=792)
    writer.add_blank_page(width=612, height=792)
    pdf_path = tmp_path / "two_pages.pdf"
    with pdf_path.open("wb") as f:
        writer.write(f)

    parser = RustPdfParser()
    result = parser.parse(pdf_path, tmp_path)
    assert isinstance(result, ParseResult)
    assert result.telemetry.parser_id == "rust_pdf"
    assert result.telemetry.duration_ms >= 0
    # 2 form-feeds in the raw text → 2 pages
    assert result.telemetry.pages_total == 2


def test_rust_pdf_parser_wraps_lopdf_error(tmp_path: Path) -> None:
    parser = RustPdfParser()
    bad = tmp_path / "not_a_pdf.pdf"
    bad.write_bytes(b"definitely not a PDF")
    result = parser.parse(bad, tmp_path)
    assert result.telemetry.valid is False
    assert "lopdf" in (result.telemetry.error or "").lower()
