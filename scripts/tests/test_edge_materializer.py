"""Tests for ``vitruvius.kg.edge_materializer`` and its integration with the evidence pipeline."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from vitruvius.kg.edge_materializer import EdgeMaterializer, FastEdge
from vitruvius.kg.enums import EdgeType, InferenceType, ValidationState
from vitruvius.kg.evidence_materializer import EvidenceMaterializer
from vitruvius.kg.json_evidence_store import KgV2Snapshot
from vitruvius.kg.schemas import (
    CanonicalNode,
    CreatedBy,
    EvidenceSpan,
    RelationshipAssertion,
    TextRangeSelector,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_snapshot(
    *,
    with_nodes: bool = True,
    with_evidence: bool = True,
    validation_status: ValidationState = ValidationState.VALIDATED,
) -> KgV2Snapshot:
    snap = KgV2Snapshot()
    if with_nodes:
        snap.canonical_nodes.extend(
            [
                CanonicalNode(
                    id="concept-floor-area",
                    type="concept",
                    label="Floor Area",
                    slug="floor-area",
                ),
                CanonicalNode(
                    id="concept-building-height",
                    type="concept",
                    label="Building Height",
                    slug="building-height",
                ),
            ]
        )
    if with_evidence:
        snap.evidence_spans.append(
            EvidenceSpan(
                id="span-001",
                document_id="doc-test",
                document_version_id="docv-test-v1",
                selector=TextRangeSelector(kind="text_range", quote="test", char_start=0, char_end=4),
                quote="test",
                normalized_text="test",
                parser="test",
                checksum="a" * 64,
            )
        )
    snap.relationship_assertions.append(
        RelationshipAssertion(
            id="assert-rel-001",
            edge_type=EdgeType.RELATED_TO,
            from_node_id="concept-floor-area",
            to_node_id="concept-building-height",
            reasoning_summary="Both govern spatial parameters.",
            inference_type=InferenceType.DIRECT_CITATION,
            confidence=0.92,
            validation_status=validation_status,
            evidence_ids=["span-001"],
        )
    )
    return snap


# ---------------------------------------------------------------------------
# Fixture (local copy so this test file is self-contained)
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
# EdgeMaterializer unit tests
# ---------------------------------------------------------------------------

class TestEdgeMaterializer:
    def test_materialize_happy_path(self) -> None:
        snap = _make_snapshot()
        mat = EdgeMaterializer(snapshot=snap)
        edges = mat.materialize(snap.relationship_assertions, skip_unvalidated=True)

        assert len(edges) == 1
        edge = edges[0]
        assert isinstance(edge, FastEdge)
        assert edge.id == "edge-assert-rel-001"
        assert edge.edge_type == EdgeType.RELATED_TO
        assert edge.from_node_id == "concept-floor-area"
        assert edge.to_node_id == "concept-building-height"
        assert edge.confidence == 0.92
        assert edge.validation_status == ValidationState.VALIDATED
        assert edge.evidence_span_count == 1

    def test_materialize_skips_unvalidated_when_flag_set(self) -> None:
        snap = _make_snapshot(validation_status=ValidationState.CANDIDATE)
        mat = EdgeMaterializer(snapshot=snap)
        edges = mat.materialize(snap.relationship_assertions, skip_unvalidated=True)
        assert len(edges) == 0

    def test_materialize_includes_unvalidated_when_flag_clear(self) -> None:
        snap = _make_snapshot(validation_status=ValidationState.CANDIDATE)
        mat = EdgeMaterializer(snapshot=snap)
        edges = mat.materialize(snap.relationship_assertions, skip_unvalidated=False)
        assert len(edges) == 1
        assert edges[0].validation_status == ValidationState.CANDIDATE

    def test_write_snapshot_returns_payload(self) -> None:
        snap = _make_snapshot()
        mat = EdgeMaterializer(snapshot=snap)
        mat.materialize(snap.relationship_assertions)
        payload = mat.write_snapshot(out_path=None)

        assert payload["schema_version"] == "2.0.0-alpha"
        assert payload["edge_count"] == 1
        assert len(payload["edges"]) == 1
        assert payload["edges"][0]["from_node_id"] == "concept-floor-area"

    def test_write_snapshot_to_disk(self, tmp_path: Path) -> None:
        snap = _make_snapshot()
        mat = EdgeMaterializer(snapshot=snap)
        mat.materialize(snap.relationship_assertions)
        out = tmp_path / "edges.json"
        mat.write_snapshot(out_path=out)

        data = json.loads(out.read_text(encoding="utf-8"))
        assert data["edge_count"] == 1
        assert data["edges"][0]["id"] == "edge-assert-rel-001"

    def test_multiple_assertions_accumulate(self) -> None:
        snap = _make_snapshot()
        snap.relationship_assertions.append(
            RelationshipAssertion(
                id="assert-rel-002",
                edge_type=EdgeType.DEPENDS_ON,
                from_node_id="concept-building-height",
                to_node_id="concept-floor-area",
                reasoning_summary="Height depends on floor plate.",
                inference_type=InferenceType.DIRECT_CITATION,
                confidence=0.85,
                validation_status=ValidationState.VALIDATED,
                evidence_ids=["span-001"],
            )
        )
        mat = EdgeMaterializer(snapshot=snap)
        edges = mat.materialize(snap.relationship_assertions)
        assert len(edges) == 2
        assert edges[0].id == "edge-assert-rel-001"
        assert edges[1].id == "edge-assert-rel-002"


# ---------------------------------------------------------------------------
# EvidenceMaterializer integration tests
# ---------------------------------------------------------------------------

class TestEvidenceMaterializerIntegration:
    def test_fast_edges_produced_for_valid_assertions(self, fake_repo: Path) -> None:
        # The fake_repo fixture creates a relationship with concept endpoints
        # that do NOT exist in the concepts dir, so validation will fail.
        # Add the missing concept files so the relationship passes validation.
        concepts_dir = fake_repo / "003_Canonical-Knowledge-Layer" / "shared" / "concepts"
        (concepts_dir / "floor-area.md").write_text(
            "---\n"
            "id: concept-floor-area\n"
            "title: Floor Area\n"
            "canonical_status: enriched\n"
            "---\n\n"
            "# Floor Area\n\n"
            "## Definition\n\n"
            "Total floor area.\n"
        )
        (concepts_dir / "building-height.md").write_text(
            "---\n"
            "id: concept-building-height\n"
            "title: Building Height\n"
            "canonical_status: enriched\n"
            "---\n\n"
            "# Building Height\n\n"
            "## Definition\n\n"
            "Total height.\n"
        )

        mat = EvidenceMaterializer(fake_repo)
        snapshot = mat.materialize_all()

        assert len(snapshot.fast_edges) == 1
        edge = snapshot.fast_edges[0]
        assert edge["from_node_id"] == "concept-floor-area"
        assert edge["to_node_id"] == "concept-building-height"
        assert edge["edge_type"] == "RELATED_TO"

    def test_no_fast_edges_when_validation_fails(self, fake_repo: Path) -> None:
        # fake_repo relationship references concept-floor-area / concept-building-height
        # which are absent from concepts dir → validation fails → no edges
        mat = EvidenceMaterializer(fake_repo)
        snapshot = mat.materialize_all()
        assert len(snapshot.fast_edges) == 0

    def test_snapshot_roundtrip_preserves_fast_edges(self, fake_repo: Path, tmp_path: Path) -> None:
        concepts_dir = fake_repo / "003_Canonical-Knowledge-Layer" / "shared" / "concepts"
        (concepts_dir / "floor-area.md").write_text(
            "---\n"
            "id: concept-floor-area\n"
            "title: Floor Area\n"
            "canonical_status: enriched\n"
            "---\n\n"
            "# Floor Area\n\n"
            "## Definition\n\n"
            "Total floor area.\n"
        )
        (concepts_dir / "building-height.md").write_text(
            "---\n"
            "id: concept-building-height\n"
            "title: Building Height\n"
            "canonical_status: enriched\n"
            "---\n\n"
            "# Building Height\n\n"
            "## Definition\n\n"
            "Total height.\n"
        )

        mat = EvidenceMaterializer(fake_repo)
        snapshot = mat.materialize_all()
        path = tmp_path / "snapshot.json"
        snapshot.write(path)
        loaded = KgV2Snapshot.read(path)

        assert len(loaded.fast_edges) == 1
        assert loaded.fast_edges[0]["assertion_id"] == "assert-rel-concept-floor-area-affects-concept-building-height"


# ---------------------------------------------------------------------------
# R2 edge_type validation
# ---------------------------------------------------------------------------

class TestEdgeTypeValidation:
    def test_r2_rejects_unknown_edge_type(self) -> None:
        from vitruvius.kg.assertion_validator import AssertionValidator

        snap = _make_snapshot()
        # Corrupt the edge_type by using model_construct with a string
        assertion = RelationshipAssertion.model_construct(
            id="assert-rel-bad",
            edge_type="bogus_type",  # type: ignore[arg-type]
            from_node_id="concept-floor-area",
            to_node_id="concept-building-height",
            reasoning_summary="Valid summary.",
            inference_type=InferenceType.DIRECT_CITATION,
            confidence=0.92,
            evidence_ids=["span-001"],
        )
        validator = AssertionValidator(
            canonical_index={
                "concept-floor-area": {"type": "concept"},
                "concept-building-height": {"type": "concept"},
            },
            evidence_index={"span-001": {"id": "span-001"}},
        )
        result = validator.validate_relationship(assertion)
        assert not result.passed
        assert any("R2" in e for e in result.errors)
