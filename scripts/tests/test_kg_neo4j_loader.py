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
            id="concept-floor-area",
            type="concept",
            label="Floor Area",
            slug="floor-area",
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
            to_node_id="concept-floor-area",
            reasoning_summary="Self-reference for testing.",
            inference_type=InferenceType.HUMAN_AUTHORED,
            confidence=0.99,
            validation_status=ValidationState.VALIDATED,
            evidence_ids=["span-001"],
        )
    )
    snap.fast_edges.append(
        {
            "id": "edge-assert-rel-001",
            "edge_type": "RELATED_TO",
            "from_node_id": "concept-floor-area",
            "to_node_id": "concept-floor-area",
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
        assert len(merge) == 1
        assert "concept-floor-area" in merge[0]

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

    def test_generates_assertion_merge(self) -> None:
        loader = Neo4jLoader(_make_snapshot())
        statements = loader.to_cypher()
        merge = [s for s in statements if "MERGE (a:Assertion" in s]
        assert len(merge) == 1
        assert "assert-rel-001" in merge[0]

    def test_generates_fast_edge_relationship(self) -> None:
        loader = Neo4jLoader(_make_snapshot())
        statements = loader.to_cypher()
        rel = [s for s in statements if "MERGE (from_node)-[r:RELATED_TO" in s]
        assert len(rel) == 1
        assert "edge-assert-rel-001" in rel[0]

    def test_reads_external_edge_snapshot(self, tmp_path: Path) -> None:
        snap = _make_snapshot()
        snap.fast_edges = []
        edge_file = tmp_path / "edges.json"
        edge_file.write_text(
            '{"edges": [{"id": "edge-x", "edge_type": "DEPENDS_ON", '
            '"from_node_id": "concept-floor-area", "to_node_id": "concept-floor-area", '
            '"assertion_id": "assert-rel-001", "confidence": 0.5}]}',
            encoding="utf-8",
        )
        loader = Neo4jLoader(snap, edge_snapshot_path=edge_file)
        statements = loader.to_cypher()
        rel = [s for s in statements if "MERGE (from_node)-[r:DEPENDS_ON" in s]
        assert len(rel) == 1
        assert "edge-x" in rel[0]


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
