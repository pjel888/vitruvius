from __future__ import annotations

import json
from functools import partial
from pathlib import Path
from unittest.mock import patch

import pytest

from vitruvius.parsers.opendataloader_parser import OpenDataLoaderParser

_PATCH_TARGET = "opendataloader_pdf.convert"


def _fake_convert(input_path, output_dir, format, md_content, sidecar_content):
    stem = Path(input_path[0]).stem
    out = Path(output_dir)
    (out / f"{stem}.md").write_text(md_content, encoding="utf-8")
    (out / f"{stem}.json").write_text(json.dumps(sidecar_content), encoding="utf-8")


def _fake_convert_md_only(input_path, output_dir, format):
    stem = Path(input_path[0]).stem
    out = Path(output_dir)
    (out / f"{stem}.md").write_text("# Hello", encoding="utf-8")


def _fake_convert_json_only(input_path, output_dir, format, sidecar_content):
    stem = Path(input_path[0]).stem
    out = Path(output_dir)
    (out / f"{stem}.json").write_text(json.dumps(sidecar_content), encoding="utf-8")


# ---------------------------------------------------------------------------
# 1. class attributes
# ---------------------------------------------------------------------------

def test_parser_id_and_version_are_set():
    assert OpenDataLoaderParser.parser_id == "opendataloader_pdf"
    assert OpenDataLoaderParser.parser_version == "0.1.0"


# ---------------------------------------------------------------------------
# 2. happy-path: result shape
# ---------------------------------------------------------------------------

def test_parse_success_returns_valid_result(tmp_path):
    parser = OpenDataLoaderParser()
    expected_md = "# Title\nBody text."
    sidecar = {"pages_total": 1, "pages_processed": 1}
    side_effect = partial(_fake_convert, md_content=expected_md, sidecar_content=sidecar)
    with patch(_PATCH_TARGET, side_effect=side_effect):
        result = parser.parse(Path("/tmp/doc.pdf"), tmp_path)
    assert result.telemetry.valid is True
    assert result.telemetry.error is None
    assert result.markdown_text == expected_md


# ---------------------------------------------------------------------------
# 3. md_length
# ---------------------------------------------------------------------------

def test_parse_populates_md_length_from_markdown(tmp_path):
    parser = OpenDataLoaderParser()
    expected_md = "x" * 1234
    sidecar = {}
    side_effect = partial(_fake_convert, md_content=expected_md, sidecar_content=sidecar)
    with patch(_PATCH_TARGET, side_effect=side_effect):
        result = parser.parse(Path("/tmp/doc.pdf"), tmp_path)
    assert result.telemetry.md_length == 1234


# ---------------------------------------------------------------------------
# 4. pages from pages_total key
# ---------------------------------------------------------------------------

def test_parse_populates_pages_from_sidecar_pages_total_key(tmp_path):
    parser = OpenDataLoaderParser()
    sidecar = {"pages_total": 10, "pages_processed": 9}
    side_effect = partial(_fake_convert, md_content="text", sidecar_content=sidecar)
    with patch(_PATCH_TARGET, side_effect=side_effect):
        result = parser.parse(Path("/tmp/doc.pdf"), tmp_path)
    assert result.telemetry.pages_total == 10
    assert result.telemetry.pages_processed == 9


# ---------------------------------------------------------------------------
# 5. fallback to page_count key
# ---------------------------------------------------------------------------

def test_parse_falls_back_to_page_count_key(tmp_path):
    parser = OpenDataLoaderParser()
    sidecar = {"page_count": 7}
    side_effect = partial(_fake_convert, md_content="text", sidecar_content=sidecar)
    with patch(_PATCH_TARGET, side_effect=side_effect):
        result = parser.parse(Path("/tmp/doc.pdf"), tmp_path)
    assert result.telemetry.pages_total == 7


# ---------------------------------------------------------------------------
# 6. pages_processed defaults to pages_total
# ---------------------------------------------------------------------------

def test_parse_defaults_pages_processed_to_pages_total(tmp_path):
    parser = OpenDataLoaderParser()
    sidecar = {"pages_total": 5}
    side_effect = partial(_fake_convert, md_content="text", sidecar_content=sidecar)
    with patch(_PATCH_TARGET, side_effect=side_effect):
        result = parser.parse(Path("/tmp/doc.pdf"), tmp_path)
    assert result.telemetry.pages_processed == 5


# ---------------------------------------------------------------------------
# 7. page_coverage_ratio
# ---------------------------------------------------------------------------

def test_parse_computes_page_coverage_ratio(tmp_path):
    parser = OpenDataLoaderParser()
    sidecar = {"pages_total": 10, "pages_processed": 8}
    side_effect = partial(_fake_convert, md_content="text", sidecar_content=sidecar)
    with patch(_PATCH_TARGET, side_effect=side_effect):
        result = parser.parse(Path("/tmp/doc.pdf"), tmp_path)
    assert result.telemetry.page_coverage_ratio == pytest.approx(0.8)


# ---------------------------------------------------------------------------
# 8. zero-page coverage — no division error
# ---------------------------------------------------------------------------

def test_parse_page_coverage_zero_on_zero_pages(tmp_path):
    parser = OpenDataLoaderParser()
    sidecar = {"pages_total": 0}
    side_effect = partial(_fake_convert, md_content="text", sidecar_content=sidecar)
    with patch(_PATCH_TARGET, side_effect=side_effect):
        result = parser.parse(Path("/tmp/doc.pdf"), tmp_path)
    assert result.telemetry.page_coverage_ratio == 0.0


# ---------------------------------------------------------------------------
# 9. text_length from sidecar
# ---------------------------------------------------------------------------

def test_parse_reads_text_length_from_sidecar(tmp_path):
    parser = OpenDataLoaderParser()
    sidecar = {"text_length": 5000}
    side_effect = partial(_fake_convert, md_content="text", sidecar_content=sidecar)
    with patch(_PATCH_TARGET, side_effect=side_effect):
        result = parser.parse(Path("/tmp/doc.pdf"), tmp_path)
    assert result.telemetry.text_length == 5000


# ---------------------------------------------------------------------------
# 10. header count
# ---------------------------------------------------------------------------

def test_parse_counts_headers_in_markdown(tmp_path):
    parser = OpenDataLoaderParser()
    md = "# H1\n## H2\nbody\n### H3\n"
    sidecar = {}
    side_effect = partial(_fake_convert, md_content=md, sidecar_content=sidecar)
    with patch(_PATCH_TARGET, side_effect=side_effect):
        result = parser.parse(Path("/tmp/doc.pdf"), tmp_path)
    assert result.telemetry.headers == 3


# ---------------------------------------------------------------------------
# 11. table count
# ---------------------------------------------------------------------------

def test_parse_counts_tables_in_markdown(tmp_path):
    parser = OpenDataLoaderParser()
    md = "| col1 | col2 |\n|---|---|\nrow1\n| col3 | col4 |\n|:--:|:--:|\n"
    sidecar = {}
    side_effect = partial(_fake_convert, md_content=md, sidecar_content=sidecar)
    with patch(_PATCH_TARGET, side_effect=side_effect):
        result = parser.parse(Path("/tmp/doc.pdf"), tmp_path)
    assert result.telemetry.tables == 2


# ---------------------------------------------------------------------------
# 12. image count
# ---------------------------------------------------------------------------

def test_parse_counts_images_in_markdown(tmp_path):
    parser = OpenDataLoaderParser()
    md = "![img1](x)\ntext\n![img2](y)"
    sidecar = {}
    side_effect = partial(_fake_convert, md_content=md, sidecar_content=sidecar)
    with patch(_PATCH_TARGET, side_effect=side_effect):
        result = parser.parse(Path("/tmp/doc.pdf"), tmp_path)
    assert result.telemetry.images == 2


# ---------------------------------------------------------------------------
# 13. ocr_applied is always False
# ---------------------------------------------------------------------------

def test_parse_sets_ocr_applied_false(tmp_path):
    parser = OpenDataLoaderParser()
    sidecar = {}
    side_effect = partial(_fake_convert, md_content="text", sidecar_content=sidecar)
    with patch(_PATCH_TARGET, side_effect=side_effect):
        result = parser.parse(Path("/tmp/doc.pdf"), tmp_path)
    assert result.telemetry.ocr_applied is False


# ---------------------------------------------------------------------------
# 14. confidence is 1.0 on success
# ---------------------------------------------------------------------------

def test_parse_sets_confidence_1_on_success(tmp_path):
    parser = OpenDataLoaderParser()
    sidecar = {}
    side_effect = partial(_fake_convert, md_content="text", sidecar_content=sidecar)
    with patch(_PATCH_TARGET, side_effect=side_effect):
        result = parser.parse(Path("/tmp/doc.pdf"), tmp_path)
    assert result.telemetry.confidence == pytest.approx(1.0)


# ---------------------------------------------------------------------------
# 15. failure when convert raises
# ---------------------------------------------------------------------------

def test_parse_failure_when_convert_raises(tmp_path):
    parser = OpenDataLoaderParser()
    with patch(_PATCH_TARGET, side_effect=RuntimeError("boom")):
        result = parser.parse(Path("/tmp/doc.pdf"), tmp_path)
    assert result.telemetry.valid is False
    assert result.telemetry.error is not None
    assert "boom" in result.telemetry.error or "RuntimeError" in result.telemetry.error
    assert result.markdown_text == ""


# ---------------------------------------------------------------------------
# 16. failure when markdown file missing
# ---------------------------------------------------------------------------

def test_parse_failure_when_markdown_file_missing(tmp_path):
    parser = OpenDataLoaderParser()
    sidecar = {}
    side_effect = partial(_fake_convert_json_only, sidecar_content=sidecar)
    with patch(_PATCH_TARGET, side_effect=side_effect):
        result = parser.parse(Path("/tmp/doc.pdf"), tmp_path)
    assert result.telemetry.valid is False
    assert result.telemetry.error is not None
    assert ".md" in result.telemetry.error or "doc" in result.telemetry.error


# ---------------------------------------------------------------------------
# 17. failure when json file missing
# ---------------------------------------------------------------------------

def test_parse_failure_when_json_file_missing(tmp_path):
    parser = OpenDataLoaderParser()
    with patch(_PATCH_TARGET, side_effect=_fake_convert_md_only):
        result = parser.parse(Path("/tmp/doc.pdf"), tmp_path)
    assert result.telemetry.valid is False
    assert result.telemetry.error is not None
    assert ".json" in result.telemetry.error or "doc" in result.telemetry.error


# ---------------------------------------------------------------------------
# 18. sidecar_metadata file_type
# ---------------------------------------------------------------------------

def test_parse_sidecar_metadata_includes_file_type(tmp_path):
    parser = OpenDataLoaderParser()
    sidecar = {}
    side_effect = partial(_fake_convert, md_content="text", sidecar_content=sidecar)
    with patch(_PATCH_TARGET, side_effect=side_effect):
        result = parser.parse(Path("/tmp/foo.pdf"), tmp_path)
    assert result.sidecar_metadata["file_type"] == "pdf"
