"""Rollback preflight report for AEC-MEPFS Backbone readiness.

This runner is intentionally read-only. It records the local Neo4j admin
surface and live graph smoke counts needed before a later stopped/isolated
dump-load rehearsal. It does not run backup, dump, load, restore, cleanup,
reset, graph rebuild, or any Cypher write.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Callable, Sequence


REPORT_SCHEMA_VERSION = "aec-bb-rollback-preflight/v1"
ROLLBACK_REPORT_ROOT = Path("006_System-Manifests/aec-mepfs-backbone/rollback")
ROLLBACK_REPORT_FILENAME = "rollback-preflight-report.json"
RUN_ID_RE = re.compile(r"^[A-Za-z0-9_.-]+$")
OUTPUT_SNIPPET_CHARS = 4000


@dataclass(frozen=True)
class CommandCapture:
    """Captured shell-free command result."""

    name: str
    argv: tuple[str, ...]
    exit_code: int
    duration_seconds: float
    stdout: str = ""
    stderr: str = ""

    @property
    def passed(self) -> bool:
        return self.exit_code == 0


CommandRunner = Callable[[str, tuple[str, ...], Path, int], CommandCapture]
GraphReader = Callable[[], dict[str, Any]]


ADMIN_COMMANDS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("neo4j_admin_version", ("neo4j-admin", "--version")),
    ("neo4j_version", ("neo4j", "version")),
    ("neo4j_admin_help", ("neo4j-admin", "--help")),
    ("database_dump_help", ("neo4j-admin", "database", "dump", "--help")),
    ("database_load_help", ("neo4j-admin", "database", "load", "--help")),
    ("backup_help", ("neo4j-admin", "backup", "--help")),
)

READ_ONLY_SMOKE_QUERIES = {
    "node_count": "MATCH (n) RETURN count(n) AS count",
    "relationship_type_counts": (
        "MATCH ()-[r]->() "
        "RETURN type(r) AS type, count(*) AS count ORDER BY count DESC"
    ),
    "backbone_shadow_nodes": (
        'MATCH (n) WHERE "BackboneShadow" IN labels(n) RETURN count(n) AS count'
    ),
    "canonical_nodes": (
        'MATCH (n) WHERE "CanonicalNode" IN labels(n) RETURN count(n) AS count'
    ),
}


def run_rollback_preflight(
    *,
    repo_root: str | Path | None = None,
    run_id: str | None = None,
    output_path: str | Path | None = None,
    timeout_seconds: int = 60,
    command_runner: CommandRunner | None = None,
    graph_reader: GraphReader | None = None,
) -> dict[str, Any]:
    """Run read-only rollback preflight checks and write a JSON report."""
    root = _repo_root(repo_root)
    resolved_run_id = _run_id(run_id)
    report_path = _resolve_report_path(
        root=root,
        run_id=resolved_run_id,
        output_path=Path(output_path) if output_path is not None else None,
    )
    runner = command_runner or _run_command

    started_at = _utc_now()
    commands = [
        _command_to_dict(runner(name, argv, root, timeout_seconds))
        for name, argv in ADMIN_COMMANDS
    ]
    errors: list[str] = []
    warnings: list[str] = []

    for command in commands:
        if not command["passed"]:
            errors.append(f"{command['name']}: command failed with exit {command['exit_code']}")

    admin_capabilities = _admin_capabilities(commands)

    live_graph = _read_graph_safely(graph_reader or _read_live_graph_counts, warnings)
    proof_status = _proof_status(admin_capabilities)
    if proof_status != "executed":
        warnings.append(
            "rollback proof is not executed; a stopped or isolated database "
            "dump/load rehearsal is still required"
        )

    finished_at = _utc_now()
    report = {
        "schema_version": REPORT_SCHEMA_VERSION,
        "ok": not errors,
        "run_id": resolved_run_id,
        "started_at_utc": started_at,
        "finished_at_utc": finished_at,
        "report_path": _relative_to_root(report_path, root),
        "proof_status": proof_status,
        "runtime_ready": False,
        "destructive_operations_executed": False,
        "backup_dump_load_executed": False,
        "required_next_action": (
            "Run a stopped or isolated Neo4j database dump/load rehearsal "
            "before any graph mutation or cleanup."
        ),
        "admin_capabilities": admin_capabilities,
        "read_only_smoke_queries": READ_ONLY_SMOKE_QUERIES,
        "live_graph": live_graph,
        "errors": sorted(set(errors)),
        "warnings": sorted(set(warnings)),
        "commands": commands,
    }
    _write_json(report_path, report)
    return report


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run AEC-MEPFS Backbone rollback preflight checks."
    )
    parser.add_argument("--repo-root", default=None)
    parser.add_argument("--run-id", default=None)
    parser.add_argument("--output", default=None)
    parser.add_argument("--timeout-seconds", type=int, default=60)
    args = parser.parse_args(argv)

    try:
        report = run_rollback_preflight(
            repo_root=args.repo_root,
            run_id=args.run_id,
            output_path=args.output,
            timeout_seconds=args.timeout_seconds,
        )
    except ValueError as exc:
        print(json.dumps({"ok": False, "errors": [str(exc)]}, indent=2, sort_keys=True))
        return 1

    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["ok"] else 1


def _run_command(
    name: str,
    argv: tuple[str, ...],
    cwd: Path,
    timeout_seconds: int,
) -> CommandCapture:
    started = time.monotonic()
    try:
        completed = subprocess.run(
            list(argv),
            cwd=cwd,
            text=True,
            capture_output=True,
            timeout=timeout_seconds,
            check=False,
        )
        return CommandCapture(
            name=name,
            argv=argv,
            exit_code=completed.returncode,
            duration_seconds=round(time.monotonic() - started, 4),
            stdout=completed.stdout,
            stderr=completed.stderr,
        )
    except FileNotFoundError as exc:
        return CommandCapture(
            name=name,
            argv=argv,
            exit_code=127,
            duration_seconds=round(time.monotonic() - started, 4),
            stderr=str(exc),
        )
    except subprocess.TimeoutExpired as exc:
        return CommandCapture(
            name=name,
            argv=argv,
            exit_code=124,
            duration_seconds=round(time.monotonic() - started, 4),
            stdout=_exception_output(exc.stdout),
            stderr=_exception_output(exc.stderr)
            or f"command timed out after {timeout_seconds} seconds",
        )


def _read_live_graph_counts() -> dict[str, Any]:
    from vitruvius.config import (
        get_kg_neo4j_password,
        get_kg_neo4j_uri,
        get_kg_neo4j_user,
    )
    from vitruvius.kg.neo4j_client import Neo4jClient

    client = Neo4jClient(
        uri=get_kg_neo4j_uri(),
        user=get_kg_neo4j_user(),
        password=get_kg_neo4j_password(),
    )
    try:
        connected = client.verify_connectivity()
        if not connected:
            return {"connectivity": False}
        return {
            "connectivity": True,
            "node_count": _first_count(
                client.run(READ_ONLY_SMOKE_QUERIES["node_count"])
            ),
            "relationship_type_counts": client.run(
                READ_ONLY_SMOKE_QUERIES["relationship_type_counts"]
            ),
            "backbone_shadow_nodes": _first_count(
                client.run(READ_ONLY_SMOKE_QUERIES["backbone_shadow_nodes"])
            ),
            "canonical_nodes": _first_count(
                client.run(READ_ONLY_SMOKE_QUERIES["canonical_nodes"])
            ),
        }
    finally:
        client.close()


def _read_graph_safely(reader: GraphReader, warnings: list[str]) -> dict[str, Any]:
    try:
        result = reader()
    except Exception as exc:
        warnings.append(f"live graph smoke failed: {type(exc).__name__}: {exc}")
        return {"connectivity": False, "error": f"{type(exc).__name__}: {exc}"}
    if not isinstance(result, dict):
        warnings.append("live graph smoke returned a non-object result")
        return {"connectivity": False, "error": "non-object graph result"}
    return result


def _admin_capabilities(commands: list[dict[str, Any]]) -> dict[str, Any]:
    by_name = {command["name"]: command for command in commands}
    dump_help = _combined_output(by_name.get("database_dump_help"))
    load_help = _combined_output(by_name.get("database_load_help"))
    backup_help = _combined_output(by_name.get("backup_help"))

    return {
        "neo4j_admin_available": bool(by_name.get("neo4j_admin_help", {}).get("passed")),
        "neo4j_admin_version": _first_nonempty_line(
            _combined_output(by_name.get("neo4j_admin_version"))
        ),
        "neo4j_version": _first_nonempty_line(_combined_output(by_name.get("neo4j_version"))),
        "database_dump_available": bool(by_name.get("database_dump_help", {}).get("passed")),
        "database_load_available": bool(by_name.get("database_load_help", {}).get("passed")),
        "backup_help_available": bool(by_name.get("backup_help", {}).get("passed")),
        "online_backup_command_available": _has_online_backup_subcommand(backup_help),
        "dump_requires_unmounted_database": _contains_phrase(
            dump_help,
            "not possible to dump a database that is mounted",
        ),
        "load_requires_unmounted_database": _contains_phrase(
            load_help,
            "not possible to replace a database that is mounted",
        ),
    }


def _proof_status(admin_capabilities: dict[str, Any]) -> str:
    if not admin_capabilities.get("database_dump_available"):
        return "blocked_no_dump_command"
    if not admin_capabilities.get("database_load_available"):
        return "blocked_no_load_command"
    if admin_capabilities.get("online_backup_command_available"):
        return "blocked_runtime_online_backup_rehearsal_required"
    return "blocked_runtime_stopped_or_isolated_database_required"


def _has_online_backup_subcommand(help_text: str) -> bool:
    lowered = help_text.lower()
    return "database backup" in lowered or "backup a database" in lowered


def _command_to_dict(result: CommandCapture) -> dict[str, Any]:
    return {
        "name": result.name,
        "argv": list(result.argv),
        "exit_code": result.exit_code,
        "passed": result.passed,
        "duration_seconds": result.duration_seconds,
        "stdout_tail": _tail(result.stdout),
        "stderr_tail": _tail(result.stderr),
    }


def _repo_root(value: str | Path | None) -> Path:
    if value is not None:
        return Path(value).resolve()
    return Path(__file__).resolve().parents[3]


def _resolve_report_path(
    *,
    root: Path,
    run_id: str,
    output_path: Path | None,
) -> Path:
    candidate = output_path or ROLLBACK_REPORT_ROOT / run_id / ROLLBACK_REPORT_FILENAME
    report_path = candidate.resolve() if candidate.is_absolute() else (root / candidate).resolve()
    allowed_root = (root / ROLLBACK_REPORT_ROOT).resolve()
    try:
        relative_parts = report_path.relative_to(allowed_root).parts
    except ValueError as exc:
        raise ValueError("report path must stay inside the rollback report directory") from exc
    if len(relative_parts) != 2 or relative_parts[0] != run_id:
        raise ValueError("report path must be scoped to the current rollback run id")
    if relative_parts[1] != ROLLBACK_REPORT_FILENAME:
        raise ValueError(f"report filename must be {ROLLBACK_REPORT_FILENAME}")
    return report_path


def _run_id(value: str | None) -> str:
    candidate = value or datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    if not RUN_ID_RE.fullmatch(candidate):
        raise ValueError("run_id must contain only letters, digits, underscore, dot, or dash")
    return candidate


def _utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _first_count(rows: list[dict[str, Any]]) -> int:
    if not rows:
        return 0
    value = rows[0].get("count", 0)
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def _combined_output(command: dict[str, Any] | None) -> str:
    if not command:
        return ""
    return f"{command.get('stdout_tail', '')}\n{command.get('stderr_tail', '')}"


def _first_nonempty_line(value: str) -> str:
    for line in value.splitlines():
        if line.strip():
            return line.strip()
    return ""


def _contains_phrase(value: str, phrase: str) -> bool:
    normalized_value = " ".join(value.lower().split())
    normalized_phrase = " ".join(phrase.lower().split())
    return normalized_phrase in normalized_value


def _exception_output(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode(errors="replace")
    return str(value)


def _tail(value: str) -> str:
    if len(value) <= OUTPUT_SNIPPET_CHARS:
        return value
    return value[-OUTPUT_SNIPPET_CHARS:]


def _relative_to_root(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
