"""Sprint 1B-M1 Task 2 — LibreOfficePreprocessor tests."""
from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest

from vitruvius.parsers.libreoffice_preprocessor import (
    LibreOfficePreprocessor,
    PreprocessResult,
)


def test_preprocessor_missing_soffice_returns_failure(tmp_path: Path) -> None:
    pre = LibreOfficePreprocessor()
    docx = tmp_path / "doc.docx"
    docx.write_text("stub")

    with patch(
        "vitruvius.parsers.libreoffice_preprocessor.find_soffice_executable",
        side_effect=FileNotFoundError("soffice missing"),
    ):
        result = pre.preprocess(source_path=docx, workdir=tmp_path)

    assert isinstance(result, PreprocessResult)
    assert result.pdf_path is None
    assert result.error is not None
    assert "soffice" in result.error.lower()


def test_preprocessor_rejects_non_office_extension(tmp_path: Path) -> None:
    pre = LibreOfficePreprocessor()
    pdf = tmp_path / "already.pdf"
    pdf.write_bytes(b"%PDF-1.4\n")

    result = pre.preprocess(source_path=pdf, workdir=tmp_path)
    assert result.pdf_path is None
    assert "not an office document" in (result.error or "").lower()


def test_preprocessor_happy_path_mocks_soffice(tmp_path: Path) -> None:
    pre = LibreOfficePreprocessor()
    docx = tmp_path / "doc.docx"
    docx.write_text("stub")

    expected_pdf = tmp_path / "doc.pdf"

    def fake_run(*args, **kwargs):
        # Simulate soffice creating the output PDF.
        expected_pdf.write_bytes(b"%PDF-1.4\n")

        class _Ret:
            returncode = 0
            stdout = b""
            stderr = b""

        return _Ret()

    with patch(
        "vitruvius.parsers.libreoffice_preprocessor.find_soffice_executable",
        return_value="/usr/bin/soffice",
    ), patch(
        "vitruvius.parsers.libreoffice_preprocessor.subprocess.run",
        side_effect=fake_run,
    ):
        result = pre.preprocess(source_path=docx, workdir=tmp_path)

    assert result.pdf_path == expected_pdf
    assert result.error is None
    assert result.duration_ms >= 0


def test_preprocessor_wraps_soffice_failure(tmp_path: Path) -> None:
    pre = LibreOfficePreprocessor()
    docx = tmp_path / "doc.docx"
    docx.write_text("stub")

    def fake_run(*args, **kwargs):
        class _Ret:
            returncode = 77
            stdout = b""
            stderr = b"soffice: conversion failed"

        return _Ret()

    with patch(
        "vitruvius.parsers.libreoffice_preprocessor.find_soffice_executable",
        return_value="/usr/bin/soffice",
    ), patch(
        "vitruvius.parsers.libreoffice_preprocessor.subprocess.run",
        side_effect=fake_run,
    ):
        result = pre.preprocess(source_path=docx, workdir=tmp_path)

    assert result.pdf_path is None
    assert "conversion failed" in (result.error or "").lower()
