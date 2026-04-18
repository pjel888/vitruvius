"""File-native JSON snapshot store for v2-alpha evidence graphs.

Aligns with Principle P1 (Filesystem is the database).  All evidence-graph
entities are written as deterministic, versioned JSON snapshots under
``005_Operational-Intelligence-Layer/graph/kg-v2/``.

When Neo4j/PostgreSQL are provisioned, these snapshots become the
rebuild-source-of-truth for the operational indexes.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .schemas import (
    CanonicalNode,
    Chunk,
    DocumentVersion,
    EvidenceSpan,
    MergeAssertion,
    PlacementAssertion,
    RelationshipAssertion,
    Section,
)


SCHEMA_VERSION = "2.0.0-alpha"


class KgV2Snapshot:
    """In-memory representation of a v2-alpha knowledge-graph snapshot."""

    def __init__(self) -> None:
        self.schema_version: str = SCHEMA_VERSION
        self.created_at: str = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        self.metadata: dict[str, Any] = {}
        self.document_versions: list[DocumentVersion] = []
        self.sections: list[Section] = []
        self.chunks: list[Chunk] = []
        self.evidence_spans: list[EvidenceSpan] = []
        self.canonical_nodes: list[CanonicalNode] = []
        self.relationship_assertions: list[RelationshipAssertion] = []
        self.placement_assertions: list[PlacementAssertion] = []
        self.merge_assertions: list[MergeAssertion] = []

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "created_at": self.created_at,
            "metadata": self.metadata,
            "document_versions": [dv.model_dump(mode="json") for dv in self.document_versions],
            "sections": [s.model_dump(mode="json") for s in self.sections],
            "chunks": [c.model_dump(mode="json") for c in self.chunks],
            "evidence_spans": [es.model_dump(mode="json") for es in self.evidence_spans],
            "canonical_nodes": [cn.model_dump(mode="json") for cn in self.canonical_nodes],
            "relationship_assertions": [ra.model_dump(mode="json") for ra in self.relationship_assertions],
            "placement_assertions": [pa.model_dump(mode="json") for pa in self.placement_assertions],
            "merge_assertions": [ma.model_dump(mode="json") for ma in self.merge_assertions],
        }

    def write(self, path: Path) -> None:
        """Write deterministic JSON snapshot (sorted keys, no trailing newline)."""
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = self.to_dict()
        text = json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False)
        path.write_text(text, encoding="utf-8")

    @classmethod
    def read(cls, path: Path) -> "KgV2Snapshot":
        """Read a snapshot from disk and rehydrate Pydantic models."""
        data = json.loads(path.read_text(encoding="utf-8"))
        snap = cls()
        snap.schema_version = data.get("schema_version", SCHEMA_VERSION)
        snap.created_at = data.get("created_at", "")
        snap.metadata = data.get("metadata", {})
        snap.document_versions = [DocumentVersion(**d) for d in data.get("document_versions", [])]
        snap.sections = [Section(**d) for d in data.get("sections", [])]
        snap.chunks = [Chunk(**d) for d in data.get("chunks", [])]
        snap.evidence_spans = [EvidenceSpan(**d) for d in data.get("evidence_spans", [])]
        snap.canonical_nodes = [CanonicalNode(**d) for d in data.get("canonical_nodes", [])]
        snap.relationship_assertions = [RelationshipAssertion(**d) for d in data.get("relationship_assertions", [])]
        snap.placement_assertions = [PlacementAssertion(**d) for d in data.get("placement_assertions", [])]
        snap.merge_assertions = [MergeAssertion(**d) for d in data.get("merge_assertions", [])]
        return snap

    def checksum(self) -> str:
        """SHA-256 of the canonical JSON representation."""
        payload = self.to_dict()
        canonical = json.dumps(payload, sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()

    def entity_counts(self) -> dict[str, int]:
        return {
            "document_versions": len(self.document_versions),
            "sections": len(self.sections),
            "chunks": len(self.chunks),
            "evidence_spans": len(self.evidence_spans),
            "canonical_nodes": len(self.canonical_nodes),
            "relationship_assertions": len(self.relationship_assertions),
            "placement_assertions": len(self.placement_assertions),
            "merge_assertions": len(self.merge_assertions),
        }
