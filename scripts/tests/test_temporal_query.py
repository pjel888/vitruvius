# scripts/tests/test_temporal_query.py
"""Sprint GT Stream GT.3.2 — versioned retrieval of TemporalEdges."""
from __future__ import annotations

from pathlib import Path

import pytest

from vitruvius.graph.contract import TemporalEdge
from vitruvius.graph.temporal_query import query_at


@pytest.fixture
def three_edge_timeline() -> list[TemporalEdge]:
    return [
        TemporalEdge(
            from_id="law-pd-1096", to_id="concept-egress-width",
            type="requires", evidence_id="rel-001", status="verified",
            valid_from="1977-02-19T00:00:00Z",
            valid_until="2004-11-30T00:00:00Z",
        ),
        TemporalEdge(
            from_id="law-pd-1096", to_id="concept-egress-width",
            type="requires", evidence_id="rel-002", status="verified",
            valid_from="2004-12-01T00:00:00Z",
            valid_until="2015-12-31T00:00:00Z",
        ),
        TemporalEdge(
            from_id="law-pd-1096", to_id="concept-egress-width",
            type="requires", evidence_id="rel-003", status="verified",
            valid_from="2016-01-01T00:00:00Z",
            valid_until=None,
        ),
    ]


def test_query_in_first_window_returns_first_edge(
    three_edge_timeline: list[TemporalEdge],
) -> None:
    result = query_at(
        three_edge_timeline,
        timestamp_utc="1990-06-15T00:00:00Z",
    )
    assert len(result) == 1
    assert result[0].evidence_id == "rel-001"


def test_query_in_second_window_returns_second_edge(
    three_edge_timeline: list[TemporalEdge],
) -> None:
    result = query_at(
        three_edge_timeline,
        timestamp_utc="2008-08-08T00:00:00Z",
    )
    assert len(result) == 1
    assert result[0].evidence_id == "rel-002"


def test_query_in_open_window_returns_current_edge(
    three_edge_timeline: list[TemporalEdge],
) -> None:
    result = query_at(
        three_edge_timeline,
        timestamp_utc="2026-04-15T00:00:00Z",
    )
    assert len(result) == 1
    assert result[0].evidence_id == "rel-003"


def test_query_before_first_window_is_empty(
    three_edge_timeline: list[TemporalEdge],
) -> None:
    result = query_at(
        three_edge_timeline,
        timestamp_utc="1900-01-01T00:00:00Z",
    )
    assert result == []


def test_query_at_exact_boundary_includes_starting_edge(
    three_edge_timeline: list[TemporalEdge],
) -> None:
    result = query_at(
        three_edge_timeline,
        timestamp_utc="2004-12-01T00:00:00Z",
    )
    assert len(result) == 1
    assert result[0].evidence_id == "rel-002"
