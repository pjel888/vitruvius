"""Sprint GT Stream GT.5.1 — mmap-backed page loader for octree binary files."""
from __future__ import annotations

from pathlib import Path

import pytest

from vitruvius.engine_rs.mmap_loader import (
    MmapPageReader,
    open_page_file,
)


@pytest.fixture
def fixture_page_file(tmp_path: Path) -> Path:
    """Write a 256-byte fixture page file: bytes 0..255 repeating."""
    path = tmp_path / "page_000.bin"
    path.write_bytes(bytes(range(256)))
    return path


def test_open_page_file_returns_reader(fixture_page_file: Path) -> None:
    with open_page_file(fixture_page_file) as reader:
        assert isinstance(reader, MmapPageReader)
        assert reader.size == 256


def test_read_first_100_bytes(fixture_page_file: Path) -> None:
    with open_page_file(fixture_page_file) as reader:
        data = reader.read(0, 100)
        assert len(data) == 100
        assert data == bytes(range(100))


def test_read_midfile_slice(fixture_page_file: Path) -> None:
    with open_page_file(fixture_page_file) as reader:
        data = reader.read(50, 10)
        assert data == bytes(range(50, 60))


def test_read_beyond_eof_raises(fixture_page_file: Path) -> None:
    with open_page_file(fixture_page_file) as reader:
        with pytest.raises(ValueError):
            reader.read(250, 100)  # 250 + 100 > 256


def test_context_manager_releases_mmap(fixture_page_file: Path) -> None:
    reader = open_page_file(fixture_page_file)
    with reader:
        pass
    # After exit the underlying mmap should be closed; reading
    # should fail with RuntimeError (our wrapper) or ValueError
    # (bare mmap).
    with pytest.raises((RuntimeError, ValueError)):
        reader.read(0, 1)
