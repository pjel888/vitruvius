"""File-backed resolver QA runner for AEC-MEPFS Backbone readiness.

This runner checks resolver golden cases from the readiness fixture. It is
intentionally runtime-disconnected: it reads JSON fixtures, writes an auditable
report, and does not call the live resolver, Neo4j, graph rebuilds, feature
flags, API routes, Explorer code, or LLMs.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Sequence

from vitruvius.kg.backbone_api_route_inventory import (
    summarize_resolver_route_boundary,
    summarize_shadow_preview_route_boundaries,
)
from vitruvius.kg.backbone_contracts import validate_backbone_contract_file


REPORT_SCHEMA_VERSION = "aec-bb-resolver-qa-report/v1"
DEFAULT_FIXTURE_PATH = Path(
    "scripts/tests/fixtures/aec_mepfs_backbone/valid_readiness_s2.json"
)
RESOLVER_QA_REPORT_ROOT = Path("006_System-Manifests/aec-mepfs-backbone/resolver-qa")
RESOLVER_QA_REPORT_FILENAME = "resolver-qa-report.json"
API_INDEX_PATH = Path("api/index.ts")
RUN_ID_RE = re.compile(r"^[A-Za-z0-9_.-]+$")
RESOLVER_RESULT_TYPES = {"single_value", "composed", "conflict", "none"}
RESOLVER_ERROR_TYPES = {
    "blocked_runtime_route",
    "deterministic_no_result",
    "invalid_input",
    "malformed_request",
    "missing_fixture_artifact",
}
REQUIRED_COVERAGE_KEYS = {
    "case_id_present",
    "composed_compatible_rationale",
    "single_value_deterministic",
    "composed_deterministic",
    "conflict_incompatible_rationale",
    "conflict_review_required",
    "effective_date_present",
    "jurisdiction_present",
    "none_absence_rationale",
    "none_insufficient",
    "expected_node_refs_present",
    "fallback_reason_present",
    "query_context_ids_static_contract",
    "query_discipline_filters_static_contract",
    "query_asset_context_present",
    "query_text_present",
    "trace_requested_boolean",
    "trace_safe_rationale_present",
    "source_evidence_traceable",
}
REQUIRED_ERROR_COVERAGE_KEYS = {
    "blocked_runtime_route_case_present",
    "deterministic_no_result_case_present",
    "invalid_input_case_present",
    "malformed_request_case_present",
    "missing_fixture_artifact_case_present",
}


def run_resolver_qa_fixture(
    fixture_path: str | Path = DEFAULT_FIXTURE_PATH,
    *,
    repo_root: str | Path | None = None,
    run_id: str | None = None,
    output_path: str | Path | None = None,
) -> dict[str, Any]:
    """Run file-backed resolver golden-case checks and write a JSON report."""
    root = _repo_root(repo_root)
    fixture = _resolve_existing_file(root, Path(fixture_path))
    resolved_run_id = _run_id(run_id)
    started_at = _utc_now()

    contract_report = validate_backbone_contract_file(fixture)
    payload = _load_payload(fixture)
    report_path = _resolve_report_path(
        root=root,
        run_id=resolved_run_id,
        output_path=Path(output_path) if output_path is not None else None,
    )

    errors = list(contract_report.errors)
    warnings = list(contract_report.warnings)
    case_results: list[dict[str, Any]] = []
    error_case_results: list[dict[str, Any]] = []
    summary = _empty_summary()
    error_summary = _empty_error_summary()
    api_route_status = _check_resolver_route_boundary(root)
    preview_route_status = _check_preview_route_boundary(root)

    if api_route_status["resolveRouteMounted"] or api_route_status["traceRouteMounted"]:
        errors.append("resolver API route boundary: /v2/resolve routes must remain unmounted")

    if contract_report.ok:
        cases = _dict_list(payload.get("resolver_golden_cases"))
        if not cases:
            errors.append("resolver_golden_cases: expected at least one resolver QA case")
        else:
            case_results = [_evaluate_resolver_case(case) for case in cases]
            summary = _summarize_case_results(case_results)
            for result in case_results:
                if not result["passed"]:
                    errors.extend(
                        f"{result['case_id']}: {error}" for error in result["errors"]
                    )
            missing_coverage = sorted(
                key for key, present in summary["required_coverage"].items() if not present
            )
            if missing_coverage:
                errors.append(
                    "resolver_golden_cases: missing required resolver QA coverage "
                    f"({', '.join(missing_coverage)})"
                )

        error_cases = _dict_list(payload.get("resolver_error_cases"))
        if not error_cases:
            errors.append("resolver_error_cases: expected static resolver error contract cases")
        else:
            error_case_results = [_evaluate_resolver_error_case(case) for case in error_cases]
            error_summary = _summarize_error_case_results(error_case_results)
            for result in error_case_results:
                if not result["passed"]:
                    errors.extend(
                        f"{result['case_id']}: {error}" for error in result["errors"]
                    )
            missing_error_coverage = sorted(
                key
                for key, present in error_summary["required_coverage"].items()
                if not present
            )
            if missing_error_coverage:
                errors.append(
                    "resolver_error_cases: missing required static error coverage "
                    f"({', '.join(missing_error_coverage)})"
                )
    else:
        warnings.append("resolver QA skipped because readiness fixture failed validation")

    contract_surface = _contract_surface_summary(summary, error_summary, preview_route_status)

    finished_at = _utc_now()
    report = {
        "schema_version": REPORT_SCHEMA_VERSION,
        "ok": not errors,
        "run_id": resolved_run_id,
        "started_at_utc": started_at,
        "finished_at_utc": finished_at,
        "fixture_path": _relative_to_root(fixture, root),
        "report_path": _relative_to_root(report_path, root),
        "contract_validation": {
            "ok": contract_report.ok,
            "errors": contract_report.errors,
            "warnings": contract_report.warnings,
        },
        "summary": summary,
        "error_summary": error_summary,
        "contract_surface": contract_surface,
        "required_coverage_keys": sorted(REQUIRED_COVERAGE_KEYS),
        "required_error_coverage_keys": sorted(REQUIRED_ERROR_COVERAGE_KEYS),
        "api_route_status": api_route_status,
        "preview_route_status": preview_route_status,
        "safety_boundaries": {
            "shadow_only": True,
            "file_backed_only": True,
            "live_resolver_invocation": False,
            "llm_hot_path": False,
            "live_neo4j_writes": False,
            "kg_rebuild": False,
            "feature_flag_cutover": False,
            "explorer_default_adoption": False,
            "protected_content_ingest": False,
            "canonical_content_admission": False,
        },
        "errors": sorted(set(errors)),
        "warnings": sorted(set(warnings)),
        "case_results": case_results,
        "error_case_results": error_case_results,
    }
    _write_json(report_path, report)
    return report


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run AEC-MEPFS Backbone resolver golden-case QA checks."
    )
    parser.add_argument("--fixture", default=str(DEFAULT_FIXTURE_PATH))
    parser.add_argument("--repo-root", default=None)
    parser.add_argument("--run-id", default=None)
    parser.add_argument("--output", default=None)
    args = parser.parse_args(argv)

    try:
        report = run_resolver_qa_fixture(
            args.fixture,
            repo_root=args.repo_root,
            run_id=args.run_id,
            output_path=args.output,
        )
    except (FileNotFoundError, ValueError) as exc:
        print(json.dumps({"ok": False, "errors": [str(exc)]}, indent=2, sort_keys=True))
        return 1

    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["ok"] else 1


def _evaluate_resolver_case(case: dict[str, Any]) -> dict[str, Any]:
    case_id = str(case.get("case_id", "")).strip()
    result_type = str(case.get("expected_result_type", "")).strip()
    confidence = str(case.get("expected_confidence", "")).strip()
    query = case.get("query") if isinstance(case.get("query"), dict) else {}
    source_evidence = case.get("source_evidence") if isinstance(case.get("source_evidence"), list) else []
    rationale = str(case.get("rationale", "")).strip().lower()
    fallback_reason = str(case.get("fallback_reason", "")).strip()
    trace_safe_rationale = str(case.get("trace_safe_rationale", "")).strip()
    jurisdiction = str(case.get("jurisdiction", "")).strip()
    effective_date = str(case.get("effective_date", "")).strip()
    asset_context = str(query.get("asset_context", "")).strip()
    query_text = str(query.get("text", "")).strip()
    context_ids = query.get("context_ids")
    discipline_filters = query.get("discipline_filters")
    trace_requested = query.get("trace_requested")
    expected_node_refs = case.get("expected_node_refs")
    source_evidence_ids = [str(item).strip() for item in source_evidence]

    errors: list[str] = []
    checks: list[str] = []

    if case_id:
        checks.append("case_id_present")
    else:
        errors.append("resolver golden cases must identify a case_id")

    if result_type not in RESOLVER_RESULT_TYPES:
        errors.append(f"unsupported resolver result type: {result_type}")

    if not query.get("concept_id"):
        errors.append("resolver golden cases must identify a concept_id")
    if query_text:
        checks.append("query_text_present")
    else:
        errors.append("resolver golden cases must identify query.text")
    if asset_context:
        checks.append("query_asset_context_present")
    else:
        errors.append("resolver golden cases must identify query.asset_context")
    if isinstance(context_ids, list) and all(isinstance(item, str) for item in context_ids):
        checks.append("query_context_ids_static_contract")
    elif context_ids is not None:
        errors.append("resolver golden cases query.context_ids must be a list of IDs")
    if isinstance(discipline_filters, list) and all(
        isinstance(item, str) for item in discipline_filters
    ):
        checks.append("query_discipline_filters_static_contract")
    elif discipline_filters is not None:
        errors.append("resolver golden cases query.discipline_filters must be a list")
    if isinstance(trace_requested, bool):
        checks.append("trace_requested_boolean")
    elif trace_requested is not None:
        errors.append("resolver golden cases query.trace_requested must be boolean")

    if jurisdiction:
        checks.append("jurisdiction_present")
    else:
        errors.append("resolver golden cases must identify a jurisdiction")

    if effective_date:
        checks.append("effective_date_present")
    else:
        errors.append("resolver golden cases must identify an effective_date")

    if not source_evidence:
        errors.append("resolver golden cases must carry source_evidence")
    elif all(source_evidence_ids) and all(isinstance(item, str) for item in source_evidence):
        checks.append("source_evidence_traceable")
    else:
        errors.append("resolver golden cases must carry non-empty source_evidence IDs")

    node_refs_valid = _valid_node_refs(expected_node_refs)
    if result_type == "none":
        if expected_node_refs == []:
            checks.append("expected_node_refs_present")
        elif expected_node_refs is None:
            errors.append("none cases must declare expected_node_refs as an empty list")
        else:
            errors.append("none cases must not declare result node references")
    elif node_refs_valid:
        checks.append("expected_node_refs_present")
    else:
        errors.append("resolver golden cases must carry canonical expected_node_refs")

    if fallback_reason:
        checks.append("fallback_reason_present")
    else:
        errors.append("resolver golden cases must carry a fallback_reason")

    if trace_safe_rationale:
        checks.append("trace_safe_rationale_present")
    else:
        errors.append("resolver golden cases must carry a trace_safe_rationale")

    if result_type == "single_value":
        checks.append("single_value_deterministic")
        if confidence != "deterministic":
            errors.append("single_value cases must be deterministic")
    elif result_type == "composed":
        checks.append("composed_deterministic")
        if confidence != "deterministic":
            errors.append("composed cases must be deterministic")
        if "compose" in rationale or "compatible" in rationale:
            checks.append("composed_compatible_rationale")
        else:
            errors.append("composed cases must explain compatible composed requirements")
    elif result_type == "conflict":
        checks.append("conflict_review_required")
        if confidence != "review_required":
            errors.append("conflict cases must require review")
        if "conflict" in rationale or "incompatible" in rationale:
            checks.append("conflict_incompatible_rationale")
        else:
            errors.append("conflict cases must explain the incompatible equal-force condition")
    elif result_type == "none":
        checks.append("none_insufficient")
        if confidence != "insufficient":
            errors.append("none cases must be insufficient")
        if any(marker in rationale for marker in ("missing", "no ", "none", "unmodeled")):
            checks.append("none_absence_rationale")
        else:
            errors.append("none cases must explain the missing or unmodeled applicability")

    return {
        "case_id": case_id,
        "expected_result_type": result_type,
        "expected_confidence": confidence,
        "jurisdiction": jurisdiction,
        "effective_date": effective_date,
        "asset_context": asset_context,
        "context_id_count": len(context_ids) if isinstance(context_ids, list) else 0,
        "discipline_filter_count": len(discipline_filters)
        if isinstance(discipline_filters, list)
        else 0,
        "expected_node_ref_count": len(expected_node_refs)
        if isinstance(expected_node_refs, list)
        else 0,
        "source_evidence_count": len(source_evidence),
        "checks": sorted(set(checks)),
        "errors": errors,
        "passed": not errors,
        "status": "passed" if not errors else "failed",
    }


def _evaluate_resolver_error_case(case: dict[str, Any]) -> dict[str, Any]:
    case_id = str(case.get("case_id", "")).strip()
    error_type = str(case.get("expected_error_type", "")).strip()
    expected_status = case.get("expected_status")
    request = case.get("request") if isinstance(case.get("request"), dict) else {}
    rationale = str(case.get("rationale", "")).strip().lower()

    errors: list[str] = []
    checks: list[str] = []

    if case_id:
        checks.append("case_id_present")
    else:
        errors.append("resolver error cases must identify a case_id")

    if error_type not in RESOLVER_ERROR_TYPES:
        errors.append(f"unsupported resolver error type: {error_type}")
    else:
        checks.append(f"{error_type}_case_present")

    if not isinstance(case.get("request"), dict):
        errors.append("resolver error cases must carry a static request object")

    if error_type == "deterministic_no_result":
        if expected_status != 200:
            errors.append("deterministic no-result cases must declare a 200 none response")
    elif not isinstance(expected_status, int) or expected_status < 400:
        errors.append("resolver error cases must declare a deterministic 4xx/5xx status")

    if error_type == "invalid_input":
        if request.get("text", None) == "":
            checks.append("invalid_input_empty_query")
        else:
            errors.append("invalid input cases must model an empty query text")
    elif error_type == "malformed_request":
        if not isinstance(request.get("context_ids"), list):
            checks.append("malformed_request_static_failure")
        else:
            errors.append("malformed request cases must model malformed context_ids")
    elif error_type == "missing_fixture_artifact":
        if "missing" in rationale or "artifact" in rationale:
            checks.append("missing_fixture_artifact_fail_closed")
        else:
            errors.append("missing fixture cases must explain fail-closed artifact handling")
    elif error_type == "blocked_runtime_route":
        route = str(request.get("route", "")).strip()
        if route.startswith("/v2/resolve"):
            checks.append("blocked_runtime_route_static_inventory")
        else:
            errors.append("blocked route cases must name a /v2/resolve* route")
    elif error_type == "deterministic_no_result":
        if "no result" in rationale or "none" in rationale or "deterministic" in rationale:
            checks.append("deterministic_no_result_safe_fallback")
        else:
            errors.append("deterministic no-result cases must explain safe fallback semantics")

    return {
        "case_id": case_id,
        "expected_error_type": error_type,
        "expected_status": expected_status,
        "checks": sorted(set(checks)),
        "errors": errors,
        "passed": not errors,
        "status": "passed" if not errors else "failed",
    }


def _summarize_case_results(results: list[dict[str, Any]]) -> dict[str, Any]:
    coverage = {key: False for key in REQUIRED_COVERAGE_KEYS}
    result_type_counts: dict[str, int] = {}
    confidence_counts: dict[str, int] = {}
    jurisdiction_counts: dict[str, int] = {}
    asset_context_counts: dict[str, int] = {}

    for result in results:
        result_type = str(result.get("expected_result_type") or "unspecified")
        confidence = str(result.get("expected_confidence") or "unspecified")
        jurisdiction = str(result.get("jurisdiction") or "unspecified")
        asset_context = str(result.get("asset_context") or "unspecified")
        result_type_counts[result_type] = result_type_counts.get(result_type, 0) + 1
        confidence_counts[confidence] = confidence_counts.get(confidence, 0) + 1
        jurisdiction_counts[jurisdiction] = jurisdiction_counts.get(jurisdiction, 0) + 1
        asset_context_counts[asset_context] = asset_context_counts.get(asset_context, 0) + 1
        for check in result.get("checks", []):
            if result.get("passed") is True and check in coverage:
                coverage[check] = True

    return {
        "cases_total": len(results),
        "cases_passed": sum(1 for result in results if result.get("passed") is True),
        "cases_failed": sum(1 for result in results if result.get("passed") is not True),
        "result_type_counts": dict(sorted(result_type_counts.items())),
        "confidence_counts": dict(sorted(confidence_counts.items())),
        "jurisdiction_counts": dict(sorted(jurisdiction_counts.items())),
        "asset_context_counts": dict(sorted(asset_context_counts.items())),
        "required_coverage": coverage,
    }


def _summarize_error_case_results(results: list[dict[str, Any]]) -> dict[str, Any]:
    coverage = {key: False for key in REQUIRED_ERROR_COVERAGE_KEYS}
    error_type_counts: dict[str, int] = {}

    for result in results:
        error_type = str(result.get("expected_error_type") or "unspecified")
        error_type_counts[error_type] = error_type_counts.get(error_type, 0) + 1
        for check in result.get("checks", []):
            if result.get("passed") is True and check in coverage:
                coverage[check] = True

    return {
        "cases_total": len(results),
        "cases_passed": sum(1 for result in results if result.get("passed") is True),
        "cases_failed": sum(1 for result in results if result.get("passed") is not True),
        "error_type_counts": dict(sorted(error_type_counts.items())),
        "required_coverage": coverage,
    }


def _empty_summary() -> dict[str, Any]:
    return {
        "cases_total": 0,
        "cases_passed": 0,
        "cases_failed": 0,
        "result_type_counts": {},
        "confidence_counts": {},
        "jurisdiction_counts": {},
        "asset_context_counts": {},
        "required_coverage": {key: False for key in REQUIRED_COVERAGE_KEYS},
    }


def _empty_error_summary() -> dict[str, Any]:
    return {
        "cases_total": 0,
        "cases_passed": 0,
        "cases_failed": 0,
        "error_type_counts": {},
        "required_coverage": {key: False for key in REQUIRED_ERROR_COVERAGE_KEYS},
    }


def _contract_surface_summary(
    summary: dict[str, Any],
    error_summary: dict[str, Any],
    preview_route_status: dict[str, Any],
) -> dict[str, Any]:
    coverage = summary.get("required_coverage", {})
    error_coverage = error_summary.get("required_coverage", {})
    preview_routes = preview_route_status.get("previewRoutesPresent", {})
    return {
        "request_shape": {
            "query_text": bool(coverage.get("query_text_present")),
            "optional_context_ids": bool(coverage.get("query_context_ids_static_contract")),
            "optional_discipline_filters": bool(
                coverage.get("query_discipline_filters_static_contract")
            ),
            "deterministic_trace_request_flag": bool(
                coverage.get("trace_requested_boolean")
            ),
        },
        "result_shape": {
            "result_types": dict(summary.get("result_type_counts", {})),
            "canonical_backbone_node_refs": bool(
                coverage.get("expected_node_refs_present")
            ),
            "confidence_classes": dict(summary.get("confidence_counts", {})),
            "source_evidence_refs": bool(coverage.get("source_evidence_traceable")),
            "fallback_reason": bool(coverage.get("fallback_reason_present")),
            "trace_safe_rationale": bool(coverage.get("trace_safe_rationale_present")),
        },
        "error_shape": {
            "error_types": dict(error_summary.get("error_type_counts", {})),
            "invalid_input": bool(error_coverage.get("invalid_input_case_present")),
            "malformed_request": bool(error_coverage.get("malformed_request_case_present")),
            "missing_fixture_artifact": bool(
                error_coverage.get("missing_fixture_artifact_case_present")
            ),
            "blocked_runtime_route": bool(
                error_coverage.get("blocked_runtime_route_case_present")
            ),
            "deterministic_no_result": bool(
                error_coverage.get("deterministic_no_result_case_present")
            ),
        },
        "preview_route_preservation": {
            "checked": preview_route_status.get("checked") is True,
            "required_routes_present": bool(preview_routes)
            and all(preview_routes.values()),
            "preview_routes_present": preview_routes,
        },
    }


def _check_resolver_route_boundary(root: Path) -> dict[str, Any]:
    return summarize_resolver_route_boundary(root, API_INDEX_PATH)


def _check_preview_route_boundary(root: Path) -> dict[str, Any]:
    status = summarize_shadow_preview_route_boundaries(root, API_INDEX_PATH)
    return {
        "checked": status.get("checked") is True,
        "path": _relative_to_root(Path(status["path"]), root)
        if isinstance(status.get("path"), Path)
        else str(status.get("path", API_INDEX_PATH)),
        "resolveRouteMounted": status.get("resolveRouteMounted") is True,
        "traceRouteMounted": status.get("traceRouteMounted") is True,
        "previewRoutesPresent": dict(status.get("previewRoutesPresent") or {}),
        "routeCount": int(status.get("routeCount") or 0),
    }


def _valid_node_refs(value: Any) -> bool:
    if not isinstance(value, list) or not value:
        return False
    for item in value:
        if not isinstance(item, dict):
            return False
        node_id = str(item.get("node_id", "")).strip()
        role = str(item.get("role", "")).strip()
        if not node_id.startswith("VTN-") or not role:
            return False
    return True


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


def _resolve_report_path(
    *,
    root: Path,
    run_id: str,
    output_path: Path | None,
) -> Path:
    candidate = output_path or (
        RESOLVER_QA_REPORT_ROOT / run_id / RESOLVER_QA_REPORT_FILENAME
    )
    report_path = candidate.resolve() if candidate.is_absolute() else (root / candidate).resolve()
    allowed_root = (root / RESOLVER_QA_REPORT_ROOT).resolve()
    try:
        relative_parts = report_path.relative_to(allowed_root).parts
    except ValueError as exc:
        raise ValueError("report path must stay inside the resolver QA report directory") from exc
    if len(relative_parts) != 2 or relative_parts[0] != run_id:
        raise ValueError("report path must be scoped to the current resolver QA run id")
    if relative_parts[1] != RESOLVER_QA_REPORT_FILENAME:
        raise ValueError(f"report filename must be {RESOLVER_QA_REPORT_FILENAME}")
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


def _dict_list(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, dict)]


def _relative_to_root(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
