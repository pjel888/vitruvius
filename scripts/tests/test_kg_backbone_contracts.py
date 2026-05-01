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


def _admitted_backbone_payload() -> dict[str, Any]:
    return json.loads(
        (FIXTURE_DIR / "admitted_backbone_nodes_l1_l2.json").read_text(encoding="utf-8")
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


def test_admitted_backbone_node_fixture_passes_strict_model_rules() -> None:
    report = validate_backbone_contract_file(
        FIXTURE_DIR / "admitted_backbone_nodes_l1_l2.json"
    )

    assert report.ok is True
    assert report.errors == []
    assert report.record_counts == {"BackboneNode": 9880}
    assert report.predicate_counts == {
        "applicable_in_jurisdiction": 12,
        "broader_than": 9856,
        "conflicts_with": 2,
        "constrains": 379,
        "governs": 104,
        "has_facet": 1532,
        "maps_to_external_standard": 739,
        "part_of": 92,
        "requires": 567,
        "supersedes": 2,
    }
    assert report.owner_coverage.to_dict() == {
        "present": 9880,
        "total": 9880,
        "ratio": 1.0,
    }
    payload = _admitted_backbone_payload()
    roots = {record["path_code"] for record in payload["records"] if record["level"] == 1}
    assert len(roots) == 24
    assert {"ARC", "CIV", "STR", "ELE", "URB", "HIS", "FIG", "SAN", "SEC", "SMS", "HRC", "LAW"} <= roots
    records = payload["records"]
    assert sum(1 for record in records if record["level"] == 2) == 406
    assert sum(1 for record in records if record["level"] == 3) == 1510
    assert sum(1 for record in records if record["level"] == 4) == 7940
    assert all(
        len(segment) == 3
        for record in records
        for segment in record["path_code"].split(".")
    )
    synthesized_records = [
        record
        for record in records
        if "synthesized from repo research" in record.get("scope_note", "")
    ]
    assert len(synthesized_records) == 870
    assert {record.get("generation_method") for record in synthesized_records} == {
        "steward_governed_batch_synthesis_from_public_topic_structures"
    }
    architecture_records = [
        record for record in records if record["path_code"].startswith("ARC")
    ]
    assert len(architecture_records) == 1259
    assert sum(1 for record in architecture_records if record["level"] == 2) == 39
    assert sum(1 for record in architecture_records if record["level"] == 3) == 146
    assert sum(1 for record in architecture_records if record["level"] == 4) == 1073
    architecture_expansion_records = [
        record
        for record in architecture_records
        if record.get("generation_method")
        == "steward_governed_batch_synthesis_from_public_architecture_licensure_and_curriculum_sources"
    ]
    assert len(architecture_expansion_records) == 105
    deep_population_records = [
        record
        for record in records
        if record.get("generation_method")
        == "steward_governed_deep_population_from_public_accreditation_licensure_curriculum_and_raw_source_filename_signals"
    ]
    assert len(deep_population_records) == 728
    assert {"ARC.WAC", "HIS.PMA", "LAW.PNB", "SEC.VSS", "SAN.WST"} <= {
        record["path_code"] for record in records
    }
    assert {"ARC.THE", "ARC.PRC", "ARC.COD", "ARC.REG"} <= {
        record["path_code"] for record in architecture_records
    }
    architecture_l4_records = [
        record for record in architecture_records if record["level"] == 4
    ]
    blocked_scaffold_suffixes = (" Concepts", " Concept Anchor", " Rule Context")
    assert not [
        record["path_code"]
        for record in architecture_l4_records
        if record["label"].endswith(blocked_scaffold_suffixes)
    ]
    architecture_l4_parent_counts: dict[str, int] = {}
    for record in architecture_l4_records:
        architecture_l4_parent_counts[record["parent_path_code"]] = (
            architecture_l4_parent_counts.get(record["parent_path_code"], 0) + 1
        )
    assert len(architecture_l4_parent_counts) == 146
    assert min(architecture_l4_parent_counts.values()) >= 6
    real_architecture_semantic_records = [
        record
        for record in architecture_l4_records
        if record.get("generation_method")
        == (
            "steward_governed_real_architecture_semantic_enrichment_from_public_"
            "licensure_curriculum_accreditation_and_professional_topic_structures"
        )
    ]
    assert len(real_architecture_semantic_records) == 878
    assert {
        "ARC.PRC.LEG.SAP",
        "ARC.PRC.LEG.SSA",
        "ARC.COD.BCA.OCR",
        "ARC.HIS.SEA.BKS",
        "ARC.WAC.MSW.GRV",
        "ARC.DTS.CPT.VFU",
    } <= {record["path_code"] for record in real_architecture_semantic_records}
    all_l4_records = [record for record in records if record["level"] == 4]
    assert not [
        record["path_code"]
        for record in all_l4_records
        if record["label"].endswith((*blocked_scaffold_suffixes, " Topics"))
    ]
    broad_semantic_records = [
        record
        for record in all_l4_records
        if record.get("generation_method")
        == (
            "steward_governed_real_broad_taxonomy_semantic_enrichment_from_public_"
            "engineering_code_curriculum_practice_and_operations_topic_structures"
        )
    ]
    assert len(broad_semantic_records) == 6240
    broad_parent_counts: dict[str, int] = {}
    for record in broad_semantic_records:
        broad_parent_counts[record["parent_path_code"]] = (
            broad_parent_counts.get(record["parent_path_code"], 0) + 1
        )
    assert len(broad_parent_counts) == 1248
    assert min(broad_parent_counts.values()) == 5
    assert max(broad_parent_counts.values()) == 5
    assert {
        "ELE.LGT",
        "FLS.EGR",
        "SAN.PHE",
        "SEC.VSS",
        "SMS.IOT",
        "LAW.NBC",
        "HRC.PRN",
        "STR.CON",
        "CIV.BRG",
    } <= {".".join(record["path_code"].split(".")[:2]) for record in broad_semantic_records}
    targeted_semantic_records = [
        record
        for record in records
        if record.get("generation_method")
        == (
            "steward_governed_targeted_semantic_enrichment_from_kimi_guided_public_"
            "aec_mepfs_standard_family_taxonomies"
        )
    ]
    assert len(targeted_semantic_records) == 141
    targeted_kinds: dict[str, int] = {}
    for record in targeted_semantic_records:
        targeted_kinds[record["semantic_node_kind"]] = (
            targeted_kinds.get(record["semantic_node_kind"], 0) + 1
        )
    assert targeted_kinds == {
        "discipline_topic": 88,
        "standard_family": 8,
        "standard_reference": 45,
    }
    assert {
        "COM.STD.ASH.VNT",
        "COM.STD.NFP.NEC",
        "COM.STD.TIA.CAB",
        "COM.STD.NIS.IOT",
        "COM.STD.ICM.VEN",
        "MEC.VEN.OAI.DCV",
        "ELE.PDS.TRS.SCS",
        "FLS.SMK.SCO.FCP",
        "PLS.PWS.BAP.RPZ",
        "SAN.PHE.HRC.HSP",
        "SEC.VSS.VIA.LPR",
        "SMS.IOT.DIX.DCE",
        "SUS.CAR.LCA.GSD",
        "OPS.AST.AIM.CBM",
    } <= {record["path_code"] for record in targeted_semantic_records}
    assert all(record.get("source_family_ids") for record in targeted_semantic_records)
    targeted_relationships = [
        relationship
        for relationship in payload["relationships"]
        if relationship.get("generation_method")
        == (
            "steward_governed_targeted_semantic_enrichment_from_kimi_guided_public_"
            "aec_mepfs_standard_family_taxonomies"
        )
    ]
    targeted_predicates: dict[str, int] = {}
    for relationship in targeted_relationships:
        targeted_predicates[relationship["predicate"]] = (
            targeted_predicates.get(relationship["predicate"], 0) + 1
        )
    assert targeted_predicates == {
        "broader_than": 141,
        "constrains": 45,
        "has_facet": 8,
        "maps_to_external_standard": 88,
        "part_of": 45,
        "requires": 88,
    }
    overlay_records = [
        record
        for record in records
        if record.get("generation_method")
        == (
            "steward_governed_cross_domain_overlay_enrichment_from_kimi_guided_public_"
            "aec_mepfs_coordination_commissioning_resilience_and_applicability_sources"
        )
    ]
    assert len(overlay_records) == 91
    overlay_kinds: dict[str, int] = {}
    for record in overlay_records:
        overlay_kinds[record["semantic_node_kind"]] = (
            overlay_kinds.get(record["semantic_node_kind"], 0) + 1
        )
    assert overlay_kinds == {
        "commissioning_overlay": 14,
        "semantic_overlay": 47,
        "semantic_overlay_parent": 3,
        "standard_family": 6,
        "standard_reference": 21,
    }
    assert {
        "COM.APP.AHJ",
        "COM.APP.SDC",
        "STR.NSC.SRN",
        "STR.NSC.FST",
        "CON.COM.IST",
        "CON.COM.COB",
        "PER.ORC.BCP",
        "PER.ORC.WSR",
        "COM.STD.FEM.NSE",
        "COM.STD.NFP.EPS",
        "COM.STD.ISO.BCM",
        "COM.STD.ISA.IAC",
    } <= {record["path_code"] for record in overlay_records}
    assert all(record.get("source_family_ids") for record in overlay_records)
    overlay_relationships = [
        relationship
        for relationship in payload["relationships"]
        if relationship.get("generation_method")
        == (
            "steward_governed_cross_domain_overlay_enrichment_from_kimi_guided_public_"
            "aec_mepfs_coordination_commissioning_resilience_and_applicability_sources"
        )
    ]
    assert len(overlay_relationships) == 460
    overlay_predicates: dict[str, int] = {}
    overlay_categories: dict[str, int] = {}
    for relationship in overlay_relationships:
        overlay_predicates[relationship["predicate"]] = (
            overlay_predicates.get(relationship["predicate"], 0) + 1
        )
        overlay_categories[relationship["semantic_overlay_category"]] = (
            overlay_categories.get(relationship["semantic_overlay_category"], 0) + 1
        )
    assert overlay_predicates == {
        "applicable_in_jurisdiction": 6,
        "broader_than": 91,
        "constrains": 164,
        "governs": 8,
        "maps_to_external_standard": 42,
        "part_of": 21,
        "requires": 128,
    }
    assert overlay_categories == {
        "applicability_overlay": 92,
        "commissioning_handover": 76,
        "equipment_anchorage": 101,
        "hierarchy": 91,
        "resilience_continuity": 79,
        "source_reference": 21,
    }

    resolver_deepening_records = [
        record
        for record in records
        if record.get("generation_method")
        == (
            "steward_governed_lea_ale_resolver_deepening_from_kimi_guided_"
            "public_query_path_and_source_rights_review"
        )
    ]
    assert len(resolver_deepening_records) == 102
    assert {
        "ARC.BLD.SRV.UCO",
        "ARC.BLD.SRV.RCP",
        "ARC.BLD.STR.SCA",
        "ARC.BLD.STR.NCC",
        "COM.STD.PHL.BFM",
    } <= {record["path_code"] for record in resolver_deepening_records}
    assert {
        "COM.STD.PHL.RUM",
        "COM.STD.PHL.RHE",
        "COM.STD.PHL.RTR",
        "COM.STD.PHL.RSB",
        "COM.STD.PHL.RFA",
        "COM.STD.PHL.RTA",
    }.isdisjoint({record["path_code"] for record in resolver_deepening_records})
    resolver_deepening_relationships = [
        relationship
        for relationship in payload["relationships"]
        if relationship.get("generation_method")
        == (
            "steward_governed_lea_ale_resolver_deepening_from_kimi_guided_"
            "public_query_path_and_source_rights_review"
        )
    ]
    assert len(resolver_deepening_relationships) == 644
    assert {
        "applicable_in_jurisdiction",
        "conflicts_with",
        "supersedes",
        "requires",
    } <= {relationship["predicate"] for relationship in resolver_deepening_relationships}


def test_candidate_backbone_node_can_remain_minimal_before_admission() -> None:
    payload = _valid_payload()
    payload["records"][0].pop("path_code", None)
    payload["records"][0].pop("pref_label", None)

    report = validate_backbone_contract(payload)

    assert report.ok is True
    assert report.errors == []


def test_admitted_backbone_node_requires_v2_fields() -> None:
    payload = _admitted_backbone_payload()
    payload["records"][0].pop("path_code")

    report = validate_backbone_contract(payload)

    assert report.ok is False
    assert "records[0].path_code: required for admitted BackboneNode" in report.errors


def test_admitted_backbone_node_rejects_mismatched_identity_alias_fields() -> None:
    payload = _admitted_backbone_payload()
    payload["records"][1]["canonical_id"] = "VTN-DOM-9999999"
    payload["records"][1]["pref_label"] = "Planning"
    payload["records"][1]["steward"] = "Another Steward"

    report = validate_backbone_contract(payload)

    assert report.ok is False
    assert "records[1].canonical_id: must match id" in report.errors
    assert "records[1].pref_label: must match label" in report.errors
    assert "records[1].steward: must match owner" in report.errors


def test_admitted_backbone_node_rejects_duplicate_path_code() -> None:
    payload = _admitted_backbone_payload()
    payload["records"][3]["path_code"] = "ARC.SPC"

    report = validate_backbone_contract(payload)

    assert report.ok is False
    assert "records: duplicate admitted BackboneNode path_code 'ARC.SPC'" in report.errors


def test_admitted_backbone_node_rejects_missing_or_wrong_parent() -> None:
    payload = _admitted_backbone_payload()
    payload["records"][1]["parent_path_code"] = "MEC"
    payload["records"][4]["parent_path_code"] = "MEC.MISSING"

    report = validate_backbone_contract(payload)

    assert report.ok is False
    assert "records[1].parent_path_code: expected ARC, found MEC" in report.errors
    assert (
        "records[4].parent_path_code: parent 'MEC.MISSING' is not admitted in fixture"
        in report.errors
    )


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
        "resolver_error_cases": 5,
        "resolver_golden_cases": 117,
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


def test_resolver_golden_cases_require_query_text_for_contract_surface() -> None:
    payload = _s2_payload()
    payload["resolver_golden_cases"][0]["query"].pop("text")

    report = validate_backbone_contract(payload)

    assert report.ok is False
    assert "resolver_golden_cases[0].query.text: required field missing" in report.errors


def test_resolver_golden_cases_require_full_result_type_coverage() -> None:
    payload = _s2_payload()
    payload["resolver_golden_cases"] = payload["resolver_golden_cases"][:3]

    report = validate_backbone_contract(payload)

    assert report.ok is False
    assert "resolver_golden_cases: missing result-type coverage (none)" in report.errors


def test_resolver_error_cases_require_full_error_type_coverage() -> None:
    payload = _s2_payload()
    payload["resolver_error_cases"] = [
        case
        for case in payload["resolver_error_cases"]
        if case["expected_error_type"] != "blocked_runtime_route"
    ]

    report = validate_backbone_contract(payload)

    assert report.ok is False
    assert (
        "resolver_error_cases: missing error-type coverage (blocked_runtime_route)"
        in report.errors
    )


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


@pytest.mark.parametrize(
    "route",
    [
        "/v2/resolve/context",
        "/v2/resolve/trace",
    ],
)
def test_api_explorer_parity_case_rejects_non_exact_resolver_routes(route: str) -> None:
    payload = _s2_payload()
    payload["api_explorer_parity_cases"][1]["route"] = route
    payload["api_explorer_parity_cases"][1]["default_off_only"] = True
    payload["api_explorer_parity_cases"][1][
        "covered_by_command"
    ] = "(cd api && bun test v2Resolver.test.ts)"
    payload["api_explorer_parity_cases"][1][
        "execution_mode"
    ] = "api_default_off_resolver_unit"

    report = validate_backbone_contract(payload)

    assert report.ok is False
    assert (
        "api_explorer_parity_cases[1].route: /v2/resolve parity cases must use "
        "exact default-off resolver routes only"
    ) in report.errors


def test_api_explorer_parity_case_requires_default_off_resolver_guard_metadata() -> None:
    payload = _s2_payload()
    payload["api_explorer_parity_cases"][1]["route"] = "/v2/resolve"

    report = validate_backbone_contract(payload)

    assert report.ok is False
    assert (
        "api_explorer_parity_cases[1].default_off_only: /v2/resolve parity cases "
        "must declare default_off_only=true"
    ) in report.errors
    assert (
        "api_explorer_parity_cases[1].execution_mode: /v2/resolve parity cases "
        "must use api_default_off_resolver_unit"
    ) in report.errors
    assert (
        "api_explorer_parity_cases[1].covered_by_command: /v2/resolve parity cases "
        "must be covered by (cd api && bun test v2Resolver.test.ts)"
    ) in report.errors


@pytest.mark.parametrize("route", ["/v2/resolve", "/v2/resolve/trace/:trace_id"])
def test_api_explorer_parity_case_allows_default_off_resolver_routes(route: str) -> None:
    payload = _s2_payload()
    payload["api_explorer_parity_cases"][1]["route"] = route
    payload["api_explorer_parity_cases"][1]["default_off_only"] = True
    payload["api_explorer_parity_cases"][1][
        "covered_by_command"
    ] = "(cd api && bun test v2Resolver.test.ts)"
    payload["api_explorer_parity_cases"][1][
        "execution_mode"
    ] = "api_default_off_resolver_unit"

    report = validate_backbone_contract(payload)

    assert report.ok is True


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
