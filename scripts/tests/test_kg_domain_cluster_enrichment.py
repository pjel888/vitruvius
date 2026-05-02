from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from vitruvius.kg.backbone_graph_quality import analyze_backbone_graph_quality
from vitruvius.kg.domain_cluster_enrichment import (
    GENERATION_METHOD,
    enrich_backbone_payload,
    enrich_readiness_fixture,
    enrich_source_rights_payload,
    summarize_delta,
)


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


def test_domain_cluster_enrichment_is_idempotent_on_current_fixture() -> None:
    payload = _load(FIXTURE)

    enriched = enrich_backbone_payload(payload)
    delta = summarize_delta(payload, enriched)

    assert delta["new_node_count"] == 0
    assert delta["new_relationship_count"] == 0
    assert delta["domain_cluster_relationship_count"] >= 115
    assert delta["domain_cluster_hierarchy_relationship_count"] >= 59


def test_domain_cluster_relationships_support_cross_discipline_reasoning() -> None:
    payload = _load(FIXTURE)

    checks = [
        ("COM.OCC.OLO", "MEC.IEQ.VER", "drives_ventilation_demand"),
        ("MEC.AHD.AHU", "MEC.AHD.DUD.SAD", "supplies_air_to"),
        ("MEC.AHD.DTD.SDF", "ARC.SPC.OCP", "serves_space"),
        ("FLS.CMP.PEN.FST", "FLS.CMP.PEN.PIP", "protects_penetration"),
        ("FLS.SCC.FID.FDA", "FLS.CMP.PEN.DUP", "protects_duct_opening"),
        ("ELE.ESP.GTS.ATS", "FLS.FPR.FPU.CTR", "requires_emergency_power"),
        ("PLS.PFE.FIS.PFX", "PLS.SDS.DRS.SDR", "drains_to"),
        ("PLS.PFE.FIS.PFX", "PLS.SAN.TRA.FXT", "requires_trap"),
        ("ARC.BLD.SRV.MPR", "ARC.BLD.SRV.MAZ", "requires_access_for"),
        ("SMS.BUA.ATL.ALM", "OPS.FAC.WOR.CWO", "triggers_work_order"),
        ("FIG.WRK.BUI.SYD", "FIG.ARD.CAA.UTZ", "designed_by"),
    ]
    for from_path, to_path, relation_type in checks:
        row = _edge(payload, from_path, to_path, relation_type)
        assert row["generation_method"] == GENERATION_METHOD
        assert row["direction"] == "from_to"
        assert 0 < row["weight"] <= 1
        assert 0 < row["confidence_score"] <= 1
        assert row["source_family_ids"]
        assert len(row["rationale"]) >= 30


def test_domain_cluster_quality_guard_passes_for_introduced_relationships() -> None:
    report = analyze_backbone_graph_quality(
        _load(FIXTURE),
        introduced_generation_method=GENERATION_METHOD,
    )

    assert report["ok"] is True
    assert report["errors"] == []
    assert report["metrics"]["introduced_node_count"] >= 59
    assert report["metrics"]["introduced_relationship_count"] >= 115
    assert report["metrics"]["generic_relationship_count"] == 0
    assert report["metrics"]["orphan_node_count"] == 0


def test_source_registry_and_resolver_cases_include_domain_cluster_evidence() -> None:
    source_payload = enrich_source_rights_payload(_load(SOURCE_RIGHTS))
    source_ids = {row["source_id"] for row in source_payload["source_rights_registry"]}
    assert {
        "SRC-W3C-LBD-BOT",
        "SRC-BRICK-SCHEMA",
        "SRC-PROJECT-HAYSTACK",
        "SRC-BUILDINGSMART-IDS-1-0",
        "SRC-CDC-LEGIONELLA-BUILDING-WATER",
        "SRC-IAPMO-UPC-METADATA",
    } <= source_ids

    readiness_payload = enrich_readiness_fixture(_load(READINESS))
    case_ids = {row["case_id"] for row in readiness_payload["resolver_golden_cases"]}
    assert {f"RES-DOMAIN-CLUSTER-{index:03d}" for index in range(1, 8)} <= case_ids
