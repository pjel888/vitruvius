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
REQUIRED_COVERAGE_KEYS = {
    "single_value_deterministic",
    "composed_deterministic",
    "conflict_review_required",
    "none_insufficient",
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
    summary = _empty_summary()
    api_route_status = _check_resolver_route_boundary(root)

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
    else:
        warnings.append("resolver QA skipped because readiness fixture failed validation")

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
        "required_coverage_keys": sorted(REQUIRED_COVERAGE_KEYS),
        "api_route_status": api_route_status,
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

    errors: list[str] = []
    checks: list[str] = []

    if result_type not in RESOLVER_RESULT_TYPES:
        errors.append(f"unsupported resolver result type: {result_type}")

    if not query.get("concept_id"):
        errors.append("resolver golden cases must identify a concept_id")
    if not source_evidence:
        errors.append("resolver golden cases must carry source_evidence")

    if result_type == "single_value":
        checks.append("single_value_deterministic")
        if confidence != "deterministic":
            errors.append("single_value cases must be deterministic")
    elif result_type == "composed":
        checks.append("composed_deterministic")
        if confidence != "deterministic":
            errors.append("composed cases must be deterministic")
    elif result_type == "conflict":
        checks.append("conflict_review_required")
        if confidence != "review_required":
            errors.append("conflict cases must require review")
        if "conflict" not in rationale and "incompatible" not in rationale:
            errors.append("conflict cases must explain the incompatible equal-force condition")
    elif result_type == "none":
        checks.append("none_insufficient")
        if confidence != "insufficient":
            errors.append("none cases must be insufficient")

    return {
        "case_id": case_id,
        "expected_result_type": result_type,
        "expected_confidence": confidence,
        "jurisdiction": str(case.get("jurisdiction", "")).strip(),
        "effective_date": str(case.get("effective_date", "")).strip(),
        "source_evidence_count": len(source_evidence),
        "checks": sorted(set(checks)),
        "errors": errors,
        "passed": not errors,
        "status": "passed" if not errors else "failed",
    }


def _summarize_case_results(results: list[dict[str, Any]]) -> dict[str, Any]:
    coverage = {key: False for key in REQUIRED_COVERAGE_KEYS}
    result_type_counts: dict[str, int] = {}
    confidence_counts: dict[str, int] = {}

    for result in results:
        result_type = str(result.get("expected_result_type") or "unspecified")
        confidence = str(result.get("expected_confidence") or "unspecified")
        result_type_counts[result_type] = result_type_counts.get(result_type, 0) + 1
        confidence_counts[confidence] = confidence_counts.get(confidence, 0) + 1
        for check in result.get("checks", []):
            if result.get("passed") is True and check in coverage:
                coverage[check] = True

    return {
        "cases_total": len(results),
        "cases_passed": sum(1 for result in results if result.get("passed") is True),
        "cases_failed": sum(1 for result in results if result.get("passed") is not True),
        "result_type_counts": dict(sorted(result_type_counts.items())),
        "confidence_counts": dict(sorted(confidence_counts.items())),
        "required_coverage": coverage,
    }


def _empty_summary() -> dict[str, Any]:
    return {
        "cases_total": 0,
        "cases_passed": 0,
        "cases_failed": 0,
        "result_type_counts": {},
        "confidence_counts": {},
        "required_coverage": {key: False for key in REQUIRED_COVERAGE_KEYS},
    }


def _check_resolver_route_boundary(root: Path) -> dict[str, Any]:
    api_index = (root / API_INDEX_PATH).resolve()
    if not api_index.is_file():
        return {
            "checked": False,
            "path": str(API_INDEX_PATH),
            "resolveRouteMounted": False,
            "traceRouteMounted": False,
            "reason": "api index file not present under repo root",
        }
    text = api_index.read_text(encoding="utf-8")
    return {
        "checked": True,
        "path": str(API_INDEX_PATH),
        "resolveRouteMounted": bool(
            re.search(r"app\.(post|all)\s*\(\s*['\"]\/v2\/resolve['\"]", text)
        ),
        "traceRouteMounted": bool(
            re.search(r"app\.(get|all)\s*\(\s*['\"]\/v2\/resolve\/trace\/", text)
        ),
    }


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
