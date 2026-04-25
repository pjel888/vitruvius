"""File-backed shadow staging for AEC-MEPFS Backbone registry candidates.

This module is intentionally runtime-disconnected. It validates the prepared
registry candidates and writes an auditable staging artifact without touching KG
schemas, Neo4j, API, Explorer, feature flags, graph rebuilds, or source content.
"""

from __future__ import annotations

import argparse
import json
import re
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Sequence

from vitruvius.kg.backbone_contracts import validate_backbone_contract_file


SHADOW_STAGING_SCHEMA_VERSION = "aec-bb-shadow-staging/v1"
SHADOW_STAGING_REPORT_SCHEMA_VERSION = "aec-bb-shadow-staging-report/v1"
DEFAULT_PREDICATE_REGISTRY_PATH = Path(
    ".ai/03_plans/AEC-MEPFS-Backbone/registry-candidates/predicate-registry.json"
)
DEFAULT_SOURCE_RIGHTS_REGISTRY_PATH = Path(
    ".ai/03_plans/AEC-MEPFS-Backbone/registry-candidates/source-rights-registry.json"
)
SHADOW_STAGING_ROOT = Path("006_System-Manifests/aec-mepfs-backbone/shadow-staging")
SHADOW_STAGING_ARTIFACT_FILENAME = "shadow-backbone-staging.json"
SHADOW_STAGING_REPORT_FILENAME = "shadow-staging-report.json"
RUN_ID_RE = re.compile(r"^[A-Za-z0-9_.-]+$")


def stage_shadow_backbone(
    *,
    predicate_registry_path: str | Path = DEFAULT_PREDICATE_REGISTRY_PATH,
    source_rights_registry_path: str | Path = DEFAULT_SOURCE_RIGHTS_REGISTRY_PATH,
    repo_root: str | Path | None = None,
    run_id: str | None = None,
    output_dir: str | Path | None = None,
) -> dict[str, Any]:
    """Validate and stage registry candidates as a file-backed shadow artifact."""
    root = _repo_root(repo_root)
    resolved_run_id = _run_id(run_id)
    predicate_path = _resolve_existing_file(root, Path(predicate_registry_path))
    source_rights_path = _resolve_existing_file(root, Path(source_rights_registry_path))
    target_dir = _resolve_output_dir(root, resolved_run_id, Path(output_dir) if output_dir else None)
    artifact_path = target_dir / SHADOW_STAGING_ARTIFACT_FILENAME
    report_path = target_dir / SHADOW_STAGING_REPORT_FILENAME
    started_at = _utc_now()

    predicate_contract = validate_backbone_contract_file(predicate_path)
    source_rights_contract = validate_backbone_contract_file(source_rights_path)
    predicate_payload = _load_json_object(predicate_path)
    source_rights_payload = _load_json_object(source_rights_path)
    predicate_rows = _list_section(predicate_payload, "predicate_registry")
    source_rows = _list_section(source_rights_payload, "source_rights_registry")

    errors = [
        f"predicate_registry: {error}" for error in predicate_contract.errors
    ] + [
        f"source_rights_registry: {error}" for error in source_rights_contract.errors
    ]
    warnings = [
        f"predicate_registry: {warning}" for warning in predicate_contract.warnings
    ] + [
        f"source_rights_registry: {warning}" for warning in source_rights_contract.warnings
    ]

    errors.extend(_duplicate_value_errors(predicate_rows, "predicate", "predicate_registry"))
    errors.extend(_duplicate_value_errors(source_rows, "source_id", "source_rights_registry"))
    errors.extend(_no_ingest_errors(source_rows))

    ok = not errors
    artifact: dict[str, Any] | None = None
    if ok:
        artifact = _build_shadow_artifact(
            run_id=resolved_run_id,
            created_at=started_at,
            predicate_path=predicate_path,
            source_rights_path=source_rights_path,
            root=root,
            predicate_rows=predicate_rows,
            source_rows=source_rows,
        )
        _write_json(artifact_path, artifact)

    finished_at = _utc_now()
    report = {
        "schema_version": SHADOW_STAGING_REPORT_SCHEMA_VERSION,
        "ok": ok,
        "run_id": resolved_run_id,
        "started_at_utc": started_at,
        "finished_at_utc": finished_at,
        "artifact_written": artifact is not None,
        "artifact_path": _relative_to_root(artifact_path, root) if artifact is not None else None,
        "report_path": _relative_to_root(report_path, root),
        "predicate_registry_path": _relative_to_root(predicate_path, root),
        "source_rights_registry_path": _relative_to_root(source_rights_path, root),
        "counts": {
            "predicate_registry": len(predicate_rows),
            "source_rights_registry": len(source_rows),
        },
        "boundaries": _shadow_boundaries(),
        "contract_reports": {
            "predicate_registry": predicate_contract.to_dict(),
            "source_rights_registry": source_rights_contract.to_dict(),
        },
        "errors": sorted(set(errors)),
        "warnings": sorted(set(warnings)),
    }
    _write_json(report_path, report)
    return report


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Stage AEC-MEPFS Backbone registry candidates as a shadow artifact."
    )
    parser.add_argument("--predicate-registry", default=str(DEFAULT_PREDICATE_REGISTRY_PATH))
    parser.add_argument("--source-rights-registry", default=str(DEFAULT_SOURCE_RIGHTS_REGISTRY_PATH))
    parser.add_argument("--repo-root", default=None)
    parser.add_argument("--run-id", default=None)
    parser.add_argument("--output-dir", default=None)
    args = parser.parse_args(argv)

    try:
        report = stage_shadow_backbone(
            predicate_registry_path=args.predicate_registry,
            source_rights_registry_path=args.source_rights_registry,
            repo_root=args.repo_root,
            run_id=args.run_id,
            output_dir=args.output_dir,
        )
    except ValueError as exc:
        print(json.dumps({"ok": False, "errors": [str(exc)]}, indent=2, sort_keys=True))
        return 1

    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["ok"] else 1


def _build_shadow_artifact(
    *,
    run_id: str,
    created_at: str,
    predicate_path: Path,
    source_rights_path: Path,
    root: Path,
    predicate_rows: list[dict[str, Any]],
    source_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "schema_version": SHADOW_STAGING_SCHEMA_VERSION,
        "run_id": run_id,
        "created_at_utc": created_at,
        "status": "shadow_staged",
        "source_paths": {
            "predicate_registry": _relative_to_root(predicate_path, root),
            "source_rights_registry": _relative_to_root(source_rights_path, root),
        },
        "counts": {
            "predicate_registry": len(predicate_rows),
            "source_rights_registry": len(source_rows),
        },
        "boundaries": _shadow_boundaries(),
        "predicate_registry": predicate_rows,
        "source_rights_registry": source_rows,
    }


def _shadow_boundaries() -> dict[str, bool]:
    return {
        "shadow_only": True,
        "file_backed_only": True,
        "live_neo4j_writes": False,
        "graph_rebuild": False,
        "feature_flag_cutover": False,
        "api_explorer_cutover": False,
        "canonical_content_admission": False,
        "protected_content_ingest": False,
    }


def _no_ingest_errors(source_rows: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    for index, row in enumerate(source_rows):
        if row.get("source_rights_class") == "content_ingest":
            errors.append(
                f"source_rights_registry[{index}].source_rights_class: "
                "content_ingest is blocked for shadow staging"
            )
        boundary = str(row.get("declared_use_boundary") or "").lower()
        if "no " not in boundary and "blocked" not in boundary:
            errors.append(
                f"source_rights_registry[{index}].declared_use_boundary: "
                "must explicitly block content ingest"
            )
    return errors


def _duplicate_value_errors(rows: list[dict[str, Any]], key: str, section: str) -> list[str]:
    seen: set[str] = set()
    duplicates: set[str] = set()
    for row in rows:
        value = str(row.get(key) or "")
        if not value:
            continue
        if value in seen:
            duplicates.add(value)
        seen.add(value)
    return [f"{section}.{key}: duplicate value '{value}'" for value in sorted(duplicates)]


def _list_section(payload: dict[str, Any], section: str) -> list[dict[str, Any]]:
    rows = payload.get(section)
    if not isinstance(rows, list):
        return []
    return [row for row in rows if isinstance(row, dict)]


def _load_json_object(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path}: expected a JSON object")
    return payload


def _resolve_existing_file(root: Path, path: Path) -> Path:
    candidate = path if path.is_absolute() else root / path
    resolved = candidate.resolve()
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"{path}: path must stay inside repository root") from exc
    if not resolved.is_file():
        raise ValueError(f"{path}: file does not exist")
    return resolved


def _resolve_output_dir(root: Path, run_id: str, output_dir: Path | None) -> Path:
    target = output_dir if output_dir is not None else SHADOW_STAGING_ROOT / run_id
    resolved = target if target.is_absolute() else root / target
    resolved = resolved.resolve()
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"{target}: output directory must stay inside repository root") from exc
    resolved.mkdir(parents=True, exist_ok=True)
    return resolved


def _repo_root(repo_root: str | Path | None) -> Path:
    return Path(repo_root).resolve() if repo_root is not None else Path.cwd().resolve()


def _run_id(run_id: str | None) -> str:
    value = run_id or datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    if not RUN_ID_RE.match(value):
        raise ValueError(f"run_id contains unsupported characters: {value}")
    return value


def _utc_now() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def _relative_to_root(path: Path, root: Path) -> str:
    return path.resolve().relative_to(root).as_posix()


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
