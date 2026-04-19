"""Tests for KG v2 graph visualization."""

from __future__ import annotations

from pathlib import Path

import pytest

from vitruvius.graph.visualize import (
    _detect_snapshot_version,
    generate_html,
    run_visualize_graph,
)
from vitruvius.kg.enums import EdgeType, NodeType, ValidationState
from vitruvius.kg.json_evidence_store import KgV2Snapshot
from vitruvius.kg.schemas import (
    CanonicalNode,
    EvidenceSpan,
    MarkdownRangeSelector,
    PlacementAssertion,
    RelationshipAssertion,
)


def _make_v2_snapshot() -> KgV2Snapshot:
    snap = KgV2Snapshot()
    snap.canonical_nodes.append(
        CanonicalNode(
            id="taxonomy-building-code",
            type=NodeType.TAXONOMY,
            label="Building Code",
            slug="building-code",
            taxonomy_path=["building-code"],
            status=ValidationState.VALIDATED,
            confidence=1.0,
        )
    )
    snap.canonical_nodes.append(
        CanonicalNode(
            id="concept-permit",
            type=NodeType.CONCEPT,
            label="Building Permit",
            slug="building-permit",
            summary="A permit is required for construction.",
            taxonomy_path=["building-code"],
            status=ValidationState.VALIDATED,
            confidence=0.95,
        )
    )
    snap.canonical_nodes.append(
        CanonicalNode(
            id="concept-variance",
            type=NodeType.CONCEPT,
            label="Zoning Variance",
            slug="zoning-variance",
            summary="Exception to zoning rules.",
            status=ValidationState.CANDIDATE,
            confidence=0.8,
        )
    )
    snap.evidence_spans.append(
        EvidenceSpan(
            id="span-001",
            document_id="doc-pd1096",
            document_version_id="docv-pd1096-v1",
            selector=MarkdownRangeSelector(heading_path=["Section 1"]),
            quote="A building permit is required.",
            normalized_text="A building permit is required.",
            parser="markdown",
            checksum="a" * 64,
        )
    )
    snap.relationship_assertions.append(
        RelationshipAssertion(
            id="assert-rel-001",
            edge_type=EdgeType.DEPENDS_ON,
            from_node_id="concept-permit",
            to_node_id="concept-variance",
            reasoning_summary="Permits depend on zoning compliance",
            inference_type="direct_citation",
            confidence=0.9,
            validation_status=ValidationState.VALIDATED,
            evidence_ids=["span-001"],
        )
    )
    snap.placement_assertions.append(
        PlacementAssertion(
            id="assert-placement-001",
            node_id="concept-permit",
            parent_node_id="taxonomy-building-code",
            reasoning_summary="Placed under building code",
            confidence=0.95,
            validation_status=ValidationState.VALIDATED,
            evidence_ids=["span-001"],
        )
    )
    snap.fast_edges.append(
        {
            "id": "edge-001",
            "edge_type": "DEPENDS_ON",
            "from_node_id": "concept-permit",
            "to_node_id": "concept-variance",
            "assertion_id": "assert-rel-001",
            "confidence": 0.9,
        }
    )
    return snap


def _make_v1_snapshot() -> dict[str, object]:
    return {
        "nodes": [
            {
                "id": "source-001",
                "type": "source",
                "trust_level": "high",
                "last_updated_utc": "2026-01-01T00:00:00Z",
            }
        ],
        "edges": [
            {
                "evidence_id": "edge-001",
                "from_id": "source-001",
                "to_id": "concept-001",
                "type": "CITES",
                "status": "validated",
            }
        ],
        "node_count": 1,
        "edge_count": 1,
    }


class TestVersionDetection:
    def test_detects_v1(self) -> None:
        assert _detect_snapshot_version(_make_v1_snapshot()) == "v1"

    def test_detects_v2(self) -> None:
        snap = _make_v2_snapshot()
        assert _detect_snapshot_version(snap.to_dict()) == "v2"

    def test_detects_unknown(self) -> None:
        assert _detect_snapshot_version({"foo": "bar"}) == "unknown"


class TestV2Rendering:
    def test_generates_html(self, tmp_path: Path) -> None:
        snap = _make_v2_snapshot()
        snap_path = tmp_path / "kg_v2.json"
        snap.write(snap_path)

        html, out_path = generate_html(str(snap_path), str(tmp_path / "out.html"), version="v2")
        assert "KG v2 Viewer" in html
        assert "cytoscape" in html.lower()
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(html, encoding="utf-8")
        assert out_path.exists()

    def test_embeds_node_data(self, tmp_path: Path) -> None:
        snap = _make_v2_snapshot()
        snap_path = tmp_path / "kg_v2.json"
        snap.write(snap_path)

        html, _ = generate_html(str(snap_path), str(tmp_path / "out.html"), version="v2")
        assert "concept-permit" in html
        assert "Building Permit" in html
        assert "taxonomy-building-code" in html

    def test_embeds_edge_data(self, tmp_path: Path) -> None:
        snap = _make_v2_snapshot()
        snap_path = tmp_path / "kg_v2.json"
        snap.write(snap_path)

        html, _ = generate_html(str(snap_path), str(tmp_path / "out.html"), version="v2")
        assert "assert-rel-001" in html
        assert "DEPENDS_ON" in html
        assert "direct_citation" in html

    def test_embeds_evidence(self, tmp_path: Path) -> None:
        snap = _make_v2_snapshot()
        snap_path = tmp_path / "kg_v2.json"
        snap.write(snap_path)

        html, _ = generate_html(str(snap_path), str(tmp_path / "out.html"), version="v2")
        assert "span-001" in html
        assert "A building permit is required." in html

    def test_cli_runs(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        snap = _make_v2_snapshot()
        snap_path = tmp_path / "kg_v2.json"
        snap.write(snap_path)

        out_path = tmp_path / "viz.html"
        rc = run_visualize_graph(
            snapshot_path=str(snap_path),
            out_path=str(out_path),
            version="v2",
        )
        assert rc == 0
        assert out_path.exists()


class TestV1Rendering:
    def test_v1_still_works(self, tmp_path: Path) -> None:
        snap_path = tmp_path / "v1.json"
        snap_path.write_text(
            "{\"nodes\": [{\"id\": \"n1\", \"type\": \"concept\", \"trust_level\": \"high\", \"last_updated_utc\": \"2026-01-01\"}], "
            "\"edges\": [{\"evidence_id\": \"e1\", \"from_id\": \"n1\", \"to_id\": \"n2\", \"type\": \"CITES\", \"status\": \"validated\"}], "
            "\"node_count\": 1, \"edge_count\": 1}"
        )
        html, _ = generate_html(str(snap_path), str(tmp_path / "out.html"), version="v1")
        assert "Knowledge Graph Viewer" in html
        assert "n1" in html

    def test_auto_detects_v1(self, tmp_path: Path) -> None:
        snap_path = tmp_path / "v1.json"
        snap_path.write_text(
            "{\"nodes\": [{\"id\": \"n1\", \"type\": \"concept\", \"trust_level\": \"high\", \"last_updated_utc\": \"2026-01-01\"}], "
            "\"edges\": [{\"evidence_id\": \"e1\", \"from_id\": \"n1\", \"to_id\": \"n2\", \"type\": \"CITES\", \"status\": \"validated\"}], "
            "\"node_count\": 1, \"edge_count\": 1}"
        )
        html, _ = generate_html(str(snap_path), str(tmp_path / "out.html"), version="auto")
        assert "Knowledge Graph Viewer" in html

    def test_auto_detects_v2(self, tmp_path: Path) -> None:
        snap = _make_v2_snapshot()
        snap_path = tmp_path / "kg_v2.json"
        snap.write(snap_path)
        html, _ = generate_html(str(snap_path), str(tmp_path / "out.html"), version="auto")
        assert "KG v2 Viewer" in html
