"""Report-producing parity runner for AEC-MEPFS Backbone readiness.

This runner is intentionally file-backed and runtime-disconnected. It executes
the parity commands declared by the readiness fixture and writes an auditable
JSON report, but it does not change KG schemas, Neo4j, API routes, Explorer
routes, feature flags, or canonical source content.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Callable, Sequence

from vitruvius.kg.backbone_contracts import validate_backbone_contract_file


REPORT_SCHEMA_VERSION = "aec-bb-parity-report/v1"
PARITY_CASES_SCHEMA_VERSION = "aec-bb-api-explorer-parity-cases/v1"
DEFAULT_FIXTURE_PATH = Path(
    "scripts/tests/fixtures/aec_mepfs_backbone/valid_integration_readiness_s3.json"
)
PARITY_REPORT_ROOT = Path("006_System-Manifests/aec-mepfs-backbone/parity")
PARITY_REPORT_FILENAME = "api-explorer-parity-report.json"
RUN_ID_RE = re.compile(r"^[A-Za-z0-9_.-]+$")
OUTPUT_SNIPPET_CHARS = 4000
REQUIRED_PARITY_CASE_CATEGORIES = {
    "direct_legacy_id_lookup",
    "direct_vtn_id_lookup",
    "edge_provenance_display",
    "empty_no_match_result",
    "invalid_node_id",
    "perspective_concepts_load",
    "perspective_default_load",
    "perspective_evidence_load",
    "perspective_regulatory_load",
    "perspective_taxonomy_load",
    "search_alias_deprecated_label",
    "search_invalid_query",
    "search_known_concept_label",
    "shadow_backbone_contract_validation",
    "shadow_backbone_evidence_preview",
    "shadow_backbone_placement_qa_preview",
    "shadow_backbone_summary_route",
    "shadow_backbone_taxonomy_graph_preview",
    "shadow_evidence_preview_opt_in_isolation",
    "shadow_graph_fail_closed",
    "shadow_graph_file_artifact",
    "shadow_placement_qa_preview_opt_in_isolation",
    "shadow_preview_opt_in_isolation",
    "source_evidence_display",
    "source_invalid_id",
    "taxonomy_navigation_root",
    "resolver_default_off_absent",
    "resolver_default_off_enabled",
    "resolver_trace_default_off",
}
PARITY_CASE_REQUIRED_FIELDS = {
    "assertions",
    "case_id",
    "covered_by_command",
    "expected_status",
    "method",
    "owner",
    "parity_category",
    "request",
    "review_status",
    "route",
    "surface",
}


@dataclass(frozen=True)
class CommandExecution:
    """Captured command execution result."""

    command: str
    exit_code: int
    duration_seconds: float
    stdout: str = ""
    stderr: str = ""

    @property
    def passed(self) -> bool:
        return self.exit_code == 0


CommandExecutor = Callable[[str, Path, int], CommandExecution]


@dataclass(frozen=True)
class AllowedCommand:
    """Shell-free command mapping for a declared parity command."""

    argv: tuple[str, ...]
    cwd_parts: tuple[str, ...] = ()
    env: dict[str, str] | None = None


ALLOWED_PARITY_COMMANDS = {
    "PYTHONPATH=scripts python3 -m pytest scripts/tests/test_kg_backbone_contracts.py -q": (
        AllowedCommand(
            argv=(
                "python3",
                "-m",
                "pytest",
                "scripts/tests/test_kg_backbone_contracts.py",
                "-q",
            ),
            env={"PYTHONPATH": "scripts"},
        )
    ),
    (
        "PYTHONPATH=scripts python3 -m pytest "
        "scripts/tests/test_kg_backbone_shadow_staging.py "
        "scripts/tests/test_kg_backbone_shadow_report_reader.py -q"
    ): AllowedCommand(
        argv=(
            "python3",
            "-m",
            "pytest",
            "scripts/tests/test_kg_backbone_shadow_staging.py",
            "scripts/tests/test_kg_backbone_shadow_report_reader.py",
            "-q",
        ),
        env={"PYTHONPATH": "scripts"},
    ),
    "(cd api && bun test perspectiveContracts.test.ts)": AllowedCommand(
        argv=("bun", "test", "perspectiveContracts.test.ts"),
        cwd_parts=("api",),
    ),
    "(cd api && bun test v2Backbone.test.ts)": AllowedCommand(
        argv=("bun", "test", "v2Backbone.test.ts"),
        cwd_parts=("api",),
    ),
    "(cd api && bun test v2Resolver.test.ts)": AllowedCommand(
        argv=("bun", "test", "v2Resolver.test.ts"),
        cwd_parts=("api",),
    ),
    (
        "(cd explorer && bun test src/utils/labels.test.ts "
        "src/components/componentInteraction.test.tsx "
        "src/components/graph/VisNetworkHost.test.ts)"
    ): AllowedCommand(
        argv=(
            "bun",
            "test",
            "src/utils/labels.test.ts",
            "src/components/componentInteraction.test.tsx",
            "src/components/graph/VisNetworkHost.test.ts",
        ),
        cwd_parts=("explorer",),
    ),
    (
        "(cd explorer && bun test src/api/graphApi.test.ts "
        "src/app.searchInspector.integration.test.tsx)"
    ): AllowedCommand(
        argv=(
            "bun",
            "test",
            "src/api/graphApi.test.ts",
            "src/app.searchInspector.integration.test.tsx",
        ),
        cwd_parts=("explorer",),
    ),
}


def run_parity_fixture(
    fixture_path: str | Path = DEFAULT_FIXTURE_PATH,
    *,
    repo_root: str | Path | None = None,
    run_id: str | None = None,
    output_path: str | Path | None = None,
    timeout_seconds: int = 300,
    executor: CommandExecutor | None = None,
) -> dict[str, Any]:
    """Run parity commands from a readiness fixture and write a JSON report."""
    root = _repo_root(repo_root)
    fixture = _resolve_existing_file(root, Path(fixture_path))
    resolved_run_id = _run_id(run_id)
    command_executor = executor or _execute_command
    started_at = _utc_now()

    contract_report = validate_backbone_contract_file(fixture)
    payload = _load_payload(fixture)
    plan = payload.get("integration_parity_runner_plan")

    report_path = _resolve_report_path(
        root=root,
        plan=plan,
        run_id=resolved_run_id,
        output_path=Path(output_path) if output_path is not None else None,
    )

    errors = list(contract_report.errors)
    warnings = list(contract_report.warnings)
    command_results: list[dict[str, Any]] = []
    case_results: list[dict[str, Any]] = []
    parity_cases_path: Path | None = None
    parity_cases: list[dict[str, Any]] = []

    if not isinstance(plan, dict):
        errors.append("integration_parity_runner_plan: expected a JSON object")
    else:
        parity_cases_path, parity_cases = _load_parity_cases(
            root=root,
            plan=plan,
            errors=errors,
            warnings=warnings,
        )

    commands = _string_list(plan.get("commands")) if isinstance(plan, dict) else []
    case_preflight_ok = len(errors) == len(contract_report.errors)
    if parity_cases:
        _validate_parity_case_coverage(
            parity_cases,
            declared_commands=commands,
            errors=errors,
        )
        case_preflight_ok = len(errors) == len(contract_report.errors)

    if not isinstance(plan, dict):
        pass
    elif not contract_report.ok:
        warnings.append("command execution skipped because readiness fixture failed validation")
    elif not case_preflight_ok:
        warnings.append("command execution skipped because parity cases failed preflight")
    else:
        for command in commands:
            result = _run_command(command_executor, command, root, timeout_seconds)
            command_results.append(_command_result_to_dict(result))
            if not result.passed:
                errors.append(f"command failed: {command}")

    if parity_cases:
        case_results = _build_case_results(parity_cases, command_results)
        for result in case_results:
            if not result["passed"]:
                errors.append(f"parity case failed: {result['case_id']}")

    finished_at = _utc_now()
    report = {
        "schema_version": REPORT_SCHEMA_VERSION,
        "ok": not errors,
        "run_id": resolved_run_id,
        "started_at_utc": started_at,
        "finished_at_utc": finished_at,
        "fixture_path": _relative_to_root(fixture, root),
        "parity_cases_path": _relative_to_root(parity_cases_path, root)
        if parity_cases_path is not None
        else None,
        "report_path": _relative_to_root(report_path, root),
        "surfaces": _string_list(plan.get("surfaces")) if isinstance(plan, dict) else [],
        "assertions": _string_list(plan.get("assertions")) if isinstance(plan, dict) else [],
        "commands_declared": _string_list(plan.get("commands")) if isinstance(plan, dict) else [],
        "commands_run": len(command_results),
        "commands_passed": sum(1 for result in command_results if result["passed"]),
        "cases_declared": len(parity_cases),
        "cases_passed": sum(1 for result in case_results if result["passed"]),
        "required_case_categories": sorted(REQUIRED_PARITY_CASE_CATEGORIES),
        "errors": sorted(set(errors)),
        "warnings": sorted(set(warnings)),
        "command_results": command_results,
        "case_results": case_results,
    }
    _write_json(report_path, report)
    return report


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run AEC-MEPFS Backbone parity checks.")
    parser.add_argument("--fixture", default=str(DEFAULT_FIXTURE_PATH))
    parser.add_argument("--repo-root", default=None)
    parser.add_argument("--run-id", default=None)
    parser.add_argument("--output", default=None)
    parser.add_argument("--timeout-seconds", type=int, default=300)
    args = parser.parse_args(argv)

    try:
        report = run_parity_fixture(
            args.fixture,
            repo_root=args.repo_root,
            run_id=args.run_id,
            output_path=args.output,
            timeout_seconds=args.timeout_seconds,
        )
    except (FileNotFoundError, ValueError) as exc:
        print(json.dumps({"ok": False, "errors": [str(exc)]}, indent=2, sort_keys=True))
        return 1

    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["ok"] else 1


def _execute_command(command: str, cwd: Path, timeout_seconds: int) -> CommandExecution:
    command_spec = ALLOWED_PARITY_COMMANDS.get(command)
    if command_spec is None:
        return CommandExecution(
            command=command,
            exit_code=127,
            duration_seconds=0.0,
            stderr="command is not in the allowed parity command registry",
        )

    started = time.monotonic()
    env = os.environ.copy()
    if command_spec.env:
        env.update(command_spec.env)
    try:
        completed = subprocess.run(
            list(command_spec.argv),
            cwd=cwd.joinpath(*command_spec.cwd_parts),
            env=env,
            text=True,
            capture_output=True,
            timeout=timeout_seconds,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        return CommandExecution(
            command=command,
            exit_code=124,
            duration_seconds=round(time.monotonic() - started, 4),
            stdout=_exception_output(exc.stdout),
            stderr=_exception_output(exc.stderr)
            or f"command timed out after {timeout_seconds} seconds",
        )
    return CommandExecution(
        command=command,
        exit_code=completed.returncode,
        duration_seconds=round(time.monotonic() - started, 4),
        stdout=completed.stdout,
        stderr=completed.stderr,
    )


def _run_command(
    executor: CommandExecutor,
    command: str,
    root: Path,
    timeout_seconds: int,
) -> CommandExecution:
    try:
        return executor(command, root, timeout_seconds)
    except subprocess.TimeoutExpired as exc:
        return CommandExecution(
            command=command,
            exit_code=124,
            duration_seconds=0.0,
            stdout=_exception_output(exc.stdout),
            stderr=_exception_output(exc.stderr)
            or f"command timed out after {timeout_seconds} seconds",
        )
    except Exception as exc:  # pragma: no cover - exercised through injected tests.
        return CommandExecution(
            command=command,
            exit_code=1,
            duration_seconds=0.0,
            stderr=f"command executor raised {type(exc).__name__}: {exc}",
        )


def _command_result_to_dict(result: CommandExecution) -> dict[str, Any]:
    return {
        "command": result.command,
        "exit_code": result.exit_code,
        "passed": result.passed,
        "duration_seconds": result.duration_seconds,
        "stdout_tail": _tail(result.stdout),
        "stderr_tail": _tail(result.stderr),
    }


def _load_parity_cases(
    *,
    root: Path,
    plan: dict[str, Any],
    errors: list[str],
    warnings: list[str],
) -> tuple[Path | None, list[dict[str, Any]]]:
    cases_path = _resolve_plan_file(
        root=root,
        value=plan.get("fixtures_path"),
        field_path="integration_parity_runner_plan.fixtures_path",
        errors=errors,
    )
    if cases_path is None:
        return None, []

    try:
        contract_report = validate_backbone_contract_file(cases_path)
        payload = _load_payload(cases_path)
    except (OSError, ValueError) as exc:
        relative_path = _relative_to_root(cases_path, root)
        errors.append(f"api_explorer_parity_cases_file: failed to load {relative_path}: {exc}")
        return cases_path, []

    errors.extend(f"api_explorer_parity_cases_file.{error}" for error in contract_report.errors)
    warnings.extend(
        f"api_explorer_parity_cases_file.{warning}" for warning in contract_report.warnings
    )
    schema_version = str(payload.get("schema_version", "")).strip()
    if schema_version != PARITY_CASES_SCHEMA_VERSION:
        errors.append(
            "api_explorer_parity_cases_file.schema_version: "
            f"expected {PARITY_CASES_SCHEMA_VERSION}"
        )

    cases = _dict_list(payload.get("api_explorer_parity_cases"))
    if not cases:
        errors.append("api_explorer_parity_cases_file.api_explorer_parity_cases: expected cases")
    return cases_path, cases


def _validate_parity_case_coverage(
    cases: list[dict[str, Any]],
    *,
    declared_commands: list[str],
    errors: list[str],
) -> None:
    declared_command_set = set(declared_commands)
    covered_command_set = set()
    categories = set()
    for index, case in enumerate(cases):
        path = f"api_explorer_parity_cases[{index}]"
        missing_fields = sorted(
            field_name
            for field_name in PARITY_CASE_REQUIRED_FIELDS
            if not _has_value(case.get(field_name))
        )
        for field_name in missing_fields:
            errors.append(f"{path}.{field_name}: required field missing")

        assertions = case.get("assertions")
        if not isinstance(assertions, list) or not assertions:
            errors.append(f"{path}.assertions: expected a non-empty list")

        category = str(case.get("parity_category", "")).strip()
        if category:
            categories.add(category)

        command = str(case.get("covered_by_command", "")).strip()
        if command and command not in declared_command_set:
            errors.append(f"{path}.covered_by_command: command is not declared by runner plan")
        elif command:
            covered_command_set.add(command)

    missing_categories = sorted(REQUIRED_PARITY_CASE_CATEGORIES - categories)
    if missing_categories:
        errors.append(
            "api_explorer_parity_cases: missing required parity categories "
            f"({', '.join(missing_categories)})"
        )
    uncovered_commands = sorted(declared_command_set - covered_command_set)
    if uncovered_commands:
        errors.append(
            "api_explorer_parity_cases: declared commands without parity case coverage "
            f"({', '.join(uncovered_commands)})"
        )


def _build_case_results(
    cases: list[dict[str, Any]],
    command_results: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    results_by_command = {str(result["command"]): result for result in command_results}
    case_results = []
    for case in cases:
        command = str(case.get("covered_by_command", "")).strip()
        command_result = results_by_command.get(command)
        command_passed = command_result is not None and bool(command_result["passed"])
        case_results.append(
            {
                "case_id": str(case.get("case_id", "")),
                "parity_category": str(case.get("parity_category", "")),
                "surface": str(case.get("surface", "")),
                "route": str(case.get("route", "")),
                "covered_by_command": command,
                "assertions": _string_list(case.get("assertions")),
                "passed": command_passed,
                "status": "passed" if command_passed else "failed",
            }
        )
    return case_results


def _load_payload(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path}: expected a JSON object")
    return payload


def _repo_root(value: str | Path | None) -> Path:
    if value is not None:
        return Path(value).resolve()
    return Path(__file__).resolve().parents[3]


def _resolve_existing_file(root: Path, value: Path) -> Path:
    path = value if value.is_absolute() else root / value
    path = path.resolve()
    if not path.is_file():
        raise FileNotFoundError(f"fixture not found: {path}")
    return path


def _resolve_plan_file(
    *,
    root: Path,
    value: Any,
    field_path: str,
    errors: list[str],
) -> Path | None:
    if not _has_value(value):
        errors.append(f"{field_path}: required field missing")
        return None

    candidate = Path(str(value).strip())
    if candidate.is_absolute():
        errors.append(f"{field_path}: path must be repo-relative")
        return None

    path = (root / candidate).resolve()
    try:
        path.relative_to(root)
    except ValueError:
        errors.append(f"{field_path}: path must stay inside the repository")
        return None

    if not path.is_file():
        errors.append(f"{field_path}: file not found at {candidate}")
        return None
    return path


def _resolve_report_path(
    *,
    root: Path,
    plan: Any,
    run_id: str,
    output_path: Path | None,
) -> Path:
    if output_path is not None:
        candidate = output_path
    elif isinstance(plan, dict) and isinstance(plan.get("report_path"), str):
        candidate = Path(plan["report_path"].replace("RUN_ID", run_id))
    else:
        candidate = PARITY_REPORT_ROOT / run_id / PARITY_REPORT_FILENAME

    if candidate.is_absolute():
        report_path = candidate.resolve()
    else:
        report_path = (root / candidate).resolve()

    allowed_root = (root / PARITY_REPORT_ROOT).resolve()
    try:
        relative_parts = report_path.relative_to(allowed_root).parts
    except ValueError as exc:
        raise ValueError("report path must stay inside the parity report directory") from exc
    if len(relative_parts) != 2 or relative_parts[0] != run_id:
        raise ValueError("report path must be scoped to the current parity run id")
    if relative_parts[1] != PARITY_REPORT_FILENAME:
        raise ValueError(f"report filename must be {PARITY_REPORT_FILENAME}")
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


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value]


def _dict_list(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, dict)]


def _has_value(value: Any) -> bool:
    return value is not None and str(value).strip() != ""


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
