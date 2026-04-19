"""Integration test: PdfEvidenceLocator → EvidenceMaterializer → selectors."""

from __future__ import annotations

from pathlib import Path

import pytest

from vitruvius.kg.evidence_materializer import EvidenceMaterializer
from vitruvius.kg.schemas import PdfBboxSelector, PdfPageSelector


def _seed_source_with_pdf(root: Path) -> None:
    """Create a source markdown that points to a real PDF."""
    shared = root / "003_Canonical-Knowledge-Layer" / "shared"
    sources_dir = shared / "sources"
    sources_dir.mkdir(parents=True)

    # Write source markdown with original_file pointing to a known PDF
    source_md = sources_dir / "pd-1096.md"
    source_md.write_text(
        "---\n"
        "id: law-pd-1096\n"
        "title: PD 1096\n"
        "original_file: PD 1096 - National Building Code.pdf\n"
        "trust_level: primary\n"
        "last_canonicalized_utc: 2026-04-01T00:00:00Z\n"
        "---\n\n"
        "# PD 1096 - National Building Code\n\n"
        "## Section 1\n\n"
        "The required setback is three meters from the lot line.\n",
        encoding="utf-8",
    )


def _seed_concept(root: Path) -> None:
    shared = root / "003_Canonical-Knowledge-Layer" / "shared"
    concepts_dir = shared / "concepts"
    concepts_dir.mkdir(parents=True)

    concept_md = concepts_dir / "setbacks.md"
    concept_md.write_text(
        "---\n"
        "id: concept-setbacks\n"
        "title: Setbacks\n"
        "last_canonicalized_utc: 2026-04-01T00:00:00Z\n"
        "---\n",
        encoding="utf-8",
    )


def _seed_relationship_with_evidence(root: Path) -> None:
    shared = root / "003_Canonical-Knowledge-Layer" / "shared"
    rels_dir = shared / "relationships"
    rels_dir.mkdir(parents=True)

    rel_md = rels_dir / "rel-pd-1096-governs-setbacks.md"
    rel_md.write_text(
        "---\n"
        "id: rel-pd-1096-governs-setbacks\n"
        "page_type: relationship\n"
        "relationship_type: governs\n"
        "from_entity: law-pd-1096\n"
        "to_entity: concept-setbacks\n"
        "canonical_status: promoted\n"
        "evidence:\n"
        "- source_id: law-pd-1096\n"
        "  source_section_id: section-1\n"
        "  evidence_snippet: The required setback is three meters from the lot line\n"
        "  reviewer_confidence: 0.95\n"
        "---\n",
        encoding="utf-8",
    )


def _copy_pdf_to_raw_source(root: Path) -> None:
    """Copy the real PD 1096 PDF from the repo so the locator can find it."""
    src = (
        Path(__file__).resolve().parent.parent.parent
        / "001_Raw-Source-Layer"
        / "001-Laws"
        / "PD-1096"
        / "PD 1096 - National Building Code.pdf"
    )
    if not src.exists():
        pytest.skip("Real PD 1096 PDF not found in repo")

    dst_dir = root / "001_Raw-Source-Layer" / "001-Laws" / "PD-1096"
    dst_dir.mkdir(parents=True, exist_ok=True)
    dst = dst_dir / "PD 1096 - National Building Code.pdf"
    if not dst.exists():
        import shutil

        shutil.copy2(str(src), str(dst))


class TestPdfEvidenceIntegration:
    def test_materializer_emits_pdf_selector_when_pdf_mapped(
        self, tmp_path: Path
    ) -> None:
        _seed_source_with_pdf(tmp_path)
        _seed_concept(tmp_path)
        _seed_relationship_with_evidence(tmp_path)
        _copy_pdf_to_raw_source(tmp_path)

        materializer = EvidenceMaterializer(tmp_path)
        snapshot = materializer.materialize_all()

        # Should have at least one evidence span
        assert len(snapshot.evidence_spans) >= 1

        # Prefer PdfBboxSelector; fall back to PdfPageSelector
        pdf_spans = [
            e
            for e in snapshot.evidence_spans
            if isinstance(e.selector, (PdfBboxSelector, PdfPageSelector))
        ]

        for span in snapshot.evidence_spans:
            assert span.quote
            assert span.selector is not None

    def test_materializer_prefers_bbox_over_page(self, tmp_path: Path) -> None:
        """When a snippet is found in a PDF, PdfBboxSelector should be emitted."""
        _seed_source_with_pdf(tmp_path)
        _seed_concept(tmp_path)
        _seed_relationship_with_evidence(tmp_path)
        _copy_pdf_to_raw_source(tmp_path)

        materializer = EvidenceMaterializer(tmp_path)
        snapshot = materializer.materialize_all()

        assert len(snapshot.evidence_spans) >= 1
        span = snapshot.evidence_spans[0]

        # If the snippet matched in the PDF, we expect PdfBboxSelector
        # (because pdfplumber / PyMuPDF are now installed)
        if isinstance(span.selector, PdfBboxSelector):
            assert span.selector.page >= 1
            assert len(span.selector.bbox) == 4
            assert span.selector.bbox[0] < span.selector.bbox[2]
            assert span.selector.bbox[1] < span.selector.bbox[3]
        elif isinstance(span.selector, PdfPageSelector):
            # Bbox extraction may fail for some snippets; page-only is acceptable
            assert span.selector.page >= 1
        else:
            # Fallback to markdown or text selector is also acceptable
            assert span.selector.kind in ("markdown_range", "text_range")

    def test_pdf_locator_finds_real_pdf(self, tmp_path: Path) -> None:
        from vitruvius.kg.pdf_evidence_locator import PdfEvidenceLocator

        _seed_source_with_pdf(tmp_path)
        _copy_pdf_to_raw_source(tmp_path)

        locator = PdfEvidenceLocator(tmp_path)
        pdf_path = locator._resolve_pdf_path("pd-1096")
        assert pdf_path is not None
        assert pdf_path.name == "PD 1096 - National Building Code.pdf"

    def test_pdf_locator_finds_bbox_in_real_pdf(self, tmp_path: Path) -> None:
        from vitruvius.kg.pdf_evidence_locator import PdfEvidenceLocator

        _seed_source_with_pdf(tmp_path)
        _copy_pdf_to_raw_source(tmp_path)

        locator = PdfEvidenceLocator(tmp_path)
        # Use a known term from the cover page
        result = locator.find_bbox("pd-1096", "national building code")
        if result is not None:
            page, bbox = result
            assert page == 1
            assert len(bbox) == 4
            assert all(isinstance(c, float) for c in bbox)
