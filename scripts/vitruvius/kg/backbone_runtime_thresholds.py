"""Runtime threshold evaluator for the AEC-MEPFS resolver runtime harness.

This module consumes the API-local runtime resolver benchmark report and emits a
separate threshold-adoption report. It intentionally rejects shadow-only
benchmark evidence and never calls Neo4j, rebuilds the KG, ingests protected
content, or changes Explorer defaults.
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import re
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence


REPORT_SCHEMA_VERSION = "aec-mepfs-runtime-threshold-adoption/v1"
RUNTIME_BENCHMARK_SCHEMA_VERSION = "aec-mepfs-resolver-runtime-benchmark/v1"
RUNTIME_THRESHOLD_REPORT_ROOT = Path(
    "006_System-Manifests/aec-mepfs-backbone/runtime-thresholds"
)
RUNTIME_THRESHOLD_REPORT_FILENAME = "runtime-threshold-adoption-report.json"
RUN_ID_RE = re.compile(r"^[A-Za-z0-9_.-]+$")

DEFAULT_THRESHOLDS_MS: Mapping[str, float] = {
    "disabled_resolve_absent": 100.0,
    "default_on_single_value_resolve": 100.0,
    "default_on_composed_resolve": 250.0,
    "default_on_conflict_resolve": 250.0,
    "default_on_none_resolve": 250.0,
    "default_on_trace_lookup": 250.0,
}

REQUIRED_RUNTIME_SCOPE = {
    "defaultOnResolverRouteInvocation": True,
    "disabledRollbackRouteAbsent": True,
    "inProcessHonoFetch": True,
    "externalApiServerNetworkCalls": False,
    "neo4jQueries": False,
    "kgRebuild": False,
    "protectedContentIngest": False,
    "explorerRuntimeCalls": False,
    "featureFlagCutover": False,
}

REQUIRED_SAFETY_INVARIANTS = {
    "guardedFlagRequired": False,
    "hiddenDefaultOnFeatureFlag": False,
    "explicitDefaultOnResolverPolicy": True,
    "disabledRollbackRouteAbsent": True,
    "protectedContentIngest": False,
    "liveNeo4jWrites": False,
    "kgRebuild": False,
    "explorerDefaultAdoption": False,
    "externalApiServerNetworkCalls": False,
}


def evaluate_runtime_thresholds(
    runtime_benchmark_report: str | Path,
    *,
    repo_root: str | Path | None = None,
    run_id: str | None = None,
    output_path: str | Path | None = None,
    thresholds_ms: Mapping[str, float] = DEFAULT_THRESHOLDS_MS,
) -> dict[str, Any]:
    """Evaluate p95 thresholds from an actual runtime resolver benchmark report."""

    root = _repo_root(repo_root)
    source_path = _resolve_existing_file(root, Path(runtime_benchmark_report), "runtime benchmark report")
    source = _load_json_object(source_path, "runtime benchmark report")
    resolved_run_id = _run_id(run_id or _string_or_none(source.get("runId")))
    report_path = _resolve_report_path(root, resolved_run_id, Path(output_path) if output_path else None)

    errors: list[str] = []
    threshold_failures: list[str] = []
    warnings: list[str] = []
    criteria = _criteria(source, thresholds_ms, errors, warnings)
    threshold_results = _threshold_results(source, thresholds_ms, errors, threshold_failures)
    operations_passed = sum(1 for item in threshold_results if item["passed"] is True)
    all_thresholds_evaluated = len(threshold_results) == len(thresholds_ms)
    all_thresholds_passed = all_thresholds_evaluated and operations_passed == len(threshold_results)
    evidence_gate_passed = not errors
    pass_fail_claim = (
        criteria["source_is_runtime_benchmark"]
        and evidence_gate_passed
        and all_thresholds_evaluated
    )

    report = {
        "schema_version": REPORT_SCHEMA_VERSION,
        "ok": not errors and all_thresholds_passed,
        "run_id": resolved_run_id,
        "generated_at_utc": _utc_now(),
        "report_path": _relative_to_root(report_path, root),
        "runtime_benchmark_report_path": _relative_to_root(source_path, root),
        "authority": {
            "packet": ".ai/03_plans/AEC-MEPFS-Backbone/2026-04-27_actual_aec_mepfs_implementation_cutover_packet.md",
            "scope": "default_on_file_backed_api_resolver_runtime",
            "global_live_authorization": False,
        },
        "threshold_policy": {
            "declared_before_final_measurement": True,
            "percentile": "p95Ms",
            "thresholds_ms": dict(thresholds_ms),
            "corpus": _get(source, ["plan", "corpus"]),
            "warmup": _get(source, ["plan", "warmup"]),
            "repetitions": _get(source, ["plan", "repetitions"]),
        },
        "passFailClaim": pass_fail_claim,
        "pass_fail_claim": pass_fail_claim,
        "pass_fail_status": "passed" if all_thresholds_passed else "failed",
        "adoption_scope": "default_on_file_backed_api_resolver_runtime",
        "implemented_api_runtime_thresholds_adopted": pass_fail_claim and all_thresholds_passed,
        "overall_aec_runtime_thresholds_adopted": False,
        "remaining_threshold_surfaces": [
            "external_api_server_p95",
            "explorer_browser_runtime_p95",
            "neo4j_live_graph_p95",
            "production_live_graph_p95",
        ],
        "criteria": criteria,
        "threshold_results": threshold_results,
        "summary": {
            "thresholds_total": len(thresholds_ms),
            "thresholds_evaluated": len(threshold_results),
            "thresholds_passed": operations_passed,
            "thresholds_failed": len(threshold_results) - operations_passed,
            "evidence_gate_passed": evidence_gate_passed,
            "all_thresholds_evaluated": all_thresholds_evaluated,
            "all_thresholds_passed": all_thresholds_passed,
        },
        "runtime_environment": source.get("environment") if isinstance(source.get("environment"), dict) else {},
        "baseline_policy": {
            "hardware_runtime_baseline_captured": criteria["runtime_environment_captured"],
            "baseline_limitations": [
                "API-local in-process Hono harness over default-on /v2/resolve only",
                "No external API server load test",
                "No Neo4j-backed or Explorer runtime measurement",
                "No protected-source corpus",
            ],
        },
        "evaluator_environment": {
            "python_version": platform.python_version(),
            "platform": platform.platform(),
            "cpu_count": os.cpu_count(),
        },
        "safety_invariants": {
            "sourceActualRuntimeHarness": criteria["source_is_runtime_benchmark"],
            "shadowOnlyEvidenceRejected": criteria["source_is_runtime_benchmark"],
            "neo4jQueries": False,
            "neo4jWrites": False,
            "kgRebuild": False,
            "protectedContentIngest": False,
            "explorerDefaultAdoption": False,
            "hiddenDefaultOnFeatureFlag": False,
            "explicitDefaultOnResolverPolicy": True,
            "disabledRollbackRouteAbsent": (
                criteria["safety_invariant_checks"]
                .get("disabledRollbackRouteAbsent", {})
                .get("passed")
                is True
            ),
            "externalApiServerNetworkCalls": False,
        },
        "errors": sorted(set(errors + threshold_failures)),
        "warnings": sorted(set(warnings)),
    }
    _write_json(report_path, report)
    return report


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Evaluate guarded AEC-MEPFS resolver runtime threshold evidence."
    )
    parser.add_argument("--runtime-benchmark-report", required=True)
    parser.add_argument("--repo-root", default=None)
    parser.add_argument("--run-id", default=None)
    parser.add_argument("--output", default=None)
    args = parser.parse_args(argv)

    try:
        report = evaluate_runtime_thresholds(
            args.runtime_benchmark_report,
            repo_root=args.repo_root,
            run_id=args.run_id,
            output_path=args.output,
        )
    except (FileNotFoundError, ValueError) as exc:
        print(json.dumps({"ok": False, "errors": [str(exc)]}, indent=2, sort_keys=True))
        return 1

    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["ok"] else 1


def _criteria(
    source: dict[str, Any],
    thresholds_ms: Mapping[str, float],
    errors: list[str],
    warnings: list[str],
) -> dict[str, Any]:
    schema = source.get("schemaVersion")
    source_is_runtime_benchmark = schema == RUNTIME_BENCHMARK_SCHEMA_VERSION
    if not source_is_runtime_benchmark:
        errors.append(
            f"runtime benchmark report schemaVersion must be {RUNTIME_BENCHMARK_SCHEMA_VERSION}"
        )

    runtime_report_ok = source.get("ok") is True
    if not runtime_report_ok:
        errors.append("runtime benchmark report must be ok=true")

    scope = source.get("benchmarkScope") if isinstance(source.get("benchmarkScope"), dict) else {}
    scope_checks: dict[str, dict[str, Any]] = {}
    for key, expected in REQUIRED_RUNTIME_SCOPE.items():
        actual = scope.get(key)
        passed = actual is expected
        scope_checks[key] = {"expected": expected, "actual": actual, "passed": passed}
        if not passed:
            errors.append(f"benchmarkScope.{key}: expected {expected!r}")

    invariants = source.get("safetyInvariants") if isinstance(source.get("safetyInvariants"), dict) else {}
    invariant_checks: dict[str, dict[str, Any]] = {}
    for key, expected in REQUIRED_SAFETY_INVARIANTS.items():
        actual = invariants.get(key)
        passed = actual is expected
        invariant_checks[key] = {"expected": expected, "actual": actual, "passed": passed}
        if not passed:
            errors.append(f"safetyInvariants.{key}: expected {expected!r}")

    plan = source.get("plan") if isinstance(source.get("plan"), dict) else {}
    corpus_fixed = isinstance(plan.get("corpus"), str) and bool(plan.get("corpus"))
    repetitions_declared = isinstance(plan.get("repetitions"), int) and plan.get("repetitions") >= 3
    warmup_declared = isinstance(plan.get("warmup"), int) and plan.get("warmup") >= 0
    percentiles_declared = plan.get("percentiles") == ["p50", "p95"]
    if not corpus_fixed:
        errors.append("plan.corpus must identify the fixed non-protected corpus")
    if not repetitions_declared:
        errors.append("plan.repetitions must be an integer >= 3")
    if not warmup_declared:
        errors.append("plan.warmup must be a non-negative integer")
    if not percentiles_declared:
        errors.append("plan.percentiles must be ['p50', 'p95']")

    environment = source.get("environment") if isinstance(source.get("environment"), dict) else {}
    runtime_environment_captured = any(environment.get(key) for key in ("bunVersion", "nodeVersion", "platform", "arch"))
    if not runtime_environment_captured:
        errors.append("environment must capture runtime platform details")

    threshold_values_valid = all(value >= 0 for value in thresholds_ms.values())
    if not threshold_values_valid:
        errors.append("threshold values must be non-negative")

    if _get(source, ["runtimeThresholdEvidence", "passFailClaim"]) is True:
        warnings.append("source runtime benchmark already claimed thresholds; evaluator treats it as input only")

    return {
        "source_is_runtime_benchmark": source_is_runtime_benchmark,
        "runtime_report_ok": runtime_report_ok,
        "runtime_scope_checks": scope_checks,
        "safety_invariant_checks": invariant_checks,
        "fixed_corpus_present": corpus_fixed,
        "repetitions_declared": repetitions_declared,
        "warmup_declared": warmup_declared,
        "percentiles_declared": percentiles_declared,
        "runtime_environment_captured": runtime_environment_captured,
        "thresholds_declared": True,
        "threshold_values_valid": threshold_values_valid,
    }


def _threshold_results(
    source: dict[str, Any],
    thresholds_ms: Mapping[str, float],
    errors: list[str],
    threshold_failures: list[str],
) -> list[dict[str, Any]]:
    raw_operations = source.get("operations")
    operations = raw_operations if isinstance(raw_operations, list) else []
    by_name: dict[str, dict[str, Any]] = {
        item["name"]: item
        for item in operations
        if isinstance(item, dict) and isinstance(item.get("name"), str)
    }
    results: list[dict[str, Any]] = []
    for operation_name, threshold_ms in thresholds_ms.items():
        operation = by_name.get(operation_name)
        if operation is None:
            errors.append(f"operation {operation_name}: missing from runtime benchmark report")
            continue
        p95 = operation.get("p95Ms")
        if not isinstance(p95, (int, float)):
            errors.append(f"operation {operation_name}: p95Ms must be numeric")
            continue
        operation_ok = operation.get("ok") is True
        passed = operation_ok and float(p95) <= threshold_ms
        if not operation_ok:
            errors.append(f"operation {operation_name}: benchmark operation was not ok")
        if float(p95) > threshold_ms:
            threshold_failures.append(
                f"operation {operation_name}: p95Ms {float(p95):.6f} exceeds threshold {threshold_ms:.6f}"
            )
        results.append(
            {
                "operation": operation_name,
                "metric": "p95Ms",
                "observed_ms": float(p95),
                "threshold_ms": threshold_ms,
                "passed": passed,
            }
        )
    return results


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


def _resolve_report_path(root: Path, run_id: str, output_path: Path | None) -> Path:
    candidate = output_path or (RUNTIME_THRESHOLD_REPORT_ROOT / run_id / RUNTIME_THRESHOLD_REPORT_FILENAME)
    report_path = candidate.resolve() if candidate.is_absolute() else (root / candidate).resolve()
    allowed_root = (root / RUNTIME_THRESHOLD_REPORT_ROOT).resolve()
    try:
        relative_parts = report_path.relative_to(allowed_root).parts
    except ValueError as exc:
        raise ValueError("report path must stay inside the runtime-thresholds evidence directory") from exc
    if len(relative_parts) != 2 or relative_parts[0] != run_id:
        raise ValueError("report path must be scoped to the current threshold run id")
    if relative_parts[1] != RUNTIME_THRESHOLD_REPORT_FILENAME:
        raise ValueError(f"report filename must be {RUNTIME_THRESHOLD_REPORT_FILENAME}")
    return report_path


def _run_id(value: str | None) -> str:
    candidate = value or datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    if not RUN_ID_RE.fullmatch(candidate):
        raise ValueError("run_id must contain only letters, digits, underscore, dot, or dash")
    return candidate


def _load_json_object(path: Path, label: str) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{label}: expected a JSON object")
    return payload


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _relative_to_root(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def _string_or_none(value: Any) -> str | None:
    return value if isinstance(value, str) else None


def _get(payload: dict[str, Any], path: Sequence[str]) -> Any:
    current: Any = payload
    for key in path:
        if not isinstance(current, dict):
            return None
        current = current.get(key)
    return current


def _utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
