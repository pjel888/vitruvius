"""Tests for EvidenceIngestor."""

from __future__ import annotations

import pytest

from vitruvius.kg.evidence_ingestor import EvidenceIngestor
from vitruvius.kg.neo4j_client import Neo4jClient
from vitruvius.kg.postgres_client import PostgresClient

neo4j = pytest.importorskip("neo4j", reason="neo4j driver not installed")
psycopg = pytest.importorskip("psycopg", reason="psycopg not installed")


@pytest.fixture(scope="module")
def neo4j_client() -> Neo4jClient:
    client = Neo4jClient()
    if not client.verify_connectivity():
        pytest.skip("Neo4j not reachable")
    return client


@pytest.fixture(scope="module")
def pg_client() -> PostgresClient:
    from vitruvius.config import get_kg_postgres_conninfo

    client = PostgresClient(conninfo=get_kg_postgres_conninfo())
    if not client.verify_connectivity():
        pytest.skip("PostgreSQL not reachable")
    return client


def test_ingest_markdown(neo4j_client: Neo4jClient, pg_client: PostgresClient, tmp_path: pytest.TempPathFactory) -> None:
    neo4j_client.reset_evidence_graph()

    raw_dir = tmp_path / "raw"
    raw_dir.mkdir()
    md_file = raw_dir / "test-document.md"
    md_file.write_text("# Section 1\nThis is test content.", encoding="utf-8")

    ingestor = EvidenceIngestor(
        neo4j=neo4j_client,
        postgres=pg_client,
        raw_source_root=raw_dir,
    )

    doc_version = ingestor.ingest(
        source_path=md_file,
        section_map=[{"title": "Section 1", "level": 1, "line_start": 1, "line_end": 2}],
        chunk_map=[{"text": "This is test content.", "char_start": 12, "char_end": 34}],
        parser_id="test_parser",
        parser_version="1.0.0",
    )

    assert doc_version.id.startswith("docv-")
    assert doc_version.mime_type == "text/markdown"

    # Verify PostgreSQL
    fetched = pg_client.get_document_version_by_sha256(doc_version.sha256)
    assert fetched is not None
    assert fetched["id"] == doc_version.id

    # Verify Neo4j
    result = neo4j_client.run(
        "MATCH (d:DocumentVersion {id: $id}) RETURN d.title AS title",
        id=doc_version.id,
    )
    assert result[0]["title"] == "test-document"

    result = neo4j_client.run(
        """
        MATCH (d:DocumentVersion {id: $id})-[:HAS_SECTION]->(s)-[:HAS_CHUNK]->(c)-[:HAS_SPAN]->(e)
        RETURN count(e) AS span_count
        """,
        id=doc_version.id,
    )
    assert result[0]["span_count"] == 1


def test_ingest_idempotent(neo4j_client: Neo4jClient, pg_client: PostgresClient, tmp_path: pytest.TempPathFactory) -> None:
    neo4j_client.reset_evidence_graph()

    raw_dir = tmp_path / "raw"
    raw_dir.mkdir()
    md_file = raw_dir / "idempotent.md"
    md_file.write_text("Same content.", encoding="utf-8")

    ingestor = EvidenceIngestor(
        neo4j=neo4j_client,
        postgres=pg_client,
        raw_source_root=raw_dir,
    )

    dv1 = ingestor.ingest(source_path=md_file)
    dv2 = ingestor.ingest(source_path=md_file)

    assert dv1.id == dv2.id
