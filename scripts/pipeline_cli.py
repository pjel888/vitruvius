from __future__ import annotations

from collections import defaultdict
import argparse
import csv
import json
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from pypdf import PdfReader


RAW_LAYER_NAME = "001_Raw-Source-Layer"
CONVERSION_LAYER_NAME = "002_Raw-Conversion-Layer"
MANIFESTS_NAME = "006_System-Manifests"
TREE_SNAPSHOTS_NAME = "tree-snapshots"
REGISTRIES_NAME = "registries"
RUNS_NAME = "runs"


@dataclass
class FileEntry:
    relative_path: str
    name: str
    extension: str
    size_bytes: int
    modified_utc: str
    parent_folder: str
    top_category: str


def utc_now_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def iso_utc_from_timestamp(ts: float) -> str:
    return datetime.fromtimestamp(ts, tz=timezone.utc).isoformat()


def get_repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


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


def write_json(path: Path, payload: dict[str, Any]) -> None:
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


def normalize_filename(name: str) -> str:
    path = Path(name)
    stem = "".join(ch.lower() for ch in path.stem if ch.isalnum())
    ext = path.suffix.lower()
    return f"{stem}{ext}"


def normalize_text(text: str) -> str:
    return " ".join(text.split())


def detect_pdf_type(pdf_path: Path, sample_pages: int = 5) -> dict[str, Any]:
    if not pdf_path.exists():
        raise FileNotFoundError(f"File not found: {pdf_path}")

    reader = PdfReader(str(pdf_path))
    total_pages = len(reader.pages)
    pages_to_check = min(sample_pages, total_pages)

    page_details: list[dict[str, Any]] = []
    total_chars = 0
    pages_with_text = 0

    for i in range(pages_to_check):
        raw = reader.pages[i].extract_text() or ""
        text = normalize_text(raw)
        char_count = len(text)

        if char_count >= 50:
            pages_with_text += 1

        total_chars += char_count
        page_details.append(
            {
                "page_number": i + 1,
                "extracted_characters": char_count,
            }
        )

    likely_text_pdf = (
        pages_with_text >= max(1, pages_to_check // 2)
        and total_chars >= 300
    )

    return {
        "pdf_path": str(pdf_path),
        "total_pages": total_pages,
        "pages_sampled": pages_to_check,
        "pages_with_usable_text": pages_with_text,
        "total_extracted_characters": total_chars,
        "page_details": page_details,
        "result": "TEXT_PDF" if likely_text_pdf else "LIKELY_SCANNED_PDF",
        "recommended_route": "OPENDATALOADER_DIRECT"
        if likely_text_pdf
        else "OCR_FIRST_THEN_OPENDATALOADER",
    }


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


def run_lint() -> int:
    repo_root = get_repo_root()
    registry_dir = ensure_registry_dir(repo_root)
    runs_dir = ensure_runs_dir(repo_root)

    latest_csv = registry_dir / "latest_raw_file_registry.csv"
    if not latest_csv.exists():
        print("No latest_raw_file_registry.csv found.")
        print("Run scan first.")
        return 1

    rows = read_csv_entries(latest_csv)

    non_pdf_files: list[str] = []
    duplicate_name_groups: dict[str, list[str]] = defaultdict(list)

    for row in rows:
        rel_path = row["relative_path"]
        ext = row["extension"].lower()
        name = row["name"]

        if ext != ".pdf":
            non_pdf_files.append(rel_path)

        duplicate_name_groups[normalize_filename(name)].append(rel_path)

    duplicate_like_files = []
    for _, paths in duplicate_name_groups.items():
        if len(paths) > 1:
            duplicate_like_files.append(sorted(paths))

    duplicate_like_files = sorted(
        duplicate_like_files,
        key=lambda g: (len(g), g[0]),
        reverse=True,
    )

    report = {
        "project": "Vitruvius",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_registry": str(latest_csv),
        "summary": {
            "total_files": len(rows),
            "non_pdf_count": len(non_pdf_files),
            "duplicate_like_group_count": len(duplicate_like_files),
        },
        "non_pdf_files": sorted(non_pdf_files),
        "duplicate_like_files": duplicate_like_files,
    }

    stamp = utc_now_stamp()
    latest_json = runs_dir / "latest_lint_report.json"
    timestamped_json = runs_dir / f"{stamp}_lint_report.json"

    latest_txt = runs_dir / "latest_lint_report.txt"
    timestamped_txt = runs_dir / f"{stamp}_lint_report.txt"

    text_lines = [
        "Vitruvius Lint Report",
        "",
        f"Total files: {len(rows)}",
        f"Non-PDF files: {len(non_pdf_files)}",
        f"Duplicate-like filename groups: {len(duplicate_like_files)}",
        "",
        "NON-PDF FILES:",
        *([f"  {p}" for p in sorted(non_pdf_files)] or ["  None"]),
        "",
        "DUPLICATE-LIKE FILE GROUPS:",
    ]

    if duplicate_like_files:
        for group in duplicate_like_files:
            text_lines.append("  ---")
            for path in group:
                text_lines.append(f"  {path}")
    else:
        text_lines.append("  None")

    report_text = "\n".join(text_lines) + "\n"

    write_json(latest_json, report)
    write_json(timestamped_json, report)
    write_text(latest_txt, report_text)
    write_text(timestamped_txt, report_text)

    print("Lint complete.")
    print(f"Non-PDF files: {len(non_pdf_files)}")
    print(f"Duplicate-like filename groups: {len(duplicate_like_files)}")
    print(f"Latest lint JSON: {latest_json}")
    print(f"Latest lint TXT: {latest_txt}")

    return 0


def run_convert() -> int:
    repo_root = get_repo_root()
    runs_dir = ensure_runs_dir(repo_root)

    latest_status_json = runs_dir / "latest_status_report.json"
    if not latest_status_json.exists():
        print("No latest_status_report.json found.")
        print("Run pipeline_cli.py run first.")
        return 1

    status_report = json.loads(latest_status_json.read_text(encoding="utf-8"))

    candidates = sorted(
        set(status_report.get("new_files", [])) | set(status_report.get("changed_files", []))
    )

    pdf_candidates = [p for p in candidates if Path(p).suffix.lower() == ".pdf"]
    skipped_non_pdf = [p for p in candidates if Path(p).suffix.lower() != ".pdf"]

    queue_items = []
    for rel_path in pdf_candidates:
        src_path = Path(rel_path)
        top_category = src_path.parts[0] if src_path.parts else "."
        stem = src_path.stem
        md_rel = Path(top_category) / "raw_markdown" / f"{stem}.md"
        json_rel = Path(top_category) / "sidecar_json" / f"{stem}.json"

        queue_items.append(
            {
                "source_relative_path": rel_path,
                "top_category": top_category,
                "planned_markdown_output": md_rel.as_posix(),
                "planned_sidecar_output": json_rel.as_posix(),
                "status": "queued",
            }
        )

    report = {
        "project": "Vitruvius",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "status_source": str(latest_status_json),
        "summary": {
            "candidate_count": len(candidates),
            "queued_pdf_count": len(queue_items),
            "skipped_non_pdf_count": len(skipped_non_pdf),
        },
        "queued_items": queue_items,
        "skipped_non_pdf": skipped_non_pdf,
    }

    stamp = utc_now_stamp()
    latest_json = runs_dir / "latest_convert_queue.json"
    timestamped_json = runs_dir / f"{stamp}_convert_queue.json"

    latest_txt = runs_dir / "latest_convert_queue.txt"
    timestamped_txt = runs_dir / f"{stamp}_convert_queue.txt"

    text_lines = [
        "Vitruvius Convert Queue",
        "",
        f"Candidate files from status: {len(candidates)}",
        f"Queued PDF files: {len(queue_items)}",
        f"Skipped non-PDF files: {len(skipped_non_pdf)}",
        "",
        "QUEUED ITEMS:",
    ]

    if queue_items:
        for item in queue_items:
            text_lines.append("  ---")
            text_lines.append(f"  source: {item['source_relative_path']}")
            text_lines.append(f"  markdown: {item['planned_markdown_output']}")
            text_lines.append(f"  sidecar: {item['planned_sidecar_output']}")
    else:
        text_lines.append("  None")

    text_lines.extend(["", "SKIPPED NON-PDF:"])
    if skipped_non_pdf:
        for item in skipped_non_pdf:
            text_lines.append(f"  {item}")
    else:
        text_lines.append("  None")

    report_text = "\n".join(text_lines) + "\n"

    write_json(latest_json, report)
    write_json(timestamped_json, report)
    write_text(latest_txt, report_text)
    write_text(timestamped_txt, report_text)

    print("Convert queue complete.")
    print(f"Candidate files: {len(candidates)}")
    print(f"Queued PDF files: {len(queue_items)}")
    print(f"Skipped non-PDF files: {len(skipped_non_pdf)}")
    print(f"Latest convert queue JSON: {latest_json}")
    print(f"Latest convert queue TXT: {latest_txt}")

    return 0


def run_detect_one(relative_pdf_path: str, sample_pages: int = 5) -> int:
    repo_root = get_repo_root()
    runs_dir = ensure_runs_dir(repo_root)
    pdf_path = repo_root / RAW_LAYER_NAME / relative_pdf_path

    if pdf_path.suffix.lower() != ".pdf":
        print("ERROR: detect-one only accepts PDF files.")
        return 1

    try:
        report = detect_pdf_type(pdf_path, sample_pages=sample_pages)
    except FileNotFoundError as exc:
        print(f"ERROR: {exc}")
        return 1

    stamp = utc_now_stamp()
    safe_stem = pdf_path.stem.replace("/", "_").replace("\\", "_")

    latest_json = runs_dir / "latest_detect_one_report.json"
    timestamped_json = runs_dir / f"{stamp}_{safe_stem}_detect_one_report.json"

    latest_txt = runs_dir / "latest_detect_one_report.txt"
    timestamped_txt = runs_dir / f"{stamp}_{safe_stem}_detect_one_report.txt"

    text_lines = [
        "Vitruvius PDF Detection Report",
        "",
        f"PDF: {relative_pdf_path}",
        f"Total pages: {report['total_pages']}",
        f"Pages sampled: {report['pages_sampled']}",
        "",
        "PAGE DETAILS:",
    ]

    for item in report["page_details"]:
        text_lines.append(
            f"  Page {item['page_number']}: {item['extracted_characters']} extracted characters"
        )

    text_lines.extend(
        [
            "",
            f"Pages with usable text: {report['pages_with_usable_text']}/{report['pages_sampled']}",
            f"Total extracted characters: {report['total_extracted_characters']}",
            "",
            f"RESULT: {report['result']}",
            f"RECOMMENDED ROUTE: {report['recommended_route']}",
        ]
    )

    report_text = "\n".join(text_lines) + "\n"

    write_json(latest_json, report)
    write_json(timestamped_json, report)
    write_text(latest_txt, report_text)
    write_text(timestamped_txt, report_text)

    print(f"PDF: {relative_pdf_path}")
    print(f"Total pages: {report['total_pages']}")
    print(f"Pages sampled: {report['pages_sampled']}")
    print()

    for item in report["page_details"]:
        print(
            f"Page {item['page_number']}: {item['extracted_characters']} extracted characters"
        )

    print()
    print(f"Pages with usable text: {report['pages_with_usable_text']}/{report['pages_sampled']}")
    print(f"Total extracted characters in sample: {report['total_extracted_characters']}")
    print()
    print(f"RESULT: {report['result']}")
    print(f"RECOMMENDED ROUTE: {report['recommended_route']}")
    print(f"Latest detect JSON: {latest_json}")
    print(f"Latest detect TXT: {latest_txt}")

    return 0


def run_pipeline() -> int:
    scan_code = run_scan()
    if scan_code != 0:
        return scan_code

    status_code = run_status()
    if status_code != 0:
        return status_code

    return run_lint()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Vitruvius pipeline entrypoint")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("scan", help="Scan raw source layer and write tree snapshots")
    subparsers.add_parser("status", help="Compare the latest two registry scans")
    subparsers.add_parser("lint", help="Check raw layer for obvious structural issues")
    subparsers.add_parser("convert", help="Build a conversion queue from latest status")
    subparsers.add_parser("run", help="Run scan, status, and lint")

    detect_one_parser = subparsers.add_parser(
        "detect-one",
        help="Detect whether one PDF is text-based or likely scanned",
    )
    detect_one_parser.add_argument(
        "relative_pdf_path",
        help="Path relative to 001_Raw-Source-Layer",
    )
    detect_one_parser.add_argument(
        "--sample-pages",
        type=int,
        default=5,
        help="How many pages to sample",
    )

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "scan":
        return run_scan()

    if args.command == "status":
        return run_status()

    if args.command == "lint":
        return run_lint()

    if args.command == "convert":
        return run_convert()

    if args.command == "run":
        return run_pipeline()

    if args.command == "detect-one":
        return run_detect_one(
            relative_pdf_path=args.relative_pdf_path,
            sample_pages=args.sample_pages,
        )

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())