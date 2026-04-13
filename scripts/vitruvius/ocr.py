from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from .constants import RAW_LAYER_NAME
from .paths import ensure_runs_dir, get_repo_root
from .reports import write_json, write_text
from .utils import utc_now_stamp


def run_ocr_queue() -> int:
    repo_root = get_repo_root()
    runs_dir = ensure_runs_dir(repo_root)

    latest_ocr_json = runs_dir / "latest_ocr_needed_report.json"
    if not latest_ocr_json.exists():
        print("No latest_ocr_needed_report.json found.")
        print("Run pipeline_cli.py convert first.")
        return 1

    ocr_report = json.loads(latest_ocr_json.read_text(encoding="utf-8"))
    ocr_items = ocr_report.get("ocr_required_items", [])

    queue_items = []
    for item in ocr_items:
        rel_path = item["source_relative_path"]
        raw_pdf = repo_root / RAW_LAYER_NAME / rel_path

        queue_items.append(
            {
                "source_relative_path": rel_path,
                "source_absolute_path": str(raw_pdf),
                "status": "pending_ocr",
            }
        )

    report = {
        "project": "Vitruvius",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "ocr_candidate_count": len(queue_items),
        "ocr_queue_items": queue_items,
    }

    stamp = utc_now_stamp()
    latest_json = runs_dir / "latest_ocr_queue_report.json"
    timestamped_json = runs_dir / f"{stamp}_ocr_queue_report.json"

    latest_txt = runs_dir / "latest_ocr_queue_report.txt"
    timestamped_txt = runs_dir / f"{stamp}_ocr_queue_report.txt"

    text_lines = [
        "Vitruvius OCR Queue Report",
        "",
        f"OCR candidate files: {len(queue_items)}",
        "",
        "OCR QUEUE ITEMS:",
    ]

    if queue_items:
        for item in queue_items:
            text_lines.append("  ---")
            text_lines.append(f"  source: {item['source_relative_path']}")
            text_lines.append(f"  status: {item['status']}")
    else:
        text_lines.append("  None")

    report_text = "\n".join(text_lines) + "\n"

    write_json(latest_json, report)
    write_json(timestamped_json, report)
    write_text(latest_txt, report_text)
    write_text(timestamped_txt, report_text)

    print("OCR queue report complete.")
    print(f"OCR candidate files: {len(queue_items)}")
    print(f"Latest OCR queue JSON: {latest_json}")
    print(f"Latest OCR queue TXT: {latest_txt}")

    return 0