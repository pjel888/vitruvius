"""Explorer default-adoption preflight reporter for AEC-MEPFS.

The reporter proves current Explorer behavior remains legacy-default and AEC
preview-only. It performs static source checks and writes an auditable report; it
does not call APIs, mutate graph state, query Neo4j, or change feature flags.
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import re
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Sequence

from vitruvius.kg.backbone_api_route_inventory import (
    REQUIRED_PREVIEW_ROUTES,
    inventory_api_routes,
)


REPORT_SCHEMA_VERSION = "aec-mepfs-explorer-default-adoption-preflight/v1"
REPORT_ROOT = Path("006_System-Manifests/aec-mepfs-backbone/explorer-default-adoption")
REPORT_FILENAME = "explorer-default-adoption-report.json"
RUN_ID_RE = re.compile(r"^[A-Za-z0-9_.-]+$")

DEFAULT_SOURCE_PATHS = {
    "app": Path("explorer/src/App.tsx"),
    "scene_store": Path("explorer/src/stores/useSceneStore.ts"),
    "home_screen": Path("explorer/src/components/HomeScreen.tsx"),
    "explorer_rail": Path("explorer/src/components/ExplorerRail.tsx"),
    "graph_api": Path("explorer/src/api/graphApi.ts"),
    "api_index": Path("api/index.ts"),
}

BACKBONE_FETCH_RE = re.compile(
    r"\bgetBackbone(?:Summary|TaxonomyPreview|PlacementQaPreview|EvidencePreview)\s*\("
)
DEFAULT_ON_FLAG_RE = re.compile(
    r"(?:default[-_ ]?on|DEFAULT_ON|VITE_[A-Z0-9_]*AEC[A-Z0-9_]*\s*={1,3}\s*true)",
    re.IGNORECASE,
)
NEO4J_MUTATION_PATTERNS = {
    "detach_delete": re.compile(r"\bDETACH\s+DELETE\b", re.IGNORECASE),
    "drop_database": re.compile(r"\bDROP\s+DATABASE\b", re.IGNORECASE),
    "create_or_replace": re.compile(r"\bCREATE\s+OR\s+REPLACE\b", re.IGNORECASE),
    "neo4j_loader": re.compile(r"\bNeo4jLoader\b"),
    "write_transaction": re.compile(r"\b(?:writeTransaction|executeWrite)\b"),
}
KG_REBUILD_PATTERNS = {
    "run_kg_pipeline": re.compile(r"\brun-kg-pipeline\b"),
    "reset_flag": re.compile(r"(?<![A-Za-z0-9_])--reset(?![A-Za-z0-9_])"),
    "reload_flag": re.compile(r"(?<![A-Za-z0-9_])--reload(?![A-Za-z0-9_])"),
    "kg_rebuild_phrase": re.compile(r"\bKG\s+(?:rebuild|reload|reset)\b", re.IGNORECASE),
}
PROTECTED_EXPOSURE_PATTERNS = {
    "protected_payload": re.compile(r"\bprotected(?:Payload|SourceText)\b"),
    "protected_text": re.compile(
        r"\bprotected\s+(?:source\s+)?(?:text|table|figure|dataset|clause)s?\b",
        re.IGNORECASE,
    ),
    "raw_protected_fields": re.compile(r"\b(?:clauseText|tableData|figureData|protectedText)\b"),
}


def run_explorer_default_adoption_preflight(
    *,
    repo_root: str | Path | None = None,
    run_id: str | None = None,
    output_path: str | Path | None = None,
    source_paths: dict[str, str | Path] | None = None,
) -> dict[str, Any]:
    """Run static Explorer default-adoption preflight checks."""

    root = _repo_root(repo_root)
    resolved_run_id = _run_id(run_id)
    report_path = _resolve_report_path(root, resolved_run_id, Path(output_path) if output_path else None)
    paths = {
        label: _resolve_existing_file(root, Path(value), label)
        for label, value in (source_paths or DEFAULT_SOURCE_PATHS).items()
    }
    source = {label: path.read_text(encoding="utf-8") for label, path in paths.items()}

    api_inventory = inventory_api_routes(paths["api_index"], root=root)
    preview_routes_present = api_inventory["previewRoutesPresent"]
    preview_routes_missing = [
        name for name, present in preview_routes_present.items() if present is not True
    ]
    checks = {
        "store_default_perspective_is_default": bool(
            re.search(r"perspectiveId\s*:\s*['\"]default['\"]", source["scene_store"])
        ),
        "explore_url_fallback_is_default": bool(
            re.search(
                r"params\.get\(\s*['\"]perspective['\"]\s*\)\s*\|\|\s*['\"]default['\"]",
                source["app"],
            )
        ),
        "default_perspective_omitted_from_url": bool(
            re.search(r"perspectiveId\s*!==\s*['\"]default['\"]", source["app"])
        ),
        "explore_loads_current_perspective_graph": bool(
            re.search(r"getNodesForPerspective\(\s*perspectiveId\s*\)", source["app"])
        ),
        "home_show_sample_graph_uses_default": bool(
            re.search(r"onClick=\{\(\)\s*=>\s*enterExplore\(['\"]default['\"]\)\}", source["home_screen"])
        ),
        "home_all_knowledge_uses_default": (
            'title="All Knowledge"' in source["home_screen"]
            and bool(
                re.search(
                    r"onClick=\{\(\)\s*=>\s*enterExplore\(['\"]default['\"]\)\}",
                    source["home_screen"],
                )
            )
        ),
        "backbone_preview_toggle_default_false": bool(
            re.search(r"showBackbonePreview[^\n=]*=\s*useState\(\s*false\s*\)", source["explorer_rail"])
        )
        or (
            "showBackbonePreview" in source["explorer_rail"]
            and bool(re.search(r"useState\(\s*false\s*\)", source["explorer_rail"]))
        ),
        "backbone_summary_fetch_limited_to_rail": (
            "getBackboneSummary" in source["explorer_rail"]
            and "getBackboneSummary" not in source["app"]
            and "getBackboneSummary" not in source["home_screen"]
        ),
        "backbone_preview_routes_are_v2_only": (
            "/v2/backbone" in source["graph_api"]
            and "/perspective/default/nodes" not in source["graph_api"]
        ),
        "api_preview_routes_remain_present": not preview_routes_missing,
        "api_resolver_routes_remain_default_off_guarded": (
            api_inventory["resolveRouteMounted"] is False
            and api_inventory["traceRouteMounted"] is False
            and api_inventory["resolverRoutePolicy"] in {"absent", "guarded_default_off"}
        ),
    }
    safety_evidence = _derive_safety_evidence(source, api_inventory)
    default_checks = {
        "store_default_perspective_is_default",
        "explore_url_fallback_is_default",
        "default_perspective_omitted_from_url",
        "home_show_sample_graph_uses_default",
        "home_all_knowledge_uses_default",
    }
    safety_invariants = {
        "neo4jMutation": bool(safety_evidence["neo4j_mutation_matches"]),
        "kgRebuild": bool(safety_evidence["kg_rebuild_matches"]),
        "protectedContentExposure": bool(safety_evidence["protected_content_exposure_matches"]),
        "automaticPreviewFetch": (
            bool(safety_evidence["automatic_preview_fetch_matches"])
            or checks["backbone_summary_fetch_limited_to_rail"] is not True
        ),
        "silentDefaultSwitch": any(checks[name] is not True for name in default_checks),
        "defaultOnFeatureFlag": bool(safety_evidence["default_on_feature_flag_matches"]),
        "explorerDefaultAdoptionEnabled": any(checks[name] is not True for name in default_checks),
    }
    missing = [name for name, passed in checks.items() if not passed]
    safety_errors = [
        f"safety invariant violated: {name}"
        for name, violated in safety_invariants.items()
        if violated
    ]

    report = {
        "schema_version": REPORT_SCHEMA_VERSION,
        "ok": not missing and not safety_errors,
        "run_id": resolved_run_id,
        "generated_at_utc": _utc_now(),
        "report_path": _relative_to_root(report_path, root),
        "authority": {
            "packet": ".ai/03_plans/AEC-MEPFS-Backbone/2026-04-27_explorer_default_adoption_packet.md",
            "scope": "explorer_default_adoption_preflight_only",
            "global_live_authorization": False,
        },
        "status": {
            "explorerDefaultAdoptionEnabled": False,
            "defaultAdoptionReady": False,
            "currentDefaultPerspective": "default",
            "aecBackbonePreviewMode": "explicit_user_opt_in",
            "nextRequiredImplementation": "graph_adapter_plus_selector_escape_path_packet",
        },
        "checks": checks,
        "api_route_inventory": {
            "path": api_inventory["path"],
            "routeCount": api_inventory["routeCount"],
            "previewRoutesRequired": REQUIRED_PREVIEW_ROUTES,
            "previewRoutesPresent": preview_routes_present,
            "previewRoutesMissing": preview_routes_missing,
            "resolverRoutePolicy": api_inventory["resolverRoutePolicy"],
            "resolveRouteMounted": api_inventory["resolveRouteMounted"],
            "traceRouteMounted": api_inventory["traceRouteMounted"],
            "defaultOffResolveRouteDeclared": api_inventory["defaultOffResolveRouteDeclared"],
            "defaultOffTraceRouteDeclared": api_inventory["defaultOffTraceRouteDeclared"],
        },
        "source_paths": {label: _relative_to_root(path, root) for label, path in paths.items()},
        "rollback": {
            "current_packet_changes_behavior": False,
            "rollback_procedure": "git revert this prep commit; no data or graph rollback required",
            "escape_path_required_for_future_adoption": True,
        },
        "safety_invariants": safety_invariants,
        "safety_evidence": safety_evidence,
        "errors": [f"check failed: {name}" for name in missing] + safety_errors,
        "environment": {
            "python_version": platform.python_version(),
            "platform": platform.platform(),
            "cpu_count": os.cpu_count(),
        },
    }
    _write_json(report_path, report)
    return report


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate AEC-MEPFS Explorer default-adoption preflight evidence."
    )
    parser.add_argument("--repo-root", default=None)
    parser.add_argument("--run-id", default=None)
    parser.add_argument("--output", default=None)
    args = parser.parse_args(argv)

    try:
        report = run_explorer_default_adoption_preflight(
            repo_root=args.repo_root,
            run_id=args.run_id,
            output_path=args.output,
        )
    except (FileNotFoundError, ValueError) as exc:
        print(json.dumps({"ok": False, "errors": [str(exc)]}, indent=2, sort_keys=True))
        return 1

    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["ok"] else 1


def _repo_root(value: str | Path | None) -> Path:
    if value is not None:
        return Path(value).resolve()
    return Path(__file__).resolve().parents[3]


def _resolve_existing_file(root: Path, value: Path, label: str) -> Path:
    path = value.resolve() if value.is_absolute() else (root / value).resolve()
    try:
        path.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"{label} path must stay inside repo root") from exc
    if not path.is_file():
        raise FileNotFoundError(f"{label} not found: {path}")
    return path


def _resolve_report_path(root: Path, run_id: str, output_path: Path | None) -> Path:
    candidate = output_path or (REPORT_ROOT / run_id / REPORT_FILENAME)
    report_path = candidate.resolve() if candidate.is_absolute() else (root / candidate).resolve()
    allowed_root = (root / REPORT_ROOT).resolve()
    try:
        relative_parts = report_path.relative_to(allowed_root).parts
    except ValueError as exc:
        raise ValueError("report path must stay inside the explorer-default-adoption evidence directory") from exc
    if len(relative_parts) != 2 or relative_parts[0] != run_id:
        raise ValueError("report path must be scoped to the current Explorer default-adoption run id")
    if relative_parts[1] != REPORT_FILENAME:
        raise ValueError(f"report filename must be {REPORT_FILENAME}")
    return report_path


def _run_id(value: str | None) -> str:
    candidate = value or datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    if not RUN_ID_RE.fullmatch(candidate):
        raise ValueError("run_id must contain only letters, digits, underscore, dot, or dash")
    return candidate


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _derive_safety_evidence(
    source: dict[str, str],
    api_inventory: dict[str, Any],
) -> dict[str, Any]:
    default_on_sources = {
        label: text for label, text in source.items() if label in {"app", "home_screen", "explorer_rail"}
    }
    preview_autofetch_sources = {
        label: text for label, text in source.items() if label in {"app", "home_screen"}
    }
    backend_sources = {
        label: text for label, text in source.items() if label in {"api_index", "graph_api"}
    }
    all_sources = dict(source)
    return {
        "neo4j_mutation_matches": _pattern_matches(backend_sources, NEO4J_MUTATION_PATTERNS),
        "kg_rebuild_matches": _pattern_matches(all_sources, KG_REBUILD_PATTERNS),
        "protected_content_exposure_matches": _pattern_matches(all_sources, PROTECTED_EXPOSURE_PATTERNS),
        "automatic_preview_fetch_matches": _regex_matches(
            preview_autofetch_sources,
            BACKBONE_FETCH_RE,
            "backbone_preview_fetch_outside_opt_in_rail",
        ),
        "default_on_feature_flag_matches": _regex_matches(
            default_on_sources,
            DEFAULT_ON_FLAG_RE,
            "default_on_aec_feature_flag",
        ),
        "api_route_policy": {
            "resolverRoutePolicy": api_inventory["resolverRoutePolicy"],
            "resolveRouteMounted": api_inventory["resolveRouteMounted"],
            "traceRouteMounted": api_inventory["traceRouteMounted"],
        },
    }


def _pattern_matches(
    sources: dict[str, str],
    patterns: dict[str, re.Pattern[str]],
) -> list[dict[str, Any]]:
    matches: list[dict[str, Any]] = []
    for pattern_name, pattern in patterns.items():
        matches.extend(_regex_matches(sources, pattern, pattern_name))
    return matches


def _regex_matches(
    sources: dict[str, str],
    pattern: re.Pattern[str],
    pattern_name: str,
) -> list[dict[str, Any]]:
    matches: list[dict[str, Any]] = []
    for label, text in sources.items():
        for line_number, line in enumerate(text.splitlines(), start=1):
            if pattern.search(line):
                matches.append(
                    {
                        "source": label,
                        "line": line_number,
                        "pattern": pattern_name,
                        "excerpt": line.strip()[:160],
                    }
                )
    return matches


def _relative_to_root(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def _utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
