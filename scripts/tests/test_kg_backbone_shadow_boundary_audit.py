from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from vitruvius.kg.backbone_shadow_boundary_audit import (
    REQUIRED_DISABLED_FEATURE_FLAGS,
    REQUIRED_PARITY_CATEGORIES,
    run_shadow_boundary_audit,
)


STAGING_RUN_ID = "TEST_STAGE"


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def _write_shadow_repo(tmp_path: Path) -> dict[str, Path]:
    config_path = tmp_path / "config" / "vitruvius.yaml"
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(
        "features:\n"
        + "".join(f"  {flag}: false\n" for flag in sorted(REQUIRED_DISABLED_FEATURE_FLAGS)),
        encoding="utf-8",
    )

    api_index = tmp_path / "api" / "index.ts"
    api_index.parent.mkdir(parents=True, exist_ok=True)
    api_index.write_text(
        "app.get('/v2/backbone', handler);\n"
        "app.get('/v2/backbone/taxonomy', handler);\n"
        "app.get('/v2/backbone/node/:id', handler);\n"
        "app.get('/v2/search', handler);\n"
        "app.get('/v2/sources/:source_id', handler);\n"
        "app.get('/v2/backbone/placement-qa', handler);\n",
        encoding="utf-8",
    )

    shadow_root = (
        tmp_path
        / "006_System-Manifests"
        / "aec-mepfs-backbone"
        / "shadow-staging"
        / STAGING_RUN_ID
    )
    graph_path = shadow_root / "shadow-backbone-graph.json"
    graph_counts = {"edges": 4, "max_depth": 2, "nodes": 7, "roots": 3}
    _write_json(
        graph_path,
        {
            "schema_version": "aec-bb-shadow-graph/v1",
            "status": "shadow_graph_staged",
            "run_id": STAGING_RUN_ID,
            "source_artifact_path": str(
                graph_path.parent / "shadow-backbone-staging.json"
            ),
            "counts": graph_counts,
            "nodes": [],
            "edges": [],
        },
    )

    consumer_path = shadow_root / "shadow-staging-consumer-report.json"
    _write_json(
        consumer_path,
        {
            "schema_version": "aec-bb-shadow-staging-consumer-report/v1",
            "ok": True,
            "run_id": STAGING_RUN_ID,
            "shadow_graph_path": str(graph_path.relative_to(tmp_path)),
            "shadow_graph_counts": graph_counts,
            "boundaries": {
                "api_explorer_cutover": False,
                "canonical_content_admission": False,
                "feature_flag_cutover": False,
                "file_backed_only": True,
                "graph_rebuild": False,
                "live_neo4j_writes": False,
                "protected_content_ingest": False,
                "shadow_only": True,
            },
            "no_ingest_boundary_coverage": {
                "content_ingest_source_count": 0,
                "content_ingest_source_ids": [],
                "explicit_no_ingest_source_count": 29,
                "missing_explicit_block_count": 0,
                "missing_explicit_block_source_ids": [],
                "sources_total": 29,
            },
        },
    )

    placement_path = (
        tmp_path
        / "006_System-Manifests"
        / "aec-mepfs-backbone"
        / "placement-qa"
        / "TEST_PLACEMENT"
        / "placement-qa-report.json"
    )
    _write_json(
        placement_path,
        _qa_report(
            "aec-bb-placement-qa-report/v1",
            {"cases_passed": 3, "cases_total": 3},
        ),
    )

    resolver_path = (
        tmp_path
        / "006_System-Manifests"
        / "aec-mepfs-backbone"
        / "resolver-qa"
        / "TEST_RESOLVER"
        / "resolver-qa-report.json"
    )
    resolver_report = _qa_report(
        "aec-bb-resolver-qa-report/v1",
        {"cases_passed": 4, "cases_total": 4},
    )
    resolver_report["safety_boundaries"]["live_resolver_invocation"] = False
    resolver_report["safety_boundaries"]["llm_hot_path"] = False
    resolver_report["api_route_status"] = {
        "checked": True,
        "path": "api/index.ts",
        "resolveRouteMounted": False,
        "traceRouteMounted": False,
    }
    _write_json(resolver_path, resolver_report)

    parity_path = (
        tmp_path
        / "006_System-Manifests"
        / "aec-mepfs-backbone"
        / "parity"
        / "TEST_PARITY"
        / "api-explorer-parity-report.json"
    )
    _write_json(
        parity_path,
        {
            "schema_version": "aec-bb-parity-report/v1",
            "ok": True,
            "run_id": "TEST_PARITY",
            "commands_run": 6,
            "commands_passed": 6,
            "cases_declared": 24,
            "cases_passed": 24,
            "required_case_categories": sorted(REQUIRED_PARITY_CATEGORIES),
        },
    )

    return {
        "consumer": consumer_path,
        "placement": placement_path,
        "resolver": resolver_path,
        "parity": parity_path,
        "config": config_path,
        "api_index": api_index,
    }


def _qa_report(schema_version: str, summary: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": schema_version,
        "ok": True,
        "run_id": "TEST_QA",
        "summary": summary,
        "safety_boundaries": {
            "canonical_content_admission": False,
            "explorer_default_adoption": False,
            "feature_flag_cutover": False,
            "file_backed_only": True,
            "kg_rebuild": False,
            "live_neo4j_writes": False,
            "protected_content_ingest": False,
            "shadow_only": True,
        },
    }


def _run(tmp_path: Path, paths: dict[str, Path]) -> dict[str, Any]:
    return run_shadow_boundary_audit(
        repo_root=tmp_path,
        run_id="TEST_AUDIT",
        consumer_report_path=paths["consumer"].relative_to(tmp_path),
        placement_qa_report_path=paths["placement"].relative_to(tmp_path),
        resolver_qa_report_path=paths["resolver"].relative_to(tmp_path),
        parity_report_path=paths["parity"].relative_to(tmp_path),
        config_path=paths["config"].relative_to(tmp_path),
        api_index_path=paths["api_index"].relative_to(tmp_path),
    )


def test_shadow_boundary_audit_writes_report_for_valid_shadow_evidence(
    tmp_path: Path,
) -> None:
    paths = _write_shadow_repo(tmp_path)

    report = _run(tmp_path, paths)

    saved = json.loads(
        (
            tmp_path
            / "006_System-Manifests"
            / "aec-mepfs-backbone"
            / "boundary-audit"
            / "TEST_AUDIT"
            / "shadow-boundary-audit-report.json"
        ).read_text(encoding="utf-8")
    )
    assert saved == report
    assert report["ok"] is True
    assert report["summary"]["checks_total"] == 10
    assert report["summary"]["checks_passed"] == 10
    assert report["summary"]["shadow_graph_counts"] == {
        "edges": 4,
        "max_depth": 2,
        "nodes": 7,
        "roots": 3,
    }
    assert all(report["safety_invariants"].values())
    assert report["api_route_status"]["resolveRouteMounted"] is False
    assert report["api_route_status"]["traceRouteMounted"] is False
    assert set(report["input_file_hashes_sha256"]) == {
        "api_index",
        "config",
        "consumer_report",
        "parity_report",
        "placement_qa_report",
        "resolver_qa_report",
        "shadow_graph",
    }
    assert len(report["input_file_hashes_sha256"]["consumer_report"]) == 64
    assert report["repo_state"] == {
        "git_head_commit": None,
        "working_tree_dirty": False,
    }


def test_shadow_boundary_audit_fails_if_shadow_read_flag_is_enabled(
    tmp_path: Path,
) -> None:
    paths = _write_shadow_repo(tmp_path)
    paths["config"].write_text(
        "features:\n"
        + "".join(
            f"  {flag}: {'true' if flag == 'k_shadow_read' else 'false'}\n"
            for flag in sorted(REQUIRED_DISABLED_FEATURE_FLAGS)
        ),
        encoding="utf-8",
    )

    report = _run(tmp_path, paths)

    assert report["ok"] is False
    assert report["safety_invariants"]["no_feature_flag_cutover"] is False
    assert any("k_shadow_read must remain false" in error for error in report["errors"])


def test_shadow_boundary_audit_fails_if_resolver_route_is_mounted(
    tmp_path: Path,
) -> None:
    paths = _write_shadow_repo(tmp_path)
    paths["api_index"].write_text(
        paths["api_index"].read_text(encoding="utf-8")
        + "app.post('/v2/resolve', handler);\n"
        + "app.get('/v2/resolve/trace/:trace_id', handler);\n",
        encoding="utf-8",
    )

    report = _run(tmp_path, paths)

    assert report["ok"] is False
    assert report["safety_invariants"]["no_resolver_route_mounting"] is False
    assert any("/v2/resolve must remain unmounted" in error for error in report["errors"])


def test_shadow_boundary_audit_fails_if_neo4j_boundary_drifts(
    tmp_path: Path,
) -> None:
    paths = _write_shadow_repo(tmp_path)
    consumer = json.loads(paths["consumer"].read_text(encoding="utf-8"))
    consumer["boundaries"]["live_neo4j_writes"] = True
    _write_json(paths["consumer"], consumer)

    report = _run(tmp_path, paths)

    assert report["ok"] is False
    assert report["safety_invariants"]["no_neo4j_writes"] is False
    assert any("live_neo4j_writes must be false" in error for error in report["errors"])


def test_shadow_boundary_audit_fails_if_protected_content_ingest_appears(
    tmp_path: Path,
) -> None:
    paths = _write_shadow_repo(tmp_path)
    consumer = json.loads(paths["consumer"].read_text(encoding="utf-8"))
    consumer["no_ingest_boundary_coverage"]["content_ingest_source_count"] = 1
    consumer["no_ingest_boundary_coverage"]["content_ingest_source_ids"] = ["SRC-TEST"]
    _write_json(paths["consumer"], consumer)

    report = _run(tmp_path, paths)

    assert report["ok"] is False
    assert report["safety_invariants"]["no_protected_content_ingest"] is False
    assert any("protected content ingest count must remain 0" in error for error in report["errors"])


def test_shadow_boundary_audit_fails_if_parity_categories_drift(
    tmp_path: Path,
) -> None:
    paths = _write_shadow_repo(tmp_path)
    parity = json.loads(paths["parity"].read_text(encoding="utf-8"))
    parity["required_case_categories"] = [
        category
        for category in parity["required_case_categories"]
        if category != "shadow_preview_opt_in_isolation"
    ]
    _write_json(paths["parity"], parity)

    report = _run(tmp_path, paths)

    assert report["ok"] is False
    assert report["safety_invariants"]["no_explorer_default_adoption"] is False
    assert any("missing required shadow boundary categories" in error for error in report["errors"])


def test_shadow_boundary_audit_fails_if_qa_schema_version_drifts(
    tmp_path: Path,
) -> None:
    paths = _write_shadow_repo(tmp_path)
    placement = json.loads(paths["placement"].read_text(encoding="utf-8"))
    placement["schema_version"] = "old-schema"
    _write_json(paths["placement"], placement)

    report = _run(tmp_path, paths)

    assert report["ok"] is False
    assert any("placement_qa: unexpected schema_version" in error for error in report["errors"])


def test_shadow_boundary_audit_fails_if_api_index_is_missing(
    tmp_path: Path,
) -> None:
    paths = _write_shadow_repo(tmp_path)
    paths["api_index"].unlink()

    report = _run(tmp_path, paths)

    assert report["ok"] is False
    assert any("api routes: api index must be checked" in error for error in report["errors"])
    assert any("file backing: api_index must exist" in error for error in report["errors"])


def test_shadow_boundary_audit_fails_if_config_yaml_is_malformed(
    tmp_path: Path,
) -> None:
    paths = _write_shadow_repo(tmp_path)
    paths["config"].write_text("features: [not: valid", encoding="utf-8")

    report = _run(tmp_path, paths)

    assert report["ok"] is False
    assert any("feature flags: config YAML must parse" in error for error in report["errors"])


def test_shadow_boundary_audit_fails_if_live_and_cached_route_status_disagree(
    tmp_path: Path,
) -> None:
    paths = _write_shadow_repo(tmp_path)
    resolver = json.loads(paths["resolver"].read_text(encoding="utf-8"))
    resolver["api_route_status"]["resolveRouteMounted"] = True
    _write_json(paths["resolver"], resolver)

    report = _run(tmp_path, paths)

    assert report["ok"] is False
    assert report["safety_invariants"]["no_resolver_route_mounting"] is False
    assert any("live API resolveRouteMounted != resolver QA" in error for error in report["errors"])


def test_shadow_boundary_audit_rejects_unsafe_run_id(tmp_path: Path) -> None:
    paths = _write_shadow_repo(tmp_path)

    with pytest.raises(ValueError, match="run_id must contain only"):
        run_shadow_boundary_audit(
            repo_root=tmp_path,
            run_id="../unsafe",
            consumer_report_path=paths["consumer"].relative_to(tmp_path),
            placement_qa_report_path=paths["placement"].relative_to(tmp_path),
            resolver_qa_report_path=paths["resolver"].relative_to(tmp_path),
            parity_report_path=paths["parity"].relative_to(tmp_path),
        )


def test_shadow_boundary_audit_rejects_output_outside_report_root(
    tmp_path: Path,
) -> None:
    paths = _write_shadow_repo(tmp_path)

    with pytest.raises(ValueError, match="boundary audit report directory"):
        run_shadow_boundary_audit(
            repo_root=tmp_path,
            run_id="TEST_AUDIT",
            output_path=Path(".ai/ACTIVE_WORK.md"),
            consumer_report_path=paths["consumer"].relative_to(tmp_path),
            placement_qa_report_path=paths["placement"].relative_to(tmp_path),
            resolver_qa_report_path=paths["resolver"].relative_to(tmp_path),
            parity_report_path=paths["parity"].relative_to(tmp_path),
        )


def test_shadow_boundary_audit_rejects_graph_path_outside_repo_root(
    tmp_path: Path,
) -> None:
    paths = _write_shadow_repo(tmp_path)
    consumer = json.loads(paths["consumer"].read_text(encoding="utf-8"))
    consumer["shadow_graph_path"] = str(tmp_path.parent / "shadow-backbone-graph.json")
    _write_json(paths["consumer"], consumer)

    with pytest.raises(ValueError, match="shadow graph path must stay inside repo root"):
        _run(tmp_path, paths)
