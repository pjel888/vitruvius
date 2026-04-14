"""Phase 8 Task 7 — pipeline CLI build-graph / query-graph / export-graph-snapshot."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


CLI = Path(__file__).resolve().parent.parent / "pipeline_cli.py"
REPO_ROOT = CLI.resolve().parent.parent


def _run_cli(args: list[str], cwd: Path) -> subprocess.CompletedProcess:
    env = {**os.environ, "PYTHONPATH": "scripts"}
    return subprocess.run(
        [sys.executable, str(CLI), *args],
        capture_output=True,
        text=True,
        cwd=str(cwd),
        env=env,
    )


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _seed_canonical_tree(root: Path) -> None:
    shared = root / "003_Canonical-Knowledge-Layer" / "shared"
    _write(shared / "sources" / "pd-1096.md", (
        "---\n"
        "id: law-pd-1096\n"
        "trust_level: primary\n"
        "last_canonicalized_utc: 2026-04-01T00:00:00Z\n"
        "---\n\n# body\n"
    ))
    _write(shared / "concepts" / "building-permit.md", (
        "---\n"
        "id: concept-building-permit\n"
        "last_canonicalized_utc: 2026-04-01T00:00:00Z\n"
        "---\n\n# body\n"
    ))
    _write(shared / "relationships" / "r.md", (
        "---\n"
        "id: rel-pd-1096-governs-building-permit\n"
        "page_type: relationship\n"
        "relationship_type: governs\n"
        "from_entity: law-pd-1096\n"
        "to_entity: concept-building-permit\n"
        "canonical_status: promoted\n"
        "---\n\n# body\n"
    ))


def test_build_graph_dry_run_returns_zero(tmp_path: Path) -> None:
    _seed_canonical_tree(tmp_path)
    result = _run_cli(["build-graph", "--dry-run"], cwd=tmp_path)
    assert result.returncode == 0, f"stderr: {result.stderr}"
    out = result.stdout
    assert "integrity" in out.lower() or "passed" in out.lower() or "node_count" in out


def test_build_graph_writes_snapshot(tmp_path: Path) -> None:
    _seed_canonical_tree(tmp_path)
    result = _run_cli(["build-graph"], cwd=tmp_path)
    assert result.returncode == 0, f"stderr: {result.stderr}"
    out_path = tmp_path / "005_Operational-Intelligence-Layer" / "graph" / "latest_graph_snapshot.json"
    assert out_path.exists(), f"snapshot not written: stdout={result.stdout} stderr={result.stderr}"
    data = json.loads(out_path.read_text(encoding="utf-8"))
    assert data["node_count"] == 2
    assert data["edge_count"] == 1
    assert data["schema_version"] == "1.0.0"


def test_query_graph_returns_path(tmp_path: Path) -> None:
    _seed_canonical_tree(tmp_path)
    build_result = _run_cli(["build-graph"], cwd=tmp_path)
    assert build_result.returncode == 0, f"build failed: {build_result.stderr}"

    result = _run_cli(
        [
            "query-graph",
            "--from", "law-pd-1096",
            "--to", "concept-building-permit",
            "--max-depth", "3",
        ],
        cwd=tmp_path,
    )
    assert result.returncode == 0, f"stderr: {result.stderr}"
    assert "rel-pd-1096-governs-building-permit" in result.stdout


def test_export_graph_snapshot_outputs_json(tmp_path: Path) -> None:
    _seed_canonical_tree(tmp_path)
    build_result = _run_cli(["build-graph"], cwd=tmp_path)
    assert build_result.returncode == 0, f"build failed: {build_result.stderr}"

    result = _run_cli(["export-graph-snapshot", "--format", "json"], cwd=tmp_path)
    assert result.returncode == 0, f"stderr: {result.stderr}"
    data = json.loads(result.stdout)
    assert data["schema_version"] == "1.0.0"
    assert data["node_count"] == 2


def test_build_graph_help_is_lazy() -> None:
    """--help on any new command must not eager-import heavy deps."""
    env = {**os.environ, "PYTHONPATH": "scripts"}
    script = (
        "import sys;"
        "import importlib.util;"
        "spec = importlib.util.spec_from_file_location('pipeline_cli', r'" + str(CLI) + "');"
        "mod = importlib.util.module_from_spec(spec);"
        "spec.loader.exec_module(mod);"
        "forbidden = {'vitruvius.graph.builder', 'vitruvius.graph.snapshot', "
        "'vitruvius.graph.integrity', 'vitruvius.graph.traverse'};"
        "leaked = forbidden & set(sys.modules.keys());"
        "print('LEAKED:' + ','.join(sorted(leaked)) if leaked else 'CLEAN');"
    )
    result = subprocess.run(
        [sys.executable, "-c", script],
        capture_output=True,
        text=True,
        cwd=str(REPO_ROOT),
        env=env,
    )
    assert result.returncode == 0, f"subprocess failed: {result.stderr}"
    assert "CLEAN" in result.stdout, (
        f"CLI eagerly imported graph modules: {result.stdout}"
    )
