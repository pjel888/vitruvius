from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from vitruvius.kg.backbone_shadow_report_reader import (
    CONSUMER_REPORT_FILENAME,
    build_shadow_staging_consumer_report,
)
from vitruvius.kg.backbone_shadow_staging import (
    SHADOW_STAGING_ARTIFACT_FILENAME,
    SHADOW_STAGING_REPORT_FILENAME,
    stage_shadow_backbone,
)


FIXED_NOW = "2026-04-25T16:00:00Z"


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
            },
            {
                "predicate": "evidenced_by",
                "direction": "claim_to_evidence",
                "category": "provenance",
                "domain_classes": ["BackboneNode"],
                "range_classes": ["Source"],
                "allowed_strength_classes": ["metadata-reference"],
                "evidence_required_fields": ["source_id", "review_status"],
                "owner": "Philip Lewis",
                "examples": ["A concept references a source family."],
                "non_examples": ["A concept ingests source text."],
                "validation_rule": "source references must stay metadata-only",
                "migration_behavior": "legacy citations require source-rights review",
            },
        ]
    }


def _source_rights_payload() -> dict[str, Any]:
    return {
        "source_rights_registry": [
            {
                "source_id": "SRC-TEST-001",
                "source_family": "Test Source A",
                "publisher_authority": "Test Publisher",
                "edition_version_effective_date": "admission-time verification required",
                "official_url": "https://example.test/source-a",
                "source_rights_class": "metadata_crosswalk",
                "clearance_state": "metadata_crosswalk_planned",
                "intended_vitruvius_use": "metadata crosswalk only",
                "steward_owner": "Philip Lewis",
                "declared_use_boundary": "no source text, tables, figures, or clauses ingested",
                "currentness_check_date": "2026-04-25",
                "update_cadence": "before source admission",
                "blocking_notes": "content ingest blocked",
            },
            {
                "source_id": "SRC-TEST-002",
                "source_family": "Test Source B",
                "publisher_authority": "Test Publisher",
                "edition_version_effective_date": "admission-time verification required",
                "official_url": "https://example.test/source-b",
                "source_rights_class": "reference_only",
                "clearance_state": "planning_reference_only",
                "intended_vitruvius_use": "source label and URL reference only",
                "steward_owner": "Philip Lewis",
                "declared_use_boundary": "content ingest blocked; metadata reference only",
                "currentness_check_date": "2026-04-25",
                "update_cadence": "before source admission",
                "blocking_notes": "content ingest blocked",
            },
        ]
    }


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _stage_valid_shadow_run(tmp_path: Path, run_id: str = "TEST_RUN") -> Path:
    predicate_path = tmp_path / "predicate-registry.json"
    source_path = tmp_path / "source-rights-registry.json"
    output_dir = (
        tmp_path
        / "006_System-Manifests"
        / "aec-mepfs-backbone"
        / "shadow-staging"
        / run_id
    )
    _write_json(predicate_path, _predicate_payload())
    _write_json(source_path, _source_rights_payload())
    staging_report = stage_shadow_backbone(
        predicate_registry_path=predicate_path,
        source_rights_registry_path=source_path,
        repo_root=tmp_path,
        run_id=run_id,
        output_dir=output_dir,
    )
    assert staging_report["ok"] is True
    return output_dir


def _mutate_json(path: Path, mutation: Any) -> None:
    payload = json.loads(path.read_text(encoding="utf-8"))
    mutation(payload)
    _write_json(path, payload)


def test_shadow_report_reader_writes_deterministic_summary(tmp_path: Path) -> None:
    output_dir = _stage_valid_shadow_run(tmp_path)

    report = build_shadow_staging_consumer_report(
        repo_root=tmp_path,
        run_id="TEST_RUN",
        clock=lambda: FIXED_NOW,
    )

    saved = json.loads((output_dir / CONSUMER_REPORT_FILENAME).read_text(encoding="utf-8"))
    assert saved == report
    assert report["ok"] is True
    assert report["schema_version"] == "aec-bb-shadow-staging-consumer-report/v1"
    assert report["counts"] == {
        "predicate_registry": 2,
        "source_rights_registry": 2,
    }
    assert report["predicate_categories"] == {
        "hierarchy": 1,
        "provenance": 1,
    }
    assert report["source_rights_classes"] == {
        "metadata_crosswalk": 1,
        "reference_only": 1,
    }
    assert report["boundary_coverage"]["safe_for_read_only_consumer"] is True
    assert report["no_ingest_boundary_coverage"]["content_ingest_source_count"] == 0
    assert report["started_at_utc"] == FIXED_NOW
    assert report["finished_at_utc"] == FIXED_NOW


def test_shadow_report_reader_preserves_boundaries_verbatim(tmp_path: Path) -> None:
    output_dir = _stage_valid_shadow_run(tmp_path)
    artifact = json.loads((output_dir / SHADOW_STAGING_ARTIFACT_FILENAME).read_text())

    report = build_shadow_staging_consumer_report(
        repo_root=tmp_path,
        run_id="TEST_RUN",
        clock=lambda: FIXED_NOW,
    )

    assert report["boundaries"] == artifact["boundaries"]


def test_shadow_report_reader_fails_closed_on_runtime_cutover_boundary(
    tmp_path: Path,
) -> None:
    output_dir = _stage_valid_shadow_run(tmp_path)
    _mutate_json(
        output_dir / SHADOW_STAGING_ARTIFACT_FILENAME,
        lambda payload: payload["boundaries"].__setitem__("api_explorer_cutover", True),
    )

    report = build_shadow_staging_consumer_report(
        repo_root=tmp_path,
        run_id="TEST_RUN",
        clock=lambda: FIXED_NOW,
    )

    saved = json.loads((output_dir / CONSUMER_REPORT_FILENAME).read_text(encoding="utf-8"))
    assert saved == report
    assert report["ok"] is False
    assert "artifact.boundaries.api_explorer_cutover: expected false" in report["errors"]


def test_shadow_report_reader_rejects_unexpected_artifact_schema(tmp_path: Path) -> None:
    output_dir = _stage_valid_shadow_run(tmp_path)
    _mutate_json(
        output_dir / SHADOW_STAGING_ARTIFACT_FILENAME,
        lambda payload: payload.__setitem__("schema_version", "future/v2"),
    )

    report = build_shadow_staging_consumer_report(
        repo_root=tmp_path,
        run_id="TEST_RUN",
        clock=lambda: FIXED_NOW,
    )

    assert report["ok"] is False
    assert any("artifact.schema_version" in error for error in report["errors"])


def test_shadow_report_reader_rejects_count_mismatch(tmp_path: Path) -> None:
    output_dir = _stage_valid_shadow_run(tmp_path)
    _mutate_json(
        output_dir / SHADOW_STAGING_ARTIFACT_FILENAME,
        lambda payload: payload["counts"].__setitem__("source_rights_registry", 99),
    )

    report = build_shadow_staging_consumer_report(
        repo_root=tmp_path,
        run_id="TEST_RUN",
        clock=lambda: FIXED_NOW,
    )

    assert report["ok"] is False
    assert "artifact.counts.source_rights_registry: expected 2, found 99" in report["errors"]


def test_shadow_report_reader_requires_producer_report_counts(tmp_path: Path) -> None:
    output_dir = _stage_valid_shadow_run(tmp_path)
    _mutate_json(
        output_dir / SHADOW_STAGING_REPORT_FILENAME,
        lambda payload: payload.pop("counts"),
    )

    report = build_shadow_staging_consumer_report(
        repo_root=tmp_path,
        run_id="TEST_RUN",
        clock=lambda: FIXED_NOW,
    )

    assert report["ok"] is False
    assert "producer_report.counts: expected object" in report["errors"]


def test_shadow_report_reader_blocks_content_ingest_class(tmp_path: Path) -> None:
    output_dir = _stage_valid_shadow_run(tmp_path)
    _mutate_json(
        output_dir / SHADOW_STAGING_ARTIFACT_FILENAME,
        lambda payload: payload["source_rights_registry"][0].__setitem__(
            "source_rights_class",
            "content_ingest",
        ),
    )

    report = build_shadow_staging_consumer_report(
        repo_root=tmp_path,
        run_id="TEST_RUN",
        clock=lambda: FIXED_NOW,
    )

    assert report["ok"] is False
    assert report["no_ingest_boundary_coverage"]["content_ingest_source_ids"] == [
        "SRC-TEST-001"
    ]
    assert any("content_ingest blocked" in error for error in report["errors"])


def test_shadow_report_reader_blocks_missing_no_ingest_boundary(tmp_path: Path) -> None:
    output_dir = _stage_valid_shadow_run(tmp_path)
    _mutate_json(
        output_dir / SHADOW_STAGING_ARTIFACT_FILENAME,
        lambda payload: payload["source_rights_registry"][1].__setitem__(
            "declared_use_boundary",
            "metadata only",
        ),
    )

    report = build_shadow_staging_consumer_report(
        repo_root=tmp_path,
        run_id="TEST_RUN",
        clock=lambda: FIXED_NOW,
    )

    assert report["ok"] is False
    assert report["no_ingest_boundary_coverage"]["missing_explicit_block_source_ids"] == [
        "SRC-TEST-002"
    ]


def test_shadow_report_reader_rejects_missing_artifact(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="file does not exist"):
        build_shadow_staging_consumer_report(
            repo_root=tmp_path,
            run_id="MISSING_RUN",
            clock=lambda: FIXED_NOW,
        )


def test_shadow_report_reader_rejects_non_object_json(tmp_path: Path) -> None:
    output_dir = _stage_valid_shadow_run(tmp_path)
    (output_dir / SHADOW_STAGING_ARTIFACT_FILENAME).write_text("[]\n", encoding="utf-8")

    with pytest.raises(ValueError, match="expected a JSON object"):
        build_shadow_staging_consumer_report(
            repo_root=tmp_path,
            run_id="TEST_RUN",
            clock=lambda: FIXED_NOW,
        )


def test_shadow_report_reader_rejects_missing_required_sections(tmp_path: Path) -> None:
    output_dir = _stage_valid_shadow_run(tmp_path)
    _mutate_json(
        output_dir / SHADOW_STAGING_ARTIFACT_FILENAME,
        lambda payload: payload.pop("source_paths"),
    )

    report = build_shadow_staging_consumer_report(
        repo_root=tmp_path,
        run_id="TEST_RUN",
        clock=lambda: FIXED_NOW,
    )

    assert report["ok"] is False
    assert "artifact.source_paths: missing required field" in report["errors"]
    assert "artifact.source_paths: expected object" in report["errors"]


def test_shadow_report_reader_handles_empty_registries(tmp_path: Path) -> None:
    run_dir = (
        tmp_path
        / "006_System-Manifests"
        / "aec-mepfs-backbone"
        / "shadow-staging"
        / "EMPTY_RUN"
    )
    artifact = {
        "schema_version": "aec-bb-shadow-staging/v1",
        "run_id": "EMPTY_RUN",
        "created_at_utc": FIXED_NOW,
        "status": "shadow_staged",
        "source_paths": {
            "predicate_registry": "predicate-registry.json",
            "source_rights_registry": "source-rights-registry.json",
        },
        "counts": {
            "predicate_registry": 0,
            "source_rights_registry": 0,
        },
        "boundaries": {
            "shadow_only": True,
            "file_backed_only": True,
            "live_neo4j_writes": False,
            "graph_rebuild": False,
            "feature_flag_cutover": False,
            "api_explorer_cutover": False,
            "canonical_content_admission": False,
            "protected_content_ingest": False,
        },
        "predicate_registry": [],
        "source_rights_registry": [],
    }
    producer_report = {
        "schema_version": "aec-bb-shadow-staging-report/v1",
        "ok": True,
        "run_id": "EMPTY_RUN",
        "artifact_written": True,
        "counts": artifact["counts"],
        "errors": [],
        "warnings": [],
    }
    _write_json(run_dir / SHADOW_STAGING_ARTIFACT_FILENAME, artifact)
    _write_json(run_dir / SHADOW_STAGING_REPORT_FILENAME, producer_report)

    report = build_shadow_staging_consumer_report(
        repo_root=tmp_path,
        run_id="EMPTY_RUN",
        clock=lambda: FIXED_NOW,
    )

    assert report["ok"] is True
    assert report["counts"] == {
        "predicate_registry": 0,
        "source_rights_registry": 0,
    }
    assert report["no_ingest_boundary_coverage"]["sources_total"] == 0


def test_shadow_report_reader_requires_safe_run_id(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="run_id must contain only"):
        build_shadow_staging_consumer_report(
            repo_root=tmp_path,
            run_id="../unsafe",
            clock=lambda: FIXED_NOW,
        )


def test_shadow_report_reader_rejects_output_outside_shadow_root(tmp_path: Path) -> None:
    _stage_valid_shadow_run(tmp_path)

    with pytest.raises(ValueError, match="shadow staging report directory"):
        build_shadow_staging_consumer_report(
            repo_root=tmp_path,
            run_id="TEST_RUN",
            output_path=Path(".ai/ACTIVE_WORK.md"),
            clock=lambda: FIXED_NOW,
        )


def test_shadow_report_reader_requires_run_scoped_output(tmp_path: Path) -> None:
    _stage_valid_shadow_run(tmp_path)

    with pytest.raises(ValueError, match="current shadow staging run id"):
        build_shadow_staging_consumer_report(
            repo_root=tmp_path,
            run_id="TEST_RUN",
            output_path=Path(
                "006_System-Manifests/aec-mepfs-backbone/shadow-staging/OTHER_RUN"
            )
            / CONSUMER_REPORT_FILENAME,
            clock=lambda: FIXED_NOW,
        )


def test_shadow_report_reader_rejects_output_filename_mismatch(tmp_path: Path) -> None:
    _stage_valid_shadow_run(tmp_path)

    with pytest.raises(ValueError, match=CONSUMER_REPORT_FILENAME):
        build_shadow_staging_consumer_report(
            repo_root=tmp_path,
            run_id="TEST_RUN",
            output_path=Path(
                "006_System-Manifests/aec-mepfs-backbone/shadow-staging/TEST_RUN"
            )
            / "other-report.json",
            clock=lambda: FIXED_NOW,
        )
