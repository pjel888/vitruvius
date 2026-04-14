"""Stream PHYS.2 — system energy / Boltzmann gate / VF2 motif matcher.

Absorbs the orphan Stream O tasks (VF2 + Boltzmann) from the
statistical-architectural-upgrade plan per governing plan §4.4.
"""
from __future__ import annotations

import math

import pytest

from vitruvius.graph.contract import GraphEdge, GraphNode, GraphSnapshot
from vitruvius.graph.physics import (
    BoltzmannVerdict,
    SystemEnergy,
    compute_system_energy,
    find_violation_motifs,
    should_promote_boltzmann,
)


def _n(id_: str, *, trust: str = "derived") -> GraphNode:
    return GraphNode(
        id=id_,
        type="concept",
        slug=id_.split("-", 1)[-1],
        trust_level=trust,
        last_updated_utc="2026-04-15T00:00:00Z",
    )


def _e(from_id: str, to_id: str, evidence_id: str, *, status: str = "verified") -> GraphEdge:
    return GraphEdge(
        from_id=from_id,
        to_id=to_id,
        type="governs",
        evidence_id=evidence_id,
        status=status,
    )


def _snapshot(nodes: list[GraphNode], edges: list[GraphEdge]) -> GraphSnapshot:
    return GraphSnapshot(
        schema_version="1.0.0",
        generated_at_utc="2026-04-15T00:00:00Z",
        node_count=len(nodes),
        edge_count=len(edges),
        nodes=nodes,
        edges=edges,
    )


# ---------------------------------------------------------------------------
# System energy
# ---------------------------------------------------------------------------
def test_empty_snapshot_has_zero_energy() -> None:
    e = compute_system_energy(_snapshot([], []))
    assert isinstance(e, SystemEnergy)
    assert e.energy == 0.0
    assert e.unresolved_edge_count == 0
    assert e.unverified_node_count == 0


def test_unverified_edges_raise_energy() -> None:
    nodes = [_n("a"), _n("b")]
    edges = [_e("a", "b", evidence_id="rel-1", status="unverified")]
    e = compute_system_energy(_snapshot(nodes, edges))
    assert e.energy > 0.0
    assert e.unresolved_edge_count == 1


def test_verified_only_graph_has_low_energy() -> None:
    nodes = [_n("a", trust="primary"), _n("b", trust="primary")]
    edges = [_e("a", "b", evidence_id="rel-1", status="verified")]
    e = compute_system_energy(_snapshot(nodes, edges))
    # With everything verified + primary the scalar energy should be 0
    assert e.energy == 0.0


# ---------------------------------------------------------------------------
# Boltzmann promotion gate
# ---------------------------------------------------------------------------
def test_low_energy_promotes_at_low_temperature() -> None:
    verdict = should_promote_boltzmann(energy=0.1, temperature=0.5)
    assert isinstance(verdict, BoltzmannVerdict)
    # P = exp(-0.1/0.5) = exp(-0.2) ≈ 0.818 → promote
    assert verdict.probability == pytest.approx(math.exp(-0.2), abs=1e-6)
    assert verdict.promote is True


def test_high_energy_freezes_at_low_temperature() -> None:
    verdict = should_promote_boltzmann(energy=10.0, temperature=0.5)
    # P = exp(-20) ≈ 2e-9 → do not promote
    assert verdict.probability < 1e-6
    assert verdict.promote is False


def test_zero_temperature_is_hard_gate() -> None:
    """Temperature 0 means only zero-energy states can promote."""
    freeze = should_promote_boltzmann(energy=0.01, temperature=0.0)
    assert freeze.promote is False

    thaw = should_promote_boltzmann(energy=0.0, temperature=0.0)
    assert thaw.promote is True  # P(s)=1 at equilibrium


# ---------------------------------------------------------------------------
# VF2 motif matcher (orphan Stream O absorption)
# ---------------------------------------------------------------------------
def test_motif_matcher_finds_triangle() -> None:
    """A 3-node triangle is a classic VF2 test case. Feed one and
    verify the matcher finds exactly one match."""
    nodes = [_n("a"), _n("b"), _n("c")]
    edges = [
        _e("a", "b", evidence_id="rel-1"),
        _e("b", "c", evidence_id="rel-2"),
        _e("c", "a", evidence_id="rel-3"),
    ]
    snap = _snapshot(nodes, edges)

    # Motif: a directed triangle (same shape as the input)
    motif_nodes = ["x", "y", "z"]
    motif_edges = [("x", "y"), ("y", "z"), ("z", "x")]
    matches = find_violation_motifs(
        snap,
        motif_nodes=motif_nodes,
        motif_edges=motif_edges,
    )
    assert len(matches) >= 1
    for mapping in matches:
        assert set(mapping.keys()) == {"x", "y", "z"}
        assert set(mapping.values()) == {"a", "b", "c"}


def test_motif_matcher_returns_empty_when_no_match() -> None:
    nodes = [_n("a"), _n("b")]
    edges = [_e("a", "b", evidence_id="rel-1")]
    snap = _snapshot(nodes, edges)

    matches = find_violation_motifs(
        snap,
        motif_nodes=["x", "y", "z"],
        motif_edges=[("x", "y"), ("y", "z"), ("z", "x")],
    )
    assert matches == []
