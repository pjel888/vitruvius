from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

import pytest

from vitruvius.kg.architecture_civil_structural_gate_review import main, run_gated_review


FIXTURE = Path("scripts/tests/fixtures/aec_mepfs_backbone/admitted_backbone_nodes_l1_l2.json")


def _load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _temp_repo_with_backbone(tmp_path: Path) -> Path:
    fixture_copy = tmp_path / FIXTURE
    fixture_copy.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(FIXTURE, fixture_copy)
    return tmp_path


def _write_evidence(repo_root: Path, rel_path: str) -> Path:
    evidence_path = repo_root / rel_path
    evidence_path.parent.mkdir(parents=True, exist_ok=True)
    evidence_path.write_text(json.dumps({"evidence": "synthetic test fixture"}), encoding="utf-8")
    return evidence_path


def test_gated_review_exports_duplicates_without_mutating_backbone(tmp_path: Path) -> None:
    repo_root = _temp_repo_with_backbone(tmp_path)
    fixture_copy = repo_root / FIXTURE
    before = fixture_copy.read_text(encoding="utf-8")

    report = run_gated_review(repo_root=repo_root, run_id="TEST_GATED_REVIEW")

    duplicate_path = repo_root / report["duplicate_merge_review_path"]
    duplicate_payload = _load(duplicate_path)

    assert report["ok"] is True
    assert report["boundaries"]["canonical_label_mutation"] is False
    assert report["boundaries"]["batch_merge_blocked"] is True
    assert report["boundaries"]["non_destructive_batch_only"] is True
    assert report["duplicate_merge_review"]["candidate_group_count"] == 514
    assert report["duplicate_merge_review"]["same_parent_blocker_group_count"] == 0
    assert report["duplicate_merge_review"]["auto_merge_allowed"] is False
    assert duplicate_payload["summary"]["canonical_label_mutation_performed"] is False
    assert duplicate_payload["candidates"][0]["auto_merge_allowed"] is False
    assert duplicate_payload["candidates"][0]["batch_merge_blocked"] is True
    assert duplicate_payload["candidates"][0]["requires_steward_decision"] is True
    assert duplicate_payload["candidates"][0]["allowed_steward_actions"]
    assert fixture_copy.read_text(encoding="utf-8") == before


def test_gated_review_flags_concrete_and_reinforced_concrete_as_p0_safety_critical(tmp_path: Path) -> None:
    repo_root = _temp_repo_with_backbone(tmp_path)

    report = run_gated_review(repo_root=repo_root, run_id="TEST_P0_CONCRETE")
    duplicate_path = repo_root / report["duplicate_merge_review_path"]
    duplicate_payload = _load(duplicate_path)

    p0_candidates = [c for c in duplicate_payload["candidates"] if c.get("priority") == "P0"]
    assert len(p0_candidates) == 2
    labels = {c["normalized_label"] for c in p0_candidates}
    assert labels == {"concrete", "reinforced concrete"}
    for c in p0_candidates:
        assert c["safety_critical"] is True
        assert c["requires_explicit_steward_decision"] is True
        assert c["batch_merge_blocked"] is True


def test_gated_review_persists_report_with_all_gate_sections(tmp_path: Path) -> None:
    repo_root = _temp_repo_with_backbone(tmp_path)

    report = run_gated_review(repo_root=repo_root, run_id="TEST_REPORT_SCHEMA")
    persisted_report = _load(repo_root / report["report_path"])

    assert persisted_report == report
    for key in (
        "schema_version",
        "run_id",
        "generated_at_utc",
        "ok",
        "status",
        "errors",
        "warnings",
        "boundaries",
        "backbone_path",
        "report_path",
        "duplicate_merge_review_path",
        "steward_duplicate_apply_plan_path",
        "readiness_artifact_paths",
        "duplicate_merge_review",
        "steward_duplicate_decision_gate",
        "criteria_admission_gate",
        "external_authority_ledger_gate",
        "protected_payload_manifest_gate",
        "payload_leak_audit",
        "live_promotion_gate",
    ):
        assert key in report
    assert report["boundaries"] == {
        "file_backed_only": True,
        "shadow_only": True,
        "canonical_label_mutation": False,
        "numeric_criteria_admission": False,
        "protected_payload_ingest": False,
        "live_neo4j_writes": False,
        "production_promotion": False,
        "batch_merge_blocked": True,
        "non_destructive_batch_only": True,
    }
    apply_plan = _load(repo_root / report["steward_duplicate_apply_plan_path"])
    assert apply_plan["status"] == "blocked_missing_steward_decision_packet"
    assert apply_plan["boundaries"]["dry_run_only"] is True
    assert apply_plan["boundaries"]["canonical_label_mutation_performed"] is False
    readiness_bundle = _load(repo_root / report["readiness_artifact_paths"]["external_gate_readiness_bundle"])
    assert readiness_bundle["status"] == "external_inputs_required"
    assert readiness_bundle["boundaries"]["production_promotion"] is False


def test_gated_review_generates_external_gate_skeletons_without_fabricating_authority(tmp_path: Path) -> None:
    repo_root = _temp_repo_with_backbone(tmp_path)

    report = run_gated_review(repo_root=repo_root, run_id="TEST_READINESS_SKELETONS")

    paths = report["readiness_artifact_paths"]
    assert set(paths) == {
        "steward_preserve_packet_skeleton",
        "criteria_packet_skeleton",
        "authority_ledger_skeleton",
        "protected_payload_manifest_skeleton",
        "live_promotion_plan_skeleton",
        "rollback_hash_chain_manifest_skeleton",
        "external_gate_readiness_bundle",
    }
    for rel_path in paths.values():
        assert rel_path.startswith(
            "006_System-Manifests/aec-mepfs-backbone/architecture-civil-structural-gated-review/"
        )

    steward_skeleton = _load(repo_root / paths["steward_preserve_packet_skeleton"])
    assert steward_skeleton["draft_only"] is True
    assert steward_skeleton["status"] == "draft_requires_steward_authority"
    assert steward_skeleton["steward"] is None
    assert steward_skeleton["authority_record_id"] is None
    assert steward_skeleton["decision_scope"] == "all_current_duplicate_candidates"
    assert steward_skeleton["default_action"] == "preserve_contextual_duplicate"
    assert len(steward_skeleton["repo_derived_context"]["candidate_set_sha256"]) == 64
    assert steward_skeleton["boundaries"]["canonical_label_mutation_performed"] is False

    criteria_skeleton = _load(repo_root / paths["criteria_packet_skeleton"])
    assert criteria_skeleton["project_id"] is None
    assert criteria_skeleton["criteria"] == []
    assert "value" in criteria_skeleton["required_criterion_fields"]
    assert criteria_skeleton["boundaries"]["numeric_criteria_admission_performed"] is False

    protected_skeleton = _load(repo_root / paths["protected_payload_manifest_skeleton"])
    assert protected_skeleton["payloads"] == []
    assert "hash_only" in protected_skeleton["allowed_exposure_policies"]
    assert protected_skeleton["boundaries"]["protected_payload_ingest_performed"] is False

    live_skeleton = _load(repo_root / paths["live_promotion_plan_skeleton"])
    assert live_skeleton["required_environment_variable_names"] == [
        "VITRUVIUS_PRODUCTION_NEO4J_URI",
        "VITRUVIUS_PRODUCTION_NEO4J_USER",
        "VITRUVIUS_PRODUCTION_NEO4J_PASSWORD",
    ]
    assert live_skeleton["credential_values_stored"] is False
    assert live_skeleton["backup_artifact_path"] is None
    assert live_skeleton["boundaries"]["production_promotion_performed"] is False


def test_gated_review_readiness_bundle_keeps_blocked_gates_blocked(tmp_path: Path) -> None:
    repo_root = _temp_repo_with_backbone(tmp_path)

    report = run_gated_review(repo_root=repo_root, run_id="TEST_READINESS_BUNDLE")
    bundle = _load(repo_root / report["readiness_artifact_paths"]["external_gate_readiness_bundle"])

    assert bundle["status"] == "external_inputs_required"
    assert bundle["draft_only"] is True
    assert bundle["gate_statuses"] == {
        "steward_duplicate_decision": "blocked_missing_steward_decision_packet",
        "project_ahj_criteria": "blocked_missing_project_ahj_packet",
        "external_authority_ledger": "blocked_missing_external_authority_ledger",
        "protected_payload_manifest": "blocked_missing_protected_payload_manifest",
        "live_promotion_credentials_and_rollback": "blocked_missing_credentials_rollback_or_plan",
    }
    assert len(bundle["blocked_categories"]) == 5
    assert bundle["operations_not_performed"]["live_neo4j_write"] is True
    assert bundle["operations_not_performed"]["production_promotion"] is True
    assert bundle["boundaries"] == report["boundaries"]


def test_gated_review_steward_skeleton_requires_per_group_decisions_for_same_parent_blockers(tmp_path: Path) -> None:
    repo_root = _temp_repo_with_backbone(tmp_path)
    fixture_copy = repo_root / FIXTURE
    payload = _load(fixture_copy)
    payload["records"].extend(
        [
            {
                "id": "TEST-SAME-PARENT-1",
                "record_type": "BackboneNode",
                "label": "Same Parent Duplicate Test Node",
                "path_code": "TEST.DUP.001",
                "parent_path_code": "TEST.DUP",
            },
            {
                "id": "TEST-SAME-PARENT-2",
                "record_type": "BackboneNode",
                "label": "Same Parent Duplicate Test Node",
                "path_code": "TEST.DUP.002",
                "parent_path_code": "TEST.DUP",
            },
        ]
    )
    fixture_copy.write_text(json.dumps(payload), encoding="utf-8")

    report = run_gated_review(repo_root=repo_root, run_id="TEST_SAME_PARENT_SKELETON")
    steward_skeleton = _load(repo_root / report["readiness_artifact_paths"]["steward_preserve_packet_skeleton"])

    assert report["duplicate_merge_review"]["same_parent_blocker_group_count"] == 1
    assert steward_skeleton["decision_scope"] is None
    assert steward_skeleton["default_action"] is None
    assert steward_skeleton["requires_explicit_per_group_decisions"] is True


def test_gated_review_validates_global_steward_duplicate_decision_without_mutation(tmp_path: Path) -> None:
    repo_root = _temp_repo_with_backbone(tmp_path)
    _write_evidence(repo_root, "006_System-Manifests/test-evidence/steward-duplicate-decision.json")
    packet = {
        "packet_id": "steward-global-preserve",
        "steward": "Philip Lewis",
        "decision_date": "2026-05-01",
        "authority_record_id": "AUTH-STEW-ACS-DUP-TEST",
        "rationale": "Current duplicate labels are contextual cross-parent or cross-root labels, not same-parent blockers.",
        "evidence_paths": ["006_System-Manifests/test-evidence/steward-duplicate-decision.json"],
        "decision_scope": "all_current_duplicate_candidates",
        "default_action": "preserve_contextual_duplicate",
    }
    packet_path = repo_root / "006_System-Manifests/test-packets/steward-duplicate-decision.json"
    packet_path.parent.mkdir(parents=True, exist_ok=True)
    packet_path.write_text(json.dumps(packet), encoding="utf-8")

    report = run_gated_review(
        repo_root=repo_root,
        steward_decision_packet_path=packet_path,
        run_id="TEST_STEWARD_DUPLICATE_DECISION",
    )

    assert report["ok"] is True
    assert report["steward_duplicate_decision_gate"]["status"] == "validated_not_applied"
    assert report["steward_duplicate_decision_gate"]["validated_decision_count"] == 514
    assert report["steward_duplicate_decision_gate"]["canonical_label_mutation_performed"] is False
    assert report["steward_duplicate_decision_gate"]["alias_application_performed"] is False
    assert report["steward_duplicate_decision_gate"]["auto_merge_allowed"] is False
    apply_plan = _load(repo_root / report["steward_duplicate_apply_plan_path"])
    assert apply_plan["status"] == "validated_not_applied"
    assert apply_plan["operation_count"] == 514
    assert apply_plan["packet_sha256"] is not None
    assert len(apply_plan["packet_sha256"]) == 64
    assert apply_plan["hash_chain_final_hash"] is not None
    assert len(apply_plan["hash_chain_final_hash"]) == 64
    assert apply_plan["operations"][0]["dry_run_only"] is True
    assert apply_plan["operations"][0]["canonical_label_mutation_performed"] is False
    assert apply_plan["operations"][0]["previous_hash"] == "0" * 64
    assert len(apply_plan["operations"][0]["operation_hash"]) == 64
    assert apply_plan["boundaries"]["batch_merge_blocked"] is True
    assert apply_plan["boundaries"]["non_destructive_batch_only"] is True


def test_gated_review_rejects_unsafe_global_steward_duplicate_action(tmp_path: Path) -> None:
    repo_root = _temp_repo_with_backbone(tmp_path)
    _write_evidence(repo_root, "006_System-Manifests/test-evidence/steward-duplicate-decision.json")
    packet = {
        "packet_id": "steward-global-unsafe",
        "steward": "Philip Lewis",
        "decision_date": "2026-05-01",
        "authority_record_id": "AUTH-STEW-ACS-DUP-TEST",
        "rationale": "Unsafe global merge should be blocked.",
        "evidence_paths": ["006_System-Manifests/test-evidence/steward-duplicate-decision.json"],
        "decision_scope": "all_current_duplicate_candidates",
        "default_action": "select_survivor_node",
    }
    packet_path = repo_root / "006_System-Manifests/test-packets/steward-duplicate-decision.json"
    packet_path.parent.mkdir(parents=True, exist_ok=True)
    packet_path.write_text(json.dumps(packet), encoding="utf-8")

    report = run_gated_review(
        repo_root=repo_root,
        steward_decision_packet_path=packet_path,
        run_id="TEST_STEWARD_DUPLICATE_UNSAFE_ACTION",
    )

    assert report["ok"] is False
    assert report["steward_duplicate_decision_gate"]["status"] == "rejected"
    assert any("global duplicate decisions" in error for error in report["errors"])


def test_gated_review_rejects_unsafe_numeric_criteria_packet(tmp_path: Path) -> None:
    packet = {
        "packet_id": "unsafe-test",
        "project_id": "project-test",
        "jurisdiction_id": "test-jurisdiction",
        "ahj_authority": "test AHJ",
        "steward_approval_id": "approval-test",
        "adopted_sources": [{"source_id": "SRC-ASCE-SEI-7"}],
        "criteria": [
            {
                "criterion_name": "Unsafe wind criterion",
                "concept_path_code": "STR.LOA.LAT.WND",
                "value": "synthetic-test-value",
                "units": "synthetic-test-units",
                "source_id": "SRC-ASCE-SEI-7",
                "adopted_edition": "test-edition",
                "ahj_basis": "test-basis",
                "effective_date": "2026-05-01",
                "source_rights_clearance_state": "not_cleared",
                "protected_payload_included": True,
            }
        ],
    }
    packet_path = tmp_path / "criteria-packet.json"
    packet_path.write_text(json.dumps(packet), encoding="utf-8")

    repo_root = _temp_repo_with_backbone(tmp_path)
    report = run_gated_review(
        repo_root=repo_root,
        criteria_packet_path=packet_path,
        run_id="TEST_REJECT_UNSAFE_CRITERIA",
    )

    assert report["ok"] is False
    assert report["criteria_admission_gate"]["status"] == "rejected"
    assert report["criteria_admission_gate"]["admitted_numeric_criteria_count"] == 0
    assert any("source_rights_clearance_state" in error for error in report["errors"])
    assert any("protected_payload_included" in error for error in report["errors"])


def test_gated_review_validates_complete_packet_without_admitting_numbers(tmp_path: Path) -> None:
    packet = {
        "packet_id": "valid-test",
        "project_id": "project-test",
        "jurisdiction_id": "test-jurisdiction",
        "ahj_authority": "test AHJ",
        "steward_approval_id": "approval-test",
        "adopted_sources": [{"source_id": "SRC-ASCE-SEI-7"}],
        "criteria": [
            {
                "criterion_name": "Synthetic wind criterion",
                "concept_path_code": "STR.LOA.LAT.WND",
                "value": "synthetic-test-value",
                "units": "synthetic-test-units",
                "source_id": "SRC-ASCE-SEI-7",
                "adopted_edition": "test-edition",
                "ahj_basis": "test-basis",
                "effective_date": "2026-05-01",
                "source_rights_clearance_state": "cleared_for_declared_use",
                "protected_payload_included": False,
            }
        ],
    }
    packet_path = tmp_path / "criteria-packet.json"
    packet_path.write_text(json.dumps(packet), encoding="utf-8")

    repo_root = _temp_repo_with_backbone(tmp_path)
    report = run_gated_review(
        repo_root=repo_root,
        criteria_packet_path=packet_path,
        run_id="TEST_VALIDATE_CRITERIA",
    )

    assert report["ok"] is True
    assert report["criteria_admission_gate"]["status"] == "validated_not_admitted"
    assert report["criteria_admission_gate"]["validated_criteria_count"] == 1
    assert report["criteria_admission_gate"]["admitted_numeric_criteria_count"] == 0
    assert report["criteria_admission_gate"]["graph_write_performed"] is False
    assert report["boundaries"]["numeric_criteria_admission"] is False


def test_gated_review_rejects_authority_ledger_with_missing_evidence(tmp_path: Path) -> None:
    ledger = {
        "authority_records": [
            {
                "authority_id": "AHJ-TEST",
                "authority_type": "ahj",
                "scope": "test",
                "decision_status": "approved",
                "steward": "Philip Lewis",
                "decision_date": "2026-05-01",
                "evidence_paths": ["does-not-exist.json"],
                "source_rights_ids": [],
            }
        ]
    }
    ledger_path = tmp_path / "authority-ledger.json"
    ledger_path.write_text(json.dumps(ledger), encoding="utf-8")

    repo_root = _temp_repo_with_backbone(tmp_path)
    report = run_gated_review(
        repo_root=repo_root,
        authority_ledger_path=ledger_path,
        run_id="TEST_REJECT_LEDGER",
    )

    assert report["ok"] is False
    assert report["external_authority_ledger_gate"]["status"] == "rejected"
    assert any("evidence path not found" in error for error in report["errors"])
    assert any("source_rights_ids" in error for error in report["errors"])


def test_gated_review_validates_authority_ledger_without_admission(tmp_path: Path) -> None:
    repo_root = _temp_repo_with_backbone(tmp_path)
    evidence_path = repo_root / "006_System-Manifests/test-authority-evidence/authority-evidence.json"
    evidence_path.parent.mkdir(parents=True, exist_ok=True)
    evidence_path.write_text(json.dumps({"evidence": "synthetic structural validation fixture"}), encoding="utf-8")
    ledger = {
        "authority_records": [
            {
                "authority_id": "AHJ-TEST",
                "authority_type": "ahj",
                "scope": "synthetic test authority decision",
                "decision_status": "approved",
                "steward": "Philip Lewis",
                "decision_date": "2026-05-01",
                "evidence_paths": ["006_System-Manifests/test-authority-evidence/authority-evidence.json"],
                "source_rights_ids": ["SRC-ASCE-SEI-7"],
            }
        ]
    }
    ledger_path = tmp_path / "authority-ledger.json"
    ledger_path.write_text(json.dumps(ledger), encoding="utf-8")

    report = run_gated_review(
        repo_root=repo_root,
        authority_ledger_path=ledger_path,
        run_id="TEST_VALIDATE_LEDGER",
    )

    assert report["ok"] is True
    assert report["external_authority_ledger_gate"]["status"] == "validated_not_admitted"
    assert report["external_authority_ledger_gate"]["validated_authority_record_count"] == 1
    assert report["external_authority_ledger_gate"]["admission_authorized"] is False
    assert report["external_authority_ledger_gate"]["graph_write_performed"] is False


def test_gated_review_rejects_forbidden_payload_keys(tmp_path: Path) -> None:
    packet = {
        "packet_id": "unsafe-payload-key",
        "project_id": "project-test",
        "jurisdiction_id": "test-jurisdiction",
        "ahj_authority": "test AHJ",
        "steward_approval_id": "approval-test",
        "adopted_sources": [{"source_id": "SRC-ASCE-SEI-7"}],
        "criteria": [
            {
                "criterion_name": "Synthetic criterion",
                "concept_path_code": "STR.LOA.LAT.WND",
                "value": "synthetic-test-value",
                "units": "synthetic-test-units",
                "source_id": "SRC-ASCE-SEI-7",
                "adopted_edition": "test-edition",
                "ahj_basis": "test-basis",
                "effective_date": "2026-05-01",
                "source_rights_clearance_state": "cleared_for_declared_use",
                "protected_payload_included": False,
                "source_text": "blocked test payload",
            }
        ],
    }
    packet_path = tmp_path / "criteria-packet.json"
    packet_path.write_text(json.dumps(packet), encoding="utf-8")

    repo_root = _temp_repo_with_backbone(tmp_path)
    report = run_gated_review(
        repo_root=repo_root,
        criteria_packet_path=packet_path,
        run_id="TEST_REJECT_PAYLOAD_KEY",
    )

    assert report["ok"] is False
    assert report["payload_leak_audit"]["status"] == "rejected_for_forbidden_payload_keys"
    assert any("source_text" in error for error in report["errors"])


def test_gated_review_rejects_unsupported_authority_type(tmp_path: Path) -> None:
    repo_root = _temp_repo_with_backbone(tmp_path)
    _write_evidence(repo_root, "006_System-Manifests/test-authority-evidence/authority-evidence.json")
    ledger = {
        "authority_records": [
            {
                "authority_id": "AUTH-UNSUPPORTED",
                "authority_type": "unsupported_authority",
                "scope": "test",
                "decision_status": "pending",
                "steward": "Philip Lewis",
                "decision_date": "2026-05-01",
                "evidence_paths": ["006_System-Manifests/test-authority-evidence/authority-evidence.json"],
            }
        ]
    }
    ledger_path = repo_root / "006_System-Manifests/test-packets/authority-ledger.json"
    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    ledger_path.write_text(json.dumps(ledger), encoding="utf-8")

    report = run_gated_review(
        repo_root=repo_root,
        authority_ledger_path=ledger_path,
        run_id="TEST_REJECT_UNSUPPORTED_AUTHORITY",
    )

    assert report["ok"] is False
    assert report["external_authority_ledger_gate"]["status"] == "rejected"
    assert report["external_authority_ledger_gate"]["validated_authority_record_count"] == 0
    assert any("unsupported authority type" in error for error in report["errors"])


def test_gated_review_scans_json_payload_even_with_non_json_suffix(tmp_path: Path) -> None:
    packet = {
        "packet_id": "unsafe-payload-key-non-json-suffix",
        "project_id": "project-test",
        "jurisdiction_id": "test-jurisdiction",
        "ahj_authority": "test AHJ",
        "steward_approval_id": "approval-test",
        "adopted_sources": [{"source_id": "SRC-ASCE-SEI-7"}],
        "criteria": [
            {
                "criterion_name": "Synthetic criterion",
                "concept_path_code": "STR.LOA.LAT.WND",
                "value": "synthetic-test-value",
                "units": "synthetic-test-units",
                "source_id": "SRC-ASCE-SEI-7",
                "adopted_edition": "test-edition",
                "ahj_basis": "test-basis",
                "effective_date": "2026-05-01",
                "source_rights_clearance_state": "cleared_for_declared_use",
                "protected_payload_included": False,
                "source_text": "blocked despite non-json suffix",
            }
        ],
    }
    packet_path = tmp_path / "criteria-packet.txt"
    packet_path.write_text(json.dumps(packet), encoding="utf-8")

    repo_root = _temp_repo_with_backbone(tmp_path)
    report = run_gated_review(
        repo_root=repo_root,
        criteria_packet_path=packet_path,
        run_id="TEST_REJECT_PAYLOAD_KEY_NON_JSON_SUFFIX",
    )

    assert report["ok"] is False
    assert report["payload_leak_audit"]["status"] == "rejected_for_forbidden_payload_keys"
    assert any("criteria_packet.criteria[0].source_text" in error for error in report["errors"])


def test_gated_review_validates_hash_only_protected_payload_manifest_without_ingest(tmp_path: Path) -> None:
    repo_root = _temp_repo_with_backbone(tmp_path)
    _write_evidence(repo_root, "006_System-Manifests/test-evidence/protected-payload-rights.json")
    manifest = {
        "manifest_id": "protected-payload-hash-only-test",
        "steward": "Philip Lewis",
        "decision_date": "2026-05-01",
        "authority_record_ids": ["AUTH-SOURCE-RIGHTS-TEST"],
        "evidence_paths": ["006_System-Manifests/test-evidence/protected-payload-rights.json"],
        "payloads": [
            {
                "payload_id": "payload-test-1",
                "source_id": "SRC-ASCE-SEI-7",
                "source_rights_id": "RIGHTS-TEST",
                "content_sha256": "a" * 64,
                "admitted_use": "hash-only custody verification",
                "exposure_policy": "hash_only",
                "payload_text_included": False,
            }
        ],
    }
    manifest_path = repo_root / "006_System-Manifests/test-packets/protected-payload-manifest.json"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

    report = run_gated_review(
        repo_root=repo_root,
        protected_payload_manifest_path=manifest_path,
        run_id="TEST_PROTECTED_PAYLOAD_HASH_ONLY",
    )

    assert report["ok"] is True
    assert report["protected_payload_manifest_gate"]["status"] == "validated_not_ingested"
    assert report["protected_payload_manifest_gate"]["validated_payload_reference_count"] == 1
    assert report["protected_payload_manifest_gate"]["protected_payload_ingest_performed"] is False
    assert report["protected_payload_manifest_gate"]["public_payload_exposure_performed"] is False


def test_gated_review_rejects_protected_payload_manifest_with_payload_text_key(tmp_path: Path) -> None:
    repo_root = _temp_repo_with_backbone(tmp_path)
    _write_evidence(repo_root, "006_System-Manifests/test-evidence/protected-payload-rights.json")
    manifest = {
        "manifest_id": "protected-payload-text-test",
        "steward": "Philip Lewis",
        "decision_date": "2026-05-01",
        "authority_record_ids": ["AUTH-SOURCE-RIGHTS-TEST"],
        "evidence_paths": ["006_System-Manifests/test-evidence/protected-payload-rights.json"],
        "payloads": [
            {
                "payload_id": "payload-test-1",
                "source_id": "SRC-ASCE-SEI-7",
                "source_rights_id": "RIGHTS-TEST",
                "content_sha256": "a" * 64,
                "admitted_use": "unsafe text exposure",
                "exposure_policy": "hash_only",
                "payload_text_included": True,
                "standard_text": "blocked protected content",
            }
        ],
    }
    manifest_path = repo_root / "006_System-Manifests/test-packets/protected-payload-manifest.json"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

    report = run_gated_review(
        repo_root=repo_root,
        protected_payload_manifest_path=manifest_path,
        run_id="TEST_PROTECTED_PAYLOAD_TEXT_REJECTED",
    )

    assert report["ok"] is False
    assert report["protected_payload_manifest_gate"]["status"] == "rejected"
    assert report["payload_leak_audit"]["status"] == "rejected_for_forbidden_payload_keys"
    assert any("standard_text" in error for error in report["errors"])


def test_gated_review_validates_live_promotion_plan_but_performs_no_write(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repo_root = _temp_repo_with_backbone(tmp_path)
    backup = _write_evidence(repo_root, "006_System-Manifests/test-live/backup.json")
    restore = _write_evidence(repo_root, "006_System-Manifests/test-live/restore-test.json")
    rollback = _write_evidence(repo_root, "006_System-Manifests/test-live/rollback-transcript.json")
    plan = {
        "plan_id": "live-promotion-dry-run-test",
        "approved_by": "Philip Lewis",
        "approved_at": "2026-05-01T00:00:00Z",
        "target_environment": "production",
        "backup_artifact_path": backup.relative_to(repo_root).as_posix(),
        "restore_test_artifact_path": restore.relative_to(repo_root).as_posix(),
        "rollback_transcript_path": rollback.relative_to(repo_root).as_posix(),
    }
    plan_path = repo_root / "006_System-Manifests/test-live/live-promotion-plan.json"
    plan_path.write_text(json.dumps(plan), encoding="utf-8")
    monkeypatch.setenv("VITRUVIUS_PRODUCTION_NEO4J_URI", "bolt://127.0.0.1:7687")
    monkeypatch.setenv("VITRUVIUS_PRODUCTION_NEO4J_USER", "neo4j")
    monkeypatch.setenv("VITRUVIUS_PRODUCTION_NEO4J_PASSWORD", "test-password")

    report = run_gated_review(
        repo_root=repo_root,
        live_promotion_plan_path=plan_path,
        run_id="TEST_LIVE_PROMOTION_DRY_RUN",
    )

    assert report["ok"] is True
    assert report["live_promotion_gate"]["status"] == "credentials_rollback_and_plan_present_dry_run_only"
    assert report["live_promotion_gate"]["missing_credential_names"] == []
    assert report["live_promotion_gate"]["live_write_performed"] is False
    assert report["live_promotion_gate"]["production_promotion_performed"] is False


def test_gated_review_live_promotion_missing_inputs_blocks_without_writes(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repo_root = _temp_repo_with_backbone(tmp_path)
    for name in (
        "VITRUVIUS_PRODUCTION_NEO4J_URI",
        "VITRUVIUS_PRODUCTION_NEO4J_USER",
        "VITRUVIUS_PRODUCTION_NEO4J_PASSWORD",
    ):
        monkeypatch.delenv(name, raising=False)

    report = run_gated_review(repo_root=repo_root, run_id="TEST_LIVE_PROMOTION_BLOCKED")

    assert report["ok"] is True
    assert report["live_promotion_gate"]["status"] == "blocked_missing_credentials_rollback_or_plan"
    assert set(report["live_promotion_gate"]["missing_credential_names"]) == {
        "VITRUVIUS_PRODUCTION_NEO4J_URI",
        "VITRUVIUS_PRODUCTION_NEO4J_USER",
        "VITRUVIUS_PRODUCTION_NEO4J_PASSWORD",
    }
    assert report["live_promotion_gate"]["missing_live_promotion_plan"] is True
    assert report["live_promotion_gate"]["live_write_performed"] is False
    assert report["live_promotion_gate"]["production_promotion_performed"] is False


def test_gated_review_rejects_live_promotion_plan_with_nonproduction_target(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repo_root = _temp_repo_with_backbone(tmp_path)
    backup = _write_evidence(repo_root, "006_System-Manifests/test-live/backup.json")
    restore = _write_evidence(repo_root, "006_System-Manifests/test-live/restore-test.json")
    rollback = _write_evidence(repo_root, "006_System-Manifests/test-live/rollback-transcript.json")
    plan = {
        "plan_id": "live-promotion-invalid-target",
        "approved_by": "Philip Lewis",
        "approved_at": "2026-05-01T00:00:00Z",
        "target_environment": "staging",
        "backup_artifact_path": backup.relative_to(repo_root).as_posix(),
        "restore_test_artifact_path": restore.relative_to(repo_root).as_posix(),
        "rollback_transcript_path": rollback.relative_to(repo_root).as_posix(),
    }
    plan_path = repo_root / "006_System-Manifests/test-live/live-promotion-plan.json"
    plan_path.write_text(json.dumps(plan), encoding="utf-8")
    monkeypatch.setenv("VITRUVIUS_PRODUCTION_NEO4J_URI", "bolt://127.0.0.1:7687")
    monkeypatch.setenv("VITRUVIUS_PRODUCTION_NEO4J_USER", "neo4j")
    monkeypatch.setenv("VITRUVIUS_PRODUCTION_NEO4J_PASSWORD", "test-password")

    report = run_gated_review(
        repo_root=repo_root,
        live_promotion_plan_path=plan_path,
        run_id="TEST_LIVE_PROMOTION_NONPRODUCTION_REJECTED",
    )

    assert report["ok"] is False
    assert report["live_promotion_gate"]["live_write_performed"] is False
    assert report["live_promotion_gate"]["production_promotion_performed"] is False
    assert any("target_environment" in error for error in report["errors"])


def test_gated_review_cli_accepts_all_gate_packet_flags(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    repo_root = _temp_repo_with_backbone(tmp_path)
    steward_evidence = _write_evidence(repo_root, "006_System-Manifests/test-cli/steward-evidence.json")
    authority_evidence = _write_evidence(repo_root, "006_System-Manifests/test-cli/authority-evidence.json")
    payload_evidence = _write_evidence(repo_root, "006_System-Manifests/test-cli/payload-evidence.json")
    backup = _write_evidence(repo_root, "006_System-Manifests/test-cli/backup.json")
    restore = _write_evidence(repo_root, "006_System-Manifests/test-cli/restore.json")
    rollback = _write_evidence(repo_root, "006_System-Manifests/test-cli/rollback.json")
    packet_dir = repo_root / "006_System-Manifests/test-cli/packets"
    packet_dir.mkdir(parents=True, exist_ok=True)

    steward_packet = packet_dir / "steward.json"
    steward_packet.write_text(
        json.dumps(
            {
                "packet_id": "steward-cli",
                "steward": "Philip Lewis",
                "decision_date": "2026-05-01",
                "authority_record_id": "AUTH-STEW-CLI",
                "rationale": "Synthetic CLI dry-run validation.",
                "evidence_paths": [steward_evidence.relative_to(repo_root).as_posix()],
                "decision_scope": "all_current_duplicate_candidates",
                "default_action": "add_display_disambiguation",
            }
        ),
        encoding="utf-8",
    )
    criteria_packet = packet_dir / "criteria.json"
    criteria_packet.write_text(
        json.dumps(
            {
                "packet_id": "criteria-cli",
                "project_id": "project-cli",
                "jurisdiction_id": "jurisdiction-cli",
                "ahj_authority": "CLI AHJ",
                "steward_approval_id": "approval-cli",
                "adopted_sources": [{"source_id": "SRC-ASCE-SEI-7"}],
                "criteria": [
                    {
                        "criterion_name": "Synthetic CLI criterion",
                        "concept_path_code": "STR.LOA.LAT.WND",
                        "value": "synthetic",
                        "units": "synthetic-units",
                        "source_id": "SRC-ASCE-SEI-7",
                        "adopted_edition": "test-edition",
                        "ahj_basis": "test-basis",
                        "effective_date": "2026-05-01",
                        "source_rights_clearance_state": "cleared_for_declared_use",
                        "protected_payload_included": False,
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    authority_ledger = packet_dir / "authority.json"
    authority_ledger.write_text(
        json.dumps(
            {
                "authority_records": [
                    {
                        "authority_id": "AUTH-CLI",
                        "authority_type": "ahj",
                        "scope": "synthetic CLI validation",
                        "decision_status": "approved",
                        "steward": "Philip Lewis",
                        "decision_date": "2026-05-01",
                        "evidence_paths": [authority_evidence.relative_to(repo_root).as_posix()],
                        "source_rights_ids": ["SRC-ASCE-SEI-7"],
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    protected_manifest = packet_dir / "protected-payload.json"
    protected_manifest.write_text(
        json.dumps(
            {
                "manifest_id": "protected-cli",
                "steward": "Philip Lewis",
                "decision_date": "2026-05-01",
                "authority_record_ids": ["AUTH-CLI"],
                "evidence_paths": [payload_evidence.relative_to(repo_root).as_posix()],
                "payloads": [
                    {
                        "payload_id": "payload-cli",
                        "source_id": "SRC-ASCE-SEI-7",
                        "source_rights_id": "RIGHTS-CLI",
                        "content_sha256": "b" * 64,
                        "admitted_use": "hash-only CLI validation",
                        "exposure_policy": "hash_only",
                        "payload_text_included": False,
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    live_plan = packet_dir / "live-plan.json"
    live_plan.write_text(
        json.dumps(
            {
                "plan_id": "live-cli",
                "approved_by": "Philip Lewis",
                "approved_at": "2026-05-01T00:00:00Z",
                "target_environment": "production",
                "backup_artifact_path": backup.relative_to(repo_root).as_posix(),
                "restore_test_artifact_path": restore.relative_to(repo_root).as_posix(),
                "rollback_transcript_path": rollback.relative_to(repo_root).as_posix(),
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setenv("VITRUVIUS_PRODUCTION_NEO4J_URI", "bolt://127.0.0.1:7687")
    monkeypatch.setenv("VITRUVIUS_PRODUCTION_NEO4J_USER", "neo4j")
    monkeypatch.setenv("VITRUVIUS_PRODUCTION_NEO4J_PASSWORD", "test-password")

    exit_code = main(
        [
            "--repo-root",
            str(repo_root),
            "--run-id",
            "TEST_CLI_ALL_FLAGS",
            "--steward-decision-packet",
            str(steward_packet),
            "--criteria-packet",
            str(criteria_packet),
            "--authority-ledger",
            str(authority_ledger),
            "--protected-payload-manifest",
            str(protected_manifest),
            "--live-promotion-plan",
            str(live_plan),
        ]
    )

    captured = capsys.readouterr()
    report = json.loads(captured.out)
    assert exit_code == 0
    assert report["steward_duplicate_decision_gate"]["status"] == "validated_not_applied"
    assert report["criteria_admission_gate"]["status"] == "validated_not_admitted"
    assert report["external_authority_ledger_gate"]["status"] == "validated_not_admitted"
    assert report["protected_payload_manifest_gate"]["status"] == "validated_not_ingested"
    assert report["live_promotion_gate"]["status"] == "credentials_rollback_and_plan_present_dry_run_only"
    assert report["boundaries"]["production_promotion"] is False


def test_gated_review_rejects_packet_path_escape(tmp_path: Path) -> None:
    repo_root = _temp_repo_with_backbone(tmp_path)
    outside_packet = tmp_path.parent / "criteria-escape.json"
    outside_packet.write_text(json.dumps({"packet_id": "escape"}), encoding="utf-8")

    with pytest.raises(ValueError, match="path escapes repository root"):
        run_gated_review(
            repo_root=repo_root,
            run_id="TEST_PACKET_PATH_ESCAPE",
            criteria_packet_path=outside_packet,
        )


def test_gated_review_rejects_raw_source_output_dir(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="immutable raw source custody layer"):
        repo_root = _temp_repo_with_backbone(tmp_path)
        run_gated_review(repo_root=repo_root, run_id="RAW_OUTPUT_BLOCKED", output_dir="001_Raw-Source-Layer/gated-review")


def test_gated_review_rejects_canonical_layer_output_dir(tmp_path: Path) -> None:
    repo_root = _temp_repo_with_backbone(tmp_path)
    with pytest.raises(ValueError, match="System-Manifests gated-review report root"):
        run_gated_review(
            repo_root=repo_root,
            run_id="CANONICAL_OUTPUT_BLOCKED",
            output_dir="003_Canonical-Knowledge-Layer/gated-review",
        )
