from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from .contract import GraphEdge, GraphNode, GraphSnapshot


def _edge_to_dict(edge: GraphEdge) -> dict:
    payload = asdict(edge)
    optional_evidence_fields = {
        "evidence_source_id",
        "evidence_source_section_id",
        "evidence_snippet",
        "reviewer_confidence",
    }
    return {
        key: value
        for key, value in payload.items()
        if key not in optional_evidence_fields or value is not None
    }


def _snapshot_to_dict(snapshot: GraphSnapshot) -> dict:
    return {
        "schema_version": snapshot.schema_version,
        "generated_at_utc": snapshot.generated_at_utc,
        "node_count": snapshot.node_count,
        "edge_count": snapshot.edge_count,
        "nodes": [asdict(n) for n in snapshot.nodes],
        "edges": [_edge_to_dict(e) for e in snapshot.edges],
    }


def write_snapshot(snapshot: GraphSnapshot, out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    payload = _snapshot_to_dict(snapshot)
    text = json.dumps(payload, sort_keys=True, indent=2, ensure_ascii=False)
    out_path.write_text(text + "\n", encoding="utf-8")


def read_snapshot(in_path: Path) -> GraphSnapshot:
    text = in_path.read_text(encoding="utf-8")
    data = json.loads(text)
    nodes = [GraphNode(**n) for n in data.get("nodes", [])]
    edges = [GraphEdge(**e) for e in data.get("edges", [])]
    return GraphSnapshot(
        schema_version=data["schema_version"],
        generated_at_utc=data["generated_at_utc"],
        node_count=data.get("node_count", len(nodes)),
        edge_count=data.get("edge_count", len(edges)),
        nodes=nodes,
        edges=edges,
    )
