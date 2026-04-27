"""Protected-source admission preflight for AEC-MEPFS.

This module proves the current source admission lane remains metadata-only and
zero-content. It reads existing source-rights/currentness artifacts, validates
that no protected content payload is present, and writes an auditable report. It
never ingests source text, calls external URLs, mutates Neo4j, or rebuilds KG
artifacts.
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import re
import sys
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Sequence

from vitruvius.kg.backbone_contracts import validate_backbone_contract


REPORT_SCHEMA_VERSION = "aec-mepfs-protected-source-admission/v1"
REPORT_ROOT = Path("006_System-Manifests/aec-mepfs-backbone/source-admission")
REPORT_FILENAME = "source-admission-report.json"
RUN_ID_RE = re.compile(r"^[A-Za-z0-9_.-]+$")

DEFAULT_SOURCE_RIGHTS_REGISTRY_PATH = Path(
    ".ai/03_plans/AEC-MEPFS-Backbone/registry-candidates/source-rights-registry.json"
)
DEFAULT_CURRENTNESS_REPORT_PATH = Path(
    "006_System-Manifests/aec-mepfs-backbone/source-currentness/20260425T140712Z/source-currentness-report.json"
)
DEFAULT_MANUAL_CURRENTNESS_REPORT_PATH = Path(
    "006_System-Manifests/aec-mepfs-backbone/source-currentness/20260425T144600Z/manual-currentness-resolution-report.json"
)

METADATA_ONLY_CLASSES = {"reference_only", "metadata_crosswalk"}
CONTENT_INGEST_CLASS = "content_ingest"
CONTENT_INGEST_INTENT_FIELDS = {
    "allowed_use_class",
    "intended_use",
    "max_admitted_use",
    "source_rights_class",
}
PROTECTED_PAYLOAD_KEYS = {
    "body",
    "clause",
    "clauses",
    "source_text",
    "sourceText",
    "source_payload",
    "sourcePayload",
    "protected_text",
    "protectedText",
    "protected_content",
    "protectedContent",
    "protected_source_text",
    "protectedSourceText",
    "clause_text",
    "clauseText",
    "table_data",
    "tableData",
    "figure_data",
    "figureData",
    "dataset_payload",
    "datasetPayload",
    "dataset",
    "datasets",
    "raw_text",
    "rawText",
    "full_text",
    "fullText",
    "payload",
    "text",
    "content",
    "table",
    "tables",
    "figure",
    "figures",
    "local_cache_path",
    "localCachePath",
}


def run_source_admission_preflight(
    *,
    repo_root: str | Path | None = None,
    run_id: str | None = None,
    output_path: str | Path | None = None,
    source_rights_registry_path: str | Path = DEFAULT_SOURCE_RIGHTS_REGISTRY_PATH,
    currentness_report_path: str | Path = DEFAULT_CURRENTNESS_REPORT_PATH,
    manual_currentness_report_path: str | Path = DEFAULT_MANUAL_CURRENTNESS_REPORT_PATH,
) -> dict[str, Any]:
    """Validate metadata-only protected-source admission state."""

    root = _repo_root(repo_root)
    resolved_run_id = _run_id(run_id)
    report_path = _resolve_report_path(root, resolved_run_id, Path(output_path) if output_path else None)
    registry_path = _resolve_existing_file(root, Path(source_rights_registry_path), "source rights registry")
    currentness_path = _resolve_existing_file(root, Path(currentness_report_path), "currentness report")
    manual_path = _resolve_existing_file(root, Path(manual_currentness_report_path), "manual currentness report")

    registry_payload = _read_json_object(registry_path, "source rights registry")
    currentness_payload = _read_json_object(currentness_path, "currentness report")
    manual_payload = _read_json_object(manual_path, "manual currentness report")

    source_rows = _list_section(registry_payload, "source_rights_registry")
    currentness_rows = _list_section(currentness_payload, "rows")
    manual_rows = _list_section(manual_payload, "rows")
    contract_report = validate_backbone_contract(registry_payload).to_dict()

    source_ids = [str(row.get("source_id", "")) for row in source_rows if isinstance(row, dict)]
    currentness_source_ids = {
        str(row.get("source_id", "")) for row in currentness_rows if isinstance(row, dict)
    }
    manual_source_ids = {
        str(row.get("source_id", "")) for row in manual_rows if isinstance(row, dict)
    }
    missing_currentness = sorted(source_id for source_id in source_ids if source_id not in currentness_source_ids)

    content_ingest_rows = [
        _row_ref(index, row)
        for index, row in enumerate(source_rows)
        if isinstance(row, dict) and _claims_content_ingest(row)
    ]
    non_metadata_classes = [
        _row_ref(index, row)
        for index, row in enumerate(source_rows)
        if isinstance(row, dict) and row.get("source_rights_class") not in METADATA_ONLY_CLASSES
    ]
    protected_payload_key_hits = _protected_payload_key_hits(
        {
            "source_rights_registry": registry_payload,
            "currentness_report": currentness_payload,
            "manual_currentness_report": manual_payload,
        }
    )

    clearance_counts = Counter(
        str(row.get("clearance_state", "")) for row in source_rows if isinstance(row, dict)
    )
    rights_class_counts = Counter(
        str(row.get("source_rights_class", "")) for row in source_rows if isinstance(row, dict)
    )
    declared_boundaries = [
        str(row.get("declared_use_boundary", "")) for row in source_rows if isinstance(row, dict)
    ]
    rows_with_no_ingest_boundary = sum(
        1 for boundary in declared_boundaries if _declares_no_content_ingest(boundary)
    )

    errors: list[str] = []
    if not contract_report["ok"]:
        errors.extend(f"contract: {error}" for error in contract_report["errors"])
    if missing_currentness:
        errors.append(
            "currentness coverage: missing source ids " + ", ".join(missing_currentness)
        )
    if content_ingest_rows:
        errors.append(
            "source_rights_registry: content_ingest rows remain blocked ("
            + ", ".join(content_ingest_rows)
            + ")"
        )
    if non_metadata_classes:
        errors.append(
            "source_rights_registry: non metadata/reference classes found ("
            + ", ".join(non_metadata_classes)
            + ")"
        )
    if protected_payload_key_hits:
        errors.append("protected payload keys found in source admission artifacts")
    if rows_with_no_ingest_boundary != len(source_rows):
        errors.append(
            "source_rights_registry: every row must declare a no-content-ingest boundary"
        )

    report = {
        "schema_version": REPORT_SCHEMA_VERSION,
        "ok": not errors,
        "run_id": resolved_run_id,
        "generated_at_utc": _utc_now(),
        "report_path": _relative_to_root(report_path, root),
        "authority": {
            "packet": ".ai/03_plans/AEC-MEPFS-Backbone/2026-04-27_protected_source_admission_packet.md",
            "classification": "GREEN_METADATA_ONLY_ZERO_CONTENT_PROOF",
            "protected_content_ingest_authorized": False,
            "canonical_content_admission_authorized": False,
            "global_live_authorization": False,
        },
        "inputs": {
            "source_rights_registry": _relative_to_root(registry_path, root),
            "currentness_report": _relative_to_root(currentness_path, root),
            "manual_currentness_report": _relative_to_root(manual_path, root),
        },
        "summary": {
            "source_rights_rows": len(source_rows),
            "currentness_rows": len(currentness_rows),
            "manual_currentness_rows": len(manual_rows),
            "source_rights_classes": dict(sorted(rights_class_counts.items())),
            "clearance_states": dict(sorted(clearance_counts.items())),
            "metadata_only_rows": sum(rights_class_counts.get(value, 0) for value in METADATA_ONLY_CLASSES),
            "content_ingest_rows": len(content_ingest_rows),
            "protected_payload_key_hits": len(protected_payload_key_hits),
            "missing_currentness_rows": len(missing_currentness),
            "rows_with_no_ingest_boundary": rows_with_no_ingest_boundary,
        },
        "status": {
            "metadataReferenceAdmissionPrepared": not errors,
            "protectedContentIngestAuthorized": False,
            "canonicalContentAdmissionAuthorized": False,
            "sourcePayloadExposureAuthorized": False,
            "contentIngestExternalBlocked": True,
            "runtimeSurfaceClaimsMade": False,
            "nextRequiredAuthority": "source-specific legal/licensing/steward record for exact protected payload fields",
        },
        "coverage": {
            "registry_source_ids": sorted(source_ids),
            "currentness_source_ids": sorted(currentness_source_ids),
            "manual_currentness_source_ids": sorted(manual_source_ids),
            "missing_currentness_source_ids": missing_currentness,
        },
        "zero_content_ingest_proof": {
            "content_ingest_rows": content_ingest_rows,
            "non_metadata_classes": non_metadata_classes,
            "protected_payload_key_hits": protected_payload_key_hits,
            "declared_boundaries_checked": len(declared_boundaries),
        },
        "contract_report": contract_report,
        "safety_invariants": {
            "protectedContentIngestIntent": bool(content_ingest_rows),
            "protectedPayloadStoredInAdmissionArtifacts": bool(protected_payload_key_hits),
            "canonicalContentAdmissionAuthorized": False,
            "globalLiveAuthorization": False,
        },
        "runtime_surface_scope": {
            "apiExplorerPayloadExposureChecked": False,
            "neo4jMutationChecked": False,
            "kgRebuildChecked": False,
            "reason": "source-admission preflight validates metadata artifacts only; API, Explorer, Neo4j, and KG behavior remain covered by their dedicated lane tests and packets",
        },
        "external_blockers": [
            "protected content ingest requires source-specific legal/licensing/steward approval",
            "local source payload caches require terms and retention policy",
            "canonical source content admission requires separate packet and rollback/removal path",
        ],
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
        description="Generate AEC-MEPFS protected-source admission preflight evidence."
    )
    parser.add_argument("--repo-root", default=None)
    parser.add_argument("--run-id", default=None)
    parser.add_argument("--output", default=None)
    parser.add_argument("--source-rights-registry", default=str(DEFAULT_SOURCE_RIGHTS_REGISTRY_PATH))
    parser.add_argument("--currentness-report", default=str(DEFAULT_CURRENTNESS_REPORT_PATH))
    parser.add_argument("--manual-currentness-report", default=str(DEFAULT_MANUAL_CURRENTNESS_REPORT_PATH))
    args = parser.parse_args(argv)

    try:
        report = run_source_admission_preflight(
            repo_root=args.repo_root,
            run_id=args.run_id,
            output_path=args.output,
            source_rights_registry_path=args.source_rights_registry,
            currentness_report_path=args.currentness_report,
            manual_currentness_report_path=args.manual_currentness_report,
        )
    except (FileNotFoundError, ValueError) as exc:
        print(json.dumps({"ok": False, "errors": [str(exc)]}, indent=2, sort_keys=True))
        return 1

    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["ok"] else 1


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
    candidate = output_path or (REPORT_ROOT / run_id / REPORT_FILENAME)
    report_path = candidate.resolve() if candidate.is_absolute() else (root / candidate).resolve()
    allowed_root = (root / REPORT_ROOT).resolve()
    try:
        relative_parts = report_path.relative_to(allowed_root).parts
    except ValueError as exc:
        raise ValueError("report path must stay inside the source-admission evidence directory") from exc
    if len(relative_parts) != 2 or relative_parts[0] != run_id:
        raise ValueError("report path must be scoped to the current source-admission run id")
    if relative_parts[1] != REPORT_FILENAME:
        raise ValueError(f"report filename must be {REPORT_FILENAME}")
    return report_path


def _read_json_object(path: Path, label: str) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{label} must be a JSON object")
    return payload


def _list_section(payload: dict[str, Any], key: str) -> list[Any]:
    value = payload.get(key, [])
    if not isinstance(value, list):
        raise ValueError(f"{key} must be a list")
    return value


def _row_ref(index: int, row: dict[str, Any]) -> str:
    source_id = str(row.get("source_id") or f"row-{index}")
    return f"{index}:{source_id}"


def _declares_no_content_ingest(boundary: str) -> bool:
    normalized = boundary.lower()
    if not normalized.strip():
        return False
    return any(token in normalized for token in ("no ", "blocked", "not ")) and any(
        token in normalized for token in ("ingest", "cache", "copy", "redistribution", "text", "table", "figure", "clause", "dataset")
    )


def _claims_content_ingest(row: dict[str, Any]) -> bool:
    return any(
        str(row.get(field_name, "")).strip() == CONTENT_INGEST_CLASS
        for field_name in CONTENT_INGEST_INTENT_FIELDS
    )


def _protected_payload_key_hits(payloads: dict[str, Any]) -> list[dict[str, str]]:
    hits: list[dict[str, str]] = []
    for label, payload in payloads.items():
        for path, key in _iter_keys(payload):
            if key in PROTECTED_PAYLOAD_KEYS:
                hits.append({"artifact": label, "path": path, "key": key})
    return sorted(hits, key=lambda item: (item["artifact"], item["path"], item["key"]))


def _iter_keys(value: Any, prefix: str = "$") -> Iterable[tuple[str, str]]:
    if isinstance(value, dict):
        for key, child in value.items():
            key_str = str(key)
            path = f"{prefix}.{key_str}"
            yield path, key_str
            yield from _iter_keys(child, path)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from _iter_keys(child, f"{prefix}[{index}]")


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
