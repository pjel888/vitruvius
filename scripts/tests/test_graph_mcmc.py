"""Stream H.4 — MCMC random walk ranking."""

from __future__ import annotations

import dataclasses

import pytest

from vitruvius.graph.contract import GraphEdge, GraphNode, GraphSnapshot
from vitruvius.graph.mcmc import MCMCStationaryDistribution, mcmc_random_walk


def _n(id_: str) -> GraphNode:
    return GraphNode(
        id=id_,
        type="concept",
        slug=id_.split("-", 1)[-1] or "x",
        trust_level="derived",
        last_updated_utc="2026-04-14T00:00:00Z",
    )


def _e(from_id: str, to_id: str, *, evidence: str = "rel-x") -> GraphEdge:
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


def test_dead_end_teleports_to_seed() -> None:
    # a -> b (dead end)
    snap = _snap(
        [_n("concept-a"), _n("concept-b")],
        [_e("concept-a", "concept-b", evidence="rel-1")],
    )
    dist = mcmc_random_walk(snap, seed_id="concept-a", steps=500)
    scores = dict(dist.visit_frequency)
    assert scores["concept-a"] > 0.0
    # a should dominate because b has no outgoing edges — every visit
    # to b immediately teleports back.
    assert scores["concept-a"] > scores["concept-b"]


def test_deterministic_via_rng_seed() -> None:
    snap = _snap(
        [_n("concept-a"), _n("concept-b"), _n("concept-c")],
        [
            _e("concept-a", "concept-b", evidence="rel-1"),
            _e("concept-b", "concept-c", evidence="rel-2"),
            _e("concept-c", "concept-a", evidence="rel-3"),
        ],
    )
    a = mcmc_random_walk(snap, seed_id="concept-a", rng_seed=42, steps=1_000)
    b = mcmc_random_walk(snap, seed_id="concept-a", rng_seed=42, steps=1_000)
    assert a == b


def test_frequencies_sum_to_one() -> None:
    snap = _snap(
        [_n("concept-a"), _n("concept-b"), _n("concept-c")],
        [
            _e("concept-a", "concept-b", evidence="rel-1"),
            _e("concept-b", "concept-c", evidence="rel-2"),
            _e("concept-c", "concept-a", evidence="rel-3"),
        ],
    )
    dist = mcmc_random_walk(snap, seed_id="concept-a", steps=2_000)
    total = sum(freq for _, freq in dist.visit_frequency)
    assert abs(total - 1.0) < 1e-9


def test_seed_has_highest_frequency_on_star_graph() -> None:
    # star: seed 'concept-center' connects to 4 leaves.
    nodes = [_n("concept-center")] + [_n(f"concept-leaf{i}") for i in range(4)]
    edges = [
        _e("concept-center", f"concept-leaf{i}", evidence=f"rel-{i}")
        for i in range(4)
    ]
    snap = _snap(nodes, edges)
    dist = mcmc_random_walk(
        snap, seed_id="concept-center", steps=5_000, rng_seed=7
    )
    scores = dict(dist.visit_frequency)
    leaf_scores = [scores[f"concept-leaf{i}"] for i in range(4)]
    assert scores["concept-center"] > max(leaf_scores)


def test_steps_parameter_honored() -> None:
    snap = _snap(
        [_n("concept-a"), _n("concept-b")],
        [_e("concept-a", "concept-b", evidence="rel-1")],
    )
    small = mcmc_random_walk(snap, seed_id="concept-a", steps=10)
    large = mcmc_random_walk(snap, seed_id="concept-a", steps=1_000)
    assert small.steps == 10
    assert large.steps == 1_000


def test_unknown_seed_raises() -> None:
    snap = _snap([_n("concept-a")], [])
    with pytest.raises(KeyError):
        mcmc_random_walk(snap, seed_id="concept-ghost", steps=10)


def test_frozen_return() -> None:
    snap = _snap(
        [_n("concept-a"), _n("concept-b")],
        [_e("concept-a", "concept-b", evidence="rel-1")],
    )
    dist = mcmc_random_walk(snap, seed_id="concept-a", steps=100)
    assert dataclasses.is_dataclass(dist)
    with pytest.raises(dataclasses.FrozenInstanceError):
        dist.alpha = 0.5  # type: ignore[misc]
    assert isinstance(dist, MCMCStationaryDistribution)
