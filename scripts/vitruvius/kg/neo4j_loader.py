"""Neo4j loader — snapshot → Cypher for the KG v2 transition.

Reads a ``KgV2Snapshot`` (and optionally a separate edge-snapshot JSON)
and produces idempotent ``MERGE`` statements suitable for Neo4j.

When ``kg_transition.neo4j_backend`` is enabled and a ``Neo4jClient`` is
provided, statements are executed directly; otherwise they are returned
as a list or written to a ``.cypher`` file.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from vitruvius.config import is_kg_neo4j_backend
from .json_evidence_store import KgV2Snapshot
from .schemas import CanonicalNode, RelationshipAssertion


class Neo4jLoader:
    """Generate and optionally execute Cypher from a v2-alpha snapshot."""

    def __init__(
        self,
        snapshot: KgV2Snapshot,
        edge_snapshot_path: Path | str | None = None,
    ) -> None:
        self.snapshot = snapshot
        self.edge_snapshot_path = (
            Path(edge_snapshot_path) if edge_snapshot_path else None
        )
        self._statements: list[str] = []

    # -- public API ----------------------------------------------------------

    def to_cypher(self) -> list[str]:
        """Generate idempotent MERGE statements for the whole snapshot."""
        self._statements = []
        self._merge_canonical_nodes()
        self._merge_document_versions()
        self._merge_sections()
        self._merge_chunks()
        self._merge_evidence_spans()
        self._merge_assertions()
        self._merge_fast_edges()
        return list(self._statements)

    def write_cypher(self, out_path: Path | str) -> Path:
        """Write statements to a ``.cypher`` file and return the path."""
        path = Path(out_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        text = "\n".join(self.to_cypher())
        path.write_text(text, encoding="utf-8")
        return path

    def load(self, client: Any | None = None) -> dict[str, Any]:
        """Execute Cypher against Neo4j when the feature flag is on.

        Returns a summary dict.  If the flag is off or no client is
        provided, returns the statements without executing them.
        """
        statements = self.to_cypher()
        if not is_kg_neo4j_backend() or client is None:
            return {
                "executed": False,
                "reason": "kg_transition.neo4j_backend=false or no client",
                "statement_count": len(statements),
                "statements": statements,
            }

        executed = 0
        errors: list[str] = []
        for stmt in statements:
            try:
                client.run(stmt)
                executed += 1
            except Exception as exc:
                errors.append(f"{exc}")

        return {
            "executed": True,
            "statement_count": len(statements),
            "executed_count": executed,
            "error_count": len(errors),
            "errors": errors,
        }

    # -- internal generators -------------------------------------------------

    def _merge_canonical_nodes(self) -> None:
        for node in self.snapshot.canonical_nodes:
            self._statements.append(_canonical_node_merge(node))

    def _merge_document_versions(self) -> None:
        for dv in self.snapshot.document_versions:
            props = _escape_props({
                "id": dv.id,
                "document_id": dv.document_id,
                "title": dv.title,
                "source_uri": dv.source_uri,
                "mime_type": dv.mime_type,
                "sha256": dv.sha256,
                "created_at": dv.created_at,
                "supersedes": dv.supersedes,
            })
            self._statements.append(
                f"MERGE (d:DocumentVersion {{id: '{_esc(dv.id)}'}})"
                f" SET d += {props}"
            )

    def _merge_sections(self) -> None:
        for sec in self.snapshot.sections:
            props = _escape_props({
                "id": sec.id,
                "document_version_id": sec.document_version_id,
                "title": sec.title,
                "level": sec.level,
            })
            self._statements.append(
                f"MERGE (s:Section {{id: '{_esc(sec.id)}'}})"
                f" SET s += {props}"
            )

    def _merge_chunks(self) -> None:
        for chunk in self.snapshot.chunks:
            props = _escape_props({
                "id": chunk.id,
                "section_id": chunk.section_id,
                "document_version_id": chunk.document_version_id,
                "text": chunk.text,
                "char_start": chunk.char_start,
                "char_end": chunk.char_end,
                "token_count": chunk.token_count,
            })
            self._statements.append(
                f"MERGE (c:Chunk {{id: '{_esc(chunk.id)}'}})"
                f" SET c += {props}"
            )

    def _merge_evidence_spans(self) -> None:
        for span in self.snapshot.evidence_spans:
            props = _escape_props({
                "id": span.id,
                "document_id": span.document_id,
                "document_version_id": span.document_version_id,
                "quote": span.quote,
                "normalized_text": span.normalized_text,
                "deep_link": span.deep_link,
                "parser": span.parser,
                "parser_version": span.parser_version,
                "ingestion_run_id": span.ingestion_run_id,
                "checksum": span.checksum,
                "created_at": span.created_at,
            })
            self._statements.append(
                f"MERGE (e:EvidenceSpan {{id: '{_esc(span.id)}'}})"
                f" SET e += {props}"
            )

    def _merge_assertions(self) -> None:
        for assertion in self.snapshot.relationship_assertions:
            props = _escape_props({
                "id": assertion.id,
                "edge_type": assertion.edge_type.value,
                "from_node_id": assertion.from_node_id,
                "to_node_id": assertion.to_node_id,
                "reasoning_summary": assertion.reasoning_summary,
                "inference_type": assertion.inference_type.value,
                "confidence": assertion.confidence,
                "validation_status": assertion.validation_status.value,
                "review_state": assertion.review_state,
                "evidence_ids": assertion.evidence_ids,
                "document_version_ids": assertion.document_version_ids,
                "created_at": assertion.created_at,
                "updated_at": assertion.updated_at,
                "version": assertion.version,
            })
            self._statements.append(
                f"MERGE (a:Assertion {{id: '{_esc(assertion.id)}'}})"
                f" SET a += {props}"
            )

    def _merge_fast_edges(self) -> None:
        edges = list(self.snapshot.fast_edges)
        if self.edge_snapshot_path and self.edge_snapshot_path.exists():
            import json

            data = json.loads(self.edge_snapshot_path.read_text(encoding="utf-8"))
            edges.extend(data.get("edges", []))

        for edge in edges:
            eid = edge.get("id", "")
            etype = edge.get("edge_type", "RELATED_TO")
            from_id = edge.get("from_node_id", "")
            to_id = edge.get("to_node_id", "")
            aid = edge.get("assertion_id", "")
            conf = edge.get("confidence", 0.0)
            self._statements.append(
                f"MATCH (from_node {{id: '{_esc(from_id)}'}}),"
                f" (to_node {{id: '{_esc(to_id)}'}})"
                f" MERGE (from_node)-[r:{_esc(etype)} {{id: '{_esc(eid)}'}}]->(to_node)"
                f" SET r.assertion_id = '{_esc(aid)}', r.confidence = {conf}"
            )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _esc(value: str) -> str:
    """Escape single quotes for Cypher string literals."""
    return value.replace("\\", "\\\\").replace("'", "\\'")


def _escape_props(props: dict[str, Any]) -> str:
    """Convert a dict to a Cypher property map string."""
    items: list[str] = []
    for key, value in props.items():
        if value is None:
            items.append(f"{key}: null")
        elif isinstance(value, bool):
            items.append(f"{key}: {str(value).lower()}")
        elif isinstance(value, (int, float)):
            items.append(f"{key}: {value}")
        elif isinstance(value, list):
            inner = ", ".join(_escape_value(v) for v in value)
            items.append(f"{key}: [{inner}]")
        else:
            items.append(f"{key}: {_escape_value(value)}")
    return "{" + ", ".join(items) + "}"


def _escape_value(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return str(value).lower()
    if isinstance(value, (int, float)):
        return str(value)
    return "'" + _esc(str(value)) + "'"


def _canonical_node_merge(node: CanonicalNode) -> str:
    props = _escape_props({
        "id": node.id,
        "type": node.type.value,
        "label": node.label,
        "slug": node.slug,
        "summary": node.summary,
        "taxonomy_path": node.taxonomy_path,
        "aliases": node.aliases,
        "status": node.status.value,
        "confidence": node.confidence,
        "version": node.version,
        "created_at": node.created_at,
        "updated_at": node.updated_at,
        "embedding_ref": node.embedding_ref,
        "primary_assertion_id": node.primary_assertion_id,
    })
    return (
        f"MERGE (n:CanonicalNode {{id: '{_esc(node.id)}'}})"
        f" SET n += {props}"
    )
