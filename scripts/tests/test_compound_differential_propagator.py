"""Stream S3.3 — differential propagator on a 5-node graph."""
from __future__ import annotations

from vitruvius.compound.dependency_tracker import DependencyTracker
from vitruvius.compound.differential_propagator import DifferentialPropagator
from vitruvius.graph.event_store import Delta


def _tracker_for_5_node_graph() -> DependencyTracker:
    """
    5-node DAG used across S3.3 tests:

        rule_setback  -- applies_to -->  building_42
        rule_setback  -- applies_to -->  building_7
        rule_height   -- applies_to -->  building_42
        rule_height   -- applies_to -->  tower_99
    """
    tracker = DependencyTracker()
    tracker.register(edge_id="rule_setback->applies", consumer="building_42")
    tracker.register(edge_id="rule_setback->applies", consumer="building_7")
    tracker.register(edge_id="rule_height->applies", consumer="building_42")
    tracker.register(edge_id="rule_height->applies", consumer="tower_99")
    return tracker


def test_single_delta_propagates_to_two_consumers() -> None:
    tracker = _tracker_for_5_node_graph()
    propagator = DifferentialPropagator(tracker)

    delta = Delta(
        event_id="evt_1",
        edge_id="rule_setback->applies",
        kind="upsert",
        payload={"min_distance": 2.5},
    )
    affected = propagator.propagate([delta])
    assert affected == ("building_42", "building_7")


def test_two_deltas_merge_and_dedupe_consumers() -> None:
    tracker = _tracker_for_5_node_graph()
    propagator = DifferentialPropagator(tracker)

    deltas = [
        Delta(event_id="evt_1", edge_id="rule_setback->applies", kind="upsert", payload={}),
        Delta(event_id="evt_2", edge_id="rule_height->applies", kind="upsert", payload={}),
    ]
    affected = propagator.propagate(deltas)
    # building_42 appears in both lists — must be emitted only once.
    assert affected == ("building_42", "building_7", "tower_99")


def test_delta_on_unknown_edge_returns_empty() -> None:
    tracker = _tracker_for_5_node_graph()
    propagator = DifferentialPropagator(tracker)

    delta = Delta(event_id="evt_x", edge_id="rule_lighting->applies", kind="upsert", payload={})
    assert propagator.propagate([delta]) == ()


def test_delete_kind_also_propagates() -> None:
    tracker = _tracker_for_5_node_graph()
    propagator = DifferentialPropagator(tracker)

    delta = Delta(event_id="evt_del", edge_id="rule_height->applies", kind="delete", payload={})
    assert propagator.propagate([delta]) == ("building_42", "tower_99")
