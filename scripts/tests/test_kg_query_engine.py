"""Tests for ``vitruvius.kg.query_engine``."""

from __future__ import annotations

from pathlib import Path

import pytest

from vitruvius.kg.enums import EdgeType, InferenceType, ValidationState
from vitruvius.kg.json_evidence_store import KgV2Snapshot
from vitruvius.kg.query_engine import QueryEngine
from vitruvius.kg.schemas import (
    CanonicalNode,
    DocumentVersion,
    EvidenceSpan,
    RelationshipAssertion,
    TextRangeSelector,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_engine() -> QueryEngine:
    snap = KgV2Snapshot()

    # Nodes
    snap.canonical_nodes.extend(
        [
            CanonicalNode(
                id="concept-floor-area",
                type="concept",
                label="Floor Area",
                slug="floor-area",
            ),
            CanonicalNode(
                id="concept-building-height",
                type="concept",
                label="Building Height",
                slug="building-height",
            ),
            CanonicalNode(
                id="concept-fire-safety",
                type="concept",
                label="Fire Safety",
                slug="fire-safety",
            ),
        ]
    )

    # Document version (should also be queryable)
    snap.document_versions.append(
        DocumentVersion(
            id="docv-pd-1096-v1",
            document_id="doc-pd-1096",
            title="PD 1096 National Building Code",
            source_uri="sources/pd-1096.md",
            sha256="a" * 64,
            created_at="2026-01-01T00:00:00Z",
        )
    )

    # Assertions
    snap.relationship_assertions.extend(
        [
            RelationshipAssertion(
                id="assert-rel-001",
                edge_type=EdgeType.RELATED_TO,
                from_node_id="concept-floor-area",
                to_node_id="concept-building-height",
                reasoning_summary="Both govern spatial parameters.",
                inference_type=InferenceType.DIRECT_CITATION,
                confidence=0.92,
                validation_status=ValidationState.VALIDATED,
                evidence_ids=["span-001"],
            ),
            RelationshipAssertion(
                id="assert-rel-002",
                edge_type=EdgeType.DEPENDS_ON,
                from_node_id="concept-building-height",
                to_node_id="concept-floor-area",
                reasoning_summary="Height depends on floor plate.",
                inference_type=InferenceType.DIRECT_CITATION,
                confidence=0.85,
                validation_status=ValidationState.VALIDATED,
                evidence_ids=["span-001"],
            ),
            RelationshipAssertion(
                id="assert-rel-003",
                edge_type=EdgeType.APPLIES_TO,
                from_node_id="concept-fire-safety",
                to_node_id="concept-building-height",
                reasoning_summary="Fire safety applies to height.",
                inference_type=InferenceType.RULE_BASED_DERIVATION,
                confidence=0.78,
                validation_status=ValidationState.REVIEW_REQUIRED,
                evidence_ids=["span-001"],
            ),
        ]
    )

    # Fast edges
    snap.fast_edges = [
        {
            "id": "edge-assert-rel-001",
            "edge_type": "RELATED_TO",
            "from_node_id": "concept-floor-area",
            "to_node_id": "concept-building-height",
            "assertion_id": "assert-rel-001",
            "confidence": 0.92,
            "validation_status": "validated",
            "evidence_span_count": 1,
            "document_version_count": 0,
        },
        {
            "id": "edge-assert-rel-002",
            "edge_type": "DEPENDS_ON",
            "from_node_id": "concept-building-height",
            "to_node_id": "concept-floor-area",
            "assertion_id": "assert-rel-002",
            "confidence": 0.85,
            "validation_status": "validated",
            "evidence_span_count": 1,
            "document_version_count": 0,
        },
    ]

    return QueryEngine(snap)


# ---------------------------------------------------------------------------
# get_node_by_id
# ---------------------------------------------------------------------------

class TestGetNodeById:
    def test_returns_node(self) -> None:
        engine = _make_engine()
        node = engine.get_node_by_id("concept-floor-area")
        assert node is not None
        assert node.label == "Floor Area"

    def test_returns_none_for_unknown(self) -> None:
        engine = _make_engine()
        assert engine.get_node_by_id("concept-missing") is None



# ---------------------------------------------------------------------------
# get_assertions_for_node
# ---------------------------------------------------------------------------

class TestGetAssertionsForNode:
    def test_bidirectional_lookup(self) -> None:
        engine = _make_engine()
        assertions = engine.get_assertions_for_node("concept-floor-area")
        assert len(assertions) == 2  # rel-001 (from) + rel-002 (to)
        ids = {a.id for a in assertions}
        assert ids == {"assert-rel-001", "assert-rel-002"}

    def test_empty_for_unknown(self) -> None:
        engine = _make_engine()
        assert engine.get_assertions_for_node("concept-missing") == []


# ---------------------------------------------------------------------------
# get_edges_for_node
# ---------------------------------------------------------------------------

class TestGetEdgesForNode:
    def test_bidirectional_lookup(self) -> None:
        engine = _make_engine()
        edges = engine.get_edges_for_node("concept-building-height")
        assert len(edges) == 2  # edge-001 (to) + edge-002 (from)
        ids = {e["id"] for e in edges}
        assert ids == {"edge-assert-rel-001", "edge-assert-rel-002"}

    def test_empty_for_unknown(self) -> None:
        engine = _make_engine()
        assert engine.get_edges_for_node("concept-missing") == []


# ---------------------------------------------------------------------------
# search_nodes_by_label
# ---------------------------------------------------------------------------

class TestSearchNodesByLabel:
    def test_exact_match(self) -> None:
        engine = _make_engine()
        results = engine.search_nodes_by_label("Floor Area")
        assert len(results) == 1
        assert results[0].id == "concept-floor-area"

    def test_case_insensitive(self) -> None:
        engine = _make_engine()
        results = engine.search_nodes_by_label("floor area")
        assert len(results) == 1
        assert results[0].id == "concept-floor-area"

    def test_substring_match(self) -> None:
        engine = _make_engine()
        results = engine.search_nodes_by_label("building")
        assert len(results) == 1  # Building Height only (documents are not CanonicalNodes)
        ids = {n.id for n in results}
        assert "concept-building-height" in ids

    def test_respects_limit(self) -> None:
        engine = _make_engine()
        results = engine.search_nodes_by_label("a", limit=1)
        assert len(results) == 1

    def test_empty_for_no_match(self) -> None:
        engine = _make_engine()
        assert engine.search_nodes_by_label("xyz") == []


# ---------------------------------------------------------------------------
# from_path factory
# ---------------------------------------------------------------------------

class TestFromPath:
    def test_roundtrip(self, tmp_path: Path) -> None:
        engine = _make_engine()
        path = tmp_path / "snapshot.json"
        engine.snapshot.write(path)

        loaded = QueryEngine.from_path(path)
        assert loaded.get_node_by_id("concept-floor-area") is not None
        assert len(loaded.get_assertions_for_node("concept-floor-area")) == 2
        assert len(loaded.get_edges_for_node("concept-building-height")) == 2
