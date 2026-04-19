"""Selector resolution for evidence spans.

Validates that a selector points to real text in a document version and
that the stored quote matches the resolved text.
"""

from __future__ import annotations

import hashlib
import logging
import re
from pathlib import Path

from .schemas import (
    EvidenceSpan,
    MarkdownRangeSelector,
    PdfBboxSelector,
    PdfPageSelector,
    TextRangeSelector,
)

logger = logging.getLogger(__name__)


class SelectorResolver:
    """Resolve selectors against source documents and verify quotes."""

    def __init__(self, raw_source_root: Path) -> None:
        self.raw_source_root = Path(raw_source_root)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def resolve(self, span: EvidenceSpan) -> str:
        """Return the text at the selector location.

        Raises ``ValueError`` if the selector cannot be resolved or the
        quote does not match.
        """
        selector = span.selector
        try:
            source_path = self._locate_source(span.document_version_id)
        except FileNotFoundError as exc:
            logger.warning(
                "Evidence-link failure: cannot locate source for %s: %s",
                span.document_version_id,
                exc,
            )
            raise

        if isinstance(selector, PdfBboxSelector):
            resolved = self._resolve_pdf_bbox(source_path, selector)
        elif isinstance(selector, PdfPageSelector):
            resolved = self._resolve_pdf_page(source_path, selector)
        elif isinstance(selector, MarkdownRangeSelector):
            resolved = self._resolve_markdown_range(source_path, selector)
        elif isinstance(selector, TextRangeSelector):
            resolved = self._resolve_text_range(source_path, selector)
        else:
            logger.warning(
                "Evidence-link failure: unsupported selector kind %r for span %s",
                selector.kind,
                span.id,
            )
            raise ValueError(f"Unsupported selector kind: {selector.kind}")

        # Verify quote matches (fuzzy — allow whitespace differences)
        if span.quote and not self._quotes_match(span.quote, resolved):
            logger.warning(
                "Evidence-link failure: quote mismatch for span %s "
                "(expected %r, got %r)",
                span.id,
                span.quote[:80],
                resolved[:80],
            )
            raise ValueError(
                f"Quote mismatch for span {span.id}: "
                f"expected {span.quote[:80]!r}, got {resolved[:80]!r}"
            )

        return resolved

    # ------------------------------------------------------------------
    # Resolution strategies
    # ------------------------------------------------------------------

    def _resolve_pdf_bbox(self, source_path: Path, selector: PdfBboxSelector) -> str:
        # Best-effort: try PyMuPDF to extract text from bbox
        try:
            import fitz  # PyMuPDF
        except ImportError:
            logger.warning("PyMuPDF not installed; falling back to page-only extraction")
            return self._resolve_pdf_page(source_path, PdfPageSelector(page=selector.page))

        doc = fitz.open(str(source_path))
        try:
            page = doc.load_page(selector.page - 1)  # 0-indexed
            rect = fitz.Rect(selector.bbox)
            text = page.get_textbox(rect).strip()
            if text:
                return text
        finally:
            doc.close()

        return self._resolve_pdf_page(source_path, PdfPageSelector(page=selector.page))

    def _resolve_pdf_page(self, source_path: Path, selector: PdfPageSelector) -> str:
        try:
            import fitz  # PyMuPDF
        except ImportError:
            # Fallback: no text extraction possible
            return ""

        doc = fitz.open(str(source_path))
        try:
            page = doc.load_page(selector.page - 1)
            return page.get_text().strip()
        finally:
            doc.close()

    def _resolve_markdown_range(self, source_path: Path, selector: MarkdownRangeSelector) -> str:
        text = source_path.read_text(encoding="utf-8")
        lines = text.splitlines()

        # If heading_path is provided, try to narrow to heading block
        if selector.heading_path:
            start_idx, end_idx = self._find_heading_block(lines, selector.heading_path)
            if start_idx is not None:
                lines = lines[start_idx:end_idx]
                # Re-index line numbers relative to block start
                line_start = selector.line_start or 1
                line_end = selector.line_end or len(lines)
                chunk = "\n".join(lines[line_start - 1 : line_end])
                return self._apply_char_range(chunk, selector.char_start, selector.char_end)

        # Absolute line range
        if selector.line_start is not None and selector.line_end is not None:
            chunk = "\n".join(lines[selector.line_start - 1 : selector.line_end])
            return self._apply_char_range(chunk, selector.char_start, selector.char_end)

        # Char range on full text
        return self._apply_char_range(text, selector.char_start, selector.char_end)

    def _resolve_text_range(self, source_path: Path, selector: TextRangeSelector) -> str:
        text = source_path.read_text(encoding="utf-8")
        return self._apply_char_range(text, selector.char_start, selector.char_end)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _locate_source(self, document_version_id: str) -> Path:
        """Best-effort locate source file from document_version_id."""
        # document_version_id format: docv-<slug>-v1
        # document_id format: doc-<slug>
        # We search raw_source_root for files matching the slug
        slug = document_version_id.replace("docv-", "").rsplit("-v", 1)[0]
        candidates = list(self.raw_source_root.rglob(f"*{slug}*"))
        pdf_candidates = [c for c in candidates if c.suffix.lower() == ".pdf"]
        md_candidates = [c for c in candidates if c.suffix.lower() in (".md", ".markdown")]
        for c in pdf_candidates + md_candidates:
            if c.is_file():
                return c
        raise FileNotFoundError(f"Could not locate source for document_version_id={document_version_id}")

    def _find_heading_block(
        self, lines: list[str], heading_path: list[str]
    ) -> tuple[int | None, int | None]:
        """Find the line range of a heading block in markdown text."""
        target_heading = heading_path[-1] if heading_path else ""
        target_level = len(heading_path)
        start_idx: int | None = None

        for i, line in enumerate(lines):
            match = re.match(r"^(#{1,6})\s+(.*)", line)
            if match:
                level = len(match.group(1))
                title = match.group(2).strip()
                if title.lower() == target_heading.lower() and level == target_level:
                    start_idx = i
                    break

        if start_idx is None:
            return None, None

        # Find next heading at same or higher level
        end_idx = len(lines)
        for j in range(start_idx + 1, len(lines)):
            match = re.match(r"^(#{1,6})\s+", lines[j])
            if match:
                level = len(match.group(1))
                if level <= target_level:
                    end_idx = j
                    break

        return start_idx, end_idx

    def _apply_char_range(self, text: str, char_start: int | None, char_end: int | None) -> str:
        start = char_start or 0
        end = char_end or len(text)
        return text[start:end]

    def _quotes_match(self, expected: str, actual: str) -> bool:
        """Fuzzy quote match: normalize whitespace and compare."""
        norm = lambda s: " ".join(s.split())
        return norm(expected) == norm(actual) or norm(expected) in norm(actual)
