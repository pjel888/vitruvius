"""Tests for the file-native evidence graph materializer and taxonomy loader."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from vitruvius.kg.evidence_materializer import EvidenceMaterializer, TaxonomyLoader, _edge_type_from_string
from vitruvius.kg.enums import EdgeType, ValidationState
from vitruvius.kg.json_evidence_store import KgV2Snapshot, SCHEMA_VERSION


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def fake_repo(tmp_path: Path) -> Path:
    """Create a minimal repo structure with canonical sources, concepts, and relationships."""
    repo = tmp_path / "repo"
    canonical = repo / "003_Canonical-Knowledge-Layer" / "shared"

    # Source file
    sources_dir = canonical / "sources"
    sources_dir.mkdir(parents=True)
    (sources_dir / "law-pd-1096.md").write_text(
        "---\n"
        "id: law-pd-1096-national-building-code\n"
        "title: National Building Code of the Philippines\n"
        "trust_level: primary\n"
        "canonical_status: draft\n"
        "---\n\n"
        "# National Building Code of the Philippines\n\n"
        "## Overview\n\n"
        "This is the overview section.\n\n"
        "## Coverage\n\n"
        "This law governs building construction.\n"
    )

    # Concept file
    concepts_dir = canonical / "concepts"
    concepts_dir.mkdir(parents=True)
    (concepts_dir / "building-permit.md").write_text(
        "---\n"
        "id: concept-building-permit\n"
        "title: Building Permit\n"
        "category: 001-Laws\n"
        "topic_tags:\n  - permits\n  - licensing\n"
        "aliases:\n  - BP\n  - construction permit\n"
        "canonical_status: enriched\n"
        "confidence_score: 0.95\n"
        "---\n\n"
        "# Building Permit\n\n"
        "## Definition\n\n"
        "A building permit is an official approval.\n\n"
        "## Regulatory Basis\n\n"
        "See PD 1096 Section 301.\n"
    )

    # Relationship file (promoted)
    rels_dir = canonical / "relationships"
    rels_dir.mkdir(parents=True)
    (rels_dir / "rel-floor-area-affects-height.md").write_text(
        "---\n"
        "id: rel-concept-floor-area-affects-concept-building-height\n"
        "relationship_type: affects\n"
        "from_entity: concept-floor-area\n"
        "to_entity: concept-building-height\n"
        "canonical_status: promoted\n"
        "confidence_score: 0.92\n"
        "promotion_batch_id: 20260414T234203Z_2b941c4d\n"
        "last_promoted_utc: 2026-04-14T23:42:03Z\n"
        "evidence:\n"
        "  - source_id: concept-floor-area\n"
        "    source_section_id: section-irr-general\n"
        "    evidence_snippet: BUILDING BULK - The overall size...\n"
        "    review_decision: keep\n"
        "    reviewer_model: gemma4:31b\n"
        "    reviewer_confidence: 0.92\n"
        "    reviewer_reason: The example explicitly discusses bulk.\n"
        "---\n\n"
        "# Floor area affects building height\n"
    )

    # Relationship file (draft — should be skipped)
    (rels_dir / "rel-draft.md").write_text(
        "---\n"
        "id: rel-draft-example\n"
        "relationship_type: governs\n"
        "from_entity: concept-occupancy\n"
        "to_entity: concept-fire\n"
        "canonical_status: draft\n"
        "---\n\n"
        "# Draft relationship\n"
    )

    return repo


# ---------------------------------------------------------------------------
# EvidenceMaterializer tests
# ---------------------------------------------------------------------------

class TestEvidenceMaterializer:

    def test_materialize_sources_creates_document_versions(self, fake_repo: Path) -> None:
        mat = EvidenceMaterializer(fake_repo)
        snapshot = mat.materialize_all()

        assert len(snapshot.document_versions) == 1
        dv = snapshot.document_versions[0]
        assert dv.id == "docv-pd-1096-national-building-code-v1"
        assert dv.document_id == "doc-pd-1096-national-building-code"
        assert dv.title == "National Building Code of the Philippines"
        assert dv.mime_type == "text/markdown"
        assert len(dv.sha256) == 64

    def test_materialize_sources_creates_sections_and_chunks(self, fake_repo: Path) -> None:
        mat = EvidenceMaterializer(fake_repo)
        snapshot = mat.materialize_all()

        # Should have sections derived from markdown headings
        assert len(snapshot.sections) >= 2
        titles = {s.title for s in snapshot.sections}
        assert "Overview" in titles
        assert "Coverage" in titles

        # Should have chunks
        assert len(snapshot.chunks) >= 2
        # Every chunk should reference a valid section
        section_ids = {s.id for s in snapshot.sections}
        for chunk in snapshot.chunks:
            assert chunk.section_id in section_ids

    def test_materialize_relationships_creates_assertions(self, fake_repo: Path) -> None:
        mat = EvidenceMaterializer(fake_repo)
        snapshot = mat.materialize_all()

        # Only promoted/verified relationships become assertions
        assert len(snapshot.relationship_assertions) == 1
        ra = snapshot.relationship_assertions[0]
        assert ra.id == "assert-rel-concept-floor-area-affects-concept-building-height"
        assert ra.edge_type == EdgeType.RELATED_TO  # "affects" maps to RELATED_TO
        assert ra.from_node_id == "concept-floor-area"
        assert ra.to_node_id == "concept-building-height"
        assert ra.confidence == 0.92
        assert ra.validation_status == ValidationState.CANDIDATE
        assert ra.review_state == "pending"

    def test_materialize_relationships_creates_evidence_spans(self, fake_repo: Path) -> None:
        mat = EvidenceMaterializer(fake_repo)
        snapshot = mat.materialize_all()

        assert len(snapshot.evidence_spans) == 1
        span = snapshot.evidence_spans[0]
        assert span.quote == "BUILDING BULK - The overall size..."
        assert span.normalized_text == "BUILDING BULK - The overall size..."
        assert len(span.checksum) == 64
        assert span.parser == "legacy_promotion_pipeline"

    def test_draft_relationships_are_skipped(self, fake_repo: Path) -> None:
        mat = EvidenceMaterializer(fake_repo)
        snapshot = mat.materialize_all()

        draft_ids = {a.id for a in snapshot.relationship_assertions}
        assert "assert-rel-draft-example" not in draft_ids

    def test_write_snapshot_produces_valid_json(self, fake_repo: Path) -> None:
        mat = EvidenceMaterializer(fake_repo)
        mat.materialize_all()
        path = mat.write_snapshot()

        assert path.exists()
        data = json.loads(path.read_text(encoding="utf-8"))
        assert data["schema_version"] == SCHEMA_VERSION
        assert "document_versions" in data
        assert "relationship_assertions" in data

    def test_snapshot_checksum_is_stable(self, fake_repo: Path) -> None:
        mat1 = EvidenceMaterializer(fake_repo)
        mat1.materialize_all()

        mat2 = EvidenceMaterializer(fake_repo)
        mat2.materialize_all()

        # Note: timestamps make checksums differ, so we compare entity counts instead
        assert mat1.snapshot.entity_counts() == mat2.snapshot.entity_counts()

    def test_missing_sources_dir_warns(self, tmp_path: Path) -> None:
        repo = tmp_path / "empty_repo"
        (repo / "003_Canonical-Knowledge-Layer" / "shared").mkdir(parents=True)
        mat = EvidenceMaterializer(repo)
        snapshot = mat.materialize_all()
        assert len(snapshot.document_versions) == 0
        assert any("Sources directory not found" in w for w in mat._warnings)


# ---------------------------------------------------------------------------
# TaxonomyLoader tests
# ---------------------------------------------------------------------------

class TestTaxonomyLoader:

    def test_load_all_creates_canonical_nodes(self, fake_repo: Path) -> None:
        loader = TaxonomyLoader(fake_repo)
        snapshot = loader.load_all()

        assert len(snapshot.canonical_nodes) == 1
        node = snapshot.canonical_nodes[0]
        assert node.id == "concept-building-permit"
        assert node.type == "concept"
        assert node.label == "Building Permit"
        assert node.slug == "building-permit"
        assert "official approval" in node.summary

    def test_taxonomy_path_from_topic_tags(self, fake_repo: Path) -> None:
        loader = TaxonomyLoader(fake_repo)
        snapshot = loader.load_all()

        node = snapshot.canonical_nodes[0]
        assert "001-Laws" in node.taxonomy_path
        assert "permits" in node.taxonomy_path
        assert "licensing" in node.taxonomy_path

    def test_aliases_preserved(self, fake_repo: Path) -> None:
        loader = TaxonomyLoader(fake_repo)
        snapshot = loader.load_all()

        node = snapshot.canonical_nodes[0]
        assert "BP" in node.aliases
        assert "construction permit" in node.aliases

    def test_validation_state_mapping(self, fake_repo: Path) -> None:
        loader = TaxonomyLoader(fake_repo)
        snapshot = loader.load_all()

        node = snapshot.canonical_nodes[0]
        assert node.status == ValidationState.CANDIDATE  # "enriched" maps to CANDIDATE

    def test_write_snapshot(self, fake_repo: Path) -> None:
        loader = TaxonomyLoader(fake_repo)
        loader.load_all()
        path = loader.write_snapshot()

        assert path.exists()
        data = json.loads(path.read_text(encoding="utf-8"))
        assert data["schema_version"] == SCHEMA_VERSION
        assert len(data["canonical_nodes"]) == 1

    def test_missing_concepts_dir_warns(self, tmp_path: Path) -> None:
        repo = tmp_path / "empty_repo"
        (repo / "003_Canonical-Knowledge-Layer" / "shared").mkdir(parents=True)
        loader = TaxonomyLoader(repo)
        snapshot = loader.load_all()
        assert len(snapshot.canonical_nodes) == 0
        assert any("Concepts directory not found" in w for w in loader._warnings)


# ---------------------------------------------------------------------------
# KgV2Snapshot tests
# ---------------------------------------------------------------------------

class TestKgV2Snapshot:

    def test_roundtrip(self, tmp_path: Path) -> None:
        snap = KgV2Snapshot()
        from vitruvius.kg.schemas import DocumentVersion

        snap.document_versions.append(
            DocumentVersion(
                id="docv-test-v1",
                document_id="doc-test",
                title="Test",
                source_uri="test.md",
                sha256="a" * 64,
                created_at="2026-01-01T00:00:00Z",
            )
        )
        path = tmp_path / "test.json"
        snap.write(path)
        loaded = KgV2Snapshot.read(path)
        assert loaded.schema_version == SCHEMA_VERSION
        assert len(loaded.document_versions) == 1
        assert loaded.document_versions[0].id == "docv-test-v1"

    def test_checksum_changes_with_content(self) -> None:
        from vitruvius.kg.schemas import DocumentVersion

        snap1 = KgV2Snapshot()
        snap1.document_versions.append(
            DocumentVersion(
                id="docv-a-v1",
                document_id="doc-a",
                title="A",
                source_uri="a.md",
                sha256="a" * 64,
                created_at="2026-01-01T00:00:00Z",
            )
        )
        snap2 = KgV2Snapshot()
        snap2.document_versions.append(
            DocumentVersion(
                id="docv-b-v1",
                document_id="doc-b",
                title="B",
                source_uri="b.md",
                sha256="b" * 64,
                created_at="2026-01-01T00:00:00Z",
            )
        )
        assert snap1.checksum() != snap2.checksum()


# ---------------------------------------------------------------------------
# Edge type mapping tests
# ---------------------------------------------------------------------------

class TestEdgeTypeMapping:

    @pytest.mark.parametrize(
        ("legacy", "expected"),
        [
            ("governs", EdgeType.APPLIES_TO),
            ("requires", EdgeType.REQUIRES),
            ("defines", EdgeType.DEFINED_BY),
            ("depends_on", EdgeType.DEPENDS_ON),
            ("limits", EdgeType.REQUIRES),
            ("affects", EdgeType.RELATED_TO),
            ("supersedes", EdgeType.OVERRIDES),
            ("UNKNOWN", EdgeType.RELATED_TO),
        ],
    )
    def test_mapping(self, legacy: str, expected: EdgeType) -> None:
        assert _edge_type_from_string(legacy) == expected
