"""Stream Y5.2 — vision OCR fallback hook tests."""
from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest

pytest.importorskip("PIL")

from vitruvius.parsers.table_graph_extractor import (
    extract_tables_with_vision_fallback,
)
from vitruvius.parsers.vision_ocr import VisionExtractedTable


def test_vision_fallback_invoked_on_csv_fail(monkeypatch, tmp_path: Path) -> None:
    from vitruvius import config as cfgmod
    monkeypatch.setattr(cfgmod, "_features_block", lambda: {"y_vision_ocr": True})

    page_image = tmp_path / "p1.png"
    page_image.write_bytes(b"PNG_BYTES")

    fake_table = VisionExtractedTable(
        rows=[["a", "b"], ["1", "2"]],
        caption="synthetic",
        source_image=page_image,
    )
    with patch(
        "vitruvius.parsers.table_graph_extractor.extract_table_from_image",
        return_value=fake_table,
    ) as mock_vision:
        result = extract_tables_with_vision_fallback(
            page_image=page_image,
            csv_result=None,
        )
    assert result is fake_table
    assert mock_vision.call_count == 1


def test_vision_fallback_not_invoked_when_csv_succeeded(
    monkeypatch, tmp_path: Path
) -> None:
    from vitruvius import config as cfgmod
    monkeypatch.setattr(cfgmod, "_features_block", lambda: {"y_vision_ocr": True})

    page_image = tmp_path / "p1.png"
    page_image.write_bytes(b"PNG")

    existing = object()  # sentinel — pretend CSV extractor returned a table

    with patch(
        "vitruvius.parsers.table_graph_extractor.extract_table_from_image",
    ) as mock_vision:
        result = extract_tables_with_vision_fallback(
            page_image=page_image,
            csv_result=existing,
        )
    assert result is existing
    assert mock_vision.call_count == 0


def test_vision_fallback_skipped_when_flag_off(
    monkeypatch, tmp_path: Path
) -> None:
    from vitruvius import config as cfgmod
    monkeypatch.setattr(cfgmod, "_features_block", lambda: {"y_vision_ocr": False})

    page_image = tmp_path / "p1.png"
    page_image.write_bytes(b"PNG")

    with patch(
        "vitruvius.parsers.table_graph_extractor.extract_table_from_image",
    ) as mock_vision:
        result = extract_tables_with_vision_fallback(
            page_image=page_image,
            csv_result=None,
        )
    assert result is None
    assert mock_vision.call_count == 0
