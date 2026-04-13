from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .constants import CONVERSION_LAYER_NAME
from .office import is_supported_office_file
from .paths import (
    build_conversion_relative_paths,
    build_ocr_pdf_relative_path,
    build_office_pdf_relative_path,
    ensure_runs_dir,
    get_repo_root,
)
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
    missing_office_files = [p for p in missing_files if is_supported_office_file(p)]
    skipped_non_supported = [
        p for p in missing_files
        if Path(p).suffix.lower() != ".pdf" and not is_supported_office_file(p)
    ]

    stale_derived_outputs: list[dict[str, Any]] = []
    missing_without_outputs: list[dict[str, Any]] = []

    supported_missing_files = sorted(missing_pdf_files + missing_office_files)

    for rel_path in supported_missing_files:
        markdown_rel, json_rel = build_conversion_relative_paths(rel_path)

        markdown_abs = repo_root / CONVERSION_LAYER_NAME / markdown_rel
        json_abs = repo_root / CONVERSION_LAYER_NAME / json_rel

        markdown_exists = markdown_abs.exists()
        json_exists = json_abs.exists()

        ocr_rel = None
        ocr_abs = None
        ocr_exists = False

        office_pdf_rel = None
        office_pdf_abs = None
        office_pdf_exists = False

        suffix = Path(rel_path).suffix.lower()

        if suffix == ".pdf":
            ocr_rel = build_ocr_pdf_relative_path(rel_path)
            ocr_abs = repo_root / CONVERSION_LAYER_NAME / ocr_rel
            ocr_exists = ocr_abs.exists()

        if is_supported_office_file(rel_path):
            office_pdf_rel = build_office_pdf_relative_path(rel_path)
            office_pdf_abs = repo_root / CONVERSION_LAYER_NAME / office_pdf_rel
            office_pdf_exists = office_pdf_abs.exists()

        item = {
            "source_relative_path": rel_path,
            "source_type": "pdf" if suffix == ".pdf" else "office",
            "expected_markdown_output": markdown_rel.as_posix(),
            "expected_json_output": json_rel.as_posix(),
            "markdown_exists": markdown_exists,
            "json_exists": json_exists,
            "expected_ocr_pdf_output": ocr_rel.as_posix() if ocr_rel else "",
            "ocr_pdf_exists": ocr_exists,
            "expected_office_pdf_output": office_pdf_rel.as_posix() if office_pdf_rel else "",
            "office_pdf_exists": office_pdf_exists,
        }

        if markdown_exists or json_exists or ocr_exists or office_pdf_exists:
            item["status"] = "stale_outputs_detected"
            stale_derived_outputs.append(item)
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
            "missing_office_count": len(missing_office_files),
            "skipped_non_supported_count": len(skipped_non_supported),
            "stale_output_count": len(stale_derived_outputs),
            "missing_without_outputs_count": len(missing_without_outputs),
        },
        "stale_derived_outputs": stale_derived_outputs,
        "missing_without_outputs": missing_without_outputs,
        "skipped_non_supported": skipped_non_supported,
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
        f"Missing Office files: {len(missing_office_files)}",
        f"Skipped non-supported missing files: {len(skipped_non_supported)}",
        f"Stale derived outputs detected: {len(stale_derived_outputs)}",
        f"Missing raw files with no derived outputs: {len(missing_without_outputs)}",
        "",
        "STALE DERIVED OUTPUTS:",
    ]

    if stale_derived_outputs:
        for item in stale_derived_outputs:
            text_lines.append("  ---")
            text_lines.append(f"  source: {item['source_relative_path']}")
            text_lines.append(f"  source_type: {item['source_type']}")
            text_lines.append(
                f"  markdown: {item['expected_markdown_output']} | exists={item['markdown_exists']}"
            )
            text_lines.append(
                f"  json: {item['expected_json_output']} | exists={item['json_exists']}"
            )
            if item["expected_ocr_pdf_output"]:
                text_lines.append(
                    f"  ocr_pdf: {item['expected_ocr_pdf_output']} | exists={item['ocr_pdf_exists']}"
                )
            if item["expected_office_pdf_output"]:
                text_lines.append(
                    f"  office_pdf: {item['expected_office_pdf_output']} | exists={item['office_pdf_exists']}"
                )
    else:
        text_lines.append("  None")

    text_lines.extend(["", "MISSING RAW FILES WITH NO DERIVED OUTPUTS:"])
    if missing_without_outputs:
        for item in missing_without_outputs:
            text_lines.append("  ---")
            text_lines.append(f"  source: {item['source_relative_path']}")
            text_lines.append(f"  source_type: {item['source_type']}")
            text_lines.append(
                f"  markdown: {item['expected_markdown_output']} | exists={item['markdown_exists']}"
            )
            text_lines.append(
                f"  json: {item['expected_json_output']} | exists={item['json_exists']}"
            )
            if item["expected_ocr_pdf_output"]:
                text_lines.append(
                    f"  ocr_pdf: {item['expected_ocr_pdf_output']} | exists={item['ocr_pdf_exists']}"
                )
            if item["expected_office_pdf_output"]:
                text_lines.append(
                    f"  office_pdf: {item['expected_office_pdf_output']} | exists={item['office_pdf_exists']}"
                )
    else:
        text_lines.append("  None")

    text_lines.extend(["", "SKIPPED NON-SUPPORTED MISSING FILES:"])
    if skipped_non_supported:
        for item in skipped_non_supported:
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
    print(f"Missing Office files: {len(missing_office_files)}")
    print(f"Stale derived outputs detected: {len(stale_derived_outputs)}")
    print(f"Missing raw files with no derived outputs: {len(missing_without_outputs)}")
    print(f"Skipped non-supported missing files: {len(skipped_non_supported)}")
    print(f"Latest reconcile JSON: {latest_json}")
    print(f"Latest reconcile TXT: {latest_txt}")

    return 0