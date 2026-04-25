"""Read-only reporting over AEC-MEPFS Backbone shadow staging artifacts.

This module consumes the file-backed shadow staging artifact and producer
report. It writes a deterministic consumer report, but it never touches KG
schemas, Neo4j, API routes, Explorer routes, feature flags, graph rebuilds, or
source content.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Callable, Sequence

from vitruvius.kg.backbone_shadow_staging import (
    SHADOW_STAGING_ARTIFACT_FILENAME,
    SHADOW_STAGING_REPORT_FILENAME,
    SHADOW_STAGING_REPORT_SCHEMA_VERSION,
    SHADOW_STAGING_ROOT,
    SHADOW_STAGING_SCHEMA_VERSION,
)


CONSUMER_REPORT_SCHEMA_VERSION = "aec-bb-shadow-staging-consumer-report/v1"
CONSUMER_REPORT_FILENAME = "shadow-staging-consumer-report.json"
RUN_ID_RE = re.compile(r"^[A-Za-z0-9_.-]+$")

REQUIRED_TRUE_BOUNDARIES = {
    "shadow_only",
    "file_backed_only",
}
REQUIRED_FALSE_BOUNDARIES = {
    "live_neo4j_writes",
    "graph_rebuild",
    "feature_flag_cutover",
    "api_explorer_cutover",
    "canonical_content_admission",
    "protected_content_ingest",
}

Clock = Callable[[], str]


def build_shadow_staging_consumer_report(
    *,
    repo_root: str | Path | None = None,
    run_id: str | None = None,
    artifact_path: str | Path | None = None,
    producer_report_path: str | Path | None = None,
    output_path: str | Path | None = None,
    clock: Clock | None = None,
) -> dict[str, Any]:
    """Read a shadow staging artifact and write a read-only summary report."""
    root = _repo_root(repo_root)
    resolved_run_id = _resolve_run_id(
        root=root,
        run_id=run_id,
        artifact_path=Path(artifact_path) if artifact_path is not None else None,
        producer_report_path=Path(producer_report_path) if producer_report_path is not None else None,
    )
    artifact = _resolve_existing_file(
        root,
        Path(artifact_path)
        if artifact_path is not None
        else SHADOW_STAGING_ROOT / resolved_run_id / SHADOW_STAGING_ARTIFACT_FILENAME,
    )
    producer_report = _resolve_existing_file(
        root,
        Path(producer_report_path)
        if producer_report_path is not None
        else SHADOW_STAGING_ROOT / resolved_run_id / SHADOW_STAGING_REPORT_FILENAME,
    )
    report_path = _resolve_output_path(
        root=root,
        run_id=resolved_run_id,
        output_path=Path(output_path) if output_path is not None else None,
    )
    now = clock or _utc_now
    started_at = now()

    artifact_payload = _load_json_object(artifact)
    producer_payload = _load_json_object(producer_report)
    summary = _summarize_payloads(
        run_id=resolved_run_id,
        artifact=artifact_payload,
        producer_report=producer_payload,
    )

    finished_at = now()
    report = {
        "schema_version": CONSUMER_REPORT_SCHEMA_VERSION,
        "ok": not summary["errors"],
        "run_id": resolved_run_id,
        "started_at_utc": started_at,
        "finished_at_utc": finished_at,
        "artifact_path": _relative_to_root(artifact, root),
        "producer_report_path": _relative_to_root(producer_report, root),
        "report_path": _relative_to_root(report_path, root),
        "counts": summary["counts"],
        "predicate_categories": summary["predicate_categories"],
        "source_rights_classes": summary["source_rights_classes"],
        "clearance_states": summary["clearance_states"],
        "boundaries": summary["boundaries"],
        "boundary_coverage": summary["boundary_coverage"],
        "no_ingest_boundary_coverage": summary["no_ingest_boundary_coverage"],
        "errors": sorted(set(summary["errors"])),
        "warnings": sorted(set(summary["warnings"])),
    }
    _write_json(report_path, report)
    return report


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Build a read-only AEC-MEPFS Backbone shadow staging consumer report."
    )
    parser.add_argument("--repo-root", default=None)
    parser.add_argument("--run-id", default=None)
    parser.add_argument("--artifact", default=None)
    parser.add_argument("--producer-report", default=None)
    parser.add_argument("--output", default=None)
    args = parser.parse_args(argv)

    try:
        report = build_shadow_staging_consumer_report(
            repo_root=args.repo_root,
            run_id=args.run_id,
            artifact_path=args.artifact,
            producer_report_path=args.producer_report,
            output_path=args.output,
        )
    except ValueError as exc:
        print(json.dumps({"ok": False, "errors": [str(exc)]}, indent=2, sort_keys=True))
        return 1

    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["ok"] else 1


def _summarize_payloads(
    *,
    run_id: str,
    artifact: dict[str, Any],
    producer_report: dict[str, Any],
) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []

    _validate_top_level_artifact(run_id, artifact, errors)
    _validate_producer_report(run_id, producer_report, errors, warnings)

    boundaries = _object_value(artifact, "boundaries", errors)
    predicate_rows = _list_value(artifact, "predicate_registry", errors)
    source_rows = _list_value(artifact, "source_rights_registry", errors)
    counts = {
        "predicate_registry": len(predicate_rows),
        "source_rights_registry": len(source_rows),
    }

    declared_counts = _object_value(artifact, "counts", errors)
    for key, actual in counts.items():
        declared = declared_counts.get(key)
        if declared != actual:
            errors.append(f"artifact.counts.{key}: expected {actual}, found {declared!r}")

    producer_counts = producer_report.get("counts")
    if isinstance(producer_counts, dict):
        for key, actual in counts.items():
            declared = producer_counts.get(key)
            if declared != actual:
                errors.append(f"producer_report.counts.{key}: expected {actual}, found {declared!r}")
    else:
        errors.append("producer_report.counts: expected object")

    _validate_boundaries(boundaries, errors)
    no_ingest_coverage = _no_ingest_boundary_coverage(source_rows, errors)

    return {
        "counts": counts,
        "predicate_categories": _counter_dict(
            row.get("category") for row in predicate_rows if isinstance(row, dict)
        ),
        "source_rights_classes": _counter_dict(
            row.get("source_rights_class") for row in source_rows if isinstance(row, dict)
        ),
        "clearance_states": _counter_dict(
            row.get("clearance_state") for row in source_rows if isinstance(row, dict)
        ),
        "boundaries": boundaries,
        "boundary_coverage": {
            "required_true": sorted(REQUIRED_TRUE_BOUNDARIES),
            "required_false": sorted(REQUIRED_FALSE_BOUNDARIES),
            "safe_for_read_only_consumer": not any(
                error.startswith("artifact.boundaries.") for error in errors
            ),
        },
        "no_ingest_boundary_coverage": no_ingest_coverage,
        "errors": errors,
        "warnings": warnings,
    }


def _validate_top_level_artifact(
    run_id: str,
    artifact: dict[str, Any],
    errors: list[str],
) -> None:
    expected_fields = {
        "schema_version",
        "run_id",
        "status",
        "source_paths",
        "counts",
        "boundaries",
        "predicate_registry",
        "source_rights_registry",
    }
    for field in sorted(expected_fields):
        if field not in artifact:
            errors.append(f"artifact.{field}: missing required field")
    if artifact.get("schema_version") != SHADOW_STAGING_SCHEMA_VERSION:
        errors.append(
            "artifact.schema_version: expected "
            f"{SHADOW_STAGING_SCHEMA_VERSION}, found {artifact.get('schema_version')!r}"
        )
    if artifact.get("run_id") != run_id:
        errors.append(f"artifact.run_id: expected {run_id}, found {artifact.get('run_id')!r}")
    if artifact.get("status") != "shadow_staged":
        errors.append("artifact.status: expected 'shadow_staged'")
    _object_value(artifact, "source_paths", errors)


def _validate_producer_report(
    run_id: str,
    producer_report: dict[str, Any],
    errors: list[str],
    warnings: list[str],
) -> None:
    if producer_report.get("schema_version") != SHADOW_STAGING_REPORT_SCHEMA_VERSION:
        errors.append(
            "producer_report.schema_version: expected "
            f"{SHADOW_STAGING_REPORT_SCHEMA_VERSION}, "
            f"found {producer_report.get('schema_version')!r}"
        )
    if producer_report.get("run_id") != run_id:
        errors.append(
            f"producer_report.run_id: expected {run_id}, found {producer_report.get('run_id')!r}"
        )
    if producer_report.get("ok") is not True:
        errors.append("producer_report.ok: expected true")
    if producer_report.get("artifact_written") is not True:
        errors.append("producer_report.artifact_written: expected true")
    report_errors = producer_report.get("errors")
    if isinstance(report_errors, list) and report_errors:
        errors.extend(f"producer_report.errors: {error}" for error in report_errors)
    report_warnings = producer_report.get("warnings")
    if isinstance(report_warnings, list):
        warnings.extend(f"producer_report.warnings: {warning}" for warning in report_warnings)


def _validate_boundaries(boundaries: dict[str, Any], errors: list[str]) -> None:
    for key in sorted(REQUIRED_TRUE_BOUNDARIES):
        if boundaries.get(key) is not True:
            errors.append(f"artifact.boundaries.{key}: expected true")
    for key in sorted(REQUIRED_FALSE_BOUNDARIES):
        if boundaries.get(key) is not False:
            errors.append(f"artifact.boundaries.{key}: expected false")


def _no_ingest_boundary_coverage(
    source_rows: list[dict[str, Any]],
    errors: list[str],
) -> dict[str, Any]:
    content_ingest_ids: list[str] = []
    missing_boundary_ids: list[str] = []
    blocker_ids: list[str] = []
    for index, row in enumerate(source_rows):
        source_id = str(row.get("source_id") or f"row-{index}")
        rights_class = str(row.get("source_rights_class") or "")
        boundary = str(row.get("declared_use_boundary") or "").lower()
        blocking_notes = str(row.get("blocking_notes") or "").lower()
        if rights_class == "content_ingest":
            content_ingest_ids.append(source_id)
            errors.append(f"source_rights_registry[{index}].source_rights_class: content_ingest blocked")
        if "no " not in boundary and "blocked" not in boundary:
            missing_boundary_ids.append(source_id)
            errors.append(
                f"source_rights_registry[{index}].declared_use_boundary: "
                "must explicitly block content ingest"
            )
        if "blocked" in boundary or "blocked" in blocking_notes:
            blocker_ids.append(source_id)

    return {
        "sources_total": len(source_rows),
        "explicit_no_ingest_source_count": len(source_rows) - len(missing_boundary_ids),
        "missing_explicit_block_count": len(missing_boundary_ids),
        "missing_explicit_block_source_ids": sorted(missing_boundary_ids),
        "content_ingest_source_count": len(content_ingest_ids),
        "content_ingest_source_ids": sorted(content_ingest_ids),
        "blocker_source_count": len(set(blocker_ids)),
        "blocker_source_ids": sorted(set(blocker_ids)),
    }


def _object_value(payload: dict[str, Any], key: str, errors: list[str]) -> dict[str, Any]:
    value = payload.get(key)
    if not isinstance(value, dict):
        errors.append(f"artifact.{key}: expected object")
        return {}
    return value


def _list_value(payload: dict[str, Any], key: str, errors: list[str]) -> list[dict[str, Any]]:
    value = payload.get(key)
    if not isinstance(value, list):
        errors.append(f"artifact.{key}: expected array")
        return []
    rows = [row for row in value if isinstance(row, dict)]
    if len(rows) != len(value):
        errors.append(f"artifact.{key}: all rows must be objects")
    return rows


def _counter_dict(values: Any) -> dict[str, int]:
    counter = Counter(str(value) for value in values if value not in (None, ""))
    return {key: counter[key] for key in sorted(counter)}


def _resolve_run_id(
    *,
    root: Path,
    run_id: str | None,
    artifact_path: Path | None,
    producer_report_path: Path | None,
) -> str:
    if run_id is not None:
        return _run_id(run_id)
    for path in (artifact_path, producer_report_path):
        if path is not None:
            return _run_id(path.parent.name)
    latest = _latest_staging_run_id(root)
    if latest is None:
        raise ValueError("no shadow staging runs found; pass --run-id or --artifact")
    return latest


def _latest_staging_run_id(root: Path) -> str | None:
    staging_root = (root / SHADOW_STAGING_ROOT).resolve()
    if not staging_root.is_dir():
        return None
    candidates = sorted(path.name for path in staging_root.iterdir() if path.is_dir())
    return candidates[-1] if candidates else None


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


def _resolve_output_path(
    *,
    root: Path,
    run_id: str,
    output_path: Path | None,
) -> Path:
    candidate = output_path or SHADOW_STAGING_ROOT / run_id / CONSUMER_REPORT_FILENAME
    report_path = candidate.resolve() if candidate.is_absolute() else (root / candidate).resolve()
    allowed_root = (root / SHADOW_STAGING_ROOT).resolve()
    try:
        relative_parts = report_path.relative_to(allowed_root).parts
    except ValueError as exc:
        raise ValueError("report path must stay inside the shadow staging report directory") from exc
    if len(relative_parts) != 2 or relative_parts[0] != run_id:
        raise ValueError("report path must be scoped to the current shadow staging run id")
    if relative_parts[1] != CONSUMER_REPORT_FILENAME:
        raise ValueError(f"report filename must be {CONSUMER_REPORT_FILENAME}")
    return report_path


def _load_json_object(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path}: expected a JSON object")
    return payload


def _repo_root(value: str | Path | None) -> Path:
    if value is not None:
        return Path(value).resolve()
    return Path(__file__).resolve().parents[3]


def _run_id(value: str) -> str:
    if not RUN_ID_RE.fullmatch(value):
        raise ValueError("run_id must contain only letters, digits, underscore, dot, or dash")
    return value


def _utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _relative_to_root(path: Path, root: Path) -> str:
    return path.resolve().relative_to(root).as_posix()


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
