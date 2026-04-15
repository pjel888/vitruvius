"""Stream S3.3 — walk the dependency tracker on every Delta.

This is the O(delta) substitute for the Phase 6 full-graph rebuild: given a
batch of Deltas, return the sorted, de-duplicated set of downstream consumers
that need re-auditing.
"""
from __future__ import annotations

from collections.abc import Iterable

from vitruvius.compound.dependency_tracker import DependencyTracker
from vitruvius.graph.event_store import Delta


class DifferentialPropagator:
    """Walks a DependencyTracker on each Delta batch.

    The propagator is stateless: all mutable state lives in the tracker.
    """

    def __init__(self, tracker: DependencyTracker) -> None:
        self._tracker = tracker

    def propagate(self, deltas: Iterable[Delta]) -> tuple[str, ...]:
        affected: set[str] = set()
        for delta in deltas:
            for consumer in self._tracker.consumers_of(delta.edge_id):
                affected.add(consumer)
        return tuple(sorted(affected))
