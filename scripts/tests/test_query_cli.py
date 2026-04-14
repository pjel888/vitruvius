"""Phase 9 Task 6 — query + query-structured CLI commands."""

from __future__ import annotations

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


def test_query_requires_snapshot(tmp_path: Path) -> None:
    # No snapshot built yet — expect graceful failure.
    result = _run_cli(["query", "What governs building permit?"], cwd=tmp_path)
    assert result.returncode == 1
    assert "no snapshot" in result.stdout.lower()


def test_query_structured_against_fresh_snapshot(tmp_path: Path) -> None:
    _seed_canonical_tree(tmp_path)
    build = _run_cli(["build-graph"], cwd=tmp_path)
    assert build.returncode == 0, f"build failed: {build.stderr}"

    result = _run_cli(
        [
            "query-structured",
            "--function", "what_governs",
            "--subject", "concept-building-permit",
        ],
        cwd=tmp_path,
    )
    assert result.returncode == 0, f"stderr: {result.stderr}"
    assert "what_governs" in result.stdout
    assert "law-pd-1096" in result.stdout


def test_query_nl_against_fresh_snapshot(tmp_path: Path) -> None:
    _seed_canonical_tree(tmp_path)
    build = _run_cli(["build-graph"], cwd=tmp_path)
    assert build.returncode == 0, f"build failed: {build.stderr}"

    result = _run_cli(
        ["query", "What governs building permit?"],
        cwd=tmp_path,
    )
    assert result.returncode == 0, f"stderr: {result.stderr}"
    assert "law-pd-1096" in result.stdout
    assert "what_governs" in result.stdout


def test_query_cli_help_is_lazy() -> None:
    """pipeline_cli.py must not eagerly import query modules."""
    env = {**os.environ, "PYTHONPATH": "scripts"}
    script = (
        "import sys;"
        "import importlib.util;"
        "spec = importlib.util.spec_from_file_location('pipeline_cli', r'" + str(CLI) + "');"
        "mod = importlib.util.module_from_spec(spec);"
        "spec.loader.exec_module(mod);"
        "forbidden = {'vitruvius.query.cli', 'vitruvius.query.engine', "
        "'vitruvius.query.nl_translator', 'vitruvius.query.cli_formatter'};"
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
        f"CLI eagerly imported query modules: {result.stdout}"
    )
