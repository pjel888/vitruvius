"""Neo4j loader — snapshot -> Cypher for the KG v2 transition.

Reads a ``KgV2Snapshot`` (and optionally a separate edge-snapshot JSON)
and produces idempotent ``MERGE`` statements suitable for Neo4j.

When ``kg_transition.neo4j_backend`` is enabled and a ``Neo4jClient`` is
provided, statements are executed directly; otherwise they are returned
as a list or written to a ``.cypher`` file.

Taxonomy-centered graph model
-----------------------------
* Taxonomy/Topic/Subtopic nodes are virtualised from ``taxonomy_path`` arrays.
* ``RelationshipAssertion`` objects become **typed edges** between
  ``CanonicalNode`` vertices (not standalone nodes).
* ``PlacementAssertion`` and ``MergeAssertion`` become ``BELONGS_TO`` and
  ``SAME_AS`` edges respectively.
* Evidence linkage is explicit: ``SUPPORTED_BY`` edges connect canonical
  concepts to ``EvidenceSpan`` nodes.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from vitruvius.config import is_kg_neo4j_backend
from .json_evidence_store import KgV2Snapshot
from .schemas import (
    CanonicalNode,
    MergeAssertion,
    PlacementAssertion,
    RelationshipAssertion,
)


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
        self._merge_taxonomy_nodes()
        self._merge_taxonomy_edges()
        self._merge_document_versions()
        self._merge_sections()
        self._merge_chunks()
        self._merge_evidence_spans()
        self._merge_assertion_edges()
        self._merge_placement_assertion_edges()
        self._merge_merge_assertion_edges()
        self._merge_support_edges()
        self._merge_evidence_relationships()
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

    def _merge_taxonomy_nodes(self) -> None:
        """Create Taxonomy, Topic, Subtopic nodes from taxonomy_path arrays."""
        segments = _extract_taxonomy_segments(self.snapshot.canonical_nodes)
        for seg_id, (kind, label) in segments.items():
            label_cypher = {
                "taxonomy": "Taxonomy",
                "topic": "Topic",
                "subtopic": "Subtopic",
            }[kind]
            props = _escape_props({
                "id": seg_id,
                "label": label,
                "kind": kind,
            })
            self._statements.append(
                f"MERGE (n:{label_cypher} {{id: '{_esc(seg_id)}'}})"
                f" SET n += {props}"
            )

    def _merge_taxonomy_edges(self) -> None:
        """Link taxonomy hierarchy and connect canonical nodes to taxonomy."""
        # Build unique parent->child pairs
        has_child: set[tuple[str, str]] = set()
        belongs_to: set[tuple[str, str]] = set()

        for node in self.snapshot.canonical_nodes:
            tp = node.taxonomy_path
            if not tp:
                continue

            # Normalise paths that use the old short-root format
            tp = _normalise_taxonomy_path(tp)

            # Hierarchy edges
            for i in range(len(tp) - 1):
                has_child.add((tp[i], tp[i + 1]))

            # Canonical node -> leaf taxonomy node
            # Skip taxonomy-root canonical nodes (they ARE the taxonomy,
            # they don't belong to it).
            if node.type.value == "taxonomy":
                continue
            leaf = tp[-1]
            belongs_to.add((node.id, leaf))

        for parent_id, child_id in sorted(has_child):
            self._statements.append(
                f"MATCH (p {{id: '{_esc(parent_id)}'}}),"
                f" (c {{id: '{_esc(child_id)}'}})"
                f" MERGE (p)-[:HAS_CHILD]->(c)"
            )

        for node_id, taxo_id in sorted(belongs_to):
            self._statements.append(
                f"MATCH (cn:CanonicalNode {{id: '{_esc(node_id)}'}}),"
                f" (tx {{id: '{_esc(taxo_id)}'}})"
                f" MERGE (cn)-[:BELONGS_TO]->(tx)"
            )

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
            selector_dict = span.selector.model_dump(mode="json") if span.selector else {}
            selector_kind = selector_dict.get("kind", "unknown")
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
                "selector_kind": selector_kind,
                "selector": selector_dict,
            })
            self._statements.append(
                f"MERGE (e:EvidenceSpan {{id: '{_esc(span.id)}'}})"
                f" SET e += {props}"
            )

    def _merge_assertion_edges(self) -> None:
        """Convert RelationshipAssertion objects into typed edges.

        Skips "orphan" assertions whose endpoints are not present in the
        canonical node set.
        """
        canonical_ids = {n.id for n in self.snapshot.canonical_nodes}
        for assertion in self.snapshot.relationship_assertions:
            if assertion.from_node_id not in canonical_ids:
                continue
            if assertion.to_node_id not in canonical_ids:
                continue
            self._statements.append(
                _assertion_edge_cypher(assertion)
            )

    def _merge_placement_assertion_edges(self) -> None:
        """Convert PlacementAssertion objects into BELONGS_TO edges."""
        canonical_ids = {n.id for n in self.snapshot.canonical_nodes}
        for pa in self.snapshot.placement_assertions:
            if pa.node_id not in canonical_ids or pa.parent_node_id not in canonical_ids:
                continue
            props = _escape_props({
                "assertion_id": pa.id,
                "reasoning_summary": pa.reasoning_summary,
                "confidence": pa.confidence,
                "validation_status": pa.validation_status.value,
            })
            self._statements.append(
                f"MATCH (a:CanonicalNode {{id: '{_esc(pa.node_id)}'}}),"
                f" (b:CanonicalNode {{id: '{_esc(pa.parent_node_id)}'}})"
                f" MERGE (a)-[r:BELONGS_TO {props}]->(b)"
            )

    def _merge_merge_assertion_edges(self) -> None:
        """Convert MergeAssertion objects into SAME_AS edges."""
        canonical_ids = {n.id for n in self.snapshot.canonical_nodes}
        for ma in self.snapshot.merge_assertions:
            if ma.from_node_id not in canonical_ids or ma.to_node_id not in canonical_ids:
                continue
            props = _escape_props({
                "assertion_id": ma.id,
                "reasoning_summary": ma.reasoning_summary,
                "confidence": ma.confidence,
                "validation_status": ma.validation_status.value,
            })
            self._statements.append(
                f"MATCH (a:CanonicalNode {{id: '{_esc(ma.from_node_id)}'}}),"
                f" (b:CanonicalNode {{id: '{_esc(ma.to_node_id)}'}})"
                f" MERGE (a)-[r:SAME_AS {props}]->(b)"
            )

    def _merge_support_edges(self) -> None:
        """Create SUPPORTED_BY edges from canonical nodes to EvidenceSpans.

        Uses the evidence_ids field on each assertion.  One canonical node
        may be supported by many spans via many assertions.
        """
        canonical_ids = {n.id for n in self.snapshot.canonical_nodes}
        evidence_ids = {e.id for e in self.snapshot.evidence_spans}

        for assertion in self.snapshot.relationship_assertions:
            if assertion.from_node_id not in canonical_ids:
                continue
            for span_id in assertion.evidence_ids:
                if span_id not in evidence_ids:
                    continue
                self._statements.append(
                    f"MATCH (c:CanonicalNode {{id: '{_esc(assertion.from_node_id)}'}}),"
                    f" (e:EvidenceSpan {{id: '{_esc(span_id)}'}})"
                    f" MERGE (c)-[r:SUPPORTED_BY {{assertion_id: '{_esc(assertion.id)}'}}]->(e)"
                )

    def _merge_evidence_relationships(self) -> None:
        """Create DocumentVersion -> Section -> Chunk evidence chain edges."""
        for sec in self.snapshot.sections:
            self._statements.append(
                f"MATCH (dv:DocumentVersion {{id: '{_esc(sec.document_version_id)}'}}),"
                f" (s:Section {{id: '{_esc(sec.id)}'}})"
                f" MERGE (dv)-[:HAS_SECTION]->(s)"
            )
        for chunk in self.snapshot.chunks:
            self._statements.append(
                f"MATCH (s:Section {{id: '{_esc(chunk.section_id)}'}}),"
                f" (c:Chunk {{id: '{_esc(chunk.id)}'}})"
                f" MERGE (s)-[:HAS_CHUNK]->(c)"
            )
        for span in self.snapshot.evidence_spans:
            self._statements.append(
                f"MATCH (dv:DocumentVersion {{id: '{_esc(span.document_version_id)}'}}),"
                f" (e:EvidenceSpan {{id: '{_esc(span.id)}'}})"
                f" MERGE (dv)-[:HAS_SPAN]->(e)"
            )

    def _merge_fast_edges(self) -> None:
        """Load supplemental fast edges that have no corresponding assertion.

        Edges whose ``assertion_id`` is already loaded by a richer assertion
        path are skipped. Assertions that point at non-canonical nodes (for
        example concept -> DocumentVersion support edges) still need their fast
        edge loaded because ``_merge_assertion_edges`` only covers
        canonical-to-canonical assertions.
        """
        canonical_ids = {n.id for n in self.snapshot.canonical_nodes}
        evidence_ids = {e.id for e in self.snapshot.evidence_spans}
        handled_assertion_ids = {
            assertion.id
            for assertion in self.snapshot.relationship_assertions
            if assertion.from_node_id in canonical_ids and assertion.to_node_id in canonical_ids
        }
        handled_assertion_ids.update(
            assertion.id
            for assertion in self.snapshot.relationship_assertions
            if assertion.from_node_id in canonical_ids
            and any(evidence_id in evidence_ids for evidence_id in assertion.evidence_ids)
        )

        edges = list(self.snapshot.fast_edges)
        if self.edge_snapshot_path and self.edge_snapshot_path.exists():
            import json

            data = json.loads(self.edge_snapshot_path.read_text(encoding="utf-8"))
            edges.extend(data.get("edges", []))

        for edge in edges:
            aid = edge.get("assertion_id", "")
            if aid and aid in handled_assertion_ids:
                continue  # already handled as a rich assertion edge
            eid = edge.get("id", "")
            etype = edge.get("edge_type", "RELATED_TO")
            from_id = edge.get("from_node_id", "")
            to_id = edge.get("to_node_id", "")
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
        "display_label": node.display_label,
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


def _extract_taxonomy_segments(
    canonical_nodes: list[CanonicalNode],
) -> dict[str, tuple[str, str]]:
    """Return a map of segment_id -> (kind, human_label).

    Scans every ``taxonomy_path`` on canonical nodes and extracts the
    unique Taxonomy / Topic / Subtopic segments.
    """
    segments: dict[str, tuple[str, str]] = {}
    for node in canonical_nodes:
        tp = node.taxonomy_path
        if not tp:
            continue
        tp = _normalise_taxonomy_path(tp)
        for seg in tp:
            kind = _taxonomy_segment_kind(seg)
            label = _taxonomy_segment_label(seg)
            segments[seg] = (kind, label)
    return segments


def _normalise_taxonomy_path(path: list[str]) -> list[str]:
    """Ensure taxonomy paths use the prefixed format.

    Old-format single-element roots like ``['architecture']`` are left
    as-is because they correspond to the taxonomy root canonical nodes.
    Three-element paths are already in the correct format.
    """
    if len(path) == 1 and not path[0].startswith("taxonomy-"):
        # Legacy short root — prepend taxonomy- prefix for consistency
        return [f"taxonomy-{path[0]}"]
    return list(path)


def _taxonomy_segment_kind(seg: str) -> str:
    if seg.startswith("taxonomy-"):
        return "taxonomy"
    if seg.startswith("topic-"):
        return "topic"
    if seg.startswith("subtopic-"):
        return "subtopic"
    return "taxonomy"


def _taxonomy_segment_label(seg: str) -> str:
    """Derive a human-readable label from a taxonomy segment slug."""
    # Strip known prefixes
    for prefix in ("taxonomy-", "topic-", "subtopic-"):
        if seg.startswith(prefix):
            seg = seg[len(prefix):]
            break
    # Replace hyphens with spaces and title-case
    return seg.replace("-", " ").title()


def _assertion_edge_cypher(assertion: RelationshipAssertion) -> str:
    """Build a MERGE statement for a rich assertion edge."""
    etype = assertion.edge_type.value
    props = _escape_props({
        "assertion_id": assertion.id,
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
    return (
        f"MATCH (a:CanonicalNode {{id: '{_esc(assertion.from_node_id)}'}}),"
        f" (b:CanonicalNode {{id: '{_esc(assertion.to_node_id)}'}})"
        f" MERGE (a)-[r:{_esc(etype)} {props}]->(b)"
    )
