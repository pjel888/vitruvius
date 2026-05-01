from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

from vitruvius.kg.architecture_interconnectivity_enrichment import (
    GENERATION_METHOD,
    SOURCE_REFERENCES,
    enrich_graph,
    enrich_resolver_fixture,
    enrich_source_rights_registry,
)
from vitruvius.kg.backbone_resolver_qa import run_resolver_qa_fixture

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
BAD_LEARNER_LABEL_PATTERNS = (
    "local raw-source filename metadata",
    "raw-source filename metadata",
    "metadata-only source-family reference",
    "metadata-only source",
    "source-family reference",
    "protected payload",
    "reviewer candidate",
    "unknown/private",
    "local file",
    "registry row",
    "planning_reference_only",
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


def _triples(payload: dict[str, Any]) -> set[tuple[str, str, str]]:
    records_by_id = {record["id"]: record for record in payload["records"]}
    return {
        (
            records_by_id[relationship["from_id"]]["path_code"],
            relationship["predicate"],
            records_by_id[relationship["to_id"]]["path_code"],
        )
        for relationship in payload["relationships"]
    }


def test_architecture_interconnectivity_is_idempotent_on_admitted_fixture() -> None:
    payload = _fixture_payload()

    enriched, report = enrich_graph(payload)

    assert report["ok"] is True
    assert report["added_node_count"] == 0
    assert report["added_relationship_count"] == 0
    assert report["improved_existing_node_count"] == 0
    assert len(enriched["records"]) == len(payload["records"])
    assert len(enriched["relationships"]) == len(payload["relationships"])


def test_architecture_interconnectivity_material_people_work_counts_are_substantial() -> None:
    payload = _fixture_payload()
    phase_nodes = _phase_nodes(payload)
    phase_relationships = _phase_relationships(payload)

    assert len(phase_nodes) == 378
    assert len(phase_relationships) == 1668
    assert Counter(record["interconnectivity_category"] for record in phase_nodes) == {
        "history_material_bridge": 1,
        "materials_taxonomy": 115,
        "people_works_materials": 136,
        "people_nationality": 25,
        "laws_standards_classification": 9,
        "project_evidence_paths": 92,
    }
    assert Counter(relationship["predicate"] for relationship in phase_relationships) == {
        "broader_than": 378,
        "constrains": 12,
        "has_facet": 1270,
        "requires": 8,
    }
    assert sum(1 for record in phase_nodes if record["path_code"].startswith("MAT")) == 115
    assert sum(1 for record in phase_nodes if record["path_code"].startswith("FIG.ARD.CAA")) == 55
    assert sum(1 for record in phase_nodes if record["path_code"].startswith("FIG.ETS.STE")) == 25
    assert sum(1 for record in phase_nodes if record["path_code"].startswith("FIG.PTE.NAT")) == 25
    assert sum(1 for record in phase_nodes if record["path_code"].startswith(("LAW.JUR", "COM.STD.AIA", "COM.STD.RIB", "COM.STD.IBS"))) == 9
    assert sum(1 for record in phase_nodes if record.get("semantic_node_kind") == "work_project_anchor") == 128
    assert all(record["visibility"] == "learner_facing" for record in phase_nodes)
    assert all(record["source_family_ids"] for record in phase_nodes)
    assert all("no protected source payload" in record["provenance_note"] for record in phase_nodes)
    assert all(relationship["governed"] is True for relationship in phase_relationships)
    assert all(relationship["source_family_ids"] for relationship in phase_relationships)
    assert all(
        "no protected source payload" in relationship["provenance_note"]
        for relationship in phase_relationships
    )


def test_architecture_interconnectivity_key_paths_are_project_anchored() -> None:
    payload = _fixture_payload()
    records_by_path = {record["path_code"]: record for record in payload["records"]}
    triples = _triples(payload)

    assert {
        "MAT.PRF",
        "MAT.ASM",
        "MAT.CMA.CEM.EXP",
        "MAT.CMA.CEM.CIP",
        "MAT.CMA.CEM.CHB",
        "MAT.TBB.BAS.BCM",
        "MAT.TBB.BAS.NIP",
        "MAT.TBB.BAS.CAP",
        "MAT.MEM.RME.WPM",
        "MAT.PRF.THE.REF",
        "FIG.AWD.PRI.PZK",
        "FIG.ARD.CAA.HAD",
        "FIG.ARD.CAA.AND",
        "FIG.ETS.STE.CAL",
        "FIG.WRK.BUI.MAX",
        "FIG.WRK.BUI.CHL",
        "FIG.WRK.BUI.MOS",
        "FIG.WRK.BUI.AQA",
        "FIG.WRK.BUI.DDP",
        "FIG.WRK.BUI.SYD",
        "FIG.WRK.BUI.CHS",
        "FIG.WRK.BUI.FEU",
        "MAT.STM.STS.CBL",
        "MAT.GLA.STG",
        "ARC.BLD.STR.FBU",
        "ARC.BLD.STR.RBV",
        "STR.SSS.MBF.DGF",
        "STR.RCS.SWC.BTC",
        "FIG.PTE.NAT.JPN",
        "FIG.PTE.NAT.GBR",
        "FIG.PTE.NAT.PHL",
        "LAW.JUR.INT",
        "LAW.JUR.PHL",
        "LAW.JUR.LOC",
        "COM.STD.AIA",
        "COM.STD.RIB",
        "COM.STD.IBS",
    } <= set(records_by_path)
    assert {
        ("FIG.AWD.PRI.PZK", "has_facet", "FIG.ARD.CAA.HAD"),
        ("FIG.ARD.CAA.HAD", "has_facet", "FIG.PTE.ROL.ARC"),
        ("FIG.ARD.CAA.HAD", "has_facet", "FIG.PTE.ROL.LAU"),
        ("FIG.ARD.CAA.HAD", "has_facet", "FIG.WRK.BUI.MAX"),
        ("FIG.WRK.BUI.MAX", "has_facet", "MAT.CMA.CEM.CIP"),
        ("FIG.ARD.CAA.AND", "has_facet", "FIG.WRK.BUI.CHL"),
        ("FIG.WRK.BUI.CHL", "has_facet", "MAT.CMA.CEM.EXP"),
        ("FIG.ARD.CAA.HAD", "has_facet", "FIG.WRK.BUI.AQA"),
        ("FIG.WRK.BUI.AQA", "has_facet", "ARC.BLD.STR.LSS"),
        ("FIG.WRK.BUI.DDP", "has_facet", "MAT.STM.MEC.ALP"),
        ("FIG.ARD.CAA.UTZ", "has_facet", "FIG.WRK.BUI.SYD"),
        ("FIG.ETS.STE.ARU", "has_facet", "FIG.WRK.BUI.SYD"),
        ("FIG.WRK.BUI.SYD", "has_facet", "ARC.BLD.STR.SHL"),
        ("FIG.ARD.CAA.LOC", "has_facet", "FIG.WRK.BUI.CHS"),
        ("FIG.WRK.BUI.CHS", "has_facet", "ARC.BLD.STR.SHL"),
        ("FIG.ARD.CAA.ANT", "has_facet", "FIG.WRK.BUI.FEU"),
        ("FIG.WRK.BUI.FEU", "has_facet", "ARC.HIS.SEA.ADP"),
        ("FIG.ETS.STE.CAL", "has_facet", "FIG.PTE.ROL.AEN"),
        ("FIG.ETS.STE.CAL", "has_facet", "CIV.BRG"),
        ("FIG.ARD.CAA.FOT", "has_facet", "ARC.BLD.STR.TNS"),
        ("ARC.HIS.SEA.PVA", "has_facet", "MAT.TBB.BAS.BCM"),
        ("ARC.HIS.SEA.PVA", "has_facet", "MAT.TBB.BAS.NIP"),
        ("ARC.HIS.SEA.PVA", "has_facet", "MAT.TBB.BAS.CAP"),
        ("ARC.TAC", "has_facet", "MAT.TBB.BAS.BCM"),
        ("MAT.FIP.FLF.CER", "has_facet", "MAT.ASM.WET"),
        ("MAT.MEM.RME.WPM", "has_facet", "MAT.ASM.ROF"),
        ("MAT.CMA.CEM.CIP", "requires", "CON.TMP.FOR"),
        ("ARC.MAT.CON.RCC", "has_facet", "ARC.BLD.STR.SLB"),
        ("MAT.GLA.CWG", "has_facet", "MAT.ASM.CUR"),
        ("MAT.GLA.CWG", "has_facet", "MAT.PRF.THE.REF"),
        ("FIG.ARD.CAA.AND", "has_facet", "FIG.PTE.NAT.JPN"),
        ("FIG.ARD.CAA.HAD", "has_facet", "FIG.PTE.NAT.GBR"),
        ("FIG.ETS.STE.CAL", "has_facet", "FIG.PTE.NAT.ESP"),
        ("FIG.PTE.ROL.AEN", "has_facet", "FIG.ETS.STE.CAL"),
        ("FIG.PTE.ROL.AEN", "has_facet", "FIG.ARD.CAA.FOT"),
        ("COM.STD.AIA", "has_facet", "LAW.JUR.USA"),
        ("COM.STD.RIB", "has_facet", "LAW.JUR.GBR"),
        ("COM.STD.IBS", "has_facet", "LAW.JUR.USA"),
        ("LAW.LGZ", "has_facet", "LAW.JUR.LOC"),
    } <= triples


def test_architecture_interconnectivity_blocks_forced_or_process_heavy_relationships() -> None:
    payload = _fixture_payload()
    records_by_id = {record["id"]: record for record in payload["records"]}
    phase_relationships = _phase_relationships(payload)
    direct_person_to_material = []
    for relationship in phase_relationships:
        from_path = records_by_id[relationship["from_id"]]["path_code"]
        to_path = records_by_id[relationship["to_id"]]["path_code"]
        if from_path.startswith(("FIG.ARD", "FIG.ETS")) and to_path.startswith(("MAT", "ARC.MAT")):
            direct_person_to_material.append((from_path, relationship["predicate"], to_path))

    assert direct_person_to_material == []
    assert all(relationship["predicate"] != "related_to" for relationship in phase_relationships)
    for record in payload["records"]:
        if record.get("visibility") == "internal_provenance_only":
            continue
        label = str(record.get("label", "")).lower()
        assert not any(pattern in label for pattern in BAD_LEARNER_LABEL_PATTERNS), record[
            "path_code"
        ]


def test_architecture_interconnectivity_philippine_evidence_paths_are_work_anchored() -> None:
    payload = _fixture_payload()
    records_by_path = {record["path_code"]: record for record in payload["records"]}
    triples = _triples(payload)

    assert {
        "FIG.ARD.CAA.ARE",
        "FIG.ARD.CAA.SAN",
        "FIG.ARD.CAA.MAN",
        "FIG.ARD.CAA.ZAR",
        "FIG.WRK.BUI.MTH",
        "FIG.WRK.BUI.SDC",
        "FIG.WRK.BUI.BHT",
        "FIG.WRK.BUI.BKB",
        "FIG.WRK.BUI.BNB",
        "FIG.PTE.ROL.NAA",
        "FIG.PTE.ROL.LAR",
    } <= set(records_by_path)
    assert {
        ("FIG.ARD.CAA.ARE", "has_facet", "FIG.WRK.BUI.MTH"),
        ("FIG.WRK.BUI.MTH", "has_facet", "ARC.HIS.SEA.ADP"),
        ("FIG.WRK.BUI.MTH", "has_facet", "MAT.GLA.STG"),
        ("FIG.ARD.CAA.SAN", "has_facet", "FIG.PTE.ROL.LAR"),
        ("FIG.ARD.CAA.SAN", "has_facet", "FIG.WRK.BUI.MCC"),
        ("FIG.WRK.BUI.MCC", "has_facet", "ARC.SIT.LAN"),
        ("FIG.ARD.CAA.MAN", "has_facet", "FIG.WRK.BUI.BHT"),
        ("FIG.WRK.BUI.BHT", "has_facet", "MAT.TBB.BAS.BCM"),
        ("FIG.WRK.BUI.BHT", "has_facet", "ARC.TAC.NVS"),
        ("FIG.ARD.CAA.ZAR", "has_facet", "FIG.WRK.BUI.SDC"),
        ("FIG.WRK.BUI.SDC", "has_facet", "ARC.MAT.CON.RCC"),
        ("FIG.WRK.BUI.BKB", "has_facet", "MAT.TBB.BAS.NIP"),
        ("FIG.WRK.BUI.BNB", "has_facet", "MAT.TBB.BAS.CAP"),
        ("FIG.WRK.BUI.TRG", "has_facet", "MAT.TBB.DIL.HDW"),
        ("FIG.WRK.BUI.IVT", "has_facet", "MAT.MST.NAS.LIM"),
        ("FIG.WRK.BUI.IFB", "has_facet", "ARC.CHC.CLC"),
    } <= triples

    for from_path, _, to_path in triples:
        if from_path.startswith(("FIG.ARD", "FIG.ETS")):
            assert not to_path.startswith(("MAT", "ARC.MAT")), (from_path, to_path)


def test_architecture_interconnectivity_resolver_cases_are_present_and_pass(tmp_path: Path) -> None:
    graph_payload = _fixture_payload()
    resolver_payload = _resolver_payload()

    enriched, report = enrich_resolver_fixture(resolver_payload, graph_payload)

    assert report["ok"] is True
    assert report["added_resolver_golden_case_count"] == 0
    assert len(enriched["resolver_golden_cases"]) == 117
    cases = [
        case
        for case in enriched["resolver_golden_cases"]
        if case["case_id"].startswith("ARCH-INT-")
    ]
    assert len(cases) == 65
    assert Counter(case["expected_result_type"] for case in cases) == {
        "single_value": 14,
        "composed": 51,
    }
    required = {
        "ARCH-INT-001",
        "ARCH-INT-003",
        "ARCH-INT-005",
        "ARCH-INT-008",
        "ARCH-INT-011",
        "ARCH-INT-016",
        "ARCH-INT-020",
        "ARCH-INT-021",
        "ARCH-INT-027",
        "ARCH-INT-033",
        "ARCH-INT-041",
        "ARCH-INT-045",
        "ARCH-INT-046",
        "ARCH-INT-049",
        "ARCH-INT-053",
        "ARCH-INT-065",
    }
    assert required <= {case["case_id"] for case in cases}
    for case in cases:
        assert case["query"]["trace_requested"] is True
        assert case["expected_node_refs"]
        assert case["source_evidence"]
        assert "protected source text" in case["trace_safe_rationale"]

    qa_report = run_resolver_qa_fixture(
        RESOLVER_FIXTURE.resolve(),
        repo_root=tmp_path,
        run_id="ARCH_INT_TEST_RUN",
    )
    assert qa_report["ok"] is True
    assert qa_report["summary"]["cases_failed"] == 0
    assert qa_report["summary"]["cases_passed"] == 117
    assert qa_report["summary"]["cases_total"] == 117


def test_architecture_interconnectivity_source_rights_rows_are_metadata_only() -> None:
    payload = _source_rights_payload()

    enriched, report = enrich_source_rights_registry(payload)

    assert report["ok"] is True
    assert report["added_source_reference_count"] == 0
    assert len(enriched["source_rights_registry"]) == 106
    rows_by_id = {row["source_id"]: row for row in enriched["source_rights_registry"]}
    assert {reference["source_id"] for reference in SOURCE_REFERENCES} <= set(rows_by_id)
    for reference in SOURCE_REFERENCES:
        row = rows_by_id[reference["source_id"]]
        assert row["source_rights_class"] in {"reference_only", "metadata_crosswalk"}
        assert row["clearance_state"] in {
            "planning_reference_only",
            "metadata_crosswalk_planned",
        }
        assert "metadata" in row["declared_use_boundary"].lower()
        assert "no" in row["declared_use_boundary"].lower()
        assert "protected" in row["declared_use_boundary"].lower()
        assert "payload" in row["declared_use_boundary"].lower()
        assert "ingested" in row["declared_use_boundary"].lower()
