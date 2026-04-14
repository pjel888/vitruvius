from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone

from pathlib import Path

from .paths import ensure_registry_dir, ensure_runs_dir, get_repo_root
from .reports import read_csv_entries, write_json, write_text
from .utils import utc_now_stamp


@dataclass(frozen=True)
class LintIssue:
    """Stream W3.2 — structured lint finding emitted by concept file checks."""
    code: str
    path: str
    message: str


_ALLOWED_STRINGENCY = {"maximize", "minimize", "qualitative"}


def _load_frontmatter(path: Path) -> dict | None:
    import yaml
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    try:
        fm = yaml.safe_load(text[3:end].strip())
    except yaml.YAMLError:
        return None
    return fm if isinstance(fm, dict) else None


def lint_concept_file(path: Path) -> list[LintIssue]:
    """Stream W3.2 — check a single concept file for stringency_vector.

    Emits:
      - ``missing_frontmatter`` when the file has no parseable frontmatter
      - ``missing_stringency_vector`` when the field is absent
      - ``invalid_stringency_vector`` when the value is not in
        {"maximize", "minimize", "qualitative"}
    """
    fm = _load_frontmatter(path)
    if fm is None:
        return [LintIssue(
            code="missing_frontmatter",
            path=str(path),
            message="no parseable frontmatter",
        )]
    issues: list[LintIssue] = []
    vector = fm.get("stringency_vector")
    if vector is None:
        issues.append(LintIssue(
            code="missing_stringency_vector",
            path=str(path),
            message=(
                f"concept {fm.get('id')!r} missing stringency_vector "
                "(allowed: maximize, minimize, qualitative)"
            ),
        ))
    elif vector not in _ALLOWED_STRINGENCY:
        issues.append(LintIssue(
            code="invalid_stringency_vector",
            path=str(path),
            message=(
                f"concept {fm.get('id')!r} has invalid "
                f"stringency_vector={vector!r}"
            ),
        ))
    return issues


def _filename_dedup_key(name: str) -> str:
    """Build a duplicate-detection key for filenames.

    Lowercases the stem, strips non-alphanumerics, preserves the lowercased
    suffix. Replaces the legacy utils.normalize_filename() call which emits
    a DeprecationWarning. The behavior is identical to the legacy function.
    """
    path = Path(name)
    stem = "".join(ch.lower() for ch in path.stem if ch.isalnum())
    ext = path.suffix.lower()
    return f"{stem}{ext}"


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

        duplicate_name_groups[_filename_dedup_key(name)].append(rel_path)

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