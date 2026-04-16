"""Phase 8 Task 5 — deterministic JSON snapshot writer."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from vitruvius.graph.contract import GraphEdge, GraphNode, GraphSnapshot
from vitruvius.graph.snapshot import read_snapshot, write_snapshot


def _snapshot() -> GraphSnapshot:
    nodes = [
        GraphNode(
            id="concept-building-permit",
            type="concept",
            slug="building-permit",
            trust_level="derived",
            last_updated_utc="2026-04-14T00:00:00Z",
        ),
        GraphNode(
            id="law-pd-1096",
            type="source",
            slug="pd-1096",
            trust_level="primary",
            last_updated_utc="2026-04-14T00:00:00Z",
        ),
    ]
    edges = [
        GraphEdge(
            from_id="law-pd-1096",
            to_id="concept-building-permit",
            type="governs",
            evidence_id="rel-pd-1096-governs-building-permit",
            status="verified",
        ),
    ]
    return GraphSnapshot(
        schema_version="1.0.0",
        generated_at_utc="2026-04-14T00:00:00Z",
        node_count=2,
        edge_count=1,
        nodes=nodes,
        edges=edges,
    )


def test_write_produces_expected_json_shape(tmp_path: Path) -> None:
    out = tmp_path / "snap.json"
    write_snapshot(_snapshot(), out)
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["schema_version"] == "1.0.0"
    assert payload["node_count"] == 2
    assert payload["edge_count"] == 1
    assert isinstance(payload["nodes"], list)
    assert isinstance(payload["edges"], list)
    assert payload["nodes"][0]["id"] == "concept-building-permit"
    assert payload["edges"][0]["evidence_id"] == "rel-pd-1096-governs-building-permit"


def test_write_is_byte_identical_on_repeat(tmp_path: Path) -> None:
    out_a = tmp_path / "a.json"
    out_b = tmp_path / "b.json"
    write_snapshot(_snapshot(), out_a)
    write_snapshot(_snapshot(), out_b)
    assert out_a.read_bytes() == out_b.read_bytes()


def test_round_trip_equals_original(tmp_path: Path) -> None:
    original = _snapshot()
    out = tmp_path / "snap.json"
    write_snapshot(original, out)
    loaded = read_snapshot(out)
    assert loaded == original


def test_round_trip_preserves_optional_metadata(tmp_path: Path) -> None:
    original = _snapshot()
    original.metadata = {
        "dataset_id": "laws-core-bundle-m1",
        "run_id": "20260416T000000Z",
        "manifest_hash": "abc123",
    }
    out = tmp_path / "snap.json"
    write_snapshot(original, out)
    loaded = read_snapshot(out)
    assert loaded == original


def test_read_missing_file_raises(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        read_snapshot(tmp_path / "nope.json")


def test_read_malformed_json_raises(tmp_path: Path) -> None:
    bad = tmp_path / "bad.json"
    bad.write_text("{not json", encoding="utf-8")
    with pytest.raises(json.JSONDecodeError):
        read_snapshot(bad)


def test_write_creates_parent_directory(tmp_path: Path) -> None:
    out = tmp_path / "nested" / "dir" / "snap.json"
    write_snapshot(_snapshot(), out)
    assert out.exists()
