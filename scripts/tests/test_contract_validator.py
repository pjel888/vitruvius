"""Sprint CLEANUP-1 Stream C1.1 — contract validator for Phase 1B → 1C handoff.

Mirrors the 12-field schema frozen in
.ai/09_archive/plans/ingestion-refinement-contract.md v2.0.0.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from vitruvius.normalization.contract_validator import (
    ContractValidationReport,
    REQUIRED_FIELDS,
    validate_sidecar_json,
)


def _valid_sidecar() -> dict:
    return {
        "source_path": "001_Raw-Source-Layer/001-Laws/PD-1096.pdf",
        "file_type": "pdf",
        "document_class": "text_pdf_complex",
        "parser_id": "rust_pdf",
        "confidence_score": 0.95,
        "pages_total": 100,
        "pages_processed": 100,
        "markdown_path": "002_Raw-Conversion-Layer/001-Laws/raw_markdown/PD-1096.md",
        "assets_extracted": [],
        "structural_context": ["Section 701", "Section 702"],
        "versioning": {
            "parser_version": "0.1.0",
            "pipeline_version": "0.1.0",
            "config_version": "v1",
        },
        "manual_review": {"required": False, "reason": None},
    }


def test_valid_sidecar_passes(tmp_path: Path) -> None:
    sidecar = tmp_path / "valid.json"
    sidecar.write_text(json.dumps(_valid_sidecar()))
    report = validate_sidecar_json(sidecar)
    assert report.ok is True
    assert report.missing_fields == ()
    assert report.nested_errors == ()


def test_missing_required_field_fails(tmp_path: Path) -> None:
    data = _valid_sidecar()
    del data["parser_id"]
    sidecar = tmp_path / "missing_parser_id.json"
    sidecar.write_text(json.dumps(data))
    report = validate_sidecar_json(sidecar)
    assert report.ok is False
    assert "parser_id" in report.missing_fields


def test_invalid_nested_versioning_fails(tmp_path: Path) -> None:
    data = _valid_sidecar()
    data["versioning"] = {"parser_version": "0.1.0"}  # missing pipeline_version + config_version
    sidecar = tmp_path / "bad_versioning.json"
    sidecar.write_text(json.dumps(data))
    report = validate_sidecar_json(sidecar)
    assert report.ok is False
    assert any("versioning.pipeline_version" in err for err in report.nested_errors)


def test_malformed_yaml_fails_cleanly(tmp_path: Path) -> None:
    sidecar = tmp_path / "malformed.json"
    sidecar.write_text("{not valid json")
    report = validate_sidecar_json(sidecar)
    assert report.ok is False
    assert any("parse" in err.lower() for err in report.nested_errors)


def test_required_fields_match_contract_v2_0_0() -> None:
    """Guards against drift — if the contract v2.0.0 adds/removes a field,
    this test fails and forces a plan update."""
    expected = {
        "source_path", "file_type", "document_class", "parser_id",
        "confidence_score", "pages_total", "pages_processed", "markdown_path",
        "assets_extracted", "structural_context", "versioning", "manual_review",
    }
    assert set(REQUIRED_FIELDS) == expected
