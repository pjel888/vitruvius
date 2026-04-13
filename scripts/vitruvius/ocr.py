from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import ocrmypdf

from .constants import CONVERSION_LAYER_NAME, RAW_LAYER_NAME
from .conversion import _write_conversion_registry_entry, convert_pdf_at_path
from .paths import build_ocr_pdf_relative_path, ensure_registry_dir, ensure_runs_dir, get_repo_root
from .reports import ensure_conversion_registry_exists, snapshot_conversion_registry, write_json, write_text
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


def run_ocr_execute(languages: list[str] | None = None, deskew: bool = True) -> int:
    repo_root = get_repo_root()
    registry_dir = ensure_registry_dir(repo_root)
    runs_dir = ensure_runs_dir(repo_root)
    ensure_conversion_registry_exists(registry_dir)

    latest_queue_json = runs_dir / "latest_ocr_queue_report.json"
    if not latest_queue_json.exists():
        print("No latest_ocr_queue_report.json found.")
        print("Run pipeline_cli.py ocr-queue first.")
        return 1

    queue_report = json.loads(latest_queue_json.read_text(encoding="utf-8"))
    queue_items = queue_report.get("ocr_queue_items", [])

    completed_ocr: list[dict[str, Any]] = []
    completed_conversion: list[dict[str, Any]] = []
    failed_items: list[dict[str, Any]] = []

    selected_languages = languages or ["eng"]

    for item in queue_items:
        rel_path = item["source_relative_path"]
        source_pdf = repo_root / RAW_LAYER_NAME / rel_path

        try:
            ocr_rel = build_ocr_pdf_relative_path(rel_path)
            ocr_abs = repo_root / CONVERSION_LAYER_NAME / ocr_rel
            ocr_abs.parent.mkdir(parents=True, exist_ok=True)

            if ocr_abs.exists():
                ocr_abs.unlink()

            ocrmypdf.ocr(
                str(source_pdf),
                str(ocr_abs),
                languages=selected_languages,
                deskew=deskew,
                skip_text=True,
                progress_bar=False,
            )

            completed_ocr.append(
                {
                    "source_relative_path": rel_path,
                    "ocr_pdf_output": str(ocr_abs),
                    "ocr_pdf_output_relative": ocr_rel.as_posix(),
                    "status": "ocr_completed",
                }
            )

            converted = convert_pdf_at_path(
                ocr_abs,
                rel_path,
                run_command="ocr-execute",
                detected_pdf_type="OCR_OUTPUT_PDF",
                processing_route="OCR_THEN_OPENDATALOADER",
                output_ocr_pdf_relative_path=f"{CONVERSION_LAYER_NAME}/{ocr_rel.as_posix()}",
            )

            completed_conversion.append(
                {
                    "source_relative_path": rel_path,
                    "ocr_pdf_output_relative": ocr_rel.as_posix(),
                    "markdown_output_relative": converted["markdown_output_relative"],
                    "json_output_relative": converted["json_output_relative"],
                    "status": "ocr_and_conversion_completed",
                }
            )

        except Exception as exc:
            failed_items.append(
                {
                    "source_relative_path": rel_path,
                    "status": "ocr_failed",
                    "error": str(exc),
                }
            )

            if source_pdf.exists():
                stat = source_pdf.stat()
                source_size_bytes = stat.st_size
                source_modified_utc = datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).isoformat()
                source_extension = source_pdf.suffix.lower()
            else:
                source_size_bytes = ""
                source_modified_utc = ""
                source_extension = Path(rel_path).suffix.lower()

            logical_parts = Path(rel_path).parts
            top_category = logical_parts[0] if logical_parts else ""

            _write_conversion_registry_entry(
                run_command="ocr-execute",
                source_relative_path=f"{RAW_LAYER_NAME}/{rel_path}",
                logical_source_relative_path=rel_path,
                source_extension=source_extension,
                source_size_bytes=source_size_bytes,
                source_modified_utc=source_modified_utc,
                top_category=top_category,
                detected_pdf_type="LIKELY_SCANNED_PDF",
                processing_route="OCR_THEN_OPENDATALOADER",
                status="FAILED",
                output_markdown_relative_path="",
                output_json_relative_path="",
                output_ocr_pdf_relative_path="",
                error_message=str(exc),
            )

    report = {
        "project": "Vitruvius",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "languages": selected_languages,
        "deskew": deskew,
        "summary": {
            "queue_count": len(queue_items),
            "ocr_completed_count": len(completed_ocr),
            "conversion_completed_count": len(completed_conversion),
            "failed_count": len(failed_items),
        },
        "ocr_completed_items": completed_ocr,
        "conversion_completed_items": completed_conversion,
        "failed_items": failed_items,
    }

    stamp = utc_now_stamp()
    latest_json = runs_dir / "latest_ocr_execute_report.json"
    timestamped_json = runs_dir / f"{stamp}_ocr_execute_report.json"

    latest_txt = runs_dir / "latest_ocr_execute_report.txt"
    timestamped_txt = runs_dir / f"{stamp}_ocr_execute_report.txt"

    text_lines = [
        "Vitruvius OCR Execute Report",
        "",
        f"Queue count: {len(queue_items)}",
        f"OCR completed: {len(completed_ocr)}",
        f"Conversion completed: {len(completed_conversion)}",
        f"Failed: {len(failed_items)}",
        f"Languages: {', '.join(selected_languages)}",
        f"Deskew: {deskew}",
        "",
        "OCR COMPLETED ITEMS:",
    ]

    if completed_ocr:
        for item in completed_ocr:
            text_lines.append("  ---")
            text_lines.append(f"  source: {item['source_relative_path']}")
            text_lines.append(f"  ocr_pdf: {item['ocr_pdf_output_relative']}")
    else:
        text_lines.append("  None")

    text_lines.extend(["", "CONVERSION COMPLETED ITEMS:"])
    if completed_conversion:
        for item in completed_conversion:
            text_lines.append("  ---")
            text_lines.append(f"  source: {item['source_relative_path']}")
            text_lines.append(f"  ocr_pdf: {item['ocr_pdf_output_relative']}")
            text_lines.append(f"  markdown: {item['markdown_output_relative']}")
            text_lines.append(f"  sidecar: {item['json_output_relative']}")
    else:
        text_lines.append("  None")

    text_lines.extend(["", "FAILED ITEMS:"])
    if failed_items:
        for item in failed_items:
            text_lines.append("  ---")
            text_lines.append(f"  source: {item['source_relative_path']}")
            text_lines.append(f"  status: {item['status']}")
            text_lines.append(f"  error: {item['error']}")
    else:
        text_lines.append("  None")

    report_text = "\n".join(text_lines) + "\n"

    write_json(latest_json, report)
    write_json(timestamped_json, report)
    write_text(latest_txt, report_text)
    write_text(timestamped_txt, report_text)

    snapshot_conversion_registry(registry_dir, stamp)

    print("OCR execute complete.")
    print(f"Queue count: {len(queue_items)}")
    print(f"OCR completed: {len(completed_ocr)}")
    print(f"Conversion completed: {len(completed_conversion)}")
    print(f"Failed: {len(failed_items)}")
    print(f"Latest OCR execute JSON: {latest_json}")
    print(f"Latest OCR execute TXT: {latest_txt}")

    return 0