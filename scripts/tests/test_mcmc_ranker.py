"""Stream I.3 — MCMC answer ranker."""

from __future__ import annotations

import pytest

from vitruvius.graph.contract import GraphEdge, GraphNode, GraphSnapshot
from vitruvius.query.mcmc_ranker import rank_answer_entities


def _n(id_: str) -> GraphNode:
    return GraphNode(
        id=id_,
        type="concept",
        slug=id_.split("-", 1)[-1] or "x",
        trust_level="derived",
        last_updated_utc="2026-04-14T00:00:00Z",
    )


def _e(from_id: str, to_id: str, *, evidence: str) -> GraphEdge:
    return GraphEdge(
        from_id=from_id,
        to_id=to_id,
        type="governs",
        evidence_id=evidence,
        status="verified",
    )


def _snap(nodes: list[GraphNode], edges: list[GraphEdge]) -> GraphSnapshot:
    return GraphSnapshot(
        schema_version="1.0.0",
        generated_at_utc="2026-04-14T00:00:00Z",
        node_count=len(nodes),
        edge_count=len(edges),
        nodes=nodes,
        edges=edges,
    )


def _star_snapshot() -> GraphSnapshot:
    return _snap(
        [_n("concept-hub")] + [_n(f"concept-{c}") for c in "abcd"],
        [
            _e("concept-hub", "concept-a", evidence="rel-1"),
            _e("concept-hub", "concept-b", evidence="rel-2"),
            _e("concept-hub", "concept-c", evidence="rel-3"),
            _e("concept-hub", "concept-d", evidence="rel-4"),
        ],
    )


def test_rank_basic_sorted_desc() -> None:
    snap = _star_snapshot()
    ranked = rank_answer_entities(
        ["concept-a", "concept-b", "concept-c", "concept-d"],
        snapshot=snap,
        seed_id="concept-hub",
        steps=2_000,
        rng_seed=42,
    )
    assert len(ranked) == 4
    scores = [score for _, score in ranked]
    assert scores == sorted(scores, reverse=True)
    assert all(score >= 0.0 for _, score in ranked)


def test_rank_is_deterministic_via_rng_seed() -> None:
    snap = _star_snapshot()
    a = rank_answer_entities(
        ["concept-a", "concept-b"],
        snapshot=snap,
        seed_id="concept-hub",
        steps=1_500,
        rng_seed=7,
    )
    b = rank_answer_entities(
        ["concept-a", "concept-b"],
        snapshot=snap,
        seed_id="concept-hub",
        steps=1_500,
        rng_seed=7,
    )
    assert a == b


def test_entity_not_in_walk_gets_zero() -> None:
    snap = _star_snapshot()
    ranked = rank_answer_entities(
        ["concept-not-present"],
        snapshot=snap,
        seed_id="concept-hub",
        steps=1_000,
        rng_seed=0,
    )
    assert ranked == [("concept-not-present", 0.0)]


def test_empty_entities_returns_empty_list() -> None:
    snap = _star_snapshot()
    ranked = rank_answer_entities(
        [],
        snapshot=snap,
        seed_id="concept-hub",
    )
    assert ranked == []


def test_unknown_seed_raises_key_error() -> None:
    snap = _star_snapshot()
    with pytest.raises(KeyError):
        rank_answer_entities(
            ["concept-a"],
            snapshot=snap,
            seed_id="concept-nope",
        )
