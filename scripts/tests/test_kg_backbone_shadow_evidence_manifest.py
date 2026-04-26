from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import pytest

from vitruvius.kg.backbone_shadow_evidence_manifest import run_shadow_evidence_manifest


PRODUCER_REPORT = Path(
    "006_System-Manifests/aec-mepfs-backbone/shadow-staging/20260426T003710Z/"
    "shadow-staging-report.json"
)
CONSUMER_REPORT = Path(
    "006_System-Manifests/aec-mepfs-backbone/shadow-staging/20260426T003710Z/"
    "shadow-staging-consumer-report.json"
)
SHADOW_GRAPH = Path(
    "006_System-Manifests/aec-mepfs-backbone/shadow-staging/20260426T003710Z/"
    "shadow-backbone-graph.json"
)
PARITY_REPORT = Path(
    "006_System-Manifests/aec-mepfs-backbone/parity/20260426T095440Z/"
    "api-explorer-parity-report.json"
)
PLACEMENT_REPORT = Path(
    "006_System-Manifests/aec-mepfs-backbone/placement-qa/20260426T015915Z/"
    "placement-qa-report.json"
)
RESOLVER_REPORT = Path(
    "006_System-Manifests/aec-mepfs-backbone/resolver-qa/20260426T060300Z/"
    "resolver-qa-report.json"
)
BOUNDARY_REPORT = Path(
    "006_System-Manifests/aec-mepfs-backbone/boundary-audit/20260426T100631Z/"
    "shadow-boundary-audit-report.json"
)
BENCHMARK_REPORT = Path(
    "006_System-Manifests/aec-mepfs-backbone/benchmarks/20260426T100632Z/"
    "benchmark-report.json"
)
ROUTE_INVENTORY_REPORT = Path(
    "006_System-Manifests/aec-mepfs-backbone/api-route-inventory/20260426T095439Z/"
    "api-route-inventory-report.json"
)
STAGING_ARTIFACT = (
    "006_System-Manifests/aec-mepfs-backbone/shadow-staging/20260426T003710Z/"
    "shadow-backbone-staging.json"
)


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def _hash_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _clean_repo_state(head: str = "abc123") -> dict[str, Any]:
    return {
        "generated_evidence_dirty": False,
        "generated_evidence_dirty_path_count": 0,
        "git_head_commit": head,
        "source_dirty_path_count": 0,
        "source_working_tree_dirty": False,
        "working_tree_dirty": False,
    }


def _write_manifest_inputs(tmp_path: Path) -> dict[str, Path]:
    api_index = tmp_path / "api" / "index.ts"
    api_index.parent.mkdir(parents=True, exist_ok=True)
    api_index.write_text(
        "app.get('/v2/backbone', handler);\n"
        "app.get('/v2/backbone/evidence', handler);\n",
        encoding="utf-8",
    )
    api_hash = _hash_file(api_index)
    paths = {
        "api_index": api_index,
        "producer": tmp_path / PRODUCER_REPORT,
        "consumer": tmp_path / CONSUMER_REPORT,
        "graph": tmp_path / SHADOW_GRAPH,
        "parity": tmp_path / PARITY_REPORT,
        "placement": tmp_path / PLACEMENT_REPORT,
        "resolver": tmp_path / RESOLVER_REPORT,
        "boundary": tmp_path / BOUNDARY_REPORT,
        "benchmark": tmp_path / BENCHMARK_REPORT,
        "route_inventory": tmp_path / ROUTE_INVENTORY_REPORT,
    }
    _write_json(
        paths["producer"],
        {
            "artifact_path": STAGING_ARTIFACT,
            "ok": True,
            "schema_version": "aec-bb-shadow-staging-report/v1",
        },
    )
    _write_json(
        paths["consumer"],
        {
            "ok": True,
            "producer_report_path": str(PRODUCER_REPORT),
            "schema_version": "aec-bb-shadow-staging-consumer-report/v1",
            "shadow_graph_counts": {"edges": 1, "max_depth": 1, "nodes": 2, "roots": 1},
            "shadow_graph_path": str(SHADOW_GRAPH),
        },
    )
    _write_json(
        paths["graph"],
        {
            "counts": {"edges": 1, "max_depth": 1, "nodes": 2, "roots": 1},
            "schema_version": "aec-bb-shadow-graph/v1",
            "source_artifact_path": STAGING_ARTIFACT,
            "status": "shadow_graph_staged",
        },
    )
    _write_json(paths["parity"], {"ok": True, "schema_version": "aec-bb-parity-report/v1"})
    _write_json(
        paths["placement"],
        {"ok": True, "schema_version": "aec-bb-placement-qa-report/v1"},
    )
    _write_json(
        paths["resolver"],
        {"ok": True, "schema_version": "aec-bb-resolver-qa-report/v1"},
    )
    _write_json(
        paths["boundary"],
        {
            "ok": True,
            "repo_state": _clean_repo_state(),
            "safety_invariants": {
                "generated_artifacts_file_backed_auditable": True,
                "no_explorer_default_adoption": True,
                "no_feature_flag_cutover": True,
                "no_kg_rebuild": True,
                "no_neo4j_writes": True,
                "no_protected_content_ingest": True,
                "no_resolver_route_mounting": True,
                "preview_read_only_shadow_only": True,
            },
            "schema_version": "aec-bb-shadow-boundary-audit-report/v1",
            "summary": {"checks_passed": 10, "checks_total": 10},
            "input_file_hashes_sha256": {"api_index": api_hash},
        },
    )
    _write_json(
        paths["benchmark"],
        {
            "benchmark_scope": {
                "api_server_calls": False,
                "explorer_runtime_calls": False,
                "feature_flag_cutover": False,
                "kg_rebuild": False,
                "neo4j_queries": False,
                "protected_content_ingest": False,
                "runtime_thresholds_evaluated": False,
                "shadow_file_backed_only": True,
            },
            "inputs": {
                "api_index": "api/index.ts",
                "boundary_audit_report": str(BOUNDARY_REPORT),
            },
            "ok": True,
            "operations": [{"name": "contract_validation", "ok": True}],
            "repo_state": _clean_repo_state(),
            "schema_version": "aec-bb-shadow-benchmark-report/v1",
            "input_file_hashes_sha256": {"api_index": api_hash},
        },
    )
    _write_json(
        paths["route_inventory"],
        {
            "ok": True,
            "repo_state": _clean_repo_state(),
            "schema_version": "aec-bb-api-route-inventory-report/v1",
            "input_file_hashes_sha256": {"api_index": api_hash},
            "summary": {
                "missing_preview_routes": [],
                "preview_routes_present": 7,
                "preview_routes_required": 7,
                "resolve_route_mounted": False,
                "route_count": 22,
                "trace_route_mounted": False,
            },
        },
    )
    return paths


def test_evidence_manifest_writes_report_for_current_shadow_packet(tmp_path: Path) -> None:
    _write_manifest_inputs(tmp_path)

    report = run_shadow_evidence_manifest(repo_root=tmp_path, run_id="TEST_MANIFEST")

    saved = json.loads(
        (
            tmp_path
            / "006_System-Manifests"
            / "aec-mepfs-backbone"
            / "evidence-manifest"
            / "TEST_MANIFEST"
            / "shadow-evidence-manifest-report.json"
        ).read_text(encoding="utf-8")
    )
    assert saved == report
    assert report["ok"] is True
    assert report["summary"]["artifact_count"] == 9
    assert report["summary"]["shadow_graph_counts"] == {
        "edges": 1,
        "max_depth": 1,
        "nodes": 2,
        "roots": 1,
    }
    assert report["artifact_results"][0]["path"] == str(PRODUCER_REPORT)
    assert report["inputs"]["api_index"] == "api/index.ts"
    assert report["repo_state"] == {
        "generated_evidence_dirty": False,
        "generated_evidence_dirty_path_count": 0,
        "git_head_commit": None,
        "source_dirty_path_count": 0,
        "source_working_tree_dirty": False,
        "working_tree_dirty": False,
    }
    assert len(report["input_file_hashes_sha256"]["api_index"]) == 64
    assert report["safety_invariants"] == {
        "all_artifacts_ok": True,
        "benchmark_shadow_file_backed_only": True,
        "boundary_audit_safety_green": True,
        "no_runtime_promotion": True,
        "resolver_routes_unmounted": True,
        "route_inventory_preview_routes_complete": True,
        "runtime_thresholds_not_evaluated": True,
    }
    assert all(len(digest) == 64 for digest in report["input_file_hashes_sha256"].values())


def test_evidence_manifest_detects_stale_benchmark_boundary_input(tmp_path: Path) -> None:
    paths = _write_manifest_inputs(tmp_path)
    benchmark = json.loads(paths["benchmark"].read_text(encoding="utf-8"))
    benchmark["inputs"]["boundary_audit_report"] = (
        "006_System-Manifests/aec-mepfs-backbone/boundary-audit/OLD/"
        "shadow-boundary-audit-report.json"
    )
    _write_json(paths["benchmark"], benchmark)

    report = run_shadow_evidence_manifest(repo_root=tmp_path, run_id="TEST_MANIFEST")

    assert report["ok"] is False
    assert report["safety_invariants"]["all_artifacts_ok"] is False
    assert any("benchmark_report.inputs.boundary_audit_report" in error for error in report["errors"])


def test_evidence_manifest_fails_if_route_inventory_mounts_resolver(tmp_path: Path) -> None:
    paths = _write_manifest_inputs(tmp_path)
    route_inventory = json.loads(paths["route_inventory"].read_text(encoding="utf-8"))
    route_inventory["summary"]["resolve_route_mounted"] = True
    _write_json(paths["route_inventory"], route_inventory)

    report = run_shadow_evidence_manifest(repo_root=tmp_path, run_id="TEST_MANIFEST")

    assert report["ok"] is False
    assert report["safety_invariants"]["resolver_routes_unmounted"] is False
    assert any("/v2/resolve must remain unmounted" in error for error in report["errors"])


def test_evidence_manifest_fails_if_boundary_safety_drifts(tmp_path: Path) -> None:
    paths = _write_manifest_inputs(tmp_path)
    boundary = json.loads(paths["boundary"].read_text(encoding="utf-8"))
    boundary["safety_invariants"]["no_neo4j_writes"] = False
    _write_json(paths["boundary"], boundary)

    report = run_shadow_evidence_manifest(repo_root=tmp_path, run_id="TEST_MANIFEST")

    assert report["ok"] is False
    assert report["safety_invariants"]["boundary_audit_safety_green"] is False


def test_evidence_manifest_fails_if_report_api_hash_is_stale(tmp_path: Path) -> None:
    paths = _write_manifest_inputs(tmp_path)
    route_inventory = json.loads(paths["route_inventory"].read_text(encoding="utf-8"))
    route_inventory["input_file_hashes_sha256"]["api_index"] = "0" * 64
    _write_json(paths["route_inventory"], route_inventory)

    report = run_shadow_evidence_manifest(repo_root=tmp_path, run_id="TEST_MANIFEST")

    assert report["ok"] is False
    assert report["safety_invariants"]["all_artifacts_ok"] is False
    assert any("route_inventory_report.input_file_hashes_sha256.api_index" in error for error in report["errors"])


def test_evidence_manifest_fails_if_input_report_commit_heads_diverge(tmp_path: Path) -> None:
    paths = _write_manifest_inputs(tmp_path)
    boundary = json.loads(paths["boundary"].read_text(encoding="utf-8"))
    boundary["repo_state"]["git_head_commit"] = "def456"
    _write_json(paths["boundary"], boundary)

    report = run_shadow_evidence_manifest(repo_root=tmp_path, run_id="TEST_MANIFEST")

    assert report["ok"] is False
    assert report["safety_invariants"]["all_artifacts_ok"] is False
    assert any("repo_state.git_head_commit values must match" in error for error in report["errors"])


def test_evidence_manifest_fails_if_input_report_source_tree_is_dirty(tmp_path: Path) -> None:
    paths = _write_manifest_inputs(tmp_path)
    boundary = json.loads(paths["boundary"].read_text(encoding="utf-8"))
    boundary["repo_state"]["source_working_tree_dirty"] = True
    boundary["repo_state"]["source_dirty_path_count"] = 1
    _write_json(paths["boundary"], boundary)

    report = run_shadow_evidence_manifest(repo_root=tmp_path, run_id="TEST_MANIFEST")

    assert report["ok"] is False
    assert report["safety_invariants"]["all_artifacts_ok"] is False
    assert any("boundary_audit_report.repo_state.source_working_tree_dirty" in error for error in report["errors"])


def test_evidence_manifest_rejects_output_outside_report_root(tmp_path: Path) -> None:
    _write_manifest_inputs(tmp_path)

    with pytest.raises(ValueError, match="evidence manifest report directory"):
        run_shadow_evidence_manifest(
            repo_root=tmp_path,
            run_id="TEST_MANIFEST",
            output_path=Path(".ai/ACTIVE_WORK.md"),
        )


def test_evidence_manifest_rejects_output_for_other_run_id(tmp_path: Path) -> None:
    _write_manifest_inputs(tmp_path)

    with pytest.raises(ValueError, match="current evidence manifest run id"):
        run_shadow_evidence_manifest(
            repo_root=tmp_path,
            run_id="TEST_MANIFEST",
            output_path=(
                Path("006_System-Manifests")
                / "aec-mepfs-backbone"
                / "evidence-manifest"
                / "OTHER"
                / "shadow-evidence-manifest-report.json"
            ),
        )


def test_evidence_manifest_rejects_missing_required_file(tmp_path: Path) -> None:
    paths = _write_manifest_inputs(tmp_path)
    paths["resolver"].unlink()

    with pytest.raises(FileNotFoundError, match="resolver QA report not found"):
        run_shadow_evidence_manifest(repo_root=tmp_path, run_id="TEST_MANIFEST")
