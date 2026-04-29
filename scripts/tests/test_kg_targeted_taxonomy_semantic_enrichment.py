from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from vitruvius.kg.targeted_taxonomy_semantic_enrichment import (
    GENERATION_METHOD,
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


def _fixture_payload() -> dict[str, object]:
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def _source_rights_payload() -> dict[str, object]:
    return json.loads(SOURCE_RIGHTS_REGISTRY.read_text(encoding="utf-8"))


def _targeted_records(payload: dict[str, object]) -> list[dict[str, object]]:
    return [
        record
        for record in payload["records"]  # type: ignore[index]
        if record.get("generation_method") == GENERATION_METHOD
    ]


def _targeted_relationships(payload: dict[str, object]) -> list[dict[str, object]]:
    return [
        relationship
        for relationship in payload["relationships"]  # type: ignore[index]
        if relationship.get("generation_method") == GENERATION_METHOD
    ]


def test_targeted_taxonomy_enrichment_is_idempotent_on_admitted_fixture() -> None:
    payload = _fixture_payload()

    enriched, report = enrich(payload)

    assert report["ok"] is True
    assert report["added_node_count"] == 0
    assert report["added_relationship_count"] == 0
    assert report["improved_existing_node_count"] == 0
    assert report["aliases_added_or_preserved_on_new_and_improved_nodes"] == 0
    assert report["rights_safety"] == {
        "protected_source_payloads_ingested": False,
        "source_payload_mode": "labels_metadata_and_source_family_references_only",
        "neo4j_mutation": False,
        "kg_rebuild_reload_reset": False,
        "api_or_explorer_runtime_behavior_changed": False,
        "codex_spark_used_for_research_or_synthesis": False,
        "kimi_used_for_advisory_synthesis": True,
    }
    assert len(enriched["records"]) == len(payload["records"])  # type: ignore[index]
    assert len(enriched["relationships"]) == len(payload["relationships"])  # type: ignore[index]


def test_targeted_taxonomy_fixture_contains_real_nodes_and_semantic_edges() -> None:
    payload = _fixture_payload()
    targeted_records = _targeted_records(payload)
    targeted_relationships = _targeted_relationships(payload)

    assert len(targeted_records) == 141
    assert Counter(record["semantic_node_kind"] for record in targeted_records) == {
        "discipline_topic": 88,
        "standard_reference": 45,
        "standard_family": 8,
    }
    assert len(targeted_relationships) == 415
    assert Counter(relationship["predicate"] for relationship in targeted_relationships) == {
        "broader_than": 141,
        "constrains": 45,
        "has_facet": 8,
        "maps_to_external_standard": 88,
        "part_of": 45,
        "requires": 88,
    }
    assert all(
        len(segment) == 3
        for record in targeted_records
        for segment in str(record["path_code"]).split(".")
    )
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
        "HRC.PRN.MIX.RFS",
        "SUS.CAR.LCA.GSD",
        "OPS.AST.AIM.CBM",
    } <= {record["path_code"] for record in targeted_records}
    for record in targeted_records:
        assert record["review_status"] == "steward_admitted"
        assert record["confidence"] == "high"
        assert record["source_family_ids"]
        assert "no standards clauses or protected source text stored" in record[
            "provenance_note"
        ]
        assert not str(record["label"]).endswith(("Concepts", "Concept Anchor", "Rule Context", "Topics"))


def test_targeted_source_rights_registry_is_idempotent_and_metadata_only() -> None:
    payload = _source_rights_payload()

    enriched, report = enrich_source_rights_registry(payload)

    assert report["ok"] is True
    assert report["added_source_reference_count"] == 0
    assert len(enriched["source_rights_registry"]) == len(payload["source_rights_registry"])  # type: ignore[index]
    source_ids = {row["source_id"] for row in enriched["source_rights_registry"]}  # type: ignore[index]
    assert {reference["source_id"] for reference in SOURCE_REFERENCES} <= source_ids
    for row in enriched["source_rights_registry"]:  # type: ignore[index]
        if row["source_id"] not in {reference["source_id"] for reference in SOURCE_REFERENCES}:
            continue
        assert row["source_rights_class"] == "reference_only"
        assert row["clearance_state"] == "planning_reference_only"
        assert "no standards text" in row["declared_use_boundary"]
        assert "clause ingest" in row["declared_use_boundary"]
