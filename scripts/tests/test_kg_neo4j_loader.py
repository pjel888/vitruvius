"""Tests for ``vitruvius.kg.neo4j_loader``."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock

import pytest

from vitruvius.kg.enums import EdgeType, InferenceType, ValidationState
from vitruvius.kg.json_evidence_store import KgV2Snapshot
from vitruvius.kg.neo4j_loader import Neo4jLoader, _esc, _escape_props
from vitruvius.kg.schemas import (
    CanonicalNode,
    Chunk,
    DocumentVersion,
    EvidenceSpan,
    MergeAssertion,
    PlacementAssertion,
    RelationshipAssertion,
    Section,
    TextRangeSelector,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_snapshot() -> KgV2Snapshot:
    snap = KgV2Snapshot()
    snap.canonical_nodes.append(
        CanonicalNode(
            id="taxonomy-spaces-occupancy",
            type="taxonomy",
            label="Spaces & Occupancy",
            slug="spaces-occupancy",
            taxonomy_path=["spaces-occupancy"],
        )
    )
    snap.canonical_nodes.append(
        CanonicalNode(
            id="concept-floor-area",
            type="concept",
            label="Floor Area",
            slug="floor-area",
            taxonomy_path=["taxonomy-spaces-occupancy", "topic-building-planning", "subtopic-dimensions"],
        )
    )
    snap.canonical_nodes.append(
        CanonicalNode(
            id="concept-building-height",
            type="concept",
            label="Building Height",
            slug="building-height",
            taxonomy_path=["taxonomy-spaces-occupancy", "topic-building-planning", "subtopic-dimensions"],
        )
    )
    snap.document_versions.append(
        DocumentVersion(
            id="docv-pd-1096-v1",
            document_id="doc-pd-1096",
            title="PD 1096",
            source_uri="sources/pd-1096.md",
            sha256="a" * 64,
            created_at="2026-01-01T00:00:00Z",
        )
    )
    snap.sections.append(
        Section(
            id="sec-pd-1096-0",
            document_version_id="docv-pd-1096-v1",
            title="Overview",
            level=2,
        )
    )
    snap.chunks.append(
        Chunk(
            id="chk-pd-1096-0000",
            section_id="sec-pd-1096-0",
            document_version_id="docv-pd-1096-v1",
            text="Sample chunk.",
            char_start=0,
            char_end=13,
            token_count=3,
        )
    )
    snap.evidence_spans.append(
        EvidenceSpan(
            id="span-001",
            document_id="doc-pd-1096",
            document_version_id="docv-pd-1096-v1",
            selector=TextRangeSelector(kind="text_range", quote="Sample", char_start=0, char_end=6),
            quote="Sample",
            normalized_text="sample",
            parser="test",
            checksum="b" * 64,
        )
    )
    snap.relationship_assertions.append(
        RelationshipAssertion(
            id="assert-rel-001",
            edge_type=EdgeType.RELATED_TO,
            from_node_id="concept-floor-area",
            to_node_id="concept-building-height",
            reasoning_summary="Floor area and height are spatial dimensions.",
            inference_type=InferenceType.HUMAN_AUTHORED,
            confidence=0.99,
            validation_status=ValidationState.VALIDATED,
            evidence_ids=["span-001"],
        )
    )
    # Orphan assertion — endpoint not in canonical_nodes
    snap.relationship_assertions.append(
        RelationshipAssertion(
            id="assert-rel-orphan",
            edge_type=EdgeType.SUPPORTED_BY,
            from_node_id="concept-floor-area",
            to_node_id="handout-missing",
            reasoning_summary="Missing endpoint.",
            inference_type=InferenceType.HUMAN_AUTHORED,
            confidence=0.5,
            validation_status=ValidationState.CANDIDATE,
        )
    )
    # Fast edge without assertion_id — should be preserved
    snap.fast_edges.append(
        {
            "id": "edge-standalone-001",
            "edge_type": "RELATED_TO",
            "from_node_id": "concept-floor-area",
            "to_node_id": "concept-building-height",
            "confidence": 0.75,
        }
    )
    # Fast edge WITH assertion_id matching a RelationshipAssertion — skipped
    snap.fast_edges.append(
        {
            "id": "edge-assert-rel-001",
            "edge_type": "RELATED_TO",
            "from_node_id": "concept-floor-area",
            "to_node_id": "concept-building-height",
            "assertion_id": "assert-rel-001",
            "confidence": 0.99,
            "validation_status": "validated",
            "evidence_span_count": 1,
            "document_version_count": 0,
        }
    )
    return snap


# ---------------------------------------------------------------------------
# Unit tests
# ---------------------------------------------------------------------------

class TestEscaping:
    def test_escapes_single_quotes(self) -> None:
        assert _esc("it's") == "it\\'s"

    def test_escapes_backslashes(self) -> None:
        assert _esc("a\\b") == "a\\\\b"


class TestEscapeProps:
    def test_string_value(self) -> None:
        assert _escape_props({"name": "test"}) == "{name: 'test'}"

    def test_int_value(self) -> None:
        assert _escape_props({"count": 42}) == "{count: 42}"

    def test_float_value(self) -> None:
        assert _escape_props({"score": 0.5}) == "{score: 0.5}"

    def test_bool_value(self) -> None:
        assert _escape_props({"ok": True}) == "{ok: true}"

    def test_none_value(self) -> None:
        assert _escape_props({"missing": None}) == "{missing: null}"

    def test_list_value(self) -> None:
        assert _escape_props({"tags": ["a", "b"]}) == "{tags: ['a', 'b']}"


class TestToCypher:
    def test_generates_canonical_node_merge(self) -> None:
        loader = Neo4jLoader(_make_snapshot())
        statements = loader.to_cypher()
        merge = [s for s in statements if "MERGE (n:CanonicalNode" in s]
        assert len(merge) == 3
        ids = ["taxonomy-spaces-occupancy", "concept-floor-area", "concept-building-height"]
        for node_id in ids:
            assert any(node_id in s for s in merge)

    def test_generates_taxonomy_nodes(self) -> None:
        loader = Neo4jLoader(_make_snapshot())
        statements = loader.to_cypher()

        tax = [s for s in statements if "MERGE (n:Taxonomy" in s]
        assert len(tax) == 1
        assert "taxonomy-spaces-occupancy" in tax[0]

        topics = [s for s in statements if "MERGE (n:Topic" in s]
        assert len(topics) == 1
        assert "topic-building-planning" in topics[0]

        subtopics = [s for s in statements if "MERGE (n:Subtopic" in s]
        assert len(subtopics) == 1
        assert "subtopic-dimensions" in subtopics[0]

    def test_generates_taxonomy_hierarchy_edges(self) -> None:
        loader = Neo4jLoader(_make_snapshot())
        statements = loader.to_cypher()
        has_child = [s for s in statements if "HAS_CHILD" in s]
        # taxonomy -> topic -> subtopic  (2 edges)
        assert len(has_child) == 2
        assert any("taxonomy-spaces-occupancy" in s and "topic-building-planning" in s for s in has_child)
        assert any("topic-building-planning" in s and "subtopic-dimensions" in s for s in has_child)

    def test_generates_belongs_to_edges(self) -> None:
        loader = Neo4jLoader(_make_snapshot())
        statements = loader.to_cypher()
        belongs = [s for s in statements if "BELONGS_TO" in s]
        # Both concepts point to the same subtopic leaf
        assert len(belongs) == 2
        assert all("subtopic-dimensions" in s for s in belongs)

    def test_generates_document_version_merge(self) -> None:
        loader = Neo4jLoader(_make_snapshot())
        statements = loader.to_cypher()
        merge = [s for s in statements if "MERGE (d:DocumentVersion" in s]
        assert len(merge) == 1
        assert "docv-pd-1096-v1" in merge[0]

    def test_generates_section_merge(self) -> None:
        loader = Neo4jLoader(_make_snapshot())
        statements = loader.to_cypher()
        merge = [s for s in statements if "MERGE (s:Section" in s]
        assert len(merge) == 1
        assert "sec-pd-1096-0" in merge[0]

    def test_generates_chunk_merge(self) -> None:
        loader = Neo4jLoader(_make_snapshot())
        statements = loader.to_cypher()
        merge = [s for s in statements if "MERGE (c:Chunk" in s]
        assert len(merge) == 1
        assert "chk-pd-1096-0000" in merge[0]

    def test_generates_evidence_span_merge(self) -> None:
        loader = Neo4jLoader(_make_snapshot())
        statements = loader.to_cypher()
        merge = [s for s in statements if "MERGE (e:EvidenceSpan" in s]
        assert len(merge) == 1
        assert "span-001" in merge[0]
        assert "selector_kind" in merge[0]
        assert "text_range" in merge[0]
        assert "selector" in merge[0]

    def test_generates_evidence_span_merge_with_pdf_bbox(self) -> None:
        from vitruvius.kg.schemas import PdfBboxSelector

        snap = _make_snapshot()
        snap.evidence_spans.append(
            EvidenceSpan(
                id="span-pdf-002",
                document_id="doc-pd-1096",
                document_version_id="docv-pd-1096-v1",
                selector=PdfBboxSelector(
                    kind="pdf_bbox", page=3, bbox=[10.0, 20.0, 30.0, 40.0], quote="hello"
                ),
                quote="hello",
                normalized_text="hello",
                parser="test",
                checksum="b" * 64,
                created_at="2026-01-01T00:00:00Z",
            )
        )
        loader = Neo4jLoader(snap)
        statements = loader.to_cypher()
        merge = [s for s in statements if "MERGE (e:EvidenceSpan" in s and "span-pdf-002" in s]
        assert len(merge) == 1
        assert "selector_kind" in merge[0]
        assert "pdf_bbox" in merge[0]
        assert "bbox" in merge[0]

    def test_generates_assertion_edge_not_node(self) -> None:
        """Assertions become typed edges, not standalone Assertion nodes."""
        loader = Neo4jLoader(_make_snapshot())
        statements = loader.to_cypher()

        # No Assertion nodes should be created
        assertion_nodes = [s for s in statements if "MERGE (a:Assertion" in s]
        assert len(assertion_nodes) == 0

        # But a RELATED_TO edge should exist with rich properties
        edges = [s for s in statements if "RELATED_TO" in s and "assert-rel-001" in s]
        assert len(edges) >= 1
        edge = edges[0]
        assert "concept-floor-area" in edge
        assert "concept-building-height" in edge
        assert "reasoning_summary" in edge
        assert "confidence" in edge

    def test_skips_orphan_assertions(self) -> None:
        """Assertions with missing endpoints must not produce Cypher."""
        loader = Neo4jLoader(_make_snapshot())
        statements = loader.to_cypher()
        orphan_edges = [s for s in statements if "assert-rel-orphan" in s]
        assert len(orphan_edges) == 0

    def test_generates_support_edges(self) -> None:
        """SUPPORTED_BY edges link canonical nodes to EvidenceSpans."""
        loader = Neo4jLoader(_make_snapshot())
        statements = loader.to_cypher()
        support = [s for s in statements if "SUPPORTED_BY" in s]
        assert len(support) == 1
        assert "concept-floor-area" in support[0]
        assert "span-001" in support[0]
        assert "assert-rel-001" in support[0]

    def test_generates_fast_edge_relationship(self) -> None:
        loader = Neo4jLoader(_make_snapshot())
        statements = loader.to_cypher()
        rel = [s for s in statements if "MERGE (from_node)-[r:RELATED_TO" in s]
        # Only the standalone fast edge is emitted; the one with a matching
        # assertion_id is suppressed because the rich assertion edge already
        # carries the same information.
        assert len(rel) == 1
        assert "edge-standalone-001" in rel[0]

    def test_reads_external_edge_snapshot(self, tmp_path: Path) -> None:
        snap = _make_snapshot()
        snap.fast_edges = []
        edge_file = tmp_path / "edges.json"
        # External edge with no matching assertion — should be loaded
        edge_file.write_text(
            '{"edges": [{"id": "edge-x", "edge_type": "DEPENDS_ON", '
            '"from_node_id": "concept-floor-area", "to_node_id": "concept-building-height", '
            '"assertion_id": "assert-external-999", "confidence": 0.5}]}',
            encoding="utf-8",
        )
        loader = Neo4jLoader(snap, edge_snapshot_path=edge_file)
        statements = loader.to_cypher()
        rel = [s for s in statements if "MERGE (from_node)-[r:DEPENDS_ON" in s]
        assert len(rel) == 1
        assert "edge-x" in rel[0]

    def test_generates_placement_assertion_edges(self) -> None:
        snap = _make_snapshot()
        snap.placement_assertions.append(
            PlacementAssertion(
                id="assert-placement-001",
                node_id="concept-floor-area",
                parent_node_id="taxonomy-spaces-occupancy",
                reasoning_summary="Floor area belongs under spaces.",
                confidence=0.95,
                validation_status=ValidationState.VALIDATED,
            )
        )
        loader = Neo4jLoader(snap)
        statements = loader.to_cypher()
        edges = [s for s in statements if "BELONGS_TO" in s and "assert-placement-001" in s]
        assert len(edges) == 1
        assert "concept-floor-area" in edges[0]
        assert "taxonomy-spaces-occupancy" in edges[0]

    def test_generates_merge_assertion_edges(self) -> None:
        snap = _make_snapshot()
        snap.merge_assertions.append(
            MergeAssertion(
                id="assert-merge-001",
                from_node_id="concept-floor-area",
                to_node_id="concept-building-height",
                reasoning_summary="These are the same concept.",
                confidence=0.8,
                validation_status=ValidationState.CANDIDATE,
            )
        )
        loader = Neo4jLoader(snap)
        statements = loader.to_cypher()
        edges = [s for s in statements if "SAME_AS" in s and "assert-merge-001" in s]
        assert len(edges) == 1
        assert "concept-floor-area" in edges[0]
        assert "concept-building-height" in edges[0]


class TestWriteCypher:
    def test_writes_to_disk(self, tmp_path: Path) -> None:
        loader = Neo4jLoader(_make_snapshot())
        path = loader.write_cypher(tmp_path / "out.cypher")
        assert path.exists()
        text = path.read_text(encoding="utf-8")
        assert "MERGE (n:CanonicalNode" in text


class TestLoad:
    def test_returns_statements_when_flag_off(self) -> None:
        loader = Neo4jLoader(_make_snapshot())
        result = loader.load(client=None)
        assert result["executed"] is False
        assert result["statement_count"] > 0
        assert len(result["statements"]) > 0

    def test_executes_when_flag_on_and_client_provided(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(
            "vitruvius.kg.neo4j_loader.is_kg_neo4j_backend", lambda: True
        )
        loader = Neo4jLoader(_make_snapshot())
        client = MagicMock()
        result = loader.load(client=client)
        assert result["executed"] is True
        assert result["executed_count"] > 0
        assert result["error_count"] == 0
        assert client.run.call_count > 0
