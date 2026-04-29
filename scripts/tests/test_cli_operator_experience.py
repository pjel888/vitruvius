from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

from vitruvius.cli_experience import (
    execute_with_cli_experience,
    resolve_output_mode,
)


CLI = Path(__file__).resolve().parent.parent / "pipeline_cli.py"
REPO_ROOT = CLI.resolve().parent.parent


def _run_cli(args: list[str]) -> subprocess.CompletedProcess:
    env = {**os.environ, "PYTHONPATH": "scripts"}
    return subprocess.run(
        [sys.executable, str(CLI), *args],
        capture_output=True,
        text=True,
        cwd=str(REPO_ROOT),
        env=env,
    )


def test_refine_help_contains_dual_layer_sections() -> None:
    result = _run_cli(["refine", "--help"])
    assert result.returncode == 0, result.stderr
    assert "Human explanation:" in result.stdout
    assert "Technical explanation:" in result.stdout
    assert "Success means:" in result.stdout
    assert "Suggested next step:" in result.stdout


def test_source_evidence_commands_are_framed_as_compatibility_paths() -> None:
    result = _run_cli(["run-with-review", "--help"])
    assert result.returncode == 0, result.stderr
    assert "source-evidence compatibility path" in result.stdout
    assert "not the primary AEC-MEPFS taxonomy authoring path" in result.stdout


def test_kg_pipeline_help_warns_against_cleanup_or_cutover_use() -> None:
    result = _run_cli(["run-kg-pipeline", "--help"])
    assert result.returncode == 0, result.stderr
    assert "source-derived KG snapshot compatibility path" in result.stdout
    assert "not a KG-first cleanup, Explorer cutover, or production graph promotion command" in result.stdout


def test_canonicalize_help_preserves_source_artifact_role() -> None:
    result = _run_cli(["canonicalize-one", "--help"])
    assert result.returncode == 0, result.stderr
    assert "trusted source-evidence artifact" in result.stdout
    assert "not a replacement for the authored AEC-MEPFS backbone" in result.stdout


def test_operator_wrapper_prints_pre_and_post_blocks(capsys) -> None:
    rc = execute_with_cli_experience(
        "refine",
        output_mode="operator",
        handler=lambda: 0,
    )
    out = capsys.readouterr().out
    assert rc == 0
    assert "Command: refine" in out
    assert "Human explanation:" in out
    assert "Result summary: success" in out


def test_auto_mode_stays_concise_for_structured_commands(monkeypatch) -> None:
    monkeypatch.setattr(sys.stdout, "isatty", lambda: True)
    assert resolve_output_mode("auto", "build-graph") == "concise"
