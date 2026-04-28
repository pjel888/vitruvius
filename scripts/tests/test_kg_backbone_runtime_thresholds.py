from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

import pytest

from vitruvius.kg.backbone_runtime_thresholds import (
    DEFAULT_THRESHOLDS_MS,
    REQUIRED_RUNTIME_SCOPE,
    REQUIRED_SAFETY_INVARIANTS,
    RUNTIME_THRESHOLD_REPORT_FILENAME,
    evaluate_runtime_thresholds,
)


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def _runtime_report() -> dict[str, Any]:
    return {
        "schemaVersion": "aec-mepfs-resolver-runtime-benchmark/v1",
        "ok": True,
        "runId": "TEST_THRESHOLDS",
        "benchmarkScope": {
            "defaultOnResolverRouteInvocation": True,
            "disabledRollbackRouteAbsent": True,
            "inProcessHonoFetch": True,
            "externalApiServerNetworkCalls": False,
            "neo4jQueries": False,
            "kgRebuild": False,
            "protectedContentIngest": False,
            "explorerRuntimeCalls": False,
            "featureFlagCutover": False,
            "runtimeThresholdsEvaluated": False,
        },
        "runtimeThresholdEvidence": {
            "evaluated": False,
            "passFailClaim": False,
            "disposition": "actual_default_on_route_harness_threshold_input_no_source_claim",
        },
        "environment": {
            "bunVersion": "1.3.0",
            "nodeVersion": "v25.0.0",
            "platform": "test-platform",
            "arch": "test-arch",
            "cpuCount": 8,
        },
        "plan": {
            "repetitions": 5,
            "warmup": 1,
            "percentiles": ["p50", "p95"],
            "corpus": "non-protected resolver golden fixtures",
        },
        "safetyInvariants": {
            "defaultOnRoutePresentOnDefaultImport": True,
            "disabledRollbackRouteAbsent": True,
            "guardedFlagRequired": False,
            "hiddenDefaultOnFeatureFlag": False,
            "explicitDefaultOnResolverPolicy": True,
            "fileBackedOnly": True,
            "protectedContentIngest": False,
            "liveNeo4jWrites": False,
            "kgRebuild": False,
            "explorerDefaultAdoption": False,
            "externalApiServerNetworkCalls": False,
            "runtimeThresholdsEvaluated": False,
            "runtimeThresholdClaim": False,
        },
        "operations": [
            {"name": name, "ok": True, "p95Ms": 12.5, "errors": []}
            for name in DEFAULT_THRESHOLDS_MS
        ],
    }


def _write_runtime_report(tmp_path: Path, payload: dict[str, Any] | None = None) -> Path:
    report_path = (
        tmp_path
        / "006_System-Manifests"
        / "aec-mepfs-backbone"
        / "runtime-resolver-benchmark"
        / "TEST_THRESHOLDS"
        / "runtime-resolver-benchmark-report.json"
    )
    _write_json(report_path, payload or _runtime_report())
    return report_path


def test_runtime_threshold_evaluator_writes_pass_fail_claim_for_actual_runtime_report(tmp_path: Path) -> None:
    source_path = _write_runtime_report(tmp_path)

    report = evaluate_runtime_thresholds(
        source_path.relative_to(tmp_path),
        repo_root=tmp_path,
        run_id="TEST_THRESHOLDS",
    )

    saved_path = (
        tmp_path
        / "006_System-Manifests"
        / "aec-mepfs-backbone"
        / "runtime-thresholds"
        / "TEST_THRESHOLDS"
        / RUNTIME_THRESHOLD_REPORT_FILENAME
    )
    saved = json.loads(saved_path.read_text(encoding="utf-8"))
    assert saved == report
    assert report["ok"] is True
    assert report["passFailClaim"] is True
    assert report["pass_fail_claim"] is True
    assert report["pass_fail_status"] == "passed"
    assert report["adoption_scope"] == "default_on_file_backed_api_resolver_runtime"
    assert report["implemented_api_runtime_thresholds_adopted"] is True
    assert report["overall_aec_runtime_thresholds_adopted"] is False
    assert report["remaining_threshold_surfaces"] == [
        "external_api_server_p95",
        "explorer_browser_runtime_p95",
        "neo4j_live_graph_p95",
        "production_live_graph_p95",
    ]
    assert report["summary"] == {
        "all_thresholds_evaluated": True,
        "all_thresholds_passed": True,
        "evidence_gate_passed": True,
        "thresholds_evaluated": 6,
        "thresholds_failed": 0,
        "thresholds_passed": 6,
        "thresholds_total": 6,
    }
    assert report["threshold_policy"]["declared_before_final_measurement"] is True
    assert report["safety_invariants"] == {
        "disabledRollbackRouteAbsent": True,
        "explicitDefaultOnResolverPolicy": True,
        "explorerDefaultAdoption": False,
        "externalApiServerNetworkCalls": False,
        "hiddenDefaultOnFeatureFlag": False,
        "kgRebuild": False,
        "neo4jQueries": False,
        "neo4jWrites": False,
        "protectedContentIngest": False,
        "shadowOnlyEvidenceRejected": True,
        "sourceActualRuntimeHarness": True,
    }


def test_runtime_threshold_evaluator_rejects_shadow_only_benchmark_schema(tmp_path: Path) -> None:
    payload = _runtime_report()
    payload["schemaVersion"] = "aec-bb-shadow-benchmark-report/v1"
    source_path = _write_runtime_report(tmp_path, payload)

    report = evaluate_runtime_thresholds(source_path.relative_to(tmp_path), repo_root=tmp_path)

    assert report["ok"] is False
    assert report["passFailClaim"] is False
    assert report["pass_fail_claim"] is False
    assert any("schemaVersion" in error for error in report["errors"])


def test_runtime_threshold_evaluator_fails_closed_for_unsafe_scope(tmp_path: Path) -> None:
    payload = _runtime_report()
    payload["benchmarkScope"]["externalApiServerNetworkCalls"] = True
    payload["safetyInvariants"]["externalApiServerNetworkCalls"] = True
    source_path = _write_runtime_report(tmp_path, payload)

    report = evaluate_runtime_thresholds(source_path.relative_to(tmp_path), repo_root=tmp_path)

    assert report["ok"] is False
    assert report["passFailClaim"] is False
    assert report["pass_fail_claim"] is False
    assert report["summary"]["evidence_gate_passed"] is False
    assert report["criteria"]["runtime_scope_checks"]["externalApiServerNetworkCalls"] == {
        "actual": True,
        "expected": False,
        "passed": False,
    }
    assert report["criteria"]["safety_invariant_checks"]["externalApiServerNetworkCalls"] == {
        "actual": True,
        "expected": False,
        "passed": False,
    }
    assert any("externalApiServerNetworkCalls" in error for error in report["errors"])


def test_runtime_threshold_evaluator_records_threshold_failure(tmp_path: Path) -> None:
    payload = _runtime_report()
    payload["operations"][1]["p95Ms"] = 101.0
    source_path = _write_runtime_report(tmp_path, payload)

    report = evaluate_runtime_thresholds(source_path.relative_to(tmp_path), repo_root=tmp_path)

    assert report["ok"] is False
    assert report["passFailClaim"] is True
    assert report["pass_fail_claim"] is True
    assert report["pass_fail_status"] == "failed"
    failed = [item for item in report["threshold_results"] if not item["passed"]]
    assert failed == [
        {
            "metric": "p95Ms",
            "observed_ms": 101.0,
            "operation": "default_on_single_value_resolve",
            "passed": False,
            "threshold_ms": 100.0,
        }
    ]


def test_runtime_threshold_evaluator_fails_when_required_operation_is_missing(tmp_path: Path) -> None:
    payload = _runtime_report()
    payload["operations"] = payload["operations"][:-1]
    source_path = _write_runtime_report(tmp_path, payload)

    report = evaluate_runtime_thresholds(source_path.relative_to(tmp_path), repo_root=tmp_path)

    assert report["ok"] is False
    assert report["passFailClaim"] is False
    assert report["passFailClaim"] is False
    assert report["pass_fail_claim"] is False
    assert report["summary"]["all_thresholds_evaluated"] is False
    assert any("default_on_trace_lookup" in error for error in report["errors"])


def test_runtime_threshold_evaluator_rejects_unsafe_run_id(tmp_path: Path) -> None:
    source_path = _write_runtime_report(tmp_path)

    with pytest.raises(ValueError, match="run_id must contain only"):
        evaluate_runtime_thresholds(source_path.relative_to(tmp_path), repo_root=tmp_path, run_id="../unsafe")


def test_runtime_threshold_evaluator_rejects_output_outside_threshold_root(tmp_path: Path) -> None:
    source_path = _write_runtime_report(tmp_path)

    with pytest.raises(ValueError, match="runtime-thresholds evidence directory"):
        evaluate_runtime_thresholds(
            source_path.relative_to(tmp_path),
            repo_root=tmp_path,
            run_id="TEST_THRESHOLDS",
            output_path=Path("outside.json"),
        )


def test_runtime_threshold_evaluator_does_not_mutate_input_report(tmp_path: Path) -> None:
    payload = _runtime_report()
    original = copy.deepcopy(payload)
    source_path = _write_runtime_report(tmp_path, payload)

    evaluate_runtime_thresholds(source_path.relative_to(tmp_path), repo_root=tmp_path)

    assert json.loads(source_path.read_text(encoding="utf-8")) == original


@pytest.mark.parametrize("scope_key, expected", sorted(REQUIRED_RUNTIME_SCOPE.items()))
def test_runtime_threshold_evaluator_fails_closed_for_every_runtime_scope_violation(
    tmp_path: Path,
    scope_key: str,
    expected: bool,
) -> None:
    payload = _runtime_report()
    payload["benchmarkScope"][scope_key] = not expected
    source_path = _write_runtime_report(tmp_path, payload)

    report = evaluate_runtime_thresholds(source_path.relative_to(tmp_path), repo_root=tmp_path)

    assert report["ok"] is False
    assert report["passFailClaim"] is False
    assert report["pass_fail_claim"] is False
    assert report["summary"]["evidence_gate_passed"] is False
    assert report["criteria"]["runtime_scope_checks"][scope_key] == {
        "actual": not expected,
        "expected": expected,
        "passed": False,
    }


@pytest.mark.parametrize("invariant_key, expected", sorted(REQUIRED_SAFETY_INVARIANTS.items()))
def test_runtime_threshold_evaluator_fails_closed_for_every_safety_invariant_violation(
    tmp_path: Path,
    invariant_key: str,
    expected: bool,
) -> None:
    payload = _runtime_report()
    payload["safetyInvariants"][invariant_key] = not expected
    source_path = _write_runtime_report(tmp_path, payload)

    report = evaluate_runtime_thresholds(source_path.relative_to(tmp_path), repo_root=tmp_path)

    assert report["ok"] is False
    assert report["passFailClaim"] is False
    assert report["pass_fail_claim"] is False
    assert report["summary"]["evidence_gate_passed"] is False
    assert report["criteria"]["safety_invariant_checks"][invariant_key] == {
        "actual": not expected,
        "expected": expected,
        "passed": False,
    }


def test_runtime_threshold_evaluator_fails_closed_when_runtime_report_not_ok(tmp_path: Path) -> None:
    payload = _runtime_report()
    payload["ok"] = False
    source_path = _write_runtime_report(tmp_path, payload)

    report = evaluate_runtime_thresholds(source_path.relative_to(tmp_path), repo_root=tmp_path)

    assert report["ok"] is False
    assert report["passFailClaim"] is False
    assert any("ok=true" in error for error in report["errors"])


@pytest.mark.parametrize(
    "plan_mutation, expected_error",
    [
        (lambda plan: plan.__setitem__("corpus", ""), "plan.corpus"),
        (lambda plan: plan.__setitem__("repetitions", 2), "plan.repetitions"),
        (lambda plan: plan.__setitem__("warmup", -1), "plan.warmup"),
        (lambda plan: plan.__setitem__("percentiles", ["p95"]), "plan.percentiles"),
    ],
)
def test_runtime_threshold_evaluator_fails_closed_for_invalid_plan_fields(
    tmp_path: Path,
    plan_mutation: Any,
    expected_error: str,
) -> None:
    payload = _runtime_report()
    plan_mutation(payload["plan"])
    source_path = _write_runtime_report(tmp_path, payload)

    report = evaluate_runtime_thresholds(source_path.relative_to(tmp_path), repo_root=tmp_path)

    assert report["ok"] is False
    assert report["passFailClaim"] is False
    assert report["summary"]["evidence_gate_passed"] is False
    assert any(expected_error in error for error in report["errors"])


def test_runtime_threshold_evaluator_fails_closed_for_missing_environment(tmp_path: Path) -> None:
    payload = _runtime_report()
    payload["environment"] = {}
    source_path = _write_runtime_report(tmp_path, payload)

    report = evaluate_runtime_thresholds(source_path.relative_to(tmp_path), repo_root=tmp_path)

    assert report["ok"] is False
    assert report["passFailClaim"] is False
    assert report["criteria"]["runtime_environment_captured"] is False
    assert any("environment" in error for error in report["errors"])


def test_runtime_threshold_evaluator_fails_closed_for_failed_operation(tmp_path: Path) -> None:
    payload = _runtime_report()
    payload["operations"][0]["ok"] = False
    source_path = _write_runtime_report(tmp_path, payload)

    report = evaluate_runtime_thresholds(source_path.relative_to(tmp_path), repo_root=tmp_path)

    assert report["ok"] is False
    assert report["passFailClaim"] is False
    assert any("benchmark operation was not ok" in error for error in report["errors"])


def test_runtime_threshold_evaluator_fails_closed_for_non_numeric_p95(tmp_path: Path) -> None:
    payload = _runtime_report()
    payload["operations"][0]["p95Ms"] = "fast"
    source_path = _write_runtime_report(tmp_path, payload)

    report = evaluate_runtime_thresholds(source_path.relative_to(tmp_path), repo_root=tmp_path)

    assert report["ok"] is False
    assert report["passFailClaim"] is False
    assert any("p95Ms must be numeric" in error for error in report["errors"])


def test_runtime_threshold_evaluator_fails_closed_for_missing_scope_and_invariants(tmp_path: Path) -> None:
    payload = _runtime_report()
    payload.pop("benchmarkScope")
    payload.pop("safetyInvariants")
    source_path = _write_runtime_report(tmp_path, payload)

    report = evaluate_runtime_thresholds(source_path.relative_to(tmp_path), repo_root=tmp_path)

    assert report["ok"] is False
    assert report["passFailClaim"] is False
    assert any("benchmarkScope" in error for error in report["errors"])
    assert any("safetyInvariants" in error for error in report["errors"])


def test_runtime_threshold_evaluator_rejects_source_path_outside_repo_root(tmp_path: Path) -> None:
    outside = tmp_path.parent / f"outside-runtime-report-{tmp_path.name}.json"
    try:
        _write_json(outside, _runtime_report())
        with pytest.raises(ValueError, match="runtime benchmark report path must stay inside repo root"):
            evaluate_runtime_thresholds(outside, repo_root=tmp_path)
    finally:
        outside.unlink(missing_ok=True)
