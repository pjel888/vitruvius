from __future__ import annotations

import json
import shutil
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import opendataloader_pdf

from .constants import CONVERSION_LAYER_NAME, RAW_LAYER_NAME
from .detection import detect_pdf_type
from .paths import build_conversion_relative_paths, ensure_runs_dir, get_repo_root
from .reports import write_json, write_text
from .utils import safe_name_for_report, utc_now_stamp


def convert_text_pdf(
    relative_pdf_path: str,
    sample_pages: int = 5,
    detection_override: dict[str, Any] | None = None,
) -> dict[str, Any]:
    repo_root = get_repo_root()

    source_pdf = repo_root / RAW_LAYER_NAME / relative_pdf_path
    if not source_pdf.exists():
        raise FileNotFoundError(f"File not found: {source_pdf}")

    if source_pdf.suffix.lower() != ".pdf":
        raise ValueError("convert_text_pdf only accepts PDF files.")

    detection = detection_override or detect_pdf_type(source_pdf, sample_pages=sample_pages)
    if detection["result"] != "TEXT_PDF":
        raise ValueError(
            f"PDF is not text-based. Route required: {detection['recommended_route']}"
        )

    markdown_rel, json_rel = build_conversion_relative_paths(relative_pdf_path)
    markdown_abs = repo_root / CONVERSION_LAYER_NAME / markdown_rel
    json_abs = repo_root / CONVERSION_LAYER_NAME / json_rel

    markdown_abs.parent.mkdir(parents=True, exist_ok=True)
    json_abs.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        opendataloader_pdf.convert(
            input_path=[str(source_pdf)],
            output_dir=str(temp_path),
            format="markdown,json",
        )

        temp_markdown = temp_path / f"{source_pdf.stem}.md"
        temp_json = temp_path / f"{source_pdf.stem}.json"

        if not temp_markdown.exists():
            raise FileNotFoundError(f"Expected markdown output not found: {temp_markdown}")

        if not temp_json.exists():
            raise FileNotFoundError(f"Expected json output not found: {temp_json}")

        if markdown_abs.exists():
            markdown_abs.unlink()

        if json_abs.exists():
            json_abs.unlink()

        shutil.move(str(temp_markdown), str(markdown_abs))
        shutil.move(str(temp_json), str(json_abs))

    return {
        "source_relative_path": relative_pdf_path,
        "source_absolute_path": str(source_pdf),
        "detection_result": detection["result"],
        "recommended_route": detection["recommended_route"],
        "markdown_output": str(markdown_abs),
        "json_output": str(json_abs),
        "markdown_output_relative": markdown_rel.as_posix(),
        "json_output_relative": json_rel.as_posix(),
        "status": "converted",
    }


def run_convert_one(relative_pdf_path: str, sample_pages: int = 5) -> int:
    repo_root = get_repo_root()
    runs_dir = ensure_runs_dir(repo_root)
    source_pdf = repo_root / RAW_LAYER_NAME / relative_pdf_path

    if not source_pdf.exists():
        print(f"ERROR: File not found: {source_pdf}")
        return 1

    if source_pdf.suffix.lower() != ".pdf":
        print("ERROR: convert-one only accepts PDF files.")
        return 1

    try:
        detection = detect_pdf_type(source_pdf, sample_pages=sample_pages)
    except Exception as exc:
        print(f"ERROR: {exc}")
        return 1

    if detection["result"] != "TEXT_PDF":
        print(f"PDF: {relative_pdf_path}")
        print(f"RESULT: {detection['result']}")
        print(f"RECOMMENDED ROUTE: {detection['recommended_route']}")
        print("Conversion stopped.")
        print("This file should go through OCR first, then OpenDataLoader.")
        return 1

    try:
        report = convert_text_pdf(
            relative_pdf_path=relative_pdf_path,
            sample_pages=sample_pages,
            detection_override=detection,
        )
    except Exception as exc:
        print(f"ERROR: {exc}")
        return 1

    stamp = utc_now_stamp()
    safe_stem = safe_name_for_report(source_pdf.stem)

    latest_json = runs_dir / "latest_convert_one_report.json"
    timestamped_json = runs_dir / f"{stamp}_{safe_stem}_convert_one_report.json"

    latest_txt = runs_dir / "latest_convert_one_report.txt"
    timestamped_txt = runs_dir / f"{stamp}_{safe_stem}_convert_one_report.txt"

    report_payload = {
        "project": "Vitruvius",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        **report,
    }

    report_text = "\n".join(
        [
            "Vitruvius Convert One Report",
            "",
            f"Source: {relative_pdf_path}",
            f"Detection result: {report['detection_result']}",
            f"Recommended route: {report['recommended_route']}",
            f"Markdown output: {report['markdown_output']}",
            f"JSON output: {report['json_output']}",
            "",
            "STATUS: converted",
        ]
    ) + "\n"

    write_json(latest_json, report_payload)
    write_json(timestamped_json, report_payload)
    write_text(latest_txt, report_text)
    write_text(timestamped_txt, report_text)

    print("Convert-one complete.")
    print(f"Source PDF: {source_pdf}")
    print(f"Detection result: {report['detection_result']}")
    print(f"Markdown output: {report['markdown_output']}")
    print(f"JSON output: {report['json_output']}")
    print(f"Latest convert-one JSON: {latest_json}")
    print(f"Latest convert-one TXT: {latest_txt}")

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

    queue_items: list[dict[str, Any]] = []
    converted_items: list[dict[str, Any]] = []
    ocr_needed_items: list[dict[str, Any]] = []
    failed_items: list[dict[str, Any]] = []

    for rel_path in pdf_candidates:
        source_pdf = repo_root / RAW_LAYER_NAME / rel_path
        markdown_rel, json_rel = build_conversion_relative_paths(rel_path)

        try:
            detection = detect_pdf_type(source_pdf)
        except Exception as exc:
            failed_items.append(
                {
                    "source_relative_path": rel_path,
                    "status": "failed_detection",
                    "error": str(exc),
                }
            )
            continue

        queue_items.append(
            {
                "source_relative_path": rel_path,
                "planned_markdown_output": markdown_rel.as_posix(),
                "planned_sidecar_output": json_rel.as_posix(),
                "detection_result": detection["result"],
                "recommended_route": detection["recommended_route"],
            }
        )

        if detection["result"] == "TEXT_PDF":
            try:
                converted = convert_text_pdf(
                    relative_pdf_path=rel_path,
                    detection_override=detection,
                )
                converted_items.append(converted)
            except Exception as exc:
                failed_items.append(
                    {
                        "source_relative_path": rel_path,
                        "status": "failed_conversion",
                        "error": str(exc),
                    }
                )
        else:
            ocr_needed_items.append(
                {
                    "source_relative_path": rel_path,
                    "planned_markdown_output": markdown_rel.as_posix(),
                    "planned_sidecar_output": json_rel.as_posix(),
                    "detection_result": detection["result"],
                    "recommended_route": detection["recommended_route"],
                    "status": "ocr_required",
                }
            )

    queue_report = {
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

    batch_report = {
        "project": "Vitruvius",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "status_source": str(latest_status_json),
        "summary": {
            "candidate_count": len(candidates),
            "pdf_candidate_count": len(pdf_candidates),
            "converted_count": len(converted_items),
            "ocr_required_count": len(ocr_needed_items),
            "failed_count": len(failed_items),
            "skipped_non_pdf_count": len(skipped_non_pdf),
        },
        "converted_items": converted_items,
        "ocr_required_items": ocr_needed_items,
        "failed_items": failed_items,
        "skipped_non_pdf": skipped_non_pdf,
    }

    ocr_report = {
        "project": "Vitruvius",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "summary": {
            "ocr_required_count": len(ocr_needed_items),
        },
        "ocr_required_items": ocr_needed_items,
    }

    stamp = utc_now_stamp()

    latest_queue_json = runs_dir / "latest_convert_queue.json"
    timestamped_queue_json = runs_dir / f"{stamp}_convert_queue.json"
    latest_queue_txt = runs_dir / "latest_convert_queue.txt"
    timestamped_queue_txt = runs_dir / f"{stamp}_convert_queue.txt"

    latest_batch_json = runs_dir / "latest_convert_batch_report.json"
    timestamped_batch_json = runs_dir / f"{stamp}_convert_batch_report.json"
    latest_batch_txt = runs_dir / "latest_convert_batch_report.txt"
    timestamped_batch_txt = runs_dir / f"{stamp}_convert_batch_report.txt"

    latest_ocr_json = runs_dir / "latest_ocr_needed_report.json"
    timestamped_ocr_json = runs_dir / f"{stamp}_ocr_needed_report.json"
    latest_ocr_txt = runs_dir / "latest_ocr_needed_report.txt"
    timestamped_ocr_txt = runs_dir / f"{stamp}_ocr_needed_report.txt"

    queue_text_lines = [
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
            queue_text_lines.append("  ---")
            queue_text_lines.append(f"  source: {item['source_relative_path']}")
            queue_text_lines.append(f"  markdown: {item['planned_markdown_output']}")
            queue_text_lines.append(f"  sidecar: {item['planned_sidecar_output']}")
            queue_text_lines.append(f"  detection: {item['detection_result']}")
            queue_text_lines.append(f"  route: {item['recommended_route']}")
    else:
        queue_text_lines.append("  None")

    queue_text_lines.extend(["", "SKIPPED NON-PDF:"])
    if skipped_non_pdf:
        for item in skipped_non_pdf:
            queue_text_lines.append(f"  {item}")
    else:
        queue_text_lines.append("  None")

    queue_text = "\n".join(queue_text_lines) + "\n"

    batch_text_lines = [
        "Vitruvius Convert Batch Report",
        "",
        f"Candidate files: {len(candidates)}",
        f"PDF candidates: {len(pdf_candidates)}",
        f"Converted: {len(converted_items)}",
        f"OCR required: {len(ocr_needed_items)}",
        f"Failed: {len(failed_items)}",
        f"Skipped non-PDF: {len(skipped_non_pdf)}",
        "",
        "CONVERTED ITEMS:",
    ]

    if converted_items:
        for item in converted_items:
            batch_text_lines.append("  ---")
            batch_text_lines.append(f"  source: {item['source_relative_path']}")
            batch_text_lines.append(f"  markdown: {item['markdown_output_relative']}")
            batch_text_lines.append(f"  sidecar: {item['json_output_relative']}")
    else:
        batch_text_lines.append("  None")

    batch_text_lines.extend(["", "OCR REQUIRED ITEMS:"])
    if ocr_needed_items:
        for item in ocr_needed_items:
            batch_text_lines.append("  ---")
            batch_text_lines.append(f"  source: {item['source_relative_path']}")
            batch_text_lines.append(f"  route: {item['recommended_route']}")
    else:
        batch_text_lines.append("  None")

    batch_text_lines.extend(["", "FAILED ITEMS:"])
    if failed_items:
        for item in failed_items:
            batch_text_lines.append("  ---")
            batch_text_lines.append(f"  source: {item['source_relative_path']}")
            batch_text_lines.append(f"  status: {item['status']}")
            batch_text_lines.append(f"  error: {item['error']}")
    else:
        batch_text_lines.append("  None")

    batch_text = "\n".join(batch_text_lines) + "\n"

    ocr_text_lines = [
        "Vitruvius OCR Needed Report",
        "",
        f"OCR required files: {len(ocr_needed_items)}",
        "",
        "OCR REQUIRED ITEMS:",
    ]

    if ocr_needed_items:
        for item in ocr_needed_items:
            ocr_text_lines.append("  ---")
            ocr_text_lines.append(f"  source: {item['source_relative_path']}")
            ocr_text_lines.append(f"  route: {item['recommended_route']}")
    else:
        ocr_text_lines.append("  None")

    ocr_text = "\n".join(ocr_text_lines) + "\n"

    write_json(latest_queue_json, queue_report)
    write_json(timestamped_queue_json, queue_report)
    write_text(latest_queue_txt, queue_text)
    write_text(timestamped_queue_txt, queue_text)

    write_json(latest_batch_json, batch_report)
    write_json(timestamped_batch_json, batch_report)
    write_text(latest_batch_txt, batch_text)
    write_text(timestamped_batch_txt, batch_text)

    write_json(latest_ocr_json, ocr_report)
    write_json(timestamped_ocr_json, ocr_report)
    write_text(latest_ocr_txt, ocr_text)
    write_text(timestamped_ocr_txt, ocr_text)

    print("Batch convert complete.")
    print(f"Candidate files: {len(candidates)}")
    print(f"PDF candidates: {len(pdf_candidates)}")
    print(f"Converted: {len(converted_items)}")
    print(f"OCR required: {len(ocr_needed_items)}")
    print(f"Failed: {len(failed_items)}")
    print(f"Skipped non-PDF files: {len(skipped_non_pdf)}")
    print(f"Latest queue JSON: {latest_queue_json}")
    print(f"Latest batch JSON: {latest_batch_json}")
    print(f"Latest OCR-needed JSON: {latest_ocr_json}")

    return 0