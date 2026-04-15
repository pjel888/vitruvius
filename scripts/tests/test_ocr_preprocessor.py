"""Sprint 1B-M2 Task 1 — OCRPreprocessor tests."""
from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest

from vitruvius.parsers.libreoffice_preprocessor import PreprocessResult
from vitruvius.parsers.ocr_preprocessor import OCRPreprocessor


def test_ocr_preprocessor_rejects_missing_file(tmp_path: Path) -> None:
    pre = OCRPreprocessor()
    missing = tmp_path / "does_not_exist.pdf"

    result = pre.preprocess(source_path=missing, workdir=tmp_path)
    assert isinstance(result, PreprocessResult)
    assert result.pdf_path is None
    assert "does not exist" in (result.error or "").lower()


def test_ocr_preprocessor_rejects_non_pdf(tmp_path: Path) -> None:
    pre = OCRPreprocessor()
    docx = tmp_path / "doc.docx"
    docx.write_text("stub")

    result = pre.preprocess(source_path=docx, workdir=tmp_path)
    assert result.pdf_path is None
    assert "not a pdf" in (result.error or "").lower()


def test_ocr_preprocessor_happy_path_mocks_ocrmypdf(tmp_path: Path) -> None:
    pre = OCRPreprocessor()
    scanned = tmp_path / "scanned.pdf"
    scanned.write_bytes(b"%PDF-1.4\n" + b"x" * 1024)

    def fake_ocr(input_file, output_file, **kwargs):
        Path(output_file).write_bytes(b"%PDF-1.4\n" + b"y" * 2048)
        return 0

    with patch(
        "vitruvius.parsers.ocr_preprocessor.ocrmypdf.ocr",
        side_effect=fake_ocr,
    ):
        result = pre.preprocess(source_path=scanned, workdir=tmp_path)

    assert result.pdf_path is not None
    assert result.pdf_path.exists()
    assert result.pdf_path.suffix == ".pdf"
    assert result.pdf_path != scanned  # not overwriting the input
    assert result.error is None
    assert result.duration_ms >= 0


def test_ocr_preprocessor_wraps_ocrmypdf_error(tmp_path: Path) -> None:
    pre = OCRPreprocessor()
    scanned = tmp_path / "scanned.pdf"
    scanned.write_bytes(b"%PDF-1.4\n")

    def fake_ocr(input_file, output_file, **kwargs):
        raise RuntimeError("tesseract missing language data")

    with patch(
        "vitruvius.parsers.ocr_preprocessor.ocrmypdf.ocr",
        side_effect=fake_ocr,
    ):
        result = pre.preprocess(source_path=scanned, workdir=tmp_path)

    assert result.pdf_path is None
    assert "tesseract" in (result.error or "").lower()
