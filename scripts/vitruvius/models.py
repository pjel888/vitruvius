from __future__ import annotations

from dataclasses import dataclass


@dataclass
class FileEntry:
    relative_path: str
    name: str
    extension: str
    size_bytes: int
    modified_utc: str
    parent_folder: str
    top_category: str