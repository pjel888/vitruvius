"""Ontology prompt builder — graph neighborhood rendering (Task F.3)."""

from __future__ import annotations

import dataclasses

import pytest

from vitruvius.review.ontology_prompt_builder import (
    GraphEdgeSummary,
    NeighborhoodPrompt,
    build_neighborhood_prompt,
    extract_neighborhood,
)


def _sample_edges() -> list[GraphEdgeSummary]:
    return [
        GraphEdgeSummary(from_id="concept-setback", to_id="concept-r1-zone", predicate="governs", confidence=0.92),
        GraphEdgeSummary(from_id="concept-building", to_id="concept-setback", predicate="requires", confidence=0.88),
        GraphEdgeSummary(from_id="concept-r1-zone", to_id="concept-max-height", predicate="limits", confidence=0.91),
        GraphEdgeSummary(from_id="concept-max-height", to_id="concept-meters", predicate="measured-in", confidence=0.80),
        GraphEdgeSummary(from_id="concept-other", to_id="concept-isolated", predicate="irrelevant", confidence=0.10),
    ]


def test_extract_neighborhood_1_hop():
    edges = _sample_edges()
    result = extract_neighborhood(edges, focal_node="concept-setback", max_hops=1)
    # should contain both edges touching concept-setback
    connected_ids = {e.from_id for e in result} | {e.to_id for e in result}
    assert "concept-setback" in connected_ids
    assert len(result) == 2


def test_extract_neighborhood_2_hop():
    edges = _sample_edges()
    result = extract_neighborhood(edges, focal_node="concept-setback", max_hops=2)
    # 2-hop from setback should include concept-r1-zone -> concept-max-height
    predicates = {e.predicate for e in result}
    assert "governs" in predicates
    assert "requires" in predicates
    assert "limits" in predicates
    # but not concept-other/concept-isolated (not reachable)
    all_ids = {e.from_id for e in result} | {e.to_id for e in result}
    assert "concept-isolated" not in all_ids


def test_extract_max_edges_per_hop_cap():
    edges = [
        GraphEdgeSummary(from_id="n", to_id=f"x{i}", predicate="p", confidence=0.5)
        for i in range(20)
    ]
    result = extract_neighborhood(edges, focal_node="n", max_hops=1, max_edges_per_hop=5)
    assert len(result) == 5


def test_extract_deterministic_output():
    edges = _sample_edges()
    a = extract_neighborhood(edges, focal_node="concept-setback", max_hops=2)
    b = extract_neighborhood(edges, focal_node="concept-setback", max_hops=2)
    assert a == b


def test_extract_empty_edge_set():
    result = extract_neighborhood([], focal_node="concept-anything", max_hops=2)
    assert result == []


def test_extract_unknown_focal_node():
    edges = _sample_edges()
    result = extract_neighborhood(edges, focal_node="concept-nonexistent", max_hops=2)
    assert result == []


def test_build_neighborhood_prompt_contains_both_neighborhoods():
    edges = _sample_edges()
    prompt = build_neighborhood_prompt(
        candidate_subject="concept-setback",
        candidate_object="concept-r1-zone",
        edges=edges,
    )
    assert "concept-setback" in prompt.rendered_text
    assert "concept-r1-zone" in prompt.rendered_text
    assert "Subject neighborhood" in prompt.rendered_text
    assert "Object neighborhood" in prompt.rendered_text


def test_build_neighborhood_prompt_rendered_contains_predicate_arrows():
    edges = _sample_edges()
    prompt = build_neighborhood_prompt(
        candidate_subject="concept-setback",
        candidate_object="concept-r1-zone",
        edges=edges,
    )
    assert "governs" in prompt.rendered_text
    assert "--[" in prompt.rendered_text
    assert "]-->" in prompt.rendered_text


def test_build_neighborhood_prompt_is_frozen():
    edges = _sample_edges()
    prompt = build_neighborhood_prompt(
        candidate_subject="concept-setback",
        candidate_object="concept-r1-zone",
        edges=edges,
    )
    with pytest.raises(dataclasses.FrozenInstanceError):
        prompt.rendered_text = "mutated"  # type: ignore[misc]


def test_build_neighborhood_prompt_empty_edges():
    prompt = build_neighborhood_prompt(
        candidate_subject="concept-setback",
        candidate_object="concept-r1-zone",
        edges=[],
    )
    assert prompt.subject_neighborhood == ()
    assert prompt.object_neighborhood == ()
    assert "concept-setback" in prompt.rendered_text
    assert "concept-r1-zone" in prompt.rendered_text
