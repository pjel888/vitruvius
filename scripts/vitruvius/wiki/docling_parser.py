"""Sprint WIKI Stream WIKI.1 — Docling PDF → Markdown converter wrapper.

Thin facade around :mod:`docling.document_converter` that produces a
:class:`DoclingParseResult` frozen dataclass. Exceptions (missing file,
non-PDF, Docling internal failure) are caught and surfaced in the
``error`` field so callers can decide whether to skip the source or
escalate — no raises through normal use.

The heavy Docling import is lazy so ``vitruvius.wiki.docling_parser``
can be imported on hosts without the package installed.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass(frozen=True)
class DoclingParseResult:
    markdown: str
    heading_count: int
    table_count: int
    error: Optional[str]


def convert_pdf_to_markdown(pdf_path: Path) -> DoclingParseResult:
    """Convert a single PDF to Markdown via Docling's document converter.

    Returns an empty-markdown result with ``error`` populated when:
      * the input file is missing
      * the extension is not ``.pdf``
      * Docling raises during conversion
    """
    pdf_path = Path(pdf_path)
    if not pdf_path.exists():
        return DoclingParseResult(
            markdown="",
            heading_count=0,
            table_count=0,
            error=f"missing file: {pdf_path}",
        )
    if pdf_path.suffix.lower() != ".pdf":
        return DoclingParseResult(
            markdown="",
            heading_count=0,
            table_count=0,
            error=f"not a PDF: {pdf_path} (suffix={pdf_path.suffix!r})",
        )

    try:
        from docling.document_converter import DocumentConverter

        converter = DocumentConverter()
        conv_result = converter.convert(str(pdf_path))
        doc = getattr(conv_result, "document", None) or conv_result
        markdown = doc.export_to_markdown() if hasattr(doc, "export_to_markdown") else ""
    except Exception as exc:  # Docling can raise a wide variety of errors
        return DoclingParseResult(
            markdown="",
            heading_count=0,
            table_count=0,
            error=f"docling conversion failed: {type(exc).__name__}: {exc}",
        )

    # Cheap structural counts — useful for quality gates later.
    heading_count = sum(1 for line in markdown.splitlines() if line.startswith("#"))
    # A rough proxy for tables: rows with pipe characters.
    table_count = sum(1 for line in markdown.splitlines() if line.count("|") >= 2) // 2

    return DoclingParseResult(
        markdown=markdown,
        heading_count=heading_count,
        table_count=table_count,
        error=None,
    )
