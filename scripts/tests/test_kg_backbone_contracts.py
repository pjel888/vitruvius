from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from vitruvius.kg.backbone_contracts import (
    validate_backbone_contract,
    validate_backbone_contract_file,
)


FIXTURE_DIR = Path(__file__).parent / "fixtures" / "aec_mepfs_backbone"


def _valid_payload() -> dict[str, Any]:
    return json.loads((FIXTURE_DIR / "valid_minimal.json").read_text(encoding="utf-8"))


def _s2_payload() -> dict[str, Any]:
    return json.loads((FIXTURE_DIR / "valid_readiness_s2.json").read_text(encoding="utf-8"))


def _s3_payload() -> dict[str, Any]:
    return json.loads(
        (FIXTURE_DIR / "valid_integration_readiness_s3.json").read_text(encoding="utf-8")
    )


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
    assert any(
        "vague governed predicate 'related_to' is blocked" in error for error in report.errors
    )


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


def test_readiness_s2_fixture_passes_with_registry_and_case_counts() -> None:
    report = validate_backbone_contract_file(FIXTURE_DIR / "valid_readiness_s2.json")

    assert report.ok is True
    assert report.errors == []
    assert report.warnings == ["shadow_rollback_plan: rollback proof is planned, not executed"]
    assert report.readiness_case_counts == {
        "api_explorer_parity_cases": 3,
        "authoring_migration_cases": 3,
        "resolver_golden_cases": 4,
    }
    assert report.predicate_registry_coverage.to_dict() == {
        "present": 12,
        "total": 12,
        "ratio": 1.0,
    }
    assert report.source_rights_registry_coverage.to_dict() == {
        "present": 3,
        "total": 3,
        "ratio": 1.0,
    }


def test_known_list_sections_fail_when_malformed() -> None:
    payload = _s2_payload()
    payload["predicate_registry"] = {"predicate": "broader_than"}
    payload["source_rights_registry"] = ["not an object"]

    report = validate_backbone_contract(payload)

    assert report.ok is False
    assert "predicate_registry: expected a list" in report.errors
    assert "source_rights_registry[0]: expected an object" in report.errors


def test_predicate_registry_entry_rejects_vague_predicate() -> None:
    payload = _s2_payload()
    payload["predicate_registry"][0]["predicate"] = "related_to"

    report = validate_backbone_contract(payload)

    assert report.ok is False
    assert any(
        "predicate_registry[0].predicate: vague predicate 'related_to' is blocked" == error
        for error in report.errors
    )


def test_predicate_registry_entry_rejects_unknown_governed_predicate() -> None:
    payload = _s2_payload()
    payload["predicate_registry"][0]["predicate"] = "influences"

    report = validate_backbone_contract(payload)

    assert report.ok is False
    assert any(
        "predicate_registry[0].predicate: unknown governed predicate 'influences'" == error
        for error in report.errors
    )


def test_predicate_registry_entry_requires_non_empty_list_fields() -> None:
    payload = _s2_payload()
    payload["predicate_registry"][0]["allowed_strength_classes"] = []

    report = validate_backbone_contract(payload)

    assert report.ok is False
    assert any(
        "predicate_registry[0].allowed_strength_classes: expected a non-empty list" == error
        for error in report.errors
    )


def test_source_rights_registry_content_ingest_requires_clearance_and_legal_review() -> None:
    payload = _s2_payload()
    payload["source_rights_registry"][0]["source_rights_class"] = "content_ingest"
    payload["source_rights_registry"][0]["clearance_state"] = "clearance_required"

    report = validate_backbone_contract(payload)

    assert report.ok is False
    assert any(
        "source_rights_registry[0]: content_ingest requires clearance_state "
        "'cleared_for_declared_use'" == error
        for error in report.errors
    )
    assert (
        "source_rights_registry[0].legal_reviewer: required for content_ingest"
        in report.errors
    )
    assert (
        "source_rights_registry[0].reviewer_decision: required for content_ingest"
        in report.errors
    )


def test_source_rights_registry_rejects_unsupported_enum_values() -> None:
    payload = _s2_payload()
    payload["source_rights_registry"][0]["clearance_state"] = "unknown"
    payload["source_rights_registry"][0]["source_rights_class"] = "free_for_everything"

    report = validate_backbone_contract(payload)

    assert report.ok is False
    assert "source_rights_registry[0].clearance_state: unsupported value 'unknown'" in report.errors
    assert (
        "source_rights_registry[0].source_rights_class: unsupported value 'free_for_everything'"
        in report.errors
    )


def test_authoring_migration_case_blocks_ai_authored_l1_or_l2_change() -> None:
    payload = _s2_payload()
    payload["authoring_migration_cases"][1]["proposed_by"] = "ai"

    report = validate_backbone_contract(payload)

    assert report.ok is False
    assert "authoring_migration_cases[1]: AI-authored L1 changes are blocked" in report.errors


@pytest.mark.parametrize(
    ("field_name", "value", "expected_error"),
    [
        (
            "proposal_level",
            "L2",
            "authoring_migration_cases[0]: auto_accept is only allowed for L3/L4 proposals",
        ),
        (
            "confidence",
            0.91,
            "authoring_migration_cases[0]: auto_accept requires confidence >= 0.92",
        ),
        (
            "workflow",
            "manual_review",
            "authoring_migration_cases[0]: auto_accept requires LD-8 PlacementAssertion workflow",
        ),
    ],
)
def test_authoring_migration_auto_accept_requires_ld8_high_confidence_l3_l4(
    field_name: str,
    value: Any,
    expected_error: str,
) -> None:
    payload = _s2_payload()
    payload["authoring_migration_cases"][0][field_name] = value

    report = validate_backbone_contract(payload)

    assert report.ok is False
    assert expected_error in report.errors


def test_resolver_golden_cases_require_effective_date_not_legacy_date_fields() -> None:
    payload = _s2_payload()
    payload["resolver_golden_cases"][0]["query_date"] = "2026-04-25"

    report = validate_backbone_contract(payload)

    assert report.ok is False
    assert "resolver_golden_cases[0].query_date: use effective_date instead" in report.errors


def test_resolver_golden_cases_require_full_result_type_coverage() -> None:
    payload = _s2_payload()
    payload["resolver_golden_cases"] = payload["resolver_golden_cases"][:3]

    report = validate_backbone_contract(payload)

    assert report.ok is False
    assert "resolver_golden_cases: missing result-type coverage (none)" in report.errors


def test_api_explorer_parity_case_requires_v1_preservation_flag() -> None:
    payload = _s2_payload()
    payload["api_explorer_parity_cases"][0]["preserves_v1"] = False

    report = validate_backbone_contract(payload)

    assert report.ok is False
    assert (
        "api_explorer_parity_cases[0].preserves_v1: v1 parity cases must preserve v1 behavior"
        in report.errors
    )


def test_api_explorer_parity_case_rejects_unknown_surface() -> None:
    payload = _s2_payload()
    payload["api_explorer_parity_cases"][0]["surface"] = "beta"

    report = validate_backbone_contract(payload)

    assert report.ok is False
    assert "api_explorer_parity_cases[0].surface: unsupported value 'beta'" in report.errors


def test_api_explorer_parity_case_requires_v2_shadow_route_and_shadow_only_flag() -> None:
    payload = _s2_payload()
    payload["api_explorer_parity_cases"][1]["route"] = "/backbone/node/:id"
    payload["api_explorer_parity_cases"][1]["shadow_only"] = False

    report = validate_backbone_contract(payload)

    assert report.ok is False
    assert (
        "api_explorer_parity_cases[1].route: v2 parity cases must use /v2 shadow routes"
        in report.errors
    )
    assert (
        "api_explorer_parity_cases[1].shadow_only: v2 parity cases must be shadow-only"
        in report.errors
    )


def test_shadow_rollback_plan_requires_true_block_and_executed_evidence() -> None:
    payload = _s2_payload()
    payload["shadow_rollback_plan"]["destructive_operations_blocked"] = False
    payload["shadow_rollback_plan"]["proof_status"] = "executed"

    report = validate_backbone_contract(payload)

    assert report.ok is False
    assert (
        "shadow_rollback_plan.destructive_operations_blocked: must be true"
        in report.errors
    )
    assert (
        "shadow_rollback_plan.evidence_artifact: required when proof_status is executed"
        in report.errors
    )


def test_integration_readiness_s3_fixture_passes_with_gate_counts() -> None:
    report = validate_backbone_contract_file(
        FIXTURE_DIR / "valid_integration_readiness_s3.json"
    )

    assert report.ok is True
    assert report.errors == []
    assert report.warnings == [
        "integration_rollback_proof_plan: rollback proof is planned, not executed"
    ]
    assert report.integration_gate_counts == {
        "blocked_external": 1,
        "blocked_runtime": 1,
        "closed": 4,
    }
    assert report.registry_location_coverage.to_dict() == {
        "present": 6,
        "total": 6,
        "ratio": 1.0,
    }


def test_integration_registry_locations_reject_unsafe_paths() -> None:
    payload = _s3_payload()
    payload["integration_registry_locations"][0]["path"] = "/tmp/predicate-registry.json"
    payload["integration_registry_locations"][1]["path"] = "001_Raw-Source-Layer/source.json"

    report = validate_backbone_contract(payload)

    assert report.ok is False
    assert (
        "integration_registry_locations[0].path: path must be repo-relative"
        in report.errors
    )
    assert (
        "integration_registry_locations[1].path: path is outside allowed readiness prefixes"
        in report.errors
    )


def test_integration_paths_reject_invalid_segment_characters() -> None:
    payload = _s3_payload()
    payload["integration_parity_runner_plan"][
        "report_path"
    ] = "006_System-Manifests/aec-mepfs-backbone/parity/<run_id>/report.json"

    report = validate_backbone_contract(payload)

    assert report.ok is False
    assert (
        "integration_parity_runner_plan.report_path: path contains invalid segment characters"
        in report.errors
    )


def test_integration_readiness_bundle_requires_all_s3_sections() -> None:
    payload = _s3_payload()
    payload.pop("integration_parity_runner_plan")
    payload.pop("integration_rollback_proof_plan")
    payload.pop("integration_benchmark_plan")
    payload.pop("integration_readiness_gates")
    payload.pop("integration_registry_locations")

    payload["integration_registry_locations"] = []

    report = validate_backbone_contract(payload)

    assert report.ok is False
    assert (
        "integration_parity_runner_plan: required when integration readiness sections "
        "are present"
    ) in report.errors
    assert (
        "integration_rollback_proof_plan: required when integration readiness sections "
        "are present"
    ) in report.errors
    assert (
        "integration_benchmark_plan: required when integration readiness sections are present"
        in report.errors
    )
    assert (
        "integration_readiness_gates: required when integration readiness sections are present"
        in report.errors
    )
    assert "integration_registry_locations: expected a non-empty list" in report.errors


def test_integration_registry_locations_reject_unknown_control_values() -> None:
    payload = _s3_payload()
    location = payload["integration_registry_locations"][0]
    location["lifecycle_state"] = "drafting"
    location["promotion_gate"] = "looks_good"
    location["runtime_consumer"] = "mystery_consumer"
    location["validator"] = "manual_review"

    report = validate_backbone_contract(payload)

    assert report.ok is False
    assert (
        "integration_registry_locations[0].lifecycle_state: unsupported value 'drafting'"
        in report.errors
    )
    assert (
        "integration_registry_locations[0].promotion_gate: unsupported value 'looks_good'"
        in report.errors
    )
    assert (
        "integration_registry_locations[0].runtime_consumer: unsupported value "
        "'mystery_consumer'"
    ) in report.errors
    assert (
        "integration_registry_locations[0].validator: unsupported value 'manual_review'"
        in report.errors
    )


def test_integration_parity_runner_requires_exact_surfaces_and_report_gate() -> None:
    payload = _s3_payload()
    payload["integration_parity_runner_plan"]["surfaces"] = ["v2"]
    payload["integration_parity_runner_plan"]["blocks_runtime_without_report"] = False

    report = validate_backbone_contract(payload)

    assert report.ok is False
    assert "integration_parity_runner_plan.surfaces: must cover exactly v1 and v2" in report.errors
    assert (
        "integration_parity_runner_plan.blocks_runtime_without_report: must be true"
        in report.errors
    )


def test_integration_rollback_proof_requires_block_and_executed_evidence() -> None:
    payload = _s3_payload()
    payload["integration_rollback_proof_plan"]["destructive_operations_blocked"] = False
    payload["integration_rollback_proof_plan"]["proof_status"] = "executed"

    report = validate_backbone_contract(payload)

    assert report.ok is False
    assert (
        "integration_rollback_proof_plan.destructive_operations_blocked: must be true"
        in report.errors
    )
    assert (
        "integration_rollback_proof_plan.evidence_artifact: required when proof_status is executed"
        in report.errors
    )


def test_integration_benchmark_plan_requires_repetitions_and_p95() -> None:
    payload = _s3_payload()
    payload["integration_benchmark_plan"]["repetitions"] = 1
    payload["integration_benchmark_plan"]["percentiles"] = ["p50"]

    report = validate_backbone_contract(payload)

    assert report.ok is False
    assert "integration_benchmark_plan.repetitions: must be >= 3" in report.errors
    assert "integration_benchmark_plan.percentiles: must include p95" in report.errors


def test_integration_benchmark_plan_rejects_non_list_percentiles() -> None:
    payload = _s3_payload()
    payload["integration_benchmark_plan"]["percentiles"] = "p95"

    report = validate_backbone_contract(payload)

    assert report.ok is False
    assert "integration_benchmark_plan.percentiles: expected a non-empty list" in report.errors


def test_open_runtime_blocking_gates_require_blocker_reason() -> None:
    payload = _s3_payload()
    payload["integration_readiness_gates"][3].pop("blocker")

    report = validate_backbone_contract(payload)

    assert report.ok is False
    assert (
        "integration_readiness_gates[3].blocker: required when an open gate blocks runtime"
        in report.errors
    )
