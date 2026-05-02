from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from vitruvius.kg.architecture_civil_structural_enrichment import (
    GENERATION_METHOD,
    apply_enrichment,
    enrich_backbone_payload,
    enrich_readiness_fixture,
    enrich_source_rights_payload,
    summarize_delta,
)
from vitruvius.kg.architecture_civil_structural_quality import (
    run_quality_score_report,
    score_architecture_civil_structural_quality,
)
from vitruvius.kg.backbone_graph_quality import analyze_backbone_graph_quality


FIXTURE = Path("scripts/tests/fixtures/aec_mepfs_backbone/admitted_backbone_nodes_l1_l2.json")
SOURCE_RIGHTS = Path(".ai/03_plans/AEC-MEPFS-Backbone/registry-candidates/source-rights-registry.json")
READINESS = Path("scripts/tests/fixtures/aec_mepfs_backbone/valid_readiness_s2.json")


def _load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _id_by_path(payload: dict[str, Any], path_code: str) -> str:
    for record in payload["records"]:
        if record.get("path_code") == path_code:
            return str(record["id"])
    raise AssertionError(f"missing path_code {path_code}")


def _edge(
    payload: dict[str, Any],
    from_path: str,
    to_path: str,
    relation_type: str,
) -> dict[str, Any]:
    from_id = _id_by_path(payload, from_path)
    to_id = _id_by_path(payload, to_path)
    for row in payload["relationships"]:
        if (
            row.get("from_id") == from_id
            and row.get("to_id") == to_id
            and row.get("relation_type") == relation_type
        ):
            return row
    raise AssertionError(f"missing edge {from_path} -> {to_path} relation_type={relation_type}")


def test_acs_enrichment_is_idempotent_on_current_fixture() -> None:
    payload = _load(FIXTURE)

    enriched = enrich_backbone_payload(payload)
    delta = summarize_delta(payload, enriched)

    assert delta["new_node_count"] == 0
    assert delta["new_relationship_count"] == 0
    assert delta["acs_relationship_count"] >= 143
    assert delta["acs_hierarchy_relationship_count"] >= 79
    assert delta["refined_node_count"] >= 87


def test_acs_relationships_support_cross_taxonomy_reasoning() -> None:
    payload = _load(FIXTURE)

    checks = [
        ("CIV.SDV.ACC.PSG", "ARC.SPC.CIR.ASR", "constrains_accessible_route_slope_and_cross_slope"),
        ("ARC.SPC.CIR.ASR", "CIV.SDV.ACC.PSG", "requires_pedestrian_gradient_control_for_accessible_route"),
        ("ARC.ENV.ROF.RDI", "CIV.DRN.CON.RDO", "discharges_roof_runoff_to_site_network"),
        ("CIV.DRN.CON.RDO", "CIV.DRN.CON.CBI", "routes_roof_runoff_to_stormwater_inlet_or_pipe"),
        ("GEO.FOE.ABP", "STR.FND.SHL.FBC", "translates_soil_capacity_to_foundation_design"),
        ("STR.RCS.SBC.SLS", "STR.SSS.BEG.SBM", "transfers_gravity_load_to"),
        ("STR.SSS.BEG.SBM", "STR.RCS.SBC.COL", "transfers_gravity_load_to"),
        ("STR.RCS.SBC.COL", "STR.FND.SHL.FTG", "transfers_gravity_load_to"),
        ("STR.WSD.DIC.DIA", "STR.WSD.DIC.CDR", "transfers_lateral_load_to_collector"),
        ("ARC.BLD.STR.FOC", "STR.WSD.DIC.DPO", "requires_diaphragm_opening_coordination"),
        ("STR.FND.SHL.RTW", "CIV.DRN.CON.PDR", "requires_rear_drainage_or_pressure_relief"),
        ("ARC.TEC.JNT.MJC", "STR.SSS.CBP.MJT", "covers_structural_movement_joint"),
        ("CIV.MIS.UCC.SUC", "STR.FND.SHL.FTG", "constrains_foundation_layout_and_clearance"),
        ("COM.APP.FHA", "CIV.HDI.FCI.DFE", "sets_flood_elevation_applicability_basis"),
        ("CIV.HDI.FCI.DFE", "CIV.SDV.GRD.FFE", "constrains_finished_floor_elevation_interface"),
        ("CIV.SDV.GRD.TPS", "GEO.RSS.SLS", "informs_slope_stability_assessment"),
        ("GEO.RSS.SLS", "STR.FND.SHL.RTW", "constrains_retaining_wall_stability_basis"),
        ("CIV.MIS.UCC.UQL", "CIV.MIS.UCC.SUC", "qualifies_utility_conflict_evidence_strength"),
        ("CIV.MIS.UCC.TPH", "CIV.MIS.UCC.UQL", "verifies_utility_quality_level_by_exposure"),
        ("CIV.PAV.SBG", "CIV.PAV.PST", "supports_pavement_structure_performance"),
        ("CIV.SDV.ACC.CRG", "ARC.SPC.CIR.ASR", "constrains_accessible_route_transition_geometry"),
        ("CIV.DRN.CON.SMA", "OPS.AST.REG.CAR", "creates_civil_asset_record_for_handover"),
        ("ARC.SPC.CIR.ASR", "CIV.RDC.PED.ATI", "requires_public_way_crossing_tie_in_review"),
        ("CIV.RDC.PED.ATI", "CIV.DRN.CON.SRO", "requires_crossing_surface_runoff_control"),
        ("CIV.DRN.HYD", "CIV.HDI.CCD.CDI", "sets_culvert_hydrology_basis"),
        ("CIV.HDI.CCD.CDI", "GEO.HAZ.FLO", "requires_flood_and_scour_hazard_review"),
        ("CIV.PAV.PSI", "GEO.FOE.DSE", "sensitive_to_subgrade_settlement_variability"),
        ("STR.LOA.CBG", "STR.LOA.LAT.WND", "gates_wind_load_basis_before_application"),
        ("CIV.DRN.CON.CBI", "OPS.MNT.PMA", "requires_drainage_inlet_maintenance_plan"),
        ("COM.APP.AHJ", "STR.LOA.LAT.WND", "requires_adopted_wind_load_basis"),
        ("COM.APP.AHJ", "STR.LOA.LAT.SEI", "requires_adopted_seismic_load_basis"),
    ]
    for from_path, to_path, relation_type in checks:
        row = _edge(payload, from_path, to_path, relation_type)
        assert row["generation_method"] == GENERATION_METHOD
        assert row["direction"] == "from_to"
        assert 0 < row["weight"] <= 1
        assert 0 < row["confidence_score"] <= 1
        assert row["source_family_ids"]
        assert len(row["rationale"]) >= 30
        assert row["applicability_basis"] == "source_family_only_ahj_or_project_basis_required"
        assert row["jurisdiction_context"] == "source-family-mixed-ahj-required"
        assert row["design_basis_status"] == "no_project_numeric_criteria_admitted"


def test_acs_quality_guards_pass_for_introduced_content() -> None:
    source_payload = _load(SOURCE_RIGHTS)
    report = analyze_backbone_graph_quality(
        _load(FIXTURE),
        introduced_generation_method=GENERATION_METHOD,
        source_rights_payload=source_payload,
    )

    assert report["ok"] is True
    assert report["errors"] == []
    assert report["metrics"]["introduced_node_count"] >= 79
    assert report["metrics"]["introduced_relationship_count"] >= 143
    assert report["metrics"]["introduced_relationship_source_family_coverage"]["ratio"] == 1.0
    assert report["metrics"]["generic_relationship_count"] == 0
    assert report["metrics"]["orphan_node_count"] == 0
    assert report["metrics"]["self_loop_count"] == 0
    assert report["metrics"]["same_parent_duplicate_normalized_label_count"] == 0
    assert report["metrics"]["sample_duplicate_normalized_labels"]


def test_acs_quality_score_meets_loop_gate() -> None:
    report = score_architecture_civil_structural_quality(
        _load(FIXTURE),
        _load(SOURCE_RIGHTS),
        _load(READINESS),
    )

    assert report["ok"] is True
    assert report["quality_score"]["total"] >= 90
    assert min(report["quality_score"]["dimensions"].values()) >= 7.5
    assert all(result["ok"] for result in report["traversal_results"])
    assert report["metrics"]["missing_required_relation_types"] == []
    assert report["metrics"]["missing_required_resolver_cases"] == []


def test_source_registry_and_resolver_cases_include_acs_evidence() -> None:
    source_payload = enrich_source_rights_payload(_load(SOURCE_RIGHTS))
    source_ids = {row["source_id"] for row in source_payload["source_rights_registry"]}
    assert {
        "SRC-US-ACCESS-BOARD-ADA-PROWAG",
        "SRC-FHWA-HEC-22-URBAN-DRAINAGE",
        "SRC-NOAA-ATLAS-14-PRECIPITATION-FREQUENCY",
        "SRC-FHWA-GEOTECH-SUBSURFACE-INVESTIGATION",
        "SRC-ACI-318-STRUCTURAL-CONCRETE",
        "SRC-AISC-360-STRUCTURAL-STEEL",
        "SRC-NIBS-WBDG-BUILDING-ENVELOPE",
        "SRC-FHWA-ASCE-38-SUE-UTILITY-DATA",
        "SRC-ASCE-24-FLOOD-RESISTANT",
    } <= source_ids

    readiness_payload = enrich_readiness_fixture(_load(READINESS))
    case_ids = {row["case_id"] for row in readiness_payload["resolver_golden_cases"]}
    assert {f"RES-ACS-{index:03d}" for index in range(1, 19)} <= case_ids


def test_acs_enrichment_rejects_raw_source_layer_write_targets(tmp_path: Path) -> None:
    raw_backbone = tmp_path / "001_Raw-Source-Layer" / "admitted_backbone_nodes_l1_l2.json"
    source_rights = tmp_path / ".ai/03_plans/AEC-MEPFS-Backbone/registry-candidates/source-rights-registry.json"
    readiness = tmp_path / "scripts/tests/fixtures/aec_mepfs_backbone/valid_readiness_s2.json"
    raw_backbone.parent.mkdir(parents=True)
    source_rights.parent.mkdir(parents=True)
    readiness.parent.mkdir(parents=True)
    raw_backbone.write_text(FIXTURE.read_text(encoding="utf-8"), encoding="utf-8")
    source_rights.write_text(SOURCE_RIGHTS.read_text(encoding="utf-8"), encoding="utf-8")
    readiness.write_text(READINESS.read_text(encoding="utf-8"), encoding="utf-8")

    with pytest.raises(ValueError, match="immutable raw source custody layer"):
        apply_enrichment(
            backbone_path="001_Raw-Source-Layer/admitted_backbone_nodes_l1_l2.json",
            source_rights_path=".ai/03_plans/AEC-MEPFS-Backbone/registry-candidates/source-rights-registry.json",
            readiness_fixture_path="scripts/tests/fixtures/aec_mepfs_backbone/valid_readiness_s2.json",
            repo_root=tmp_path,
            run_id="RAW_TARGET_BLOCKED",
        )

    assert not (tmp_path / "006_System-Manifests/aec-mepfs-backbone/architecture-civil-structural-enrichment/RAW_TARGET_BLOCKED").exists()


def test_acs_quality_report_rejects_raw_source_output_path() -> None:
    with pytest.raises(ValueError, match="immutable raw source custody layer"):
        run_quality_score_report(
            FIXTURE,
            source_rights_path=SOURCE_RIGHTS,
            readiness_fixture_path=READINESS,
            run_id="RAW_OUTPUT_BLOCKED",
            output_path="001_Raw-Source-Layer/RAW_OUTPUT_BLOCKED/architecture-civil-structural-quality-report.json",
        )


def test_acs_quality_report_rejects_unexpected_output_filename() -> None:
    with pytest.raises(ValueError, match="output filename must be architecture-civil-structural-quality-report.json"):
        run_quality_score_report(
            FIXTURE,
            source_rights_path=SOURCE_RIGHTS,
            readiness_fixture_path=READINESS,
            run_id="BAD_FILENAME",
            output_path="006_System-Manifests/aec-mepfs-backbone/architecture-civil-structural-quality/BAD_FILENAME/not-quality.json",
        )
