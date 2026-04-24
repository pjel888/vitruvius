"""Tests for UnifiedSnapshotBuilder."""

from __future__ import annotations

from pathlib import Path

import pytest

from vitruvius.kg.enums import NodeType, ValidationState
from vitruvius.kg.json_evidence_store import KgV2Snapshot
from vitruvius.kg.schemas import (
    CanonicalNode,
    Chunk,
    DocumentVersion,
    EvidenceSpan,
    RelationshipAssertion,
    Section,
    TextRangeSelector,
)
from vitruvius.kg.unified_snapshot_builder import UnifiedSnapshotBuilder


class TestGeneratePlacements:
    def test_creates_placement_for_concept_with_taxonomy_path(self) -> None:
        builder = UnifiedSnapshotBuilder(Path("."))
        nodes = [
            CanonicalNode(
                id="taxonomy-building-code",
                type=NodeType.TAXONOMY,
                label="Building Code",
                slug="building-code",
                taxonomy_path=["building-code"],
                status=ValidationState.VALIDATED,
                confidence=1.0,
            ),
            CanonicalNode(
                id="concept-permit",
                type=NodeType.CONCEPT,
                label="Building Permit",
                slug="building-permit",
                taxonomy_path=["building-code"],
                status=ValidationState.VALIDATED,
                confidence=0.9,
            ),
        ]
        placements = builder._generate_placements(nodes)
        assert len(placements) == 1
        assert placements[0].node_id == "concept-permit"
        assert placements[0].parent_node_id == "taxonomy-building-code"
        assert "building-code" in placements[0].reasoning_summary

    def test_no_placement_for_taxonomy_root(self) -> None:
        builder = UnifiedSnapshotBuilder(Path("."))
        nodes = [
            CanonicalNode(
                id="taxonomy-root",
                type=NodeType.TAXONOMY,
                label="Root",
                slug="root",
                taxonomy_path=["root"],
                status=ValidationState.VALIDATED,
                confidence=1.0,
            ),
        ]
        placements = builder._generate_placements(nodes)
        assert len(placements) == 0

    def test_no_placement_for_concept_without_path(self) -> None:
        builder = UnifiedSnapshotBuilder(Path("."))
        nodes = [
            CanonicalNode(
                id="concept-orphan",
                type=NodeType.CONCEPT,
                label="Orphan",
                slug="orphan",
                taxonomy_path=[],
                status=ValidationState.CANDIDATE,
                confidence=0.5,
            ),
        ]
        placements = builder._generate_placements(nodes)
        assert len(placements) == 0

    def test_skips_placement_when_no_taxonomy_match(self) -> None:
        builder = UnifiedSnapshotBuilder(Path("."))
        nodes = [
            CanonicalNode(
                id="concept-x",
                type=NodeType.CONCEPT,
                label="X",
                slug="x",
                taxonomy_path=["nonexistent", "path"],
                status=ValidationState.CANDIDATE,
                confidence=0.5,
            ),
        ]
        placements = builder._generate_placements(nodes)
        assert len(placements) == 0

    def test_matches_prefixed_concept_path_to_unprefixed_taxonomy_root(self) -> None:
        builder = UnifiedSnapshotBuilder(Path("."))
        nodes = [
            CanonicalNode(
                id="taxonomy-accessibility",
                type=NodeType.TAXONOMY,
                label="Accessibility",
                slug="accessibility",
                taxonomy_path=["accessibility"],
                status=ValidationState.VALIDATED,
                confidence=1.0,
            ),
            CanonicalNode(
                id="concept-accessible-route",
                type=NodeType.CONCEPT,
                label="Accessible Route",
                slug="accessible-route",
                taxonomy_path=["taxonomy-accessibility", "topic-barrier-free-design"],
                status=ValidationState.VALIDATED,
                confidence=0.9,
            ),
        ]

        placements = builder._generate_placements(nodes)

        assert len(placements) == 1
        assert placements[0].node_id == "concept-accessible-route"
        assert placements[0].parent_node_id == "taxonomy-accessibility"


class TestBuildIntegration:
    def test_build_produces_snapshot(self, tmp_path: Path) -> None:
        # Create minimal repo structure
        canonical_root = tmp_path / "003_Canonical-Knowledge-Layer" / "shared"
        concepts_dir = canonical_root / "concepts"
        concepts_dir.mkdir(parents=True)
        taxonomy_dir = canonical_root / "taxonomy"
        taxonomy_dir.mkdir(parents=True)
        sources_dir = canonical_root / "sources"
        sources_dir.mkdir(parents=True)

        # Write a concept file
        concept_file = concepts_dir / "building-permit.md"
        concept_file.write_text(
            "---\n"
            "id: concept-building-permit\n"
            "title: Building Permit\n"
            "topic_tags:\n  - building-code\n"
            "canonical_status: verified\n"
            "---\n\n"
            "## Definition\n"
            "A permit is required.\n",
            encoding="utf-8",
        )

        # Write a taxonomy root
        taxonomy_file = taxonomy_dir / "building-code.md"
        taxonomy_file.write_text(
            "---\n"
            "id: taxonomy-building-code\n"
            "title: Building Code\n"
            "canonical_status: verified\n"
            "---\n",
            encoding="utf-8",
        )

        # Write a source file
        source_file = sources_dir / "pd-1096.md"
        source_file.write_text(
            "---\n"
            "id: law-pd-1096\n"
            "title: PD 1096\n"
            "---\n\n"
            "## Section 1\n"
            "Building permits are required.\n",
            encoding="utf-8",
        )

        builder = UnifiedSnapshotBuilder(repo_root=tmp_path)
        snapshot = builder.build()

        # Should have canonical nodes
        assert len(snapshot.canonical_nodes) >= 2  # taxonomy + concept
        node_ids = {n.id for n in snapshot.canonical_nodes}
        assert "taxonomy-building-code" in node_ids
        assert "concept-building-permit" in node_ids

        # Should have document versions
        assert len(snapshot.document_versions) >= 1

        # Should have placement assertions
        concept_placements = [
            p for p in snapshot.placement_assertions if p.node_id == "concept-building-permit"
        ]
        assert len(concept_placements) >= 1

        # Should have fast edges
        assert len(snapshot.fast_edges) >= 1
        placement_edges = [
            e for e in snapshot.fast_edges if e["edge_type"] == "BELONGS_TO"
        ]
        assert len(placement_edges) >= 1

    def test_write_snapshot_roundtrip(self, tmp_path: Path) -> None:
        canonical_root = tmp_path / "003_Canonical-Knowledge-Layer" / "shared"
        taxonomy_dir = canonical_root / "taxonomy"
        taxonomy_dir.mkdir(parents=True)
        taxonomy_file = taxonomy_dir / "root.md"
        taxonomy_file.write_text(
            "---\nid: taxonomy-root\ntitle: Root\ncanonical_status: verified\n---\n",
            encoding="utf-8",
        )

        builder = UnifiedSnapshotBuilder(repo_root=tmp_path)
        snapshot = builder.build()
        out_path = builder.write_snapshot(snapshot=snapshot, out_path=tmp_path / "out.json")
        assert out_path.exists()

        loaded = KgV2Snapshot.read(out_path)
        assert len(loaded.canonical_nodes) == len(snapshot.canonical_nodes)
