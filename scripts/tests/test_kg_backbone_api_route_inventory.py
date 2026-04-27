from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

import pytest

from vitruvius.kg.backbone_api_route_inventory import (
    inventory_api_routes,
    run_api_route_inventory,
    summarize_resolver_route_boundary,
    summarize_shadow_preview_route_boundaries,
)


def _write_api_index(tmp_path: Path, body: str) -> Path:
    path = tmp_path / "api" / "index.ts"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")
    return path


def _valid_api_index() -> str:
    return (
        "const ignored = \"app.post('/v2/resolve', handler)\";\n"
        "// app.post('/v2/resolve', handler);\n"
        "/* app.get('/v2/resolve/trace/:trace_id', handler); */\n"
        "app.get('/health', handler);\n"
        "app.get('/v2/backbone', handler);\n"
        "app.get('/v2/backbone/taxonomy', handler);\n"
        "app.get('/v2/backbone/node/:id', handler);\n"
        "app.get('/v2/search', handler);\n"
        "app.get('/v2/sources/:source_id', handler);\n"
        "app.get('/v2/backbone/placement-qa', handler);\n"
        "app.get('/v2/backbone/evidence', handler);\n"
    )


def test_route_inventory_writes_report_for_expected_preview_routes(tmp_path: Path) -> None:
    _write_api_index(tmp_path, _valid_api_index())

    report = run_api_route_inventory(repo_root=tmp_path, run_id="TEST_ROUTES")

    saved = json.loads(
        (
            tmp_path
            / "006_System-Manifests"
            / "aec-mepfs-backbone"
            / "api-route-inventory"
            / "TEST_ROUTES"
            / "api-route-inventory-report.json"
        ).read_text(encoding="utf-8")
    )
    assert saved == report
    assert report["ok"] is True
    assert report["summary"] == {
        "default_off_resolve_route_declared": False,
        "default_off_trace_route_declared": False,
        "guarded_resolve_route_count": 0,
        "checked": True,
        "missing_preview_routes": [],
        "preview_routes_present": 7,
        "preview_routes_required": 7,
        "resolve_route_declared": False,
        "resolve_route_mounted": False,
        "resolver_route_policy": "absent",
        "route_count": 8,
        "trace_route_declared": False,
        "trace_route_mounted": False,
        "unauthorized_resolve_route_count": 0,
    }
    assert report["api_route_status"]["forbiddenResolveRoutes"] == []
    assert report["api_route_status"]["guardedResolveRoutes"] == []
    assert report["input_file_hashes_sha256"]["api_index"]
    assert report["repo_state"] == {
        "generated_evidence_dirty": False,
        "generated_evidence_dirty_path_count": 0,
        "git_head_commit": None,
        "source_dirty_path_count": 0,
        "source_working_tree_dirty": False,
        "working_tree_dirty": False,
    }
    assert report["safety_boundaries"] == {
        "api_server_calls": False,
        "explorer_default_adoption": False,
        "explorer_runtime_calls": False,
        "feature_flag_cutover": False,
        "file_backed_only": True,
        "kg_rebuild": False,
        "live_neo4j_writes": False,
        "protected_content_ingest": False,
        "resolver_route_mounting": False,
        "resolver_route_default_off_guarded": False,
        "shadow_only": True,
    }


def test_route_inventory_splits_source_dirty_from_generated_evidence_dirty(
    tmp_path: Path,
) -> None:
    _write_api_index(tmp_path, _valid_api_index())
    subprocess.run(["git", "init"], cwd=tmp_path, check=True, capture_output=True, text=True)
    subprocess.run(["git", "add", "api/index.ts"], cwd=tmp_path, check=True)
    subprocess.run(
        [
            "git",
            "-c",
            "user.email=test@example.test",
            "-c",
            "user.name=Test User",
            "commit",
            "-m",
            "seed",
        ],
        cwd=tmp_path,
        check=True,
        capture_output=True,
        text=True,
    )
    generated = (
        tmp_path
        / "006_System-Manifests"
        / "aec-mepfs-backbone"
        / "parity"
        / "TEST"
        / "api-explorer-parity-report.json"
    )
    generated.parent.mkdir(parents=True)
    generated.write_text("{}", encoding="utf-8")
    source = tmp_path / ".ai" / "source-drift.md"
    source.parent.mkdir()
    source.write_text("drift", encoding="utf-8")

    report = run_api_route_inventory(repo_root=tmp_path, run_id="TEST_ROUTES")

    assert report["repo_state"]["working_tree_dirty"] is True
    assert report["repo_state"]["generated_evidence_dirty"] is True
    assert report["repo_state"]["generated_evidence_dirty_path_count"] == 1
    assert report["repo_state"]["source_working_tree_dirty"] is True
    assert report["repo_state"]["source_dirty_path_count"] == 1
    assert report["repo_state"]["working_tree_dirty"] == (
        report["repo_state"]["source_working_tree_dirty"]
        or report["repo_state"]["generated_evidence_dirty"]
    )


def test_inventory_ignores_comment_and_string_route_lookalikes(tmp_path: Path) -> None:
    api_index = _write_api_index(tmp_path, _valid_api_index())

    inventory = inventory_api_routes(api_index, root=tmp_path)

    assert inventory["resolveRouteMounted"] is False
    assert inventory["traceRouteMounted"] is False
    assert inventory["forbiddenResolveRoutes"] == []
    assert all(inventory["previewRoutesPresent"].values())
    assert {route["path"] for route in inventory["routes"]} == {
        "/health",
        "/v2/backbone",
        "/v2/backbone/node/:id",
        "/v2/backbone/evidence",
        "/v2/backbone/placement-qa",
        "/v2/backbone/taxonomy",
        "/v2/search",
        "/v2/sources/:source_id",
    }


def test_route_inventory_fails_if_resolver_routes_are_mounted(tmp_path: Path) -> None:
    _write_api_index(
        tmp_path,
        _valid_api_index()
        + "app.get('/v2/resolve', handler);\n"
        + "app.get('/v2/resolve/trace/:trace_id', handler);\n",
    )

    report = run_api_route_inventory(repo_root=tmp_path, run_id="TEST_ROUTES")

    assert report["ok"] is False
    assert report["summary"]["resolve_route_mounted"] is True
    assert report["summary"]["trace_route_mounted"] is True
    assert [route["path"] for route in report["api_route_status"]["forbiddenResolveRoutes"]] == [
        "/v2/resolve",
        "/v2/resolve/trace/:trace_id",
    ]
    assert any(
        "/v2/resolve must remain absent or default-off guarded" in error
        for error in report["errors"]
    )
    assert any(
        "/v2/resolve/trace must remain absent or default-off guarded" in error
        for error in report["errors"]
    )


def test_route_inventory_allows_default_off_guarded_resolver_routes(tmp_path: Path) -> None:
    _write_api_index(
        tmp_path,
        _valid_api_index()
        + "if (isAecMepfsResolverRuntimeEnabled()) {\n"
        + "  app.post('/v2/resolve', handler);\n"
        + "  app.get('/v2/resolve/trace/:trace_id', handler);\n"
        + "}\n",
    )

    report = run_api_route_inventory(repo_root=tmp_path, run_id="TEST_ROUTES")

    assert report["ok"] is True
    assert report["summary"]["resolve_route_mounted"] is False
    assert report["summary"]["trace_route_mounted"] is False
    assert report["summary"]["resolve_route_declared"] is True
    assert report["summary"]["trace_route_declared"] is True
    assert report["summary"]["default_off_resolve_route_declared"] is True
    assert report["summary"]["default_off_trace_route_declared"] is True
    assert report["summary"]["resolver_route_policy"] == "guarded_default_off"
    assert report["summary"]["guarded_resolve_route_count"] == 2
    assert report["summary"]["unauthorized_resolve_route_count"] == 0
    assert report["api_route_status"]["forbiddenResolveRoutes"] == []
    assert [route["path"] for route in report["api_route_status"]["guardedResolveRoutes"]] == [
        "/v2/resolve",
        "/v2/resolve/trace/:trace_id",
    ]
    assert all(
        route["guard"] == "VITRUVIUS_AEC_MEPFS_RESOLVER_RUNTIME"
        for route in report["api_route_status"]["guardedResolveRoutes"]
    )
    assert report["safety_boundaries"]["resolver_route_mounting"] is False
    assert report["safety_boundaries"]["resolver_route_default_off_guarded"] is True


def test_route_inventory_fails_if_resolver_child_route_is_mounted(tmp_path: Path) -> None:
    _write_api_index(
        tmp_path,
        _valid_api_index() + "app.post('/v2/resolve/context', handler);\n",
    )

    report = run_api_route_inventory(repo_root=tmp_path, run_id="TEST_ROUTES")

    assert report["ok"] is False
    assert report["summary"]["resolve_route_mounted"] is True
    assert report["summary"]["trace_route_mounted"] is False
    assert [route["path"] for route in report["api_route_status"]["forbiddenResolveRoutes"]] == [
        "/v2/resolve/context",
    ]
    assert any(
        "/v2/resolve must remain absent or default-off guarded" in error
        for error in report["errors"]
    )


def test_route_inventory_fails_if_preview_route_is_missing(tmp_path: Path) -> None:
    _write_api_index(
        tmp_path,
        _valid_api_index().replace("app.get('/v2/search', handler);\n", ""),
    )

    report = run_api_route_inventory(repo_root=tmp_path, run_id="TEST_ROUTES")

    assert report["ok"] is False
    assert report["summary"]["missing_preview_routes"] == ["search_preview"]


def test_route_inventory_rejects_unsafe_run_id(tmp_path: Path) -> None:
    _write_api_index(tmp_path, _valid_api_index())

    with pytest.raises(ValueError, match="run_id must contain only"):
        run_api_route_inventory(repo_root=tmp_path, run_id="../unsafe")


def test_route_inventory_rejects_output_outside_report_root(tmp_path: Path) -> None:
    _write_api_index(tmp_path, _valid_api_index())

    with pytest.raises(ValueError, match="route inventory report directory"):
        run_api_route_inventory(
            repo_root=tmp_path,
            run_id="TEST_ROUTES",
            output_path=Path(".ai/ACTIVE_WORK.md"),
        )


def test_route_inventory_rejects_output_for_other_run_id(tmp_path: Path) -> None:
    _write_api_index(tmp_path, _valid_api_index())

    with pytest.raises(ValueError, match="current route inventory run id"):
        run_api_route_inventory(
            repo_root=tmp_path,
            run_id="TEST_ROUTES",
            output_path=(
                Path("006_System-Manifests")
                / "aec-mepfs-backbone"
                / "api-route-inventory"
                / "OTHER"
                / "api-route-inventory-report.json"
            ),
        )


def test_route_inventory_reports_missing_api_index(tmp_path: Path) -> None:
    report = run_api_route_inventory(repo_root=tmp_path, run_id="TEST_ROUTES")

    assert report["ok"] is False
    assert report["summary"]["checked"] is False
    assert report["summary"]["missing_preview_routes"] == [
        "backbone_summary",
        "taxonomy_preview",
        "node_preview",
        "search_preview",
        "source_preview",
        "placement_qa_preview",
        "evidence_preview",
    ]
    assert report["input_file_hashes_sha256"]["api_index"] is None


def test_resolver_route_boundary_summary_preserves_existing_missing_file_shape(
    tmp_path: Path,
) -> None:
    assert summarize_resolver_route_boundary(tmp_path) == {
        "checked": False,
        "path": "api/index.ts",
        "reason": "api index file not present under repo root",
        "resolveRouteMounted": False,
        "traceRouteMounted": False,
        "resolveRouteDeclared": False,
        "traceRouteDeclared": False,
        "defaultOffResolveRouteDeclared": False,
        "defaultOffTraceRouteDeclared": False,
        "resolverRoutePolicy": "absent",
    }


def test_shadow_preview_route_boundary_summary_uses_path_objects(tmp_path: Path) -> None:
    api_index = _write_api_index(tmp_path, _valid_api_index())

    status = summarize_shadow_preview_route_boundaries(tmp_path)

    assert status["checked"] is True
    assert status["path"] == api_index.resolve()
    assert status["resolveRouteMounted"] is False
    assert status["traceRouteMounted"] is False
    assert status["resolveRouteDeclared"] is False
    assert status["traceRouteDeclared"] is False
    assert status["defaultOffResolveRouteDeclared"] is False
    assert status["defaultOffTraceRouteDeclared"] is False
    assert status["resolverRoutePolicy"] == "absent"
    assert all(status["previewRoutesPresent"].values())
    assert status["routeCount"] == 8
