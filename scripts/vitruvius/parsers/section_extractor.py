"""Markdown section extractor — derives ``SectionBlock`` list from parser output.

This module closes Gate 3 (parser text-only) by post-processing the
``markdown_text`` field of any ``ParseResult`` into a structured
``section_map``.  It reuses the ATX-heading logic from
``ast_chunker`` but emits the lighter ``SectionBlock`` dataclass
expected by the evidence graph ingestion pipeline.

Usage::

    from vitruvius.parsers.section_extractor import derive_section_map
    result = parser.parse(path, work_dir)
    result.section_map = derive_section_map(result.markdown_text)
"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

from .base_parser import SectionBlock

if TYPE_CHECKING:
    from .base_parser import ParseResult


_HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")


def post_process_parse_result(result: "ParseResult") -> "ParseResult":
    """Populate ``section_map`` on a ``ParseResult`` if it is unset.

    This is the recommended hook for every concrete parser to call right
    before returning its ``ParseResult``.
    """
    if result.section_map is None and result.markdown_text:
        result.section_map = derive_section_map(result.markdown_text)
    return result


def derive_section_map(markdown_text: str) -> list[SectionBlock]:
    """Return a list of ``SectionBlock`` objects extracted from ATX headings.

    Each heading becomes a section with line and character offsets.
    The section body spans from the end of the heading line to the
    start of the next heading (or EOF).
    """
    if not markdown_text:
        return []

    # Strip YAML frontmatter so it does not confuse heading detection
    text = markdown_text
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            text = text[end + 4 :].lstrip("\n")

    lines = text.splitlines()
    sections: list[SectionBlock] = []
    current_start_line: int | None = None
    current_char_start: int | None = None
    current_level: int = 2
    current_title: str = ""

    # char offset tracks position in the original *full* markdown_text
    char_offset = markdown_text.find(text) if text is not markdown_text else 0

    for line_idx, line in enumerate(lines, start=1):
        m = _HEADING_RE.match(line)
        if m is None:
            continue

        # Close previous section
        if current_start_line is not None:
            prev_body_end = char_offset + sum(len(l) + 1 for l in lines[: line_idx - 1])
            sections.append(
                SectionBlock(
                    title=current_title,
                    level=current_level,
                    line_start=current_start_line,
                    line_end=line_idx - 1,
                    char_start=current_char_start,
                    char_end=prev_body_end,
                )
            )

        # Start new section
        current_level = len(m.group(1))
        current_title = m.group(2).strip()
        current_start_line = line_idx
        current_char_start = char_offset + sum(len(l) + 1 for l in lines[: line_idx - 1]) + len(line) + 1

    # Close final section
    if current_start_line is not None:
        total_chars = char_offset + sum(len(l) + 1 for l in lines)
        sections.append(
            SectionBlock(
                title=current_title,
                level=current_level,
                line_start=current_start_line,
                line_end=len(lines),
                char_start=current_char_start,
                char_end=total_chars,
            )
        )

    return sections
