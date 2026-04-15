"""Stream S3.1 — Delta wrapper on top of the event store."""
from __future__ import annotations

from vitruvius.graph.event_store import Delta


def test_delta_round_trip() -> None:
    delta = Delta(
        event_id="evt_001",
        edge_id="building_42->setback_rule_3",
        kind="upsert",
        payload={"distance": 1.8},
    )
    payload = delta.to_json()
    restored = Delta.from_json(payload)
    assert restored == delta


def test_delta_rejects_unknown_kind() -> None:
    import pytest

    with pytest.raises(ValueError):
        Delta(
            event_id="evt_002",
            edge_id="building_42->setback_rule_3",
            kind="frobnicate",
            payload={},
        )


def test_delta_upsert_and_delete_accepted() -> None:
    Delta(event_id="a", edge_id="x->y", kind="upsert", payload={})
    Delta(event_id="b", edge_id="x->y", kind="delete", payload={})
