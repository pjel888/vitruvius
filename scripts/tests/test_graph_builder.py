"""Phase 8 Task 2 + Task 3 — builder walker tests."""

from __future__ import annotations

from pathlib import Path

import pytest

from vitruvius.graph.builder import (
    build_snapshot,
    walk_concepts,
    walk_relationships,
    walk_sources,
)
from vitruvius.graph.contract import GraphEdge, GraphNode, GraphSnapshot, validate_node


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_walk_sources_emits_one_node_per_file(tmp_path: Path) -> None:
    src = tmp_path / "sources"
    _write(src / "pd-1096.md", (
        "---\n"
        "id: law-pd-1096\n"
        "trust_level: primary\n"
        "last_canonicalized_utc: 2026-04-01T00:00:00Z\n"
        "---\n\n# body\n"
    ))
    nodes = walk_sources(src)
    assert len(nodes) == 1
    node = nodes[0]
    assert isinstance(node, GraphNode)
    assert node.id == "law-pd-1096"
    assert node.type == "source"
    assert node.trust_level == "primary"
    assert node.slug == "pd-1096"
    assert node.last_updated_utc == "2026-04-01T00:00:00Z"
    validate_node(node)


def test_walk_sources_defaults_trust_to_tertiary(tmp_path: Path) -> None:
    src = tmp_path / "sources"
    _write(src / "law-x.md", (
        "---\n"
        "id: law-x\n"
        "last_canonicalized_utc: 2026-04-01T00:00:00Z\n"
        "---\n\n# body\n"
    ))
    nodes = walk_sources(src)
    assert len(nodes) == 1
    assert nodes[0].trust_level == "tertiary"


def test_walk_sources_sorted_by_id(tmp_path: Path) -> None:
    src = tmp_path / "sources"
    _write(src / "b.md", (
        "---\nid: law-b\ntrust_level: primary\n"
        "last_canonicalized_utc: 2026-04-01T00:00:00Z\n---\n"
    ))
    _write(src / "a.md", (
        "---\nid: law-a\ntrust_level: primary\n"
        "last_canonicalized_utc: 2026-04-01T00:00:00Z\n---\n"
    ))
    nodes = walk_sources(src)
    assert [n.id for n in nodes] == ["law-a", "law-b"]


def test_walk_sources_empty_dir_returns_empty(tmp_path: Path) -> None:
    src = tmp_path / "sources"
    src.mkdir()
    assert walk_sources(src) == []


def test_walk_sources_missing_dir_returns_empty(tmp_path: Path) -> None:
    src = tmp_path / "sources_missing"
    assert walk_sources(src) == []


def test_walk_sources_skips_files_without_id(tmp_path: Path) -> None:
    src = tmp_path / "sources"
    _write(src / "broken.md", "---\ntrust_level: primary\n---\n")
    _write(src / "good.md", (
        "---\nid: law-good\ntrust_level: primary\n"
        "last_canonicalized_utc: 2026-04-01T00:00:00Z\n---\n"
    ))
    nodes = walk_sources(src)
    assert len(nodes) == 1
    assert nodes[0].id == "law-good"


def test_walk_concepts_sets_type_and_derived_trust(tmp_path: Path) -> None:
    concepts = tmp_path / "concepts"
    _write(concepts / "building-permit.md", (
        "---\n"
        "id: concept-building-permit\n"
        "last_canonicalized_utc: 2026-04-01T00:00:00Z\n"
        "---\n\n# body\n"
    ))
    nodes = walk_concepts(concepts)
    assert len(nodes) == 1
    node = nodes[0]
    assert node.id == "concept-building-permit"
    assert node.type == "concept"
    assert node.trust_level == "derived"
    assert node.slug == "building-permit"
    validate_node(node)


def test_walk_concepts_sorted_by_id(tmp_path: Path) -> None:
    concepts = tmp_path / "concepts"
    _write(concepts / "z.md", (
        "---\nid: concept-z\n"
        "last_canonicalized_utc: 2026-04-01T00:00:00Z\n---\n"
    ))
    _write(concepts / "a.md", (
        "---\nid: concept-a\n"
        "last_canonicalized_utc: 2026-04-01T00:00:00Z\n---\n"
    ))
    nodes = walk_concepts(concepts)
    assert [n.id for n in nodes] == ["concept-a", "concept-z"]


def test_walk_concepts_missing_dir_returns_empty(tmp_path: Path) -> None:
    assert walk_concepts(tmp_path / "nope") == []


def test_walk_concepts_uses_file_mtime_fallback_for_missing_date(tmp_path: Path) -> None:
    concepts = tmp_path / "concepts"
    _write(concepts / "x.md", "---\nid: concept-x\n---\n")
    nodes = walk_concepts(concepts)
    assert len(nodes) == 1
    assert nodes[0].last_updated_utc  # non-empty
    validate_node(nodes[0])


# --- Task 3: walk_relationships + build_snapshot ---


def _rel(id_: str, from_id: str, predicate: str, to_id: str, status: str) -> str:
    return (
        "---\n"
        f"id: {id_}\n"
        "page_type: relationship\n"
        f"relationship_type: {predicate}\n"
        f"from_entity: {from_id}\n"
        f"to_entity: {to_id}\n"
        f"canonical_status: {status}\n"
        "---\n\n# body\n"
    )


def test_walk_relationships_promoted_and_verified(tmp_path: Path) -> None:
    rels = tmp_path / "relationships"
    _write(rels / "a.md", _rel(
        "rel-law-x-governs-concept-y",
        "law-x",
        "governs",
        "concept-y",
        "promoted",
    ))
    _write(rels / "b.md", _rel(
        "rel-concept-y-affects-concept-z",
        "concept-y",
        "affects",
        "concept-z",
        "verified",
    ))
    edges = walk_relationships(rels)
    assert len(edges) == 2
    statuses = {e.evidence_id: e.status for e in edges}
    assert statuses["rel-law-x-governs-concept-y"] == "unverified"
    assert statuses["rel-concept-y-affects-concept-z"] == "verified"


def test_walk_relationships_skips_draft(tmp_path: Path) -> None:
    rels = tmp_path / "relationships"
    _write(rels / "draft.md", _rel(
        "rel-law-x-governs-concept-y",
        "law-x",
        "governs",
        "concept-y",
        "draft",
    ))
    assert walk_relationships(rels) == []


def test_walk_relationships_missing_dir(tmp_path: Path) -> None:
    assert walk_relationships(tmp_path / "nope") == []


def test_walk_relationships_sorted_by_key(tmp_path: Path) -> None:
    rels = tmp_path / "relationships"
    _write(rels / "b.md", _rel(
        "rel-b", "law-alpha", "governs", "concept-delta", "promoted"
    ))
    _write(rels / "a.md", _rel(
        "rel-a", "law-alpha", "affects", "concept-gamma", "promoted"
    ))
    edges = walk_relationships(rels)
    assert [e.evidence_id for e in edges] == ["rel-a", "rel-b"]


def test_build_snapshot_empty_root(tmp_path: Path) -> None:
    snapshot = build_snapshot(tmp_path, now="2026-04-14T00:00:00Z")
    assert isinstance(snapshot, GraphSnapshot)
    assert snapshot.schema_version == "1.0.0"
    assert snapshot.node_count == 0
    assert snapshot.edge_count == 0
    assert snapshot.nodes == []
    assert snapshot.edges == []
    assert snapshot.generated_at_utc == "2026-04-14T00:00:00Z"


def test_build_snapshot_full_tree(tmp_path: Path) -> None:
    canonical = tmp_path / "shared"
    _write(canonical / "sources" / "pd-1096.md", (
        "---\nid: law-pd-1096\ntrust_level: primary\n"
        "last_canonicalized_utc: 2026-04-01T00:00:00Z\n---\n"
    ))
    _write(canonical / "concepts" / "building-permit.md", (
        "---\nid: concept-building-permit\n"
        "last_canonicalized_utc: 2026-04-01T00:00:00Z\n---\n"
    ))
    _write(canonical / "relationships" / "r.md", _rel(
        "rel-pd-1096-governs-building-permit",
        "law-pd-1096",
        "governs",
        "concept-building-permit",
        "promoted",
    ))
    snapshot = build_snapshot(canonical, now="2026-04-14T00:00:00Z")
    assert snapshot.node_count == 2
    assert snapshot.edge_count == 1
    assert [n.id for n in snapshot.nodes] == [
        "concept-building-permit",
        "law-pd-1096",
    ]
    assert snapshot.edges[0].from_id == "law-pd-1096"
    assert snapshot.edges[0].to_id == "concept-building-permit"
    assert snapshot.edges[0].status == "unverified"


def test_build_snapshot_sorts_edges_deterministically(tmp_path: Path) -> None:
    canonical = tmp_path / "shared"
    _write(canonical / "relationships" / "one.md", _rel(
        "rel-beta", "law-pd-1096", "affects", "concept-x", "promoted"
    ))
    _write(canonical / "relationships" / "two.md", _rel(
        "rel-alpha", "law-pd-1096", "affects", "concept-x", "promoted"
    ))
    snapshot = build_snapshot(canonical, now="2026-04-14T00:00:00Z")
    assert [e.evidence_id for e in snapshot.edges] == ["rel-alpha", "rel-beta"]


def test_build_snapshot_is_deterministic(tmp_path: Path) -> None:
    canonical = tmp_path / "shared"
    _write(canonical / "sources" / "pd-1096.md", (
        "---\nid: law-pd-1096\ntrust_level: primary\n"
        "last_canonicalized_utc: 2026-04-01T00:00:00Z\n---\n"
    ))
    _write(canonical / "concepts" / "x.md", (
        "---\nid: concept-x\n"
        "last_canonicalized_utc: 2026-04-01T00:00:00Z\n---\n"
    ))
    _write(canonical / "relationships" / "r.md", _rel(
        "rel-x", "law-pd-1096", "governs", "concept-x", "promoted"
    ))
    a = build_snapshot(canonical, now="2026-04-14T00:00:00Z")
    b = build_snapshot(canonical, now="2026-04-14T00:00:00Z")
    assert a == b
