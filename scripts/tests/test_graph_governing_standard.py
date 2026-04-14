"""Stream W3.4 — is_governing_standard on graph edges (additive)."""
from __future__ import annotations

from pathlib import Path

from vitruvius.graph.builder import walk_relationships
from vitruvius.graph.contract import GraphEdge


def _write(path: Path, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")


def test_edge_with_governing_true(tmp_path: Path) -> None:
    rel_dir = tmp_path / "relationships"
    _write(
        rel_dir / "rel-winner.md",
        "---\n"
        "id: rel-pd-1096-requires-concept-setbacks\n"
        "page_type: relationship\n"
        "relationship_type: requires\n"
        "from_entity: law-pd-1096\n"
        "to_entity: concept-setbacks\n"
        "canonical_status: promoted\n"
        "is_governing_standard: true\n"
        "---\n",
    )
    edges = walk_relationships(rel_dir)
    assert len(edges) == 1
    assert edges[0].is_governing_standard is True


def test_edge_with_governing_false(tmp_path: Path) -> None:
    rel_dir = tmp_path / "relationships"
    _write(
        rel_dir / "rel-loser.md",
        "---\n"
        "id: rel-pd-1096-requires-concept-setbacks-old\n"
        "page_type: relationship\n"
        "relationship_type: requires\n"
        "from_entity: law-pd-1096\n"
        "to_entity: concept-setbacks\n"
        "canonical_status: promoted\n"
        "is_governing_standard: false\n"
        "---\n",
    )
    edges = walk_relationships(rel_dir)
    assert edges[0].is_governing_standard is False


def test_edge_defaults_governing_to_none_when_absent(tmp_path: Path) -> None:
    rel_dir = tmp_path / "relationships"
    _write(
        rel_dir / "rel-legacy.md",
        "---\n"
        "id: rel-pd-1096-governs-concept-building-permit\n"
        "page_type: relationship\n"
        "relationship_type: governs\n"
        "from_entity: law-pd-1096\n"
        "to_entity: concept-building-permit\n"
        "canonical_status: promoted\n"
        "---\n",
    )
    edges = walk_relationships(rel_dir)
    assert edges[0].is_governing_standard is None
