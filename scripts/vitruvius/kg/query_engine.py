"""Query Engine v2 — file-native knowledge graph queries.

Loads a ``KgV2Snapshot`` from disk and provides fast, indexed lookups
over canonical nodes, assertions, and materialized edges.

No Neo4j or PostgreSQL is required.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .json_evidence_store import KgV2Snapshot
from .schemas import (
    CanonicalNode,
    EvidenceSpan,
    MergeAssertion,
    PlacementAssertion,
    RelationshipAssertion,
)


class QueryEngine:
    """In-memory query engine over a v2-alpha knowledge-graph snapshot."""

    def __init__(self, snapshot: KgV2Snapshot) -> None:
        self.snapshot = snapshot
        self._node_by_id: dict[str, CanonicalNode] = {}
        self._assertions_by_node: dict[str, list[RelationshipAssertion]] = {}
        self._placements_by_node: dict[str, list[PlacementAssertion]] = {}
        self._merges_by_node: dict[str, list[MergeAssertion]] = {}
        self._assertion_by_id: dict[str, RelationshipAssertion | PlacementAssertion | MergeAssertion] = {}
        self._evidence_by_id: dict[str, EvidenceSpan] = {}
        self._edges_by_node: dict[str, list[dict[str, Any]]] = {}
        self._node_label_index: dict[str, list[str]] = {}
        self._taxonomy_roots: list[CanonicalNode] = []
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

    def get_placement_for_node(self, node_id: str) -> list[PlacementAssertion]:
        """Return all placement assertions for *node_id*."""
        return self._placements_by_node.get(node_id, [])

    def get_merge_assertions_for_node(self, node_id: str) -> list[MergeAssertion]:
        """Return all merge assertions where *node_id* is either source or target."""
        return self._merges_by_node.get(node_id, [])

    def get_assertion_by_id(
        self, assertion_id: str
    ) -> RelationshipAssertion | PlacementAssertion | MergeAssertion | None:
        """Return any assertion (relationship, placement, or merge) by ID."""
        return self._assertion_by_id.get(assertion_id)

    def get_evidence_for_assertion(
        self, assertion_id: str
    ) -> list[EvidenceSpan]:
        """Return evidence spans linked to *assertion_id*."""
        assertion = self._assertion_by_id.get(assertion_id)
        if assertion is None:
            return []
        evidence_ids: list[str] = []
        if isinstance(assertion, (RelationshipAssertion, PlacementAssertion, MergeAssertion)):
            evidence_ids = getattr(assertion, "evidence_ids", [])
        return [self._evidence_by_id[eid] for eid in evidence_ids if eid in self._evidence_by_id]

    def get_evidence_for_node(self, node_id: str) -> list[EvidenceSpan]:
        """Return all evidence spans supporting *node_id* across all its assertions."""
        spans: list[EvidenceSpan] = []
        seen: set[str] = set()
        for assertion in self.get_assertions_for_node(node_id):
            for eid in assertion.evidence_ids:
                if eid not in seen and eid in self._evidence_by_id:
                    spans.append(self._evidence_by_id[eid])
                    seen.add(eid)
        for placement in self.get_placement_for_node(node_id):
            for eid in placement.evidence_ids:
                if eid not in seen and eid in self._evidence_by_id:
                    spans.append(self._evidence_by_id[eid])
                    seen.add(eid)
        return spans

    def get_node_neighborhood(
        self, node_id: str
    ) -> list[tuple[CanonicalNode, RelationshipAssertion]]:
        """Return related canonical nodes and the assertions that connect them."""
        results: list[tuple[CanonicalNode, RelationshipAssertion]] = []
        for assertion in self.get_assertions_for_node(node_id):
            other_id = (
                assertion.to_node_id
                if assertion.from_node_id == node_id
                else assertion.from_node_id
            )
            other_node = self._node_by_id.get(other_id)
            if other_node is not None:
                results.append((other_node, assertion))
        return results

    def get_taxonomy_tree(self) -> list[CanonicalNode]:
        """Return all taxonomy-root nodes."""
        return list(self._taxonomy_roots)

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
            if node.type.value == "taxonomy":
                self._taxonomy_roots.append(node)

        # Evidence index
        for span in self.snapshot.evidence_spans:
            self._evidence_by_id[span.id] = span

        # Assertion index (bidirectional)
        for assertion in self.snapshot.relationship_assertions:
            self._assertion_by_id[assertion.id] = assertion
            for nid in (assertion.from_node_id, assertion.to_node_id):
                self._assertions_by_node.setdefault(nid, []).append(assertion)

        # Placement assertion index
        for placement in self.snapshot.placement_assertions:
            self._assertion_by_id[placement.id] = placement
            self._placements_by_node.setdefault(placement.node_id, []).append(placement)

        # Merge assertion index (bidirectional)
        for merge in self.snapshot.merge_assertions:
            self._assertion_by_id[merge.id] = merge
            for nid in (merge.from_node_id, merge.to_node_id):
                self._merges_by_node.setdefault(nid, []).append(merge)

        # Edge index (bidirectional)
        for edge in self.snapshot.fast_edges:
            for nid in (edge["from_node_id"], edge["to_node_id"]):
                self._edges_by_node.setdefault(nid, []).append(edge)
