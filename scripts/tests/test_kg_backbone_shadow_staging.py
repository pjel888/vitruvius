from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from vitruvius.kg.backbone_shadow_staging import (
    SHADOW_STAGING_ARTIFACT_FILENAME,
    SHADOW_STAGING_REPORT_FILENAME,
    stage_shadow_backbone,
)


def _predicate_payload() -> dict[str, Any]:
    return {
        "predicate_registry": [
            {
                "predicate": "broader_than",
                "direction": "parent_to_child",
                "category": "hierarchy",
                "domain_classes": ["BackboneNode"],
                "range_classes": ["BackboneNode"],
                "allowed_strength_classes": ["steward-curated"],
                "evidence_required_fields": ["owner", "review_status"],
                "owner": "Philip Lewis",
                "examples": ["Architecture is broader than architectural accessibility."],
                "non_examples": ["A source document mentions a concept."],
                "validation_rule": "must not replace provenance",
                "migration_behavior": "legacy links require steward mapping",
            }
        ]
    }


def _source_rights_payload() -> dict[str, Any]:
    return {
        "source_rights_registry": [
            {
                "source_id": "SRC-TEST-001",
                "source_family": "Test Source",
                "publisher_authority": "Test Publisher",
                "edition_version_effective_date": "admission-time verification required",
                "official_url": "https://example.test/source",
                "source_rights_class": "metadata_crosswalk",
                "clearance_state": "metadata_crosswalk_planned",
                "intended_vitruvius_use": "metadata crosswalk only",
                "steward_owner": "Philip Lewis",
                "declared_use_boundary": "no source text, tables, figures, or clauses ingested",
                "currentness_check_date": "2026-04-25",
                "update_cadence": "before source admission",
                "blocking_notes": "content ingest blocked",
            }
        ]
    }


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def test_shadow_staging_writes_file_backed_artifact_without_live_boundaries(tmp_path: Path) -> None:
    predicate_path = tmp_path / "predicate-registry.json"
    source_path = tmp_path / "source-rights-registry.json"
    output_dir = tmp_path / "shadow"
    _write_json(predicate_path, _predicate_payload())
    _write_json(source_path, _source_rights_payload())

    report = stage_shadow_backbone(
        predicate_registry_path=predicate_path,
        source_rights_registry_path=source_path,
        repo_root=tmp_path,
        run_id="TEST_RUN",
        output_dir=output_dir,
    )

    assert report["ok"] is True
    assert report["artifact_written"] is True
    assert report["counts"] == {
        "predicate_registry": 1,
        "source_rights_registry": 1,
    }
    assert report["boundaries"]["shadow_only"] is True
    assert report["boundaries"]["live_neo4j_writes"] is False
    assert report["boundaries"]["protected_content_ingest"] is False

    artifact = json.loads((output_dir / SHADOW_STAGING_ARTIFACT_FILENAME).read_text())
    assert artifact["status"] == "shadow_staged"
    assert artifact["predicate_registry"][0]["predicate"] == "broader_than"
    assert artifact["source_rights_registry"][0]["source_id"] == "SRC-TEST-001"
    assert (output_dir / SHADOW_STAGING_REPORT_FILENAME).is_file()


def test_shadow_staging_blocks_content_ingest_even_when_registry_is_structured(
    tmp_path: Path,
) -> None:
    predicate_path = tmp_path / "predicate-registry.json"
    source_path = tmp_path / "source-rights-registry.json"
    output_dir = tmp_path / "shadow"
    source_payload = _source_rights_payload()
    source_payload["source_rights_registry"][0]["source_rights_class"] = "content_ingest"
    source_payload["source_rights_registry"][0]["clearance_state"] = "cleared_for_declared_use"
    _write_json(predicate_path, _predicate_payload())
    _write_json(source_path, source_payload)

    report = stage_shadow_backbone(
        predicate_registry_path=predicate_path,
        source_rights_registry_path=source_path,
        repo_root=tmp_path,
        run_id="TEST_RUN",
        output_dir=output_dir,
    )

    assert report["ok"] is False
    assert report["artifact_written"] is False
    assert any("content_ingest is blocked for shadow staging" in error for error in report["errors"])
    assert not (output_dir / SHADOW_STAGING_ARTIFACT_FILENAME).exists()
    assert (output_dir / SHADOW_STAGING_REPORT_FILENAME).is_file()


def test_shadow_staging_rejects_unsafe_run_id(tmp_path: Path) -> None:
    predicate_path = tmp_path / "predicate-registry.json"
    source_path = tmp_path / "source-rights-registry.json"
    _write_json(predicate_path, _predicate_payload())
    _write_json(source_path, _source_rights_payload())

    with pytest.raises(ValueError, match="run_id contains unsupported characters"):
        stage_shadow_backbone(
            predicate_registry_path=predicate_path,
            source_rights_registry_path=source_path,
            repo_root=tmp_path,
            run_id="../bad",
        )
