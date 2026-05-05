"""Neo4j client for the Knowledge Graph transition.

Provides a thin, retry-aware wrapper around the official Neo4j Python driver
with helper methods for the canonical + evidence + assertion graph schema.
"""

from __future__ import annotations

import logging
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Generator

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class Neo4jConnectivityStatus:
    ok: bool
    reason: str = "ok"
    error: str = ""

    def __bool__(self) -> bool:
        return self.ok


def _classify_connectivity_error(exc: Exception) -> str:
    if isinstance(exc, ImportError):
        return "driver_missing"

    message = f"{type(exc).__name__}: {exc}".lower()
    code = str(
        getattr(exc, "code", "")
        or getattr(exc, "neo4j_code", "")
        or getattr(exc, "gql_status", "")
    ).lower()
    combined = f"{code} {message}"
    if (
        "security.unauthorized" in combined
        or "unauthorized" in combined
        or "authentication" in combined
        or "autherror" in combined
        or "securityerror" in combined
    ):
        return "auth_failed"
    return "unreachable"


class Neo4jClient:
    """Lazy-initialising Neo4j driver wrapper.

    The driver is created on first use so that importing this module does
    not require a running Neo4j instance.
    """

    def __init__(
        self,
        uri: str = "bolt://localhost:7687",
        user: str = "neo4j",
        password: str = "password",
        database: str = "neo4j",
    ) -> None:
        self._uri = uri
        self._user = user
        self._password = password
        self._database = database
        self._driver: Any | None = None

    # ------------------------------------------------------------------
    # Driver lifecycle
    # ------------------------------------------------------------------

    def _ensure_driver(self) -> Any:
        if self._driver is None:
            try:
                from neo4j import GraphDatabase
            except ImportError as exc:
                raise ImportError(
                    "neo4j driver is required for kg_transition.neo4j_backend. "
                    "Install it: pip install neo4j"
                ) from exc
            self._driver = GraphDatabase.driver(
                self._uri, auth=(self._user, self._password)
            )
        return self._driver

    def close(self) -> None:
        if self._driver is not None:
            self._driver.close()
            self._driver = None

    def check_connectivity(self) -> Neo4jConnectivityStatus:
        try:
            driver = self._ensure_driver()
            driver.verify_connectivity()
            return Neo4jConnectivityStatus(ok=True)
        except Exception as exc:
            logger.warning("Neo4j connectivity check failed: %s", exc)
            return Neo4jConnectivityStatus(
                ok=False,
                reason=_classify_connectivity_error(exc),
                error=str(exc),
            )

    def verify_connectivity(self) -> bool:
        return self.check_connectivity().ok

    # ------------------------------------------------------------------
    # Session helpers
    # ------------------------------------------------------------------

    @contextmanager
    def session(self) -> Generator[Any, None, None]:
        driver = self._ensure_driver()
        sess = driver.session(database=self._database)
        try:
            yield sess
        finally:
            sess.close()

    def run(self, cypher: str, **params: Any) -> list[dict[str, Any]]:
        with self.session() as sess:
            result = sess.run(cypher, **params)
            return [record.data() for record in result]

    # ------------------------------------------------------------------
    # Schema bootstrap (idempotent)
    # ------------------------------------------------------------------

    def init_schema(self) -> None:
        """Create constraints and indexes if they do not already exist."""
        constraints = [
            "CREATE CONSTRAINT canonical_node_id IF NOT EXISTS FOR (n:CanonicalNode) REQUIRE n.id IS UNIQUE",
            "CREATE CONSTRAINT assertion_id IF NOT EXISTS FOR (a:Assertion) REQUIRE a.id IS UNIQUE",
            "CREATE CONSTRAINT evidence_span_id IF NOT EXISTS FOR (e:EvidenceSpan) REQUIRE e.id IS UNIQUE",
            "CREATE CONSTRAINT document_version_id IF NOT EXISTS FOR (d:DocumentVersion) REQUIRE d.id IS UNIQUE",
            "CREATE CONSTRAINT section_id IF NOT EXISTS FOR (s:Section) REQUIRE s.id IS UNIQUE",
            "CREATE CONSTRAINT chunk_id IF NOT EXISTS FOR (c:Chunk) REQUIRE c.id IS UNIQUE",
        ]
        indexes = [
            "CREATE INDEX canonical_node_type IF NOT EXISTS FOR (n:CanonicalNode) ON (n.type)",
            "CREATE INDEX canonical_node_status IF NOT EXISTS FOR (n:CanonicalNode) ON (n.status)",
            "CREATE INDEX assertion_edge_type IF NOT EXISTS FOR (a:Assertion) ON (a.edge_type)",
            "CREATE INDEX assertion_status IF NOT EXISTS FOR (a:Assertion) ON (a.validation_status)",
            "CREATE INDEX evidence_span_docv IF NOT EXISTS FOR (e:EvidenceSpan) ON (e.document_version_id)",
        ]
        with self.session() as sess:
            for stmt in constraints:
                try:
                    sess.run(stmt)
                except Exception as exc:
                    logger.warning("Constraint init skipped (may already exist): %s — %s", stmt, exc)
            for stmt in indexes:
                try:
                    sess.run(stmt)
                except Exception as exc:
                    logger.warning("Index init skipped (may already exist): %s — %s", stmt, exc)
        logger.info("Neo4j schema initialised")

    def reset_evidence_graph(self) -> None:
        """Delete all evidence-graph nodes (useful for dev/testing)."""
        self.run(
            "MATCH (n:DocumentVersion|Section|Chunk|EvidenceSpan) DETACH DELETE n"
        )
        logger.info("Neo4j evidence graph reset")

    def reset_canonical_graph(self) -> None:
        """Delete all canonical + assertion nodes (useful for dev/testing)."""
        self.run(
            "MATCH (n:CanonicalNode|Assertion) DETACH DELETE n"
        )
        logger.info("Neo4j canonical graph reset")
