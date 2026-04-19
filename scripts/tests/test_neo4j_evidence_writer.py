"""Tests for Neo4jEvidenceWriter."""

from __future__ import annotations

from typing import Any

import pytest

from vitruvius.kg.json_evidence_store import KgV2Snapshot
from vitruvius.kg.neo4j_evidence_writer import Neo4jEvidenceWriter
from vitruvius.kg.schemas import (
    Chunk,
    DocumentVersion,
    EvidenceSpan,
    MarkdownRangeSelector,
    Section,
)


class FakeNeo4jClient:
    """In-memory stand-in for Neo4jClient."""

    def __init__(self) -> None:
        self.statements: list[tuple[str, dict[str, Any]]] = []

    def run(self, query: str, **params: Any) -> None:
        self.statements.append((query, params))

    def close(self) -> None:
        pass


@pytest.fixture
def fake_client() -> FakeNeo4jClient:
    return FakeNeo4jClient()


@pytest.fixture
def writer(fake_client: FakeNeo4jClient) -> Neo4jEvidenceWriter:
    return Neo4jEvidenceWriter(fake_client)


@pytest.fixture
def document_version() -> DocumentVersion:
    return DocumentVersion(
        id="docv-test-v1",
        document_id="doc-test",
        title="Test Document",
        source_uri="test.md",
        mime_type="text/markdown",
        sha256="a" * 64,
        created_at="2026-01-01T00:00:00Z",
    )


@pytest.fixture
def section() -> Section:
    return Section(
        id="sec-test-001",
        document_version_id="docv-test-v1",
        title="Introduction",
        level=2,
        line_start=1,
        line_end=10,
        char_start=0,
        char_end=100,
    )


@pytest.fixture
def chunk() -> Chunk:
    return Chunk(
        id="chk-test-001",
        section_id="sec-test-001",
        document_version_id="docv-test-v1",
        text="This is test content.",
        char_start=0,
        char_end=22,
        token_count=4,
    )


@pytest.fixture
def evidence_span() -> EvidenceSpan:
    return EvidenceSpan(
        id="span-test-001",
        document_id="doc-test",
        document_version_id="docv-test-v1",
        selector=MarkdownRangeSelector(heading_path=["Introduction"], line_start=1, line_end=1),
        quote="This is test content.",
        normalized_text="This is test content.",
        deep_link="/viewer/doc-test/docv-test-v1",
        parser="test",
        checksum="b" * 64,
        created_at="2026-01-01T00:00:00Z",
    )


class TestWriteDocumentVersion:
    def test_writes_merge_statement(self, writer: Neo4jEvidenceWriter, fake_client: FakeNeo4jClient, document_version: DocumentVersion) -> None:
        writer.write_document_version(document_version)
        assert len(fake_client.statements) == 1
        query, params = fake_client.statements[0]
        assert "MERGE (d:DocumentVersion {id: $id})" in query
        assert params["id"] == "docv-test-v1"
        assert params["title"] == "Test Document"


class TestWriteSection:
    def test_writes_merge_and_relationship(self, writer: Neo4jEvidenceWriter, fake_client: FakeNeo4jClient, section: Section) -> None:
        writer.write_section(section)
        assert len(fake_client.statements) == 1
        query, params = fake_client.statements[0]
        assert "MERGE (s:Section {id: $id})" in query
        assert "MERGE (d)-[:HAS_SECTION]->(s)" in query
        assert params["id"] == "sec-test-001"
        assert params["document_version_id"] == "docv-test-v1"


class TestWriteChunk:
    def test_writes_merge_and_relationship(self, writer: Neo4jEvidenceWriter, fake_client: FakeNeo4jClient, chunk: Chunk) -> None:
        writer.write_chunk(chunk)
        assert len(fake_client.statements) == 1
        query, params = fake_client.statements[0]
        assert "MERGE (c:Chunk {id: $id})" in query
        assert "MERGE (s)-[:HAS_CHUNK]->(c)" in query
        assert params["id"] == "chk-test-001"
        assert params["section_id"] == "sec-test-001"


class TestWriteEvidenceSpan:
    def test_writes_merge_and_relationship(self, writer: Neo4jEvidenceWriter, fake_client: FakeNeo4jClient, evidence_span: EvidenceSpan) -> None:
        writer.write_evidence_span(evidence_span)
        assert len(fake_client.statements) == 1
        query, params = fake_client.statements[0]
        assert "MERGE (e:EvidenceSpan {id: $id})" in query
        assert "MERGE (c)-[:HAS_SPAN]->(e)" in query
        assert params["id"] == "span-test-001"
        assert params["chunk_id"] == "chk-test-001"


class TestWriteSnapshot:
    def test_batch_writes_all_entities(
        self,
        writer: Neo4jEvidenceWriter,
        fake_client: FakeNeo4jClient,
        document_version: DocumentVersion,
        section: Section,
        chunk: Chunk,
        evidence_span: EvidenceSpan,
    ) -> None:
        snapshot = KgV2Snapshot()
        snapshot.document_versions.append(document_version)
        snapshot.sections.append(section)
        snapshot.chunks.append(chunk)
        snapshot.evidence_spans.append(evidence_span)

        counts = writer.write_snapshot(snapshot)

        assert counts["document_versions"] == 1
        assert counts["sections"] == 1
        assert counts["chunks"] == 1
        assert counts["evidence_spans"] == 1
        assert len(fake_client.statements) == 4

    def test_empty_snapshot_writes_nothing(self, writer: Neo4jEvidenceWriter, fake_client: FakeNeo4jClient) -> None:
        counts = writer.write_snapshot(KgV2Snapshot())
        assert counts == {"document_versions": 0, "sections": 0, "chunks": 0, "evidence_spans": 0}
        assert len(fake_client.statements) == 0


class TestDeleteEvidenceChain:
    def test_emits_detach_delete(self, writer: Neo4jEvidenceWriter, fake_client: FakeNeo4jClient) -> None:
        writer.delete_evidence_chain()
        assert len(fake_client.statements) == 1
        query, _ = fake_client.statements[0]
        assert "DETACH DELETE n" in query
