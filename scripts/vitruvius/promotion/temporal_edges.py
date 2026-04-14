from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import date, datetime, timezone
from typing import Iterable

DEFAULT_JURISDICTION = "national"
ISO_DATE_FORMAT = "%Y-%m-%d"
PD_1096_SIGNING_DATE = "1977-02-19"


@dataclass(frozen=True)
class TemporalEdge:
    """A knowledge-graph edge with temporal and jurisdictional validity."""

    edge_id: str
    from_entity: str
    predicate: str
    to_entity: str
    valid_from: str
    valid_until: str | None = None
    jurisdiction: str = DEFAULT_JURISDICTION


class TemporalValidationError(ValueError):
    """Raised when a TemporalEdge has inconsistent date bounds or jurisdiction."""


def _parse_iso_date(text: str) -> date:
    return datetime.strptime(text, ISO_DATE_FORMAT).date()


def _today_iso(now: datetime | None = None) -> str:
    moment = now if now is not None else datetime.now(timezone.utc)
    return moment.strftime(ISO_DATE_FORMAT)


def validate_temporal_edge(edge: TemporalEdge) -> None:
    if not edge.jurisdiction:
        raise TemporalValidationError(
            f"validate_temporal_edge: edge {edge.edge_id!r} has empty jurisdiction"
        )

    try:
        from_date = _parse_iso_date(edge.valid_from)
    except ValueError as exc:
        raise TemporalValidationError(
            f"validate_temporal_edge: edge {edge.edge_id!r} has malformed "
            f"valid_from={edge.valid_from!r}; expected YYYY-MM-DD"
        ) from exc

    if edge.valid_until is None:
        return

    try:
        until_date = _parse_iso_date(edge.valid_until)
    except ValueError as exc:
        raise TemporalValidationError(
            f"validate_temporal_edge: edge {edge.edge_id!r} has malformed "
            f"valid_until={edge.valid_until!r}; expected YYYY-MM-DD"
        ) from exc

    if until_date < from_date:
        raise TemporalValidationError(
            f"validate_temporal_edge: edge {edge.edge_id!r} has "
            f"valid_until={edge.valid_until!r} before valid_from={edge.valid_from!r}"
        )


def stamp_new_edge(
    *,
    edge_id: str,
    from_entity: str,
    predicate: str,
    to_entity: str,
    jurisdiction: str = DEFAULT_JURISDICTION,
    now: datetime | None = None,
) -> TemporalEdge:
    """Create a freshly-stamped TemporalEdge with valid_from=today, valid_until=None."""
    edge = TemporalEdge(
        edge_id=edge_id,
        from_entity=from_entity,
        predicate=predicate,
        to_entity=to_entity,
        valid_from=_today_iso(now),
        valid_until=None,
        jurisdiction=jurisdiction,
    )
    validate_temporal_edge(edge)
    return edge


def cap_predecessor(
    predecessor: TemporalEdge,
    *,
    cap_date: str | None = None,
    now: datetime | None = None,
) -> TemporalEdge:
    """Return a copy of `predecessor` with `valid_until` stamped (today or `cap_date`)."""
    cap_str = cap_date if cap_date is not None else _today_iso(now)

    try:
        cap_parsed = _parse_iso_date(cap_str)
    except ValueError as exc:
        raise TemporalValidationError(
            f"cap_predecessor: malformed cap_date={cap_str!r}; expected YYYY-MM-DD"
        ) from exc

    try:
        from_parsed = _parse_iso_date(predecessor.valid_from)
    except ValueError as exc:
        raise TemporalValidationError(
            f"cap_predecessor: predecessor {predecessor.edge_id!r} has malformed "
            f"valid_from={predecessor.valid_from!r}"
        ) from exc

    if cap_parsed < from_parsed:
        raise TemporalValidationError(
            f"cap_predecessor: cap_date={cap_str!r} is before "
            f"predecessor.valid_from={predecessor.valid_from!r} "
            f"(edge_id={predecessor.edge_id!r})"
        )

    capped = replace(predecessor, valid_until=cap_str)
    validate_temporal_edge(capped)
    return capped


def backfill_legacy_edge(
    *,
    edge_id: str,
    from_entity: str,
    predicate: str,
    to_entity: str,
    jurisdiction: str = DEFAULT_JURISDICTION,
    legacy_date: str = PD_1096_SIGNING_DATE,
) -> TemporalEdge:
    """Create a TemporalEdge for a pre-upgrade entry with an explicit valid_from."""
    edge = TemporalEdge(
        edge_id=edge_id,
        from_entity=from_entity,
        predicate=predicate,
        to_entity=to_entity,
        valid_from=legacy_date,
        valid_until=None,
        jurisdiction=jurisdiction,
    )
    validate_temporal_edge(edge)
    return edge


def filter_edges_valid_at(
    edges: Iterable[TemporalEdge],
    *,
    query_date: str,
    jurisdiction: str | None = None,
) -> list[TemporalEdge]:
    """Return the subset of edges whose validity interval contains `query_date`."""
    try:
        target = _parse_iso_date(query_date)
    except ValueError as exc:
        raise TemporalValidationError(
            f"filter_edges_valid_at: malformed query_date={query_date!r}; "
            f"expected YYYY-MM-DD"
        ) from exc

    matches: list[TemporalEdge] = []
    for edge in edges:
        if jurisdiction is not None and edge.jurisdiction != jurisdiction:
            continue

        try:
            from_date = _parse_iso_date(edge.valid_from)
        except ValueError as exc:
            raise TemporalValidationError(
                f"filter_edges_valid_at: edge {edge.edge_id!r} has malformed "
                f"valid_from={edge.valid_from!r}"
            ) from exc

        if target < from_date:
            continue

        if edge.valid_until is not None:
            try:
                until_date = _parse_iso_date(edge.valid_until)
            except ValueError as exc:
                raise TemporalValidationError(
                    f"filter_edges_valid_at: edge {edge.edge_id!r} has malformed "
                    f"valid_until={edge.valid_until!r}"
                ) from exc
            if target > until_date:
                continue

        matches.append(edge)

    return matches
