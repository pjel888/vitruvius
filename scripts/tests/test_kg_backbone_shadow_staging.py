from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from vitruvius.kg.backbone_shadow_staging import (
    SHADOW_GRAPH_ARTIFACT_FILENAME,
    SHADOW_STAGING_ARTIFACT_FILENAME,
    SHADOW_STAGING_REPORT_FILENAME,
    stage_shadow_backbone,
)


def _predicate_payload() -> dict[str, Any]:
    return {
        "predicate_registry": [
            {
                "predicate": "broader_than",
                "direction": "parent_to_child",
                "category": "hierarchy",
                "domain_classes": ["BackboneNode"],
                "range_classes": ["BackboneNode"],
                "allowed_strength_classes": ["steward-curated"],
                "evidence_required_fields": ["owner", "review_status"],
                "owner": "Philip Lewis",
                "examples": ["Architecture is broader than architectural accessibility."],
                "non_examples": ["A source document mentions a concept."],
                "validation_rule": "must not replace provenance",
                "migration_behavior": "legacy links require steward mapping",
            }
        ]
    }


def _source_rights_payload() -> dict[str, Any]:
    return {
        "source_rights_registry": [
            {
                "source_id": "SRC-TEST-001",
                "source_family": "Test Source",
                "publisher_authority": "Test Publisher",
                "edition_version_effective_date": "admission-time verification required",
                "official_url": "https://example.test/source",
                "source_rights_class": "metadata_crosswalk",
                "clearance_state": "metadata_crosswalk_planned",
                "intended_vitruvius_use": "metadata crosswalk only",
                "steward_owner": "Philip Lewis",
                "declared_use_boundary": "no source text, tables, figures, or clauses ingested",
                "currentness_check_date": "2026-04-25",
                "update_cadence": "before source admission",
                "blocking_notes": "content ingest blocked",
            }
        ]
    }


def _backbone_nodes_payload() -> dict[str, Any]:
    return {
        "records": [
            {
                "id": "VTN-DOM-0000001",
                "canonical_id": "VTN-DOM-0000001",
                "record_type": "BackboneNode",
                "review_status": "steward_admitted",
                "label": "Architecture",
                "pref_label": "Architecture",
                "definition": "Built-environment discipline covering building form, space, use, and coordination.",
                "path_code": "ARC",
                "level": 1,
                "parent_path_code": None,
                "owner": "Philip Lewis",
                "steward": "Philip Lewis",
                "release_version": "0.1.0",
            },
            {
                "id": "VTN-DOM-0000002",
                "canonical_id": "VTN-DOM-0000002",
                "record_type": "BackboneNode",
                "review_status": "steward_admitted",
                "label": "Spatial Planning",
                "pref_label": "Spatial Planning",
                "definition": "Architectural organization of rooms, circulation, access, use, and spatial performance.",
                "path_code": "ARC.SPC",
                "level": 2,
                "parent_path_code": "ARC",
                "owner": "Philip Lewis",
                "steward": "Philip Lewis",
                "release_version": "0.1.0",
            },
        ],
        "relationships": [
            {
                "from_id": "VTN-DOM-0000001",
                "predicate": "broader_than",
                "to_id": "VTN-DOM-0000002",
                "governed": True,
            }
        ],
    }


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def test_shadow_staging_writes_file_backed_artifact_without_live_boundaries(tmp_path: Path) -> None:
    predicate_path = tmp_path / "predicate-registry.json"
    source_path = tmp_path / "source-rights-registry.json"
    output_dir = tmp_path / "shadow"
    _write_json(predicate_path, _predicate_payload())
    _write_json(source_path, _source_rights_payload())

    report = stage_shadow_backbone(
        predicate_registry_path=predicate_path,
        source_rights_registry_path=source_path,
        repo_root=tmp_path,
        run_id="TEST_RUN",
        output_dir=output_dir,
    )

    assert report["ok"] is True
    assert report["artifact_written"] is True
    assert report["shadow_graph_written"] is False
    assert report["counts"] == {
        "predicate_registry": 1,
        "source_rights_registry": 1,
    }
    assert report["boundaries"]["shadow_only"] is True
    assert report["boundaries"]["live_neo4j_writes"] is False
    assert report["boundaries"]["protected_content_ingest"] is False

    artifact = json.loads((output_dir / SHADOW_STAGING_ARTIFACT_FILENAME).read_text())
    assert artifact["status"] == "shadow_staged"
    assert artifact["predicate_registry"][0]["predicate"] == "broader_than"
    assert artifact["source_rights_registry"][0]["source_id"] == "SRC-TEST-001"
    assert (output_dir / SHADOW_STAGING_REPORT_FILENAME).is_file()


def test_shadow_staging_can_stage_admitted_backbone_nodes_without_live_cutover(
    tmp_path: Path,
) -> None:
    predicate_path = tmp_path / "predicate-registry.json"
    source_path = tmp_path / "source-rights-registry.json"
    backbone_nodes_path = tmp_path / "backbone-nodes.json"
    output_dir = tmp_path / "shadow"
    _write_json(predicate_path, _predicate_payload())
    _write_json(source_path, _source_rights_payload())
    _write_json(backbone_nodes_path, _backbone_nodes_payload())

    report = stage_shadow_backbone(
        predicate_registry_path=predicate_path,
        source_rights_registry_path=source_path,
        backbone_nodes_path=backbone_nodes_path,
        repo_root=tmp_path,
        run_id="TEST_RUN",
        output_dir=output_dir,
    )

    assert report["ok"] is True
    assert report["artifact_written"] is True
    assert report["shadow_graph_written"] is True
    assert report["backbone_nodes_path"] == "backbone-nodes.json"
    assert report["shadow_graph_path"] == "shadow/shadow-backbone-graph.json"
    assert report["counts"] == {
        "predicate_registry": 1,
        "source_rights_registry": 1,
        "backbone_nodes": 2,
    }
    assert report["contract_reports"]["backbone_nodes"]["record_counts"] == {
        "BackboneNode": 2,
    }

    artifact = json.loads((output_dir / SHADOW_STAGING_ARTIFACT_FILENAME).read_text())
    assert artifact["source_paths"]["backbone_nodes"] == "backbone-nodes.json"
    assert artifact["counts"]["backbone_nodes"] == 2
    assert artifact["backbone_nodes"][1]["path_code"] == "ARC.SPC"
    assert "shadow_graph" not in artifact

    shadow_graph = json.loads((output_dir / SHADOW_GRAPH_ARTIFACT_FILENAME).read_text())
    assert shadow_graph["source_artifact_path"] == "shadow/shadow-backbone-staging.json"
    assert shadow_graph["counts"] == {
        "nodes": 2,
        "edges": 1,
        "roots": 1,
        "max_depth": 2,
    }
    assert [node["path_code"] for node in shadow_graph["nodes"]] == [
        "ARC",
        "ARC.SPC",
    ]
    assert shadow_graph["edges"] == [
        {
            "id": "VTN-DOM-0000001--broader_than--VTN-DOM-0000002",
            "from_id": "VTN-DOM-0000001",
            "to_id": "VTN-DOM-0000002",
            "predicate": "broader_than",
            "from_path_code": "ARC",
            "to_path_code": "ARC.SPC",
        }
    ]
    assert artifact["boundaries"]["api_explorer_cutover"] is False
    assert artifact["boundaries"]["live_neo4j_writes"] is False


def test_shadow_staging_preserves_optional_edge_reasoning_metadata(
    tmp_path: Path,
) -> None:
    predicate_path = tmp_path / "predicate-registry.json"
    source_path = tmp_path / "source-rights-registry.json"
    backbone_nodes_path = tmp_path / "backbone-nodes.json"
    output_dir = tmp_path / "shadow"
    payload = _backbone_nodes_payload()
    payload["relationships"][0].update(
        {
            "relation_type": "taxonomy_parent_of",
            "relation_category": "taxonomy",
            "relation_nature": ["informational"],
            "direction": "from_to",
            "weight": 1.0,
            "confidence_score": 0.96,
            "discipline": ["architecture"],
            "lifecycle_phase": ["planning", "design"],
            "source_family_ids": ["SRC-TEST-001"],
            "rationale": "Parent-child taxonomy edge preserved with optional reasoning metadata.",
            "provenance_note": "metadata only",
            "generation_method": "test_metadata_preservation",
            "review_status": "steward_admitted",
            "semantic_overlay_category": "test",
            "applicability_basis": "source_family_only_ahj_or_project_basis_required",
            "jurisdiction_context": "source-family-mixed-ahj-required",
            "design_basis_status": "no_project_numeric_criteria_admitted",
        }
    )
    _write_json(predicate_path, _predicate_payload())
    _write_json(source_path, _source_rights_payload())
    _write_json(backbone_nodes_path, payload)

    report = stage_shadow_backbone(
        predicate_registry_path=predicate_path,
        source_rights_registry_path=source_path,
        backbone_nodes_path=backbone_nodes_path,
        repo_root=tmp_path,
        run_id="TEST_RUN",
        output_dir=output_dir,
    )

    assert report["ok"] is True
    shadow_graph = json.loads((output_dir / SHADOW_GRAPH_ARTIFACT_FILENAME).read_text())
    edge = shadow_graph["edges"][0]
    assert edge["relation_type"] == "taxonomy_parent_of"
    assert edge["relation_category"] == "taxonomy"
    assert edge["weight"] == 1.0
    assert edge["source_family_ids"] == ["SRC-TEST-001"]
    assert edge["rationale"].startswith("Parent-child taxonomy edge")
    assert edge["applicability_basis"] == "source_family_only_ahj_or_project_basis_required"
    assert edge["jurisdiction_context"] == "source-family-mixed-ahj-required"
    assert edge["design_basis_status"] == "no_project_numeric_criteria_admitted"


def test_shadow_staging_excludes_candidate_nodes_from_shadow_graph(
    tmp_path: Path,
) -> None:
    predicate_path = tmp_path / "predicate-registry.json"
    source_path = tmp_path / "source-rights-registry.json"
    backbone_nodes_path = tmp_path / "backbone-nodes.json"
    output_dir = tmp_path / "shadow"
    payload = _backbone_nodes_payload()
    payload["records"].append(
        {
            "id": "VTN-DOM-0000003",
            "canonical_id": "VTN-DOM-0000003",
            "record_type": "BackboneNode",
            "review_status": "candidate",
            "label": "Candidate Node",
            "pref_label": "Candidate Node",
            "definition": "Candidate-only row that must not enter the shadow graph.",
            "path_code": "ARC.CAN",
            "level": 2,
            "parent_path_code": "ARC",
            "owner": "Philip Lewis",
            "steward": "Philip Lewis",
            "release_version": "0.1.0",
        }
    )
    _write_json(predicate_path, _predicate_payload())
    _write_json(source_path, _source_rights_payload())
    _write_json(backbone_nodes_path, payload)

    report = stage_shadow_backbone(
        predicate_registry_path=predicate_path,
        source_rights_registry_path=source_path,
        backbone_nodes_path=backbone_nodes_path,
        repo_root=tmp_path,
        run_id="TEST_RUN",
        output_dir=output_dir,
    )

    assert report["ok"] is True
    artifact = json.loads((output_dir / SHADOW_STAGING_ARTIFACT_FILENAME).read_text())
    shadow_graph = json.loads((output_dir / SHADOW_GRAPH_ARTIFACT_FILENAME).read_text())
    assert artifact["counts"]["backbone_nodes"] == 2
    assert shadow_graph["counts"]["nodes"] == 2
    assert {node["id"] for node in shadow_graph["nodes"]} == {
        "VTN-DOM-0000001",
        "VTN-DOM-0000002",
    }


def test_shadow_staging_rejects_shadow_graph_edges_to_non_admitted_nodes(
    tmp_path: Path,
) -> None:
    predicate_path = tmp_path / "predicate-registry.json"
    source_path = tmp_path / "source-rights-registry.json"
    backbone_nodes_path = tmp_path / "backbone-nodes.json"
    output_dir = tmp_path / "shadow"
    payload = _backbone_nodes_payload()
    payload["relationships"].append(
        {
            "from_id": "VTN-DOM-0000001",
            "predicate": "broader_than",
            "to_id": "VTN-DOM-9999999",
            "governed": True,
        }
    )
    _write_json(predicate_path, _predicate_payload())
    _write_json(source_path, _source_rights_payload())
    _write_json(backbone_nodes_path, payload)

    report = stage_shadow_backbone(
        predicate_registry_path=predicate_path,
        source_rights_registry_path=source_path,
        backbone_nodes_path=backbone_nodes_path,
        repo_root=tmp_path,
        run_id="TEST_RUN",
        output_dir=output_dir,
    )

    assert report["ok"] is False
    assert report["artifact_written"] is False
    assert (
        "shadow_graph.relationships[1].to_id: 'VTN-DOM-9999999' is not an admitted BackboneNode"
        in report["errors"]
    )


def test_shadow_staging_rejects_relationship_predicates_missing_from_registry(
    tmp_path: Path,
) -> None:
    predicate_path = tmp_path / "predicate-registry.json"
    source_path = tmp_path / "source-rights-registry.json"
    backbone_nodes_path = tmp_path / "backbone-nodes.json"
    output_dir = tmp_path / "shadow"
    payload = _backbone_nodes_payload()
    payload["relationships"].append(
        {
            "from_id": "VTN-DOM-0000001",
            "predicate": "requires",
            "to_id": "VTN-DOM-0000002",
            "governed": True,
        }
    )
    _write_json(predicate_path, _predicate_payload())
    _write_json(source_path, _source_rights_payload())
    _write_json(backbone_nodes_path, payload)

    report = stage_shadow_backbone(
        predicate_registry_path=predicate_path,
        source_rights_registry_path=source_path,
        backbone_nodes_path=backbone_nodes_path,
        repo_root=tmp_path,
        run_id="TEST_RUN",
        output_dir=output_dir,
    )

    assert report["ok"] is False
    assert report["artifact_written"] is False
    assert (
        "shadow_graph.relationships[1].predicate: 'requires' is not present in predicate_registry"
        in report["errors"]
    )
    assert not (output_dir / SHADOW_GRAPH_ARTIFACT_FILENAME).exists()


def test_shadow_staging_requires_parent_hierarchy_edge_for_l2_nodes(
    tmp_path: Path,
) -> None:
    predicate_path = tmp_path / "predicate-registry.json"
    source_path = tmp_path / "source-rights-registry.json"
    backbone_nodes_path = tmp_path / "backbone-nodes.json"
    output_dir = tmp_path / "shadow"
    payload = _backbone_nodes_payload()
    payload["relationships"] = []
    _write_json(predicate_path, _predicate_payload())
    _write_json(source_path, _source_rights_payload())
    _write_json(backbone_nodes_path, payload)

    report = stage_shadow_backbone(
        predicate_registry_path=predicate_path,
        source_rights_registry_path=source_path,
        backbone_nodes_path=backbone_nodes_path,
        repo_root=tmp_path,
        run_id="TEST_RUN",
        output_dir=output_dir,
    )

    assert report["ok"] is False
    assert (
        "shadow_graph.nodes[1]: missing broader_than edge from parent "
        "VTN-DOM-0000001 to VTN-DOM-0000002"
    ) in report["errors"]


def test_shadow_staging_rejects_empty_admitted_backbone_node_payload(
    tmp_path: Path,
) -> None:
    predicate_path = tmp_path / "predicate-registry.json"
    source_path = tmp_path / "source-rights-registry.json"
    backbone_nodes_path = tmp_path / "backbone-nodes.json"
    output_dir = tmp_path / "shadow"
    payload = _backbone_nodes_payload()
    for record in payload["records"]:
        record["review_status"] = "candidate"
    _write_json(predicate_path, _predicate_payload())
    _write_json(source_path, _source_rights_payload())
    _write_json(backbone_nodes_path, payload)

    report = stage_shadow_backbone(
        predicate_registry_path=predicate_path,
        source_rights_registry_path=source_path,
        backbone_nodes_path=backbone_nodes_path,
        repo_root=tmp_path,
        run_id="TEST_RUN",
        output_dir=output_dir,
    )

    assert report["ok"] is False
    assert report["artifact_written"] is False
    assert (
        "backbone_nodes: expected at least one admitted BackboneNode record"
        in report["errors"]
    )
    assert not (output_dir / SHADOW_STAGING_ARTIFACT_FILENAME).exists()


def test_shadow_staging_blocks_content_ingest_even_when_registry_is_structured(
    tmp_path: Path,
) -> None:
    predicate_path = tmp_path / "predicate-registry.json"
    source_path = tmp_path / "source-rights-registry.json"
    output_dir = tmp_path / "shadow"
    source_payload = _source_rights_payload()
    source_payload["source_rights_registry"][0]["source_rights_class"] = "content_ingest"
    source_payload["source_rights_registry"][0]["clearance_state"] = "cleared_for_declared_use"
    _write_json(predicate_path, _predicate_payload())
    _write_json(source_path, source_payload)

    report = stage_shadow_backbone(
        predicate_registry_path=predicate_path,
        source_rights_registry_path=source_path,
        repo_root=tmp_path,
        run_id="TEST_RUN",
        output_dir=output_dir,
    )

    assert report["ok"] is False
    assert report["artifact_written"] is False
    assert any("content_ingest is blocked for shadow staging" in error for error in report["errors"])
    assert not (output_dir / SHADOW_STAGING_ARTIFACT_FILENAME).exists()
    assert (output_dir / SHADOW_STAGING_REPORT_FILENAME).is_file()


def test_shadow_staging_rejects_unsafe_run_id(tmp_path: Path) -> None:
    predicate_path = tmp_path / "predicate-registry.json"
    source_path = tmp_path / "source-rights-registry.json"
    _write_json(predicate_path, _predicate_payload())
    _write_json(source_path, _source_rights_payload())

    with pytest.raises(ValueError, match="run_id contains unsupported characters"):
        stage_shadow_backbone(
            predicate_registry_path=predicate_path,
            source_rights_registry_path=source_path,
            repo_root=tmp_path,
            run_id="../bad",
        )
