"""Stream M.3 — OWL/Turtle exporter for graph snapshot."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

rdflib = pytest.importorskip("rdflib")

from vitruvius.ontology.owl_exporter import (
    IFC_NAMESPACE,
    VITRUVIUS_NAMESPACE,
    export_snapshot_as_turtle,
)


def _write_snapshot(path: Path, payload: dict) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, sort_keys=True, indent=2), encoding="utf-8")
    return path


def _make_snapshot(nodes: list[dict], edges: list[dict]) -> dict:
    return {
        "schema_version": "1.0.0",
        "generated_at_utc": "2026-04-15T00:00:00Z",
        "node_count": len(nodes),
        "edge_count": len(edges),
        "nodes": nodes,
        "edges": edges,
    }


def _write_mapping(path: Path, body: str) -> Path:
    path.write_text(body, encoding="utf-8")
    return path


def test_empty_snapshot_emits_prefixes_only(tmp_path: Path) -> None:
    snap = _write_snapshot(tmp_path / "snap.json", _make_snapshot([], []))
    out = tmp_path / "out.ttl"
    export_snapshot_as_turtle(snap, out)
    text = out.read_text(encoding="utf-8")
    assert "@prefix" in text
    assert VITRUVIUS_NAMESPACE in text or "vitruvius" in text


def test_happy_path_nodes_and_edges(tmp_path: Path) -> None:
    snap = _write_snapshot(
        tmp_path / "snap.json",
        _make_snapshot(
            nodes=[
                {
                    "id": "law-pd-1096",
                    "type": "source",
                    "slug": "pd-1096",
                    "trust_level": "primary",
                    "last_updated_utc": "2026-04-01T00:00:00Z",
                },
                {
                    "id": "concept-doors-and-exits",
                    "type": "concept",
                    "slug": "doors-and-exits",
                    "trust_level": "derived",
                    "last_updated_utc": "2026-04-01T00:00:00Z",
                },
            ],
            edges=[
                {
                    "from_id": "law-pd-1096",
                    "to_id": "concept-doors-and-exits",
                    "type": "governs",
                    "evidence_id": "rel-pd-1096-governs-doors-and-exits",
                    "status": "verified",
                }
            ],
        ),
    )
    out = tmp_path / "out.ttl"
    export_snapshot_as_turtle(snap, out)
    g = rdflib.Graph()
    g.parse(out.as_posix(), format="turtle")
    assert len(g) > 0
    text = out.read_text(encoding="utf-8")
    assert "concept-doors-and-exits" in text
    assert "governs" in text or "vitruvius" in text


def test_ifc_same_as_emitted_when_mapping_exists(tmp_path: Path) -> None:
    snap = _write_snapshot(
        tmp_path / "snap.json",
        _make_snapshot(
            nodes=[
                {
                    "id": "concept-doors-and-exits",
                    "type": "concept",
                    "slug": "doors-and-exits",
                    "trust_level": "derived",
                    "last_updated_utc": "2026-04-01T00:00:00Z",
                }
            ],
            edges=[],
        ),
    )
    out = tmp_path / "out.ttl"
    mapping_path = _write_mapping(
        tmp_path / "mapping.yaml",
        "- concept_id: concept-doors-and-exits\n"
        "  ifc_class: IfcDoor\n"
        "  psets: [Pset_DoorCommon]\n"
        "  notes: test\n",
    )
    export_snapshot_as_turtle(snap, out, ifc_mapping_path=mapping_path)
    g = rdflib.Graph()
    g.parse(out.as_posix(), format="turtle")
    q = (
        "PREFIX owl: <http://www.w3.org/2002/07/owl#> "
        "SELECT ?a WHERE { ?a owl:sameAs ?b }"
    )
    rows = list(g.query(q))
    assert len(rows) >= 1
    text = out.read_text(encoding="utf-8")
    assert "IfcDoor" in text


def test_no_same_as_when_mapping_absent(tmp_path: Path) -> None:
    snap = _write_snapshot(
        tmp_path / "snap.json",
        _make_snapshot(
            nodes=[
                {
                    "id": "concept-unknown",
                    "type": "concept",
                    "slug": "unknown",
                    "trust_level": "derived",
                    "last_updated_utc": "2026-04-01T00:00:00Z",
                }
            ],
            edges=[],
        ),
    )
    out = tmp_path / "out.ttl"
    mapping_path = _write_mapping(tmp_path / "mapping.yaml", "[]\n")
    export_snapshot_as_turtle(snap, out, ifc_mapping_path=mapping_path)
    text = out.read_text(encoding="utf-8")
    assert "owl:sameAs" not in text
    assert "IfcDoor" not in text


def test_deterministic_output(tmp_path: Path) -> None:
    snap = _write_snapshot(
        tmp_path / "snap.json",
        _make_snapshot(
            nodes=[
                {
                    "id": "concept-zeta",
                    "type": "concept",
                    "slug": "zeta",
                    "trust_level": "derived",
                    "last_updated_utc": "2026-04-01T00:00:00Z",
                },
                {
                    "id": "concept-alpha",
                    "type": "concept",
                    "slug": "alpha",
                    "trust_level": "derived",
                    "last_updated_utc": "2026-04-01T00:00:00Z",
                },
            ],
            edges=[
                {
                    "from_id": "concept-alpha",
                    "to_id": "concept-zeta",
                    "type": "relates_to",
                    "evidence_id": "rel-a-z",
                    "status": "verified",
                }
            ],
        ),
    )
    out1 = tmp_path / "out1.ttl"
    out2 = tmp_path / "out2.ttl"
    export_snapshot_as_turtle(snap, out1)
    export_snapshot_as_turtle(snap, out2)
    assert out1.read_bytes() == out2.read_bytes()


def test_output_path_parent_created(tmp_path: Path) -> None:
    snap = _write_snapshot(tmp_path / "snap.json", _make_snapshot([], []))
    nested = tmp_path / "deep" / "nest" / "out.ttl"
    assert not nested.parent.exists()
    export_snapshot_as_turtle(snap, nested)
    assert nested.exists()


def test_malformed_snapshot_raises(tmp_path: Path) -> None:
    bad = tmp_path / "bad.json"
    bad.write_text("not-json-at-all{{{", encoding="utf-8")
    out = tmp_path / "out.ttl"
    with pytest.raises(Exception):
        export_snapshot_as_turtle(bad, out)


def test_spatial_instance_node_exported(tmp_path: Path) -> None:
    snap = _write_snapshot(
        tmp_path / "snap.json",
        _make_snapshot(
            nodes=[
                {
                    "id": "instance-door-01",
                    "type": "spatial_instance",
                    "slug": "door-01",
                    "trust_level": "derived",
                    "last_updated_utc": "2026-04-01T00:00:00Z",
                }
            ],
            edges=[],
        ),
    )
    out = tmp_path / "out.ttl"
    export_snapshot_as_turtle(snap, out)
    g = rdflib.Graph()
    g.parse(out.as_posix(), format="turtle")
    assert len(g) > 0
    text = out.read_text(encoding="utf-8")
    assert "instance-door-01" in text


def test_ifc_namespace_is_documented_constant() -> None:
    assert IFC_NAMESPACE.startswith("http")
    assert VITRUVIUS_NAMESPACE.startswith("http")
