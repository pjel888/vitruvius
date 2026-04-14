"""Stream H.5 — TDA Betti number computation."""

from __future__ import annotations

import dataclasses

import pytest

from vitruvius.graph.contract import GraphEdge, GraphNode, GraphSnapshot
from vitruvius.graph.tda import (
    MAX_TDA_NODES,
    BettiNumbers,
    TDACapacityError,
    TDAReport,
    compute_betti_numbers,
)


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


def test_tree_has_b1_zero() -> None:
    # Linear chain: a -> b -> c -> d, no cycles.
    snap = _snap(
        [_n(f"concept-{c}") for c in "abcd"],
        [
            _e("concept-a", "concept-b", evidence="rel-1"),
            _e("concept-b", "concept-c", evidence="rel-2"),
            _e("concept-c", "concept-d", evidence="rel-3"),
        ],
    )
    report = compute_betti_numbers(snap)
    assert report.betti.b0 == 1
    assert report.betti.b1 == 0


def test_one_cycle_has_b1_one() -> None:
    # Triangle.
    snap = _snap(
        [_n("concept-a"), _n("concept-b"), _n("concept-c")],
        [
            _e("concept-a", "concept-b", evidence="rel-1"),
            _e("concept-b", "concept-c", evidence="rel-2"),
            _e("concept-c", "concept-a", evidence="rel-3"),
        ],
    )
    report = compute_betti_numbers(snap)
    assert report.betti.b0 == 1
    assert report.betti.b1 == 1
    assert len(report.loop_candidates) == 1


def test_two_disjoint_cycles_b1_two() -> None:
    snap = _snap(
        [_n(f"concept-{c}") for c in ["a", "b", "c", "d", "e", "f"]],
        [
            # triangle 1
            _e("concept-a", "concept-b", evidence="rel-1"),
            _e("concept-b", "concept-c", evidence="rel-2"),
            _e("concept-c", "concept-a", evidence="rel-3"),
            # triangle 2
            _e("concept-d", "concept-e", evidence="rel-4"),
            _e("concept-e", "concept-f", evidence="rel-5"),
            _e("concept-f", "concept-d", evidence="rel-6"),
        ],
    )
    report = compute_betti_numbers(snap)
    assert report.betti.b0 == 2
    assert report.betti.b1 == 2


def test_two_components_b0_two() -> None:
    snap = _snap(
        [_n(f"concept-{c}") for c in "abcd"],
        [
            _e("concept-a", "concept-b", evidence="rel-1"),
            _e("concept-c", "concept-d", evidence="rel-2"),
        ],
    )
    report = compute_betti_numbers(snap)
    assert report.betti.b0 == 2
    assert report.betti.b1 == 0


def test_tda_capacity_error_on_too_many_nodes() -> None:
    big_nodes = [_n(f"concept-x{i:04d}") for i in range(MAX_TDA_NODES + 1)]
    snap = _snap(big_nodes, [])
    with pytest.raises(TDACapacityError):
        compute_betti_numbers(snap)


def test_empty_snapshot_is_all_zero() -> None:
    snap = _snap([], [])
    report = compute_betti_numbers(snap)
    assert report.betti.b0 == 0
    assert report.betti.b1 == 0
    assert report.loop_candidates == ()


def test_frozen_return() -> None:
    snap = _snap(
        [_n("concept-a"), _n("concept-b")],
        [_e("concept-a", "concept-b", evidence="rel-1")],
    )
    report = compute_betti_numbers(snap)
    assert dataclasses.is_dataclass(report)
    with pytest.raises(dataclasses.FrozenInstanceError):
        report.snapshot_size = 999  # type: ignore[misc]
    assert isinstance(report.betti, BettiNumbers)
    with pytest.raises(dataclasses.FrozenInstanceError):
        report.betti.b0 = 999  # type: ignore[misc]
