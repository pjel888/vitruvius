from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from vitruvius.kg.backbone_contracts import (
    validate_backbone_contract,
    validate_backbone_contract_file,
)


FIXTURE_DIR = Path(__file__).parent / "fixtures" / "aec_mepfs_backbone"


def _valid_payload() -> dict[str, Any]:
    return json.loads((FIXTURE_DIR / "valid_minimal.json").read_text(encoding="utf-8"))


def test_valid_minimal_candidate_fixture_passes() -> None:
    report = validate_backbone_contract_file(FIXTURE_DIR / "valid_minimal.json")

    assert report.ok is True
    assert report.passed is True
    assert report.errors == []
    assert report.record_counts == {
        "BackboneNode": 1,
        "CanonicalConcept": 1,
        "Overlay": 1,
    }
    assert report.predicate_counts == {
        "applicable_in_jurisdiction": 1,
        "broader_than": 1,
    }
    assert report.owner_coverage.to_dict() == {
        "present": 3,
        "total": 3,
        "ratio": 1.0,
    }
    assert report.source_rights_coverage.to_dict() == {
        "present": 1,
        "total": 1,
        "ratio": 1.0,
    }


def test_invalid_vtn_id_fails() -> None:
    payload = _valid_payload()
    payload["records"][0]["id"] = "ARC-PH-0001"

    report = validate_backbone_contract(payload)

    assert report.ok is False
    assert any("does not match VTN-<kind>-<7 digits>" in error for error in report.errors)


def test_vague_governed_predicate_fails() -> None:
    payload = _valid_payload()
    payload["relationships"][0]["predicate"] = "RELATED_TO"

    report = validate_backbone_contract(payload)

    assert report.ok is False
    assert any("vague governed predicate 'related_to' is blocked" in error for error in report.errors)


def test_unknown_governed_predicate_fails() -> None:
    payload = _valid_payload()
    payload["relationships"][0]["predicate"] = "influences"

    report = validate_backbone_contract(payload)

    assert report.ok is False
    assert any("unknown governed predicate 'influences'" in error for error in report.errors)


def test_content_ingest_source_without_clearance_fails() -> None:
    payload = _valid_payload()
    payload["source_mappings"][0]["source_rights_class"] = "content_ingest"
    payload["source_mappings"][0]["clearance_state"] = "clearance_required"

    report = validate_backbone_contract(payload)

    assert report.ok is False
    assert any(
        "content_ingest requires clearance_state 'cleared_for_declared_use'" in error
        for error in report.errors
    )


def test_missing_owner_fails() -> None:
    payload = _valid_payload()
    payload["records"][1]["owner"] = ""

    report = validate_backbone_contract(payload)

    assert report.ok is False
    assert report.owner_coverage.to_dict() == {
        "present": 2,
        "total": 3,
        "ratio": 0.6667,
    }
    assert any("records[1].owner: required field missing" == error for error in report.errors)


def test_jurisdiction_mutated_canonical_record_fails() -> None:
    payload = _valid_payload()
    payload["records"][1]["jurisdiction_scope"] = "PH"

    report = validate_backbone_contract(payload)

    assert report.ok is False
    assert any(
        "canonical records must not carry jurisdiction fields (jurisdiction_scope)" in error
        for error in report.errors
    )


def test_report_ordering_is_deterministic() -> None:
    payload = _valid_payload()
    payload["records"][0]["owner"] = ""
    payload["relationships"][0]["predicate"] = "RELATED_TO"
    payload["relationships"][1]["predicate"] = "influences"
    payload["source_mappings"][0]["official_url"] = ""

    first = validate_backbone_contract(payload).to_dict()
    second = validate_backbone_contract(payload).to_dict()

    assert first == second
    assert first["errors"] == sorted(first["errors"])
