"""Tests for PlacementEngine."""

from __future__ import annotations

import pytest

from vitruvius.kg.placement_engine import PlacementEngine
from vitruvius.kg.schemas import CanonicalNode, TaxonomyNode
from vitruvius.kg.enums import NodeType


def _make_taxonomy_node(path: list[str], embedding: list[float] | None = None) -> TaxonomyNode:
    return TaxonomyNode(
        id="taxonomy-" + "-".join(path),
        path=path,
        label=" ".join(path).title(),
        embedding=embedding,
    )


def _make_canonical_node(
    node_type: NodeType = NodeType.CONCEPT,
    label: str = "Test",
    embedding_ref: str | None = None,
) -> CanonicalNode:
    return CanonicalNode(
        id=f"{node_type.value}-{label.lower().replace(' ', '-')}",
        type=node_type,
        label=label,
        slug=label.lower().replace(" ", "-"),
        summary="Summary",
        taxonomy_path=[],
        aliases=[],
        status="candidate",
        confidence=0.9,
        version=1,
        created_at="2026-01-01T00:00:00Z",
        updated_at="2026-01-01T00:00:00Z",
        embedding_ref=embedding_ref,
    )


class TestRuleBasedPlacement:
    def test_concept_placed_under_concepts(self) -> None:
        tax = [_make_taxonomy_node(["concepts"])]
        engine = PlacementEngine(tax)
        node = _make_canonical_node(NodeType.CONCEPT, "Permit")
        paths = engine.place(node)
        assert paths == ["concepts"]

    def test_rule_placed_under_rules(self) -> None:
        tax = [_make_taxonomy_node(["rules"])]
        engine = PlacementEngine(tax)
        node = _make_canonical_node(NodeType.RULE, "Max Height")
        paths = ["rules"]

    def test_procedure_placed_under_procedures(self) -> None:
        tax = [_make_taxonomy_node(["procedures"])]
        engine = PlacementEngine(tax)
        node = _make_canonical_node(NodeType.PROCEDURE, "Inspection")
        paths = engine.place(node)
        assert paths == ["procedures"]

    def test_exception_placed_under_exceptions(self) -> None:
        tax = [_make_taxonomy_node(["exceptions"])]
        engine = PlacementEngine(tax)
        node = _make_canonical_node(NodeType.EXCEPTION, "Historic Building")
        paths = engine.place(node)
        assert paths == ["exceptions"]

    def test_definition_placed_under_concepts_definitions(self) -> None:
        tax = [_make_taxonomy_node(["concepts", "definitions"])]
        engine = PlacementEngine(tax)
        node = _make_canonical_node(NodeType.DEFINITION, "Setback")
        paths = engine.place(node)
        assert paths == ["concepts/definitions"]


class TestFallbackPlacement:
    def test_fallback_to_root_when_no_rule_match(self) -> None:
        tax = [_make_taxonomy_node(["other"])]
        engine = PlacementEngine(tax)
        node = _make_canonical_node(NodeType.CONCEPT, "X")
        paths = engine.place(node)
        # No "concepts" in taxonomy, so falls back to "/"
        assert paths == ["/"]

    def test_empty_taxonomy_fallback(self) -> None:
        engine = PlacementEngine([])
        node = _make_canonical_node(NodeType.CONCEPT, "X")
        paths = engine.place(node)
        assert paths == ["/"]


class TestEmbeddingPlacement:
    def test_embedding_similarity_placement(self) -> None:
        tax = [
            _make_taxonomy_node(["concepts"], embedding=[1.0, 0.0, 0.0]),
            _make_taxonomy_node(["rules"], embedding=[0.0, 1.0, 0.0]),
        ]
        engine = PlacementEngine(tax)
        # Node embedding closer to concepts
        node = _make_canonical_node(
            NodeType.CONCEPT, "X", embedding_ref="[0.95, 0.1, 0.0]"
        )
        paths = engine.place(node)
        assert paths == ["concepts"]

    def test_embedding_fallback_when_no_embedding(self) -> None:
        tax = [_make_taxonomy_node(["other"], embedding=[1.0, 0.0, 0.0])]
        engine = PlacementEngine(tax)
        node = _make_canonical_node(NodeType.CONCEPT, "X", embedding_ref=None)
        paths = engine.place(node)
        # Falls back to "/" because no rule match and no embedding
        assert paths == ["/"]


class TestAmbiguity:
    def test_ambiguity_when_top_two_close(self) -> None:
        tax = [
            _make_taxonomy_node(["topics"], embedding=[1.0, 0.0, 0.0]),
            _make_taxonomy_node(["areas"], embedding=[0.95, 0.1, 0.0]),
        ]
        engine = PlacementEngine(tax)
        # Use TERM to bypass rule-based tier
        node = _make_canonical_node(
            NodeType.TERM, "X", embedding_ref="[0.97, 0.05, 0.0]"
        )
        paths = engine.place(node)
        # Top path should be topics (most similar)
        assert paths[0] == "topics"
        # Both paths returned because scores are within 0.1
        assert len(paths) == 2
        # Ambiguity check
        assert engine.is_ambiguous(node, paths)

    def test_not_ambiguous_when_scores_far_apart(self) -> None:
        tax = [
            _make_taxonomy_node(["concepts"], embedding=[1.0, 0.0, 0.0]),
            _make_taxonomy_node(["rules"], embedding=[0.0, 1.0, 0.0]),
        ]
        engine = PlacementEngine(tax)
        node = _make_canonical_node(
            NodeType.CONCEPT, "X", embedding_ref="[0.99, 0.01, 0.0]"
        )
        paths = engine.place(node)
        assert not engine.is_ambiguous(node, paths)
