"""Static contract checks for candidate AEC-MEPFS Backbone registry records.

This module is intentionally file-backed and runtime-disconnected. It validates
future backbone registry fixtures before any KG schema, loader, API, Explorer,
or Neo4j path consumes them.
"""

from __future__ import annotations

import json
import re
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


VTN_ID_RE = re.compile(
    r"^VTN-(DOM|CON|RUL|DEF|PRO|EXC|JUR|AUT|ADF|ADE|APP|OVR|STD|MAP|LOC|REL)-\d{7}$"
)

GOVERNED_PREDICATES = {
    "applicable_in_jurisdiction",
    "broader_than",
    "conflicts_with",
    "constrains",
    "evidenced_by",
    "governs",
    "has_facet",
    "maps_to_external_standard",
    "narrower_than",
    "part_of",
    "requires",
    "supersedes",
}

VAGUE_PREDICATES = {
    "affects",
    "connected_to",
    "related_to",
    "similar_to",
}

SOURCE_MAPPING_FIELDS = {
    "clearance_state",
    "currentness_check_date",
    "official_url",
    "source_rights_class",
}

REQUIRED_RECORD_FIELDS = {
    "id",
    "label",
    "owner",
    "record_type",
    "review_status",
}

CANONICAL_RECORD_TYPES = {
    "BackboneNode",
    "CanonicalConcept",
}

JURISDICTION_FIELDS = {
    "barangay",
    "city",
    "country",
    "jurisdiction",
    "jurisdiction_scope",
    "locality",
    "province",
    "region",
}

PREDICATE_REGISTRY_FIELDS = {
    "allowed_strength_classes",
    "category",
    "direction",
    "domain_classes",
    "evidence_required_fields",
    "examples",
    "migration_behavior",
    "non_examples",
    "owner",
    "predicate",
    "range_classes",
    "validation_rule",
}

SOURCE_RIGHTS_REGISTRY_FIELDS = {
    "blocking_notes",
    "clearance_state",
    "currentness_check_date",
    "declared_use_boundary",
    "edition_version_effective_date",
    "intended_vitruvius_use",
    "official_url",
    "publisher_authority",
    "source_family",
    "source_id",
    "source_rights_class",
    "steward_owner",
    "update_cadence",
}

AUTHORING_MIGRATION_CASE_FIELDS = {
    "case_id",
    "case_type",
    "expected_output",
    "input",
    "owner",
    "rationale",
    "review_status",
    "source_evidence",
}

RESOLVER_GOLDEN_CASE_FIELDS = {
    "case_id",
    "effective_date",
    "expected_confidence",
    "expected_result_type",
    "jurisdiction",
    "owner",
    "query",
    "rationale",
    "review_status",
    "source_evidence",
}

API_EXPLORER_PARITY_CASE_FIELDS = {
    "case_id",
    "expected_shape",
    "expected_status",
    "method",
    "owner",
    "request",
    "review_status",
    "route",
    "surface",
}

SHADOW_ROLLBACK_PLAN_FIELDS = {
    "backup_export_command",
    "destructive_operations_blocked",
    "owner",
    "restore_command",
    "rollback_decision_gate",
    "review_status",
    "smoke_queries",
}

CLEARANCE_STATES = {
    "planning_reference_only",
    "metadata_crosswalk_planned",
    "clearance_required",
    "cleared_for_declared_use",
    "rejected_for_local_use",
    "unverified_currentness",
}

SOURCE_RIGHTS_CLASSES = {
    "reference_only",
    "metadata_crosswalk",
    "summary_extract",
    "content_ingest",
    "public-law",
    "open-reference",
    "open-free-with-attribution",
    "licensed-crosswalk",
    "subscription-text",
    "contextual-only",
    "deferred",
}

RESOLVER_RESULT_TYPES = {"single_value", "composed", "conflict", "none"}
RESOLVER_CONFIDENCE_CLASSES = {"deterministic", "review_required", "insufficient"}
HTTP_METHODS = {"GET", "POST"}
API_EXPLORER_SURFACES = {"v1", "v2"}

LIST_SECTIONS = {
    "api_explorer_parity_cases",
    "authoring_migration_cases",
    "predicate_registry",
    "records",
    "relationships",
    "resolver_golden_cases",
    "source_mappings",
    "source_rights_registry",
}


@dataclass(frozen=True)
class Coverage:
    """Coverage count for required fields."""

    present: int = 0
    total: int = 0

    @property
    def ratio(self) -> float:
        if self.total == 0:
            return 1.0
        return round(self.present / self.total, 4)

    def to_dict(self) -> dict[str, int | float]:
        return {
            "present": self.present,
            "total": self.total,
            "ratio": self.ratio,
        }


@dataclass
class BackboneContractReport:
    """Validation report for a candidate backbone registry payload."""

    ok: bool = True
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    record_counts: dict[str, int] = field(default_factory=dict)
    predicate_counts: dict[str, int] = field(default_factory=dict)
    readiness_case_counts: dict[str, int] = field(default_factory=dict)
    owner_coverage: Coverage = field(default_factory=Coverage)
    source_rights_coverage: Coverage = field(default_factory=Coverage)
    source_rights_registry_coverage: Coverage = field(default_factory=Coverage)
    predicate_registry_coverage: Coverage = field(default_factory=Coverage)

    @property
    def passed(self) -> bool:
        return self.ok

    def finalize(self) -> "BackboneContractReport":
        self.errors = sorted(self.errors)
        self.warnings = sorted(self.warnings)
        self.record_counts = dict(sorted(self.record_counts.items()))
        self.predicate_counts = dict(sorted(self.predicate_counts.items()))
        self.readiness_case_counts = dict(sorted(self.readiness_case_counts.items()))
        self.ok = not self.errors
        return self

    def to_dict(self) -> dict[str, Any]:
        report = self.finalize()
        return {
            "ok": report.ok,
            "errors": report.errors,
            "warnings": report.warnings,
            "record_counts": report.record_counts,
            "predicate_counts": report.predicate_counts,
            "readiness_case_counts": report.readiness_case_counts,
            "owner_coverage": report.owner_coverage.to_dict(),
            "source_rights_coverage": report.source_rights_coverage.to_dict(),
            "source_rights_registry_coverage": report.source_rights_registry_coverage.to_dict(),
            "predicate_registry_coverage": report.predicate_registry_coverage.to_dict(),
        }


def validate_backbone_contract(payload: dict[str, Any]) -> BackboneContractReport:
    """Validate a candidate backbone registry payload."""
    report = BackboneContractReport()
    _validate_list_sections(payload, report)

    records = _as_list(payload.get("records"))
    relationships = _as_list(payload.get("relationships"))
    source_mappings = _as_list(payload.get("source_mappings"))
    source_rights_registry = _as_list(payload.get("source_rights_registry"))
    predicate_registry = _as_list(payload.get("predicate_registry"))
    authoring_migration_cases = _as_list(payload.get("authoring_migration_cases"))
    resolver_golden_cases = _as_list(payload.get("resolver_golden_cases"))
    api_explorer_parity_cases = _as_list(payload.get("api_explorer_parity_cases"))

    report.record_counts = _record_counts(records)
    report.predicate_counts = _predicate_counts(relationships)
    report.readiness_case_counts = _readiness_case_counts(
        authoring_migration_cases,
        resolver_golden_cases,
        api_explorer_parity_cases,
    )
    report.owner_coverage = _owner_coverage(records)
    report.source_rights_coverage = _source_rights_coverage(source_mappings)
    report.source_rights_registry_coverage = _required_field_coverage(
        source_rights_registry,
        SOURCE_RIGHTS_REGISTRY_FIELDS,
    )
    report.predicate_registry_coverage = _required_field_coverage(
        predicate_registry,
        PREDICATE_REGISTRY_FIELDS,
    )

    for index, record in enumerate(records):
        _validate_record(record, f"records[{index}]", report)

    for index, relationship in enumerate(relationships):
        _validate_relationship(relationship, f"relationships[{index}]", report)

    for index, source_mapping in enumerate(source_mappings):
        _validate_source_mapping(source_mapping, f"source_mappings[{index}]", report)

    for index, source_row in enumerate(source_rights_registry):
        _validate_source_rights_registry_row(
            source_row,
            f"source_rights_registry[{index}]",
            report,
        )

    for index, predicate_entry in enumerate(predicate_registry):
        _validate_predicate_registry_entry(
            predicate_entry,
            f"predicate_registry[{index}]",
            report,
        )

    for index, case in enumerate(authoring_migration_cases):
        _validate_authoring_migration_case(
            case,
            f"authoring_migration_cases[{index}]",
            report,
        )

    for index, case in enumerate(resolver_golden_cases):
        _validate_resolver_golden_case(
            case,
            f"resolver_golden_cases[{index}]",
            report,
        )
    _validate_resolver_case_coverage(resolver_golden_cases, report)

    for index, case in enumerate(api_explorer_parity_cases):
        _validate_api_explorer_parity_case(
            case,
            f"api_explorer_parity_cases[{index}]",
            report,
        )

    _validate_shadow_rollback_plan(payload.get("shadow_rollback_plan"), report)

    return report.finalize()


def validate_backbone_contract_file(path: str | Path) -> BackboneContractReport:
    """Read and validate a JSON candidate backbone registry fixture."""
    fixture_path = Path(path)
    payload = json.loads(fixture_path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        report = BackboneContractReport()
        report.errors.append("payload: expected a JSON object")
        return report.finalize()
    return validate_backbone_contract(payload)


def _validate_record(record: dict[str, Any], path: str, report: BackboneContractReport) -> None:
    missing = sorted(field for field in REQUIRED_RECORD_FIELDS if not _has_value(record.get(field)))
    for field_name in missing:
        report.errors.append(f"{path}.{field_name}: required field missing")

    record_id = str(record.get("id", ""))
    if record_id and not VTN_ID_RE.match(record_id):
        report.errors.append(f"{path}.id: '{record_id}' does not match VTN-<kind>-<7 digits>")

    record_type = str(record.get("record_type", ""))
    if record_type in CANONICAL_RECORD_TYPES:
        present_jurisdiction_fields = sorted(
            field_name for field_name in JURISDICTION_FIELDS if _has_value(record.get(field_name))
        )
        if present_jurisdiction_fields:
            joined = ", ".join(present_jurisdiction_fields)
            report.errors.append(
                f"{path}: canonical records must not carry jurisdiction fields ({joined})"
            )


def _validate_relationship(
    relationship: dict[str, Any],
    path: str,
    report: BackboneContractReport,
) -> None:
    for field_name in ("from_id", "to_id"):
        value = relationship.get(field_name)
        if not _has_value(value):
            report.errors.append(f"{path}.{field_name}: required field missing")
        elif not VTN_ID_RE.match(str(value)):
            report.errors.append(f"{path}.{field_name}: '{value}' does not match VTN ID pattern")

    predicate = _normalize_predicate(relationship.get("predicate") or relationship.get("edge_type"))
    if not predicate:
        report.errors.append(f"{path}.predicate: required field missing")
        return

    is_governed = bool(relationship.get("governed", True))
    if is_governed and predicate in VAGUE_PREDICATES:
        report.errors.append(f"{path}.predicate: vague governed predicate '{predicate}' is blocked")
        return

    if is_governed and predicate not in GOVERNED_PREDICATES:
        report.errors.append(f"{path}.predicate: unknown governed predicate '{predicate}'")


def _validate_source_mapping(
    source_mapping: dict[str, Any],
    path: str,
    report: BackboneContractReport,
) -> None:
    source_mapping_id = source_mapping.get("id")
    if _has_value(source_mapping_id) and not VTN_ID_RE.match(str(source_mapping_id)):
        report.errors.append(f"{path}.id: '{source_mapping_id}' does not match VTN ID pattern")

    for field_name in sorted(SOURCE_MAPPING_FIELDS):
        if not _has_value(source_mapping.get(field_name)):
            report.errors.append(f"{path}.{field_name}: required field missing")

    if (
        _claims_content_ingest(source_mapping)
        and source_mapping.get("clearance_state") != "cleared_for_declared_use"
    ):
        report.errors.append(
            f"{path}: content_ingest requires clearance_state 'cleared_for_declared_use'"
        )


def _validate_source_rights_registry_row(
    row: dict[str, Any],
    path: str,
    report: BackboneContractReport,
) -> None:
    _validate_required_fields(row, SOURCE_RIGHTS_REGISTRY_FIELDS, path, report)
    _validate_enum(row, "clearance_state", CLEARANCE_STATES, path, report)
    _validate_enum(row, "source_rights_class", SOURCE_RIGHTS_CLASSES, path, report)

    if _claims_content_ingest(row) and row.get("clearance_state") != "cleared_for_declared_use":
        report.errors.append(
            f"{path}: content_ingest requires clearance_state 'cleared_for_declared_use'"
        )

    if _claims_content_ingest(row):
        for field_name in ("legal_reviewer", "reviewer_decision"):
            if not _has_value(row.get(field_name)):
                report.errors.append(f"{path}.{field_name}: required for content_ingest")


def _validate_predicate_registry_entry(
    entry: dict[str, Any],
    path: str,
    report: BackboneContractReport,
) -> None:
    _validate_required_fields(entry, PREDICATE_REGISTRY_FIELDS, path, report)

    predicate = _normalize_predicate(entry.get("predicate"))
    if predicate in VAGUE_PREDICATES:
        report.errors.append(f"{path}.predicate: vague predicate '{predicate}' is blocked")
    elif predicate and predicate not in GOVERNED_PREDICATES:
        report.errors.append(f"{path}.predicate: unknown governed predicate '{predicate}'")

    for field_name in (
        "allowed_strength_classes",
        "domain_classes",
        "evidence_required_fields",
        "examples",
        "non_examples",
        "range_classes",
    ):
        if field_name in entry and not _has_list_items(entry.get(field_name)):
            report.errors.append(f"{path}.{field_name}: expected a non-empty list")


def _validate_authoring_migration_case(
    case: dict[str, Any],
    path: str,
    report: BackboneContractReport,
) -> None:
    _validate_required_fields(case, AUTHORING_MIGRATION_CASE_FIELDS, path, report)

    proposal_level = str(case.get("proposal_level", "")).upper()
    proposed_by = str(case.get("proposed_by", "")).strip().lower()
    if proposal_level in {"L1", "L2"} and proposed_by == "ai":
        report.errors.append(f"{path}: AI-authored {proposal_level} changes are blocked")

    if _as_bool(case.get("auto_accept")):
        confidence = _as_float(case.get("confidence"))
        workflow = str(case.get("workflow", "")).strip()
        if proposal_level not in {"L3", "L4"}:
            report.errors.append(f"{path}: auto_accept is only allowed for L3/L4 proposals")
        if confidence is None or confidence < 0.92:
            report.errors.append(f"{path}: auto_accept requires confidence >= 0.92")
        if workflow != "LD-8 PlacementAssertion":
            report.errors.append(f"{path}: auto_accept requires LD-8 PlacementAssertion workflow")


def _validate_resolver_golden_case(
    case: dict[str, Any],
    path: str,
    report: BackboneContractReport,
) -> None:
    _validate_required_fields(case, RESOLVER_GOLDEN_CASE_FIELDS, path, report)
    _validate_enum(case, "expected_result_type", RESOLVER_RESULT_TYPES, path, report)
    _validate_enum(case, "expected_confidence", RESOLVER_CONFIDENCE_CLASSES, path, report)

    for legacy_date_field in ("date", "query_date"):
        if _has_value(case.get(legacy_date_field)):
            report.errors.append(f"{path}.{legacy_date_field}: use effective_date instead")


def _validate_resolver_case_coverage(
    cases: list[dict[str, Any]],
    report: BackboneContractReport,
) -> None:
    if not cases:
        return

    present = {str(case.get("expected_result_type", "")).strip() for case in cases}
    missing = sorted(RESOLVER_RESULT_TYPES - present)
    if missing:
        joined = ", ".join(missing)
        report.errors.append(f"resolver_golden_cases: missing result-type coverage ({joined})")


def _validate_api_explorer_parity_case(
    case: dict[str, Any],
    path: str,
    report: BackboneContractReport,
) -> None:
    _validate_required_fields(case, API_EXPLORER_PARITY_CASE_FIELDS, path, report)
    _validate_enum(case, "method", HTTP_METHODS, path, report)

    route = str(case.get("route", "")).strip()
    surface = str(case.get("surface", "")).strip().lower()
    if surface and surface not in API_EXPLORER_SURFACES:
        report.errors.append(f"{path}.surface: unsupported value '{surface}'")
    if surface == "v1" and _as_bool(case.get("preserves_v1")) is not True:
        report.errors.append(f"{path}.preserves_v1: v1 parity cases must preserve v1 behavior")
    if surface == "v2":
        if not route.startswith("/v2/"):
            report.errors.append(f"{path}.route: v2 parity cases must use /v2 shadow routes")
        if _as_bool(case.get("shadow_only")) is not True:
            report.errors.append(f"{path}.shadow_only: v2 parity cases must be shadow-only")


def _validate_shadow_rollback_plan(value: Any, report: BackboneContractReport) -> None:
    if value is None:
        return
    if not isinstance(value, dict):
        report.errors.append("shadow_rollback_plan: expected a JSON object")
        return

    _validate_required_fields(value, SHADOW_ROLLBACK_PLAN_FIELDS, "shadow_rollback_plan", report)
    if _as_bool(value.get("destructive_operations_blocked")) is not True:
        report.errors.append(
            "shadow_rollback_plan.destructive_operations_blocked: must be true"
        )

    if "smoke_queries" in value and not _has_list_items(value.get("smoke_queries")):
        report.errors.append("shadow_rollback_plan.smoke_queries: expected a non-empty list")

    if str(value.get("proof_status", "")).strip() == "executed" and not _has_value(
        value.get("evidence_artifact")
    ):
        report.errors.append(
            "shadow_rollback_plan.evidence_artifact: required when proof_status is executed"
        )
    elif str(value.get("proof_status", "")).strip() != "executed":
        report.warnings.append("shadow_rollback_plan: rollback proof is planned, not executed")


def _record_counts(records: list[dict[str, Any]]) -> dict[str, int]:
    counts = Counter(str(record.get("record_type") or "unknown") for record in records)
    return dict(sorted(counts.items()))


def _predicate_counts(relationships: list[dict[str, Any]]) -> dict[str, int]:
    counts = Counter(
        _normalize_predicate(relationship.get("predicate") or relationship.get("edge_type"))
        or "unknown"
        for relationship in relationships
    )
    return dict(sorted(counts.items()))


def _owner_coverage(records: list[dict[str, Any]]) -> Coverage:
    present = sum(1 for record in records if _has_value(record.get("owner")))
    return Coverage(present=present, total=len(records))


def _source_rights_coverage(source_mappings: list[dict[str, Any]]) -> Coverage:
    present = 0
    for mapping in source_mappings:
        if all(_has_value(mapping.get(field_name)) for field_name in SOURCE_MAPPING_FIELDS):
            present += 1
    return Coverage(present=present, total=len(source_mappings))


def _required_field_coverage(
    rows: list[dict[str, Any]],
    required_fields: set[str],
) -> Coverage:
    present = 0
    for row in rows:
        if all(_has_value(row.get(field_name)) for field_name in required_fields):
            present += 1
    return Coverage(present=present, total=len(rows))


def _readiness_case_counts(
    authoring_migration_cases: list[dict[str, Any]],
    resolver_golden_cases: list[dict[str, Any]],
    api_explorer_parity_cases: list[dict[str, Any]],
) -> dict[str, int]:
    return {
        "api_explorer_parity_cases": len(api_explorer_parity_cases),
        "authoring_migration_cases": len(authoring_migration_cases),
        "resolver_golden_cases": len(resolver_golden_cases),
    }


def _claims_content_ingest(record: dict[str, Any]) -> bool:
    fields = (
        "allowed_use_class",
        "intended_use",
        "max_admitted_use",
        "source_rights_class",
    )
    return any(str(record.get(field_name, "")).strip() == "content_ingest" for field_name in fields)


def _validate_required_fields(
    row: dict[str, Any],
    required_fields: set[str],
    path: str,
    report: BackboneContractReport,
) -> None:
    for field_name in sorted(required_fields):
        if not _has_value(row.get(field_name)):
            report.errors.append(f"{path}.{field_name}: required field missing")


def _validate_enum(
    row: dict[str, Any],
    field_name: str,
    allowed_values: set[str],
    path: str,
    report: BackboneContractReport,
) -> None:
    if not _has_value(row.get(field_name)):
        return
    value = str(row.get(field_name, "")).strip()
    if value not in allowed_values:
        report.errors.append(f"{path}.{field_name}: unsupported value '{value}'")


def _validate_list_sections(payload: dict[str, Any], report: BackboneContractReport) -> None:
    for section_name in sorted(LIST_SECTIONS):
        if section_name not in payload:
            continue
        section_value = payload.get(section_name)
        if not isinstance(section_value, list):
            report.errors.append(f"{section_name}: expected a list")
            continue
        for index, item in enumerate(section_value):
            if not isinstance(item, dict):
                report.errors.append(f"{section_name}[{index}]: expected an object")


def _as_list(value: Any) -> list[dict[str, Any]]:
    if value is None:
        return []
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, dict)]


def _has_value(value: Any) -> bool:
    return value is not None and str(value).strip() != ""


def _has_list_items(value: Any) -> bool:
    return isinstance(value, list) and len(value) > 0


def _normalize_predicate(value: Any) -> str:
    return str(value or "").strip().lower()


def _as_bool(value: Any) -> bool:
    return value is True or str(value).strip().lower() == "true"


def _as_float(value: Any) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None
