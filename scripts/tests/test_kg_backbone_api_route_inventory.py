from __future__ import annotations

import json
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
        "checked": True,
        "missing_preview_routes": [],
        "preview_routes_present": 6,
        "preview_routes_required": 6,
        "resolve_route_mounted": False,
        "route_count": 7,
        "trace_route_mounted": False,
    }
    assert report["input_file_hashes_sha256"]["api_index"]
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
        "shadow_only": True,
    }


def test_inventory_ignores_comment_and_string_route_lookalikes(tmp_path: Path) -> None:
    api_index = _write_api_index(tmp_path, _valid_api_index())

    inventory = inventory_api_routes(api_index, root=tmp_path)

    assert inventory["resolveRouteMounted"] is False
    assert inventory["traceRouteMounted"] is False
    assert all(inventory["previewRoutesPresent"].values())
    assert {route["path"] for route in inventory["routes"]} == {
        "/health",
        "/v2/backbone",
        "/v2/backbone/node/:id",
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
    assert any("/v2/resolve must remain unmounted" in error for error in report["errors"])
    assert any("/v2/resolve/trace must remain unmounted" in error for error in report["errors"])


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
    }


def test_shadow_preview_route_boundary_summary_uses_path_objects(tmp_path: Path) -> None:
    api_index = _write_api_index(tmp_path, _valid_api_index())

    status = summarize_shadow_preview_route_boundaries(tmp_path)

    assert status["checked"] is True
    assert status["path"] == api_index.resolve()
    assert status["resolveRouteMounted"] is False
    assert status["traceRouteMounted"] is False
    assert all(status["previewRoutesPresent"].values())
    assert status["routeCount"] == 7
