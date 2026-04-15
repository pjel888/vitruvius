"""Sprint WIKI Stream WIKI.1 — Docling PDF→Markdown converter tests."""
from __future__ import annotations

from pathlib import Path

import pytest

# Docling is a heavy transitive (torch + accelerate + ocrmac). Skip
# gracefully on hosts without the dep so the test collection never
# blocks a pipeline that doesn't need wiki ingestion.
pytest.importorskip("docling")

from vitruvius.wiki.docling_parser import (
    DoclingParseResult,
    convert_pdf_to_markdown,
)


def test_returns_empty_parse_for_missing_file(tmp_path: Path) -> None:
    result = convert_pdf_to_markdown(tmp_path / "does-not-exist.pdf")
    assert isinstance(result, DoclingParseResult)
    assert result.markdown == ""
    assert result.error is not None
    assert "missing" in result.error.lower()


def test_rejects_non_pdf_file(tmp_path: Path) -> None:
    txt = tmp_path / "note.txt"
    txt.write_text("plain text, not a PDF", encoding="utf-8")
    result = convert_pdf_to_markdown(txt)
    assert result.markdown == ""
    assert result.error is not None
    assert "pdf" in result.error.lower()


def test_result_dataclass_frozen(tmp_path: Path) -> None:
    res = DoclingParseResult(markdown="x", heading_count=0, table_count=0, error=None)
    with pytest.raises(Exception):
        res.markdown = "y"  # type: ignore[misc]
