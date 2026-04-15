# scripts/vitruvius/graph/temporal_query.py
"""Sprint GT Stream GT.3.2 — versioned retrieval for TemporalEdges.

Mirrors the projection semantics of
``scripts/vitruvius/graph/event_store.project_graph_at`` (Sprint HP.3)
but works on the in-memory ``TemporalEdge`` list that the Phase 8
snapshot builder produces. The event store's ``project_graph_at``
remains the authoritative on-disk projector; this module is the
in-memory equivalent that reads from a pre-materialised list.
"""
from __future__ import annotations

from typing import Iterable

from vitruvius.graph.contract import TemporalEdge


def query_at(
    edges: Iterable[TemporalEdge],
    *,
    timestamp_utc: str,
) -> list[TemporalEdge]:
    """Return every ``TemporalEdge`` whose
    ``valid_from <= timestamp_utc`` and
    (``valid_until`` is ``None`` or ``timestamp_utc < valid_until``).

    Timestamps are compared as ISO-8601 strings — the contract
    validator guarantees the format is lexicographically sortable.
    """
    matches: list[TemporalEdge] = []
    for edge in edges:
        if edge.valid_from > timestamp_utc:
            continue
        if edge.valid_until is not None and timestamp_utc >= edge.valid_until:
            continue
        matches.append(edge)
    return matches
