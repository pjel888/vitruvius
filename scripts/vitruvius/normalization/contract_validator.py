"""Sprint CLEANUP-1 Stream C1.1 — Ingestion → Refinement contract validator.

Validates Phase 1B sidecar JSON output against the v2.0.0 frozen contract
in .ai/09_archive/plans/ingestion-refinement-contract.md. Returns a
ContractValidationReport with ok=True iff every required field is
present and every nested sub-object is complete.

Gated behind `p1c_contract_validator` in config/vitruvius.yaml. When
the flag is off the validator is bypassed entirely (flag-OFF =
pre-CLEANUP-1 behavior byte-identical).

Perf call: pure dict traversal, no compute — above the Rust Line per
AD-036. Python is the correct choice.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Tuple

REQUIRED_FIELDS: Tuple[str, ...] = (
    "source_path",
    "file_type",
    "document_class",
    "parser_id",
    "confidence_score",
    "pages_total",
    "pages_processed",
    "markdown_path",
    "assets_extracted",
    "structural_context",
    "versioning",
    "manual_review",
)

REQUIRED_VERSIONING_KEYS: Tuple[str, ...] = (
    "parser_version",
    "pipeline_version",
    "config_version",
)

REQUIRED_MANUAL_REVIEW_KEYS: Tuple[str, ...] = ("required", "reason")


@dataclass(frozen=True)
class ContractValidationReport:
    ok: bool
    missing_fields: Tuple[str, ...] = ()
    nested_errors: Tuple[str, ...] = ()


def validate_sidecar_json(path: Path) -> ContractValidationReport:
    """Validate a Phase 1B sidecar JSON file against the v2.0.0 contract.

    Returns ContractValidationReport(ok=True) iff every required field
    is present and every nested object is complete. Any parse error,
    missing field, or incomplete nested object returns ok=False with
    a populated missing_fields / nested_errors tuple.
    """
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        return ContractValidationReport(
            ok=False,
            nested_errors=(f"failed to parse sidecar JSON: {exc}",),
        )

    if not isinstance(data, dict):
        return ContractValidationReport(
            ok=False,
            nested_errors=("sidecar root is not a JSON object",),
        )

    missing = tuple(f for f in REQUIRED_FIELDS if f not in data)
    nested: list[str] = []

    versioning = data.get("versioning")
    if isinstance(versioning, dict):
        for key in REQUIRED_VERSIONING_KEYS:
            if key not in versioning:
                nested.append(f"versioning.{key} missing")
    elif "versioning" in data:
        nested.append("versioning is not a JSON object")

    manual_review = data.get("manual_review")
    if isinstance(manual_review, dict):
        for key in REQUIRED_MANUAL_REVIEW_KEYS:
            if key not in manual_review:
                nested.append(f"manual_review.{key} missing")
    elif "manual_review" in data:
        nested.append("manual_review is not a JSON object")

    ok = not missing and not nested
    return ContractValidationReport(
        ok=ok,
        missing_fields=missing,
        nested_errors=tuple(nested),
    )
