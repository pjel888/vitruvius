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
    owner_coverage: Coverage = field(default_factory=Coverage)
    source_rights_coverage: Coverage = field(default_factory=Coverage)

    @property
    def passed(self) -> bool:
        return self.ok

    def finalize(self) -> "BackboneContractReport":
        self.errors = sorted(self.errors)
        self.warnings = sorted(self.warnings)
        self.record_counts = dict(sorted(self.record_counts.items()))
        self.predicate_counts = dict(sorted(self.predicate_counts.items()))
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
            "owner_coverage": report.owner_coverage.to_dict(),
            "source_rights_coverage": report.source_rights_coverage.to_dict(),
        }


def validate_backbone_contract(payload: dict[str, Any]) -> BackboneContractReport:
    """Validate a candidate backbone registry payload."""
    records = _as_list(payload.get("records"))
    relationships = _as_list(payload.get("relationships"))
    source_mappings = _as_list(payload.get("source_mappings"))

    report = BackboneContractReport()
    report.record_counts = _record_counts(records)
    report.predicate_counts = _predicate_counts(relationships)
    report.owner_coverage = _owner_coverage(records)
    report.source_rights_coverage = _source_rights_coverage(source_mappings)

    for index, record in enumerate(records):
        _validate_record(record, f"records[{index}]", report)

    for index, relationship in enumerate(relationships):
        _validate_relationship(relationship, f"relationships[{index}]", report)

    for index, source_mapping in enumerate(source_mappings):
        _validate_source_mapping(source_mapping, f"source_mappings[{index}]", report)

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
    for field_name in sorted(SOURCE_MAPPING_FIELDS):
        if not _has_value(source_mapping.get(field_name)):
            report.errors.append(f"{path}.{field_name}: required field missing")

    if _claims_content_ingest(source_mapping) and source_mapping.get("clearance_state") != "cleared_for_declared_use":
        report.errors.append(
            f"{path}: content_ingest requires clearance_state 'cleared_for_declared_use'"
        )


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


def _claims_content_ingest(record: dict[str, Any]) -> bool:
    fields = (
        "allowed_use_class",
        "intended_use",
        "max_admitted_use",
        "source_rights_class",
    )
    return any(str(record.get(field_name, "")).strip() == "content_ingest" for field_name in fields)


def _as_list(value: Any) -> list[dict[str, Any]]:
    if value is None:
        return []
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, dict)]


def _has_value(value: Any) -> bool:
    return value is not None and str(value).strip() != ""


def _normalize_predicate(value: Any) -> str:
    return str(value or "").strip().lower()
