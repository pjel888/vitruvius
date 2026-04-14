"""Stream L.7 — CLI integration tests for ingest-spatial + evaluate-spatial."""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

z3 = pytest.importorskip("z3")


SCRIPTS_DIR = Path(__file__).resolve().parent.parent
CLI = SCRIPTS_DIR / "pipeline_cli.py"
REPO_ROOT = SCRIPTS_DIR.parent


def _run_cli(
    args: list[str], cwd: Path, config_path: Path | None = None
) -> subprocess.CompletedProcess:
    env = {**os.environ, "PYTHONPATH": str(SCRIPTS_DIR)}
    if config_path is not None:
        env["VITRUVIUS_CONFIG"] = str(config_path)
    return subprocess.run(
        [sys.executable, str(CLI), *args],
        capture_output=True,
        text=True,
        cwd=str(cwd),
        env=env,
    )


def _seed_spatial_tree(root: Path) -> None:
    spatial = root / "001B_Spatial-Source-Layer"
    spatial.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema_version": "1.0.0",
        "spatial_context_id": "spatial-test-01",
        "generated_at_utc": "2026-04-15T09:00:00Z",
        "instances": [
            {
                "instance_id": "instance-corridor-01",
                "canonical_concept_id": "concept-means-of-egress",
            },
            {
                "instance_id": "instance-door-01",
                "canonical_concept_id": "concept-doors-and-exits",
            },
        ],
        "spatial_edges": [
            {
                "source_instance": "instance-corridor-01",
                "predicate": "spatial_clearance",
                "target_instance": "instance-door-01",
                "value": 1.1,
                "unit": "meters",
            }
        ],
    }
    (spatial / "sample.json").write_text(json.dumps(payload), encoding="utf-8")


def _write_config(path: Path, *, ingestion_on: bool, solver_on: bool) -> None:
    path.write_text(
        "project_name: Vitruvius\n"
        "features:\n"
        f"  l_spatial_ingestion: {'true' if ingestion_on else 'false'}\n"
        f"  l_z3_constraint_solver: {'true' if solver_on else 'false'}\n",
        encoding="utf-8",
    )


def test_ingest_spatial_flag_off_prints_disabled_and_exits_zero(tmp_path: Path) -> None:
    _seed_spatial_tree(tmp_path)
    cfg = tmp_path / "vitruvius.yaml"
    _write_config(cfg, ingestion_on=False, solver_on=False)
    result = _run_cli(["ingest-spatial"], cwd=tmp_path, config_path=cfg)
    assert result.returncode == 0, f"stderr: {result.stderr}"
    assert "feature disabled" in result.stdout.lower()
    assert "l_spatial_ingestion" in result.stdout


def test_ingest_spatial_flag_on_summary(tmp_path: Path) -> None:
    _seed_spatial_tree(tmp_path)
    cfg = tmp_path / "vitruvius.yaml"
    _write_config(cfg, ingestion_on=True, solver_on=False)
    result = _run_cli(["ingest-spatial"], cwd=tmp_path, config_path=cfg)
    assert result.returncode == 0, f"stderr: {result.stderr}"
    out = json.loads(result.stdout)
    assert out["files_processed"] == 1
    assert out["instance_count"] == 2
    assert out["edge_count"] == 1
    assert out["skipped_count"] == 0


def test_evaluate_spatial_flag_off_prints_disabled(tmp_path: Path) -> None:
    cfg = tmp_path / "vitruvius.yaml"
    _write_config(cfg, ingestion_on=False, solver_on=False)
    obs = tmp_path / "obs.json"
    obs.write_text(json.dumps({"setback_meters": 3.0}), encoding="utf-8")
    result = _run_cli(
        [
            "evaluate-spatial",
            "--concepts",
            "concept-setback",
            "--observations",
            str(obs),
        ],
        cwd=tmp_path,
        config_path=cfg,
    )
    assert result.returncode == 0, f"stderr: {result.stderr}"
    assert "feature disabled" in result.stdout.lower()
    assert "l_z3_constraint_solver" in result.stdout


def test_evaluate_spatial_happy_path(tmp_path: Path) -> None:
    cfg = tmp_path / "vitruvius.yaml"
    _write_config(cfg, ingestion_on=True, solver_on=True)

    rules_dir = tmp_path / "005_Operational-Intelligence-Layer" / "spatial"
    rules_dir.mkdir(parents=True)
    rules = {
        "concept-setback": {
            "variable": "setback_meters",
            "operator": ">=",
            "threshold": 2.0,
        }
    }
    rules_file = rules_dir / "constraints.json"
    rules_file.write_text(json.dumps(rules), encoding="utf-8")

    obs = tmp_path / "obs.json"
    obs.write_text(json.dumps({"setback_meters": 3.0}), encoding="utf-8")

    result = _run_cli(
        [
            "evaluate-spatial",
            "--concepts",
            "concept-setback",
            "--observations",
            str(obs),
            "--rules",
            str(rules_file),
        ],
        cwd=tmp_path,
        config_path=cfg,
    )
    assert result.returncode == 0, f"stderr: {result.stderr}"
    out = json.loads(result.stdout)
    assert out["evaluated"] == 1
    assert out["passed"] == 1
    assert out["failed"] == 0
    assert out["results"][0]["concept_id"] == "concept-setback"
    assert out["results"][0]["passed"] is True
