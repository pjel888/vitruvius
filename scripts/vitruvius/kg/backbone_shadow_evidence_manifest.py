"""Consolidated manifest for AEC-MEPFS Backbone shadow evidence.

The manifest verifies existing file-backed reports and records their hashes in
one auditable packet. It does not call API or Explorer runtimes, query Neo4j,
rebuild KG artifacts, ingest protected content, change feature flags, or
promote shadow artifacts.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Sequence

from vitruvius.kg.backbone_repo_state import read_repo_state


REPORT_SCHEMA_VERSION = "aec-bb-shadow-evidence-manifest-report/v1"
EVIDENCE_MANIFEST_REPORT_ROOT = Path(
    "006_System-Manifests/aec-mepfs-backbone/evidence-manifest"
)
EVIDENCE_MANIFEST_REPORT_FILENAME = "shadow-evidence-manifest-report.json"
RUN_ID_RE = re.compile(r"^[A-Za-z0-9_.-]+$")

DEFAULT_PRODUCER_REPORT_PATH = Path(
    "006_System-Manifests/aec-mepfs-backbone/shadow-staging/20260426T003710Z/"
    "shadow-staging-report.json"
)
DEFAULT_CONSUMER_REPORT_PATH = Path(
    "006_System-Manifests/aec-mepfs-backbone/shadow-staging/20260426T003710Z/"
    "shadow-staging-consumer-report.json"
)
DEFAULT_SHADOW_GRAPH_PATH = Path(
    "006_System-Manifests/aec-mepfs-backbone/shadow-staging/20260426T003710Z/"
    "shadow-backbone-graph.json"
)
DEFAULT_PARITY_REPORT_PATH = Path(
    "006_System-Manifests/aec-mepfs-backbone/parity/20260426T095440Z/"
    "api-explorer-parity-report.json"
)
DEFAULT_PLACEMENT_QA_REPORT_PATH = Path(
    "006_System-Manifests/aec-mepfs-backbone/placement-qa/20260426T015915Z/"
    "placement-qa-report.json"
)
DEFAULT_RESOLVER_QA_REPORT_PATH = Path(
    "006_System-Manifests/aec-mepfs-backbone/resolver-qa/20260426T060300Z/"
    "resolver-qa-report.json"
)
DEFAULT_BOUNDARY_AUDIT_REPORT_PATH = Path(
    "006_System-Manifests/aec-mepfs-backbone/boundary-audit/20260426T100631Z/"
    "shadow-boundary-audit-report.json"
)
DEFAULT_BENCHMARK_REPORT_PATH = Path(
    "006_System-Manifests/aec-mepfs-backbone/benchmarks/20260426T100632Z/"
    "benchmark-report.json"
)
DEFAULT_ROUTE_INVENTORY_REPORT_PATH = Path(
    "006_System-Manifests/aec-mepfs-backbone/api-route-inventory/20260426T095439Z/"
    "api-route-inventory-report.json"
)
DEFAULT_API_INDEX_PATH = Path("api/index.ts")

EXPECTED_ARTIFACTS = {
    "producer_report": ("aec-bb-shadow-staging-report/v1", True),
    "consumer_report": ("aec-bb-shadow-staging-consumer-report/v1", True),
    "shadow_graph": ("aec-bb-shadow-graph/v1", False),
    "parity_report": ("aec-bb-parity-report/v1", True),
    "placement_qa_report": ("aec-bb-placement-qa-report/v1", True),
    "resolver_qa_report": ("aec-bb-resolver-qa-report/v1", True),
    "boundary_audit_report": ("aec-bb-shadow-boundary-audit-report/v1", True),
    "benchmark_report": ("aec-bb-shadow-benchmark-report/v1", True),
    "route_inventory_report": ("aec-bb-api-route-inventory-report/v1", True),
}
EXPECTED_BENCHMARK_OPERATION_NAMES = (
    "contract_validation",
    "shadow_evidence_json_read",
    "shadow_graph_shape_scan",
    "api_route_static_scan",
    "input_hash_scan",
)
BENCHMARK_RUNTIME_THRESHOLD_DISPOSITION = "not_evaluated_shadow_file_backed_only"
REQUIRED_BENCHMARK_BLOCKED_RUNTIME_SCOPE = (
    "runtime_resolver_invocation",
    "api_server_calls",
    "explorer_runtime_calls",
    "neo4j_queries",
)


def run_shadow_evidence_manifest(
    *,
    repo_root: str | Path | None = None,
    run_id: str | None = None,
    output_path: str | Path | None = None,
    producer_report_path: str | Path = DEFAULT_PRODUCER_REPORT_PATH,
    consumer_report_path: str | Path = DEFAULT_CONSUMER_REPORT_PATH,
    shadow_graph_path: str | Path = DEFAULT_SHADOW_GRAPH_PATH,
    parity_report_path: str | Path = DEFAULT_PARITY_REPORT_PATH,
    placement_qa_report_path: str | Path = DEFAULT_PLACEMENT_QA_REPORT_PATH,
    resolver_qa_report_path: str | Path = DEFAULT_RESOLVER_QA_REPORT_PATH,
    boundary_audit_report_path: str | Path = DEFAULT_BOUNDARY_AUDIT_REPORT_PATH,
    benchmark_report_path: str | Path = DEFAULT_BENCHMARK_REPORT_PATH,
    route_inventory_report_path: str | Path = DEFAULT_ROUTE_INVENTORY_REPORT_PATH,
    api_index_path: str | Path = DEFAULT_API_INDEX_PATH,
) -> dict[str, Any]:
    """Verify current shadow evidence files and write a manifest report."""
    root = _repo_root(repo_root)
    resolved_run_id = _run_id(run_id)
    started_at = _utc_now()
    paths = {
        "producer_report": _resolve_existing_file(
            root,
            Path(producer_report_path),
            "producer report",
        ),
        "consumer_report": _resolve_existing_file(
            root,
            Path(consumer_report_path),
            "consumer report",
        ),
        "shadow_graph": _resolve_existing_file(root, Path(shadow_graph_path), "shadow graph"),
        "parity_report": _resolve_existing_file(root, Path(parity_report_path), "parity report"),
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
        "boundary_audit_report": _resolve_existing_file(
            root,
            Path(boundary_audit_report_path),
            "boundary audit report",
        ),
        "benchmark_report": _resolve_existing_file(
            root,
            Path(benchmark_report_path),
            "benchmark report",
        ),
        "route_inventory_report": _resolve_existing_file(
            root,
            Path(route_inventory_report_path),
            "route inventory report",
        ),
    }
    api_index = _resolve_existing_file(root, Path(api_index_path), "API index")
    payloads = {
        label: _load_json_object(path, label)
        for label, path in paths.items()
    }
    report_path = _resolve_report_path(
        root=root,
        run_id=resolved_run_id,
        output_path=Path(output_path) if output_path is not None else None,
    )

    errors: list[str] = []
    warnings: list[str] = []
    artifact_results = [
        _validate_artifact(label, payloads[label], paths[label], root)
        for label in EXPECTED_ARTIFACTS
    ]
    for result in artifact_results:
        errors.extend(result["errors"])
        warnings.extend(result["warnings"])

    repo_state = read_repo_state(root)
    errors.extend(_cross_check_paths(root, paths, payloads, api_index, repo_state))
    safety_invariants = _safety_invariants(payloads, errors)
    for name, value in safety_invariants.items():
        if not value:
            errors.append(f"safety invariant failed: {name}")
    errors = sorted(set(errors))

    finished_at = _utc_now()
    report = {
        "schema_version": REPORT_SCHEMA_VERSION,
        "ok": not errors,
        "run_id": resolved_run_id,
        "started_at_utc": started_at,
        "finished_at_utc": finished_at,
        "report_path": _relative_to_root(report_path, root),
        "inputs": {
            **{label: _relative_to_root(path, root) for label, path in paths.items()},
            "api_index": _relative_to_root(api_index, root),
        },
        "input_file_hashes_sha256": {
            **{label: _hash_file(path) for label, path in paths.items()},
            "api_index": _hash_file(api_index),
        },
        "repo_state": repo_state,
        "summary": _summary(payloads),
        "safety_invariants": safety_invariants,
        "artifact_results": artifact_results,
        "errors": errors,
        "warnings": sorted(set(warnings)),
    }
    _write_json(report_path, report)
    return report


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate an AEC-MEPFS Backbone shadow evidence manifest."
    )
    parser.add_argument("--repo-root", default=None)
    parser.add_argument("--run-id", default=None)
    parser.add_argument("--output", default=None)
    parser.add_argument("--producer-report", default=str(DEFAULT_PRODUCER_REPORT_PATH))
    parser.add_argument("--consumer-report", default=str(DEFAULT_CONSUMER_REPORT_PATH))
    parser.add_argument("--shadow-graph", default=str(DEFAULT_SHADOW_GRAPH_PATH))
    parser.add_argument("--parity-report", default=str(DEFAULT_PARITY_REPORT_PATH))
    parser.add_argument("--placement-qa-report", default=str(DEFAULT_PLACEMENT_QA_REPORT_PATH))
    parser.add_argument("--resolver-qa-report", default=str(DEFAULT_RESOLVER_QA_REPORT_PATH))
    parser.add_argument("--boundary-audit-report", default=str(DEFAULT_BOUNDARY_AUDIT_REPORT_PATH))
    parser.add_argument("--benchmark-report", default=str(DEFAULT_BENCHMARK_REPORT_PATH))
    parser.add_argument("--route-inventory-report", default=str(DEFAULT_ROUTE_INVENTORY_REPORT_PATH))
    parser.add_argument("--api-index", default=str(DEFAULT_API_INDEX_PATH))
    args = parser.parse_args(argv)

    try:
        report = run_shadow_evidence_manifest(
            repo_root=args.repo_root,
            run_id=args.run_id,
            output_path=args.output,
            producer_report_path=args.producer_report,
            consumer_report_path=args.consumer_report,
            shadow_graph_path=args.shadow_graph,
            parity_report_path=args.parity_report,
            placement_qa_report_path=args.placement_qa_report,
            resolver_qa_report_path=args.resolver_qa_report,
            boundary_audit_report_path=args.boundary_audit_report,
            benchmark_report_path=args.benchmark_report,
            route_inventory_report_path=args.route_inventory_report,
            api_index_path=args.api_index,
        )
    except (FileNotFoundError, ValueError) as exc:
        print(json.dumps({"ok": False, "errors": [str(exc)]}, indent=2, sort_keys=True))
        return 1

    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["ok"] else 1


def _validate_artifact(
    label: str,
    payload: dict[str, Any],
    path: Path,
    root: Path,
) -> dict[str, Any]:
    expected_schema, requires_ok = EXPECTED_ARTIFACTS[label]
    errors: list[str] = []
    warnings: list[str] = []
    if payload.get("schema_version") != expected_schema:
        errors.append(f"{label}: unexpected schema_version")
    if requires_ok and payload.get("ok") is not True:
        errors.append(f"{label}: ok must be true")
    if label == "shadow_graph" and payload.get("status") != "shadow_graph_staged":
        errors.append("shadow_graph: status must be shadow_graph_staged")
    if label == "benchmark_report":
        scope = _dict(payload.get("benchmark_scope"))
        if scope.get("runtime_thresholds_evaluated") is not False:
            errors.append("benchmark_report: runtime thresholds must remain unevaluated")
        if scope.get("shadow_file_backed_only") is not True:
            errors.append("benchmark_report: must remain shadow file-backed only")
        errors.extend(_validate_benchmark_operation_coverage(payload))
        errors.extend(_validate_benchmark_runtime_threshold_evidence(payload))
    if label == "route_inventory_report":
        summary = _dict(payload.get("summary"))
        if summary.get("missing_preview_routes"):
            errors.append("route_inventory_report: preview routes must all be present")
        if summary.get("resolve_route_mounted") is not False:
            errors.append("route_inventory_report: unauthorized /v2/resolve must remain unmounted")
        if summary.get("trace_route_mounted") is not False:
            errors.append("route_inventory_report: unauthorized /v2/resolve/trace must remain unmounted")
        if summary.get("resolve_route_declared") is True and summary.get(
            "default_off_resolve_route_declared"
        ) is not True:
            errors.append(
                "route_inventory_report: declared /v2/resolve* routes must be default-off guarded"
            )
    return {
        "label": label,
        "path": _relative_to_root(path, root),
        "schema_version": payload.get("schema_version"),
        "ok": not errors,
        "errors": errors,
        "warnings": warnings,
    }


def _cross_check_paths(
    root: Path,
    paths: dict[str, Path],
    payloads: dict[str, dict[str, Any]],
    api_index_path: Path,
    manifest_repo_state: dict[str, Any],
) -> list[str]:
    errors: list[str] = []
    producer = payloads["producer_report"]
    consumer = payloads["consumer_report"]
    graph = payloads["shadow_graph"]
    benchmark = payloads["benchmark_report"]
    api_index_hash = _hash_file(api_index_path)

    _expect_payload_path(
        errors,
        "producer_report.artifact_path",
        producer.get("artifact_path"),
        "006_System-Manifests/aec-mepfs-backbone/shadow-staging/20260426T003710Z/"
        "shadow-backbone-staging.json",
    )
    _expect_payload_path(
        errors,
        "consumer_report.producer_report_path",
        consumer.get("producer_report_path"),
        _relative_to_root(paths["producer_report"], root),
    )
    _expect_payload_path(
        errors,
        "consumer_report.shadow_graph_path",
        consumer.get("shadow_graph_path"),
        _relative_to_root(paths["shadow_graph"], root),
    )
    _expect_payload_path(
        errors,
        "shadow_graph.source_artifact_path",
        graph.get("source_artifact_path"),
        producer.get("artifact_path"),
    )
    benchmark_inputs = _dict(benchmark.get("inputs"))
    _expect_payload_path(
        errors,
        "benchmark_report.inputs.boundary_audit_report",
        benchmark_inputs.get("boundary_audit_report"),
        _relative_to_root(paths["boundary_audit_report"], root),
    )
    _expect_payload_path(
        errors,
        "benchmark_report.inputs.api_index",
        benchmark_inputs.get("api_index"),
        "api/index.ts",
    )
    for label in ("route_inventory_report", "boundary_audit_report", "benchmark_report"):
        input_hashes = _dict(payloads[label].get("input_file_hashes_sha256"))
        if input_hashes.get("api_index") != api_index_hash:
            errors.append(
                f"{label}.input_file_hashes_sha256.api_index must match current api/index.ts"
            )
    consumer_counts = _dict(consumer.get("shadow_graph_counts"))
    graph_counts = _dict(graph.get("counts"))
    if consumer_counts != graph_counts:
        errors.append("consumer_report.shadow_graph_counts must match shadow_graph.counts")
    errors.extend(_cross_check_repo_state_freshness(payloads, manifest_repo_state))
    return errors


def _cross_check_repo_state_freshness(
    payloads: dict[str, dict[str, Any]],
    manifest_repo_state: dict[str, Any],
) -> list[str]:
    errors: list[str] = []
    manifest_head = manifest_repo_state.get("git_head_commit")
    observed_heads: dict[str, str] = {}
    for label, payload in payloads.items():
        repo_state = _dict(payload.get("repo_state"))
        if not repo_state:
            continue
        head = repo_state.get("git_head_commit")
        if isinstance(head, str) and head:
            observed_heads[label] = head
        if repo_state.get("source_working_tree_dirty") is True:
            errors.append(f"{label}.repo_state.source_working_tree_dirty must be false")
        source_dirty_count = repo_state.get("source_dirty_path_count")
        if isinstance(source_dirty_count, (int, float)) and source_dirty_count > 0:
            errors.append(f"{label}.repo_state.source_dirty_path_count must be 0")
    if isinstance(manifest_head, str) and manifest_head:
        for label, head in observed_heads.items():
            if head != manifest_head:
                errors.append(
                    f"{label}.repo_state.git_head_commit must match evidence manifest git_head_commit"
                )
    elif len(set(observed_heads.values())) > 1:
        errors.append("input report repo_state.git_head_commit values must match")
    return errors


def _safety_invariants(payloads: dict[str, dict[str, Any]], errors: list[str]) -> dict[str, bool]:
    boundary_invariants = _dict(payloads["boundary_audit_report"].get("safety_invariants"))
    benchmark_scope = _dict(payloads["benchmark_report"].get("benchmark_scope"))
    route_summary = _dict(payloads["route_inventory_report"].get("summary"))
    return {
        "all_artifacts_ok": not errors,
        "boundary_audit_safety_green": all(boundary_invariants.values()),
        "benchmark_shadow_file_backed_only": benchmark_scope.get("shadow_file_backed_only") is True,
        "runtime_thresholds_not_evaluated": benchmark_scope.get(
            "runtime_thresholds_evaluated"
        ) is False,
        "route_inventory_preview_routes_complete": route_summary.get(
            "missing_preview_routes"
        ) == [],
        "resolver_routes_absent_or_default_off": (
            route_summary.get("resolve_route_mounted") is False
            and route_summary.get("trace_route_mounted") is False
            and (
                route_summary.get("resolve_route_declared") is not True
                or route_summary.get("default_off_resolve_route_declared") is True
            )
        ),
        "no_runtime_promotion": (
            benchmark_scope.get("api_server_calls") is False
            and benchmark_scope.get("explorer_runtime_calls") is False
            and benchmark_scope.get("neo4j_queries") is False
            and benchmark_scope.get("kg_rebuild") is False
            and benchmark_scope.get("feature_flag_cutover") is False
            and benchmark_scope.get("protected_content_ingest") is False
        ),
    }


def _summary(payloads: dict[str, dict[str, Any]]) -> dict[str, Any]:
    graph_counts = _dict(payloads["shadow_graph"].get("counts"))
    boundary_summary = _dict(payloads["boundary_audit_report"].get("summary"))
    benchmark_operations = payloads["benchmark_report"].get("operations")
    benchmark_operation_coverage = _dict(payloads["benchmark_report"].get("operation_coverage"))
    benchmark_threshold_evidence = _dict(
        payloads["benchmark_report"].get("runtime_threshold_evidence")
    )
    route_summary = _dict(payloads["route_inventory_report"].get("summary"))
    return {
        "artifact_count": len(EXPECTED_ARTIFACTS),
        "shadow_graph_counts": graph_counts,
        "boundary_checks_passed": boundary_summary.get("checks_passed"),
        "boundary_checks_total": boundary_summary.get("checks_total"),
        "benchmark_operations_passed": sum(
            1 for operation in _dict_list(benchmark_operations) if operation.get("ok") is True
        ),
        "benchmark_operations_total": len(_dict_list(benchmark_operations)),
        "benchmark_required_operations_present": benchmark_operation_coverage.get(
            "all_required_operations_present"
        ),
        "benchmark_runtime_threshold_disposition": benchmark_threshold_evidence.get("disposition"),
        "benchmark_declared_threshold_count": benchmark_threshold_evidence.get(
            "declared_threshold_count"
        ),
        "route_count": route_summary.get("route_count"),
        "preview_routes_present": route_summary.get("preview_routes_present"),
        "preview_routes_required": route_summary.get("preview_routes_required"),
        "resolver_route_policy": route_summary.get("resolver_route_policy", "absent"),
    }


def _validate_benchmark_operation_coverage(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    coverage = _dict(payload.get("operation_coverage"))
    if not coverage:
        return ["benchmark_report.operation_coverage: required"]
    required_operations = coverage.get("required_operations")
    if not isinstance(required_operations, list) or not all(
        isinstance(item, str) for item in required_operations
    ):
        errors.append("benchmark_report.operation_coverage.required_operations: expected string list")
    else:
        required_set = set(required_operations)
        expected_set = set(EXPECTED_BENCHMARK_OPERATION_NAMES)
        if required_set != expected_set:
            errors.append("benchmark_report.operation_coverage.required_operations: unexpected list")
        if len(required_operations) != len(required_set):
            errors.append("benchmark_report.operation_coverage.required_operations: duplicates found")
    if coverage.get("missing_required_operations") != []:
        errors.append("benchmark_report.operation_coverage.missing_required_operations: must be empty")
    if coverage.get("unexpected_operations") != []:
        errors.append("benchmark_report.operation_coverage.unexpected_operations: must be empty")
    if coverage.get("all_required_operations_present") is not True:
        errors.append("benchmark_report.operation_coverage.all_required_operations_present: must be true")
    if coverage.get("all_operations_ok") is not True:
        errors.append("benchmark_report.operation_coverage.all_operations_ok: must be true")
    operations = _dict_list(payload.get("operations"))
    if coverage.get("operations_total") != len(operations):
        errors.append("benchmark_report.operation_coverage.operations_total: must match operations")
    operations_passed = sum(1 for operation in operations if operation.get("ok") is True)
    if coverage.get("operations_passed") != operations_passed:
        errors.append("benchmark_report.operation_coverage.operations_passed: must match operations")
    return errors


def _validate_benchmark_runtime_threshold_evidence(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    threshold_evidence = _dict(payload.get("runtime_threshold_evidence"))
    if not threshold_evidence:
        return ["benchmark_report.runtime_threshold_evidence: required"]
    plan = _dict(payload.get("plan"))
    declared_commands = _string_list(plan.get("declared_commands"))
    declared_thresholds = _string_list(plan.get("declared_thresholds"))
    expected_future_runtime_commands = [
        command
        for command in declared_commands
        if command.strip().lower().startswith("future ")
    ]
    declared_command_count = len(declared_commands)
    declared_threshold_count = len(declared_thresholds)
    if threshold_evidence.get("declared_command_count") != declared_command_count:
        errors.append(
            "benchmark_report.runtime_threshold_evidence.declared_command_count: "
            "must match plan.declared_commands"
        )
    if threshold_evidence.get("declared_threshold_count") != declared_threshold_count:
        errors.append(
            "benchmark_report.runtime_threshold_evidence.declared_threshold_count: "
            "must match plan.declared_thresholds"
        )
    if threshold_evidence.get("declared_thresholds_evaluated") is not False:
        errors.append(
            "benchmark_report.runtime_threshold_evidence.declared_thresholds_evaluated: "
            "must be false"
        )
    if threshold_evidence.get("runtime_thresholds_evaluated") is not False:
        errors.append(
            "benchmark_report.runtime_threshold_evidence.runtime_thresholds_evaluated: "
            "must be false"
        )
    if threshold_evidence.get("disposition") != BENCHMARK_RUNTIME_THRESHOLD_DISPOSITION:
        errors.append("benchmark_report.runtime_threshold_evidence.disposition: unexpected value")
    future_runtime_commands = threshold_evidence.get("future_runtime_commands_declared")
    if not isinstance(future_runtime_commands, list) or not all(
        isinstance(item, str) for item in future_runtime_commands
    ):
        errors.append(
            "benchmark_report.runtime_threshold_evidence.future_runtime_commands_declared: "
            "expected string list"
        )
    elif future_runtime_commands != expected_future_runtime_commands:
        errors.append(
            "benchmark_report.runtime_threshold_evidence.future_runtime_commands_declared: "
            "must match future commands declared in plan.declared_commands"
        )
    if threshold_evidence.get("future_runtime_command_count") != len(
        expected_future_runtime_commands
    ):
        errors.append(
            "benchmark_report.runtime_threshold_evidence.future_runtime_command_count: "
            "must match future commands declared in plan.declared_commands"
        )
    blocked_scope = threshold_evidence.get("blocked_runtime_scope")
    if not isinstance(blocked_scope, list):
        errors.append(
            "benchmark_report.runtime_threshold_evidence.blocked_runtime_scope: expected list"
        )
    else:
        missing = [
            item for item in REQUIRED_BENCHMARK_BLOCKED_RUNTIME_SCOPE if item not in blocked_scope
        ]
        if missing:
            errors.append(
                "benchmark_report.runtime_threshold_evidence.blocked_runtime_scope: "
                f"missing {', '.join(missing)}"
            )
    return errors


def _expect_payload_path(
    errors: list[str],
    label: str,
    value: Any,
    expected: Any,
) -> None:
    if value != expected:
        errors.append(f"{label}: expected {expected!r}, got {value!r}")


def _load_json_object(path: Path, label: str) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"{label}: invalid JSON at line {exc.lineno}, column {exc.colno}") from exc
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
    run_id: str,
    output_path: Path | None,
) -> Path:
    candidate = output_path or (
        EVIDENCE_MANIFEST_REPORT_ROOT / run_id / EVIDENCE_MANIFEST_REPORT_FILENAME
    )
    report_path = candidate.resolve() if candidate.is_absolute() else (root / candidate).resolve()
    allowed_root = (root / EVIDENCE_MANIFEST_REPORT_ROOT).resolve()
    try:
        relative_parts = report_path.relative_to(allowed_root).parts
    except ValueError as exc:
        raise ValueError("report path must stay inside the evidence manifest report directory") from exc
    if len(relative_parts) != 2 or relative_parts[0] != run_id:
        raise ValueError("report path must be scoped to the current evidence manifest run id")
    if relative_parts[1] != EVIDENCE_MANIFEST_REPORT_FILENAME:
        raise ValueError(f"report filename must be {EVIDENCE_MANIFEST_REPORT_FILENAME}")
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


def _hash_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _relative_to_root(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _dict_list(value: Any) -> list[dict[str, Any]]:
    return [item for item in value if isinstance(item, dict)] if isinstance(value, list) else []


def _string_list(value: Any) -> list[str]:
    return [item for item in value if isinstance(item, str)] if isinstance(value, list) else []


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
