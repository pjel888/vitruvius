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


def run_export_graph_owl() -> int:
    """Export the current Phase 8 snapshot to RDF Turtle.

    Writes ``005_Operational-Intelligence-Layer/graph/latest_graph_snapshot.ttl``
    under the current working directory and prints the rendered Turtle
    to stdout. Returns ``0`` on success or ``2`` when the snapshot
    file is missing (caller must run ``build-graph`` first).
    """
    repo_root = Path.cwd()
    snapshot_path = repo_root / _SNAPSHOT_RELPATH
    if not snapshot_path.exists():
        print(json.dumps({
            "error": "no snapshot found — run build-graph first",
            "expected_path": str(_SNAPSHOT_RELPATH),
        }, indent=2))
        return 2

    mapping_path = repo_root / _IFC_MAPPING_RELPATH
    output_path = repo_root / _OWL_OUTPUT_RELPATH

    export_snapshot_as_turtle(
        snapshot_path,
        output_path,
        ifc_mapping_path=mapping_path if mapping_path.exists() else None,
    )

    body = output_path.read_text(encoding="utf-8")
    print(body, end="" if body.endswith("\n") else "\n")
    return 0
