"""Tests for SelectorResolver."""

from __future__ import annotations

import pytest

from vitruvius.kg.schemas import EvidenceSpan, MarkdownRangeSelector, PdfPageSelector, TextRangeSelector
from vitruvius.kg.selector_resolver import SelectorResolver


@pytest.fixture
def resolver(tmp_path: pytest.TempPathFactory) -> SelectorResolver:
    return SelectorResolver(tmp_path)


def test_resolve_text_range(tmp_path: pytest.TempPathFactory) -> None:
    md_file = tmp_path / "test.md"
    md_file.write_text("Hello world\nSecond line", encoding="utf-8")

    resolver = SelectorResolver(tmp_path)
    span = EvidenceSpan(
        id="span-001",
        document_id="doc-test",
        document_version_id="docv-test-v1",
        selector=TextRangeSelector(char_start=0, char_end=11, quote="Hello world"),
        quote="Hello world",
        normalized_text="Hello world",
        parser="test",
        checksum="a" * 64,
    )
    resolved = resolver.resolve(span)
    assert resolved == "Hello world"


def test_resolve_markdown_heading_block(tmp_path: pytest.TempPathFactory) -> None:
    md_file = tmp_path / "test.md"
    md_file.write_text("# Heading\nContent line 1\nContent line 2\n# Next\nSkip", encoding="utf-8")

    resolver = SelectorResolver(tmp_path)
    span = EvidenceSpan(
        id="span-002",
        document_id="doc-test",
        document_version_id="docv-test-v1",
        selector=MarkdownRangeSelector(
            heading_path=["Heading"],
            line_start=1,
            line_end=2,
            quote="Content line 1",
        ),
        quote="Content line 1",
        normalized_text="Content line 1",
        parser="test",
        checksum="b" * 64,
    )
    resolved = resolver.resolve(span)
    assert "Content line 1" in resolved


def test_quote_mismatch_raises(tmp_path: pytest.TempPathFactory) -> None:
    md_file = tmp_path / "test.md"
    md_file.write_text("Actual text", encoding="utf-8")

    resolver = SelectorResolver(tmp_path)
    span = EvidenceSpan(
        id="span-003",
        document_id="doc-test",
        document_version_id="docv-test-v1",
        selector=TextRangeSelector(char_start=0, char_end=11, quote="Actual text"),
        quote="Wrong quote",
        normalized_text="Actual text",
        parser="test",
        checksum="c" * 64,
    )
    with pytest.raises(ValueError, match="Quote mismatch"):
        resolver.resolve(span)


def test_locate_source_not_found(tmp_path: pytest.TempPathFactory) -> None:
    resolver = SelectorResolver(tmp_path)
    with pytest.raises(FileNotFoundError):
        resolver._locate_source("docv-nonexistent-v1")
