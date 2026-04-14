"""Bipartite CSV-to-graph extractor for Task B.3 (statistical/architectural upgrade)."""

from __future__ import annotations

import csv
import hashlib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

_ID_LEN = 12


def _stable_id(*parts: str) -> str:
    """First 12 hex chars of SHA-1 over a NUL-joined parts tuple."""
    joined = "\x00".join(parts)
    return hashlib.sha1(joined.encode("utf-8")).hexdigest()[:_ID_LEN]


@dataclass(frozen=True)
class TableNode:
    id: str
    name: str
    kind: str


@dataclass(frozen=True)
class TableEdge:
    edge_id: str
    row_id: str
    col_id: str
    cell_value: str


@dataclass
class TableSubgraph:
    source_path: str
    row_nodes: list[TableNode] = field(default_factory=list)
    column_nodes: list[TableNode] = field(default_factory=list)
    edges: list[TableEdge] = field(default_factory=list)

    def to_json_dict(self) -> dict[str, Any]:
        return {
            "source_path": self.source_path,
            "row_nodes": [n.__dict__ for n in self.row_nodes],
            "column_nodes": [n.__dict__ for n in self.column_nodes],
            "edges": [e.__dict__ for e in self.edges],
        }


def extract_table_subgraph(csv_path: Path) -> TableSubgraph:
    """Project a CSV into a deterministic bipartite TableSubgraph.

    Assumes the first column is the row label. Empty/whitespace-only rows
    are skipped. Empty cells become edges with cell_value == "".
    """
    filename = csv_path.name
    subgraph = TableSubgraph(source_path=str(csv_path))

    with csv_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.reader(handle)
        try:
            header = next(reader)
        except StopIteration:
            return subgraph

        data_columns = header[1:]
        for col_name in data_columns:
            subgraph.column_nodes.append(
                TableNode(
                    id=f"col:{_stable_id(filename, col_name)}",
                    name=col_name,
                    kind="col",
                )
            )

        for raw_row in reader:
            if not any(cell.strip() for cell in raw_row):
                continue
            row_label = raw_row[0]
            row_id = f"row:{_stable_id(filename, row_label)}"
            subgraph.row_nodes.append(
                TableNode(id=row_id, name=row_label, kind="row")
            )
            for col_node, cell_value in zip(
                subgraph.column_nodes, raw_row[1 : 1 + len(data_columns)]
            ):
                subgraph.edges.append(
                    TableEdge(
                        edge_id=_stable_id(
                            filename, row_label, col_node.name, cell_value
                        ),
                        row_id=row_id,
                        col_id=col_node.id,
                        cell_value=cell_value,
                    )
                )

    return subgraph
