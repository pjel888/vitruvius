# scripts/tests/test_temporal_edge_schema.py
"""Sprint GT Stream GT.3.1 — TemporalEdge schema."""
from __future__ import annotations

import pytest

from vitruvius.graph.contract import (
    ContractViolation,
    GraphEdge,
    TemporalEdge,
    validate_temporal_edge,
)


def test_temporal_edge_round_trip() -> None:
    edge = TemporalEdge(
        from_id="law-pd-1096",
        to_id="concept-egress-width",
        type="requires",
        evidence_id="rel-0001",
        status="verified",
        valid_from="1977-02-19T00:00:00Z",
        valid_until="2004-11-30T00:00:00Z",
    )
    assert edge.from_id == "law-pd-1096"
    assert edge.valid_from == "1977-02-19T00:00:00Z"
    assert edge.valid_until == "2004-11-30T00:00:00Z"
    validate_temporal_edge(edge)


def test_temporal_edge_open_interval_allowed() -> None:
    edge = TemporalEdge(
        from_id="law-pd-1096",
        to_id="concept-egress-width",
        type="requires",
        evidence_id="rel-0002",
        status="verified",
        valid_from="2004-12-01T00:00:00Z",
        valid_until=None,
    )
    validate_temporal_edge(edge)


def test_temporal_edge_rejects_bad_valid_from() -> None:
    edge = TemporalEdge(
        from_id="law-pd-1096",
        to_id="concept-egress-width",
        type="requires",
        evidence_id="rel-0003",
        status="verified",
        valid_from="not-a-date",
        valid_until=None,
    )
    with pytest.raises(ContractViolation):
        validate_temporal_edge(edge)


def test_temporal_edge_rejects_inverted_interval() -> None:
    edge = TemporalEdge(
        from_id="law-pd-1096",
        to_id="concept-egress-width",
        type="requires",
        evidence_id="rel-0004",
        status="verified",
        valid_from="2010-01-01T00:00:00Z",
        valid_until="2005-01-01T00:00:00Z",
    )
    with pytest.raises(ContractViolation):
        validate_temporal_edge(edge)


def test_temporal_edge_ordering_is_stable() -> None:
    a = TemporalEdge(
        from_id="law-pd-1096", to_id="concept-x", type="requires",
        evidence_id="rel-001", status="verified",
        valid_from="2000-01-01T00:00:00Z", valid_until=None,
    )
    b = TemporalEdge(
        from_id="law-pd-1096", to_id="concept-x", type="requires",
        evidence_id="rel-002", status="verified",
        valid_from="2010-01-01T00:00:00Z", valid_until=None,
    )
    ordered = sorted([b, a], key=lambda e: e.valid_from)
    assert ordered[0].valid_from == "2000-01-01T00:00:00Z"
    assert ordered[1].valid_from == "2010-01-01T00:00:00Z"
