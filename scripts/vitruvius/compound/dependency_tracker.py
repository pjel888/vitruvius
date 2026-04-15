"""Stream S3.2 — maps edge IDs to downstream consumers for O(delta) updates.

This is the data structure the Stream S3.3 differential propagator walks on
every Delta. Keeping it independent from the event store lets us swap
implementations (e.g. RocksDB-backed) without touching the propagator.
"""
from __future__ import annotations

from collections import defaultdict


class DependencyTracker:
    """Bidirectional map: edge_id -> set of consumer IDs.

    The tracker is the mutable half of the differential dataflow pair —
    callers register downstream dependencies once at graph build time, and
    the :class:`DifferentialPropagator` walks it on every incoming Delta.
    """

    def __init__(self) -> None:
        self._by_edge: dict[str, set[str]] = defaultdict(set)

    def register(self, *, edge_id: str, consumer: str) -> None:
        if not edge_id:
            raise ValueError("edge_id must be non-empty")
        if not consumer:
            raise ValueError("consumer must be non-empty")
        self._by_edge[edge_id].add(consumer)

    def unregister(self, *, edge_id: str, consumer: str) -> None:
        bucket = self._by_edge.get(edge_id)
        if bucket is not None:
            bucket.discard(consumer)
            if not bucket:
                del self._by_edge[edge_id]

    def consumers_of(self, edge_id: str) -> tuple[str, ...]:
        bucket = self._by_edge.get(edge_id, set())
        return tuple(sorted(bucket))
