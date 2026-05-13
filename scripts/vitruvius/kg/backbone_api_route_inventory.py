"""Static API route inventory for AEC-MEPFS Backbone shadow checks.

This module inventories direct Hono `app.<method>(...)` route declarations in
`api/index.ts`. It is file-backed and does not start the API server, call
Explorer, query Neo4j, rebuild KG artifacts, or promote shadow routes.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Sequence

from vitruvius.kg.backbone_repo_state import read_repo_state


REPORT_SCHEMA_VERSION = "aec-bb-api-route-inventory-report/v1"
API_ROUTE_INVENTORY_REPORT_ROOT = Path(
    "006_System-Manifests/aec-mepfs-backbone/api-route-inventory"
)
API_ROUTE_INVENTORY_REPORT_FILENAME = "api-route-inventory-report.json"
API_INDEX_PATH = Path("api/index.ts")
RUN_ID_RE = re.compile(r"^[A-Za-z0-9_.-]+$")
HIDDEN_ROUTE_METHODS = {"all", "delete", "get", "options", "patch", "post", "put"}
RESOLVER_RUNTIME_FLAG = "VITRUVIUS_AEC_MEPFS_RESOLVER_RUNTIME"
REQUIRED_PREVIEW_ROUTES = {
    "backbone_summary": "/v2/backbone",
    "taxonomy_preview": "/v2/backbone/taxonomy",
    "node_preview": "/v2/backbone/node/:id",
    "search_preview": "/v2/search",
    "source_preview": "/v2/sources/:source_id",
    "placement_qa_preview": "/v2/backbone/placement-qa",
    "evidence_preview": "/v2/backbone/evidence",
    "source_gap_workqueue_preview": "/v2/backbone/source-gap-workqueue",
}


def run_api_route_inventory(
    *,
    repo_root: str | Path | None = None,
    run_id: str | None = None,
    output_path: str | Path | None = None,
    api_index_path: str | Path = API_INDEX_PATH,
) -> dict[str, Any]:
    """Inventory direct API route declarations and write a JSON report."""
    root = _repo_root(repo_root)
    resolved_run_id = _run_id(run_id)
    started_at = _utc_now()
    api_index = _resolve_path_inside_root(root, Path(api_index_path), "api index")
    report_path = _resolve_report_path(
        root=root,
        run_id=resolved_run_id,
        output_path=Path(output_path) if output_path is not None else None,
    )

    errors: list[str] = []
    warnings: list[str] = []
    if not api_index.is_file():
        inventory = _missing_inventory(api_index, root)
        errors.append("api index file must exist for route inventory")
    else:
        inventory = inventory_api_routes(api_index, root=root)
        route_errors = _route_boundary_errors(inventory)
        errors.extend(route_errors)
        warnings.extend(inventory["warnings"])

    finished_at = _utc_now()
    report = {
        "schema_version": REPORT_SCHEMA_VERSION,
        "ok": not errors,
        "run_id": resolved_run_id,
        "started_at_utc": started_at,
        "finished_at_utc": finished_at,
        "report_path": _relative_to_root(report_path, root),
        "inputs": {
            "api_index": _relative_to_root(api_index, root),
        },
        "input_file_hashes_sha256": {
            "api_index": _hash_file(api_index) if api_index.is_file() else None,
        },
        "repo_state": read_repo_state(root),
        "summary": {
            "checked": inventory["checked"],
            "route_count": len(inventory["routes"]),
            "preview_routes_present": sum(
                1 for present in inventory["previewRoutesPresent"].values() if present
            ),
            "preview_routes_required": len(REQUIRED_PREVIEW_ROUTES),
            "missing_preview_routes": [
                name
                for name, present in inventory["previewRoutesPresent"].items()
                if not present
            ],
            "resolve_route_mounted": inventory["resolveRouteMounted"],
            "trace_route_mounted": inventory["traceRouteMounted"],
            "resolve_route_declared": inventory["resolveRouteDeclared"],
            "trace_route_declared": inventory["traceRouteDeclared"],
            "default_off_resolve_route_declared": inventory["defaultOffResolveRouteDeclared"],
            "default_off_trace_route_declared": inventory["defaultOffTraceRouteDeclared"],
            "default_on_resolve_route_declared": inventory["defaultOnResolveRouteDeclared"],
            "default_on_trace_route_declared": inventory["defaultOnTraceRouteDeclared"],
            "disabled_rollback_guard_declared": inventory["disabledRollbackGuardDeclared"],
            "guarded_resolve_route_count": len(inventory["guardedResolveRoutes"]),
            "unauthorized_resolve_route_count": len(inventory["forbiddenResolveRoutes"]),
            "resolver_route_policy": inventory["resolverRoutePolicy"],
        },
        "api_route_status": inventory,
        "safety_boundaries": {
            "shadow_only": True,
            "file_backed_only": True,
            "api_server_calls": False,
            "explorer_runtime_calls": False,
            "live_neo4j_writes": False,
            "kg_rebuild": False,
            "feature_flag_cutover": False,
            "explorer_default_adoption": False,
            "protected_content_ingest": False,
            "resolver_route_mounting": inventory["resolveRouteMounted"],
            "resolver_route_default_off_guarded": inventory["defaultOffResolveRouteDeclared"],
            "resolver_route_default_on": inventory["defaultOnResolveRouteDeclared"],
            "resolver_route_rollback_disable_flag": inventory["disabledRollbackGuardDeclared"],
        },
        "errors": sorted(set(errors)),
        "warnings": sorted(set(warnings)),
    }
    _write_json(report_path, report)
    return report


def inventory_api_routes(path: str | Path, *, root: str | Path | None = None) -> dict[str, Any]:
    """Return route inventory for direct Hono app route declarations."""
    repo_root = _repo_root(root) if root is not None else Path(path).resolve().parents[1]
    api_index = Path(path).resolve()
    text = api_index.read_text(encoding="utf-8")
    resolver_runtime_default_enabled = _resolver_runtime_default_enabled(text)
    routes = _extract_hono_routes(
        text,
        resolver_runtime_default_enabled=resolver_runtime_default_enabled,
    )
    resolver_routes = _resolver_routes(routes)
    guarded_resolver_routes = [
        route for route in resolver_routes if route.get("runtimeGuarded") is True
    ]
    unauthorized_resolver_routes = [
        route for route in resolver_routes if route.get("runtimeGuarded") is not True
    ]
    guarded_trace_routes = [
        route for route in guarded_resolver_routes if _is_trace_resolver_path(route["path"])
    ]
    unauthorized_trace_routes = [
        route for route in unauthorized_resolver_routes if _is_trace_resolver_path(route["path"])
    ]
    preview_routes_present = {
        name: _has_route(routes, "get", route)
        for name, route in REQUIRED_PREVIEW_ROUTES.items()
    }
    return {
        "checked": True,
        "path": _relative_to_root(api_index, repo_root),
        "routeCount": len(routes),
        "routes": routes,
        "forbiddenResolveRoutes": unauthorized_resolver_routes,
        "guardedResolveRoutes": guarded_resolver_routes,
        "resolveRouteDeclared": bool(resolver_routes),
        "traceRouteDeclared": bool(guarded_trace_routes or unauthorized_trace_routes),
        "defaultOffResolveRouteDeclared": bool(guarded_resolver_routes) and not resolver_runtime_default_enabled,
        "defaultOffTraceRouteDeclared": bool(guarded_trace_routes) and not resolver_runtime_default_enabled,
        "defaultOnResolveRouteDeclared": bool(guarded_resolver_routes) and resolver_runtime_default_enabled,
        "defaultOnTraceRouteDeclared": bool(guarded_trace_routes) and resolver_runtime_default_enabled,
        "disabledRollbackGuardDeclared": bool(guarded_resolver_routes) and resolver_runtime_default_enabled,
        "resolverRoutePolicy": _resolver_route_policy(
            resolver_routes=resolver_routes,
            unauthorized_resolver_routes=unauthorized_resolver_routes,
            guarded_resolver_routes=guarded_resolver_routes,
            resolver_runtime_default_enabled=resolver_runtime_default_enabled,
        ),
        "resolverRuntimeGuard": {
            "flag": RESOLVER_RUNTIME_FLAG,
            "defaultEnabled": resolver_runtime_default_enabled,
            "disabledValues": ["0", "false", "no", "off", "disabled"],
        },
        "resolveRouteMounted": (
            resolver_runtime_default_enabled
            and _has_forbidden_resolver_route(guarded_resolver_routes)
        ) or _has_forbidden_resolver_route(unauthorized_resolver_routes),
        "traceRouteMounted": (
            resolver_runtime_default_enabled
            and _has_forbidden_trace_route(guarded_resolver_routes)
        ) or _has_forbidden_trace_route(unauthorized_resolver_routes),
        "previewRoutesPresent": preview_routes_present,
        "warnings": [
            "route inventory scans direct Hono app.<method>(...) declarations in api/index.ts",
            (
                f"/v2/resolve* declarations must be wrapped by {RESOLVER_RUNTIME_FLAG} "
                "runtime policy with an explicit disable/rollback path"
            ),
        ],
    }


def summarize_resolver_route_boundary(
    root: str | Path,
    api_index_path: str | Path = API_INDEX_PATH,
) -> dict[str, Any]:
    """Return the resolver QA route-status shape used by existing reports."""
    repo_root = _repo_root(root)
    api_index = _resolve_path_inside_root(repo_root, Path(api_index_path), "api index")
    if not api_index.is_file():
        return {
            "checked": False,
            "path": Path(api_index_path).as_posix(),
            "resolveRouteMounted": False,
            "traceRouteMounted": False,
            "resolveRouteDeclared": False,
            "traceRouteDeclared": False,
            "defaultOffResolveRouteDeclared": False,
            "defaultOffTraceRouteDeclared": False,
            "defaultOnResolveRouteDeclared": False,
            "defaultOnTraceRouteDeclared": False,
            "disabledRollbackGuardDeclared": False,
            "resolverRoutePolicy": "absent",
            "reason": "api index file not present under repo root",
        }
    inventory = inventory_api_routes(api_index, root=repo_root)
    return {
        "checked": True,
        "path": Path(api_index_path).as_posix(),
        "resolveRouteMounted": inventory["resolveRouteMounted"],
        "traceRouteMounted": inventory["traceRouteMounted"],
        "resolveRouteDeclared": inventory["resolveRouteDeclared"],
        "traceRouteDeclared": inventory["traceRouteDeclared"],
        "defaultOffResolveRouteDeclared": inventory["defaultOffResolveRouteDeclared"],
        "defaultOffTraceRouteDeclared": inventory["defaultOffTraceRouteDeclared"],
        "defaultOnResolveRouteDeclared": inventory["defaultOnResolveRouteDeclared"],
        "defaultOnTraceRouteDeclared": inventory["defaultOnTraceRouteDeclared"],
        "disabledRollbackGuardDeclared": inventory["disabledRollbackGuardDeclared"],
        "resolverRoutePolicy": inventory["resolverRoutePolicy"],
    }


def summarize_shadow_preview_route_boundaries(
    root: str | Path,
    api_index_path: str | Path = API_INDEX_PATH,
) -> dict[str, Any]:
    """Return route status for shadow boundary/benchmark checks."""
    repo_root = _repo_root(root)
    api_index = _resolve_path_inside_root(repo_root, Path(api_index_path), "api index")
    if not api_index.is_file():
        return {
            "checked": False,
            "path": api_index,
            "resolveRouteMounted": False,
            "traceRouteMounted": False,
            "resolveRouteDeclared": False,
            "traceRouteDeclared": False,
            "defaultOffResolveRouteDeclared": False,
            "defaultOffTraceRouteDeclared": False,
            "resolverRoutePolicy": "absent",
            "previewRoutesPresent": {},
            "routeCount": 0,
            "routes": [],
            "warnings": [],
            "reason": "api index file not present under repo root",
        }
    inventory = inventory_api_routes(api_index, root=repo_root)
    return {
        "checked": True,
        "path": api_index,
        "resolveRouteMounted": inventory["resolveRouteMounted"],
        "traceRouteMounted": inventory["traceRouteMounted"],
        "resolveRouteDeclared": inventory["resolveRouteDeclared"],
        "traceRouteDeclared": inventory["traceRouteDeclared"],
        "defaultOffResolveRouteDeclared": inventory["defaultOffResolveRouteDeclared"],
        "defaultOffTraceRouteDeclared": inventory["defaultOffTraceRouteDeclared"],
        "defaultOnResolveRouteDeclared": inventory["defaultOnResolveRouteDeclared"],
        "defaultOnTraceRouteDeclared": inventory["defaultOnTraceRouteDeclared"],
        "disabledRollbackGuardDeclared": inventory["disabledRollbackGuardDeclared"],
        "resolverRoutePolicy": inventory["resolverRoutePolicy"],
        "previewRoutesPresent": inventory["previewRoutesPresent"],
        "routeCount": inventory["routeCount"],
        "routes": inventory["routes"],
        "warnings": inventory["warnings"],
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate an AEC-MEPFS Backbone shadow API route inventory."
    )
    parser.add_argument("--repo-root", default=None)
    parser.add_argument("--run-id", default=None)
    parser.add_argument("--output", default=None)
    parser.add_argument("--api-index", default=str(API_INDEX_PATH))
    args = parser.parse_args(argv)

    try:
        report = run_api_route_inventory(
            repo_root=args.repo_root,
            run_id=args.run_id,
            output_path=args.output,
            api_index_path=args.api_index,
        )
    except ValueError as exc:
        print(json.dumps({"ok": False, "errors": [str(exc)]}, indent=2, sort_keys=True))
        return 1

    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["ok"] else 1


def _extract_hono_routes(
    text: str,
    *,
    resolver_runtime_default_enabled: bool = False,
) -> list[dict[str, Any]]:
    routes: list[dict[str, Any]] = []
    index = 0
    line = 1
    column = 1

    def advance_to(target: int) -> None:
        nonlocal index, line, column
        while index < min(target, len(text)):
            if text[index] == "\n":
                line += 1
                column = 1
            else:
                column += 1
            index += 1

    while index < len(text):
        if text.startswith("//", index):
            newline = text.find("\n", index)
            advance_to(len(text) if newline == -1 else newline)
            continue
        if text.startswith("/*", index):
            close = text.find("*/", index + 2)
            advance_to(len(text) if close == -1 else close + 2)
            continue
        if text[index] in {"'", '"', "`"}:
            advance_to(_consume_quoted_literal(text, index)[1])
            continue
        if text.startswith("app.", index):
            route = _read_route_declaration(text, index, line, column)
            if route is not None:
                if _is_forbidden_resolver_path(route["path"]):
                    if _is_default_off_resolver_guarded(text, route["line"]):
                        route["runtimeGuarded"] = True
                        route["defaultOffGuarded"] = not resolver_runtime_default_enabled
                        route["defaultOnGuarded"] = resolver_runtime_default_enabled
                        route["guard"] = RESOLVER_RUNTIME_FLAG
                    else:
                        route["runtimeGuarded"] = False
                        route["defaultOffGuarded"] = False
                        route["defaultOnGuarded"] = False
                routes.append(route)
                advance_to(route["_end"])
                route.pop("_end", None)
                continue
        advance_to(index + 1)
    return routes


def _read_route_declaration(
    text: str,
    start: int,
    line: int,
    column: int,
) -> dict[str, Any] | None:
    method_start = start + len("app.")
    method_end = method_start
    while method_end < len(text) and (
        text[method_end].isalnum() or text[method_end] == "_"
    ):
        method_end += 1
    method = text[method_start:method_end].lower()
    if method not in HIDDEN_ROUTE_METHODS:
        return None
    cursor = _skip_whitespace(text, method_end)
    if cursor >= len(text) or text[cursor] != "(":
        return None
    cursor = _skip_whitespace(text, cursor + 1)
    if cursor >= len(text) or text[cursor] not in {"'", '"', "`"}:
        return None
    path, end = _consume_quoted_literal(text, cursor)
    if not path.startswith("/"):
        return None
    return {
        "method": method,
        "path": path,
        "line": line,
        "column": column,
        "_end": end,
    }


def _consume_quoted_literal(text: str, start: int) -> tuple[str, int]:
    quote = text[start]
    cursor = start + 1
    chars: list[str] = []
    while cursor < len(text):
        char = text[cursor]
        if char == "\\" and cursor + 1 < len(text):
            chars.append(text[cursor + 1])
            cursor += 2
            continue
        if char == quote:
            return "".join(chars), cursor + 1
        chars.append(char)
        cursor += 1
    return "".join(chars), cursor


def _skip_whitespace(text: str, cursor: int) -> int:
    while cursor < len(text) and text[cursor].isspace():
        cursor += 1
    return cursor


def _has_route(routes: list[dict[str, Any]], method: str, path: str) -> bool:
    return any(route["method"] == method and route["path"] == path for route in routes)


def _resolver_routes(routes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [route for route in routes if _is_forbidden_resolver_path(route["path"])]


def _forbidden_resolver_routes(routes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        route
        for route in routes
        if _is_forbidden_resolver_path(route["path"])
        and route.get("runtimeGuarded") is not True
    ]


def _has_forbidden_resolver_route(routes: list[dict[str, Any]]) -> bool:
    return any(_is_forbidden_resolver_path(route["path"]) for route in routes)


def _is_forbidden_resolver_path(path: str) -> bool:
    return path == "/v2/resolve" or path.startswith("/v2/resolve/")


def _is_trace_resolver_path(path: str) -> bool:
    return path == "/v2/resolve/trace" or path.startswith("/v2/resolve/trace/")


def _has_forbidden_trace_route(routes: list[dict[str, Any]]) -> bool:
    return any(_is_trace_resolver_path(route["path"]) for route in routes)


def _resolver_route_policy(
    *,
    resolver_routes: list[dict[str, Any]],
    unauthorized_resolver_routes: list[dict[str, Any]],
    guarded_resolver_routes: list[dict[str, Any]],
    resolver_runtime_default_enabled: bool,
) -> str:
    if unauthorized_resolver_routes:
        return "unsafe_mounted"
    if guarded_resolver_routes:
        if resolver_runtime_default_enabled:
            return "default_on_file_backed_with_disable_flag"
        return "guarded_default_off"
    if resolver_routes:
        return "unsafe_mounted"
    return "absent"


def _resolver_runtime_default_enabled(text: str) -> bool:
    return (
        "AEC_MEPFS_RESOLVER_RUNTIME_DEFAULT = 'on'" in text
        or 'AEC_MEPFS_RESOLVER_RUNTIME_DEFAULT = "on"' in text
        or "if (!value) return true;" in text
    )


def _is_default_off_resolver_guarded(text: str, line: int) -> bool:
    lines = text.splitlines()
    route_line_index = max(0, line - 1)
    context = "\n".join(lines[max(0, route_line_index - 8) : route_line_index + 1])
    return "if (isAecMepfsResolverRuntimeEnabled())" in context


def _route_boundary_errors(inventory: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if inventory.get("checked") is not True:
        errors.append("api route inventory: api index must be checked")
    policy = inventory.get("resolverRoutePolicy")
    default_on_policy = policy == "default_on_file_backed_with_disable_flag"
    if inventory.get("resolveRouteMounted") is not False and not default_on_policy:
        errors.append(
            "api route inventory: /v2/resolve must remain absent, default-off guarded, or default-on with disable flag"
        )
    if inventory.get("traceRouteMounted") is not False and not default_on_policy:
        errors.append(
            "api route inventory: /v2/resolve/trace must remain absent, default-off guarded, or default-on with disable flag"
        )
    missing_routes = [
        name
        for name, present in inventory.get("previewRoutesPresent", {}).items()
        if not present
    ]
    if missing_routes:
        errors.append(
            "api route inventory: missing expected preview routes "
            f"({', '.join(missing_routes)})"
        )
    return errors


def _missing_inventory(path: Path, root: Path) -> dict[str, Any]:
    return {
        "checked": False,
        "path": _relative_to_root(path, root),
        "routeCount": 0,
        "routes": [],
        "forbiddenResolveRoutes": [],
        "guardedResolveRoutes": [],
        "resolveRouteDeclared": False,
        "traceRouteDeclared": False,
        "defaultOffResolveRouteDeclared": False,
        "defaultOffTraceRouteDeclared": False,
        "defaultOnResolveRouteDeclared": False,
        "defaultOnTraceRouteDeclared": False,
        "disabledRollbackGuardDeclared": False,
        "resolverRoutePolicy": "absent",
        "resolveRouteMounted": False,
        "traceRouteMounted": False,
        "previewRoutesPresent": {name: False for name in REQUIRED_PREVIEW_ROUTES},
        "warnings": [],
        "reason": "api index file not present under repo root",
    }


def _repo_root(value: str | Path | None) -> Path:
    if value is not None:
        return Path(value).resolve()
    return Path(__file__).resolve().parents[3]


def _resolve_path_inside_root(root: Path, value: Path, label: str) -> Path:
    path = value.resolve() if value.is_absolute() else (root / value).resolve()
    try:
        path.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"{label} path must stay inside repo root") from exc
    return path


def _resolve_report_path(
    *,
    root: Path,
    run_id: str,
    output_path: Path | None,
) -> Path:
    candidate = output_path or (
        API_ROUTE_INVENTORY_REPORT_ROOT / run_id / API_ROUTE_INVENTORY_REPORT_FILENAME
    )
    report_path = candidate.resolve() if candidate.is_absolute() else (root / candidate).resolve()
    allowed_root = (root / API_ROUTE_INVENTORY_REPORT_ROOT).resolve()
    try:
        relative_parts = report_path.relative_to(allowed_root).parts
    except ValueError as exc:
        raise ValueError("report path must stay inside the route inventory report directory") from exc
    if len(relative_parts) != 2 or relative_parts[0] != run_id:
        raise ValueError("report path must be scoped to the current route inventory run id")
    if relative_parts[1] != API_ROUTE_INVENTORY_REPORT_FILENAME:
        raise ValueError(f"report filename must be {API_ROUTE_INVENTORY_REPORT_FILENAME}")
    return report_path


def _run_id(value: str | None) -> str:
    candidate = value or datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    if not RUN_ID_RE.fullmatch(candidate):
        raise ValueError("run_id must contain only letters, digits, underscore, dot, or dash")
    return candidate


def _utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _hash_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _relative_to_root(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
