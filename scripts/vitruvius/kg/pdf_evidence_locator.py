"""PDF evidence locator — maps evidence snippets to PDF page numbers and bounding boxes.

Uses ``pypdf`` (already a project dependency) for page-level text search and
``pdfplumber`` (preferred) or ``PyMuPDF`` (fallback) for bounding-box extraction.
Produces ``PdfPageSelector`` and ``PdfBboxSelector`` data for EvidenceSpan records
when the original source is a PDF.
"""

from __future__ import annotations

import logging
import re
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


def _normalize_text(text: str) -> str:
    """Collapse whitespace and lower-case for fuzzy matching."""
    return re.sub(r"\s+", " ", text.strip().lower())


def _load_frontmatter(path: Path) -> dict[str, Any] | None:
    """Minimal frontmatter loader that tolerates colons in values."""
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    try:
        import yaml

        data = yaml.safe_load(text[3:end].strip())
    except Exception:
        return None
    return data if isinstance(data, dict) else None


class PdfEvidenceLocator:
    """Find PDF page numbers and bounding boxes for evidence snippets."""

    def __init__(self, repo_root: Path | str) -> None:
        self.repo_root = Path(repo_root)
        self._source_pdf_index: dict[str, Path] = {}
        self._pdf_cache: dict[str, Any] = {}  # path -> PdfReader

    # -- public API ----------------------------------------------------------

    def find_page(self, source_slug: str, text_snippet: str) -> int | None:
        """Return 1-based page number where *text_snippet* appears, or None."""
        pdf_path = self._resolve_pdf_path(source_slug)
        if pdf_path is None:
            return None

        reader = self._get_reader(pdf_path)
        if reader is None:
            return None

        needle = _normalize_text(text_snippet)
        if len(needle) < 10:
            # Too short for reliable matching
            return None

        for idx, page in enumerate(reader.pages):
            page_text = _normalize_text(page.extract_text() or "")
            if needle in page_text:
                return idx + 1  # 1-based

        logger.debug("Exact match failed for %s, trying fuzzy", source_slug)
        return self._fuzzy_page_search(reader, needle)

    def find_bbox(
        self, source_slug: str, text_snippet: str
    ) -> tuple[int, list[float]] | None:
        """Return (1-based page, [x0, y0, x1, y1]) where *text_snippet* appears.

        Uses ``pdfplumber`` first, then ``PyMuPDF`` as fallback.
        Returns ``None`` if no mapping or no match.
        """
        pdf_path = self._resolve_pdf_path(source_slug)
        if pdf_path is None:
            return None

        needle = _normalize_text(text_snippet)
        if len(needle) < 10:
            return None

        # Try pdfplumber first
        result = self._bbox_with_pdfplumber(pdf_path, needle)
        if result is not None:
            return result

        # Fallback to PyMuPDF
        result = self._bbox_with_pymupdf(pdf_path, needle)
        if result is not None:
            return result

        return None

    def find_page_with_fallback(
        self,
        source_slug: str,
        text_snippet: str,
        section_heading: str = "",
    ) -> int | None:
        """Try snippet first, then section heading, then return None."""
        page = self.find_page(source_slug, text_snippet)
        if page is not None:
            return page
        if section_heading:
            page = self.find_page(source_slug, section_heading)
        return page

    def find_bbox_with_fallback(
        self,
        source_slug: str,
        text_snippet: str,
        section_heading: str = "",
    ) -> tuple[int, list[float]] | None:
        """Try snippet bbox first, then section heading bbox, then return None."""
        result = self.find_bbox(source_slug, text_snippet)
        if result is not None:
            return result
        if section_heading:
            result = self.find_bbox(source_slug, section_heading)
        return result

    # -- internal ------------------------------------------------------------

    def _resolve_pdf_path(self, source_slug: str) -> Path | None:
        """Map a source slug (e.g. 'pd-1096') to the original PDF path."""
        if source_slug in self._source_pdf_index:
            return self._source_pdf_index[source_slug]

        # Build index on first miss
        self._build_source_pdf_index()
        return self._source_pdf_index.get(source_slug)

    def _build_source_pdf_index(self) -> None:
        """Walk source markdown files and map slugs to original PDFs."""
        sources_dir = self.repo_root / "003_Canonical-Knowledge-Layer" / "shared" / "sources"
        if not sources_dir.exists():
            return

        for md_path in sources_dir.rglob("*.md"):
            fm = _load_frontmatter(md_path)
            if not fm:
                continue

            source_id = fm.get("id", "")
            if not source_id:
                continue

            slug = source_id.replace("law-", "").replace("handout-", "").replace("irr-", "")
            pdf_candidates: list[str] = []

            # original_file field
            orig = fm.get("original_file", "")
            if isinstance(orig, str) and orig.lower().endswith(".pdf"):
                pdf_candidates.append(orig)

            # source_documents list
            docs = fm.get("source_documents", [])
            if isinstance(docs, list):
                for doc in docs:
                    if isinstance(doc, str) and doc.lower().endswith(".pdf"):
                        pdf_candidates.append(doc)

            for pdf_rel in pdf_candidates:
                # Normalize path separators
                pdf_rel = pdf_rel.replace("//", "/")
                candidate = self.repo_root / pdf_rel
                if candidate.exists():
                    self._source_pdf_index[slug] = candidate
                    self._source_pdf_index[source_id] = candidate
                    break
                # Try searching under 001_Raw-Source-Layer by basename
                basename = Path(pdf_rel).name
                for found in (self.repo_root / "001_Raw-Source-Layer").rglob(basename):
                    self._source_pdf_index[slug] = found
                    self._source_pdf_index[source_id] = found
                    break

    def _get_reader(self, pdf_path: Path) -> Any | None:
        """Return cached pypdf.PdfReader for *pdf_path*."""
        cache_key = str(pdf_path)
        if cache_key in self._pdf_cache:
            return self._pdf_cache[cache_key]
        try:
            from pypdf import PdfReader

            reader = PdfReader(str(pdf_path))
            self._pdf_cache[cache_key] = reader
            return reader
        except Exception as exc:
            logger.warning("Failed to read PDF %s: %s", pdf_path, exc)
            return None

    def _fuzzy_page_search(self, reader: Any, needle: str) -> int | None:
        """Fallback: search for any contiguous 30-char substring of needle."""
        if len(needle) < 30:
            return None
        # Take middle chunk — less likely to be truncated by page breaks
        start = len(needle) // 2 - 15
        sub = needle[start : start + 30]
        for idx, page in enumerate(reader.pages):
            page_text = _normalize_text(page.extract_text() or "")
            if sub in page_text:
                return idx + 1
        return None

    def _bbox_with_pdfplumber(
        self, pdf_path: Path, needle: str
    ) -> tuple[int, list[float]] | None:
        """Search with pdfplumber; return (page, [x0, y0, x1, y1])."""
        try:
            import pdfplumber
        except ImportError:
            return None

        try:
            with pdfplumber.open(str(pdf_path)) as pdf:
                for idx, page in enumerate(pdf.pages):
                    results = page.search(needle)
                    if results:
                        # Use first match; union all char bboxes in the match
                        match = results[0]
                        chars = match.get("chars", [])
                        if chars:
                            x0 = min(c["x0"] for c in chars)
                            y0 = min(c["top"] for c in chars)
                            x1 = max(c["x1"] for c in chars)
                            y1 = max(c["bottom"] for c in chars)
                            return idx + 1, [round(x0, 2), round(y0, 2), round(x1, 2), round(y1, 2)]
                        # Fallback to word-level bbox
                        return (
                            idx + 1,
                            [
                                round(match["x0"], 2),
                                round(match["top"], 2),
                                round(match["x1"], 2),
                                round(match["bottom"], 2),
                            ],
                        )
        except Exception as exc:
            logger.debug("pdfplumber search failed for %s: %s", pdf_path.name, exc)
        return None

    def _bbox_with_pymupdf(
        self, pdf_path: Path, needle: str
    ) -> tuple[int, list[float]] | None:
        """Search with PyMuPDF; return (page, [x0, y0, x1, y1])."""
        try:
            import fitz
        except ImportError:
            return None

        try:
            doc = fitz.open(str(pdf_path))
            for idx in range(len(doc)):
                page = doc[idx]
                rects = page.search_for(needle)
                if rects:
                    r = rects[0]
                    bbox = [round(r.x0, 2), round(r.y0, 2), round(r.x1, 2), round(r.y1, 2)]
                    doc.close()
                    return idx + 1, bbox
            doc.close()
        except Exception as exc:
            logger.debug("PyMuPDF search failed for %s: %s", pdf_path.name, exc)
        return None
