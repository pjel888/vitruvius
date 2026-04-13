from __future__ import annotations

import csv
import json
from dataclasses import asdict
from pathlib import Path

from .models import FileEntry


def write_json(path: Path, payload: dict) -> None:
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def write_text(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")


def write_csv(path: Path, entries: list[FileEntry]) -> None:
    fieldnames = [
        "relative_path",
        "name",
        "extension",
        "size_bytes",
        "modified_utc",
        "parent_folder",
        "top_category",
    ]

    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for entry in entries:
            writer.writerow(asdict(entry))


def read_csv_entries(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def get_timestamped_registry_files(registry_dir: Path) -> list[Path]:
    files = [
        p
        for p in registry_dir.glob("*_raw_file_registry.csv")
        if not p.name.startswith("latest_")
    ]
    return sorted(files, key=lambda p: p.name)


def build_signature(row: dict[str, str]) -> tuple[str, str, str]:
    return (
        row["size_bytes"],
        row["modified_utc"],
        row["extension"],
    )