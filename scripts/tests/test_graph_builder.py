"""Phase 8 Task 2 + Task 3 — builder walker tests."""

from __future__ import annotations

from pathlib import Path

import pytest

from vitruvius.graph.builder import (
    build_snapshot,
    walk_concept_basis_edges,
    walk_concepts,
    walk_relationships,
    walk_source_referenced_concept_edges,
    walk_source_relationship_edges,
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
    assert node.title == "Pd 1096"
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
    assert node.title == "Building Permit"
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
    _write(
        rels / "a.md",
        (
            _rel(
                "rel-law-x-governs-concept-y",
                "law-x",
                "governs",
                "concept-y",
                "promoted",
            ).replace(
                "---\n\n# body\n",
                "evidence:\n"
                "- source_id: law-x\n"
                "  source_section_id: sec-1\n"
                "  evidence_snippet: Example evidence\n"
                "  reviewer_confidence: 0.91\n"
                "---\n\n# body\n",
            )
        ),
    )
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
    first = next(e for e in edges if e.evidence_id == "rel-law-x-governs-concept-y")
    assert first.evidence_source_id == "law-x"
    assert first.evidence_source_section_id == "sec-1"
    assert first.evidence_snippet == "Example evidence"
    assert first.reviewer_confidence == 0.91


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


def test_walk_relationships_accepts_explicit_paths_outside_default_dir(tmp_path: Path) -> None:
    rels = tmp_path / "relationships"
    external = tmp_path / "dataset" / "staged.md"
    _write(external, _rel(
        "rel-staged", "law-alpha", "governs", "concept-beta", "promoted"
    ))
    edges = walk_relationships(rels, allowed_paths=[external])
    assert len(edges) == 1
    assert edges[0].evidence_id == "rel-staged"


def test_walk_source_relationship_edges_emits_frontmatter_edges(tmp_path: Path) -> None:
    sources = tmp_path / "sources"
    _write(
        sources / "irr.md",
        (
            "---\n"
            "id: irr-example\n"
            "trust_level: primary\n"
            "relationships:\n"
            "- implements: law-example\n"
            "---\n"
        ),
    )
    edges = walk_source_relationship_edges(
        sources,
        valid_target_ids={"irr-example", "law-example"},
    )
    assert len(edges) == 1
    edge = edges[0]
    assert edge.from_id == "irr-example"
    assert edge.to_id == "law-example"
    assert edge.type == "implements"
    assert edge.status == "verified"
    assert edge.evidence_id.startswith("rel-meta-")


def test_walk_concept_basis_edges_emits_source_to_concept_edges(tmp_path: Path) -> None:
    concepts = tmp_path / "concepts"
    _write(
        concepts / "doors.md",
        (
            "---\n"
            "id: concept-doors\n"
            "regulatory_basis:\n"
            "- source_id: law-example\n"
            "  section_id: sec-1007\n"
            "  evidence_snippet: Example snippet\n"
            "---\n"
        ),
    )
    edges = walk_concept_basis_edges(
        concepts,
        valid_source_ids={"law-example"},
    )
    assert len(edges) == 1
    edge = edges[0]
    assert edge.from_id == "law-example"
    assert edge.to_id == "concept-doors"
    assert edge.type == "defines"
    assert edge.status == "verified"
    assert edge.evidence_source_section_id == "sec-1007"
    assert edge.evidence_snippet == "Example snippet"
    assert edge.evidence_id.startswith("rel-basis-")


def test_walk_source_referenced_concept_edges_emits_covers_edges_for_orphan_sources(
    tmp_path: Path,
) -> None:
    sources = tmp_path / "sources"
    _write(
        sources / "guide.md",
        (
            "---\n"
            "id: handout-example\n"
            "trust_level: primary\n"
            "last_canonicalized_utc: 2026-04-01T00:00:00Z\n"
            "---\n\n"
            "# Example\n\n"
            "## Referenced Concepts\n"
            "- concept-alpha\n"
            "- concept-alpha\n"
            "- concept-beta\n"
            "- law-example\n"
        ),
    )
    edges = walk_source_referenced_concept_edges(
        sources,
        valid_target_ids={"concept-alpha", "concept-beta"},
        allowed_source_ids={"handout-example"},
    )
    assert [(edge.to_id, edge.type, edge.status) for edge in edges] == [
        ("concept-alpha", "covers", "unverified"),
        ("concept-beta", "covers", "unverified"),
    ]
    assert all(edge.evidence_id.startswith("rel-ref-") for edge in edges)


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


def test_build_snapshot_adds_provenance_edges_and_filters_ungrounded_placeholders(
    tmp_path: Path,
) -> None:
    canonical = tmp_path / "shared"
    _write(
        canonical / "sources" / "law.md",
        (
            "---\n"
            "id: law-example\n"
            "trust_level: primary\n"
            "last_canonicalized_utc: 2026-04-01T00:00:00Z\n"
            "---\n"
        ),
    )
    _write(
        canonical / "sources" / "irr.md",
        (
            "---\n"
            "id: irr-example\n"
            "trust_level: primary\n"
            "last_canonicalized_utc: 2026-04-01T00:00:00Z\n"
            "relationships:\n"
            "- implements: law-example\n"
            "---\n"
        ),
    )
    _write(
        canonical / "sources" / "stale.md",
        (
            "---\n"
            "id: law-stale\n"
            "trust_level: primary\n"
            "last_canonicalized_utc: 2026-04-01T00:00:00Z\n"
            "relationships:\n"
            "- implemented_by: irr-missing\n"
            "---\n"
        ),
    )
    _write(
        canonical / "concepts" / "doors.md",
        (
            "---\n"
            "id: concept-doors\n"
            "last_canonicalized_utc: 2026-04-01T00:00:00Z\n"
            "regulatory_basis:\n"
            "- source_id: law-example\n"
            "  section_id: sec-1007\n"
            "  evidence_snippet: Example snippet\n"
            "---\n"
        ),
    )
    _write(
        canonical / "concepts" / "parking.md",
        (
            "---\n"
            "id: concept-parking\n"
            "canonical_status: draft\n"
            "last_canonicalized_utc: 2026-04-01T00:00:00Z\n"
            "---\n"
        ),
    )
    snapshot = build_snapshot(canonical, now="2026-04-14T00:00:00Z")
    node_ids = [n.id for n in snapshot.nodes]
    assert "law-example" in node_ids
    assert "irr-example" in node_ids
    assert "concept-doors" in node_ids
    assert "concept-parking" not in node_ids
    assert "law-stale" not in node_ids
    edge_pairs = {(e.from_id, e.type, e.to_id) for e in snapshot.edges}
    assert ("irr-example", "implements", "law-example") in edge_pairs
    assert ("law-example", "defines", "concept-doors") in edge_pairs


def test_build_snapshot_keeps_unreferenced_sources_without_broken_frontmatter_links(
    tmp_path: Path,
) -> None:
    canonical = tmp_path / "shared"
    _write(
        canonical / "sources" / "standalone.md",
        (
            "---\n"
            "id: law-standalone\n"
            "trust_level: primary\n"
            "last_canonicalized_utc: 2026-04-01T00:00:00Z\n"
            "---\n"
        ),
    )
    snapshot = build_snapshot(canonical, now="2026-04-14T00:00:00Z")
    assert [n.id for n in snapshot.nodes] == ["law-standalone"]
    assert snapshot.edges == []


def test_build_snapshot_adds_referenced_concept_edges_only_for_orphan_sources(
    tmp_path: Path,
) -> None:
    canonical = tmp_path / "shared"
    _write(
        canonical / "sources" / "orphan.md",
        (
            "---\n"
            "id: handout-orphan\n"
            "trust_level: primary\n"
            "last_canonicalized_utc: 2026-04-01T00:00:00Z\n"
            "---\n\n"
            "# Orphan\n\n"
            "## Referenced Concepts\n"
            "- concept-energy\n"
        ),
    )
    _write(
        canonical / "sources" / "linked.md",
        (
            "---\n"
            "id: irr-linked\n"
            "trust_level: primary\n"
            "last_canonicalized_utc: 2026-04-01T00:00:00Z\n"
            "relationships:\n"
            "- implements: law-example\n"
            "---\n\n"
            "# Linked\n\n"
            "## Referenced Concepts\n"
            "- concept-energy\n"
        ),
    )
    _write(
        canonical / "sources" / "law.md",
        (
            "---\n"
            "id: law-example\n"
            "trust_level: primary\n"
            "last_canonicalized_utc: 2026-04-01T00:00:00Z\n"
            "---\n"
        ),
    )
    _write(
        canonical / "concepts" / "energy.md",
        (
            "---\n"
            "id: concept-energy\n"
            "last_canonicalized_utc: 2026-04-01T00:00:00Z\n"
            "---\n"
        ),
    )

    snapshot = build_snapshot(canonical, now="2026-04-14T00:00:00Z")
    edge_pairs = {(e.from_id, e.type, e.to_id) for e in snapshot.edges}
    assert ("handout-orphan", "covers", "concept-energy") in edge_pairs
    assert ("irr-linked", "covers", "concept-energy") not in edge_pairs
    assert ("irr-linked", "implements", "law-example") in edge_pairs


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


def test_build_snapshot_preserves_duplicate_node_ids_for_integrity_reporting(tmp_path: Path) -> None:
    canonical = tmp_path / "shared"
    _write(canonical / "sources" / "a.md", (
        "---\nid: irr-dup\ntrust_level: primary\n"
        "last_canonicalized_utc: 2026-04-01T00:00:00Z\n---\n"
    ))
    _write(canonical / "sources" / "b.md", (
        "---\nid: irr-dup\ntrust_level: primary\n"
        "last_canonicalized_utc: 2026-04-01T00:00:00Z\n---\n"
    ))
    snapshot = build_snapshot(canonical, now="2026-04-14T00:00:00Z")
    assert [n.id for n in snapshot.nodes] == ["irr-dup", "irr-dup"]


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


def test_build_snapshot_respects_explicit_allowlists(tmp_path: Path) -> None:
    canonical = tmp_path / "shared"
    allowed_source = canonical / "sources" / "allowed.md"
    blocked_source = canonical / "sources" / "blocked.md"
    allowed_concept = canonical / "concepts" / "allowed-concept.md"
    blocked_concept = canonical / "concepts" / "blocked-concept.md"
    allowed_relationship = canonical / "relationships" / "allowed.md"
    blocked_relationship = canonical / "relationships" / "blocked.md"

    _write(allowed_source, (
        "---\nid: law-allowed\ntrust_level: primary\n"
        "last_canonicalized_utc: 2026-04-01T00:00:00Z\n---\n"
    ))
    _write(blocked_source, (
        "---\nid: law-blocked\ntrust_level: primary\n"
        "last_canonicalized_utc: 2026-04-01T00:00:00Z\n---\n"
    ))
    _write(allowed_concept, (
        "---\nid: concept-allowed\n"
        "last_canonicalized_utc: 2026-04-01T00:00:00Z\n---\n"
    ))
    _write(blocked_concept, (
        "---\nid: concept-blocked\n"
        "last_canonicalized_utc: 2026-04-01T00:00:00Z\n---\n"
    ))
    _write(allowed_relationship, _rel(
        "rel-allowed", "law-allowed", "governs", "concept-allowed", "promoted"
    ))
    _write(blocked_relationship, _rel(
        "rel-blocked", "law-blocked", "governs", "concept-blocked", "promoted"
    ))

    snapshot = build_snapshot(
        canonical,
        now="2026-04-14T00:00:00Z",
        source_paths=[allowed_source],
        concept_paths=[allowed_concept],
        relationship_paths=[allowed_relationship],
    )

    assert [node.id for node in snapshot.nodes] == ["concept-allowed", "law-allowed"]
    assert [edge.evidence_id for edge in snapshot.edges] == ["rel-allowed"]
