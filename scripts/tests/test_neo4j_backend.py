"""Tests for Neo4j KG backend connectivity and schema.

These tests are skipped if the neo4j driver is not installed or if
no Neo4j instance is reachable at the configured URI.
"""

from __future__ import annotations

import pytest

neo4j = pytest.importorskip("neo4j", reason="neo4j driver not installed")

from vitruvius.kg.neo4j_client import Neo4jClient


@pytest.fixture(scope="module")
def neo4j_client() -> Neo4jClient:
    client = Neo4jClient()
    if not client.verify_connectivity():
        pytest.skip("Neo4j instance not reachable")
    return client


def test_connectivity(neo4j_client: Neo4jClient) -> None:
    assert neo4j_client.verify_connectivity() is True


def test_init_schema_idempotent(neo4j_client: Neo4jClient) -> None:
    # Should not raise even if called twice
    neo4j_client.init_schema()
    neo4j_client.init_schema()


def test_crud_canonical_node(neo4j_client: Neo4jClient) -> None:
    neo4j_client.init_schema()
    neo4j_client.reset_canonical_graph()

    neo4j_client.run(
        """
        MERGE (n:CanonicalNode {id: $id})
        SET n.type = 'concept',
            n.label = 'Test Concept',
            n.status = 'candidate'
        """,
        id="concept-test-neo4j-001",
    )

    result = neo4j_client.run(
        "MATCH (n:CanonicalNode {id: $id}) RETURN n.label AS label",
        id="concept-test-neo4j-001",
    )
    assert result[0]["label"] == "Test Concept"


def test_crud_assertion(neo4j_client: Neo4jClient) -> None:
    neo4j_client.init_schema()
    neo4j_client.reset_canonical_graph()

    # Create nodes
    neo4j_client.run(
        "MERGE (a:CanonicalNode {id: $a_id}) SET a.type = 'concept'",
        a_id="concept-a",
    )
    neo4j_client.run(
        "MERGE (b:CanonicalNode {id: $b_id}) SET b.type = 'concept'",
        b_id="concept-b",
    )
    # Create assertion
    neo4j_client.run(
        """
        MERGE (assert:Assertion {id: $assert_id})
        SET assert.edge_type = 'DEPENDS_ON',
            assert.confidence = 0.9,
            assert.validation_status = 'validated'
        WITH assert
        MATCH (a:CanonicalNode {id: $a_id}), (b:CanonicalNode {id: $b_id})
        MERGE (a)-[:FROM]->(assert)-[:TO]->(b)
        """,
        assert_id="assert-test-001",
        a_id="concept-a",
        b_id="concept-b",
    )

    result = neo4j_client.run(
        """
        MATCH (a:CanonicalNode {id: 'concept-a'})-[:FROM]->(assert:Assertion)-[:TO]->(b:CanonicalNode {id: 'concept-b'})
        RETURN assert.confidence AS confidence
        """
    )
    assert result[0]["confidence"] == 0.9


def test_evidence_graph_chain(neo4j_client: Neo4jClient) -> None:
    neo4j_client.init_schema()
    neo4j_client.reset_evidence_graph()

    neo4j_client.run(
        "MERGE (d:DocumentVersion {id: $id}) SET d.title = 'Test Doc'",
        id="docv-test-evidence-001",
    )
    neo4j_client.run(
        """
        MERGE (s:Section {id: 'sec-001'}) SET s.title = 'Section 1'
        WITH s
        MATCH (d:DocumentVersion {id: 'docv-test-evidence-001'})
        MERGE (d)-[:HAS_SECTION]->(s)
        """
    )
    neo4j_client.run(
        """
        MERGE (c:Chunk {id: 'chk-001'}) SET c.text = 'Hello world'
        WITH c
        MATCH (s:Section {id: 'sec-001'})
        MERGE (s)-[:HAS_CHUNK]->(c)
        """
    )
    neo4j_client.run(
        """
        MERGE (e:EvidenceSpan {id: 'span-001'}) SET e.quote = 'Hello'
        WITH e
        MATCH (c:Chunk {id: 'chk-001'})
        MERGE (c)-[:HAS_SPAN]->(e)
        """
    )

    result = neo4j_client.run(
        """
        MATCH (d:DocumentVersion)-[:HAS_SECTION]->(s)-[:HAS_CHUNK]->(c)-[:HAS_SPAN]->(e)
        RETURN count(e) AS span_count
        """
    )
    assert result[0]["span_count"] == 1
