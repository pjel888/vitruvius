from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .constants import CONVERSION_LAYER_NAME
from .paths import build_conversion_relative_paths, ensure_runs_dir, get_repo_root
from .reports import write_json, write_text
from .utils import utc_now_stamp


def run_reconcile() -> int:
    repo_root = get_repo_root()
    runs_dir = ensure_runs_dir(repo_root)

    latest_status_json = runs_dir / "latest_status_report.json"
    if not latest_status_json.exists():
        print("No latest_status_report.json found.")
        print("Run pipeline_cli.py run first.")
        return 1

    status_report = json.loads(latest_status_json.read_text(encoding="utf-8"))
    missing_files = sorted(status_report.get("missing_files", []))

    missing_pdf_files = [p for p in missing_files if Path(p).suffix.lower() == ".pdf"]
    skipped_non_pdf = [p for p in missing_files if Path(p).suffix.lower() != ".pdf"]

    stale_converted_outputs: list[dict[str, Any]] = []
    missing_without_outputs: list[dict[str, Any]] = []

    for rel_path in missing_pdf_files:
        markdown_rel, json_rel = build_conversion_relative_paths(rel_path)

        markdown_abs = repo_root / CONVERSION_LAYER_NAME / markdown_rel
        json_abs = repo_root / CONVERSION_LAYER_NAME / json_rel

        markdown_exists = markdown_abs.exists()
        json_exists = json_abs.exists()

        item = {
            "source_relative_path": rel_path,
            "expected_markdown_output": markdown_rel.as_posix(),
            "expected_json_output": json_rel.as_posix(),
            "markdown_exists": markdown_exists,
            "json_exists": json_exists,
        }

        if markdown_exists or json_exists:
            item["status"] = "stale_outputs_detected"
            stale_converted_outputs.append(item)
        else:
            item["status"] = "no_derived_outputs_found"
            missing_without_outputs.append(item)

    report = {
        "project": "Vitruvius",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "status_source": str(latest_status_json),
        "summary": {
            "missing_file_count": len(missing_files),
            "missing_pdf_count": len(missing_pdf_files),
            "skipped_non_pdf_count": len(skipped_non_pdf),
            "stale_output_count": len(stale_converted_outputs),
            "missing_without_outputs_count": len(missing_without_outputs),
        },
        "stale_converted_outputs": stale_converted_outputs,
        "missing_without_outputs": missing_without_outputs,
        "skipped_non_pdf": skipped_non_pdf,
    }

    stamp = utc_now_stamp()
    latest_json = runs_dir / "latest_reconcile_report.json"
    timestamped_json = runs_dir / f"{stamp}_reconcile_report.json"

    latest_txt = runs_dir / "latest_reconcile_report.txt"
    timestamped_txt = runs_dir / f"{stamp}_reconcile_report.txt"

    text_lines = [
        "Vitruvius Reconcile Report",
        "",
        f"Missing files from status: {len(missing_files)}",
        f"Missing PDF files: {len(missing_pdf_files)}",
        f"Skipped non-PDF missing files: {len(skipped_non_pdf)}",
        f"Stale converted outputs detected: {len(stale_converted_outputs)}",
        f"Missing raw files with no derived outputs: {len(missing_without_outputs)}",
        "",
        "STALE CONVERTED OUTPUTS:",
    ]

    if stale_converted_outputs:
        for item in stale_converted_outputs:
            text_lines.append("  ---")
            text_lines.append(f"  source: {item['source_relative_path']}")
            text_lines.append(f"  markdown: {item['expected_markdown_output']} | exists={item['markdown_exists']}")
            text_lines.append(f"  json: {item['expected_json_output']} | exists={item['json_exists']}")
    else:
        text_lines.append("  None")

    text_lines.extend(["", "MISSING RAW FILES WITH NO DERIVED OUTPUTS:"])
    if missing_without_outputs:
        for item in missing_without_outputs:
            text_lines.append("  ---")
            text_lines.append(f"  source: {item['source_relative_path']}")
            text_lines.append(f"  markdown: {item['expected_markdown_output']} | exists={item['markdown_exists']}")
            text_lines.append(f"  json: {item['expected_json_output']} | exists={item['json_exists']}")
    else:
        text_lines.append("  None")

    text_lines.extend(["", "SKIPPED NON-PDF MISSING FILES:"])
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

    print("Reconcile complete.")
    print(f"Missing files: {len(missing_files)}")
    print(f"Missing PDF files: {len(missing_pdf_files)}")
    print(f"Stale converted outputs detected: {len(stale_converted_outputs)}")
    print(f"Missing raw files with no derived outputs: {len(missing_without_outputs)}")
    print(f"Skipped non-PDF missing files: {len(skipped_non_pdf)}")
    print(f"Latest reconcile JSON: {latest_json}")
    print(f"Latest reconcile TXT: {latest_txt}")

    return 0