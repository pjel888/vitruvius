"""Stream O.1 — watched-sources registry loader tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from vitruvius.foraging.watched_sources import (
    WatchedSource,
    WatchedSourcesError,
    load_watched_sources,
)


def _write(tmp_path: Path, body: str) -> Path:
    path = tmp_path / "watched_sources.yaml"
    path.write_text(body, encoding="utf-8")
    return path


def test_load_empty_registry_returns_empty(tmp_path: Path) -> None:
    path = _write(tmp_path, "sources: []\n")
    assert load_watched_sources(path) == []


def test_load_single_source(tmp_path: Path) -> None:
    path = _write(
        tmp_path,
        "sources:\n"
        "  - name: DPWH\n"
        "    url: https://example.invalid/dpwh\n"
        "    category: 001-Laws\n"
        "    subcategory: RA-pending\n"
        "    frequency: weekly\n",
    )
    sources = load_watched_sources(path)
    assert len(sources) == 1
    src = sources[0]
    assert isinstance(src, WatchedSource)
    assert src.name == "DPWH"
    assert src.url == "https://example.invalid/dpwh"
    assert src.frequency == "weekly"


def test_invalid_frequency_rejected(tmp_path: Path) -> None:
    path = _write(
        tmp_path,
        "sources:\n"
        "  - name: DPWH\n"
        "    url: https://example.invalid\n"
        "    category: 001-Laws\n"
        "    frequency: hourly\n",
    )
    with pytest.raises(WatchedSourcesError, match="frequency"):
        load_watched_sources(path)


def test_non_https_url_rejected(tmp_path: Path) -> None:
    path = _write(
        tmp_path,
        "sources:\n"
        "  - name: Bad\n"
        "    url: http://insecure\n"
        "    category: 001-Laws\n"
        "    frequency: daily\n",
    )
    with pytest.raises(WatchedSourcesError, match="https"):
        load_watched_sources(path)


def test_duplicate_name_rejected(tmp_path: Path) -> None:
    path = _write(
        tmp_path,
        "sources:\n"
        "  - name: DPWH\n"
        "    url: https://example.invalid/a\n"
        "    category: 001-Laws\n"
        "    frequency: daily\n"
        "  - name: DPWH\n"
        "    url: https://example.invalid/b\n"
        "    category: 001-Laws\n"
        "    frequency: weekly\n",
    )
    with pytest.raises(WatchedSourcesError, match="duplicate"):
        load_watched_sources(path)
