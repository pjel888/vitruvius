"""Tests for QueryEngine v2 canonical-first inspection methods."""

from __future__ import annotations

from pathlib import Path

import pytest

from vitruvius.kg.enums import EdgeType, InferenceType, ValidationState
from vitruvius.kg.json_evidence_store import KgV2Snapshot
from vitruvius.kg.query_engine import QueryEngine
from vitruvius.kg.schemas import (
    CanonicalNode,
    EvidenceSpan,
    MergeAssertion,
    PlacementAssertion,
    RelationshipAssertion,
    TextRangeSelector,
)


def _make_engine() -> QueryEngine:
    snap = KgV2Snapshot()

    # Nodes — include taxonomy root
    snap.canonical_nodes.extend(
        [
            CanonicalNode(
                id="taxonomy-building-code",
                type="taxonomy",
                label="Building Code",
                slug="building-code",
                taxonomy_path=["building-code"],
            ),
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

    # Evidence spans
    snap.evidence_spans.append(
        EvidenceSpan(
            id="span-001",
            document_id="doc-pd-1096",
            document_version_id="docv-pd-1096-v1",
            selector=TextRangeSelector(kind="text_range", char_start=0, char_end=10),
            quote="Floor area is defined as...",
            normalized_text="floor area defined",
            parser="test",
            checksum="a" * 64,
        )
    )

    # Relationship assertions
    snap.relationship_assertions.append(
        RelationshipAssertion(
            id="assert-rel-001",
            edge_type=EdgeType.RELATED_TO,
            from_node_id="concept-floor-area",
            to_node_id="concept-building-height",
            reasoning_summary="Both govern spatial parameters.",
            inference_type=InferenceType.DIRECT_CITATION,
            confidence=0.92,
            validation_status=ValidationState.VALIDATED,
            evidence_ids=["span-001"],
        )
    )

    # Placement assertions
    snap.placement_assertions.append(
        PlacementAssertion(
            id="assert-placement-001",
            node_id="concept-floor-area",
            parent_node_id="taxonomy-building-code",
            reasoning_summary="Placed under building code",
            confidence=0.9,
            validation_status=ValidationState.CANDIDATE,
            evidence_ids=["span-001"],
        )
    )

    # Merge assertions
    snap.merge_assertions.append(
        MergeAssertion(
            id="assert-merge-001",
            from_node_id="concept-floor-area",
            to_node_id="concept-building-height",
            reasoning_summary="Exact duplicate",
            confidence=1.0,
            validation_status=ValidationState.REVIEW_REQUIRED,
        )
    )

    return QueryEngine(snap)


class TestPlacementQueries:
    def test_get_placement_for_node(self) -> None:
        engine = _make_engine()
        placements = engine.get_placement_for_node("concept-floor-area")
        assert len(placements) == 1
        assert placements[0].parent_node_id == "taxonomy-building-code"

    def test_get_placement_empty_for_unknown(self) -> None:
        engine = _make_engine()
        assert engine.get_placement_for_node("concept-missing") == []


class TestMergeQueries:
    def test_get_merge_assertions_for_node(self) -> None:
        engine = _make_engine()
        merges = engine.get_merge_assertions_for_node("concept-floor-area")
        assert len(merges) == 1
        assert merges[0].to_node_id == "concept-building-height"

    def test_get_merge_assertions_bidirectional(self) -> None:
        engine = _make_engine()
        merges_from = engine.get_merge_assertions_for_node("concept-floor-area")
        merges_to = engine.get_merge_assertions_for_node("concept-building-height")
        assert len(merges_from) == 1
        assert len(merges_to) == 1
        assert merges_from[0].id == merges_to[0].id


class TestAssertionById:
    def test_get_relationship_assertion(self) -> None:
        engine = _make_engine()
        assertion = engine.get_assertion_by_id("assert-rel-001")
        assert assertion is not None
        assert assertion.confidence == 0.92

    def test_get_placement_assertion(self) -> None:
        engine = _make_engine()
        assertion = engine.get_assertion_by_id("assert-placement-001")
        assert assertion is not None
        assert assertion.node_id == "concept-floor-area"

    def test_get_merge_assertion(self) -> None:
        engine = _make_engine()
        assertion = engine.get_assertion_by_id("assert-merge-001")
        assert assertion is not None
        assert assertion.from_node_id == "concept-floor-area"

    def test_get_assertion_none_for_unknown(self) -> None:
        engine = _make_engine()
        assert engine.get_assertion_by_id("assert-missing") is None


class TestEvidenceQueries:
    def test_get_evidence_for_assertion(self) -> None:
        engine = _make_engine()
        spans = engine.get_evidence_for_assertion("assert-rel-001")
        assert len(spans) == 1
        assert spans[0].id == "span-001"

    def test_get_evidence_for_node(self) -> None:
        engine = _make_engine()
        spans = engine.get_evidence_for_node("concept-floor-area")
        assert len(spans) == 1
        assert spans[0].id == "span-001"

    def test_get_evidence_empty_for_unknown(self) -> None:
        engine = _make_engine()
        assert engine.get_evidence_for_assertion("assert-missing") == []
        assert engine.get_evidence_for_node("concept-missing") == []


class TestNeighborhood:
    def test_get_node_neighborhood(self) -> None:
        engine = _make_engine()
        neighbors = engine.get_node_neighborhood("concept-floor-area")
        assert len(neighbors) == 1
        node, assertion = neighbors[0]
        assert node.id == "concept-building-height"
        assert assertion.id == "assert-rel-001"

    def test_get_node_neighborhood_empty(self) -> None:
        engine = _make_engine()
        assert engine.get_node_neighborhood("taxonomy-building-code") == []


class TestTaxonomyTree:
    def test_get_taxonomy_tree(self) -> None:
        engine = _make_engine()
        roots = engine.get_taxonomy_tree()
        assert len(roots) == 1
        assert roots[0].id == "taxonomy-building-code"
