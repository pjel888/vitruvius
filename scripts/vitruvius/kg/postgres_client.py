"""PostgreSQL client for the Knowledge Graph transition registry.

Provides connection pooling, CRUD helpers, and audit logging for the
operational metadata tables defined in ``scripts/vitruvius/db/schema.sql``.
"""

from __future__ import annotations

import json
import logging
from contextlib import contextmanager
from typing import Any, Generator

logger = logging.getLogger(__name__)


class PostgresClient:
    """Lazy-initialising PostgreSQL connection wrapper."""

    def __init__(
        self,
        conninfo: str = "dbname=vitruvius user=postgres password=password host=localhost port=5432",
    ) -> None:
        self._conninfo = conninfo
        self._pool: Any | None = None

    def _ensure_pool(self) -> Any:
        if self._pool is None:
            try:
                import psycopg
                from psycopg_pool import ConnectionPool
            except ImportError as exc:
                raise ImportError(
                    "psycopg is required for kg_transition.postgres_registry. "
                    "Install it: pip install psycopg[binary]"
                ) from exc
            self._pool = ConnectionPool(
                conninfo=self._conninfo,
                min_size=1,
                max_size=4,
                open=True,
            )
        return self._pool

    def close(self) -> None:
        if self._pool is not None:
            self._pool.close()
            self._pool = None

    def verify_connectivity(self) -> bool:
        try:
            pool = self._ensure_pool()
            with pool.connection() as conn:
                conn.execute("SELECT 1")
            return True
        except Exception as exc:
            logger.warning("PostgreSQL connectivity check failed: %s", exc)
            return False

    @contextmanager
    def connection(self) -> Generator[Any, None, None]:
        pool = self._ensure_pool()
        with pool.connection() as conn:
            yield conn

    @contextmanager
    def transaction(self) -> Generator[Any, None, None]:
        with self.connection() as conn:
            with conn.transaction():
                yield conn

    # ------------------------------------------------------------------
    # Audit helper
    # ------------------------------------------------------------------

    def log_audit(
        self,
        event_type: str,
        actor: str,
        details: dict[str, Any] | None = None,
    ) -> None:
        with self.connection() as conn:
            conn.execute(
                "INSERT INTO audit_event (id, event_type, actor, details) VALUES (gen_random_uuid()::text, %s, %s, %s)",
                (event_type, actor, json.dumps(details) if details else None),
            )

    # ------------------------------------------------------------------
    # Document version helpers
    # ------------------------------------------------------------------

    def insert_document_version(self, record: dict[str, Any]) -> None:
        with self.connection() as conn:
            conn.execute(
                """
                INSERT INTO document_version (id, document_id, title, source_uri, mime_type, sha256, supersedes)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO UPDATE SET
                    title = EXCLUDED.title,
                    source_uri = EXCLUDED.source_uri,
                    mime_type = EXCLUDED.mime_type,
                    sha256 = EXCLUDED.sha256
                """,
                (
                    record["id"],
                    record["document_id"],
                    record["title"],
                    record["source_uri"],
                    record.get("mime_type", "application/pdf"),
                    record["sha256"],
                    record.get("supersedes"),
                ),
            )

    def get_document_version_by_sha256(self, sha256: str) -> dict[str, Any] | None:
        with self.connection() as conn:
            cur = conn.execute(
                "SELECT * FROM document_version WHERE sha256 = %s LIMIT 1", (sha256,)
            )
            row = cur.fetchone()
            if row is None:
                return None
            return dict(row)

    # ------------------------------------------------------------------
    # Review queue helpers
    # ------------------------------------------------------------------

    def enqueue_review(
        self,
        item_type: str,
        item_id: str,
        confidence: float,
        escalation_reason: str | None = None,
    ) -> None:
        with self.connection() as conn:
            conn.execute(
                """
                INSERT INTO review_queue (id, item_type, item_id, confidence, escalation_reason)
                VALUES (gen_random_uuid()::text, %s, %s, %s, %s)
                ON CONFLICT (item_id) DO UPDATE SET
                    confidence = EXCLUDED.confidence,
                    status = 'pending',
                    escalation_reason = EXCLUDED.escalation_reason,
                    updated_at = NOW()
                """,
                (item_type, item_id, confidence, escalation_reason),
            )

    def dequeue_pending_review(self, item_type: str | None = None) -> list[dict[str, Any]]:
        with self.connection() as conn:
            if item_type:
                cur = conn.execute(
                    "SELECT * FROM review_queue WHERE status = 'pending' AND item_type = %s ORDER BY created_at",
                    (item_type,),
                )
            else:
                cur = conn.execute(
                    "SELECT * FROM review_queue WHERE status = 'pending' ORDER BY created_at"
                )
            return [dict(row) for row in cur.fetchall()]

    def resolve_review(self, item_id: str, decision: str, actor: str) -> None:
        with self.connection() as conn:
            conn.execute(
                "UPDATE review_queue SET status = %s, updated_at = NOW() WHERE item_id = %s",
                (decision, item_id),
            )
            self.log_audit("review_resolved", actor, {"item_id": item_id, "decision": decision})
