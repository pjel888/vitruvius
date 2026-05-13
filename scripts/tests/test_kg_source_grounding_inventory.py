import json
from pathlib import Path

from pipeline_cli import build_parser
from vitruvius.kg.source_grounding_inventory import (
    SourceGroundingInventoryConfig,
    run_source_grounding_inventory,
)


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def _write_jsonl(path: Path, records: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(record) + "\n" for record in records), encoding="utf-8")


def _read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def test_source_grounding_inventory_counts_resource_and_overlay_coverage(tmp_path: Path) -> None:
    input_path = tmp_path / "backbone.json"
    resource_root = tmp_path / "resource-layer"
    overlay_root = tmp_path / "semantic-overlays"
    output_root = tmp_path / "inventory"
    overlay_dir = overlay_root / "RUN_A"

    _write_json(
        input_path,
        {
            "records": [
                {
                    "id": "N1",
                    "label": "Accessible Routes",
                    "pref_label": "Accessible Routes",
                    "review_status": "steward_admitted",
                    "path_code": "ACC.RTE",
                },
                {
                    "id": "N2",
                    "label": "Route Width",
                    "pref_label": "Route Width",
                    "review_status": "steward_admitted",
                    "path_code": "ACC.RTE.WID",
                },
            ],
            "relationships": [
                {
                    "from_id": "N1",
                    "predicate": "broader_than",
                    "to_id": "N2",
                    "governed": True,
                }
            ],
        },
    )
    _write_json(
        resource_root / "resources.json",
        {
            "resources": [
                {
                    "id": "RES1",
                    "title": "Accessibility Standard",
                    "resourceType": "standard",
                    "sourceAuthority": "official",
                    "accessType": "open_access",
                    "disciplineTags": ["accessibility"],
                    "taxonomyTags": ["ACC"],
                    "verificationStatus": "content_verified",
                    "createdAt": "2026-05-13T00:00:00Z",
                    "updatedAt": "2026-05-13T00:00:00Z",
                }
            ]
        },
    )
    _write_json(
        resource_root / "node-resource-links.json",
        {
            "nodeResourceLinks": [
                {
                    "id": "LINK1",
                    "nodeId": "N1",
                    "resourceId": "RES1",
                    "relationship": "supports",
                    "relevanceScore": 0.9,
                    "authorityScore": 0.9,
                    "confidenceScore": 0.9,
                    "rationale": "Direct support",
                    "supportsEdgeIds": ["N1--broader_than--N2"],
                    "reviewStatus": "accepted",
                    "createdAt": "2026-05-13T00:00:00Z",
                    "updatedAt": "2026-05-13T00:00:00Z",
                }
            ]
        },
    )
    _write_json(resource_root / "source-families.json", {"sourceFamilies": []})
    _write_json(resource_root / "resource-checks.json", {"resourceChecks": []})
    _write_json(resource_root / "resource-candidates.json", {"resourceCandidates": []})
    _write_json(overlay_dir / "relationship-improvement-report.json", {"status": "completed"})
    _write_jsonl(
        overlay_dir / "accepted-relationships.jsonl",
        [{"final_edge_key": "N2--requires--N1", "from_id": "N2", "predicate": "requires", "to_id": "N1"}],
    )
    _write_jsonl(
        overlay_dir / "accepted-node-consolidations.jsonl",
        [{"node_a_id": "N1", "node_b_id": "N2", "decision_status": "accepted"}],
    )

    summary = run_source_grounding_inventory(
        SourceGroundingInventoryConfig(
            input_path=input_path,
            output_root=output_root,
            run_id="TEST_INV",
            resource_layer_root=resource_root,
            semantic_overlay_root=overlay_root,
            relationship_run_id="RUN_A",
        )
    )

    report = json.loads(Path(summary.report_path).read_text(encoding="utf-8"))
    assert summary.node_source_backed_count == 1
    assert summary.relationship_source_backed_count == 1
    assert report["coverage"]["nodes"]["domain_synthesis"] == 1
    assert report["pending_overlay_summary"]["pending_relationship_overlay_count"] == 1
    assert report["pending_overlay_summary"]["pending_node_consolidation_overlay_count"] == 1
    assert report["source_gap_workqueue"]["enabled"] is True
    assert report["source_gap_workqueue"]["workqueue_item_count"] >= 1
    assert Path(summary.workqueue_path or "").exists()
    assert Path(summary.source_link_proposals_path or "").exists()
    assert report["safety"]["active_graph_mutation"] is False
    assert "reasoning_content" not in json.dumps(report)
    assert "sk-" not in json.dumps(report)


def test_source_grounding_inventory_is_no_write_for_inputs(tmp_path: Path) -> None:
    input_path = tmp_path / "backbone.json"
    resource_root = tmp_path / "resource-layer"
    before = {"records": [], "relationships": []}
    _write_json(input_path, before)
    _write_json(resource_root / "resources.json", {"resources": []})
    _write_json(resource_root / "node-resource-links.json", {"nodeResourceLinks": []})
    _write_json(resource_root / "source-families.json", {"sourceFamilies": []})
    _write_json(resource_root / "resource-checks.json", {"resourceChecks": []})
    _write_json(resource_root / "resource-candidates.json", {"resourceCandidates": []})
    input_before = input_path.read_text(encoding="utf-8")
    links_before = (resource_root / "node-resource-links.json").read_text(encoding="utf-8")

    run_source_grounding_inventory(
        SourceGroundingInventoryConfig(
            input_path=input_path,
            output_root=tmp_path / "inventory",
            run_id="NO_WRITE",
            resource_layer_root=resource_root,
            semantic_overlay_root=tmp_path / "semantic-overlays",
            relationship_run_id="none",
        )
    )

    assert input_path.read_text(encoding="utf-8") == input_before
    assert (resource_root / "node-resource-links.json").read_text(encoding="utf-8") == links_before


def test_source_grounding_inventory_writes_ranked_gap_workqueue_and_proposals(tmp_path: Path) -> None:
    input_path = tmp_path / "backbone.json"
    resource_root = tmp_path / "resource-layer"
    output_root = tmp_path / "inventory"
    _write_json(
        input_path,
        {
            "records": [
                {
                    "id": "N_FIRE",
                    "label": "Fire Safety Requirement",
                    "pref_label": "Fire Safety Requirement",
                    "review_status": "steward_admitted",
                    "path_code": "FLS.FIR.REQ",
                },
                {
                    "id": "N_EXIT",
                    "label": "Exit Access",
                    "pref_label": "Exit Access",
                    "review_status": "steward_admitted",
                    "path_code": "FLS.EGR.EXA",
                },
            ],
            "relationships": [
                {
                    "from_id": "N_FIRE",
                    "predicate": "requires",
                    "to_id": "N_EXIT",
                    "governed": True,
                }
            ],
        },
    )
    _write_json(
        resource_root / "resources.json",
        {
            "resources": [
                {
                    "id": "RES_FIRE",
                    "title": "Fire Safety Code Exit Access Guidance",
                    "resourceType": "government_guidance",
                    "sourceAuthority": "government",
                    "authorityTier": 1,
                    "accessType": "public_web",
                    "verificationStatus": "link_verified",
                    "disciplineTags": ["fire safety", "egress"],
                    "taxonomyTags": ["FLS", "exit access"],
                    "keywords": ["fire safety", "exit access", "requirements"],
                }
            ]
        },
    )
    _write_json(resource_root / "node-resource-links.json", {"nodeResourceLinks": []})
    _write_json(resource_root / "source-families.json", {"sourceFamilies": []})

    summary = run_source_grounding_inventory(
        SourceGroundingInventoryConfig(
            input_path=input_path,
            output_root=output_root,
            run_id="WORKQUEUE",
            resource_layer_root=resource_root,
            semantic_overlay_root=tmp_path / "semantic-overlays",
            relationship_run_id="none",
            max_workqueue_items=10,
            max_resource_proposals_per_item=2,
        )
    )

    workqueue = _read_jsonl(Path(summary.workqueue_path or ""))
    proposals = _read_jsonl(Path(summary.source_link_proposals_path or ""))
    assert workqueue
    assert proposals
    assert workqueue[0]["item_type"] == "relationship_source_gap"
    assert workqueue[0]["edge_key"] == "N_FIRE--requires--N_EXIT"
    assert workqueue[0]["suggested_resources"][0]["resource_id"] == "RES_FIRE"
    assert workqueue[0]["proposal_ids"]
    assert proposals[0]["target_type"] == "relationship"
    assert proposals[0]["auto_admit"] is False
    assert proposals[0]["active_graph_mutation"] is False
    assert proposals[0]["resource_layer_mutation"] is False


def test_source_grounding_inventory_gap_workqueue_can_be_disabled(tmp_path: Path) -> None:
    input_path = tmp_path / "backbone.json"
    resource_root = tmp_path / "resource-layer"
    _write_json(input_path, {"records": [], "relationships": []})
    _write_json(resource_root / "resources.json", {"resources": []})
    _write_json(resource_root / "node-resource-links.json", {"nodeResourceLinks": []})
    _write_json(resource_root / "source-families.json", {"sourceFamilies": []})

    summary = run_source_grounding_inventory(
        SourceGroundingInventoryConfig(
            input_path=input_path,
            output_root=tmp_path / "inventory",
            run_id="NO_WORKQUEUE",
            resource_layer_root=resource_root,
            semantic_overlay_root=tmp_path / "semantic-overlays",
            relationship_run_id="none",
            write_gap_workqueue=False,
        )
    )
    report = json.loads(Path(summary.report_path).read_text(encoding="utf-8"))

    assert summary.workqueue_path is None
    assert summary.source_link_proposals_path is None
    assert report["source_gap_workqueue"]["enabled"] is False


def test_source_grounding_inventory_workqueue_artifacts_are_sanitized(tmp_path: Path) -> None:
    input_path = tmp_path / "backbone.json"
    resource_root = tmp_path / "resource-layer"
    _write_json(
        input_path,
        {
            "records": [{"id": "N1", "label": "Bearer sk-secret reasoning_content", "review_status": "steward_admitted"}],
            "relationships": [],
        },
    )
    _write_json(
        resource_root / "resources.json",
        {
            "resources": [
                {
                    "id": "RES1",
                    "title": "Bearer sk-secret reasoning_content",
                    "resourceType": "government_guidance",
                    "sourceAuthority": "government",
                    "authorityTier": 1,
                    "verificationStatus": "link_verified",
                    "keywords": ["secret"],
                }
            ]
        },
    )
    _write_json(resource_root / "node-resource-links.json", {"nodeResourceLinks": []})
    _write_json(resource_root / "source-families.json", {"sourceFamilies": []})

    summary = run_source_grounding_inventory(
        SourceGroundingInventoryConfig(
            input_path=input_path,
            output_root=tmp_path / "inventory",
            run_id="SANITIZED",
            resource_layer_root=resource_root,
            semantic_overlay_root=tmp_path / "semantic-overlays",
            relationship_run_id="none",
        )
    )

    artifacts = [
        Path(summary.report_path).read_text(encoding="utf-8"),
        Path(summary.summary_path).read_text(encoding="utf-8"),
        Path(summary.workqueue_path or "").read_text(encoding="utf-8"),
        Path(summary.source_link_proposals_path or "").read_text(encoding="utf-8"),
    ]
    combined = "\n".join(artifacts)
    assert "reasoning_content" not in combined
    assert "Bearer " not in combined
    assert "sk-secret" not in combined


def test_pipeline_cli_accepts_source_grounding_inventory_command() -> None:
    args = build_parser().parse_args(
        [
            "aec-source-grounding-inventory",
            "--run-id",
            "CLI_PARSE",
            "--relationship-run-id",
            "latest",
            "--max-gap-examples",
            "10",
            "--max-workqueue-items",
            "25",
            "--max-resource-proposals-per-item",
            "3",
            "--min-resource-proposal-score",
            "0.2",
        ]
    )

    assert args.command == "aec-source-grounding-inventory"
    assert args.run_id == "CLI_PARSE"
    assert args.relationship_run_id == "latest"
    assert args.max_gap_examples == 10
    assert args.write_gap_workqueue is True
    assert args.max_workqueue_items == 25
    assert args.max_resource_proposals_per_item == 3
    assert args.min_resource_proposal_score == 0.2


def test_pipeline_cli_can_disable_source_grounding_workqueue() -> None:
    args = build_parser().parse_args(
        [
            "aec-source-grounding-inventory",
            "--run-id",
            "CLI_PARSE_NO_QUEUE",
            "--no-write-gap-workqueue",
        ]
    )

    assert args.command == "aec-source-grounding-inventory"
    assert args.write_gap_workqueue is False
