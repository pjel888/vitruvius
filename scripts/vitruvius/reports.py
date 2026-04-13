from __future__ import annotations

import csv
import json
import shutil
from dataclasses import asdict
from pathlib import Path

from .models import FileEntry


CONVERSION_REGISTRY_HEADERS = [
    "timestamp_utc",
    "run_command",
    "source_relative_path",
    "logical_source_relative_path",
    "source_extension",
    "source_size_bytes",
    "source_modified_utc",
    "top_category",
    "detected_pdf_type",
    "processing_route",
    "status",
    "output_markdown_relative_path",
    "output_json_relative_path",
    "output_ocr_pdf_relative_path",
    "error_message",
]

SPREADSHEET_REGISTRY_HEADERS = [
    "timestamp_utc",
    "run_command",
    "source_relative_path",
    "logical_source_relative_path",
    "source_extension",
    "source_size_bytes",
    "source_modified_utc",
    "top_category",
    "sheet_name",
    "output_csv_relative_path",
    "output_json_relative_path",
    "row_count",
    "column_count",
    "status",
    "error_message",
]


def ensure_parent_dir(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def ensure_csv_with_headers(path: Path, headers: list[str]) -> None:
    ensure_parent_dir(path)

    if path.exists():
        return

    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()


def ensure_conversion_registry_exists(registry_dir: Path) -> Path:
    latest_path = registry_dir / "latest_conversion_registry.csv"
    ensure_csv_with_headers(latest_path, CONVERSION_REGISTRY_HEADERS)
    return latest_path


def ensure_spreadsheet_registry_exists(registry_dir: Path) -> Path:
    latest_path = registry_dir / "latest_spreadsheet_registry.csv"
    ensure_csv_with_headers(latest_path, SPREADSHEET_REGISTRY_HEADERS)
    return latest_path


def write_json(path: Path, payload: dict) -> None:
    ensure_parent_dir(path)
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def write_text(path: Path, content: str) -> None:
    ensure_parent_dir(path)
    path.write_text(content, encoding="utf-8")


def write_csv(path: Path, entries: list[FileEntry]) -> None:
    ensure_parent_dir(path)

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


def append_conversion_registry_row(registry_dir: Path, row: dict) -> Path:
    latest_path = ensure_conversion_registry_exists(registry_dir)

    normalized_row = {key: row.get(key, "") for key in CONVERSION_REGISTRY_HEADERS}

    with latest_path.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CONVERSION_REGISTRY_HEADERS)
        writer.writerow(normalized_row)

    return latest_path


def snapshot_conversion_registry(registry_dir: Path, timestamp_utc: str) -> Path:
    latest_path = ensure_conversion_registry_exists(registry_dir)
    snapshot_path = registry_dir / f"{timestamp_utc}_conversion_registry.csv"
    shutil.copy2(latest_path, snapshot_path)
    return snapshot_path


def append_spreadsheet_registry_row(registry_dir: Path, row: dict) -> Path:
    latest_path = ensure_spreadsheet_registry_exists(registry_dir)

    normalized_row = {key: row.get(key, "") for key in SPREADSHEET_REGISTRY_HEADERS}

    with latest_path.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=SPREADSHEET_REGISTRY_HEADERS)
        writer.writerow(normalized_row)

    return latest_path


def snapshot_spreadsheet_registry(registry_dir: Path, timestamp_utc: str) -> Path:
    latest_path = ensure_spreadsheet_registry_exists(registry_dir)
    snapshot_path = registry_dir / f"{timestamp_utc}_spreadsheet_registry.csv"
    shutil.copy2(latest_path, snapshot_path)
    return snapshot_path