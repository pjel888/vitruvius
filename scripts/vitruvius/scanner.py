from __future__ import annotations

import hashlib
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

from .constants import RAW_LAYER_NAME
from .models import FileEntry
from .paths import ensure_registry_dir, ensure_snapshot_dir, get_repo_root
from .reports import write_csv, write_json, write_text
from .utils import iso_utc_from_timestamp, utc_now_stamp


def _sha256_of_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def build_file_entries(raw_root: Path) -> list[FileEntry]:
    entries: list[FileEntry] = []

    for path in sorted(raw_root.rglob("*")):
        if not path.is_file():
            continue

        stat = path.stat()
        rel = path.relative_to(raw_root).as_posix()
        parts = Path(rel).parts
        top_category = parts[0] if parts else "."

        entries.append(
            FileEntry(
                relative_path=rel,
                name=path.name,
                extension=path.suffix.lower(),
                size_bytes=stat.st_size,
                modified_utc=iso_utc_from_timestamp(stat.st_mtime),
                sha256=_sha256_of_file(path),
                parent_folder=path.parent.relative_to(raw_root).as_posix()
                if path.parent != raw_root
                else ".",
                top_category=top_category,
            )
        )

    return entries


def build_tree_lines(root: Path, base_indent: str = "") -> list[str]:
    lines: list[str] = [f"{base_indent}{root.name}/"]

    children = sorted(
        root.iterdir(),
        key=lambda p: (p.is_file(), p.name.lower()),
    )

    for child in children:
        if child.is_dir():
            lines.extend(build_tree_lines(child, base_indent + "  "))
        else:
            lines.append(f"{base_indent}  {child.name}")

    return lines


def run_scan() -> int:
    repo_root = get_repo_root()
    raw_root = repo_root / RAW_LAYER_NAME

    if not raw_root.exists():
        print(f"ERROR: Missing raw source layer: {raw_root}")
        return 1

    snapshot_dir = ensure_snapshot_dir(repo_root)
    registry_dir = ensure_registry_dir(repo_root)
    stamp = utc_now_stamp()

    file_entries = build_file_entries(raw_root)
    tree_lines = build_tree_lines(raw_root)

    payload = {
        "project": "Vitruvius",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "repo_root": str(repo_root),
        "raw_root": str(raw_root),
        "file_count": len(file_entries),
        "files": [asdict(entry) for entry in file_entries],
    }

    timestamped_json = snapshot_dir / f"{stamp}_raw_tree_snapshot.json"
    latest_json = snapshot_dir / "latest_raw_tree_snapshot.json"

    timestamped_txt = snapshot_dir / f"{stamp}_raw_tree_snapshot.txt"
    latest_txt = snapshot_dir / "latest_raw_tree_snapshot.txt"

    timestamped_csv = registry_dir / f"{stamp}_raw_file_registry.csv"
    latest_csv = registry_dir / "latest_raw_file_registry.csv"

    write_json(timestamped_json, payload)
    write_json(latest_json, payload)

    tree_text = "\n".join(tree_lines) + "\n"
    write_text(timestamped_txt, tree_text)
    write_text(latest_txt, tree_text)

    write_csv(timestamped_csv, file_entries)
    write_csv(latest_csv, file_entries)

    print("Scan complete.")
    print(f"Raw layer: {raw_root}")
    print(f"Files found: {len(file_entries)}")
    print(f"Latest JSON snapshot: {latest_json}")
    print(f"Latest TXT snapshot: {latest_txt}")
    print(f"Latest CSV registry: {latest_csv}")

    return 0