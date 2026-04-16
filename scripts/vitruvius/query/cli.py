from __future__ import annotations

import json
from pathlib import Path

from ..graph.dataset_manifest import provenance_for_snapshot, render_query_provenance
from ..graph.snapshot import read_snapshot
from .cli_formatter import render_query_result
from .engine import (
    edges_between,
    neighbors_query,
    supersession_chain,
    what_affects,
    what_defines,
    what_depends_on,
    what_governs,
    what_limits,
    what_requires,
)
from .nl_translator import translate_question


_SNAPSHOT_RELPATH = (
    Path("005_Operational-Intelligence-Layer") / "graph" / "latest_graph_snapshot.json"
)


_STRUCTURED_FUNCTIONS = {
    "what_governs": what_governs,
    "what_requires": what_requires,
    "what_limits": what_limits,
    "what_defines": what_defines,
    "what_depends_on": what_depends_on,
    "what_affects": what_affects,
    "supersession_chain": supersession_chain,
    "neighbors": neighbors_query,
}


def _resolve_snapshot_path(snapshot_path: str | None) -> tuple[Path, str]:
    if snapshot_path is None:
        return Path.cwd() / _SNAPSHOT_RELPATH, str(_SNAPSHOT_RELPATH)
    path = Path(snapshot_path)
    if not path.is_absolute():
        path = Path.cwd() / path
    try:
        display_path = str(path.relative_to(Path.cwd()))
    except ValueError:
        display_path = str(path)
    return path, display_path


def _load_snapshot_or_fail(snapshot_path: str | None = None):
    path, display_path = _resolve_snapshot_path(snapshot_path)
    if not path.exists():
        print(json.dumps({
            "error": "no snapshot found",
            "expected_path": display_path,
            "hint": "run `build-graph` first",
        }, indent=2))
        return None
    return read_snapshot(path), display_path


def run_query(question: str, *, snapshot_path: str | None = None) -> int:
    loaded = _load_snapshot_or_fail(snapshot_path)
    if loaded is None:
        return 1
    snapshot, display_path = loaded
    known = tuple(n.id for n in snapshot.nodes)
    translation = translate_question(question, known_entities=known)
    func = _STRUCTURED_FUNCTIONS.get(translation.function)
    subject = translation.arguments.get("subject")
    if func is None or subject is None:
        result = neighbors_query("", snapshot)
    else:
        result = func(subject, snapshot)
    provenance = provenance_for_snapshot(snapshot, snapshot_path=display_path)
    print(render_query_provenance(provenance) + render_query_result(result), end="")
    return 0 if result.has_evidence else 1


def run_query_structured(
    *,
    function: str,
    subject: str | None = None,
    a: str | None = None,
    b: str | None = None,
    snapshot_path: str | None = None,
) -> int:
    loaded = _load_snapshot_or_fail(snapshot_path)
    if loaded is None:
        return 1
    snapshot, display_path = loaded

    if function == "edges_between":
        if not a or not b:
            print(json.dumps({
                "error": "edges_between requires --a and --b",
            }, indent=2))
            return 2
        result = edges_between(a, b, snapshot)
    else:
        func = _STRUCTURED_FUNCTIONS.get(function)
        if func is None:
            print(json.dumps({
                "error": f"unknown function {function!r}",
                "allowed": sorted(list(_STRUCTURED_FUNCTIONS) + ["edges_between"]),
            }, indent=2))
            return 2
        if not subject:
            print(json.dumps({
                "error": f"function {function} requires --subject",
            }, indent=2))
            return 2
        result = func(subject, snapshot)
    provenance = provenance_for_snapshot(snapshot, snapshot_path=display_path)
    print(render_query_provenance(provenance) + render_query_result(result), end="")
    return 0 if result.has_evidence else 1
