"""Tests for EdgeMaterializer placement support."""

from __future__ import annotations

from vitruvius.kg.edge_materializer import EdgeMaterializer
from vitruvius.kg.enums import EdgeType, ValidationState
from vitruvius.kg.schemas import PlacementAssertion, RelationshipAssertion


def _make_relationship_assertion(
    status: ValidationState = ValidationState.VALIDATED,
) -> RelationshipAssertion:
    return RelationshipAssertion(
        id="assert-rel-001",
        edge_type=EdgeType.RELATED_TO,
        from_node_id="concept-a",
        to_node_id="concept-b",
        reasoning_summary="Reason",
        inference_type="direct_citation",
        confidence=0.9,
        validation_status=status,
        evidence_ids=["span-001"],
    )


def _make_placement_assertion(
    status: ValidationState = ValidationState.VALIDATED,
) -> PlacementAssertion:
    return PlacementAssertion(
        id="assert-placement-001",
        node_id="concept-a",
        parent_node_id="taxonomy-root",
        reasoning_summary="Placed by rule",
        confidence=0.85,
        validation_status=status,
        evidence_ids=["span-002"],
    )


class TestMaterializePlacements:
    def test_creates_belongs_to_edge(self) -> None:
        mat = EdgeMaterializer()
        placements = [_make_placement_assertion()]
        edges = mat.materialize_placements(placements)
        assert len(edges) == 1
        assert edges[0].edge_type == EdgeType.BELONGS_TO
        assert edges[0].from_node_id == "concept-a"
        assert edges[0].to_node_id == "taxonomy-root"
        assert edges[0].assertion_id == "assert-placement-001"

    def test_skips_unvalidated_when_flag_set(self) -> None:
        mat = EdgeMaterializer()
        placements = [_make_placement_assertion(ValidationState.CANDIDATE)]
        edges = mat.materialize_placements(placements, skip_unvalidated=True)
        assert len(edges) == 0

    def test_includes_unvalidated_when_flag_clear(self) -> None:
        mat = EdgeMaterializer()
        placements = [_make_placement_assertion(ValidationState.CANDIDATE)]
        edges = mat.materialize_placements(placements, skip_unvalidated=False)
        assert len(edges) == 1

    def test_mixed_with_relationship_edges(self) -> None:
        mat = EdgeMaterializer()
        rels = [_make_relationship_assertion()]
        placements = [_make_placement_assertion()]
        mat.materialize(rels)
        mat.materialize_placements(placements)
        payload = mat.write_snapshot(out_path=None)
        assert payload["edge_count"] == 2
        types = {e["edge_type"] for e in payload["edges"]}
        assert types == {"RELATED_TO", "BELONGS_TO"}
