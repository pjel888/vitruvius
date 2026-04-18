"""Query Engine v2 — file-native knowledge graph queries.

Loads a ``KgV2Snapshot`` from disk and provides fast, indexed lookups
over canonical nodes, assertions, and materialized edges.

No Neo4j or PostgreSQL is required.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .json_evidence_store import KgV2Snapshot
from .schemas import CanonicalNode, RelationshipAssertion


class QueryEngine:
    """In-memory query engine over a v2-alpha knowledge-graph snapshot."""

    def __init__(self, snapshot: KgV2Snapshot) -> None:
        self.snapshot = snapshot
        self._node_by_id: dict[str, CanonicalNode] = {}
        self._assertions_by_node: dict[str, list[RelationshipAssertion]] = {}
        self._edges_by_node: dict[str, list[dict[str, Any]]] = {}
        self._node_label_index: dict[str, list[str]] = {}
        self._build_indexes()

    # -- factory -------------------------------------------------------------

    @classmethod
    def from_path(cls, path: Path | str) -> "QueryEngine":
        """Load a snapshot from disk and return a ready QueryEngine."""
        snap = KgV2Snapshot.read(Path(path))
        return cls(snap)

    # -- public API ----------------------------------------------------------

    def get_node_by_id(self, node_id: str) -> CanonicalNode | None:
        """Return a canonical node by its exact ID."""
        return self._node_by_id.get(node_id)

    def get_assertions_for_node(
        self, node_id: str
    ) -> list[RelationshipAssertion]:
        """Return all relationship assertions where *node_id* is either
        the subject or the object.
        """
        return self._assertions_by_node.get(node_id, [])

    def get_edges_for_node(self, node_id: str) -> list[dict[str, Any]]:
        """Return all fast edges where *node_id* is either the source
        or the target.
        """
        return self._edges_by_node.get(node_id, [])

    def search_nodes_by_label(
        self, query: str, *, limit: int = 10
    ) -> list[CanonicalNode]:
        """Case-insensitive substring search over node labels."""
        q = query.lower()
        matched: list[CanonicalNode] = []
        for label, node_ids in self._node_label_index.items():
            if q in label:
                for nid in node_ids:
                    node = self._node_by_id.get(nid)
                    if node and node not in matched:
                        matched.append(node)
            if len(matched) >= limit:
                break
        return matched[:limit]

    # -- internal ------------------------------------------------------------

    def _build_indexes(self) -> None:
        # Node index
        for node in self.snapshot.canonical_nodes:
            self._node_by_id[node.id] = node
            label_key = node.label.lower()
            self._node_label_index.setdefault(label_key, []).append(node.id)

        # Document versions are *not* CanonicalNodes; they live in
        # snapshot.document_versions.  Downstream callers can traverse
        # assertions.edges to reach them via document_version_ids.

        # Assertion index (bidirectional)
        for assertion in self.snapshot.relationship_assertions:
            for nid in (assertion.from_node_id, assertion.to_node_id):
                self._assertions_by_node.setdefault(nid, []).append(assertion)

        # Edge index (bidirectional)
        for edge in self.snapshot.fast_edges:
            for nid in (edge["from_node_id"], edge["to_node_id"]):
                self._edges_by_node.setdefault(nid, []).append(edge)
