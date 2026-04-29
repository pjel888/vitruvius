from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

from vitruvius.kg.lea_ale_semantic_enrichment import (
    GENERATION_METHOD,
    RAW_SOURCE_RIGHTS_CLASSIFICATION,
    SOURCE_REFERENCES,
    enrich,
    enrich_source_rights_registry,
)

FIXTURE = (
    Path(__file__).parent
    / "fixtures"
    / "aec_mepfs_backbone"
    / "admitted_backbone_nodes_l1_l2.json"
)
SOURCE_RIGHTS_REGISTRY = (
    Path(__file__).parents[2]
    / ".ai"
    / "03_plans"
    / "AEC-MEPFS-Backbone"
    / "registry-candidates"
    / "source-rights-registry.json"
)


def _fixture_payload() -> dict[str, Any]:
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def _source_rights_payload() -> dict[str, Any]:
    return json.loads(SOURCE_RIGHTS_REGISTRY.read_text(encoding="utf-8"))


def _lea_records(payload: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        record
        for record in payload["records"]
        if record.get("generation_method") == GENERATION_METHOD
    ]


def _lea_relationships(payload: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        relationship
        for relationship in payload["relationships"]
        if relationship.get("generation_method") == GENERATION_METHOD
    ]


def test_lea_ale_enrichment_is_idempotent_on_admitted_fixture() -> None:
    payload = _fixture_payload()

    enriched, report = enrich(payload)

    assert report["ok"] is True
    assert report["added_node_count"] == 0
    assert report["added_relationship_count"] == 0
    assert report["improved_existing_node_count"] == 0
    assert report["aliases_added_or_preserved_on_new_and_improved_nodes"] == 0
    assert report["rights_safety"] == {
        "protected_source_payloads_ingested": False,
        "source_payload_mode": "labels_metadata_aliases_original_summaries_and_source_family_references_only",
        "exam_questions_or_answer_keys_ingested": False,
        "reviewer_text_ingested": False,
        "protected_code_tables_clauses_figures_or_diagrams_ingested": False,
        "neo4j_mutation": False,
        "kg_rebuild_reload_reset": False,
        "api_or_explorer_runtime_behavior_changed": False,
        "codex_spark_used_for_research_or_synthesis": False,
        "kimi_used_for_advisory_synthesis": True,
    }
    assert len(enriched["records"]) == len(payload["records"])
    assert len(enriched["relationships"]) == len(payload["relationships"])


def test_lea_ale_fixture_contains_subject_domain_expansion_not_exam_area_flattening() -> None:
    payload = _fixture_payload()
    records_by_id = {record["id"]: record for record in payload["records"]}
    lea_records = _lea_records(payload)
    lea_relationships = _lea_relationships(payload)

    assert len(lea_records) == 236
    assert Counter(record["semantic_node_kind"] for record in lea_records) == {
        "lea_arch_work": 6,
        "lea_contracts_admin": 10,
        "lea_exam_meta": 12,
        "lea_fil_architect": 6,
        "lea_history_ph_architecture": 12,
        "lea_history_world_architecture": 9,
        "lea_interiors": 6,
        "lea_materials_methods": 13,
        "lea_ph_accessibility": 12,
        "lea_ph_building_code": 16,
        "lea_ph_fire_code": 29,
        "lea_ph_law_practice": 10,
        "lea_ph_sanitation_code": 6,
        "lea_ph_water_code": 6,
        "lea_site_planning": 10,
        "lea_structural_concepts": 8,
        "lea_theory_design_principle": 12,
        "lea_tropical_design": 8,
        "lea_urban_planning": 8,
        "lea_utilities_systems": 8,
        "standard_family": 1,
        "standard_reference": 28,
    }
    assert Counter(record["lea_ale_category"] for record in lea_records) == {
        "accessibility_universal_design": 12,
        "fire_life_safety": 29,
        "history_theory_philippine_architecture": 45,
        "interiors_human_factors": 6,
        "lea_exam_meta": 12,
        "materials_construction_specifications": 13,
        "philippine_law_code": 26,
        "professional_practice_contracts": 10,
        "site_planning_urban_design": 18,
        "source_reference": 29,
        "structural_utilities_systems": 16,
        "sustainability_climate_resilience": 8,
        "water_sanitation_public_health": 12,
    }
    assert len(lea_relationships) == 1193
    assert Counter(relationship["predicate"] for relationship in lea_relationships) == {
        "broader_than": 236,
        "constrains": 85,
        "governs": 90,
        "has_facet": 238,
        "maps_to_external_standard": 465,
        "part_of": 29,
        "requires": 50,
    }
    cross_domain = [
        relationship
        for relationship in lea_relationships
        if records_by_id[relationship["from_id"]]["path_code"].split(".")[0]
        != records_by_id[relationship["to_id"]]["path_code"].split(".")[0]
    ]
    assert len(cross_domain) == 799

    path_codes = {record["path_code"] for record in lea_records}
    assert {
        "ARC.REG.PHL.ALE",
        "ARC.REG.PHL.BLE",
        "ARC.REG.PHL.TOS",
        "ARC.HIS.SEA.TRG",
        "ARC.HIS.SEA.IVT",
        "FIG.ARD.CAA.LOC",
        "ARC.THE.DPR.ANT",
        "ARC.SIT.SAN.PRG",
        "URB.LUZ.CLU.LCC",
        "LAW.AAP.SAP.ADO",
        "LAW.PNB.PIE.BPE",
        "LAW.PFC.FSI.FSE",
        "LAW.PFC.OFS.EGR",
        "LAW.PAL.ACR.ARS",
        "LAW.WCW.DRE.WAE",
        "LAW.SCP.MPF.TOI",
        "ARC.MAT.CON.RCC",
        "ARC.BLD.STR.LDP",
        "ARC.BLD.SRV.HVC",
        "ARC.INT.PAC.IEQ",
        "CON.DMC.DBB.RFI",
        "COM.STD.PHL.RAA",
        "COM.STD.PHL.NBC",
        "COM.STD.PHL.RBR",
    } <= path_codes
    assert all(
        len(segment) == 3
        for record in lea_records
        for segment in str(record["path_code"]).split(".")
    )
    blocked_phrases = (
        "Advanced Topic",
        "Miscellaneous",
        "General Concepts",
        "TBD",
        "Concept Anchor",
        "Rule Context",
    )
    assert not [
        record["path_code"]
        for record in lea_records
        if any(phrase in record["label"] for phrase in blocked_phrases)
    ]
    for record in lea_records:
        assert record["review_status"] == "steward_admitted"
        assert record["confidence"] == "high"
        assert record["source_family_ids"]
        assert "no protected source payload" in record["provenance_note"]
    for relationship in lea_relationships:
        assert relationship["governed"] is True
        assert relationship["source_family_ids"]
        assert "no protected source payload" in relationship["provenance_note"]


def test_lea_ale_relationships_answer_practical_philippine_architecture_questions() -> None:
    payload = _fixture_payload()
    records_by_id = {record["id"]: record for record in payload["records"]}
    records_by_path = {record["path_code"]: record for record in payload["records"]}
    triples = {
        (
            records_by_id[relationship["from_id"]]["path_code"],
            relationship["predicate"],
            records_by_id[relationship["to_id"]]["path_code"],
        )
        for relationship in _lea_relationships(payload)
    }

    expected_triples = {
        ("LAW.PNB.PIE.BPE", "requires", "LAW.AAP.SAP.ADO"),
        ("LAW.PNB.PIE.OPM", "requires", "LAW.PFC.FSI.FIC"),
        ("LAW.PFC.EPE.ASP", "requires", "ARC.BLD.SRV.PWS"),
        ("LAW.PFC.EPE.SMC", "requires", "ARC.BLD.SRV.HVC"),
        ("LAW.PAL.ACR.ATO", "requires", "ARC.BLD.SRV.SDR"),
        ("LAW.WCW.DRE.WAE", "constrains", "ARC.SIT.SAN.DRN"),
        ("URB.LUZ.CLU.LCC", "requires", "LAW.PNB.PIE.BPE"),
        ("ARC.HIS.SEA.BKS", "has_facet", "ARC.TAC.NVS.XVN"),
        ("FIG.ARD.CAA.LOC", "has_facet", "FIG.WRK.BUI.CCP"),
        ("ARC.BLD.STR.SGL", "constrains", "ARC.SIT.SAN.BUB"),
        ("ARC.MAT.FIN.CEF", "requires", "LAW.PFC.EPE.ASP"),
        ("CON.DMC.DBB.ASB", "requires", "OPS.PRM"),
    }
    assert expected_triples <= triples

    improved_aliases = {
        "ARC.REG.PHL": "BLEA",
        "LAW.AAP": "Architecture Act",
        "LAW.PNB": "NBCP",
        "LAW.PFC": "FCP",
        "LAW.PAL": "BP 344",
        "URB.LUZ.CLU": "CLUP",
        "ARC.TAC": "Philippine climate design",
        "OPS.AST.AIM": "digital handover",
    }
    for path_code, alias in improved_aliases.items():
        assert alias in records_by_path[path_code].get("aliases", [])
        assert records_by_path[path_code].get("source_family_ids")


def test_lea_ale_source_rights_registry_is_idempotent_and_metadata_only() -> None:
    payload = _source_rights_payload()

    enriched, report = enrich_source_rights_registry(payload)

    assert report["ok"] is True
    assert report["added_source_reference_count"] == 0
    assert len(enriched["source_rights_registry"]) == len(payload["source_rights_registry"])
    source_ids = {row["source_id"] for row in enriched["source_rights_registry"]}
    assert {reference["source_id"] for reference in SOURCE_REFERENCES} <= source_ids
    rows_by_id = {row["source_id"]: row for row in enriched["source_rights_registry"]}
    assert len(SOURCE_REFERENCES) == 28
    assert len(RAW_SOURCE_RIGHTS_CLASSIFICATION) == 3
    for source_id in {reference["source_id"] for reference in SOURCE_REFERENCES}:
        row = rows_by_id[source_id]
        assert "metadata" in row["declared_use_boundary"] or "metadata" in row["intended_vitruvius_use"]
        assert "no" in row["declared_use_boundary"].lower()
        assert row["clearance_state"] in {
            "planning_reference_only",
            "clearance_required",
        }
        assert row["source_rights_class"] == "reference_only"
    for raw in RAW_SOURCE_RIGHTS_CLASSIFICATION:
        row = rows_by_id[raw["source_id"]]
        assert row["clearance_state"] == "clearance_required"
        assert "no PDF/spreadsheet payload" in row["declared_use_boundary"]
