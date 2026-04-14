from __future__ import annotations

from dataclasses import asdict
from pathlib import Path

import pytest

from vitruvius.parsers.base_parser import BaseParser, ParseResult, ParserTelemetry


def _minimal_telemetry() -> ParserTelemetry:
    return ParserTelemetry(
        parser_id="stub_parser",
        attempt_index=0,
        duration_ms=42,
        pages_total=5,
        pages_processed=5,
        page_coverage_ratio=1.0,
        text_length=1024,
        md_length=800,
        headers=3,
        tables=1,
        images=2,
        captions=1,
        ocr_applied=False,
        confidence=0.95,
        valid=True,
    )


def test_parser_telemetry_required_fields():
    t = _minimal_telemetry()
    assert t.parser_id == "stub_parser"
    assert t.attempt_index == 0
    assert t.duration_ms == 42
    assert t.pages_total == 5
    assert t.pages_processed == 5
    assert t.page_coverage_ratio == 1.0
    assert t.text_length == 1024
    assert t.md_length == 800
    assert t.headers == 3
    assert t.tables == 1
    assert t.images == 2
    assert t.captions == 1
    assert t.assets_extracted == []
    assert t.ocr_applied is False
    assert t.confidence == 0.95
    assert t.valid is True
    assert t.error is None


def test_parser_telemetry_rejects_missing_required_fields():
    with pytest.raises(TypeError):
        ParserTelemetry(
            parser_id="stub_parser",
            attempt_index=0,
            duration_ms=42,
        )


def test_parse_result_construction():
    t = _minimal_telemetry()
    result = ParseResult(markdown_text="# Hello", telemetry=t)
    assert result.markdown_text == "# Hello"
    assert result.telemetry is t
    assert result.sidecar_metadata == {}


def test_base_parser_cannot_be_instantiated_directly():
    with pytest.raises(TypeError):
        BaseParser()


def test_base_parser_concrete_subclass_requires_parse_method():
    class IncompleteParser(BaseParser):
        parser_id = "incomplete"
        parser_version = "0.1.0"

    with pytest.raises(TypeError):
        IncompleteParser()


def test_base_parser_subclass_without_parser_id_rejected():
    with pytest.raises(TypeError):
        class NoIdParser(BaseParser):
            parser_version = "0.1.0"

            def parse(self, source_path: Path, work_dir: Path) -> ParseResult:
                raise NotImplementedError


def test_base_parser_subclass_without_parser_version_rejected():
    with pytest.raises(TypeError):
        class NoVersionParser(BaseParser):
            parser_id = "no_version"

            def parse(self, source_path: Path, work_dir: Path) -> ParseResult:
                raise NotImplementedError


def test_base_parser_valid_concrete_subclass_works(tmp_path):
    class StubParser(BaseParser):
        parser_id = "stub"
        parser_version = "1.0.0"

        def parse(self, source_path: Path, work_dir: Path) -> ParseResult:
            t = ParserTelemetry(
                parser_id=self.parser_id,
                attempt_index=0,
                duration_ms=1,
                pages_total=1,
                pages_processed=1,
                page_coverage_ratio=1.0,
                text_length=7,
                md_length=7,
                headers=1,
                tables=0,
                images=0,
                captions=0,
                ocr_applied=False,
                confidence=1.0,
                valid=True,
            )
            return ParseResult(markdown_text="# stub", telemetry=t)

    tmp_file = tmp_path / "input.pdf"
    tmp_file.write_bytes(b"")
    result = StubParser().parse(tmp_file, tmp_path)
    assert result.markdown_text == "# stub"


def test_parser_telemetry_field_order_matches_contract():
    """Regression pin: asdict() key order must exactly match the §6 JSON schema contract."""
    t = ParserTelemetry(
        parser_id="x",
        attempt_index=0,
        duration_ms=0,
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
        valid=True,
    )
    keys = list(asdict(t).keys())
    expected = [
        "parser_id",
        "attempt_index",
        "duration_ms",
        "pages_total",
        "pages_processed",
        "page_coverage_ratio",
        "text_length",
        "md_length",
        "headers",
        "tables",
        "images",
        "captions",
        "assets_extracted",
        "ocr_applied",
        "confidence",
        "valid",
        "error",
    ]
    assert keys == expected, f"Field order mismatch — got: {keys}"


def test_abstract_intermediate_subclass_allowed(tmp_path):
    """Regression pin: intermediate abstract subclasses must not require parser_id/parser_version."""
    import abc

    class OCRCapableParser(BaseParser):
        @abc.abstractmethod
        def preprocess(self, source_path: Path) -> bytes: ...

    class ConcreteOCRParser(OCRCapableParser):
        parser_id = "ocr_stub"
        parser_version = "1.0.0"

        def preprocess(self, source_path: Path) -> bytes:
            return b""

        def parse(self, source_path: Path, work_dir: Path) -> ParseResult:
            t = ParserTelemetry(
                parser_id=self.parser_id,
                attempt_index=0,
                duration_ms=1,
                pages_total=1,
                pages_processed=1,
                page_coverage_ratio=1.0,
                text_length=5,
                md_length=5,
                headers=0,
                tables=0,
                images=0,
                captions=0,
                ocr_applied=True,
                confidence=0.9,
                valid=True,
            )
            return ParseResult(markdown_text="ocr", telemetry=t)

    tmp_file = tmp_path / "input.pdf"
    tmp_file.write_bytes(b"")
    result = ConcreteOCRParser().parse(tmp_file, tmp_path)
    assert isinstance(result, ParseResult)
    assert result.markdown_text == "ocr"


def test_parse_result_positional_rejected():
    """Regression pin: ParseResult must reject positional construction (kw_only=True)."""
    t = _minimal_telemetry()
    with pytest.raises(TypeError):
        ParseResult("md text", {}, t)  # type: ignore[call-arg]
    result = ParseResult(markdown_text="md text", sidecar_metadata={}, telemetry=t)
    assert result.markdown_text == "md text"
