from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from vitruvius.kg.backbone_explorer_default_adoption import (
    REPORT_FILENAME,
    run_explorer_default_adoption_preflight,
)


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _source_files(tmp_path: Path) -> dict[str, Path]:
    paths = {
        "app": tmp_path / "explorer/src/App.tsx",
        "scene_store": tmp_path / "explorer/src/stores/useSceneStore.ts",
        "home_screen": tmp_path / "explorer/src/components/HomeScreen.tsx",
        "explorer_rail": tmp_path / "explorer/src/components/ExplorerRail.tsx",
        "graph_api": tmp_path / "explorer/src/api/graphApi.ts",
        "api_index": tmp_path / "api/index.ts",
    }
    _write(
        paths["app"],
        "const urlPerspective = params.get('perspective') || 'default';\n"
        "if (perspectiveId && perspectiveId !== 'default') params.set('perspective', perspectiveId);\n"
        "const { nodes, edges } = await getNodesForPerspective(perspectiveId);\n",
    )
    _write(paths["scene_store"], "perspectiveId: 'default',\n")
    _write(
        paths["home_screen"],
        "<button onClick={() => enterExplore('default')}>Show sample graph</button>\n"
        "<PerspectiveCard title=\"All Knowledge\" onClick={() => enterExplore('default')} />\n",
    )
    _write(
        paths["explorer_rail"],
        "const [showBackbonePreview, setShowBackbonePreview] = useState(false);\n"
        "await getBackboneSummary();\n",
    )
    _write(paths["graph_api"], "export async function getBackboneSummary(){ return api('/v2/backbone'); }\n")
    _write(
        paths["api_index"],
        "app.get('/v2/backbone', handler);\n"
        "app.get('/v2/backbone/taxonomy', handler);\n"
        "app.get('/v2/backbone/node/:id', handler);\n"
        "app.get('/v2/backbone/placement-qa', handler);\n"
        "app.get('/v2/backbone/evidence', handler);\n"
        "app.get('/v2/search', handler);\n"
        "app.get('/v2/sources/:source_id', handler);\n",
    )
    return paths


def _run(tmp_path: Path, paths: dict[str, Path] | None = None) -> dict[str, Any]:
    source_paths = paths or _source_files(tmp_path)
    return run_explorer_default_adoption_preflight(
        repo_root=tmp_path,
        run_id="TEST_EXPLORER_DEFAULT",
        source_paths={label: path.relative_to(tmp_path) for label, path in source_paths.items()},
    )


def test_explorer_default_adoption_preflight_writes_no_behavior_change_report(tmp_path: Path) -> None:
    report = _run(tmp_path)

    saved_path = (
        tmp_path
        / "006_System-Manifests"
        / "aec-mepfs-backbone"
        / "explorer-default-adoption"
        / "TEST_EXPLORER_DEFAULT"
        / REPORT_FILENAME
    )
    saved = json.loads(saved_path.read_text(encoding="utf-8"))
    assert saved == report
    assert report["ok"] is True
    assert report["status"] == {
        "aecBackbonePreviewMode": "explicit_user_opt_in",
        "currentDefaultPerspective": "default",
        "defaultAdoptionReady": False,
        "explorerDefaultAdoptionEnabled": False,
        "nextRequiredImplementation": "graph_adapter_plus_selector_escape_path_packet",
    }
    assert all(report["checks"].values())
    assert report["api_route_inventory"]["previewRoutesMissing"] == []
    assert report["api_route_inventory"]["resolverRoutePolicy"] == "absent"
    assert report["rollback"] == {
        "current_packet_changes_behavior": False,
        "escape_path_required_for_future_adoption": True,
        "rollback_procedure": "git revert this prep commit; no data or graph rollback required",
    }
    assert report["safety_invariants"] == {
        "automaticPreviewFetch": False,
        "defaultOnFeatureFlag": False,
        "explorerDefaultAdoptionEnabled": False,
        "kgRebuild": False,
        "neo4jMutation": False,
        "protectedContentExposure": False,
        "silentDefaultSwitch": False,
    }
    assert report["safety_evidence"]["automatic_preview_fetch_matches"] == []
    assert report["safety_evidence"]["neo4j_mutation_matches"] == []


def test_explorer_default_adoption_preflight_fails_if_store_default_changes(tmp_path: Path) -> None:
    paths = _source_files(tmp_path)
    _write(paths["scene_store"], "perspectiveId: 'aec-mepfs',\n")

    report = _run(tmp_path, paths)

    assert report["ok"] is False
    assert report["checks"]["store_default_perspective_is_default"] is False
    assert "check failed: store_default_perspective_is_default" in report["errors"]


def test_explorer_default_adoption_preflight_fails_if_preview_autofetch_enters_app(tmp_path: Path) -> None:
    paths = _source_files(tmp_path)
    _write(
        paths["app"],
        "const urlPerspective = params.get('perspective') || 'default';\n"
        "if (perspectiveId && perspectiveId !== 'default') params.set('perspective', perspectiveId);\n"
        "const { nodes, edges } = await getNodesForPerspective(perspectiveId);\n"
        "await getBackboneSummary();\n",
    )

    report = _run(tmp_path, paths)

    assert report["ok"] is False
    assert report["checks"]["backbone_summary_fetch_limited_to_rail"] is False
    assert report["safety_invariants"]["automaticPreviewFetch"] is True
    assert "check failed: backbone_summary_fetch_limited_to_rail" in report["errors"]
    assert "safety invariant violated: automaticPreviewFetch" in report["errors"]


def test_explorer_default_adoption_preflight_fails_if_api_preview_route_missing(tmp_path: Path) -> None:
    paths = _source_files(tmp_path)
    _write(
        paths["api_index"],
        "app.get('/v2/backbone', handler);\n"
        "app.get('/v2/backbone/taxonomy', handler);\n"
        "app.get('/v2/backbone/node/:id', handler);\n"
        "app.get('/v2/backbone/placement-qa', handler);\n"
        "app.get('/v2/search', handler);\n"
        "app.get('/v2/sources/:source_id', handler);\n",
    )

    report = _run(tmp_path, paths)

    assert report["ok"] is False
    assert report["checks"]["api_preview_routes_remain_present"] is False
    assert report["api_route_inventory"]["previewRoutesMissing"] == ["evidence_preview"]
    assert "check failed: api_preview_routes_remain_present" in report["errors"]


def test_explorer_default_adoption_preflight_fails_on_default_on_feature_flag(tmp_path: Path) -> None:
    paths = _source_files(tmp_path)
    _write(
        paths["app"],
        "const urlPerspective = params.get('perspective') || 'default';\n"
        "if (perspectiveId && perspectiveId !== 'default') params.set('perspective', perspectiveId);\n"
        "const { nodes, edges } = await getNodesForPerspective(perspectiveId);\n"
        "const AEC_DEFAULT_ON = true;\n",
    )

    report = _run(tmp_path, paths)

    assert report["ok"] is False
    assert report["safety_invariants"]["defaultOnFeatureFlag"] is True
    assert "safety invariant violated: defaultOnFeatureFlag" in report["errors"]


def test_explorer_default_adoption_preflight_rejects_unsafe_run_id(tmp_path: Path) -> None:
    paths = _source_files(tmp_path)

    with pytest.raises(ValueError, match="run_id must contain only"):
        run_explorer_default_adoption_preflight(
            repo_root=tmp_path,
            run_id="../unsafe",
            source_paths={label: path.relative_to(tmp_path) for label, path in paths.items()},
        )


def test_explorer_default_adoption_preflight_rejects_output_outside_report_root(tmp_path: Path) -> None:
    paths = _source_files(tmp_path)

    with pytest.raises(ValueError, match="explorer-default-adoption evidence directory"):
        run_explorer_default_adoption_preflight(
            repo_root=tmp_path,
            run_id="TEST_EXPLORER_DEFAULT",
            output_path=Path("outside.json"),
            source_paths={label: path.relative_to(tmp_path) for label, path in paths.items()},
        )


def test_explorer_default_adoption_preflight_rejects_source_outside_repo_root(tmp_path: Path) -> None:
    paths = _source_files(tmp_path)
    outside = tmp_path.parent / f"outside-explorer-source-{tmp_path.name}.tsx"
    try:
        _write(outside, "perspectiveId: 'default'\n")
        with pytest.raises(ValueError, match="scene_store path must stay inside repo root"):
            run_explorer_default_adoption_preflight(
                repo_root=tmp_path,
                run_id="TEST_EXPLORER_DEFAULT",
                source_paths={**{label: path.relative_to(tmp_path) for label, path in paths.items()}, "scene_store": outside},
            )
    finally:
        outside.unlink(missing_ok=True)
