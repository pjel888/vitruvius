# scripts/vitruvius/graph/parquet_archiver.py
"""Sprint GT Stream GT.3.3 — Parquet archiver for TemporalEdge snapshots.

Uses pyarrow (already installed as a transitive Docling dependency).
Produces a columnar Parquet file suitable for cold-storage archival
of graph snapshots at a given UTC timestamp.
"""
from __future__ import annotations

from pathlib import Path
from typing import Iterable

import pyarrow as pa
import pyarrow.parquet as pq

from vitruvius.graph.contract import TemporalEdge


_SCHEMA = pa.schema([
    ("from_id", pa.string()),
    ("to_id", pa.string()),
    ("type", pa.string()),
    ("evidence_id", pa.string()),
    ("status", pa.string()),
    ("valid_from", pa.string()),
    ("valid_until", pa.string()),  # nullable — None becomes pa.null()
])


def write_temporal_edges_to_parquet(
    edges: Iterable[TemporalEdge],
    path: Path,
) -> None:
    """Write a sequence of TemporalEdges to a Parquet file at ``path``.
    The parent directory is created if missing. An empty iterable
    still produces a valid, schema-only Parquet file."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    rows = list(edges)
    columns: dict[str, list] = {
        "from_id": [e.from_id for e in rows],
        "to_id": [e.to_id for e in rows],
        "type": [e.type for e in rows],
        "evidence_id": [e.evidence_id for e in rows],
        "status": [e.status for e in rows],
        "valid_from": [e.valid_from for e in rows],
        "valid_until": [e.valid_until for e in rows],
    }
    table = pa.Table.from_pydict(columns, schema=_SCHEMA)
    pq.write_table(table, path)


def read_temporal_edges_from_parquet(path: Path) -> list[TemporalEdge]:
    """Read a Parquet file produced by ``write_temporal_edges_to_parquet``
    and rebuild the list of TemporalEdges. Preserves ``None`` for the
    open-interval ``valid_until`` column."""
    table = pq.read_table(Path(path))
    n = table.num_rows
    if n == 0:
        return []

    from_id = table.column("from_id").to_pylist()
    to_id = table.column("to_id").to_pylist()
    type_ = table.column("type").to_pylist()
    evidence_id = table.column("evidence_id").to_pylist()
    status = table.column("status").to_pylist()
    valid_from = table.column("valid_from").to_pylist()
    valid_until = table.column("valid_until").to_pylist()

    return [
        TemporalEdge(
            from_id=from_id[i],
            to_id=to_id[i],
            type=type_[i],
            evidence_id=evidence_id[i],
            status=status[i],
            valid_from=valid_from[i],
            valid_until=valid_until[i],
        )
        for i in range(n)
    ]
