"""Neo4j evidence writer — focused evidence chain persistence.

Writes ``DocumentVersion → Section → Chunk → EvidenceSpan`` chains to Neo4j
from either individual entities or a full ``KgV2Snapshot``.  Complements
:mod:`evidence_ingestor` (raw-file → graph) and :mod:`neo4j_loader`
(snapshot → Cypher) with a direct driver-based writer.

All writes are idempotent (MERGE on ``id``).
"""

from __future__ import annotations

import logging
from typing import Any

from .json_evidence_store import KgV2Snapshot
from .neo4j_client import Neo4jClient
from .schemas import Chunk, DocumentVersion, EvidenceSpan, Section

logger = logging.getLogger(__name__)


class Neo4jEvidenceWriter:
    """Write evidence-chain entities to Neo4j.

    Usage::

        writer = Neo4jEvidenceWriter(neo4j_client)
        writer.write_document_version(dv)
        writer.write_section(sec)
        writer.write_chunk(chk)
        writer.write_evidence_span(span)

    Or batch from a snapshot::

        writer.write_snapshot(snapshot)
    """

    def __init__(self, client: Neo4jClient) -> None:
        self.client = client

    # ------------------------------------------------------------------
    # Single-entity writes
    # ------------------------------------------------------------------

    def write_document_version(self, dv: DocumentVersion) -> None:
        """MERGE a ``DocumentVersion`` node."""
        self.client.run(
            """
            MERGE (d:DocumentVersion {id: $id})
            SET d.document_id = $document_id,
                d.title = $title,
                d.source_uri = $source_uri,
                d.mime_type = $mime_type,
                d.sha256 = $sha256,
                d.created_at = $created_at
            """,
            id=dv.id,
            document_id=dv.document_id,
            title=dv.title,
            source_uri=dv.source_uri,
            mime_type=dv.mime_type,
            sha256=dv.sha256,
            created_at=dv.created_at,
        )
        logger.debug("Wrote DocumentVersion %s", dv.id)

    def write_section(self, sec: Section) -> None:
        """MERGE a ``Section`` node and link it to its ``DocumentVersion``."""
        self.client.run(
            """
            MERGE (s:Section {id: $id})
            SET s.document_version_id = $document_version_id,
                s.title = $title,
                s.level = $level,
                s.line_start = $line_start,
                s.line_end = $line_end,
                s.char_start = $char_start,
                s.char_end = $char_end
            WITH s
            MATCH (d:DocumentVersion {id: $document_version_id})
            MERGE (d)-[:HAS_SECTION]->(s)
            """,
            id=sec.id,
            document_version_id=sec.document_version_id,
            title=sec.title,
            level=sec.level,
            line_start=sec.line_start,
            line_end=sec.line_end,
            char_start=sec.char_start,
            char_end=sec.char_end,
        )
        logger.debug("Wrote Section %s", sec.id)

    def write_chunk(self, chk: Chunk) -> None:
        """MERGE a ``Chunk`` node and link it to its ``Section``."""
        self.client.run(
            """
            MERGE (c:Chunk {id: $id})
            SET c.document_version_id = $document_version_id,
                c.text = $text,
                c.char_start = $char_start,
                c.char_end = $char_end,
                c.token_count = $token_count
            WITH c
            MATCH (s:Section {id: $section_id})
            MERGE (s)-[:HAS_CHUNK]->(c)
            """,
            id=chk.id,
            document_version_id=chk.document_version_id,
            text=chk.text,
            char_start=chk.char_start,
            char_end=chk.char_end,
            token_count=chk.token_count,
            section_id=chk.section_id,
        )
        logger.debug("Wrote Chunk %s", chk.id)

    def write_evidence_span(self, span: EvidenceSpan) -> None:
        """MERGE an ``EvidenceSpan`` node and link it to its ``Chunk``."""
        selector_dict = span.selector.model_dump()
        self.client.run(
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
        logger.debug("Wrote EvidenceSpan %s", span.id)

    # ------------------------------------------------------------------
    # Batch writes
    # ------------------------------------------------------------------

    def write_snapshot(self, snapshot: KgV2Snapshot) -> dict[str, int]:
        """Write every evidence-chain entity in *snapshot* to Neo4j.

        Returns counts of each entity type written.
        """
        counts: dict[str, int] = {
            "document_versions": 0,
            "sections": 0,
            "chunks": 0,
            "evidence_spans": 0,
        }

        for dv in snapshot.document_versions:
            self.write_document_version(dv)
            counts["document_versions"] += 1

        for sec in snapshot.sections:
            self.write_section(sec)
            counts["sections"] += 1

        for chk in snapshot.chunks:
            self.write_chunk(chk)
            counts["chunks"] += 1

        for span in snapshot.evidence_spans:
            self.write_evidence_span(span)
            counts["evidence_spans"] += 1

        logger.info(
            "Wrote evidence snapshot: %d DocumentVersions, %d Sections, %d Chunks, %d EvidenceSpans",
            counts["document_versions"],
            counts["sections"],
            counts["chunks"],
            counts["evidence_spans"],
        )
        return counts

    # ------------------------------------------------------------------
    # Idempotency helpers
    # ------------------------------------------------------------------

    def delete_evidence_chain(self) -> None:
        """Remove **all** evidence-chain nodes and relationships.

        Useful for rollback / test teardown.  Does **not** touch
        ``CanonicalNode``, ``RelationshipAssertion``, or fast-edge data.
        """
        self.client.run(
            """
            MATCH (n:DocumentVersion|Section|Chunk|EvidenceSpan)
            DETACH DELETE n
            """
        )
        logger.warning("Deleted all evidence-chain nodes from Neo4j")
