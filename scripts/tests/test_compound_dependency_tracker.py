"""Stream S3.2 — edge-ID dependency tracker."""
from __future__ import annotations

import pytest

from vitruvius.compound.dependency_tracker import DependencyTracker


def test_register_and_query_single_edge() -> None:
    tracker = DependencyTracker()
    tracker.register(edge_id="a->b", consumer="building_42_audit")
    assert tracker.consumers_of("a->b") == ("building_42_audit",)


def test_register_multiple_consumers_sorted() -> None:
    tracker = DependencyTracker()
    tracker.register(edge_id="a->b", consumer="building_9")
    tracker.register(edge_id="a->b", consumer="building_42")
    tracker.register(edge_id="a->b", consumer="building_7")
    assert tracker.consumers_of("a->b") == ("building_42", "building_7", "building_9")


def test_register_is_idempotent() -> None:
    tracker = DependencyTracker()
    tracker.register(edge_id="a->b", consumer="building_42")
    tracker.register(edge_id="a->b", consumer="building_42")
    assert tracker.consumers_of("a->b") == ("building_42",)


def test_query_unknown_edge_returns_empty_tuple() -> None:
    tracker = DependencyTracker()
    assert tracker.consumers_of("never-registered") == ()


def test_unregister_removes_consumer() -> None:
    tracker = DependencyTracker()
    tracker.register(edge_id="a->b", consumer="building_42")
    tracker.register(edge_id="a->b", consumer="building_7")
    tracker.unregister(edge_id="a->b", consumer="building_42")
    assert tracker.consumers_of("a->b") == ("building_7",)


def test_register_empty_ids_rejected() -> None:
    tracker = DependencyTracker()
    with pytest.raises(ValueError):
        tracker.register(edge_id="", consumer="building_42")
    with pytest.raises(ValueError):
        tracker.register(edge_id="a->b", consumer="")
