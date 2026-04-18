"""Sprint 1B-M1 Task 1 — DoclingParser (BaseParser implementation).

Thin adapter around :func:`vitruvius.wiki.docling_parser.convert_pdf_to_markdown`
that reshapes the Sprint WIKI :class:`DoclingParseResult` into the Phase 1B
:class:`BaseParser` contract.

Delegation pattern: the heavy Docling import lives inside the wiki
module. This file only imports the wiki wrapper, so ``from
vitruvius.parsers.docling_parser import DoclingParser`` is cheap
even when docling is not installed (the wrapper's lazy-import
error only surfaces at :meth:`parse` time).
"""
from __future__ import annotations

import time
from pathlib import Path
from typing import Any

from vitruvius.parsers.base_parser import BaseParser, ParseResult, ParserTelemetry
from vitruvius.parsers.section_extractor import post_process_parse_result
from vitruvius.wiki.docling_parser import convert_pdf_to_markdown


class DoclingParser(BaseParser):
    """Parser chain entry for docling-backed PDF conversion."""

    parser_id = "docling"
    parser_version = "wiki-1.0"

    def parse(self, source_path: Path, work_dir: Path) -> ParseResult:
        start = time.perf_counter()
        wiki_result = convert_pdf_to_markdown(pdf_path=source_path)
        duration_ms = int((time.perf_counter() - start) * 1000)

        if wiki_result.error is not None:
            telemetry = ParserTelemetry(
                parser_id=self.parser_id,
                attempt_index=0,
                duration_ms=duration_ms,
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
                valid=False,
                error=wiki_result.error,
            )
            return ParseResult(
                markdown_text="",
                telemetry=telemetry,
                sidecar_metadata={},
            )

        markdown = wiki_result.markdown
        telemetry = ParserTelemetry(
            parser_id=self.parser_id,
            attempt_index=0,
            duration_ms=duration_ms,
            pages_total=0,  # docling facade does not report this today
            pages_processed=0,
            page_coverage_ratio=1.0 if markdown else 0.0,
            text_length=len(markdown),
            md_length=len(markdown),
            headers=wiki_result.heading_count,
            tables=wiki_result.table_count,
            images=0,
            captions=0,
            ocr_applied=False,
            confidence=1.0 if markdown else 0.0,
            valid=bool(markdown),
            error=None if markdown else "empty markdown",
        )

        sidecar: dict[str, Any] = {
            "parser_id": self.parser_id,
            "parser_version": self.parser_version,
            "heading_count": wiki_result.heading_count,
            "table_count": wiki_result.table_count,
        }

        return post_process_parse_result(ParseResult(
            markdown_text=markdown,
            telemetry=telemetry,
            sidecar_metadata=sidecar,
        ))
