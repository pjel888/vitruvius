"""Tests for MergeAdjudicator."""

from __future__ import annotations

import pytest

from vitruvius.kg.merge_adjudicator import MergeAdjudicator
from vitruvius.kg.schemas import CanonicalNode, MergeAssertion
from vitruvius.kg.enums import NodeType, ValidationState


def _make_node(
    node_type: NodeType = NodeType.CONCEPT,
    label: str = "Test",
    node_id: str | None = None,
) -> CanonicalNode:
    slug = label.lower().replace(" ", "-")
    return CanonicalNode(
        id=node_id or f"{node_type.value}-{slug}",
        type=node_type,
        label=label,
        slug=slug,
        summary="Summary",
        taxonomy_path=[],
        aliases=[],
        status="candidate",
        confidence=0.9,
        version=1,
        created_at="2026-01-01T00:00:00Z",
        updated_at="2026-01-01T00:00:00Z",
    )


class TestNoMerges:
    def test_empty_nodes(self) -> None:
        adj = MergeAdjudicator()
        assert adj.propose([]) == []

    def test_single_node(self) -> None:
        adj = MergeAdjudicator()
        nodes = [_make_node(NodeType.CONCEPT, "A")]
        assert adj.propose(nodes) == []

    def test_unique_nodes_no_merge(self) -> None:
        adj = MergeAdjudicator()
        nodes = [
            _make_node(NodeType.CONCEPT, "Building Permit"),
            _make_node(NodeType.CONCEPT, "Zoning Variance"),
        ]
        merges = adj.propose(nodes)
        assert len(merges) == 0


class TestExactMatchMerges:
    def test_exact_label_merge_proposed(self) -> None:
        adj = MergeAdjudicator()
        nodes = [
            _make_node(NodeType.CONCEPT, "Building Permit", "concept-a"),
            _make_node(NodeType.CONCEPT, "building permit", "concept-b"),
        ]
        merges = adj.propose(nodes)
        assert len(merges) == 1
        assert merges[0].from_node_id == "concept-a"
        assert merges[0].to_node_id == "concept-b"
        assert merges[0].validation_status == ValidationState.REVIEW_REQUIRED
        assert "building permit" in merges[0].reasoning_summary.lower()

    def test_different_types_not_merged(self) -> None:
        adj = MergeAdjudicator()
        nodes = [
            _make_node(NodeType.CONCEPT, "Permit", "concept-a"),
            _make_node(NodeType.RULE, "Permit", "rule-a"),
        ]
        merges = adj.propose(nodes)
        assert len(merges) == 0

    def test_three_way_merge_all_pairs(self) -> None:
        adj = MergeAdjudicator()
        nodes = [
            _make_node(NodeType.CONCEPT, "X", "concept-1"),
            _make_node(NodeType.CONCEPT, "x", "concept-2"),
            _make_node(NodeType.CONCEPT, "X ", "concept-3"),
        ]
        merges = adj.propose(nodes)
        # 3 nodes → C(3,2) = 3 pairs
        assert len(merges) == 3
        ids = {(m.from_node_id, m.to_node_id) for m in merges}
        assert ("concept-1", "concept-2") in ids
        assert ("concept-1", "concept-3") in ids
        assert ("concept-2", "concept-3") in ids

    def test_assertion_id_format(self) -> None:
        adj = MergeAdjudicator()
        nodes = [
            _make_node(NodeType.CONCEPT, "X", "concept-a"),
            _make_node(NodeType.CONCEPT, "X", "concept-b"),
        ]
        merges = adj.propose(nodes)
        assert len(merges) == 1
        assert merges[0].id.startswith("assert-merge-")

    def test_confidence_is_one(self) -> None:
        adj = MergeAdjudicator()
        nodes = [
            _make_node(NodeType.CONCEPT, "X", "concept-a"),
            _make_node(NodeType.CONCEPT, "X", "concept-b"),
        ]
        merges = adj.propose(nodes)
        assert merges[0].confidence == 1.0
