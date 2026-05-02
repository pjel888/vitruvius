from __future__ import annotations

from pathlib import Path

import pytest

from vitruvius.kg.backbone_graph_quality import GENERIC_RELATIONS, analyze_backbone_graph_quality, run_graph_quality_report


FIXTURE = Path("scripts/tests/fixtures/aec_mepfs_backbone/admitted_backbone_nodes_l1_l2.json")


def _node(node_id: str, label: str, path_code: str, *, generation_method: str = "base", parent_path_code: str | None = None):
    return {
        "id": node_id,
        "record_type": "BackboneNode",
        "label": label,
        "path_code": path_code,
        "parent_path_code": parent_path_code,
        "definition": f"Substantive definition for {label} with enough detail for validation.",
        "generation_method": generation_method,
    }


def _edge(from_id: str, to_id: str, predicate: str = "requires", *, generation_method: str = "base", edge_type: str | None = None):
    row = {
        "from_id": from_id,
        "to_id": to_id,
        "predicate": predicate,
        "generation_method": generation_method,
        "governed": True,
        "relation_type": "requires_test_reasoning",
        "relation_category": "coordination",
        "relation_nature": ["informational"],
        "direction": "from_to",
        "weight": 0.8,
        "confidence_score": 0.8,
        "discipline": ["aec"],
        "lifecycle_phase": ["design"],
        "source_family_ids": ["SRC-TEST"],
        "rationale": "This test relationship has enough rationale text to satisfy metadata validation.",
        "provenance_note": "Metadata-only test provenance.",
    }
    if edge_type is not None:
        row["predicate"] = ""
        row["edge_type"] = edge_type
    return row


def _payload(nodes=None, edges=None):
    return {"records": nodes or [], "relationships": edges or []}


def test_graph_quality_blocks_historical_self_loops_even_in_scoped_runs() -> None:
    payload = _payload(
        [_node("A", "A", "A"), _node("B", "B", "B", generation_method="new")],
        [_edge("A", "A", generation_method="historical"), _edge("A", "B", generation_method="new")],
    )

    report = analyze_backbone_graph_quality(payload, introduced_generation_method="new")

    assert report["ok"] is False
    assert any("self-loop" in error for error in report["errors"])
    assert report["metrics"]["self_loop_count"] == 1
    assert report["metrics"]["sample_self_loop_relationships"][0]["from_id"] == "A"


def test_graph_quality_blocks_introduced_self_loops() -> None:
    payload = _payload([_node("A", "A", "A", generation_method="new")], [_edge("A", "A", generation_method="new")])

    report = analyze_backbone_graph_quality(payload, introduced_generation_method="new")

    assert report["ok"] is False
    assert any("self-loop" in error for error in report["errors"])
    assert report["metrics"]["self_loop_count"] == 1


def test_graph_quality_duplicate_label_samples_and_same_parent_errors() -> None:
    payload = _payload(
        [
            _node("P", "Parent", "P"),
            _node("A", "Duplicate Label", "P.A", parent_path_code="P"),
            _node("B", "Duplicate Label", "P.B", parent_path_code="P"),
        ],
        [_edge("P", "A", "broader_than"), _edge("P", "B", "broader_than"), _edge("A", "P"), _edge("B", "P")],
    )

    report = analyze_backbone_graph_quality(payload, introduced_generation_method="new")

    assert report["ok"] is False
    assert report["metrics"]["duplicate_normalized_label_group_count"] == 1
    assert report["metrics"]["duplicate_normalized_label_node_count"] == 2
    assert report["metrics"]["duplicate_normalized_label_excess_count"] == 1
    assert report["metrics"]["same_parent_duplicate_normalized_label_count"] == 1
    assert report["metrics"]["duplicate_normalized_label_context_summary"]["review_class_counts"] == {
        "same_parent_blocker": 1,
    }
    assert report["metrics"]["sample_duplicate_normalized_labels"][0]["normalized_label"] == "duplicate label"
    assert any("same-parent duplicate" in error for error in report["errors"])


def test_graph_quality_writes_non_destructive_duplicate_label_context_index(tmp_path: Path) -> None:
    payload = _payload(
        [
            _node("ARC", "Architecture", "ARC"),
            _node("CIV", "Civil Engineering", "CIV"),
            _node("A", "Maintenance Access", "ARC.A", parent_path_code="ARC"),
            _node("B", "Maintenance Access", "CIV.B", parent_path_code="CIV"),
        ],
        [
            _edge("ARC", "A", "broader_than"),
            _edge("CIV", "B", "broader_than"),
            _edge("A", "ARC"),
            _edge("B", "CIV"),
        ],
    )
    fixture = tmp_path / "fixture.json"
    fixture.write_text(__import__("json").dumps(payload), encoding="utf-8")

    report = run_graph_quality_report(
        fixture,
        repo_root=tmp_path,
        run_id="DUPLICATE_CONTEXT",
        output_path="006_System-Manifests/aec-mepfs-backbone/graph-quality/DUPLICATE_CONTEXT/graph-quality-report.json",
    )

    assert report["ok"] is True
    assert report["warnings"] == ["duplicate normalized labels present: 1"]
    assert report["metrics"]["same_parent_duplicate_normalized_label_count"] == 0
    assert report["metrics"]["duplicate_normalized_label_context_summary"]["review_class_counts"] == {
        "contextual_duplicate": 1,
    }
    assert report["metrics"]["duplicate_normalized_label_context_summary"]["duplicate_scope_counts"] == {
        "cross_root": 1,
    }
    index_path = tmp_path / report["duplicate_label_context_index_path"]
    index = __import__("json").loads(index_path.read_text(encoding="utf-8"))
    assert index["schema_version"] == "aec-mepfs-backbone-duplicate-label-context-index/v1"
    assert index["group_count"] == 1
    assert index["groups"][0]["review_class"] == "contextual_duplicate"
    assert index["groups"][0]["nodes"][0]["display_hint"].startswith("Maintenance Access - ")


def test_graph_quality_counts_generic_predicate_and_edge_type_consistently() -> None:
    assert "related_to" in GENERIC_RELATIONS
    predicate_payload = _payload([_node("A", "A", "A"), _node("B", "B", "B")], [_edge("A", "B", "related_to")])
    edge_type_payload = _payload([_node("A", "A", "A"), _node("B", "B", "B")], [_edge("A", "B", edge_type="related_to")])

    predicate_report = analyze_backbone_graph_quality(predicate_payload, introduced_generation_method="new")
    edge_type_report = analyze_backbone_graph_quality(edge_type_payload, introduced_generation_method="new")

    assert predicate_report["metrics"]["generic_relationship_count"] == 1
    assert edge_type_report["metrics"]["generic_relationship_count"] == 1
    assert predicate_report["ok"] is False
    assert edge_type_report["ok"] is False


def test_graph_quality_reports_introduced_non_hierarchy_orphans() -> None:
    payload = _payload(
        [_node("A", "Parent", "A"), _node("B", "Child", "A.B", generation_method="new", parent_path_code="A")],
        [_edge("A", "B", "broader_than", generation_method="new")],
    )

    report = analyze_backbone_graph_quality(payload, introduced_generation_method="new")

    assert report["ok"] is False
    assert report["metrics"]["introduced_non_hierarchy_orphan_count"] == 1
    assert report["metrics"]["sample_introduced_non_hierarchy_orphan_path_codes"] == ["A.B"]
    assert any("introduced nodes without non-hierarchy relationships" in error for error in report["errors"])


def test_graph_quality_report_rejects_raw_source_output_path() -> None:
    with pytest.raises(ValueError, match="immutable raw source custody layer"):
        run_graph_quality_report(
            FIXTURE,
            run_id="RAW_OUTPUT_BLOCKED",
            output_path="001_Raw-Source-Layer/RAW_OUTPUT_BLOCKED/graph-quality-report.json",
        )


def test_graph_quality_report_rejects_unexpected_output_filename() -> None:
    with pytest.raises(ValueError, match="output filename must be graph-quality-report.json"):
        run_graph_quality_report(
            FIXTURE,
            run_id="BAD_FILENAME",
            output_path="006_System-Manifests/aec-mepfs-backbone/graph-quality/BAD_FILENAME/not-graph-quality.json",
        )
