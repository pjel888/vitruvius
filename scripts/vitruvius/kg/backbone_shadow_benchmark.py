"""File-backed benchmark runner for AEC-MEPFS Backbone shadow readiness.

The benchmark measures local file-backed validation/read/scan operations over
existing shadow evidence. It does not execute runtime resolver paths, call API
or Explorer servers, query Neo4j, rebuild the KG, or evaluate live latency
budgets.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import platform
import re
import subprocess
import sys
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Callable, Sequence

from vitruvius.kg.backbone_api_route_inventory import summarize_shadow_preview_route_boundaries
from vitruvius.kg.backbone_contracts import validate_backbone_contract_file


REPORT_SCHEMA_VERSION = "aec-bb-shadow-benchmark-report/v1"
DEFAULT_FIXTURE_PATH = Path(
    "scripts/tests/fixtures/aec_mepfs_backbone/valid_integration_readiness_s3.json"
)
BENCHMARK_REPORT_ROOT = Path("006_System-Manifests/aec-mepfs-backbone/benchmarks")
BENCHMARK_REPORT_FILENAME = "benchmark-report.json"
DEFAULT_CONSUMER_REPORT_PATH = Path(
    "006_System-Manifests/aec-mepfs-backbone/shadow-staging/20260426T003710Z/"
    "shadow-staging-consumer-report.json"
)
DEFAULT_SHADOW_GRAPH_PATH = Path(
    "006_System-Manifests/aec-mepfs-backbone/shadow-staging/20260426T003710Z/"
    "shadow-backbone-graph.json"
)
DEFAULT_PLACEMENT_QA_REPORT_PATH = Path(
    "006_System-Manifests/aec-mepfs-backbone/placement-qa/20260426T015915Z/"
    "placement-qa-report.json"
)
DEFAULT_RESOLVER_QA_REPORT_PATH = Path(
    "006_System-Manifests/aec-mepfs-backbone/resolver-qa/20260426T060300Z/"
    "resolver-qa-report.json"
)
DEFAULT_PARITY_REPORT_PATH = Path(
    "006_System-Manifests/aec-mepfs-backbone/parity/20260426T062032Z/"
    "api-explorer-parity-report.json"
)
DEFAULT_BOUNDARY_AUDIT_REPORT_PATH = Path(
    "006_System-Manifests/aec-mepfs-backbone/boundary-audit/20260426T075100Z/"
    "shadow-boundary-audit-report.json"
)
DEFAULT_API_INDEX_PATH = Path("api/index.ts")
RUN_ID_RE = re.compile(r"^[A-Za-z0-9_.-]+$")
Timer = Callable[[], float]


def run_shadow_benchmark(
    fixture_path: str | Path = DEFAULT_FIXTURE_PATH,
    *,
    repo_root: str | Path | None = None,
    run_id: str | None = None,
    output_path: str | Path | None = None,
    consumer_report_path: str | Path = DEFAULT_CONSUMER_REPORT_PATH,
    shadow_graph_path: str | Path = DEFAULT_SHADOW_GRAPH_PATH,
    placement_qa_report_path: str | Path = DEFAULT_PLACEMENT_QA_REPORT_PATH,
    resolver_qa_report_path: str | Path = DEFAULT_RESOLVER_QA_REPORT_PATH,
    parity_report_path: str | Path = DEFAULT_PARITY_REPORT_PATH,
    boundary_audit_report_path: str | Path = DEFAULT_BOUNDARY_AUDIT_REPORT_PATH,
    api_index_path: str | Path = DEFAULT_API_INDEX_PATH,
    timer: Timer | None = None,
) -> dict[str, Any]:
    """Run local file-backed benchmark operations and write a JSON report."""
    root = _repo_root(repo_root)
    fixture = _resolve_existing_file(root, Path(fixture_path), "fixture")
    resolved_run_id = _run_id(run_id)
    started_at = _utc_now()
    clock = timer or time.perf_counter

    contract_report = validate_backbone_contract_file(fixture)
    payload = _load_json_object(fixture, "fixture")
    plan = payload.get("integration_benchmark_plan")
    report_path = _resolve_report_path(
        root=root,
        plan=plan,
        run_id=resolved_run_id,
        output_path=Path(output_path) if output_path is not None else None,
    )

    evidence_paths = {
        "consumer_report": _resolve_existing_file(root, Path(consumer_report_path), "consumer report"),
        "shadow_graph": _resolve_existing_file(root, Path(shadow_graph_path), "shadow graph"),
        "placement_qa_report": _resolve_existing_file(
            root,
            Path(placement_qa_report_path),
            "placement QA report",
        ),
        "resolver_qa_report": _resolve_existing_file(
            root,
            Path(resolver_qa_report_path),
            "resolver QA report",
        ),
        "parity_report": _resolve_existing_file(root, Path(parity_report_path), "parity report"),
        "boundary_audit_report": _resolve_existing_file(
            root,
            Path(boundary_audit_report_path),
            "boundary audit report",
        ),
        "api_index": _resolve_existing_file(root, Path(api_index_path), "api index"),
    }

    errors = list(contract_report.errors)
    warnings = list(contract_report.warnings)
    operations: list[dict[str, Any]] = []

    if not isinstance(plan, dict):
        errors.append("integration_benchmark_plan: expected a JSON object")
        repetitions = 0
        percentiles: list[str] = []
        declared_commands: list[str] = []
        declared_thresholds: list[str] = []
    else:
        repetitions = int(plan.get("repetitions") or 0)
        percentiles = _string_list(plan.get("percentiles"))
        declared_commands = _string_list(plan.get("commands"))
        declared_thresholds = _string_list(plan.get("thresholds"))
        future_commands = [command for command in declared_commands if "future " in command]
        if future_commands:
            warnings.append(
                "runtime benchmark commands are declared but not executed by this "
                "shadow file-backed runner"
            )

    if contract_report.ok and isinstance(plan, dict) and repetitions >= 3:
        operation_specs: list[tuple[str, Callable[[], None]]] = [
            ("contract_validation", lambda: _assert_contract_valid(fixture)),
            ("shadow_evidence_json_read", lambda: _read_shadow_evidence(evidence_paths)),
            ("shadow_graph_shape_scan", lambda: _scan_shadow_graph(evidence_paths["shadow_graph"])),
            (
                "api_route_static_scan",
                lambda: _scan_api_routes(root, evidence_paths["api_index"]),
            ),
            ("input_hash_scan", lambda: _hash_files(evidence_paths)),
        ]
        operations = [
            _run_operation(name, operation, repetitions, clock, errors)
            for name, operation in operation_specs
        ]
    elif not contract_report.ok:
        warnings.append("benchmark operations skipped because readiness fixture failed validation")
    elif repetitions < 3:
        errors.append("integration_benchmark_plan.repetitions: must be >= 3")

    finished_at = _utc_now()
    report = {
        "schema_version": REPORT_SCHEMA_VERSION,
        "ok": not errors,
        "run_id": resolved_run_id,
        "started_at_utc": started_at,
        "finished_at_utc": finished_at,
        "fixture_path": _relative_to_root(fixture, root),
        "report_path": _relative_to_root(report_path, root),
        "inputs": {
            label: _relative_to_root(path, root) for label, path in evidence_paths.items()
        },
        "input_file_hashes_sha256": _hash_input_files(evidence_paths),
        "repo_state": _read_repo_state(root),
        "environment": {
            "python_version": platform.python_version(),
            "platform": platform.platform(),
            "cpu_count": os.cpu_count(),
        },
        "benchmark_scope": {
            "shadow_file_backed_only": True,
            "runtime_resolver_invocation": False,
            "api_server_calls": False,
            "explorer_runtime_calls": False,
            "neo4j_queries": False,
            "kg_rebuild": False,
            "feature_flag_cutover": False,
            "protected_content_ingest": False,
            "runtime_thresholds_evaluated": False,
        },
        "plan": {
            "repetitions": repetitions,
            "percentiles": percentiles,
            "declared_commands": declared_commands,
            "declared_thresholds": declared_thresholds,
            "runtime_threshold_disposition": "not_evaluated_shadow_file_backed_only",
        },
        "operations": operations,
        "errors": sorted(set(errors)),
        "warnings": sorted(set(warnings)),
    }
    _write_json(report_path, report)
    return report


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run AEC-MEPFS Backbone shadow file-backed benchmarks."
    )
    parser.add_argument("--fixture", default=str(DEFAULT_FIXTURE_PATH))
    parser.add_argument("--repo-root", default=None)
    parser.add_argument("--run-id", default=None)
    parser.add_argument("--output", default=None)
    parser.add_argument("--consumer-report", default=str(DEFAULT_CONSUMER_REPORT_PATH))
    parser.add_argument("--shadow-graph", default=str(DEFAULT_SHADOW_GRAPH_PATH))
    parser.add_argument("--placement-qa-report", default=str(DEFAULT_PLACEMENT_QA_REPORT_PATH))
    parser.add_argument("--resolver-qa-report", default=str(DEFAULT_RESOLVER_QA_REPORT_PATH))
    parser.add_argument("--parity-report", default=str(DEFAULT_PARITY_REPORT_PATH))
    parser.add_argument("--boundary-audit-report", default=str(DEFAULT_BOUNDARY_AUDIT_REPORT_PATH))
    parser.add_argument("--api-index", default=str(DEFAULT_API_INDEX_PATH))
    args = parser.parse_args(argv)

    try:
        report = run_shadow_benchmark(
            args.fixture,
            repo_root=args.repo_root,
            run_id=args.run_id,
            output_path=args.output,
            consumer_report_path=args.consumer_report,
            shadow_graph_path=args.shadow_graph,
            placement_qa_report_path=args.placement_qa_report,
            resolver_qa_report_path=args.resolver_qa_report,
            parity_report_path=args.parity_report,
            boundary_audit_report_path=args.boundary_audit_report,
            api_index_path=args.api_index,
        )
    except (FileNotFoundError, ValueError) as exc:
        print(json.dumps({"ok": False, "errors": [str(exc)]}, indent=2, sort_keys=True))
        return 1

    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["ok"] else 1


def _run_operation(
    name: str,
    operation: Callable[[], None],
    repetitions: int,
    timer: Timer,
    errors: list[str],
) -> dict[str, Any]:
    durations_ms: list[float] = []
    operation_errors: list[str] = []
    for index in range(repetitions):
        start = timer()
        try:
            operation()
        except (FileNotFoundError, ValueError, json.JSONDecodeError) as exc:
            operation_errors.append(f"{name}[{index + 1}]: {exc}")
        finally:
            end = timer()
        durations_ms.append(max(0.0, (end - start) * 1000.0))
        if operation_errors:
            break
    errors.extend(operation_errors)
    return {
        "name": name,
        "ok": not operation_errors,
        "repetitions": len(durations_ms),
        "durations_ms": [round(value, 6) for value in durations_ms],
        "p50_ms": round(_percentile(durations_ms, 50), 6),
        "p95_ms": round(_percentile(durations_ms, 95), 6),
        "errors": operation_errors,
    }


def _assert_contract_valid(fixture: Path) -> None:
    report = validate_backbone_contract_file(fixture)
    if not report.ok:
        raise ValueError("; ".join(report.errors))


def _read_shadow_evidence(paths: dict[str, Path]) -> None:
    for label, path in paths.items():
        if label == "api_index":
            path.read_text(encoding="utf-8")
            continue
        _load_json_object(path, label)


def _scan_shadow_graph(path: Path) -> None:
    graph = _load_json_object(path, "shadow graph")
    counts = graph.get("counts")
    if not isinstance(counts, dict):
        raise ValueError("shadow graph counts must be present")
    if counts.get("nodes", 0) <= 0:
        raise ValueError("shadow graph must contain at least one node")
    if not isinstance(graph.get("nodes"), list) or not isinstance(graph.get("edges"), list):
        raise ValueError("shadow graph nodes and edges must be lists")


def _scan_api_routes(root: Path, path: Path) -> None:
    status = summarize_shadow_preview_route_boundaries(root, path)
    if status.get("checked") is not True:
        raise ValueError("api route inventory must be checked")
    if status.get("resolveRouteMounted") is not False:
        raise ValueError("/v2/resolve must remain unmounted")
    if status.get("traceRouteMounted") is not False:
        raise ValueError("/v2/resolve/trace must remain unmounted")
    missing_routes = [
        name
        for name, present in status.get("previewRoutesPresent", {}).items()
        if not present
    ]
    if missing_routes:
        raise ValueError(f"missing expected preview routes ({', '.join(missing_routes)})")


def _hash_files(paths: dict[str, Path]) -> None:
    _hash_input_files(paths)


def _percentile(values: list[float], percentile: int) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    index = max(0, min(len(ordered) - 1, math.ceil((percentile / 100.0) * len(ordered)) - 1))
    return ordered[index]


def _load_json_object(path: Path, label: str) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{label}: expected a JSON object")
    return payload


def _repo_root(value: str | Path | None) -> Path:
    if value is not None:
        return Path(value).resolve()
    return Path(__file__).resolve().parents[3]


def _resolve_existing_file(root: Path, value: Path, label: str) -> Path:
    path = value.resolve() if value.is_absolute() else (root / value).resolve()
    try:
        path.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"{label} path must stay inside repo root") from exc
    if not path.is_file():
        raise FileNotFoundError(f"{label} not found: {path}")
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
        candidate = BENCHMARK_REPORT_ROOT / run_id / BENCHMARK_REPORT_FILENAME
    report_path = candidate.resolve() if candidate.is_absolute() else (root / candidate).resolve()
    allowed_root = (root / BENCHMARK_REPORT_ROOT).resolve()
    try:
        relative_parts = report_path.relative_to(allowed_root).parts
    except ValueError as exc:
        raise ValueError("report path must stay inside the benchmark report directory") from exc
    if len(relative_parts) != 2 or relative_parts[0] != run_id:
        raise ValueError("report path must be scoped to the current benchmark run id")
    if relative_parts[1] != BENCHMARK_REPORT_FILENAME:
        raise ValueError(f"report filename must be {BENCHMARK_REPORT_FILENAME}")
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


def _hash_input_files(paths: dict[str, Path]) -> dict[str, str]:
    hashes: dict[str, str] = {}
    for label, path in paths.items():
        digest = hashlib.sha256()
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
        hashes[label] = digest.hexdigest()
    return hashes


def _read_repo_state(root: Path) -> dict[str, Any]:
    head = _run_git(root, "rev-parse", "HEAD")
    status = _run_git(root, "status", "--short")
    return {
        "git_head_commit": head,
        "working_tree_dirty": bool(status),
    }


def _run_git(root: Path, *args: str) -> str | None:
    try:
        result = subprocess.run(
            ("git", *args),
            cwd=root,
            check=False,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    if result.returncode != 0:
        return None
    return result.stdout.strip()


def _relative_to_root(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, str)]


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
