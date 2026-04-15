# scripts/tests/test_parquet_archiver.py
"""Sprint GT Stream GT.3.3 — Parquet archiver round-trip."""
from __future__ import annotations

from pathlib import Path

import pytest

pyarrow = pytest.importorskip("pyarrow")

from vitruvius.graph.contract import TemporalEdge
from vitruvius.graph.parquet_archiver import (
    read_temporal_edges_from_parquet,
    write_temporal_edges_to_parquet,
)


@pytest.fixture
def five_edge_snapshot() -> list[TemporalEdge]:
    return [
        TemporalEdge(
            from_id=f"law-pd-109{i}",
            to_id="concept-egress-width",
            type="requires",
            evidence_id=f"rel-{i:04d}",
            status="verified",
            valid_from=f"200{i}-01-01T00:00:00Z",
            valid_until=None if i == 4 else f"201{i}-01-01T00:00:00Z",
        )
        for i in range(5)
    ]


def test_round_trip_preserves_row_count(
    tmp_path: Path, five_edge_snapshot: list[TemporalEdge]
) -> None:
    out = tmp_path / "snapshot.parquet"
    write_temporal_edges_to_parquet(five_edge_snapshot, out)
    assert out.exists()
    recovered = read_temporal_edges_from_parquet(out)
    assert len(recovered) == 5


def test_round_trip_preserves_field_values(
    tmp_path: Path, five_edge_snapshot: list[TemporalEdge]
) -> None:
    out = tmp_path / "snapshot.parquet"
    write_temporal_edges_to_parquet(five_edge_snapshot, out)
    recovered = read_temporal_edges_from_parquet(out)

    for original, restored in zip(five_edge_snapshot, recovered):
        assert restored.from_id == original.from_id
        assert restored.to_id == original.to_id
        assert restored.type == original.type
        assert restored.evidence_id == original.evidence_id
        assert restored.status == original.status
        assert restored.valid_from == original.valid_from
        assert restored.valid_until == original.valid_until


def test_round_trip_preserves_open_interval(
    tmp_path: Path, five_edge_snapshot: list[TemporalEdge]
) -> None:
    out = tmp_path / "snapshot.parquet"
    write_temporal_edges_to_parquet(five_edge_snapshot, out)
    recovered = read_temporal_edges_from_parquet(out)
    assert recovered[4].valid_until is None


def test_empty_list_round_trips(tmp_path: Path) -> None:
    out = tmp_path / "empty.parquet"
    write_temporal_edges_to_parquet([], out)
    assert out.exists()
    recovered = read_temporal_edges_from_parquet(out)
    assert recovered == []
