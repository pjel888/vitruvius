from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

import pytest

from vitruvius.kg.backbone_rollback_preflight import (
    ADMIN_COMMANDS,
    CommandCapture,
    run_rollback_preflight,
)


def _successful_runner() -> Any:
    calls: list[tuple[str, tuple[str, ...]]] = []

    def run(name: str, argv: tuple[str, ...], cwd: Path, timeout_seconds: int) -> CommandCapture:
        del cwd
        del timeout_seconds
        calls.append((name, argv))
        stdout_by_name = {
            "neo4j_admin_version": "neo4j-admin 2026.03.1\n",
            "neo4j_version": "neo4j 2026.03.1\n",
            "database_dump_help": (
                "Dump a database into a single-file archive.\n"
                "It is not possible to dump a database that is mounted in a running Neo4j server.\n"
            ),
            "database_load_help": (
                "Load a database from an archive.\n"
                "It is not possible to replace a database that is mounted in a running Neo4j server.\n"
            ),
            "backup_help": "Usage: neo4j-admin backup [COMMAND]\nCommands:\n  help, -h, --help\n",
        }
        return CommandCapture(
            name=name,
            argv=argv,
            exit_code=0,
            duration_seconds=0.01,
            stdout=stdout_by_name.get(name, "Usage: neo4j-admin\n"),
        )

    run.calls = calls
    return run


def _graph_reader() -> dict[str, Any]:
    return {
        "connectivity": True,
        "node_count": 2429,
        "relationship_type_counts": [{"type": "DEFINED_BY", "count": 4}],
        "backbone_shadow_nodes": 0,
        "canonical_nodes": 313,
    }


def test_rollback_preflight_writes_blocking_report(tmp_path: Path) -> None:
    output_path = Path(
        "006_System-Manifests/aec-mepfs-backbone/rollback/TEST_RUN"
    ) / "rollback-preflight-report.json"
    runner = _successful_runner()

    report = run_rollback_preflight(
        repo_root=tmp_path,
        run_id="TEST_RUN",
        output_path=output_path,
        command_runner=runner,
        graph_reader=_graph_reader,
    )

    saved = json.loads((tmp_path / output_path).read_text(encoding="utf-8"))
    assert saved == report
    assert report["ok"] is True
    assert report["runtime_ready"] is False
    assert report["destructive_operations_executed"] is False
    assert report["backup_dump_load_executed"] is False
    assert report["proof_status"] == "blocked_runtime_stopped_or_isolated_database_required"
    assert report["admin_capabilities"]["database_dump_available"] is True
    assert report["admin_capabilities"]["database_load_available"] is True
    assert report["admin_capabilities"]["online_backup_command_available"] is False
    assert report["admin_capabilities"]["dump_requires_unmounted_database"] is True
    assert report["live_graph"]["node_count"] == 2429
    assert runner.calls == list(ADMIN_COMMANDS)


def test_rollback_preflight_rejects_unsafe_run_id(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="run_id must contain only"):
        run_rollback_preflight(
            repo_root=tmp_path,
            run_id="../unsafe",
            command_runner=_successful_runner(),
            graph_reader=_graph_reader,
        )


def test_rollback_preflight_rejects_output_outside_rollback_root(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="rollback report directory"):
        run_rollback_preflight(
            repo_root=tmp_path,
            run_id="TEST_RUN",
            output_path=Path(".ai/ACTIVE_WORK.md"),
            command_runner=_successful_runner(),
            graph_reader=_graph_reader,
        )


def test_rollback_preflight_requires_run_scoped_output(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="current rollback run id"):
        run_rollback_preflight(
            repo_root=tmp_path,
            run_id="TEST_RUN",
            output_path=Path(
                "006_System-Manifests/aec-mepfs-backbone/rollback/OTHER_RUN"
            ) / "rollback-preflight-report.json",
            command_runner=_successful_runner(),
            graph_reader=_graph_reader,
        )


def test_rollback_preflight_preserves_report_when_command_fails(tmp_path: Path) -> None:
    output_path = Path(
        "006_System-Manifests/aec-mepfs-backbone/rollback/TEST_RUN"
    ) / "rollback-preflight-report.json"

    def failing_runner(
        name: str,
        argv: tuple[str, ...],
        cwd: Path,
        timeout_seconds: int,
    ) -> CommandCapture:
        del cwd
        del timeout_seconds
        return CommandCapture(
            name=name,
            argv=argv,
            exit_code=127 if name == "database_dump_help" else 0,
            duration_seconds=0.01,
            stderr="missing command" if name == "database_dump_help" else "",
        )

    report = run_rollback_preflight(
        repo_root=tmp_path,
        run_id="TEST_RUN",
        output_path=output_path,
        command_runner=failing_runner,
        graph_reader=_graph_reader,
    )

    saved = json.loads((tmp_path / output_path).read_text(encoding="utf-8"))
    assert saved == report
    assert report["ok"] is False
    assert "database_dump_help: command failed with exit 127" in report["errors"]
    assert report["proof_status"] == "blocked_no_dump_command"


def test_rollback_preflight_preserves_report_when_graph_smoke_fails(tmp_path: Path) -> None:
    output_path = Path(
        "006_System-Manifests/aec-mepfs-backbone/rollback/TEST_RUN"
    ) / "rollback-preflight-report.json"

    def broken_graph_reader() -> dict[str, Any]:
        raise RuntimeError("neo4j unavailable")

    report = run_rollback_preflight(
        repo_root=tmp_path,
        run_id="TEST_RUN",
        output_path=output_path,
        command_runner=_successful_runner(),
        graph_reader=broken_graph_reader,
    )

    assert report["ok"] is True
    assert report["live_graph"]["connectivity"] is False
    assert any("live graph smoke failed" in warning for warning in report["warnings"])


def test_rollback_preflight_command_timeout_is_recorded(tmp_path: Path) -> None:
    output_path = Path(
        "006_System-Manifests/aec-mepfs-backbone/rollback/TEST_RUN"
    ) / "rollback-preflight-report.json"

    def timeout_runner(
        name: str,
        argv: tuple[str, ...],
        cwd: Path,
        timeout_seconds: int,
    ) -> CommandCapture:
        del cwd
        if name == "neo4j_admin_version":
            exc = subprocess.TimeoutExpired(
                cmd=list(argv),
                timeout=timeout_seconds,
                output="partial",
                stderr="timed out",
            )
            return CommandCapture(
                name=name,
                argv=argv,
                exit_code=124,
                duration_seconds=0.01,
                stdout=str(exc.output),
                stderr=str(exc.stderr),
            )
        return CommandCapture(name=name, argv=argv, exit_code=0, duration_seconds=0.01)

    report = run_rollback_preflight(
        repo_root=tmp_path,
        run_id="TEST_RUN",
        output_path=output_path,
        command_runner=timeout_runner,
        graph_reader=_graph_reader,
    )

    assert report["ok"] is False
    assert "neo4j_admin_version: command failed with exit 124" in report["errors"]
