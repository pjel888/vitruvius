"""Table-to-Graph XLSX wrapper — multi-sheet deterministic projection."""

from __future__ import annotations

from pathlib import Path

from openpyxl import Workbook

from vitruvius.parsers.table_graph_extractor import (
    TableSubgraph,
    extract_xlsx_subgraphs,
)


def _make_workbook(path: Path, sheets: dict[str, list[list]]) -> None:
    wb = Workbook()
    default = wb.active
    wb.remove(default)
    for name, rows in sheets.items():
        ws = wb.create_sheet(title=name)
        for row in rows:
            ws.append(row)
    wb.save(path)


def test_single_sheet_xlsx_returns_one_subgraph(tmp_path: Path) -> None:
    xlsx = tmp_path / "one.xlsx"
    _make_workbook(xlsx, {
        "Sheet1": [
            ["Zone", "MaxHeight", "Setback"],
            ["R1", 8, 2],
            ["R2", 12, 3],
        ],
    })
    subgraphs = extract_xlsx_subgraphs(xlsx)
    assert len(subgraphs) == 1
    sg = subgraphs[0]
    assert isinstance(sg, TableSubgraph)
    assert len(sg.row_nodes) == 2
    assert len(sg.column_nodes) == 2
    assert len(sg.edges) == 4


def test_multi_sheet_xlsx_returns_subgraph_per_sheet(tmp_path: Path) -> None:
    xlsx = tmp_path / "multi.xlsx"
    _make_workbook(xlsx, {
        "Zoning": [["Zone", "MaxHeight"], ["R1", 8]],
        "Occupancy": [["Class", "MaxLoad"], ["A1", 50], ["A2", 100]],
    })
    subgraphs = extract_xlsx_subgraphs(xlsx)
    assert len(subgraphs) == 2
    assert "#Zoning" in subgraphs[0].source_path
    assert "#Occupancy" in subgraphs[1].source_path
    assert len(subgraphs[1].row_nodes) == 2


def test_xlsx_source_path_uses_hash_delimiter(tmp_path: Path) -> None:
    xlsx = tmp_path / "delim.xlsx"
    _make_workbook(xlsx, {"SheetA": [["A", "B"], [1, 2]]})
    sg = extract_xlsx_subgraphs(xlsx)[0]
    assert sg.source_path == f"{xlsx.name}#SheetA"


def test_xlsx_empty_sheet_returns_empty_subgraph(tmp_path: Path) -> None:
    xlsx = tmp_path / "empty.xlsx"
    _make_workbook(xlsx, {
        "Full": [["A", "B"], [1, 2]],
        "Empty": [],
    })
    subgraphs = extract_xlsx_subgraphs(xlsx)
    assert len(subgraphs) == 2
    empty = next(sg for sg in subgraphs if "#Empty" in sg.source_path)
    assert empty.row_nodes == []
    assert empty.column_nodes == []
    assert empty.edges == []


def test_xlsx_numeric_cells_become_string_values(tmp_path: Path) -> None:
    xlsx = tmp_path / "nums.xlsx"
    _make_workbook(xlsx, {"S": [["A", "B"], [1, 2.5]]})
    sg = extract_xlsx_subgraphs(xlsx)[0]
    values = {e.cell_value for e in sg.edges}
    assert values == {"2.5"}
    assert sg.row_nodes[0].name == "1"


def test_xlsx_none_cells_become_empty_strings(tmp_path: Path) -> None:
    xlsx = tmp_path / "holes.xlsx"
    _make_workbook(xlsx, {"S": [["A", "B", "C"], [1, None, 3]]})
    sg = extract_xlsx_subgraphs(xlsx)[0]
    vals = sorted(e.cell_value for e in sg.edges)
    assert vals == ["", "3"]


def test_xlsx_deterministic_across_runs(tmp_path: Path) -> None:
    xlsx = tmp_path / "stable.xlsx"
    _make_workbook(xlsx, {"S": [["A", "B"], [1, 2], [3, 4]]})
    sg1 = extract_xlsx_subgraphs(xlsx)[0]
    sg2 = extract_xlsx_subgraphs(xlsx)[0]
    assert [e.edge_id for e in sg1.edges] == [e.edge_id for e in sg2.edges]
    assert [n.id for n in sg1.row_nodes] == [n.id for n in sg2.row_nodes]


def test_xlsx_header_only_sheet_has_columns_but_no_rows(tmp_path: Path) -> None:
    xlsx = tmp_path / "headeronly.xlsx"
    _make_workbook(xlsx, {"S": [["A", "B", "C"]]})
    sg = extract_xlsx_subgraphs(xlsx)[0]
    assert len(sg.column_nodes) == 2
    assert sg.row_nodes == []
    assert sg.edges == []


def test_xlsx_whitespace_only_rows_are_skipped(tmp_path: Path) -> None:
    xlsx = tmp_path / "ws.xlsx"
    _make_workbook(xlsx, {
        "S": [
            ["A", "B"],
            ["1", "2"],
            [None, None],
            ["  ", "  "],
            ["3", "4"],
        ],
    })
    sg = extract_xlsx_subgraphs(xlsx)[0]
    assert len(sg.row_nodes) == 2
    assert len(sg.edges) == 2


def test_xlsx_cross_sheet_ids_differ_for_same_row_label(tmp_path: Path) -> None:
    xlsx = tmp_path / "dup.xlsx"
    _make_workbook(xlsx, {
        "One": [["Key", "Value"], ["R1", "a"]],
        "Two": [["Key", "Value"], ["R1", "b"]],
    })
    subgraphs = extract_xlsx_subgraphs(xlsx)
    one_row_id = subgraphs[0].row_nodes[0].id
    two_row_id = subgraphs[1].row_nodes[0].id
    assert one_row_id != two_row_id
