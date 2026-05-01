from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

from vitruvius.kg.backbone_resolver_qa import run_resolver_qa_fixture
from vitruvius.kg.lea_ale_resolver_deepening import (
    GENERATION_METHOD,
    RAW_SOURCE_RIGHTS_CLASSIFICATION,
    SOURCE_REFERENCES,
    enrich_graph,
    enrich_resolver_fixture,
    enrich_source_rights_registry,
)

FIXTURE = (
    Path(__file__).parent
    / "fixtures"
    / "aec_mepfs_backbone"
    / "admitted_backbone_nodes_l1_l2.json"
)
RESOLVER_FIXTURE = (
    Path(__file__).parent
    / "fixtures"
    / "aec_mepfs_backbone"
    / "valid_readiness_s2.json"
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


def _resolver_payload() -> dict[str, Any]:
    return json.loads(RESOLVER_FIXTURE.read_text(encoding="utf-8"))


def _source_rights_payload() -> dict[str, Any]:
    return json.loads(SOURCE_RIGHTS_REGISTRY.read_text(encoding="utf-8"))


def _phase_nodes(payload: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        record
        for record in payload["records"]
        if record.get("generation_method") == GENERATION_METHOD
    ]


def _phase_relationships(payload: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        relationship
        for relationship in payload["relationships"]
        if relationship.get("generation_method") == GENERATION_METHOD
    ]


def test_lea_ale_resolver_deepening_is_idempotent_on_admitted_fixture() -> None:
    payload = _fixture_payload()

    enriched, report = enrich_graph(payload)

    assert report["ok"] is True
    assert report["added_node_count"] == 0
    assert report["added_relationship_count"] == 0
    assert report["improved_existing_node_count"] == 0
    assert report["aliases_added_or_preserved_on_new_and_improved_nodes"] == 0
    assert len(enriched["records"]) == len(payload["records"])
    assert len(enriched["relationships"]) == len(payload["relationships"])


def test_lea_ale_resolver_deepening_nodes_and_relationships_are_substantial() -> None:
    payload = _fixture_payload()
    records_by_id = {record["id"]: record for record in payload["records"]}
    records_by_path = {record["path_code"]: record for record in payload["records"]}
    phase_nodes = _phase_nodes(payload)
    phase_relationships = _phase_relationships(payload)

    assert len(phase_nodes) == 102
    assert Counter(record["lea_ale_category"] for record in phase_nodes) == {
        "source_reference": 10,
        "structural_concepts": 41,
        "utilities_building_systems": 51,
    }
    assert Counter(record["semantic_node_kind"] for record in phase_nodes) == {
        "lea_electrical_detail": 9,
        "lea_fire_vertical_ict_detail": 14,
        "lea_mechanical_detail": 10,
        "lea_plumbing_sanitary_detail": 9,
        "lea_structural_system_detail": 41,
        "lea_utilities_coordination_detail": 9,
        "standard_reference": 10,
    }
    assert len(phase_relationships) == 644
    assert Counter(relationship["predicate"] for relationship in phase_relationships) == {
        "applicable_in_jurisdiction": 6,
        "broader_than": 102,
        "conflicts_with": 2,
        "constrains": 73,
        "governs": 6,
        "has_facet": 16,
        "maps_to_external_standard": 144,
        "requires": 293,
        "supersedes": 2,
    }
    cross_domain = [
        relationship
        for relationship in phase_relationships
        if records_by_id[relationship["from_id"]]["path_code"].split(".")[0]
        != records_by_id[relationship["to_id"]]["path_code"].split(".")[0]
    ]
    utilities_relationships = [
        relationship
        for relationship in phase_relationships
        if records_by_id[relationship["from_id"]]["path_code"].startswith("ARC.BLD.SRV")
        or records_by_id[relationship["to_id"]]["path_code"].startswith("ARC.BLD.SRV")
    ]
    structural_relationships = [
        relationship
        for relationship in phase_relationships
        if records_by_id[relationship["from_id"]]["path_code"].startswith("ARC.BLD.STR")
        or records_by_id[relationship["to_id"]]["path_code"].startswith("ARC.BLD.STR")
    ]
    assert len(cross_domain) == 272
    assert len(utilities_relationships) == 410
    assert len(structural_relationships) == 138
    assert {
        "ARC.BLD.SRV.UCO",
        "ARC.BLD.SRV.SHA",
        "ARC.BLD.SRV.RIS",
        "ARC.BLD.SRV.RCP",
        "ARC.BLD.SRV.IAQ",
        "ARC.BLD.SRV.FPR",
        "ARC.BLD.SRV.FAP",
        "ARC.BLD.SRV.ICT",
        "ARC.BLD.STR.SCA",
        "ARC.BLD.STR.CGD",
        "ARC.BLD.STR.FDS",
        "ARC.BLD.STR.NCC",
        "COM.STD.PHL.BFM",
        "COM.STD.PHL.NCD",
        "COM.STD.PHL.DGB",
    } <= set(records_by_path)
    assert {
        "COM.STD.PHL.RUM",
        "COM.STD.PHL.RHE",
        "COM.STD.PHL.RTR",
        "COM.STD.PHL.RSB",
        "COM.STD.PHL.RFA",
        "COM.STD.PHL.RTA",
    }.isdisjoint(records_by_path)
    assert all(
        len(segment) == 3
        for record in phase_nodes
        for segment in str(record["path_code"]).split(".")
    )
    for record in phase_nodes:
        assert record["review_status"] == "steward_admitted"
        assert record["source_family_ids"]
        assert "no protected source payload" in record["provenance_note"]
    for relationship in phase_relationships:
        assert relationship["governed"] is True
        assert relationship["source_family_ids"]
        assert "no protected source payload" in relationship["provenance_note"]


def test_lea_ale_deepening_relationships_support_query_paths() -> None:
    payload = _fixture_payload()
    records_by_id = {record["id"]: record for record in payload["records"]}
    triples = {
        (
            records_by_id[relationship["from_id"]]["path_code"],
            relationship["predicate"],
            records_by_id[relationship["to_id"]]["path_code"],
        )
        for relationship in payload["relationships"]
    }

    assert {
        ("LAW.AAP", "governs", "LAW.AAP.SIS"),
        ("LAW.AAP.SIS", "requires", "LAW.AAP.SAP.ADO"),
        ("LAW.PNB.PIE.PRV", "requires", "LAW.AAP.SAP.ADO"),
        ("LAW.PNB.OUC.OCL", "constrains", "LAW.PFC.OFS.OCL"),
        ("LAW.PFC.FSI.FSE", "requires", "LAW.PNB.PIE.BPE"),
        ("LAW.PFC.FSI.FIC", "requires", "LAW.PNB.PIE.OPM"),
        ("LAW.PAL.ACR.ARS", "requires", "ARC.INT.PAC.ISP"),
        ("LAW.WCW.DRE.FLD", "constrains", "ARC.BLD.SRV.STD"),
        ("LAW.SCP.MPF.TOI", "requires", "ARC.BLD.SRV.PFP"),
        ("ARC.HIS.SEA.BKS", "has_facet", "ARC.TAC.NVS.XVN"),
        ("URB.LUZ.CLU.LCC", "requires", "LAW.ZON"),
        ("ARC.MAT.DUR", "requires", "ARC.BLD.SRV.STD"),
        ("ARC.BLD.STR.CGD", "constrains", "ARC.INT.PAC.ISP"),
        ("ARC.BLD.STR.NCC", "constrains", "ARC.BLD.SRV.PLC"),
        ("ARC.BLD.SRV.RCP", "requires", "ARC.BLD.SRV.FAP"),
        ("ARC.BLD.SRV.ERP", "requires", "ARC.BLD.SRV.FPR"),
        ("ARC.BLD.SRV.SEC", "requires", "ARC.BLD.SRV.ICT"),
        ("ARC.BLD.STR.SGL", "requires", "ARC.BLD.STR.CGD"),
        ("ARC.BLD.STR.FDS", "has_facet", "ARC.BLD.STR.PIF"),
        ("COM.STD.PHL.NIR", "supersedes", "COM.STD.PHL.NBC"),
    } <= triples


def test_lea_ale_resolver_fixture_has_golden_cases_and_safety_cases(tmp_path: Path) -> None:
    graph_payload = _fixture_payload()
    resolver_payload = _resolver_payload()

    enriched, report = enrich_resolver_fixture(resolver_payload, graph_payload)

    assert report["ok"] is True
    assert report["added_resolver_golden_case_count"] == 0
    assert len(enriched["resolver_golden_cases"]) == 117
    lea_cases = [case for case in enriched["resolver_golden_cases"] if case["case_id"].startswith("LEA-RES-")]
    assert len(lea_cases) == 45
    assert Counter(case["expected_result_type"] for case in enriched["resolver_golden_cases"]) == {
        "single_value": 54,
        "composed": 57,
        "conflict": 3,
        "none": 3,
    }
    assert {case["case_id"] for case in lea_cases} >= {
        "LEA-RES-001",
        "LEA-RES-011",
        "LEA-RES-016",
        "LEA-RES-021",
        "LEA-RES-024",
        "LEA-RES-030",
        "LEA-RES-042",
        "LEA-RES-044",
        "LEA-RES-045",
    }
    for case in lea_cases:
        assert case["query"]["trace_requested"] is True
        assert case["trace_safe_rationale"].startswith("Metadata-only LEA/ALE")
        assert "protected source text" in case["trace_safe_rationale"]
        assert case["source_evidence"]
        if case["expected_result_type"] != "none":
            assert case["expected_node_refs"]
    qa_report = run_resolver_qa_fixture(
        RESOLVER_FIXTURE.resolve(),
        repo_root=tmp_path,
        run_id="LEA_TEST_RUN",
    )
    assert qa_report["ok"] is True
    assert qa_report["summary"]["cases_total"] == 117
    assert qa_report["summary"]["cases_passed"] == 117


def test_lea_ale_source_rights_deepening_is_metadata_only_and_idempotent() -> None:
    payload = _source_rights_payload()

    enriched, report = enrich_source_rights_registry(payload)

    assert report["ok"] is True
    assert report["added_source_reference_count"] == 0
    assert len(enriched["source_rights_registry"]) == len(payload["source_rights_registry"])
    assert len(SOURCE_REFERENCES) == 16
    assert len(RAW_SOURCE_RIGHTS_CLASSIFICATION) == 6
    rows_by_id = {row["source_id"]: row for row in enriched["source_rights_registry"]}
    assert {reference["source_id"] for reference in SOURCE_REFERENCES} <= set(rows_by_id)
    for reference in SOURCE_REFERENCES:
        row = rows_by_id[reference["source_id"]]
        assert row["source_rights_class"] == "reference_only"
        assert row["clearance_state"] in {"planning_reference_only", "clearance_required"}
        assert "metadata" in row["declared_use_boundary"].lower()
        assert all(
            blocked in row["declared_use_boundary"].lower()
            for blocked in ("no", "questions", "answer", "tables", "figures", "diagrams")
        )
    for raw in RAW_SOURCE_RIGHTS_CLASSIFICATION:
        row = rows_by_id[raw["source_id"]]
        assert row["clearance_state"] == "clearance_required"
        assert "raw-source custody metadata only" in row["declared_use_boundary"]
        assert "no PDF/spreadsheet payload" in row["declared_use_boundary"]
        assert "not be ingested" in row["blocking_notes"]
