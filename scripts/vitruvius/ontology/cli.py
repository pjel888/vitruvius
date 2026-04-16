"""Stream M.4 — ``export-graph-owl`` CLI handler.

Reads the Phase 8 snapshot produced by ``build-graph`` and writes an
RDF Turtle file via :func:`owl_exporter.export_snapshot_as_turtle`.
Uses the default repo-shipped ``ifc_mapping.yaml`` when present so
concepts with IFC cross-links get ``owl:sameAs`` triples for free.

Follows the spatial CLI convention: paths are resolved against
``Path.cwd()`` so tests can run the handler inside a ``tmp_path``
working directory.
"""
from __future__ import annotations

import json
from pathlib import Path

from .owl_exporter import export_snapshot_as_turtle


_SNAPSHOT_RELPATH = (
    Path("005_Operational-Intelligence-Layer") / "graph" / "latest_graph_snapshot.json"
)
_IFC_MAPPING_RELPATH = (
    Path("scripts") / "vitruvius" / "ontology" / "ifc_mapping.yaml"
)
_OWL_OUTPUT_RELPATH = (
    Path("005_Operational-Intelligence-Layer") / "graph" / "latest_graph_snapshot.ttl"
)


def _resolve_path(path_value: str | None, default_relpath: Path) -> tuple[Path, str]:
    if path_value is None:
        return Path.cwd() / default_relpath, str(default_relpath)
    path = Path(path_value)
    if not path.is_absolute():
        path = Path.cwd() / path
    try:
        display_path = str(path.relative_to(Path.cwd()))
    except ValueError:
        display_path = str(path)
    return path, display_path


def run_export_graph_owl(
    *,
    snapshot_path: str | None = None,
    out_path: str | None = None,
) -> int:
    """Export the current Phase 8 snapshot to RDF Turtle.

    Writes ``005_Operational-Intelligence-Layer/graph/latest_graph_snapshot.ttl``
    under the current working directory and prints the rendered Turtle
    to stdout. Returns ``0`` on success or ``2`` when the snapshot
    file is missing (caller must run ``build-graph`` first).
    """
    snapshot_path_resolved, display_snapshot_path = _resolve_path(snapshot_path, _SNAPSHOT_RELPATH)
    if not snapshot_path_resolved.exists():
        print(json.dumps({
            "error": "no snapshot found — run build-graph first",
            "expected_path": display_snapshot_path,
        }, indent=2))
        return 2

    repo_root = Path.cwd()
    mapping_path = repo_root / _IFC_MAPPING_RELPATH
    if out_path is None:
        output_path = (
            repo_root / _OWL_OUTPUT_RELPATH
            if snapshot_path is None
            else snapshot_path_resolved.with_suffix(".ttl")
        )
    else:
        output_path = Path(out_path)
        if not output_path.is_absolute():
            output_path = repo_root / output_path

    export_snapshot_as_turtle(
        snapshot_path_resolved,
        output_path,
        ifc_mapping_path=mapping_path if mapping_path.exists() else None,
    )

    body = output_path.read_text(encoding="utf-8")
    print(body, end="" if body.endswith("\n") else "\n")
    return 0
