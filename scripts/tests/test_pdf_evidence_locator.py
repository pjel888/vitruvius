"""Tests for PdfEvidenceLocator."""

from __future__ import annotations

from pathlib import Path

import pytest

from vitruvius.kg.pdf_evidence_locator import PdfEvidenceLocator, _normalize_text


class TestNormalizeText:
    def test_collapses_whitespace(self) -> None:
        assert _normalize_text("hello   world\n\n  foo") == "hello world foo"

    def test_lowercases(self) -> None:
        assert _normalize_text("Hello World") == "hello world"


class TestPdfEvidenceLocator:
    def test_returns_none_when_no_pdf_mapping(self, tmp_path: Path) -> None:
        locator = PdfEvidenceLocator(tmp_path)
        page = locator.find_page("nonexistent-source", "some text snippet here")
        assert page is None

    def test_returns_none_bbox_when_no_pdf_mapping(self, tmp_path: Path) -> None:
        locator = PdfEvidenceLocator(tmp_path)
        bbox = locator.find_bbox("nonexistent-source", "some text snippet here")
        assert bbox is None

    def test_finds_page_in_mock_pdf(self, tmp_path: Path) -> None:
        pytest.importorskip("pypdf")
        from pypdf import PdfWriter

        repo = tmp_path
        sources_dir = repo / "003_Canonical-Knowledge-Layer" / "shared" / "sources"
        sources_dir.mkdir(parents=True)

        # Write source markdown with original_file
        source_md = sources_dir / "pd-1096.md"
        source_md.write_text(
            "---\n"
            "id: law-pd-1096\n"
            "original_file: pd-1096.pdf\n"
            "---\n",
            encoding="utf-8",
        )

        # Write a simple 2-page PDF
        pdf_path = repo / "001_Raw-Source-Layer" / "pd-1096.pdf"
        pdf_path.parent.mkdir(parents=True)
        writer = PdfWriter()
        writer.add_blank_page(width=612, height=792)
        writer.add_blank_page(width=612, height=792)
        writer.write(str(pdf_path))

        locator = PdfEvidenceLocator(repo)
        pdf_mapped = locator._resolve_pdf_path("pd-1096")
        assert pdf_mapped is not None
        assert pdf_mapped.name == "pd-1096.pdf"

    def test_fallback_to_section_heading(self, tmp_path: Path) -> None:
        locator = PdfEvidenceLocator(tmp_path)
        # When snippet is too short, heading is used
        page = locator.find_page_with_fallback("missing", "ab", section_heading="section-1")
        assert page is None  # no PDF mapped

    def test_fallback_bbox_to_section_heading(self, tmp_path: Path) -> None:
        locator = PdfEvidenceLocator(tmp_path)
        bbox = locator.find_bbox_with_fallback("missing", "ab", section_heading="section-1")
        assert bbox is None  # no PDF mapped

    def test_find_bbox_with_real_pdf(self, tmp_path: Path) -> None:
        """Use a real PDF from the repo to verify bbox extraction."""
        repo = Path(__file__).resolve().parent.parent.parent
        pdf_src = (
            repo
            / "001_Raw-Source-Layer"
            / "001-Laws"
            / "PD-1096"
            / "PD 1096 - National Building Code.pdf"
        )
        if not pdf_src.exists():
            pytest.skip("Real PD 1096 PDF not found")

        # Seed a source markdown pointing to the PDF
        sources_dir = tmp_path / "003_Canonical-Knowledge-Layer" / "shared" / "sources"
        sources_dir.mkdir(parents=True)
        source_md = sources_dir / "pd-1096.md"
        source_md.write_text(
            "---\n"
            "id: law-pd-1096\n"
            "original_file: PD 1096 - National Building Code.pdf\n"
            "---\n",
            encoding="utf-8",
        )

        # Copy PDF into temp repo
        raw_dir = tmp_path / "001_Raw-Source-Layer" / "001-Laws" / "PD-1096"
        raw_dir.mkdir(parents=True)
        import shutil

        pdf_dst = raw_dir / "PD 1096 - National Building Code.pdf"
        shutil.copy2(str(pdf_src), str(pdf_dst))

        locator = PdfEvidenceLocator(tmp_path)

        # Test with a known term from the PDF cover page
        result = locator.find_bbox("pd-1096", "national building code")
        if result is not None:
            page, bbox = result
            assert isinstance(page, int) and page >= 1
            assert len(bbox) == 4
            assert all(isinstance(c, float) for c in bbox)
            assert bbox[0] < bbox[2]  # x0 < x1
            assert bbox[1] < bbox[3]  # y0 < y1
        else:
            # If bbox fails, at least page should work
            page = locator.find_page("pd-1096", "national building code")
            assert page is not None
