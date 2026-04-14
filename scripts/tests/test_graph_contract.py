"""Phase 8 Task 1 — contract dataclasses + validators."""

from __future__ import annotations

import dataclasses

import pytest

from vitruvius.graph.contract import (
    ALLOWED_EDGE_STATUSES,
    ALLOWED_ID_PREFIXES,
    ALLOWED_NODE_TYPES,
    ALLOWED_TRUST_LEVELS,
    ContractViolation,
    GraphEdge,
    GraphNode,
    GraphSnapshot,
    validate_edge,
    validate_node,
)


def _good_node() -> GraphNode:
    return GraphNode(
        id="concept-building-permit",
        type="concept",
        slug="building-permit",
        trust_level="derived",
        last_updated_utc="2026-04-14T00:00:00Z",
    )


def _good_edge() -> GraphEdge:
    return GraphEdge(
        from_id="law-pd-1096-national-building-code",
        to_id="concept-building-permit",
        type="governs",
        evidence_id="rel-pd-1096-governs-building-permit",
        status="verified",
    )


def test_good_node_passes() -> None:
    validate_node(_good_node())


def test_node_bad_id_prefix_raises() -> None:
    bad = dataclasses.replace(_good_node(), id="zzz-something")
    with pytest.raises(ContractViolation):
        validate_node(bad)


def test_node_bad_type_raises() -> None:
    bad = dataclasses.replace(_good_node(), type="entity")
    with pytest.raises(ContractViolation):
        validate_node(bad)


def test_node_bad_trust_level_raises() -> None:
    bad = dataclasses.replace(_good_node(), trust_level="gold")
    with pytest.raises(ContractViolation):
        validate_node(bad)


def test_node_empty_slug_raises() -> None:
    bad = dataclasses.replace(_good_node(), slug="")
    with pytest.raises(ContractViolation):
        validate_node(bad)


def test_node_bad_date_raises() -> None:
    bad = dataclasses.replace(_good_node(), last_updated_utc="not-a-date")
    with pytest.raises(ContractViolation):
        validate_node(bad)


def test_good_edge_passes() -> None:
    validate_edge(_good_edge())


def test_edge_bad_from_id_raises() -> None:
    bad = dataclasses.replace(_good_edge(), from_id="xxx-broken")
    with pytest.raises(ContractViolation):
        validate_edge(bad)


def test_edge_bad_to_id_raises() -> None:
    bad = dataclasses.replace(_good_edge(), to_id="xxx-broken")
    with pytest.raises(ContractViolation):
        validate_edge(bad)


def test_edge_bad_evidence_id_raises() -> None:
    bad = dataclasses.replace(_good_edge(), evidence_id="other-123")
    with pytest.raises(ContractViolation):
        validate_edge(bad)


def test_edge_bad_status_raises() -> None:
    bad = dataclasses.replace(_good_edge(), status="pending")
    with pytest.raises(ContractViolation):
        validate_edge(bad)


def test_edge_empty_type_raises() -> None:
    bad = dataclasses.replace(_good_edge(), type="")
    with pytest.raises(ContractViolation):
        validate_edge(bad)


def test_contract_violation_is_value_error() -> None:
    assert issubclass(ContractViolation, ValueError)


def test_graph_node_is_frozen() -> None:
    node = _good_node()
    with pytest.raises(dataclasses.FrozenInstanceError):
        node.id = "concept-other"  # type: ignore[misc]


def test_graph_edge_is_frozen() -> None:
    edge = _good_edge()
    with pytest.raises(dataclasses.FrozenInstanceError):
        edge.type = "affects"  # type: ignore[misc]


def test_allowed_sets_are_frozensets() -> None:
    assert isinstance(ALLOWED_NODE_TYPES, frozenset)
    assert isinstance(ALLOWED_TRUST_LEVELS, frozenset)
    assert isinstance(ALLOWED_EDGE_STATUSES, frozenset)
    assert isinstance(ALLOWED_ID_PREFIXES, frozenset)


def test_graph_snapshot_roundtrips_fields() -> None:
    node = _good_node()
    edge = _good_edge()
    snapshot = GraphSnapshot(
        schema_version="1.0.0",
        generated_at_utc="2026-04-14T00:00:00Z",
        node_count=1,
        edge_count=1,
        nodes=[node],
        edges=[edge],
    )
    assert snapshot.schema_version == "1.0.0"
    assert snapshot.node_count == 1
    assert snapshot.edge_count == 1
    assert snapshot.nodes == [node]
    assert snapshot.edges == [edge]
