from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from vitruvius.kg.backbone_neo4j_rehearsal import (
    REPORT_FILENAME,
    run_neo4j_rehearsal_readiness,
)


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def _isolated_report() -> dict[str, Any]:
    return {
        "report_kind": "aec_mepfs_isolated_neo4j_dump_load_rehearsal",
        "scope": "offline throwaway database only; live Neo4j not stopped or touched",
        "created_at_utc": "2026-04-27T00:00:00Z",
        "steps": [
            {"args": ["neo4j-admin", "database", "import", "full", "aecbbrollback"], "returncode": 0},
            {"args": ["neo4j-admin", "database", "dump", "aecbbrollback"], "returncode": 0},
            {"args": ["neo4j-admin", "database", "load", "aecbbrollback"], "returncode": 0},
        ],
        "summary": {
            "all_steps_zero": True,
            "database": "aecbbrollback",
            "dump_file_exists": True,
            "dump_file_size_bytes": 4186,
            "import_expected_nodes": 2,
            "import_expected_relationships": 1,
            "live_neo4j_stopped": False,
            "live_neo4j_touched": False,
            "neo4j_version": "2026.03.1",
            "restored_database_dir_exists": True,
            "source_database_dir_exists": True,
            "step_returncodes": [0, 0, 0],
        },
    }


def _preflight_report() -> dict[str, Any]:
    return {
        "schema_version": "aec-bb-rollback-preflight/v1",
        "ok": True,
        "proof_status": "blocked_runtime_stopped_or_isolated_database_required",
        "runtime_ready": False,
        "destructive_operations_executed": False,
        "backup_dump_load_executed": False,
        "admin_capabilities": {
            "database_dump_available": True,
            "database_load_available": True,
            "dump_requires_unmounted_database": True,
            "load_requires_unmounted_database": True,
        },
        "live_graph": {
            "connectivity": True,
            "node_count": 10,
            "backbone_shadow_nodes": 0,
        },
    }


def _source_admission_report() -> dict[str, Any]:
    return {
        "schema_version": "aec-mepfs-protected-source-admission/v1",
        "ok": True,
        "status": {
            "canonicalContentAdmissionAuthorized": False,
            "contentIngestExternalBlocked": True,
            "metadataReferenceAdmissionPrepared": True,
            "protectedContentIngestAuthorized": False,
            "runtimeSurfaceClaimsMade": False,
            "sourcePayloadExposureAuthorized": False,
        },
        "safety_invariants": {
            "canonicalContentAdmissionAuthorized": False,
            "globalLiveAuthorization": False,
            "protectedContentIngestIntent": False,
            "protectedPayloadStoredInAdmissionArtifacts": False,
        },
        "summary": {
            "content_ingest_rows": 0,
            "currentness_rows": 2,
            "metadata_only_rows": 2,
            "missing_currentness_rows": 0,
            "protected_payload_key_hits": 0,
            "source_rights_rows": 2,
        },
    }


def _write_reports(tmp_path: Path, *, isolated: dict[str, Any] | None = None, preflight: dict[str, Any] | None = None) -> tuple[Path, Path]:
    isolated_path = tmp_path / "rollback/isolated-dump-load-rehearsal-report.json"
    preflight_path = tmp_path / "rollback/rollback-preflight-report.json"
    _write_json(isolated_path, isolated or _isolated_report())
    _write_json(preflight_path, preflight or _preflight_report())
    return isolated_path, preflight_path


def _write_source_admission_report(tmp_path: Path, payload: dict[str, Any] | None = None) -> Path:
    source_path = tmp_path / "source-admission/SOURCE/source-admission-report.json"
    _write_json(source_path, payload or _source_admission_report())
    return source_path


def _run(
    tmp_path: Path,
    *,
    isolated: dict[str, Any] | None = None,
    preflight: dict[str, Any] | None = None,
    include_source_admission: bool = True,
    source_admission: dict[str, Any] | None = None,
) -> dict[str, Any]:
    isolated_path, preflight_path = _write_reports(tmp_path, isolated=isolated, preflight=preflight)
    kwargs: dict[str, Any] = {}
    if include_source_admission:
        source_path = _write_source_admission_report(tmp_path, source_admission)
        kwargs["source_admission_report_path"] = source_path.relative_to(tmp_path)
    return run_neo4j_rehearsal_readiness(
        repo_root=tmp_path,
        run_id="TEST_NEO4J_REHEARSAL",
        isolated_rehearsal_report_path=isolated_path.relative_to(tmp_path),
        rollback_preflight_report_path=preflight_path.relative_to(tmp_path),
        **kwargs,
    )


def test_neo4j_rehearsal_readiness_writes_blocked_live_promotion_report(tmp_path: Path) -> None:
    report = _run(tmp_path)

    saved_path = (
        tmp_path
        / "006_System-Manifests"
        / "aec-mepfs-backbone"
        / "neo4j-rehearsal"
        / "TEST_NEO4J_REHEARSAL"
        / REPORT_FILENAME
    )
    assert json.loads(saved_path.read_text(encoding="utf-8")) == report
    assert report["ok"] is True
    assert report["status"] == {
        "isolatedRehearsalVerified": True,
        "livePromotionReady": False,
        "nextRequiredPacket": "dedicated_live_promotion_packet_with_fresh_backup_restore_graph_diff_and_rollback_transcript",
        "primaryGraphMutationAuthorized": False,
        "productionLivePromotionAuthorized": False,
        "readOnlyPreflightAvailable": True,
    }
    assert report["isolated_rehearsal_summary"]["live_neo4j_touched"] is False
    assert report["destructive_command_matches"] == []
    assert all(gate["satisfied"] is False for gate in report["live_promotion_prerequisites"] if gate["gate"] != "source_admission_no_protected_ingest_or_valid_authority")
    assert report["inputs"]["source_admission_report"] == "source-admission/SOURCE/source-admission-report.json"
    assert all(report["checks"]["source_admission"].values())
    source_gate = next(gate for gate in report["live_promotion_prerequisites"] if gate["gate"] == "source_admission_no_protected_ingest_or_valid_authority")
    assert source_gate["satisfied"] is True


def test_neo4j_rehearsal_readiness_fails_if_live_neo4j_was_touched(tmp_path: Path) -> None:
    isolated = _isolated_report()
    isolated["summary"]["live_neo4j_touched"] = True

    report = _run(tmp_path, isolated=isolated)

    assert report["ok"] is False
    assert report["checks"]["isolated_rehearsal"]["live_neo4j_not_touched"] is False
    assert "check failed: live_neo4j_not_touched" in report["errors"]
    assert report["safety_invariants"]["liveNeo4jTouched"] is True


def test_neo4j_rehearsal_readiness_fails_on_nonzero_rehearsal_step(tmp_path: Path) -> None:
    isolated = _isolated_report()
    isolated["summary"]["step_returncodes"] = [0, 1, 0]
    isolated["summary"]["all_steps_zero"] = False

    report = _run(tmp_path, isolated=isolated)

    assert report["ok"] is False
    assert report["checks"]["isolated_rehearsal"]["all_steps_zero"] is False
    assert report["checks"]["isolated_rehearsal"]["step_returncodes_all_zero"] is False


def test_neo4j_rehearsal_readiness_requires_blocked_preflight_proof_status(tmp_path: Path) -> None:
    preflight = _preflight_report()
    preflight["proof_status"] = "executed_runtime_ready"

    report = _run(tmp_path, preflight=preflight)

    assert report["ok"] is False
    assert report["checks"]["rollback_preflight"]["preflight_proof_status_blocks_runtime"] is False
    assert "check failed: preflight_proof_status_blocks_runtime" in report["errors"]


def test_neo4j_rehearsal_readiness_fails_on_destructive_command_token(tmp_path: Path) -> None:
    isolated = _isolated_report()
    isolated["steps"].append({"args": ["cypher-shell", "MATCH (n) DETACH DELETE n"], "returncode": 0})

    report = _run(tmp_path, isolated=isolated)

    assert report["ok"] is False
    assert report["destructive_command_matches"][0]["token"] == "DETACH DELETE"
    assert "destructive command tokens found in rehearsal/preflight evidence" in report["errors"]


def test_neo4j_rehearsal_readiness_does_not_satisfy_source_gate_without_evidence(tmp_path: Path) -> None:
    report = _run(tmp_path, include_source_admission=False)

    assert report["ok"] is True
    assert report["inputs"]["source_admission_report"] is None
    assert report["checks"]["source_admission"]["source_admission_report_available"] is False
    source_gate = next(gate for gate in report["live_promotion_prerequisites"] if gate["gate"] == "source_admission_no_protected_ingest_or_valid_authority")
    assert source_gate["satisfied"] is False


def test_neo4j_rehearsal_readiness_fails_on_unsafe_source_admission_evidence(tmp_path: Path) -> None:
    source = _source_admission_report()
    source["status"]["protectedContentIngestAuthorized"] = True
    source["summary"]["content_ingest_rows"] = 1

    report = _run(tmp_path, source_admission=source)

    assert report["ok"] is False
    assert report["checks"]["source_admission"]["protected_content_ingest_not_authorized"] is False
    assert report["checks"]["source_admission"]["no_content_ingest_rows"] is False
    assert report["safety_invariants"]["protectedContentIngestAuthorized"] is True
    source_gate = next(gate for gate in report["live_promotion_prerequisites"] if gate["gate"] == "source_admission_no_protected_ingest_or_valid_authority")
    assert source_gate["satisfied"] is False
    assert "source admission evidence does not prove metadata-only/no-protected-ingest boundary" in report["errors"]


def test_neo4j_rehearsal_readiness_rejects_unsafe_run_id(tmp_path: Path) -> None:
    isolated_path, preflight_path = _write_reports(tmp_path)

    with pytest.raises(ValueError, match="run_id must contain only"):
        run_neo4j_rehearsal_readiness(
            repo_root=tmp_path,
            run_id="../unsafe",
            isolated_rehearsal_report_path=isolated_path.relative_to(tmp_path),
            rollback_preflight_report_path=preflight_path.relative_to(tmp_path),
        )


def test_neo4j_rehearsal_readiness_rejects_output_outside_report_root(tmp_path: Path) -> None:
    isolated_path, preflight_path = _write_reports(tmp_path)

    with pytest.raises(ValueError, match="neo4j-rehearsal evidence directory"):
        run_neo4j_rehearsal_readiness(
            repo_root=tmp_path,
            run_id="TEST_NEO4J_REHEARSAL",
            output_path=Path("outside.json"),
            isolated_rehearsal_report_path=isolated_path.relative_to(tmp_path),
            rollback_preflight_report_path=preflight_path.relative_to(tmp_path),
        )


def test_neo4j_rehearsal_readiness_rejects_input_outside_repo_root(tmp_path: Path) -> None:
    isolated_path, preflight_path = _write_reports(tmp_path)
    outside = tmp_path.parent / f"outside-neo4j-rehearsal-{tmp_path.name}.json"
    try:
        _write_json(outside, _isolated_report())
        with pytest.raises(ValueError, match="isolated rehearsal report path must stay inside repo root"):
            run_neo4j_rehearsal_readiness(
                repo_root=tmp_path,
                run_id="TEST_NEO4J_REHEARSAL",
                isolated_rehearsal_report_path=outside,
                rollback_preflight_report_path=preflight_path.relative_to(tmp_path),
            )
    finally:
        outside.unlink(missing_ok=True)
