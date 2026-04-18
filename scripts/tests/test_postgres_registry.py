"""Tests for PostgreSQL KG registry.

These tests are skipped if psycopg is not installed or if no PostgreSQL
instance is reachable at the configured conninfo.
"""

from __future__ import annotations

import pytest

psycopg = pytest.importorskip("psycopg", reason="psycopg not installed")

from vitruvius.kg.postgres_client import PostgresClient


@pytest.fixture(scope="module")
def pg_client() -> PostgresClient:
    from vitruvius.config import get_kg_postgres_conninfo

    client = PostgresClient(conninfo=get_kg_postgres_conninfo())
    if not client.verify_connectivity():
        pytest.skip("PostgreSQL instance not reachable")
    return client


def test_connectivity(pg_client: PostgresClient) -> None:
    assert pg_client.verify_connectivity() is True


def test_document_version_crud(pg_client: PostgresClient) -> None:
    record = {
        "id": "docv-test-pg-001",
        "document_id": "doc-test-pg",
        "title": "Test Document",
        "source_uri": "/test.pdf",
        "mime_type": "application/pdf",
        "sha256": "a" * 64,
        "supersedes": None,
    }
    pg_client.insert_document_version(record)

    fetched = pg_client.get_document_version_by_sha256("a" * 64)
    assert fetched is not None
    assert fetched["title"] == "Test Document"


def test_review_queue_crud(pg_client: PostgresClient) -> None:
    pg_client.enqueue_review(
        item_type="canonical_node",
        item_id="concept-test-pg-001",
        confidence=0.85,
        escalation_reason="ambiguous_placement",
    )

    pending = pg_client.dequeue_pending_review(item_type="canonical_node")
    assert any(r["item_id"] == "concept-test-pg-001" for r in pending)

    pg_client.resolve_review("concept-test-pg-001", "approved", actor="test_runner")
    pending_after = pg_client.dequeue_pending_review(item_type="canonical_node")
    assert not any(r["item_id"] == "concept-test-pg-001" for r in pending_after)


def test_audit_event_logging(pg_client: PostgresClient) -> None:
    pg_client.log_audit("test_event", "test_runner", {"detail": 123})
    # Audit events are fire-and-forget; we just verify no exception is raised.
