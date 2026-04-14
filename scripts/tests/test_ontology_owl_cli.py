"""Stream M.4 — ``export-graph-owl`` CLI handler tests."""
from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

pytest.importorskip("rdflib")

from vitruvius.ontology.cli import run_export_graph_owl


def _write_snapshot(snap_path: Path, *, nodes: list[dict], edges: list[dict]) -> None:
    snap_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema_version": "1.0.0",
        "generated_at_utc": "2026-04-15T00:00:00Z",
        "node_count": len(nodes),
        "edge_count": len(edges),
        "nodes": nodes,
        "edges": edges,
    }
    snap_path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def test_export_graph_owl_returns_2_when_snapshot_missing(
    monkeypatch, tmp_path: Path, capsys
) -> None:
    monkeypatch.chdir(tmp_path)
    rc = run_export_graph_owl()
    assert rc == 2
    out = capsys.readouterr().out
    assert "no snapshot found" in out


def test_export_graph_owl_writes_turtle_and_prints_to_stdout(
    monkeypatch, tmp_path: Path, capsys
) -> None:
    monkeypatch.chdir(tmp_path)
    snap_path = tmp_path / "005_Operational-Intelligence-Layer" / "graph" / "latest_graph_snapshot.json"
    _write_snapshot(
        snap_path,
        nodes=[
            {
                "id": "law-pd-1096",
                "type": "source",
                "slug": "pd-1096",
                "trust_level": "primary",
                "last_updated_utc": "2026-04-01T00:00:00Z",
            },
            {
                "id": "concept-doors-and-exits",
                "type": "concept",
                "slug": "doors-and-exits",
                "trust_level": "derived",
                "last_updated_utc": "2026-04-01T00:00:00Z",
            },
        ],
        edges=[
            {
                "from_id": "law-pd-1096",
                "to_id": "concept-doors-and-exits",
                "type": "governs",
                "evidence_id": "rel-pd-1096-governs-doors-and-exits",
                "status": "verified",
            }
        ],
    )

    rc = run_export_graph_owl()
    assert rc == 0

    out = capsys.readouterr().out
    assert "@prefix" in out
    assert "concept-doors-and-exits" in out

    ttl_path = tmp_path / "005_Operational-Intelligence-Layer" / "graph" / "latest_graph_snapshot.ttl"
    assert ttl_path.exists()
    assert "@prefix" in ttl_path.read_text(encoding="utf-8")
