"""Stream I.1 — ontology-embedded NL prompt builder."""

from __future__ import annotations

import json

from vitruvius.graph.contract import GraphEdge, GraphNode, GraphSnapshot
from vitruvius.query.nl_translator import ALLOWED_FUNCTIONS
from vitruvius.query.ontology_prompt import build_ontology_prompt


def _n(id_: str, *, type_: str = "concept", trust: str = "derived") -> GraphNode:
    return GraphNode(
        id=id_,
        type=type_,
        slug=id_.split("-", 1)[-1] or "x",
        trust_level=trust,
        last_updated_utc="2026-04-14T00:00:00Z",
    )


def _e(from_id: str, to_id: str, *, type_: str = "governs",
       evidence: str = "rel-x") -> GraphEdge:
    return GraphEdge(
        from_id=from_id,
        to_id=to_id,
        type=type_,
        evidence_id=evidence,
        status="verified",
    )


def _snap(nodes, edges) -> GraphSnapshot:
    return GraphSnapshot(
        schema_version="1.0.0",
        generated_at_utc="2026-04-14T00:00:00Z",
        node_count=len(nodes),
        edge_count=len(edges),
        nodes=nodes,
        edges=edges,
    )


def _dense_snapshot() -> GraphSnapshot:
    nodes = [_n(f"concept-{c}") for c in "abcdefghij"]
    edges = [
        _e(f"concept-{a}", f"concept-{b}", evidence=f"rel-{a}{b}")
        for a, b in zip("abcdefghi", "bcdefghij")
    ]
    # Add extra hub edges so centrality has variance.
    edges += [
        _e("concept-a", "concept-c", evidence="rel-ac"),
        _e("concept-a", "concept-e", evidence="rel-ae"),
    ]
    return _snap(nodes, edges)


def test_prompt_contains_known_entities_and_allowed_functions() -> None:
    snap = _dense_snapshot()
    prompt = build_ontology_prompt(
        "What governs concept-a?",
        snapshot=snap,
        top_k_central=5,
    )
    payload = json.loads(prompt)
    assert payload["allowed_functions"] == list(ALLOWED_FUNCTIONS)
    assert payload["question"] == "What governs concept-a?"
    assert len(payload["known_entities"]) <= 5
    assert all(
        isinstance(eid, str) and eid.startswith("concept-")
        for eid in payload["known_entities"]
    )


def test_prompt_top_k_honoured() -> None:
    snap = _dense_snapshot()
    prompt = build_ontology_prompt(
        "q", snapshot=snap, top_k_central=3,
    )
    payload = json.loads(prompt)
    assert len(payload["known_entities"]) == 3


def test_prompt_includes_community_summaries() -> None:
    snap = _dense_snapshot()
    prompt = build_ontology_prompt("q", snapshot=snap, top_k_central=50)
    payload = json.loads(prompt)
    assert "community_summaries" in payload
    assert isinstance(payload["community_summaries"], list)
    assert all(
        isinstance(s, str) and s.startswith("Community")
        for s in payload["community_summaries"]
    )


def test_empty_snapshot_produces_empty_lists() -> None:
    snap = _snap([], [])
    prompt = build_ontology_prompt("q", snapshot=snap)
    payload = json.loads(prompt)
    assert payload["known_entities"] == []
    assert payload["community_summaries"] == []


def test_prompt_is_deterministic() -> None:
    snap = _dense_snapshot()
    a = build_ontology_prompt("q", snapshot=snap, top_k_central=7)
    b = build_ontology_prompt("q", snapshot=snap, top_k_central=7)
    assert a == b


def test_prompt_length_bounded_by_top_k() -> None:
    snap = _dense_snapshot()
    small = build_ontology_prompt("q", snapshot=snap, top_k_central=1)
    big = build_ontology_prompt("q", snapshot=snap, top_k_central=50)
    # More entities should produce a longer (or equal) prompt.
    assert len(big) >= len(small)
    # Zero k yields no entities.
    zero = build_ontology_prompt("q", snapshot=snap, top_k_central=0)
    zero_payload = json.loads(zero)
    assert zero_payload["known_entities"] == []
