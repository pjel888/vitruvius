"""File-backed placement QA runner for AEC-MEPFS Backbone readiness.

This runner checks authoring/migration QA cases from the readiness fixture. It
is intentionally runtime-disconnected: it reads JSON fixtures, writes an
auditable report, and does not call PlacementEngine, Neo4j, graph rebuilds,
feature flags, API routes, or Explorer code.
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


REPORT_SCHEMA_VERSION = "aec-bb-placement-qa-report/v1"
DEFAULT_FIXTURE_PATH = Path(
    "scripts/tests/fixtures/aec_mepfs_backbone/valid_readiness_s2.json"
)
PLACEMENT_QA_REPORT_ROOT = Path("006_System-Manifests/aec-mepfs-backbone/placement-qa")
PLACEMENT_QA_REPORT_FILENAME = "placement-qa-report.json"
RUN_ID_RE = re.compile(r"^[A-Za-z0-9_.-]+$")
AUTO_ACCEPT_CONFIDENCE_THRESHOLD = 0.92
LD8_WORKFLOW = "LD-8 PlacementAssertion"
REQUIRED_COVERAGE_KEYS = {
    "case_id_present",
    "input_context_present",
    "l3_l4_ld8_auto_accept",
    "ld8_auto_accept_rationale",
    "l1_l2_human_review",
    "legacy_label_alias",
    "legacy_label_rationale",
    "owner_present",
    "proposal_level_present",
    "review_status_candidate",
    "source_evidence_ids_present",
}


def run_placement_qa_fixture(
    fixture_path: str | Path = DEFAULT_FIXTURE_PATH,
    *,
    repo_root: str | Path | None = None,
    run_id: str | None = None,
    output_path: str | Path | None = None,
) -> dict[str, Any]:
    """Run file-backed placement QA checks and write a JSON report."""
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

    if contract_report.ok:
        cases = _dict_list(payload.get("authoring_migration_cases"))
        if not cases:
            errors.append("authoring_migration_cases: expected at least one QA case")
        else:
            case_results = [_evaluate_authoring_case(case) for case in cases]
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
                    "authoring_migration_cases: missing required QA coverage "
                    f"({', '.join(missing_coverage)})"
                )
    else:
        warnings.append("placement QA skipped because readiness fixture failed validation")

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
        "safety_boundaries": {
            "shadow_only": True,
            "file_backed_only": True,
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
        description="Run AEC-MEPFS Backbone placement QA checks."
    )
    parser.add_argument("--fixture", default=str(DEFAULT_FIXTURE_PATH))
    parser.add_argument("--repo-root", default=None)
    parser.add_argument("--run-id", default=None)
    parser.add_argument("--output", default=None)
    args = parser.parse_args(argv)

    try:
        report = run_placement_qa_fixture(
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


def _evaluate_authoring_case(case: dict[str, Any]) -> dict[str, Any]:
    case_id = str(case.get("case_id", "")).strip()
    case_type = str(case.get("case_type", "")).strip()
    proposal_level = str(case.get("proposal_level", "")).upper()
    proposed_by = str(case.get("proposed_by", "")).strip().lower()
    auto_accept = _as_bool(case.get("auto_accept"))
    confidence = _as_float(case.get("confidence"))
    workflow = str(case.get("workflow", "")).strip()
    expected_output = case.get("expected_output") if isinstance(case.get("expected_output"), dict) else {}
    input_value = case.get("input") if isinstance(case.get("input"), dict) else {}
    source_evidence = case.get("source_evidence") if isinstance(case.get("source_evidence"), list) else []
    source_evidence_ids = [str(item).strip() for item in source_evidence]
    owner = str(case.get("owner", "")).strip()
    review_status = str(case.get("review_status", "")).strip()
    rationale = str(case.get("rationale", "")).strip().lower()

    errors: list[str] = []
    checks: list[str] = []

    if case_id:
        checks.append("case_id_present")
    else:
        errors.append("authoring migration cases must identify a case_id")

    if owner:
        checks.append("owner_present")
    else:
        errors.append("authoring migration cases must identify an owner")

    if review_status == "candidate":
        checks.append("review_status_candidate")
    else:
        errors.append("authoring migration cases must remain candidate review_status")

    if proposal_level:
        checks.append("proposal_level_present")
    else:
        errors.append("authoring migration cases must identify a proposal_level")

    if _has_input_context(input_value):
        checks.append("input_context_present")
    else:
        errors.append("authoring migration cases must carry label or legacy_label input context")

    if not source_evidence:
        errors.append("authoring migration cases must carry source_evidence")
    elif all(source_evidence_ids) and all(isinstance(item, str) for item in source_evidence):
        checks.append("source_evidence_ids_present")
    else:
        errors.append("authoring migration cases must carry non-empty source_evidence IDs")

    if proposal_level in {"L1", "L2"}:
        checks.append("l1_l2_human_review")
        if proposed_by == "ai":
            errors.append(f"AI-authored {proposal_level} changes are blocked")
        if auto_accept:
            errors.append(f"{proposal_level} changes cannot be auto-accepted")
        if expected_output.get("review_queue") != "two_human_review":
            errors.append("L1/L2 changes must route to two_human_review")

    if auto_accept:
        checks.append("auto_accept_policy")
        if proposal_level not in {"L3", "L4"}:
            errors.append("auto_accept is only allowed for L3/L4 proposals")
        if confidence is None or confidence < AUTO_ACCEPT_CONFIDENCE_THRESHOLD:
            errors.append("auto_accept requires confidence >= 0.92")
        if workflow != LD8_WORKFLOW:
            errors.append("auto_accept requires LD-8 PlacementAssertion workflow")
        if expected_output.get("review_queue") != "auto_accept_sampling_audit":
            errors.append("auto_accept cases must route to auto_accept_sampling_audit")
        if "ld-8" in rationale or "auto-accept" in rationale or "auto accept" in rationale:
            checks.append("ld8_auto_accept_rationale")
        else:
            errors.append("auto_accept cases must explain LD-8 auto-accept rationale")

    if _is_legacy_alias_case(case_type, case):
        checks.append("legacy_label_alias")
        if expected_output.get("canonical_label_source") != "steward_approved_label":
            errors.append("legacy aliases must preserve steward-approved canonical labels")
        if expected_output.get("legacy_label_storage") != "alias_or_source_label":
            errors.append("legacy labels must be stored as aliases or source labels")
        if auto_accept:
            errors.append("legacy alias migration cannot be auto-accepted")
        if "alias" in rationale and "canonical" in rationale:
            checks.append("legacy_label_rationale")
        else:
            errors.append("legacy alias cases must explain alias and canonical label handling")

    return {
        "case_id": case_id,
        "case_type": case_type,
        "proposal_level": proposal_level,
        "proposed_by": proposed_by,
        "auto_accept": auto_accept,
        "confidence": confidence,
        "workflow": workflow,
        "owner": owner,
        "review_status": review_status,
        "expected_review_queue": expected_output.get("review_queue"),
        "source_evidence_count": len(source_evidence),
        "checks": sorted(set(checks)),
        "errors": errors,
        "passed": not errors,
        "status": "passed" if not errors else "failed",
    }


def _summarize_case_results(results: list[dict[str, Any]]) -> dict[str, Any]:
    coverage = {key: False for key in REQUIRED_COVERAGE_KEYS}
    review_queue_counts: dict[str, int] = {}
    level_counts: dict[str, int] = {}
    case_type_counts: dict[str, int] = {}
    proposed_by_counts: dict[str, int] = {}
    workflow_counts: dict[str, int] = {}
    auto_accept_count = 0

    for result in results:
        level = str(result.get("proposal_level") or "unspecified")
        case_type = str(result.get("case_type") or "unspecified")
        proposed_by = str(result.get("proposed_by") or "unspecified")
        workflow = str(result.get("workflow") or "unspecified")
        level_counts[level] = level_counts.get(level, 0) + 1
        case_type_counts[case_type] = case_type_counts.get(case_type, 0) + 1
        proposed_by_counts[proposed_by] = proposed_by_counts.get(proposed_by, 0) + 1
        workflow_counts[workflow] = workflow_counts.get(workflow, 0) + 1
        queue = result.get("expected_review_queue")
        if queue:
            queue_key = str(queue)
            review_queue_counts[queue_key] = review_queue_counts.get(queue_key, 0) + 1

        if result.get("auto_accept") is True:
            auto_accept_count += 1
            if (
                level in {"L3", "L4"}
                and result.get("workflow") == LD8_WORKFLOW
                and result.get("passed") is True
            ):
                coverage["l3_l4_ld8_auto_accept"] = True
        if "l1_l2_human_review" in result.get("checks", []) and result.get("passed") is True:
            coverage["l1_l2_human_review"] = True
        if "legacy_label_alias" in result.get("checks", []) and result.get("passed") is True:
            coverage["legacy_label_alias"] = True
        for check in result.get("checks", []):
            if result.get("passed") is True and check in coverage:
                coverage[check] = True

    return {
        "cases_total": len(results),
        "cases_passed": sum(1 for result in results if result.get("passed") is True),
        "cases_failed": sum(1 for result in results if result.get("passed") is not True),
        "auto_accept_cases": auto_accept_count,
        "case_type_counts": dict(sorted(case_type_counts.items())),
        "proposed_by_counts": dict(sorted(proposed_by_counts.items())),
        "review_queue_counts": dict(sorted(review_queue_counts.items())),
        "proposal_level_counts": dict(sorted(level_counts.items())),
        "workflow_counts": dict(sorted(workflow_counts.items())),
        "required_coverage": coverage,
    }


def _empty_summary() -> dict[str, Any]:
    return {
        "cases_total": 0,
        "cases_passed": 0,
        "cases_failed": 0,
        "auto_accept_cases": 0,
        "case_type_counts": {},
        "proposed_by_counts": {},
        "review_queue_counts": {},
        "proposal_level_counts": {},
        "workflow_counts": {},
        "required_coverage": {key: False for key in REQUIRED_COVERAGE_KEYS},
    }


def _is_legacy_alias_case(case_type: str, case: dict[str, Any]) -> bool:
    input_value = case.get("input") if isinstance(case.get("input"), dict) else {}
    return case_type == "legacy_label_alias" or input_value.get("mapping_type") == "alias"


def _has_input_context(value: dict[str, Any]) -> bool:
    return bool(str(value.get("label") or value.get("legacy_label") or "").strip())


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
        PLACEMENT_QA_REPORT_ROOT / run_id / PLACEMENT_QA_REPORT_FILENAME
    )
    report_path = candidate.resolve() if candidate.is_absolute() else (root / candidate).resolve()
    allowed_root = (root / PLACEMENT_QA_REPORT_ROOT).resolve()
    try:
        relative_parts = report_path.relative_to(allowed_root).parts
    except ValueError as exc:
        raise ValueError("report path must stay inside the placement QA report directory") from exc
    if len(relative_parts) != 2 or relative_parts[0] != run_id:
        raise ValueError("report path must be scoped to the current placement QA run id")
    if relative_parts[1] != PLACEMENT_QA_REPORT_FILENAME:
        raise ValueError(f"report filename must be {PLACEMENT_QA_REPORT_FILENAME}")
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


def _as_bool(value: Any) -> bool:
    return value is True


def _as_float(value: Any) -> float | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int | float):
        return float(value)
    return None


def _relative_to_root(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
