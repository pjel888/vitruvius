from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


CLI = Path(__file__).resolve().parent.parent / "pipeline_cli.py"


def _run_cli(args: list[str], cwd: Path) -> subprocess.CompletedProcess:
    env = {**os.environ, "PYTHONPATH": "scripts"}
    return subprocess.run(
        [sys.executable, str(CLI), *args],
        capture_output=True,
        text=True,
        cwd=str(cwd),
        env=env,
    )


def _write_snapshot(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema_version": "1.0.0",
        "generated_at_utc": "2026-04-16T00:00:00Z",
        "node_count": 2,
        "edge_count": 1,
        "nodes": [
            {
                "id": "law-pd-1096",
                "type": "source",
                "slug": "pd-1096",
                "trust_level": "primary",
                "last_updated_utc": "2026-04-01T00:00:00Z",
            },
            {
                "id": "concept-building-permit",
                "type": "concept",
                "slug": "building-permit",
                "trust_level": "derived",
                "last_updated_utc": "2026-04-01T00:00:00Z",
            },
        ],
        "edges": [
            {
                "from_id": "law-pd-1096",
                "to_id": "concept-building-permit",
                "type": "governs",
                "evidence_id": "rel-pd-1096-governs-building-permit",
                "status": "verified",
                "evidence_source_id": "law-pd-1096",
                "evidence_source_section_id": "sec-301",
            }
        ],
        "metadata": {
            "dataset_id": "demo-dataset",
            "run_id": "20260416T000000Z",
            "contributing_law_ids": ["pd-1096"],
        },
    }
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def test_visualize_graph_writes_dataset_html_artifact(tmp_path: Path) -> None:
    snapshot_path = (
        tmp_path
        / "005_Operational-Intelligence-Layer"
        / "graph"
        / "datasets"
        / "demo-dataset"
        / "20260416T000000Z_graph_snapshot.json"
    )
    _write_snapshot(snapshot_path)

    result = _run_cli(["visualize-graph", "--snapshot", str(snapshot_path)], cwd=tmp_path)
    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    out_path = tmp_path / payload["out_path"]
    assert out_path.exists()
    html = out_path.read_text(encoding="utf-8")
    assert "cytoscape.min.js" in html
    assert "demo-dataset" in html
    assert "20260416T000000Z" in html
    assert "concept-building-permit" in html


def test_visualize_graph_missing_snapshot_returns_2(tmp_path: Path) -> None:
    result = _run_cli(["visualize-graph", "--snapshot", "missing.json"], cwd=tmp_path)
    assert result.returncode == 2
    assert "no snapshot found" in result.stdout
