"""Sprint 1B-M1 Task 1 — DoclingParser tests."""
from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest

from vitruvius.parsers.base_parser import BaseParser, ParseResult, ParserTelemetry
from vitruvius.parsers.docling_parser import DoclingParser


def test_docling_parser_is_base_parser() -> None:
    parser = DoclingParser()
    assert isinstance(parser, BaseParser)
    assert parser.parser_id == "docling"
    assert parser.parser_version


def test_docling_parser_missing_file_returns_failure(tmp_path: Path) -> None:
    parser = DoclingParser()
    missing = tmp_path / "does_not_exist.pdf"
    result = parser.parse(missing, tmp_path)
    assert isinstance(result, ParseResult)
    assert result.telemetry.valid is False
    assert "missing file" in (result.telemetry.error or "").lower()
    assert result.markdown_text == ""


def test_docling_parser_rejects_non_pdf(tmp_path: Path) -> None:
    parser = DoclingParser()
    docx = tmp_path / "sample.docx"
    docx.write_text("not really a docx")
    result = parser.parse(docx, tmp_path)
    assert result.telemetry.valid is False
    assert "not a pdf" in (result.telemetry.error or "").lower()


def test_docling_parser_happy_path_mocks_wiki(tmp_path: Path) -> None:
    """Mock the Sprint WIKI docling wrapper so the test doesn't load Docling itself."""
    from vitruvius.wiki.docling_parser import DoclingParseResult as WikiResult

    parser = DoclingParser()
    pdf = tmp_path / "fake.pdf"
    pdf.write_bytes(b"%PDF-1.4\n")  # minimum-viable PDF marker

    fake_result = WikiResult(
        markdown="# Title\n\nPage body text with several words.",
        heading_count=1,
        table_count=0,
        error=None,
    )

    with patch(
        "vitruvius.parsers.docling_parser.convert_pdf_to_markdown",
        return_value=fake_result,
    ):
        result = parser.parse(pdf, tmp_path)

    assert result.telemetry.valid is True
    assert result.telemetry.parser_id == "docling"
    assert result.telemetry.error is None
    assert result.markdown_text == "# Title\n\nPage body text with several words."
    assert result.telemetry.headers == 1
    assert result.telemetry.tables == 0
    assert result.telemetry.md_length == len(result.markdown_text)


def test_docling_parser_wraps_wiki_error(tmp_path: Path) -> None:
    from vitruvius.wiki.docling_parser import DoclingParseResult as WikiResult

    parser = DoclingParser()
    pdf = tmp_path / "corrupt.pdf"
    pdf.write_bytes(b"%PDF-1.4\n")

    fake_result = WikiResult(
        markdown="",
        heading_count=0,
        table_count=0,
        error="Docling internal failure: bad xref table",
    )

    with patch(
        "vitruvius.parsers.docling_parser.convert_pdf_to_markdown",
        return_value=fake_result,
    ):
        result = parser.parse(pdf, tmp_path)

    assert result.telemetry.valid is False
    assert "Docling internal failure" in (result.telemetry.error or "")
    assert result.markdown_text == ""


def test_docling_parser_populates_section_map(tmp_path: Path) -> None:
    from vitruvius.wiki.docling_parser import DoclingParseResult as WikiResult

    parser = DoclingParser()
    pdf = tmp_path / "doc.pdf"
    pdf.write_bytes(b"%PDF-1.4\n")

    fake_result = WikiResult(
        markdown="# Title\n\nBody.\n\n## Section A\n\nMore body.\n",
        heading_count=2,
        table_count=0,
        error=None,
    )

    with patch(
        "vitruvius.parsers.docling_parser.convert_pdf_to_markdown",
        return_value=fake_result,
    ):
        result = parser.parse(pdf, tmp_path)

    assert result.section_map is not None
    assert len(result.section_map) == 2
    assert result.section_map[0].title == "Title"
    assert result.section_map[1].title == "Section A"
