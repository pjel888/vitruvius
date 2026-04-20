"""Evidence graph ingestion pipeline.

Transforms a raw source document into the evidence graph chain:
    DocumentVersion → Section → Chunk → EvidenceSpan

Operates on structured parser output (section_map + chunk_map) and
produces resolvable, citable evidence spans with selectors.
"""

from __future__ import annotations

import hashlib
import logging
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .neo4j_client import Neo4jClient
from .postgres_client import PostgresClient
from .schemas import (
    Chunk,
    DocumentVersion,
    EvidenceSpan,
    MarkdownRangeSelector,
    PdfPageSelector,
    Section,
)
from .selector_resolver import SelectorResolver

logger = logging.getLogger(__name__)


class EvidenceIngestor:
    """Ingest a document into the evidence graph."""

    def __init__(
        self,
        neo4j: Neo4jClient,
        postgres: PostgresClient,
        raw_source_root: Path,
    ) -> None:
        self.neo4j = neo4j
        self.postgres = postgres
        self.resolver = SelectorResolver(raw_source_root)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def ingest(
        self,
        source_path: Path,
        section_map: list[dict[str, Any]] | None = None,
        chunk_map: list[dict[str, Any]] | None = None,
        parser_id: str = "unknown",
        parser_version: str | None = None,
        ingestion_run_id: str | None = None,
    ) -> DocumentVersion:
        """Ingest a single document into the evidence graph.

        Idempotent: skips if SHA-256 already exists in PostgreSQL.
        """
        sha256 = self._sha256_file(source_path)

        existing = self.postgres.get_document_version_by_sha256(sha256)
        if existing:
            logger.info("Skipping ingest for %s — already ingested as %s", source_path, existing["id"])
            if isinstance(existing.get("created_at"), datetime):
                existing["created_at"] = existing["created_at"].isoformat()
            return DocumentVersion.model_validate(existing)

        doc_id = self._derive_document_id(source_path)
        doc_version_id = f"{doc_id.replace('doc-', 'docv-')}-v1"
        title = source_path.stem
        mime_type = self._mime_type(source_path)

        doc_version = DocumentVersion(
            id=doc_version_id,
            document_id=doc_id,
            title=title,
            source_uri=str(source_path),
            mime_type=mime_type,
            sha256=sha256,
            created_at=datetime.now(timezone.utc).isoformat(),
        )

        # Persist to PostgreSQL
        self.postgres.insert_document_version(doc_version.model_dump())
        self.postgres.log_audit(
            "document_ingested",
            "evidence_ingestor",
            {"document_version_id": doc_version_id, "path": str(source_path)},
        )

        # Build evidence chain
        sections = self._build_sections(doc_version, section_map)
        chunks = self._build_chunks(doc_version, sections, chunk_map)
        spans = self._build_spans(doc_version, chunks, source_path, parser_id, parser_version, ingestion_run_id)

        # Write to Neo4j
        self._write_to_neo4j(doc_version, sections, chunks, spans)

        logger.info(
            "Ingested %s → %d sections, %d chunks, %d spans",
            source_path, len(sections), len(chunks), len(spans),
        )
        return doc_version

    # ------------------------------------------------------------------
    # Internal builders
    # ------------------------------------------------------------------

    def _build_sections(
        self,
        doc_version: DocumentVersion,
        section_map: list[dict[str, Any]] | None,
    ) -> list[Section]:
        if not section_map:
            return []

        sections: list[Section] = []
        for idx, sec in enumerate(section_map, start=1):
            sec_id = f"sec-{doc_version.document_id.replace('doc-', '')}-{idx:03d}"
            sections.append(
                Section(
                    id=sec_id,
                    document_version_id=doc_version.id,
                    title=sec.get("title", "Untitled Section"),
                    level=sec.get("level", 2),
                    line_start=sec.get("line_start"),
                    line_end=sec.get("line_end"),
                    char_start=sec.get("char_start"),
                    char_end=sec.get("char_end"),
                )
            )
        return sections

    def _build_chunks(
        self,
        doc_version: DocumentVersion,
        sections: list[Section],
        chunk_map: list[dict[str, Any]] | None,
    ) -> list[Chunk]:
        if not chunk_map:
            # If no chunk map provided, create one giant chunk per document
            text = Path(doc_version.source_uri).read_text(encoding="utf-8")
            return [
                Chunk(
                    id=f"chk-{doc_version.document_id.replace('doc-', '')}-001",
                    section_id=sections[0].id if sections else "",
                    document_version_id=doc_version.id,
                    text=text,
                    char_start=0,
                    char_end=len(text),
                )
            ]

        chunks: list[Chunk] = []
        for idx, chk in enumerate(chunk_map, start=1):
            chunk_id = f"chk-{doc_version.document_id.replace('doc-', '')}-{idx:03d}"
            chunks.append(
                Chunk(
                    id=chunk_id,
                    section_id=chk.get("section_id", sections[0].id if sections else ""),
                    document_version_id=doc_version.id,
                    text=chk.get("text", ""),
                    char_start=chk.get("char_start", 0),
                    char_end=chk.get("char_end", 0),
                )
            )
        return chunks

    def _build_spans(
        self,
        doc_version: DocumentVersion,
        chunks: list[Chunk],
        source_path: Path,
        parser_id: str,
        parser_version: str | None,
        ingestion_run_id: str | None,
    ) -> list[EvidenceSpan]:
        spans: list[EvidenceSpan] = []

        # Build heading index for markdown files to produce richer selectors
        heading_index: dict[str, tuple[list[str], int]] = {}
        if doc_version.mime_type in ("text/markdown", "text/x-markdown"):
            heading_index = self._index_markdown_headings(source_path)

        # For PDFs, pre-build a page-text index so we can map chunks to pages
        pdf_page_index: dict[str, int] = {}
        if doc_version.mime_type == "application/pdf":
            pdf_page_index = self._index_pdf_pages(source_path)

        for chunk in chunks:
            span_id = f"span-{chunk.id.replace('chk-', '')}"

            # Choose selector based on file type
            if doc_version.mime_type == "application/pdf":
                page = pdf_page_index.get(chunk.text[:200].strip(), 1)
                selector = PdfPageSelector(page=page, quote=chunk.text[:200])
            else:
                # Try to resolve a heading path for this chunk
                heading_path, line_start = self._resolve_chunk_position(
                    chunk, heading_index
                )
                line_end = line_start + chunk.text.count("\n")
                selector = MarkdownRangeSelector(
                    heading_path=heading_path,
                    line_start=max(1, line_start),
                    line_end=max(1, line_end),
                    quote=chunk.text[:200],
                )

            spans.append(
                EvidenceSpan(
                    id=span_id,
                    document_id=doc_version.document_id,
                    document_version_id=doc_version.id,
                    selector=selector,
                    quote=chunk.text[:500],
                    normalized_text=chunk.text,
                    deep_link=f"/viewer/{doc_version.document_id}/{doc_version.id}",
                    parser=parser_id,
                    parser_version=parser_version,
                    ingestion_run_id=ingestion_run_id,
                    checksum=hashlib.sha256(chunk.text.encode("utf-8")).hexdigest(),
                    created_at=datetime.now(timezone.utc).isoformat(),
                )
            )
        return spans

    def _write_to_neo4j(
        self,
        doc_version: DocumentVersion,
        sections: list[Section],
        chunks: list[Chunk],
        spans: list[EvidenceSpan],
    ) -> None:
        # DocumentVersion
        self.neo4j.run(
            """
            MERGE (d:DocumentVersion {id: $id})
            SET d.document_id = $document_id,
                d.title = $title,
                d.source_uri = $source_uri,
                d.mime_type = $mime_type,
                d.sha256 = $sha256,
                d.created_at = $created_at
            """,
            **doc_version.model_dump(),
        )

        # Sections
        for sec in sections:
            self.neo4j.run(
                """
                MERGE (s:Section {id: $id})
                SET s.document_version_id = $document_version_id,
                    s.title = $title,
                    s.level = $level
                WITH s
                MATCH (d:DocumentVersion {id: $document_version_id})
                MERGE (d)-[:HAS_SECTION]->(s)
                """,
                **sec.model_dump(),
            )

        # Chunks
        for chk in chunks:
            self.neo4j.run(
                """
                MERGE (c:Chunk {id: $id})
                SET c.document_version_id = $document_version_id,
                    c.text = $text,
                    c.char_start = $char_start,
                    c.char_end = $char_end
                WITH c
                MATCH (s:Section {id: $section_id})
                MERGE (s)-[:HAS_CHUNK]->(c)
                """,
                **chk.model_dump(),
            )

        # Spans
        for span in spans:
            selector_dict = span.selector.model_dump()
            self.neo4j.run(
                """
                MERGE (e:EvidenceSpan {id: $id})
                SET e.document_id = $document_id,
                    e.document_version_id = $document_version_id,
                    e.quote = $quote,
                    e.normalized_text = $normalized_text,
                    e.deep_link = $deep_link,
                    e.parser = $parser,
                    e.parser_version = $parser_version,
                    e.checksum = $checksum,
                    e.created_at = $created_at,
                    e.selector_kind = $selector_kind
                WITH e
                MATCH (c:Chunk {id: $chunk_id})
                MERGE (c)-[:HAS_SPAN]->(e)
                """,
                id=span.id,
                document_id=span.document_id,
                document_version_id=span.document_version_id,
                quote=span.quote,
                normalized_text=span.normalized_text,
                deep_link=span.deep_link,
                parser=span.parser,
                parser_version=span.parser_version,
                checksum=span.checksum,
                created_at=span.created_at,
                selector_kind=selector_dict.get("kind"),
                chunk_id=span.id.replace("span-", "chk-"),
            )

    # ------------------------------------------------------------------
    # Selector helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _index_markdown_headings(path: Path) -> dict[str, tuple[list[str], int]]:
        """Return a map of heading text → (heading_path, line_number)."""
        index: dict[str, tuple[list[str], int]] = {}
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except OSError:
            return index

        current_path: list[str] = []
        current_levels: list[int] = []

        for line_no, line in enumerate(lines, start=1):
            match = __import__("re").match(r"^(#{1,6})\s+(.*)", line)
            if not match:
                continue
            level = len(match.group(1))
            title = match.group(2).strip()

            # Pop higher or equal levels
            while current_levels and current_levels[-1] >= level:
                current_path.pop()
                current_levels.pop()
            current_path.append(title)
            current_levels.append(level)

            index[title.lower()] = (list(current_path), line_no)

        return index

    @staticmethod
    def _resolve_chunk_position(
        chunk: Chunk,
        heading_index: dict[str, tuple[list[str], int]],
    ) -> tuple[list[str], int]:
        """Try to find the best heading path and line start for a chunk."""
        # Heuristic: if chunk text starts with a known heading, use it
        first_line = chunk.text.splitlines()[0] if chunk.text else ""
        first_line_stripped = first_line.lstrip("# ").strip().lower()
        if first_line_stripped in heading_index:
            path, line_no = heading_index[first_line_stripped]
            return path, line_no

        # Fallback: empty heading path, line 1
        return [], 1

    @staticmethod
    def _index_pdf_pages(path: Path) -> dict[str, int]:
        """Return a map of page text → 1-based page number for a PDF.

        Uses pdfplumber when available; falls back to PyMuPDF.
        """
        index: dict[str, int] = {}
        # Try pdfplumber first
        try:
            import pdfplumber

            with pdfplumber.open(str(path)) as pdf:
                for idx, page in enumerate(pdf.pages):
                    text = (page.extract_text() or "").strip()
                    if text:
                        index[text] = idx + 1  # 1-based
            return index
        except Exception:
            pass

        # Fallback to PyMuPDF
        try:
            import fitz

            doc = fitz.open(str(path))
            for idx in range(len(doc)):
                text = doc[idx].get_text().strip()
                if text:
                    index[text] = idx + 1
            doc.close()
            return index
        except Exception:
            pass

        return index

    # ------------------------------------------------------------------
    # Utilities
    # ------------------------------------------------------------------

    @staticmethod
    def _sha256_file(path: Path) -> str:
        h = hashlib.sha256()
        with path.open("rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        return h.hexdigest()

    @staticmethod
    def _derive_document_id(source_path: Path) -> str:
        slug = source_path.stem.lower().replace(" ", "-").replace("_", "-")[:64]
        return f"doc-{slug}"

    @staticmethod
    def _mime_type(path: Path) -> str:
        suffix = path.suffix.lower()
        if suffix == ".pdf":
            return "application/pdf"
        if suffix in (".md", ".markdown"):
            return "text/markdown"
        return "application/octet-stream"
