"""AST-based semantic chunker — Task C.2.

Parses refined markdown into a heading tree by ATX depth and emits
bounded chunks that carry the full parent chain as metadata. Sections
that exceed the token budget split at paragraph boundaries; we never
cut mid-paragraph.

Token counting is `len(body.split())` — a deliberately cheap proxy so
this module has zero external dependencies. The 512-token default is
a safety margin, not an exact count.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


DEFAULT_MAX_TOKENS = 512

_FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*(?:\n|$)", re.DOTALL)
_HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
_ID_LINE_RE = re.compile(r"^id\s*:\s*(.+?)\s*$", re.MULTILINE)


@dataclass(frozen=True)
class Chunk:
    chunk_id: str
    source_path: str
    source_section_id: str
    parent_titles: tuple[str, ...]
    heading: str
    body: str
    token_count: int


@dataclass
class _Section:
    depth: int
    heading: str
    parent_titles: tuple[str, ...]
    body_lines: list[str]


def _extract_frontmatter(markdown: str) -> tuple[str, str]:
    match = _FRONTMATTER_RE.match(markdown)
    if match is None:
        return "", markdown
    section_id = ""
    id_match = _ID_LINE_RE.search(match.group(1))
    if id_match is not None:
        section_id = id_match.group(1).strip().strip('"').strip("'")
    return section_id, markdown[match.end():]


def _source_slug(source_path: str) -> str:
    stem = Path(source_path).stem
    slug = re.sub(r"[^A-Za-z0-9_.-]+", "-", stem).strip("-")
    return slug or "doc"


def _parse_sections(markdown: str) -> list[_Section]:
    lines = markdown.splitlines()
    sections: list[_Section] = []
    current = _Section(depth=0, heading="", parent_titles=(), body_lines=[])
    chain: list[tuple[int, str]] = []

    for line in lines:
        heading_match = _HEADING_RE.match(line)
        if heading_match is None:
            current.body_lines.append(line)
            continue

        if current.heading or current.body_lines:
            sections.append(current)

        depth = len(heading_match.group(1))
        heading_text = heading_match.group(2).strip()

        while chain and chain[-1][0] >= depth:
            chain.pop()

        parent_titles = tuple(h for _, h in chain)
        current = _Section(
            depth=depth,
            heading=heading_text,
            parent_titles=parent_titles,
            body_lines=[],
        )
        chain.append((depth, heading_text))

    if current.heading or current.body_lines:
        sections.append(current)

    return sections


def _section_body(section: _Section) -> str:
    body = "\n".join(section.body_lines).strip("\n")
    while "\n\n\n" in body:
        body = body.replace("\n\n\n", "\n\n")
    return body


def _split_body_by_paragraphs(body: str, max_tokens: int) -> list[str]:
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", body) if p.strip()]
    if not paragraphs:
        return []

    chunks: list[str] = []
    buffer: list[str] = []
    buffer_tokens = 0

    for paragraph in paragraphs:
        para_tokens = len(paragraph.split())
        if buffer and buffer_tokens + para_tokens > max_tokens:
            chunks.append("\n\n".join(buffer))
            buffer = [paragraph]
            buffer_tokens = para_tokens
            continue
        buffer.append(paragraph)
        buffer_tokens += para_tokens

    if buffer:
        chunks.append("\n\n".join(buffer))
    return chunks


def split_into_chunks(
    markdown: str,
    *,
    source_path: str,
    max_tokens: int = DEFAULT_MAX_TOKENS,
) -> list[Chunk]:
    if not markdown.strip():
        return []

    section_id, remainder = _extract_frontmatter(markdown)
    if not remainder.strip():
        return []

    sections = _parse_sections(remainder)
    slug = _source_slug(source_path)

    results: list[Chunk] = []
    index = 0

    for section in sections:
        body = _section_body(section)
        if not body and not section.heading:
            continue

        bodies = _split_body_by_paragraphs(body, max_tokens) if body else [""]
        if not bodies:
            bodies = [""]

        for body_part in bodies:
            results.append(
                Chunk(
                    chunk_id=f"{slug}::{index:04d}",
                    source_path=source_path,
                    source_section_id=section_id,
                    parent_titles=section.parent_titles,
                    heading=section.heading,
                    body=body_part,
                    token_count=len(body_part.split()),
                )
            )
            index += 1

    return results
