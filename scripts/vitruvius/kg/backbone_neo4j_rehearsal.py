"""Neo4j isolated rehearsal readiness validator for AEC-MEPFS.

The validator reads existing rollback/dump-load evidence and writes a bounded
readiness report. It does not run Neo4j writes, stop servers, dump/load primary
databases, rebuild KG artifacts, or promote graph data.
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
from typing import Any, Sequence


REPORT_SCHEMA_VERSION = "aec-mepfs-neo4j-rehearsal-readiness/v1"
REPORT_ROOT = Path("006_System-Manifests/aec-mepfs-backbone/neo4j-rehearsal")
REPORT_FILENAME = "neo4j-rehearsal-readiness-report.json"
SOURCE_ADMISSION_REPORT_ROOT = Path("006_System-Manifests/aec-mepfs-backbone/source-admission")
SOURCE_ADMISSION_REPORT_FILENAME = "source-admission-report.json"
RUN_ID_RE = re.compile(r"^[A-Za-z0-9_.-]+$")

DEFAULT_ISOLATED_REHEARSAL_REPORT_PATH = Path(
    "006_System-Manifests/aec-mepfs-backbone/rollback/20260425T144332Z/isolated-dump-load-rehearsal-report.json"
)
DEFAULT_ROLLBACK_PREFLIGHT_REPORT_PATH = Path(
    "006_System-Manifests/aec-mepfs-backbone/rollback/20260425T130816Z/rollback-preflight-report.json"
)

DESTRUCTIVE_TOKENS = (
    "DETACH DELETE",
    "DROP DATABASE",
    "CREATE OR REPLACE",
    "run-kg-pipeline",
    "--reset",
    "--reload",
)


def run_neo4j_rehearsal_readiness(
    *,
    repo_root: str | Path | None = None,
    run_id: str | None = None,
    output_path: str | Path | None = None,
    isolated_rehearsal_report_path: str | Path = DEFAULT_ISOLATED_REHEARSAL_REPORT_PATH,
    rollback_preflight_report_path: str | Path = DEFAULT_ROLLBACK_PREFLIGHT_REPORT_PATH,
    source_admission_report_path: str | Path | None = None,
) -> dict[str, Any]:
    """Validate isolated Neo4j rehearsal evidence and write a readiness report."""

    root = _repo_root(repo_root)
    resolved_run_id = _run_id(run_id)
    report_path = _resolve_report_path(root, resolved_run_id, Path(output_path) if output_path else None)
    isolated_path = _resolve_existing_file(root, Path(isolated_rehearsal_report_path), "isolated rehearsal report")
    preflight_path = _resolve_existing_file(root, Path(rollback_preflight_report_path), "rollback preflight report")
    source_admission_path = _resolve_optional_source_admission_report(root, source_admission_report_path)

    isolated_report = _read_json_object(isolated_path, "isolated rehearsal report")
    preflight_report = _read_json_object(preflight_path, "rollback preflight report")
    source_admission_report = (
        _read_json_object(source_admission_path, "source admission report") if source_admission_path else None
    )

    isolated_checks = _isolated_rehearsal_checks(isolated_report)
    preflight_checks = _rollback_preflight_checks(preflight_report)
    source_admission_checks = _source_admission_checks(source_admission_report)
    destructive_matches = _destructive_command_matches(isolated_report) + _destructive_command_matches(preflight_report)
    missing = [name for name, passed in {**isolated_checks, **preflight_checks}.items() if not passed]
    errors: list[str] = []
    if missing:
        errors.extend(f"check failed: {name}" for name in missing)
    if destructive_matches:
        errors.append("destructive command tokens found in rehearsal/preflight evidence")
    if source_admission_report is not None and not all(source_admission_checks.values()):
        errors.append("source admission evidence does not prove metadata-only/no-protected-ingest boundary")

    isolated_verified = not [name for name, passed in isolated_checks.items() if not passed]
    source_admission_gate_satisfied = bool(source_admission_report) and all(source_admission_checks.values())
    report = {
        "schema_version": REPORT_SCHEMA_VERSION,
        "ok": not errors,
        "run_id": resolved_run_id,
        "generated_at_utc": _utc_now(),
        "report_path": _relative_to_root(report_path, root),
        "authority": {
            "packet": ".ai/03_plans/AEC-MEPFS-Backbone/2026-04-27_neo4j_isolated_rehearsal_packet.md",
            "classification": "GREEN_REHEARSAL_VALIDATION_AND_PROMOTION_PREP_ONLY",
            "production_live_promotion_authorized": False,
            "primary_graph_mutation_authorized": False,
            "global_live_authorization": False,
        },
        "inputs": {
            "isolated_rehearsal_report": _relative_to_root(isolated_path, root),
            "rollback_preflight_report": _relative_to_root(preflight_path, root),
            "source_admission_report": _relative_to_root(source_admission_path, root) if source_admission_path else None,
        },
        "status": {
            "isolatedRehearsalVerified": isolated_verified,
            "readOnlyPreflightAvailable": preflight_checks.get("preflight_report_read_only", False),
            "productionLivePromotionAuthorized": False,
            "primaryGraphMutationAuthorized": False,
            "livePromotionReady": False,
            "nextRequiredPacket": "dedicated_live_promotion_packet_with_fresh_backup_restore_graph_diff_and_rollback_transcript",
        },
        "checks": {
            "isolated_rehearsal": isolated_checks,
            "rollback_preflight": preflight_checks,
            "source_admission": source_admission_checks,
        },
        "isolated_rehearsal_summary": _isolated_summary(isolated_report),
        "rollback_preflight_summary": _preflight_summary(preflight_report),
        "source_admission_summary": _source_admission_summary(source_admission_report),
        "live_promotion_prerequisites": _live_promotion_prerequisites(source_admission_gate_satisfied),
        "destructive_command_matches": destructive_matches,
        "safety_invariants": {
            "liveNeo4jTouched": bool(_get(isolated_report, "summary.live_neo4j_touched")),
            "primaryGraphMutationAuthorized": False,
            "productionLivePromotionAuthorized": False,
            "kgRebuildAuthorized": False,
            "protectedContentIngestAuthorized": _source_admission_authorizes_protected_ingest(source_admission_report),
            "globalLiveAuthorization": False,
        },
        "errors": errors,
        "environment": {
            "python_version": platform.python_version(),
            "platform": platform.platform(),
            "cpu_count": os.cpu_count(),
        },
    }
    _write_json(report_path, report)
    return report


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate AEC-MEPFS Neo4j isolated rehearsal readiness evidence."
    )
    parser.add_argument("--repo-root", default=None)
    parser.add_argument("--run-id", default=None)
    parser.add_argument("--output", default=None)
    parser.add_argument("--isolated-rehearsal-report", default=str(DEFAULT_ISOLATED_REHEARSAL_REPORT_PATH))
    parser.add_argument("--rollback-preflight-report", default=str(DEFAULT_ROLLBACK_PREFLIGHT_REPORT_PATH))
    parser.add_argument(
        "--source-admission-report",
        default=None,
        help="Optional metadata-only source-admission report. Defaults to latest report when available.",
    )
    args = parser.parse_args(argv)

    try:
        report = run_neo4j_rehearsal_readiness(
            repo_root=args.repo_root,
            run_id=args.run_id,
            output_path=args.output,
            isolated_rehearsal_report_path=args.isolated_rehearsal_report,
            rollback_preflight_report_path=args.rollback_preflight_report,
            source_admission_report_path=args.source_admission_report,
        )
    except (FileNotFoundError, ValueError) as exc:
        print(json.dumps({"ok": False, "errors": [str(exc)]}, indent=2, sort_keys=True))
        return 1

    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["ok"] else 1


def _isolated_rehearsal_checks(report: dict[str, Any]) -> dict[str, bool]:
    summary = report.get("summary", {}) if isinstance(report.get("summary"), dict) else {}
    step_returncodes = summary.get("step_returncodes", [])
    return {
        "isolated_report_kind_matches": report.get("report_kind") == "aec_mepfs_isolated_neo4j_dump_load_rehearsal",
        "scope_is_offline_throwaway": "offline throwaway" in str(report.get("scope", "")).lower(),
        "all_steps_zero": summary.get("all_steps_zero") is True,
        "step_returncodes_all_zero": isinstance(step_returncodes, list) and bool(step_returncodes) and all(code == 0 for code in step_returncodes),
        "dump_file_exists": summary.get("dump_file_exists") is True,
        "restored_database_dir_exists": summary.get("restored_database_dir_exists") is True,
        "source_database_dir_exists": summary.get("source_database_dir_exists") is True,
        "live_neo4j_not_touched": summary.get("live_neo4j_touched") is False,
        "expected_fixture_imported": summary.get("import_expected_nodes") == 2 and summary.get("import_expected_relationships") == 1,
    }


def _rollback_preflight_checks(report: dict[str, Any]) -> dict[str, bool]:
    return {
        "preflight_schema_matches": report.get("schema_version") == "aec-bb-rollback-preflight/v1",
        "preflight_proof_status_blocks_runtime": report.get("proof_status") == "blocked_runtime_stopped_or_isolated_database_required",
        "preflight_report_read_only": report.get("destructive_operations_executed") is False,
        "backup_dump_load_not_executed_by_preflight": report.get("backup_dump_load_executed") is False,
        "runtime_ready_false": report.get("runtime_ready") is False,
    }


def _source_admission_checks(report: dict[str, Any] | None) -> dict[str, bool]:
    if report is None:
        return {
            "source_admission_report_available": False,
            "source_admission_schema_matches": False,
            "source_admission_ok": False,
            "protected_content_ingest_not_authorized": False,
            "source_payload_exposure_not_authorized": False,
            "canonical_content_admission_not_authorized": False,
            "no_content_ingest_rows": False,
            "no_protected_payload_hits": False,
            "currentness_coverage_complete": False,
        }

    status = report.get("status", {}) if isinstance(report.get("status"), dict) else {}
    summary = report.get("summary", {}) if isinstance(report.get("summary"), dict) else {}
    invariants = report.get("safety_invariants", {}) if isinstance(report.get("safety_invariants"), dict) else {}
    return {
        "source_admission_report_available": True,
        "source_admission_schema_matches": report.get("schema_version") == "aec-mepfs-protected-source-admission/v1",
        "source_admission_ok": report.get("ok") is True,
        "protected_content_ingest_not_authorized": status.get("protectedContentIngestAuthorized") is False,
        "source_payload_exposure_not_authorized": status.get("sourcePayloadExposureAuthorized") is False,
        "canonical_content_admission_not_authorized": status.get("canonicalContentAdmissionAuthorized") is False,
        "no_content_ingest_rows": summary.get("content_ingest_rows") == 0,
        "no_protected_payload_hits": summary.get("protected_payload_key_hits") == 0
        and invariants.get("protectedPayloadStoredInAdmissionArtifacts") is False,
        "currentness_coverage_complete": summary.get("missing_currentness_rows") == 0,
    }


def _isolated_summary(report: dict[str, Any]) -> dict[str, Any]:
    summary = report.get("summary", {}) if isinstance(report.get("summary"), dict) else {}
    return {
        "database": summary.get("database"),
        "neo4j_version": summary.get("neo4j_version"),
        "step_returncodes": summary.get("step_returncodes"),
        "dump_file_exists": summary.get("dump_file_exists"),
        "dump_file_size_bytes": summary.get("dump_file_size_bytes"),
        "live_neo4j_touched": summary.get("live_neo4j_touched"),
        "live_neo4j_stopped": summary.get("live_neo4j_stopped"),
        "import_expected_nodes": summary.get("import_expected_nodes"),
        "import_expected_relationships": summary.get("import_expected_relationships"),
    }


def _preflight_summary(report: dict[str, Any]) -> dict[str, Any]:
    admin = report.get("admin_capabilities", {}) if isinstance(report.get("admin_capabilities"), dict) else {}
    live_graph = report.get("live_graph", {}) if isinstance(report.get("live_graph"), dict) else {}
    return {
        "proof_status": report.get("proof_status"),
        "runtime_ready": report.get("runtime_ready"),
        "destructive_operations_executed": report.get("destructive_operations_executed"),
        "backup_dump_load_executed": report.get("backup_dump_load_executed"),
        "database_dump_available": admin.get("database_dump_available"),
        "database_load_available": admin.get("database_load_available"),
        "dump_requires_unmounted_database": admin.get("dump_requires_unmounted_database"),
        "load_requires_unmounted_database": admin.get("load_requires_unmounted_database"),
        "live_graph_connectivity": live_graph.get("connectivity"),
        "live_graph_node_count": live_graph.get("node_count"),
        "live_graph_backbone_shadow_nodes": live_graph.get("backbone_shadow_nodes"),
    }


def _source_admission_summary(report: dict[str, Any] | None) -> dict[str, Any]:
    if report is None:
        return {
            "source_admission_report_available": False,
            "metadata_only_rows": None,
            "content_ingest_rows": None,
            "protected_payload_key_hits": None,
            "protected_content_ingest_authorized": None,
            "source_payload_exposure_authorized": None,
            "canonical_content_admission_authorized": None,
        }
    status = report.get("status", {}) if isinstance(report.get("status"), dict) else {}
    summary = report.get("summary", {}) if isinstance(report.get("summary"), dict) else {}
    return {
        "source_admission_report_available": True,
        "metadata_only_rows": summary.get("metadata_only_rows"),
        "content_ingest_rows": summary.get("content_ingest_rows"),
        "protected_payload_key_hits": summary.get("protected_payload_key_hits"),
        "protected_content_ingest_authorized": status.get("protectedContentIngestAuthorized"),
        "source_payload_exposure_authorized": status.get("sourcePayloadExposureAuthorized"),
        "canonical_content_admission_authorized": status.get("canonicalContentAdmissionAuthorized"),
    }


def _source_admission_authorizes_protected_ingest(report: dict[str, Any] | None) -> bool:
    if report is None:
        return False
    status = report.get("status", {}) if isinstance(report.get("status"), dict) else {}
    return status.get("protectedContentIngestAuthorized") is True


def _live_promotion_prerequisites(source_admission_gate_satisfied: bool) -> list[dict[str, Any]]:
    return [
        {"gate": "dedicated_live_promotion_packet", "satisfied": False},
        {"gate": "fresh_live_backup_or_export", "satisfied": False},
        {"gate": "restore_proof_against_isolated_target", "satisfied": False},
        {"gate": "pre_post_graph_count_diff", "satisfied": False},
        {"gate": "shadow_namespace_or_database_load", "satisfied": False},
        {"gate": "source_admission_no_protected_ingest_or_valid_authority", "satisfied": source_admission_gate_satisfied},
        {"gate": "api_explorer_parity_current_for_promoted_surface", "satisfied": False},
        {"gate": "rollback_transcript_written_before_mutation", "satisfied": False},
        {"gate": "scoped_live_promotion_authorization", "satisfied": False},
    ]


def _destructive_command_matches(value: Any, prefix: str = "$") -> list[dict[str, str]]:
    matches: list[dict[str, str]] = []
    if isinstance(value, dict):
        for key, child in value.items():
            matches.extend(_destructive_command_matches(child, f"{prefix}.{key}"))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            matches.extend(_destructive_command_matches(child, f"{prefix}[{index}]"))
    elif isinstance(value, str):
        for token in DESTRUCTIVE_TOKENS:
            if token in value:
                matches.append({"path": prefix, "token": token})
    return matches


def _get(payload: dict[str, Any], dotted: str) -> Any:
    current: Any = payload
    for part in dotted.split("."):
        if not isinstance(current, dict):
            return None
        current = current.get(part)
    return current


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


def _resolve_optional_source_admission_report(root: Path, value: str | Path | None) -> Path | None:
    if value is not None:
        return _resolve_existing_file(root, Path(value), "source admission report")
    report_root = (root / SOURCE_ADMISSION_REPORT_ROOT).resolve()
    if not report_root.is_dir():
        return None
    candidates = sorted(report_root.glob(f"*/{SOURCE_ADMISSION_REPORT_FILENAME}"))
    return candidates[-1].resolve() if candidates else None


def _resolve_report_path(root: Path, run_id: str, output_path: Path | None) -> Path:
    candidate = output_path or (REPORT_ROOT / run_id / REPORT_FILENAME)
    report_path = candidate.resolve() if candidate.is_absolute() else (root / candidate).resolve()
    allowed_root = (root / REPORT_ROOT).resolve()
    try:
        relative_parts = report_path.relative_to(allowed_root).parts
    except ValueError as exc:
        raise ValueError("report path must stay inside the neo4j-rehearsal evidence directory") from exc
    if len(relative_parts) != 2 or relative_parts[0] != run_id:
        raise ValueError("report path must be scoped to the current Neo4j rehearsal run id")
    if relative_parts[1] != REPORT_FILENAME:
        raise ValueError(f"report filename must be {REPORT_FILENAME}")
    return report_path


def _read_json_object(path: Path, label: str) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{label} must be a JSON object")
    return payload


def _run_id(value: str | None) -> str:
    candidate = value or datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    if not RUN_ID_RE.fullmatch(candidate):
        raise ValueError("run_id must contain only letters, digits, underscore, dot, or dash")
    return candidate


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _relative_to_root(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def _utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
