"""File-backed safety-boundary audit for AEC-MEPFS Backbone shadow work.

This runner consolidates existing shadow evidence into one auditable report. It
does not query Neo4j, run the KG pipeline, call API routes, invoke Explorer, or
promote any shadow artifact into a runtime graph.
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

import yaml

from vitruvius.kg.backbone_api_route_inventory import (
    REQUIRED_PREVIEW_ROUTES,
    summarize_shadow_preview_route_boundaries,
)
from vitruvius.kg.backbone_repo_state import read_repo_state


REPORT_SCHEMA_VERSION = "aec-bb-shadow-boundary-audit-report/v1"
BOUNDARY_AUDIT_REPORT_ROOT = Path(
    "006_System-Manifests/aec-mepfs-backbone/boundary-audit"
)
BOUNDARY_AUDIT_REPORT_FILENAME = "shadow-boundary-audit-report.json"
DEFAULT_CONSUMER_REPORT_PATH = Path(
    "006_System-Manifests/aec-mepfs-backbone/shadow-staging/20260426T003710Z/"
    "shadow-staging-consumer-report.json"
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
    "006_System-Manifests/aec-mepfs-backbone/parity/20260426T095440Z/"
    "api-explorer-parity-report.json"
)
DEFAULT_CONFIG_PATH = Path("config/vitruvius.yaml")
DEFAULT_API_INDEX_PATH = Path("api/index.ts")
RUN_ID_RE = re.compile(r"^[A-Za-z0-9_.-]+$")

REQUIRED_DISABLED_FEATURE_FLAGS = {
    "k_backbone_validation",
    "k_jurisdictional_overrides",
    "k_rosetta_stone",
    "k_shadow_read",
    "k_standards_mapping",
    "k_taxonomy_v2",
    "k_vitruvian_context",
}
REQUIRED_PARITY_CATEGORIES = {
    "shadow_backbone_summary_route",
    "shadow_backbone_taxonomy_graph_preview",
    "shadow_backbone_placement_qa_preview",
    "shadow_backbone_evidence_preview",
    "shadow_graph_file_artifact",
    "shadow_graph_fail_closed",
    "shadow_evidence_preview_opt_in_isolation",
    "shadow_preview_opt_in_isolation",
    "shadow_placement_qa_preview_opt_in_isolation",
    "source_evidence_display",
    "source_invalid_id",
}
EXPECTED_QA_SCHEMA_VERSIONS = {
    "placement_qa": "aec-bb-placement-qa-report/v1",
    "resolver_qa": "aec-bb-resolver-qa-report/v1",
}


def run_shadow_boundary_audit(
    *,
    repo_root: str | Path | None = None,
    run_id: str | None = None,
    output_path: str | Path | None = None,
    consumer_report_path: str | Path = DEFAULT_CONSUMER_REPORT_PATH,
    placement_qa_report_path: str | Path = DEFAULT_PLACEMENT_QA_REPORT_PATH,
    resolver_qa_report_path: str | Path = DEFAULT_RESOLVER_QA_REPORT_PATH,
    parity_report_path: str | Path = DEFAULT_PARITY_REPORT_PATH,
    config_path: str | Path = DEFAULT_CONFIG_PATH,
    api_index_path: str | Path = DEFAULT_API_INDEX_PATH,
) -> dict[str, Any]:
    """Audit current shadow evidence and write a JSON boundary report."""
    root = _repo_root(repo_root)
    resolved_run_id = _run_id(run_id)
    started_at = _utc_now()

    consumer_path = _resolve_existing_file(root, Path(consumer_report_path), "consumer report")
    consumer_report = _load_json_object(consumer_path, "consumer report")
    graph_path = _resolve_shadow_graph_path(root, consumer_report)
    graph_report = _load_json_object(graph_path, "shadow graph")
    placement_path = _resolve_existing_file(
        root,
        Path(placement_qa_report_path),
        "placement QA report",
    )
    placement_report = _load_json_object(placement_path, "placement QA report")
    resolver_path = _resolve_existing_file(
        root,
        Path(resolver_qa_report_path),
        "resolver QA report",
    )
    resolver_report = _load_json_object(resolver_path, "resolver QA report")
    parity_path = _resolve_existing_file(root, Path(parity_report_path), "parity report")
    parity_report = _load_json_object(parity_path, "parity report")
    config = _read_feature_flags(root, Path(config_path))
    api_route_status = _check_api_route_boundaries(root, Path(api_index_path))
    report_path = _resolve_report_path(
        root=root,
        run_id=resolved_run_id,
        output_path=Path(output_path) if output_path is not None else None,
    )

    checks = [
        _check_consumer_report(consumer_report),
        _check_shadow_graph(consumer_report, graph_report),
        _check_qa_report(
            "placement_qa",
            placement_report,
            EXPECTED_QA_SCHEMA_VERSIONS["placement_qa"],
        ),
        _check_qa_report(
            "resolver_qa",
            resolver_report,
            EXPECTED_QA_SCHEMA_VERSIONS["resolver_qa"],
        ),
        _check_resolver_qa_report(resolver_report),
        _check_parity_report(parity_report),
        _check_feature_flags(config),
        _check_api_routes(api_route_status),
        _check_live_vs_cached_resolver_route_status(api_route_status, resolver_report),
        _check_file_backing(
            root,
            {
                "consumer_report": consumer_path,
                "shadow_graph": graph_path,
                "placement_qa_report": placement_path,
                "resolver_qa_report": resolver_path,
                "parity_report": parity_path,
                "config": config["path"],
                "api_index": api_route_status.get("path"),
            },
        ),
    ]
    errors = sorted({error for check in checks for error in check["errors"]})
    warnings = sorted({warning for check in checks for warning in check["warnings"]})
    safety_invariants = _build_safety_invariants(
        consumer_report=consumer_report,
        placement_report=placement_report,
        resolver_report=resolver_report,
        parity_report=parity_report,
        feature_flags=config,
        api_route_status=api_route_status,
        check_errors=errors,
    )
    for invariant, passed in safety_invariants.items():
        if not passed:
            errors.append(f"safety invariant failed: {invariant}")
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
            "consumer_report_path": _relative_to_root(consumer_path, root),
            "shadow_graph_path": _relative_to_root(graph_path, root),
            "placement_qa_report_path": _relative_to_root(placement_path, root),
            "resolver_qa_report_path": _relative_to_root(resolver_path, root),
            "parity_report_path": _relative_to_root(parity_path, root),
            "config_path": _relative_to_root(config["path"], root),
            "api_index_path": _relative_to_root(api_route_status["path"], root)
            if isinstance(api_route_status.get("path"), Path)
            else str(api_route_status.get("path")),
        },
        "input_file_hashes_sha256": _hash_input_files(
            {
                "consumer_report": consumer_path,
                "shadow_graph": graph_path,
                "placement_qa_report": placement_path,
                "resolver_qa_report": resolver_path,
                "parity_report": parity_path,
                "config": config["path"],
                "api_index": api_route_status.get("path"),
            }
        ),
        "repo_state": read_repo_state(root),
        "summary": {
            "checks_total": len(checks),
            "checks_passed": sum(1 for check in checks if check["ok"]),
            "consumer_run_id": consumer_report.get("run_id"),
            "shadow_graph_counts": graph_report.get("counts", {}),
            "placement_qa_cases_passed": placement_report.get("summary", {}).get("cases_passed"),
            "resolver_qa_cases_passed": resolver_report.get("summary", {}).get("cases_passed"),
            "parity_commands_passed": parity_report.get("commands_passed"),
            "parity_cases_passed": parity_report.get("cases_passed"),
        },
        "safety_invariants": safety_invariants,
        "feature_flags": config["flags"],
        "api_route_status": _serializable_route_status(api_route_status, root),
        "check_results": checks,
        "errors": errors,
        "warnings": warnings,
    }
    _write_json(report_path, report)
    return report


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run AEC-MEPFS Backbone shadow safety-boundary audit."
    )
    parser.add_argument("--repo-root", default=None)
    parser.add_argument("--run-id", default=None)
    parser.add_argument("--output", default=None)
    parser.add_argument("--consumer-report", default=str(DEFAULT_CONSUMER_REPORT_PATH))
    parser.add_argument("--placement-qa-report", default=str(DEFAULT_PLACEMENT_QA_REPORT_PATH))
    parser.add_argument("--resolver-qa-report", default=str(DEFAULT_RESOLVER_QA_REPORT_PATH))
    parser.add_argument("--parity-report", default=str(DEFAULT_PARITY_REPORT_PATH))
    parser.add_argument("--config", default=str(DEFAULT_CONFIG_PATH))
    parser.add_argument("--api-index", default=str(DEFAULT_API_INDEX_PATH))
    args = parser.parse_args(argv)

    try:
        report = run_shadow_boundary_audit(
            repo_root=args.repo_root,
            run_id=args.run_id,
            output_path=args.output,
            consumer_report_path=args.consumer_report,
            placement_qa_report_path=args.placement_qa_report,
            resolver_qa_report_path=args.resolver_qa_report,
            parity_report_path=args.parity_report,
            config_path=args.config,
            api_index_path=args.api_index,
        )
    except (FileNotFoundError, ValueError) as exc:
        print(json.dumps({"ok": False, "errors": [str(exc)]}, indent=2, sort_keys=True))
        return 1

    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["ok"] else 1


def _check_consumer_report(report: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    if report.get("schema_version") != "aec-bb-shadow-staging-consumer-report/v1":
        errors.append("consumer report: unexpected schema_version")
    if report.get("ok") is not True:
        errors.append("consumer report: ok must be true")
    _require_boundaries(
        errors,
        "consumer report",
        report.get("boundaries"),
        {
            "shadow_only": True,
            "file_backed_only": True,
            "live_neo4j_writes": False,
            "graph_rebuild": False,
            "feature_flag_cutover": False,
            "api_explorer_cutover": False,
            "protected_content_ingest": False,
            "canonical_content_admission": False,
        },
    )
    no_ingest = report.get("no_ingest_boundary_coverage")
    if not isinstance(no_ingest, dict):
        errors.append("consumer report: missing no_ingest_boundary_coverage")
    else:
        if no_ingest.get("content_ingest_source_count") != 0:
            errors.append("consumer report: protected content ingest count must remain 0")
        if no_ingest.get("missing_explicit_block_count") != 0:
            errors.append("consumer report: every source row must keep explicit no-ingest coverage")
    return _check("consumer_report", errors, warnings)


def _check_shadow_graph(consumer_report: dict[str, Any], graph: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    if graph.get("schema_version") != "aec-bb-shadow-graph/v1":
        errors.append("shadow graph: unexpected schema_version")
    if graph.get("status") != "shadow_graph_staged":
        errors.append("shadow graph: status must be shadow_graph_staged")
    if graph.get("run_id") != consumer_report.get("run_id"):
        errors.append("shadow graph: run_id must match consumer report")
    expected_counts = consumer_report.get("shadow_graph_counts")
    if isinstance(expected_counts, dict) and graph.get("counts") != expected_counts:
        errors.append("shadow graph: counts must match consumer report")
    counts = graph.get("counts")
    if not isinstance(counts, dict):
        errors.append("shadow graph: counts must be present")
    else:
        for key in ("nodes", "edges", "roots", "max_depth"):
            if not isinstance(counts.get(key), int) or counts.get(key, -1) < 0:
                errors.append(f"shadow graph: counts.{key} must be a non-negative integer")
    return _check("shadow_graph", errors, warnings)


def _check_qa_report(
    name: str,
    report: dict[str, Any],
    expected_schema_version: str,
) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    if report.get("schema_version") != expected_schema_version:
        errors.append(f"{name}: unexpected schema_version")
    if report.get("ok") is not True:
        errors.append(f"{name}: ok must be true")
    _require_boundaries(
        errors,
        name,
        report.get("safety_boundaries"),
        {
            "shadow_only": True,
            "file_backed_only": True,
            "live_neo4j_writes": False,
            "kg_rebuild": False,
            "feature_flag_cutover": False,
            "explorer_default_adoption": False,
            "protected_content_ingest": False,
            "canonical_content_admission": False,
        },
    )
    summary = report.get("summary")
    if not isinstance(summary, dict):
        errors.append(f"{name}: summary must be present")
    elif summary.get("cases_passed") != summary.get("cases_total"):
        errors.append(f"{name}: all cases must pass")
    return _check(name, errors, warnings)


def _check_resolver_qa_report(report: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    _require_boundaries(
        errors,
        "resolver_qa",
        report.get("safety_boundaries"),
        {
            "live_resolver_invocation": False,
            "llm_hot_path": False,
        },
    )
    route_status = report.get("api_route_status")
    if not isinstance(route_status, dict):
        errors.append("resolver_qa: missing api_route_status")
    else:
        if route_status.get("resolveRouteMounted") is not False:
            errors.append("resolver_qa: /v2/resolve must remain unmounted")
        if route_status.get("traceRouteMounted") is not False:
            errors.append("resolver_qa: /v2/resolve/trace must remain unmounted")
    return _check("resolver_route_guard", errors, warnings)


def _check_parity_report(report: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    if report.get("schema_version") != "aec-bb-parity-report/v1":
        errors.append("parity report: unexpected schema_version")
    if report.get("ok") is not True:
        errors.append("parity report: ok must be true")
    if report.get("commands_run", 0) <= 0:
        errors.append("parity report: commands_run must be positive")
    if report.get("commands_passed") != report.get("commands_run"):
        errors.append("parity report: all commands must pass")
    if report.get("cases_declared", 0) <= 0:
        errors.append("parity report: cases_declared must be positive")
    if report.get("cases_passed") != report.get("cases_declared"):
        errors.append("parity report: all cases must pass")
    categories = set(_string_list(report.get("required_case_categories")))
    missing_categories = sorted(REQUIRED_PARITY_CATEGORIES - categories)
    if missing_categories:
        errors.append(
            "parity report: missing required shadow boundary categories "
            f"({', '.join(missing_categories)})"
        )
    return _check("api_explorer_parity", errors, warnings)


def _check_feature_flags(config: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    if not config["exists"]:
        errors.append("feature flags: config file must exist")
    if config["malformed"]:
        errors.append("feature flags: config YAML must parse")
    flags = config["flags"]
    for flag in sorted(REQUIRED_DISABLED_FEATURE_FLAGS):
        if flags.get(flag) is not False:
            errors.append(f"feature flags: {flag} must remain false")
    return _check("feature_flags_default_off", errors, warnings)


def _check_api_routes(status: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    if status.get("checked") is not True:
        errors.append("api routes: api index must be checked")
    if status.get("resolveRouteMounted") is not False:
        errors.append("api routes: /v2/resolve must remain unmounted")
    if status.get("traceRouteMounted") is not False:
        errors.append("api routes: /v2/resolve/trace must remain unmounted")
    missing_routes = [
        name for name, present in status.get("previewRoutesPresent", {}).items() if not present
    ]
    if missing_routes:
        errors.append(f"api routes: missing expected preview routes ({', '.join(missing_routes)})")
    return _check("api_route_boundaries", errors, warnings)


def _check_live_vs_cached_resolver_route_status(
    api_route_status: dict[str, Any],
    resolver_report: dict[str, Any],
) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    resolver_route_status = _dict(resolver_report.get("api_route_status"))
    for key in ("resolveRouteMounted", "traceRouteMounted"):
        live_value = api_route_status.get(key)
        cached_value = resolver_route_status.get(key)
        if live_value is not cached_value:
            errors.append(f"resolver route status drift: live API {key} != resolver QA {key}")
    return _check("resolver_route_status_consistency", errors, warnings)


def _check_file_backing(root: Path, paths: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    for label, value in paths.items():
        if not isinstance(value, Path):
            errors.append(f"file backing: {label} path must be a Path")
            continue
        try:
            value.resolve().relative_to(root)
        except ValueError:
            errors.append(f"file backing: {label} must stay inside repo root")
            continue
        if not value.is_file():
            errors.append(f"file backing: {label} must exist")
    return _check("file_backed_artifacts", errors, warnings)


def _build_safety_invariants(
    *,
    consumer_report: dict[str, Any],
    placement_report: dict[str, Any],
    resolver_report: dict[str, Any],
    parity_report: dict[str, Any],
    feature_flags: dict[str, Any],
    api_route_status: dict[str, Any],
    check_errors: list[str],
) -> dict[str, bool]:
    consumer_boundaries = _dict(consumer_report.get("boundaries"))
    placement_boundaries = _dict(placement_report.get("safety_boundaries"))
    resolver_boundaries = _dict(resolver_report.get("safety_boundaries"))
    no_ingest = _dict(consumer_report.get("no_ingest_boundary_coverage"))
    flags = feature_flags["flags"]
    parity_categories = set(_string_list(parity_report.get("required_case_categories")))

    return {
        "no_neo4j_writes": (
            consumer_boundaries.get("live_neo4j_writes") is False
            and placement_boundaries.get("live_neo4j_writes") is False
            and resolver_boundaries.get("live_neo4j_writes") is False
        ),
        "no_kg_rebuild": (
            consumer_boundaries.get("graph_rebuild") is False
            and placement_boundaries.get("kg_rebuild") is False
            and resolver_boundaries.get("kg_rebuild") is False
        ),
        "no_protected_content_ingest": (
            consumer_boundaries.get("protected_content_ingest") is False
            and placement_boundaries.get("protected_content_ingest") is False
            and resolver_boundaries.get("protected_content_ingest") is False
            and no_ingest.get("content_ingest_source_count") == 0
        ),
        "no_feature_flag_cutover": (
            consumer_boundaries.get("feature_flag_cutover") is False
            and placement_boundaries.get("feature_flag_cutover") is False
            and resolver_boundaries.get("feature_flag_cutover") is False
            and all(flags.get(flag) is False for flag in REQUIRED_DISABLED_FEATURE_FLAGS)
        ),
        "no_explorer_default_adoption": (
            consumer_boundaries.get("api_explorer_cutover") is False
            and placement_boundaries.get("explorer_default_adoption") is False
            and resolver_boundaries.get("explorer_default_adoption") is False
            and {
                "shadow_preview_opt_in_isolation",
                "shadow_placement_qa_preview_opt_in_isolation",
                "shadow_evidence_preview_opt_in_isolation",
            }.issubset(parity_categories)
        ),
        "no_resolver_route_mounting": (
            api_route_status.get("resolveRouteMounted") is False
            and api_route_status.get("traceRouteMounted") is False
            and _dict(resolver_report.get("api_route_status")).get("resolveRouteMounted") is False
            and _dict(resolver_report.get("api_route_status")).get("traceRouteMounted") is False
        ),
        "preview_read_only_shadow_only": (
            consumer_boundaries.get("shadow_only") is True
            and consumer_boundaries.get("file_backed_only") is True
            and placement_boundaries.get("shadow_only") is True
            and placement_boundaries.get("file_backed_only") is True
            and resolver_boundaries.get("shadow_only") is True
            and resolver_boundaries.get("file_backed_only") is True
            and parity_report.get("ok") is True
        ),
        "generated_artifacts_file_backed_auditable": not check_errors,
    }


def _require_boundaries(
    errors: list[str],
    label: str,
    boundaries: Any,
    expected: dict[str, bool],
) -> None:
    if not isinstance(boundaries, dict):
        errors.append(f"{label}: missing boundary object")
        return
    for key, value in expected.items():
        if boundaries.get(key) is not value:
            errors.append(f"{label}: {key} must be {str(value).lower()}")


def _check(name: str, errors: list[str], warnings: list[str]) -> dict[str, Any]:
    return {
        "name": name,
        "ok": not errors,
        "errors": errors,
        "warnings": warnings,
    }


def _read_feature_flags(root: Path, value: Path) -> dict[str, Any]:
    path = _resolve_path_inside_root(root, value, "config")
    result = {
        "path": path,
        "exists": path.is_file(),
        "malformed": False,
        "flags": {},
    }
    if not path.is_file():
        return result
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError:
        result["malformed"] = True
        return result
    features = raw.get("features") if isinstance(raw, dict) else None
    if isinstance(features, dict):
        result["flags"] = {str(key): bool(value) for key, value in features.items()}
    return result


def _check_api_route_boundaries(root: Path, value: Path) -> dict[str, Any]:
    return summarize_shadow_preview_route_boundaries(root, value)


def _resolve_shadow_graph_path(root: Path, consumer_report: dict[str, Any]) -> Path:
    raw_path = consumer_report.get("shadow_graph_path")
    if not isinstance(raw_path, str) or not raw_path.strip():
        raise ValueError("consumer report must include shadow_graph_path")
    path = _resolve_existing_file(root, Path(raw_path), "shadow graph")
    if path.name != "shadow-backbone-graph.json":
        raise ValueError("shadow graph filename must be shadow-backbone-graph.json")
    return path


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
    path = _resolve_path_inside_root(root, value, label)
    if not path.is_file():
        raise FileNotFoundError(f"{label} not found: {path}")
    return path


def _resolve_path_inside_root(root: Path, value: Path, label: str) -> Path:
    path = value.resolve() if value.is_absolute() else (root / value).resolve()
    try:
        path.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"{label} path must stay inside repo root") from exc
    return path


def _resolve_report_path(
    *,
    root: Path,
    run_id: str,
    output_path: Path | None,
) -> Path:
    candidate = output_path or (
        BOUNDARY_AUDIT_REPORT_ROOT / run_id / BOUNDARY_AUDIT_REPORT_FILENAME
    )
    report_path = candidate.resolve() if candidate.is_absolute() else (root / candidate).resolve()
    allowed_root = (root / BOUNDARY_AUDIT_REPORT_ROOT).resolve()
    try:
        relative_parts = report_path.relative_to(allowed_root).parts
    except ValueError as exc:
        raise ValueError("report path must stay inside the boundary audit report directory") from exc
    if len(relative_parts) != 2 or relative_parts[0] != run_id:
        raise ValueError("report path must be scoped to the current boundary audit run id")
    if relative_parts[1] != BOUNDARY_AUDIT_REPORT_FILENAME:
        raise ValueError(f"report filename must be {BOUNDARY_AUDIT_REPORT_FILENAME}")
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


def _hash_input_files(paths: dict[str, Any]) -> dict[str, str | None]:
    hashes: dict[str, str | None] = {}
    for label, value in paths.items():
        if not isinstance(value, Path) or not value.is_file():
            hashes[label] = None
            continue
        digest = hashlib.sha256()
        with value.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
        hashes[label] = digest.hexdigest()
    return hashes


def _relative_to_root(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, str)]


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _serializable_route_status(status: dict[str, Any], root: Path) -> dict[str, Any]:
    path = status.get("path")
    serializable = dict(status)
    if isinstance(path, Path):
        serializable["path"] = _relative_to_root(path, root)
    return serializable


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
