"""Sprint GT Stream GT.5.1 — mmap-backed lazy page loader.

Thin Python wrapper around ``mmap.mmap`` so the GT.2 engine_rs
Rust crate (and the Python side) can share the same on-disk
octree page format. Keeping the loader in Python makes it
available before the Rust crate finishes its mmap integration
and lets the test suite exercise page behaviour without building
Rust.
"""
from __future__ import annotations

import mmap
from pathlib import Path
from types import TracebackType
from typing import Optional


class MmapPageReader:
    """Context-managed, read-only view over a binary page file."""

    def __init__(self, fh, mm: mmap.mmap) -> None:
        self._fh = fh
        self._mm: Optional[mmap.mmap] = mm

    @property
    def size(self) -> int:
        if self._mm is None:
            raise RuntimeError("page file is closed")
        return len(self._mm)

    def read(self, offset: int, length: int) -> bytes:
        if self._mm is None:
            raise RuntimeError("page file is closed")
        if offset < 0 or length < 0:
            raise ValueError(f"offset/length must be non-negative (got {offset}, {length})")
        if offset + length > len(self._mm):
            raise ValueError(
                f"read range [{offset}, {offset + length}) exceeds "
                f"page file size {len(self._mm)}"
            )
        return bytes(self._mm[offset : offset + length])

    def close(self) -> None:
        if self._mm is not None:
            self._mm.close()
            self._mm = None
        if self._fh is not None:
            self._fh.close()
            self._fh = None

    def __enter__(self) -> "MmapPageReader":
        return self

    def __exit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc: Optional[BaseException],
        tb: Optional[TracebackType],
    ) -> None:
        self.close()


def open_page_file(path: Path) -> MmapPageReader:
    """Open a binary page file and return a read-only
    ``MmapPageReader``. Caller must use the returned reader as a
    context manager (or explicitly call ``close``)."""
    path = Path(path)
    fh = open(path, "rb")
    mm = mmap.mmap(fh.fileno(), 0, access=mmap.ACCESS_READ)
    return MmapPageReader(fh, mm)
