from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from vitruvius.kg.backbone_source_admission import (
    REPORT_FILENAME,
    run_source_admission_preflight,
)


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def _registry_payload() -> dict[str, Any]:
    return {
        "registry_kind": "source_rights_registry_candidate",
        "release_candidate_id": "source-rights.test",
        "status": "candidate_not_steward_admitted",
        "owner": "Philip Lewis",
        "created_at_utc": "2026-04-27T00:00:00Z",
        "runtime_consumer": "none_until_integration_packet",
        "source": "test",
        "source_rights_registry": [
            {
                "source_id": "SRC-TEST-REF",
                "source_family": "Reference Standard",
                "publisher_authority": "Publisher",
                "edition_version_effective_date": "admission-time verification required",
                "official_url": "https://example.com/reference",
                "source_rights_class": "reference_only",
                "clearance_state": "planning_reference_only",
                "intended_vitruvius_use": "source-family citation only",
                "steward_owner": "Philip Lewis",
                "declared_use_boundary": "no standards text, table, figure, or clause ingest",
                "currentness_check_date": "2026-04-27",
                "update_cadence": "before source admission",
                "blocking_notes": "content ingest blocked until explicit license/legal review",
            },
            {
                "source_id": "SRC-TEST-XWALK",
                "source_family": "Crosswalk Standard",
                "publisher_authority": "Publisher",
                "edition_version_effective_date": "dynamic; admission-time verification required",
                "official_url": "https://example.com/crosswalk",
                "source_rights_class": "metadata_crosswalk",
                "clearance_state": "metadata_crosswalk_planned",
                "intended_vitruvius_use": "identifier mapping after steward review",
                "steward_owner": "Philip Lewis",
                "declared_use_boundary": "no local cache or dataset payload ingest until terms are recorded",
                "currentness_check_date": "2026-04-27",
                "update_cadence": "before mapping release",
                "blocking_notes": "license/API terms required before caching",
            },
        ],
    }


def _currentness_payload(source_ids: list[str] | None = None) -> dict[str, Any]:
    ids = source_ids or ["SRC-TEST-REF", "SRC-TEST-XWALK"]
    return {
        "report_kind": "aec_mepfs_source_currentness_evidence",
        "run_id": "TEST_CURRENTNESS",
        "created_at_utc": "2026-04-27T00:00:00Z",
        "scope": "metadata-only currentness fixture",
        "registry_path": "source-rights-registry.json",
        "transport": "fixture",
        "summary": {"total_rows": len(ids)},
        "rows": [
            {
                "source_id": source_id,
                "source_family": source_id,
                "publisher_authority": "Publisher",
                "source_rights_class": "reference_only",
                "clearance_state": "planning_reference_only",
                "declared_use_boundary": "no source text, table, figure, or clause ingest",
                "evidence_status": "fixture_current",
                "legal_decision_status": "pending_human_or_legal_reviewer",
                "steward_admission_status": "pending_named_steward_decision",
                "canonical_admission_status": "not_admitted",
                "blocking_notes": "content ingest blocked",
                "url_checks": [],
            }
            for source_id in ids
        ],
    }


def _manual_payload() -> dict[str, Any]:
    return {
        "report_kind": "aec_mepfs_manual_currentness_resolution",
        "run_id": "TEST_MANUAL_CURRENTNESS",
        "created_at_utc": "2026-04-27T00:00:00Z",
        "scope": "manual/currentness evidence fixture; no content ingest or legal clearance",
        "summary": {
            "cleared_for_content_ingest": 0,
            "resolved_for_declared_reference_or_metadata_use": 1,
        },
        "rows": [
            {
                "source_id": "SRC-TEST-XWALK",
                "source_family": "Crosswalk Standard",
                "review_result": "resolved_for_metadata_crosswalk_with_terms_review",
                "decision_basis": "Fixture evidence only; no content ingest.",
                "review_sources": ["https://example.com/crosswalk"],
                "previous_issue": "fixture",
                "residual_caveat": "terms review required before caching",
            }
        ],
    }


def _write_sources(tmp_path: Path, *, registry: dict[str, Any] | None = None, currentness: dict[str, Any] | None = None, manual: dict[str, Any] | None = None) -> tuple[Path, Path, Path]:
    registry_path = tmp_path / "registry/source-rights-registry.json"
    currentness_path = tmp_path / "currentness/source-currentness-report.json"
    manual_path = tmp_path / "currentness/manual-currentness-resolution-report.json"
    _write_json(registry_path, registry or _registry_payload())
    _write_json(currentness_path, currentness or _currentness_payload())
    _write_json(manual_path, manual or _manual_payload())
    return registry_path, currentness_path, manual_path


def _run(tmp_path: Path, *, registry: dict[str, Any] | None = None, currentness: dict[str, Any] | None = None, manual: dict[str, Any] | None = None) -> dict[str, Any]:
    registry_path, currentness_path, manual_path = _write_sources(
        tmp_path,
        registry=registry,
        currentness=currentness,
        manual=manual,
    )
    return run_source_admission_preflight(
        repo_root=tmp_path,
        run_id="TEST_SOURCE_ADMISSION",
        source_rights_registry_path=registry_path.relative_to(tmp_path),
        currentness_report_path=currentness_path.relative_to(tmp_path),
        manual_currentness_report_path=manual_path.relative_to(tmp_path),
    )


def test_source_admission_preflight_writes_metadata_only_zero_content_report(tmp_path: Path) -> None:
    report = _run(tmp_path)

    saved_path = (
        tmp_path
        / "006_System-Manifests"
        / "aec-mepfs-backbone"
        / "source-admission"
        / "TEST_SOURCE_ADMISSION"
        / REPORT_FILENAME
    )
    assert json.loads(saved_path.read_text(encoding="utf-8")) == report
    assert report["ok"] is True
    assert report["summary"]["source_rights_rows"] == 2
    assert report["summary"]["content_ingest_rows"] == 0
    assert report["summary"]["protected_payload_key_hits"] == 0
    assert report["summary"]["missing_currentness_rows"] == 0
    assert report["status"] == {
        "canonicalContentAdmissionAuthorized": False,
        "contentIngestExternalBlocked": True,
        "metadataReferenceAdmissionPrepared": True,
        "nextRequiredAuthority": "source-specific legal/licensing/steward record for exact protected payload fields",
        "protectedContentIngestAuthorized": False,
        "runtimeSurfaceClaimsMade": False,
        "sourcePayloadExposureAuthorized": False,
    }
    assert report["safety_invariants"]["protectedContentIngestIntent"] is False
    assert report["safety_invariants"]["protectedPayloadStoredInAdmissionArtifacts"] is False
    assert report["runtime_surface_scope"] == {
        "apiExplorerPayloadExposureChecked": False,
        "kgRebuildChecked": False,
        "neo4jMutationChecked": False,
        "reason": "source-admission preflight validates metadata artifacts only; API, Explorer, Neo4j, and KG behavior remain covered by their dedicated lane tests and packets",
    }


def test_source_admission_preflight_fails_on_content_ingest_row(tmp_path: Path) -> None:
    registry = _registry_payload()
    registry["source_rights_registry"][0]["source_rights_class"] = "content_ingest"
    registry["source_rights_registry"][0]["clearance_state"] = "cleared_for_declared_use"
    registry["source_rights_registry"][0]["legal_reviewer"] = "External Counsel"
    registry["source_rights_registry"][0]["reviewer_decision"] = "fixture-cleared"

    report = _run(tmp_path, registry=registry)

    assert report["ok"] is False
    assert report["summary"]["content_ingest_rows"] == 1
    assert report["safety_invariants"]["protectedContentIngestIntent"] is True
    assert any("content_ingest rows remain blocked" in error for error in report["errors"])


def test_source_admission_preflight_fails_on_content_ingest_alias_fields(tmp_path: Path) -> None:
    registry = _registry_payload()
    registry["source_rights_registry"][0]["allowed_use_class"] = "content_ingest"

    report = _run(tmp_path, registry=registry)

    assert report["ok"] is False
    assert report["summary"]["content_ingest_rows"] == 1
    assert report["zero_content_ingest_proof"]["content_ingest_rows"] == ["0:SRC-TEST-REF"]


def test_source_admission_preflight_fails_on_protected_payload_key(tmp_path: Path) -> None:
    registry = _registry_payload()
    registry["source_rights_registry"][0]["clauseText"] = "Do not store me"

    report = _run(tmp_path, registry=registry)

    assert report["ok"] is False
    assert report["summary"]["protected_payload_key_hits"] == 1
    assert report["safety_invariants"]["protectedPayloadStoredInAdmissionArtifacts"] is True
    assert report["zero_content_ingest_proof"]["protected_payload_key_hits"][0]["key"] == "clauseText"


def test_source_admission_preflight_fails_on_protected_payload_alias_key(tmp_path: Path) -> None:
    currentness = _currentness_payload()
    currentness["rows"][0]["source_payload"] = {"text": "Do not store me"}

    report = _run(tmp_path, currentness=currentness)

    assert report["ok"] is False
    keys = {hit["key"] for hit in report["zero_content_ingest_proof"]["protected_payload_key_hits"]}
    assert {"source_payload", "text"} <= keys


def test_source_admission_preflight_fails_on_missing_currentness_coverage(tmp_path: Path) -> None:
    currentness = _currentness_payload(["SRC-TEST-REF"])

    report = _run(tmp_path, currentness=currentness)

    assert report["ok"] is False
    assert report["summary"]["missing_currentness_rows"] == 1
    assert report["coverage"]["missing_currentness_source_ids"] == ["SRC-TEST-XWALK"]


def test_source_admission_preflight_rejects_unsafe_run_id(tmp_path: Path) -> None:
    registry_path, currentness_path, manual_path = _write_sources(tmp_path)

    with pytest.raises(ValueError, match="run_id must contain only"):
        run_source_admission_preflight(
            repo_root=tmp_path,
            run_id="../unsafe",
            source_rights_registry_path=registry_path.relative_to(tmp_path),
            currentness_report_path=currentness_path.relative_to(tmp_path),
            manual_currentness_report_path=manual_path.relative_to(tmp_path),
        )


def test_source_admission_preflight_rejects_output_outside_report_root(tmp_path: Path) -> None:
    registry_path, currentness_path, manual_path = _write_sources(tmp_path)

    with pytest.raises(ValueError, match="source-admission evidence directory"):
        run_source_admission_preflight(
            repo_root=tmp_path,
            run_id="TEST_SOURCE_ADMISSION",
            output_path=Path("outside.json"),
            source_rights_registry_path=registry_path.relative_to(tmp_path),
            currentness_report_path=currentness_path.relative_to(tmp_path),
            manual_currentness_report_path=manual_path.relative_to(tmp_path),
        )


def test_source_admission_preflight_rejects_paths_outside_repo_root(tmp_path: Path) -> None:
    registry_path, currentness_path, manual_path = _write_sources(tmp_path)
    outside = tmp_path.parent / f"outside-source-registry-{tmp_path.name}.json"
    try:
        _write_json(outside, _registry_payload())
        with pytest.raises(ValueError, match="source rights registry path must stay inside repo root"):
            run_source_admission_preflight(
                repo_root=tmp_path,
                run_id="TEST_SOURCE_ADMISSION",
                source_rights_registry_path=outside,
                currentness_report_path=currentness_path.relative_to(tmp_path),
                manual_currentness_report_path=manual_path.relative_to(tmp_path),
            )
    finally:
        outside.unlink(missing_ok=True)
