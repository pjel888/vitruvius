"""Table-to-Graph extractor — deterministic bipartite projection of CSV files."""

from __future__ import annotations

import json
from pathlib import Path

from vitruvius.parsers.table_graph_extractor import (
    TableEdge,
    TableNode,
    TableSubgraph,
    extract_table_subgraph,
)


def test_simple_csv_extracts_four_cell_edges(tmp_path: Path) -> None:
    csv = tmp_path / "table.csv"
    csv.write_text("Zone,MaxHeight,Setback\nR1,8,2\nR2,12,3\n")
    subgraph = extract_table_subgraph(csv)
    assert len(subgraph.edges) == 4


def test_header_row_becomes_column_nodes(tmp_path: Path) -> None:
    csv = tmp_path / "table.csv"
    csv.write_text("Zone,MaxHeight\nR1,8\n")
    subgraph = extract_table_subgraph(csv)
    col_names = {n.name for n in subgraph.column_nodes}
    assert col_names == {"MaxHeight"}
    assert len(subgraph.row_nodes) == 1
    assert subgraph.row_nodes[0].name == "R1"


def test_extract_deterministic_id_generation(tmp_path: Path) -> None:
    csv = tmp_path / "t.csv"
    csv.write_text("A,B\n1,2\n")
    sg1 = extract_table_subgraph(csv)
    sg2 = extract_table_subgraph(csv)
    assert [e.edge_id for e in sg1.edges] == [e.edge_id for e in sg2.edges]
    assert [n.id for n in sg1.row_nodes] == [n.id for n in sg2.row_nodes]
    assert [n.id for n in sg1.column_nodes] == [n.id for n in sg2.column_nodes]


def test_subgraph_serializes_to_json(tmp_path: Path) -> None:
    csv = tmp_path / "t.csv"
    csv.write_text("A,B\n1,2\n")
    sg = extract_table_subgraph(csv)
    out = tmp_path / "sg.json"
    out.write_text(json.dumps(sg.to_json_dict(), indent=2, sort_keys=True))
    data = json.loads(out.read_text())
    assert "edges" in data
    assert data["edges"][0]["cell_value"] == "2"


def test_empty_rows_are_skipped(tmp_path: Path) -> None:
    csv = tmp_path / "t.csv"
    csv.write_text("A,B\n1,2\n\n,\n3,4\n")
    subgraph = extract_table_subgraph(csv)
    assert len(subgraph.row_nodes) == 2
    assert len(subgraph.edges) == 2


def test_empty_cell_becomes_edge_with_empty_value(tmp_path: Path) -> None:
    csv = tmp_path / "t.csv"
    csv.write_text("A,B,C\n1,,3\n")
    subgraph = extract_table_subgraph(csv)
    assert len(subgraph.edges) == 2
    empty_edges = [e for e in subgraph.edges if e.cell_value == ""]
    assert len(empty_edges) == 1


def test_json_roundtrip_is_byte_identical(tmp_path: Path) -> None:
    csv = tmp_path / "t.csv"
    csv.write_text("A,B\n1,2\n3,4\n")
    sg1 = extract_table_subgraph(csv)
    sg2 = extract_table_subgraph(csv)
    s1 = json.dumps(sg1.to_json_dict(), sort_keys=True, indent=2)
    s2 = json.dumps(sg2.to_json_dict(), sort_keys=True, indent=2)
    assert s1 == s2
