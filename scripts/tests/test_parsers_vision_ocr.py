"""Stream Y5.1 + Y5.3 — vision OCR wrapper + ple-vision-probe tests."""
from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest

pytest.importorskip("PIL")

from vitruvius.parsers.vision_ocr import VisionExtractedTable, extract_table_from_image


FAKE_VISION_JSON = """
{
  "rows": [
    ["Header 1", "Header 2"],
    ["cell1", "cell2"],
    ["cell3", "cell4"]
  ],
  "caption": "Table VII.1 — Occupancy classification"
}
"""


def test_vision_call_parses_structured_json(tmp_path: Path) -> None:
    img_path = tmp_path / "page.png"
    img_path.write_bytes(b"FAKE_PNG_BYTES")

    with patch(
        "vitruvius.parsers.vision_ocr._call_ollama_vision",
        return_value=FAKE_VISION_JSON,
    ), patch(
        "vitruvius.parsers.vision_ocr._pixel_count",
        return_value=500_000,
    ):
        table = extract_table_from_image(img_path, model="moondream:latest")

    assert isinstance(table, VisionExtractedTable)
    assert len(table.rows) == 3
    assert table.rows[0] == ["Header 1", "Header 2"]
    assert "Occupancy" in table.caption


def test_vision_call_returns_none_on_empty_response(tmp_path: Path) -> None:
    img_path = tmp_path / "page.png"
    img_path.write_bytes(b"FAKE_PNG_BYTES")

    with patch(
        "vitruvius.parsers.vision_ocr._call_ollama_vision",
        return_value="",
    ), patch(
        "vitruvius.parsers.vision_ocr._pixel_count",
        return_value=500_000,
    ):
        table = extract_table_from_image(img_path, model="moondream:latest")
    assert table is None


def test_vision_call_rejects_oversized_image(tmp_path: Path) -> None:
    img_path = tmp_path / "page.png"
    img_path.write_bytes(b"x" * 100)
    with patch(
        "vitruvius.parsers.vision_ocr._pixel_count",
        return_value=2_100_000,
    ):
        with pytest.raises(ValueError, match="exceeds max_image_pixels"):
            extract_table_from_image(
                img_path,
                model="moondream:latest",
                max_pixels=2_000_000,
            )


# ---------------------------------------------------------------------------
# Stream Y5.3 — ple-vision-probe
# ---------------------------------------------------------------------------
def test_vision_probe_passes_when_ram_sufficient() -> None:
    from vitruvius.parsers.vision_ocr import run_ple_vision_probe

    with patch(
        "vitruvius.parsers.vision_ocr._free_ram_gb", return_value=4.0,
    ), patch(
        "vitruvius.parsers.vision_ocr._ollama_model_available", return_value=True,
    ):
        rc = run_ple_vision_probe(required_free_gb=3.5, model="moondream:latest")
    assert rc == 0


def test_vision_probe_fails_on_low_ram() -> None:
    from vitruvius.parsers.vision_ocr import run_ple_vision_probe

    with patch(
        "vitruvius.parsers.vision_ocr._free_ram_gb", return_value=1.0,
    ), patch(
        "vitruvius.parsers.vision_ocr._ollama_model_available", return_value=True,
    ):
        rc = run_ple_vision_probe(required_free_gb=3.5, model="moondream:latest")
    assert rc == 1


def test_vision_probe_fails_on_missing_model() -> None:
    from vitruvius.parsers.vision_ocr import run_ple_vision_probe

    with patch(
        "vitruvius.parsers.vision_ocr._free_ram_gb", return_value=4.0,
    ), patch(
        "vitruvius.parsers.vision_ocr._ollama_model_available", return_value=False,
    ):
        rc = run_ple_vision_probe(required_free_gb=3.5, model="moondream:latest")
    assert rc == 2
