from __future__ import annotations

from pathlib import Path

from .constants import (
    MANIFESTS_NAME,
    REGISTRIES_NAME,
    RUNS_NAME,
    TREE_SNAPSHOTS_NAME,
)


def get_repo_root() -> Path:
    return Path(__file__).resolve().parent.parent.parent


def ensure_snapshot_dir(repo_root: Path) -> Path:
    path = repo_root / MANIFESTS_NAME / TREE_SNAPSHOTS_NAME
    path.mkdir(parents=True, exist_ok=True)
    return path


def ensure_registry_dir(repo_root: Path) -> Path:
    path = repo_root / MANIFESTS_NAME / REGISTRIES_NAME
    path.mkdir(parents=True, exist_ok=True)
    return path


def ensure_runs_dir(repo_root: Path) -> Path:
    path = repo_root / MANIFESTS_NAME / RUNS_NAME
    path.mkdir(parents=True, exist_ok=True)
    return path


def build_conversion_relative_paths(relative_source_path: str) -> tuple[Path, Path]:
    src = Path(relative_source_path)

    if len(src.parts) < 2:
        raise ValueError(f"Unexpected source path structure: {relative_source_path}")

    top_category = src.parts[0]
    nested_parts = src.parts[1:-1]
    stem = src.stem

    markdown_rel = Path(top_category) / "raw_markdown" / Path(*nested_parts) / f"{stem}.md"
    json_rel = Path(top_category) / "sidecar_json" / Path(*nested_parts) / f"{stem}.json"

    return markdown_rel, json_rel


def build_ocr_pdf_relative_path(relative_source_path: str) -> Path:
    src = Path(relative_source_path)

    if len(src.parts) < 2:
        raise ValueError(f"Unexpected source path structure: {relative_source_path}")

    top_category = src.parts[0]
    nested_parts = src.parts[1:-1]
    filename = src.name

    return Path(top_category) / "ocr_pdf" / Path(*nested_parts) / filename


def build_office_pdf_relative_path(relative_source_path: str) -> Path:
    src = Path(relative_source_path)

    if len(src.parts) < 2:
        raise ValueError(f"Unexpected source path structure: {relative_source_path}")

    top_category = src.parts[0]
    nested_parts = src.parts[1:-1]
    stem = src.stem

    return Path(top_category) / "office_pdf" / Path(*nested_parts) / f"{stem}.pdf"


def build_spreadsheet_csv_relative_dir(relative_source_path: str) -> Path:
    src = Path(relative_source_path)

    if len(src.parts) < 2:
        raise ValueError(f"Unexpected source path structure: {relative_source_path}")

    top_category = src.parts[0]
    nested_parts = src.parts[1:-1]
    stem = src.stem

    return Path(top_category) / "spreadsheet_csv" / Path(*nested_parts) / stem


def build_spreadsheet_json_relative_dir(relative_source_path: str) -> Path:
    src = Path(relative_source_path)

    if len(src.parts) < 2:
        raise ValueError(f"Unexpected source path structure: {relative_source_path}")

    top_category = src.parts[0]
    nested_parts = src.parts[1:-1]
    stem = src.stem

    return Path(top_category) / "spreadsheet_json" / Path(*nested_parts) / stem


def build_spreadsheet_manifest_relative_path(relative_source_path: str) -> Path:
    src = Path(relative_source_path)

    if len(src.parts) < 2:
        raise ValueError(f"Unexpected source path structure: {relative_source_path}")

    top_category = src.parts[0]
    nested_parts = src.parts[1:-1]
    stem = src.stem

    return Path(top_category) / "spreadsheet_manifest" / Path(*nested_parts) / f"{stem}.json"