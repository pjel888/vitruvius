"""Temporal graph edge helpers — ISO date validation, stamp, cap, backfill, filter."""

from __future__ import annotations

from datetime import datetime, timezone

import pytest

from vitruvius.promotion.temporal_edges import (
    DEFAULT_JURISDICTION,
    ISO_DATE_FORMAT,
    TemporalEdge,
    TemporalValidationError,
    backfill_legacy_edge,
    cap_predecessor,
    filter_edges_valid_at,
    stamp_new_edge,
    validate_temporal_edge,
)


NOW = datetime(2026, 4, 14, 12, 0, 0, tzinfo=timezone.utc)


def test_new_edge_stamps_today() -> None:
    edge = stamp_new_edge(
        edge_id="edge-1",
        from_entity="concept-a",
        predicate="governs",
        to_entity="concept-b",
        now=NOW,
    )
    assert edge.valid_from == "2026-04-14"
    assert edge.valid_until is None


def test_default_jurisdiction_national() -> None:
    edge = stamp_new_edge(
        edge_id="e",
        from_entity="a",
        predicate="g",
        to_entity="b",
        now=NOW,
    )
    assert edge.jurisdiction == "national"
    assert DEFAULT_JURISDICTION == "national"


def test_iso_date_format_constant() -> None:
    assert ISO_DATE_FORMAT == "%Y-%m-%d"


def test_custom_jurisdiction_preserved() -> None:
    edge = stamp_new_edge(
        edge_id="e",
        from_entity="a",
        predicate="g",
        to_entity="b",
        jurisdiction="lgu-quezon-city",
        now=NOW,
    )
    assert edge.jurisdiction == "lgu-quezon-city"


def test_cap_predecessor_on_supersede() -> None:
    predecessor = stamp_new_edge(
        edge_id="old",
        from_entity="a",
        predicate="g",
        to_entity="b",
        now=datetime(2020, 1, 1, tzinfo=timezone.utc),
    )
    capped = cap_predecessor(predecessor, now=NOW)
    assert capped.edge_id == "old"
    assert capped.valid_from == "2020-01-01"
    assert capped.valid_until == "2026-04-14"
    # Original unchanged
    assert predecessor.valid_until is None


def test_cap_predecessor_with_explicit_date() -> None:
    predecessor = stamp_new_edge(
        edge_id="old",
        from_entity="a",
        predicate="g",
        to_entity="b",
        now=datetime(2020, 1, 1, tzinfo=timezone.utc),
    )
    capped = cap_predecessor(predecessor, cap_date="2025-06-15")
    assert capped.valid_until == "2025-06-15"


def test_cap_predecessor_returns_new_instance() -> None:
    predecessor = stamp_new_edge(
        edge_id="old",
        from_entity="a",
        predicate="g",
        to_entity="b",
        now=datetime(2020, 1, 1, tzinfo=timezone.utc),
    )
    capped = cap_predecessor(predecessor, cap_date="2025-06-15")
    assert capped is not predecessor
    assert predecessor.valid_until is None


def test_cap_date_before_valid_from_raises() -> None:
    predecessor = stamp_new_edge(
        edge_id="old",
        from_entity="a",
        predicate="g",
        to_entity="b",
        now=datetime(2020, 1, 1, tzinfo=timezone.utc),
    )
    with pytest.raises(TemporalValidationError):
        cap_predecessor(predecessor, cap_date="2019-01-01")


def test_valid_until_must_be_after_valid_from() -> None:
    bad = TemporalEdge(
        edge_id="e",
        from_entity="a",
        predicate="g",
        to_entity="b",
        valid_from="2026-01-01",
        valid_until="2025-12-31",
    )
    with pytest.raises(TemporalValidationError):
        validate_temporal_edge(bad)


def test_valid_until_equal_to_valid_from_is_valid() -> None:
    ok = TemporalEdge(
        edge_id="e",
        from_entity="a",
        predicate="g",
        to_entity="b",
        valid_from="2026-04-14",
        valid_until="2026-04-14",
    )
    validate_temporal_edge(ok)  # should not raise


def test_valid_until_none_is_valid() -> None:
    ok = TemporalEdge(
        edge_id="e",
        from_entity="a",
        predicate="g",
        to_entity="b",
        valid_from="2026-04-14",
        valid_until=None,
    )
    validate_temporal_edge(ok)


def test_malformed_valid_from_raises() -> None:
    bad = TemporalEdge(
        edge_id="e",
        from_entity="a",
        predicate="g",
        to_entity="b",
        valid_from="not-a-date",
    )
    with pytest.raises(TemporalValidationError):
        validate_temporal_edge(bad)


def test_malformed_valid_until_raises() -> None:
    bad = TemporalEdge(
        edge_id="e",
        from_entity="a",
        predicate="g",
        to_entity="b",
        valid_from="2026-04-14",
        valid_until="2026/04/15",
    )
    with pytest.raises(TemporalValidationError):
        validate_temporal_edge(bad)


def test_empty_jurisdiction_raises() -> None:
    bad = TemporalEdge(
        edge_id="e",
        from_entity="a",
        predicate="g",
        to_entity="b",
        valid_from="2026-04-14",
        jurisdiction="",
    )
    with pytest.raises(TemporalValidationError):
        validate_temporal_edge(bad)


def test_legacy_edge_backfill() -> None:
    edge = backfill_legacy_edge(
        edge_id="rel-law-pd1096-governs-concept-permit",
        from_entity="law-pd-1096",
        predicate="governs",
        to_entity="concept-building-permit",
    )
    assert edge.valid_from == "1977-02-19"
    assert edge.valid_until is None
    assert edge.jurisdiction == "national"


def test_legacy_edge_backfill_custom_date() -> None:
    edge = backfill_legacy_edge(
        edge_id="rel-x",
        from_entity="a",
        predicate="g",
        to_entity="b",
        legacy_date="2010-01-01",
        jurisdiction="lgu-cebu",
    )
    assert edge.valid_from == "2010-01-01"
    assert edge.jurisdiction == "lgu-cebu"


def test_filter_edges_valid_at_single_interval() -> None:
    e1 = TemporalEdge("e1", "a", "g", "b", valid_from="2020-01-01", valid_until="2022-12-31")
    e2 = TemporalEdge("e2", "a", "g", "c", valid_from="2023-01-01", valid_until=None)
    # 2021 → only e1 active
    active = filter_edges_valid_at([e1, e2], query_date="2021-06-15")
    assert [e.edge_id for e in active] == ["e1"]
    # 2024 → only e2
    active = filter_edges_valid_at([e1, e2], query_date="2024-06-15")
    assert [e.edge_id for e in active] == ["e2"]


def test_filter_edges_valid_at_endpoint_inclusive() -> None:
    e1 = TemporalEdge("e1", "a", "g", "b", valid_from="2020-01-01", valid_until="2022-12-31")
    # Both endpoints are inclusive
    assert filter_edges_valid_at([e1], query_date="2020-01-01")
    assert filter_edges_valid_at([e1], query_date="2022-12-31")
    # One day outside is not
    assert not filter_edges_valid_at([e1], query_date="2019-12-31")
    assert not filter_edges_valid_at([e1], query_date="2023-01-01")


def test_filter_by_jurisdiction() -> None:
    national = TemporalEdge("e1", "a", "g", "b", valid_from="2020-01-01", jurisdiction="national")
    qc = TemporalEdge("e2", "a", "g", "b", valid_from="2020-01-01", jurisdiction="lgu-quezon-city")
    active = filter_edges_valid_at([national, qc], query_date="2026-04-14", jurisdiction="lgu-quezon-city")
    assert [e.edge_id for e in active] == ["e2"]


def test_filter_by_jurisdiction_none_returns_all() -> None:
    national = TemporalEdge("e1", "a", "g", "b", valid_from="2020-01-01", jurisdiction="national")
    qc = TemporalEdge("e2", "a", "g", "b", valid_from="2020-01-01", jurisdiction="lgu-quezon-city")
    active = filter_edges_valid_at([national, qc], query_date="2026-04-14")
    assert {e.edge_id for e in active} == {"e1", "e2"}


def test_edge_is_frozen() -> None:
    edge = stamp_new_edge(
        edge_id="e",
        from_entity="a",
        predicate="g",
        to_entity="b",
        now=NOW,
    )
    with pytest.raises(AttributeError):
        edge.valid_from = "2000-01-01"  # type: ignore[misc]
