from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

from vitruvius.kg.cross_domain_overlay_enrichment import (
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


def _fixture_payload() -> dict[str, Any]:
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def _source_rights_payload() -> dict[str, Any]:
    return json.loads(SOURCE_RIGHTS_REGISTRY.read_text(encoding="utf-8"))


def _overlay_records(payload: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        record
        for record in payload["records"]
        if record.get("generation_method") == GENERATION_METHOD
    ]


def _overlay_relationships(payload: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        relationship
        for relationship in payload["relationships"]
        if relationship.get("generation_method") == GENERATION_METHOD
    ]


def test_cross_domain_overlay_enrichment_is_idempotent_on_admitted_fixture() -> None:
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
    assert len(enriched["records"]) == len(payload["records"])
    assert len(enriched["relationships"]) == len(payload["relationships"])


def test_cross_domain_overlay_fixture_contains_practical_aec_mepfs_semantics() -> None:
    payload = _fixture_payload()
    records_by_id = {record["id"]: record for record in payload["records"]}
    overlay_records = _overlay_records(payload)
    overlay_relationships = _overlay_relationships(payload)

    assert len(overlay_records) == 91
    assert Counter(record["semantic_node_kind"] for record in overlay_records) == {
        "commissioning_overlay": 14,
        "semantic_overlay": 47,
        "semantic_overlay_parent": 3,
        "standard_family": 6,
        "standard_reference": 21,
    }
    assert len(overlay_relationships) == 460
    assert Counter(relationship["predicate"] for relationship in overlay_relationships) == {
        "applicable_in_jurisdiction": 6,
        "broader_than": 91,
        "constrains": 164,
        "governs": 8,
        "maps_to_external_standard": 42,
        "part_of": 21,
        "requires": 128,
    }
    assert Counter(
        relationship["semantic_overlay_category"] for relationship in overlay_relationships
    ) == {
        "applicability_overlay": 92,
        "commissioning_handover": 76,
        "equipment_anchorage": 101,
        "hierarchy": 91,
        "resilience_continuity": 79,
        "source_reference": 21,
    }
    cross_domain = [
        relationship
        for relationship in overlay_relationships
        if records_by_id[relationship["from_id"]]["path_code"].split(".")[0]
        != records_by_id[relationship["to_id"]]["path_code"].split(".")[0]
    ]
    assert len(cross_domain) == 321
    assert all(
        len(segment) == 3
        for record in overlay_records
        for segment in str(record["path_code"]).split(".")
    )
    assert {
        "COM.APP.AHJ",
        "COM.APP.FHA",
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
    for record in overlay_records:
        assert record["review_status"] == "steward_admitted"
        assert record["confidence"] == "high"
        assert record["source_family_ids"]
        assert "no standards clauses or protected source text stored" in record[
            "provenance_note"
        ]
        assert not str(record["label"]).endswith(("Concepts", "Concept Anchor", "Rule Context", "Topics"))
    for relationship in overlay_relationships:
        assert relationship["governed"] is True
        assert relationship["source_family_ids"]
        assert "metadata-only semantic overlay relationship" in relationship[
            "provenance_note"
        ]


def test_cross_domain_overlay_improves_existing_endpoints_with_aliases_and_sources() -> None:
    payload = _fixture_payload()
    records_by_path = {record["path_code"]: record for record in payload["records"]}

    expected_aliases = {
        "MEC.PLT": "mechanical equipment anchorage",
        "ELE.PDS": "switchgear support coordination",
        "FLS.FDA.FAC": "fire alarm acceptance",
        "PLS.PWS.BAP": "backflow testing",
        "SMS.CSB.NES": "OT network segmentation",
        "DIG.DTA.LDH": "digital handover",
        "COM.OCC.OCL": "occupancy trigger",
        "ELE.ESP.GTS": "generator anchorage",
    }
    for path_code, alias in expected_aliases.items():
        aliases = records_by_path[path_code].get("aliases", [])
        assert alias in aliases
        assert records_by_path[path_code].get("source_family_ids")


def test_cross_domain_source_rights_registry_is_idempotent_and_metadata_only() -> None:
    payload = _source_rights_payload()

    enriched, report = enrich_source_rights_registry(payload)

    assert report["ok"] is True
    assert report["added_source_reference_count"] == 0
    assert len(enriched["source_rights_registry"]) == len(payload["source_rights_registry"])
    source_ids = {row["source_id"] for row in enriched["source_rights_registry"]}
    assert {reference["source_id"] for reference in SOURCE_REFERENCES} <= source_ids
    for row in enriched["source_rights_registry"]:
        if row["source_id"] not in {reference["source_id"] for reference in SOURCE_REFERENCES}:
            continue
        assert row["source_rights_class"] == "reference_only"
        assert row["clearance_state"] == "planning_reference_only"
        assert "no standards text" in row["declared_use_boundary"]
        assert "clause ingest" in row["declared_use_boundary"]
        assert row["blocking_notes"].startswith("content ingest blocked")
