"""Phase 8 Task 2 + Task 3 — builder walker tests."""

from __future__ import annotations

from pathlib import Path

import pytest

from vitruvius.graph.builder import walk_concepts, walk_sources
from vitruvius.graph.contract import GraphNode, validate_node


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
