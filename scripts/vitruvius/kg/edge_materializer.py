"""Edge materializer — creates fast traversal edges from validated assertions.

For every validated ``RelationshipAssertion``, produces a direct edge record
that can be written to:

- A file-native JSON snapshot (default, no DB required)
- Neo4j (when ``kg_transition.neo4j_backend`` is enabled)

The assertion node remains the source of truth; the materialized edge is a
read-optimized traversal structure.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .enums import EdgeType, ValidationState
from .json_evidence_store import KgV2Snapshot
from .schemas import PlacementAssertion, RelationshipAssertion


# ---------------------------------------------------------------------------
# Fast edge record
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class FastEdge:
    """A denormalized edge suitable for graph traversal queries."""

    id: str
    edge_type: EdgeType
    from_node_id: str
    to_node_id: str
    assertion_id: str
    confidence: float
    validation_status: ValidationState
    evidence_span_count: int
    document_version_count: int


# ---------------------------------------------------------------------------
# Materializer
# ---------------------------------------------------------------------------

class EdgeMaterializer:
    """Materialize fast edges from validated relationship assertions."""

    def __init__(self, snapshot: KgV2Snapshot | None = None) -> None:
        self.snapshot = snapshot or KgV2Snapshot()
        self._edges: list[FastEdge] = []

    # -- public API ---------------------------------------------------------

    def _node_exists(self, node_id: str) -> bool:
        """Check whether a node ID exists in the snapshot's canonical nodes."""
        if not self.snapshot.canonical_nodes:
            return True  # No snapshot provided — skip validation
        return any(n.id == node_id for n in self.snapshot.canonical_nodes)

    def materialize(
        self,
        assertions: list[RelationshipAssertion],
        *,
        skip_unvalidated: bool = True,
    ) -> list[FastEdge]:
        """Convert relationship assertions to fast edges, appending to internal state."""
        for assertion in assertions:
            if skip_unvalidated and assertion.validation_status != ValidationState.VALIDATED:
                continue
            if not self._node_exists(assertion.from_node_id):
                continue
            if not self._node_exists(assertion.to_node_id):
                continue
            edge = self._to_fast_edge(assertion)
            self._edges.append(edge)
        return list(self._edges)

    def materialize_placements(
        self,
        placements: list[PlacementAssertion],
        *,
        skip_unvalidated: bool = True,
    ) -> list[FastEdge]:
        """Convert placement assertions to BELONGS_TO fast edges."""
        for placement in placements:
            if skip_unvalidated and placement.validation_status != ValidationState.VALIDATED:
                continue
            if not self._node_exists(placement.node_id):
                continue
            if not self._node_exists(placement.parent_node_id):
                continue
            edge = FastEdge(
                id=f"edge-{placement.id}",
                edge_type=EdgeType.BELONGS_TO,
                from_node_id=placement.node_id,
                to_node_id=placement.parent_node_id,
                assertion_id=placement.id,
                confidence=placement.confidence,
                validation_status=placement.validation_status,
                evidence_span_count=len(placement.evidence_ids),
                document_version_count=0,
            )
            self._edges.append(edge)
        return list(self._edges)

    def write_snapshot(self, out_path: Any | None = None) -> Any:
        """Persist materialized edges alongside the snapshot.

        For now this returns the edge list as a simple JSON-serializable
        structure.  A future Neo4j writer will convert these to Cypher
        ``CREATE`` statements.
        """
        payload = {
            "schema_version": "2.0.0-alpha",
            "edge_count": len(self._edges),
            "edges": [
                {
                    "id": e.id,
                    "edge_type": e.edge_type.value,
                    "from_node_id": e.from_node_id,
                    "to_node_id": e.to_node_id,
                    "assertion_id": e.assertion_id,
                    "confidence": e.confidence,
                    "validation_status": e.validation_status.value,
                    "evidence_span_count": e.evidence_span_count,
                    "document_version_count": e.document_version_count,
                }
                for e in self._edges
            ],
        }
        if out_path is not None:
            import json
            from pathlib import Path

            Path(out_path).write_text(
                json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False),
                encoding="utf-8",
            )
        return payload

    # -- internal -----------------------------------------------------------

    @staticmethod
    def _to_fast_edge(assertion: RelationshipAssertion) -> FastEdge:
        return FastEdge(
            id=f"edge-{assertion.id}",
            edge_type=assertion.edge_type,
            from_node_id=assertion.from_node_id,
            to_node_id=assertion.to_node_id,
            assertion_id=assertion.id,
            confidence=assertion.confidence,
            validation_status=assertion.validation_status,
            evidence_span_count=len(assertion.evidence_ids),
            document_version_count=len(assertion.document_version_ids),
        )
