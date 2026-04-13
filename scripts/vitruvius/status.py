from __future__ import annotations

from datetime import datetime, timezone

from .paths import ensure_registry_dir, ensure_runs_dir, get_repo_root
from .reports import (
    build_signature,
    get_timestamped_registry_files,
    read_csv_entries,
    write_json,
    write_text,
)
from .utils import utc_now_stamp


def run_status() -> int:
    repo_root = get_repo_root()
    registry_dir = ensure_registry_dir(repo_root)
    runs_dir = ensure_runs_dir(repo_root)

    registry_files = get_timestamped_registry_files(registry_dir)

    if len(registry_files) < 2:
        print("Not enough timestamped registry files to compare.")
        print("Run scan at least twice first.")
        return 1

    previous_file = registry_files[-2]
    current_file = registry_files[-1]

    previous_rows = read_csv_entries(previous_file)
    current_rows = read_csv_entries(current_file)

    previous_by_path = {row["relative_path"]: row for row in previous_rows}
    current_by_path = {row["relative_path"]: row for row in current_rows}

    previous_paths = set(previous_by_path.keys())
    current_paths = set(current_by_path.keys())

    new_paths = sorted(current_paths - previous_paths)
    missing_paths = sorted(previous_paths - current_paths)

    common_paths = sorted(previous_paths & current_paths)

    changed_paths: list[str] = []
    unchanged_paths: list[str] = []

    for rel_path in common_paths:
        prev_sig = build_signature(previous_by_path[rel_path])
        curr_sig = build_signature(current_by_path[rel_path])

        if prev_sig != curr_sig:
            changed_paths.append(rel_path)
        else:
            unchanged_paths.append(rel_path)

    report = {
        "project": "Vitruvius",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "previous_registry": str(previous_file),
        "current_registry": str(current_file),
        "summary": {
            "previous_count": len(previous_rows),
            "current_count": len(current_rows),
            "new_count": len(new_paths),
            "changed_count": len(changed_paths),
            "missing_count": len(missing_paths),
            "unchanged_count": len(unchanged_paths),
        },
        "new_files": new_paths,
        "changed_files": changed_paths,
        "missing_files": missing_paths,
        "unchanged_files": unchanged_paths,
    }

    stamp = utc_now_stamp()
    latest_json = runs_dir / "latest_status_report.json"
    timestamped_json = runs_dir / f"{stamp}_status_report.json"

    latest_txt = runs_dir / "latest_status_report.txt"
    timestamped_txt = runs_dir / f"{stamp}_status_report.txt"

    text_lines = [
        "Vitruvius Status Report",
        "",
        f"Previous registry: {previous_file.name}",
        f"Current registry: {current_file.name}",
        "",
        f"Previous count: {len(previous_rows)}",
        f"Current count: {len(current_rows)}",
        f"New files: {len(new_paths)}",
        f"Changed files: {len(changed_paths)}",
        f"Missing files: {len(missing_paths)}",
        f"Unchanged files: {len(unchanged_paths)}",
        "",
        "NEW FILES:",
        *([f"  {p}" for p in new_paths] or ["  None"]),
        "",
        "CHANGED FILES:",
        *([f"  {p}" for p in changed_paths] or ["  None"]),
        "",
        "MISSING FILES:",
        *([f"  {p}" for p in missing_paths] or ["  None"]),
    ]
    report_text = "\n".join(text_lines) + "\n"

    write_json(latest_json, report)
    write_json(timestamped_json, report)
    write_text(latest_txt, report_text)
    write_text(timestamped_txt, report_text)

    print("Status comparison complete.")
    print(f"Previous registry: {previous_file.name}")
    print(f"Current registry: {current_file.name}")
    print(f"New files: {len(new_paths)}")
    print(f"Changed files: {len(changed_paths)}")
    print(f"Missing files: {len(missing_paths)}")
    print(f"Unchanged files: {len(unchanged_paths)}")
    print(f"Latest status JSON: {latest_json}")
    print(f"Latest status TXT: {latest_txt}")

    return 0