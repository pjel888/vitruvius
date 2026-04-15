"""Sprint RUST-PDF-1 Task 1 — Python binding smoke test."""
from __future__ import annotations

import pytest

rust_pdf = pytest.importorskip("vitruvius_rust_pdf")


def test_version_is_nonempty() -> None:
    assert rust_pdf.version()
    assert isinstance(rust_pdf.version(), str)


def test_extract_empty_bytes_returns_empty() -> None:
    assert rust_pdf.extract_pdf_text(b"") == ""


def test_extract_invalid_pdf_raises_value_error() -> None:
    with pytest.raises(ValueError, match="lopdf failed"):
        rust_pdf.extract_pdf_text(b"not a pdf")


def test_extract_minimum_viable_pdf_returns_string(tmp_path) -> None:
    """Generate a real minimum-viable PDF via pypdf.PdfWriter, then
    verify that lopdf can load it and extract_pdf_text returns a
    string. This is a round-trip smoke test across two independent
    PDF implementations — pypdf creates, lopdf reads."""
    pypdf = pytest.importorskip("pypdf")
    writer = pypdf.PdfWriter()
    writer.add_blank_page(width=612, height=792)
    out = tmp_path / "minimal.pdf"
    with out.open("wb") as f:
        writer.write(f)

    pdf_bytes = out.read_bytes()
    assert pdf_bytes.startswith(b"%PDF")

    result = rust_pdf.extract_pdf_text(pdf_bytes)
    assert isinstance(result, str)
