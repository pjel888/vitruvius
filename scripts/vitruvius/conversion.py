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
from .office import convert_office_to_pdf, is_supported_office_file
from .paths import build_conversion_relative_paths, ensure_registry_dir, ensure_runs_dir, get_repo_root
from .reports import (
    append_conversion_registry_row,
    ensure_conversion_registry_exists,
    snapshot_conversion_registry,
    write_json,
    write_text,
)
from .utils import safe_name_for_report, utc_now_stamp


SUPPORTED_DIRECT_INPUT_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".pptx",
    ".doc",
    ".ppt",
}


def _build_registry_row(
    *,
    run_command: str,
    source_relative_path: str,
    logical_source_relative_path: str,
    source_extension: str,
    source_size_bytes: int | str,
    source_modified_utc: str,
    top_category: str,
    detected_pdf_type: str,
    processing_route: str,
    status: str,
    output_markdown_relative_path: str = "",
    output_json_relative_path: str = "",
    output_ocr_pdf_relative_path: str = "",
    error_message: str = "",
) -> dict[str, Any]:
    return {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "run_command": run_command,
        "source_relative_path": source_relative_path,
        "logical_source_relative_path": logical_source_relative_path,
        "source_extension": source_extension,
        "source_size_bytes": source_size_bytes,
        "source_modified_utc": source_modified_utc,
        "top_category": top_category,
        "detected_pdf_type": detected_pdf_type,
        "processing_route": processing_route,
        "status": status,
        "output_markdown_relative_path": output_markdown_relative_path,
        "output_json_relative_path": output_json_relative_path,
        "output_ocr_pdf_relative_path": output_ocr_pdf_relative_path,
        "error_message": error_message,
    }


def _write_conversion_registry_entry(
    *,
    run_command: str,
    source_relative_path: str,
    logical_source_relative_path: str,
    source_extension: str,
    source_size_bytes: int | str,
    source_modified_utc: str,
    top_category: str,
    detected_pdf_type: str,
    processing_route: str,
    status: str,
    output_markdown_relative_path: str = "",
    output_json_relative_path: str = "",
    output_ocr_pdf_relative_path: str = "",
    error_message: str = "",
) -> None:
    repo_root = get_repo_root()
    registry_dir = ensure_registry_dir(repo_root)

    ensure_conversion_registry_exists(registry_dir)

    row = _build_registry_row(
        run_command=run_command,
        source_relative_path=source_relative_path,
        logical_source_relative_path=logical_source_relative_path,
        source_extension=source_extension,
        source_size_bytes=source_size_bytes,
        source_modified_utc=source_modified_utc,
        top_category=top_category,
        detected_pdf_type=detected_pdf_type,
        processing_route=processing_route,
        status=status,
        output_markdown_relative_path=output_markdown_relative_path,
        output_json_relative_path=output_json_relative_path,
        output_ocr_pdf_relative_path=output_ocr_pdf_relative_path,
        error_message=error_message,
    )

    append_conversion_registry_row(registry_dir, row)


def _repo_relative_string(path: Path, repo_root: Path) -> str:
    if path.is_absolute():
        try:
            return path.relative_to(repo_root).as_posix()
        except ValueError:
            return str(path)
    return path.as_posix()


def _raw_layer_relative_string(relative_source_path: str) -> str:
    return f"{RAW_LAYER_NAME}/{Path(relative_source_path).as_posix()}"


def _conversion_layer_relative_string(relative_output_path: Path) -> str:
    return f"{CONVERSION_LAYER_NAME}/{relative_output_path.as_posix()}"


def _source_metadata_from_raw(relative_source_path: str) -> dict[str, Any]:
    repo_root = get_repo_root()
    source_path = repo_root / RAW_LAYER_NAME / relative_source_path

    if not source_path.exists():
        raise FileNotFoundError(f"Source file not found: {source_path}")

    stat = source_path.stat()
    parts = Path(relative_source_path).parts
    top_category = parts[0] if parts else ""

    return {
        "source_path": source_path,
        "source_relative_path": _raw_layer_relative_string(relative_source_path),
        "logical_source_relative_path": Path(relative_source_path).as_posix(),
        "source_extension": source_path.suffix.lower(),
        "source_size_bytes": stat.st_size,
        "source_modified_utc": datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).isoformat(),
        "top_category": top_category,
    }


def convert_pdf_at_path(
    pdf_path: Path,
    logical_relative_source_path: str,
    *,
    run_command: str = "convert",
    registry_source_relative_path: str = "",
    registry_source_extension: str = ".pdf",
    registry_source_size_bytes: int | str = "",
    registry_source_modified_utc: str = "",
    registry_top_category: str = "",
    detected_pdf_type: str = "TEXT_PDF",
    processing_route: str = "OPENDATALOADER_DIRECT",
    output_ocr_pdf_relative_path: str = "",
) -> dict[str, Any]:
    repo_root = get_repo_root()

    if not pdf_path.exists():
        raise FileNotFoundError(f"File not found: {pdf_path}")

    if pdf_path.suffix.lower() != ".pdf":
        raise ValueError("convert_pdf_at_path only accepts PDF files.")

    markdown_rel, json_rel = build_conversion_relative_paths(logical_relative_source_path)
    markdown_abs = repo_root / CONVERSION_LAYER_NAME / markdown_rel
    json_abs = repo_root / CONVERSION_LAYER_NAME / json_rel

    markdown_abs.parent.mkdir(parents=True, exist_ok=True)
    json_abs.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        opendataloader_pdf.convert(
            input_path=[str(pdf_path)],
            output_dir=str(temp_path),
            format="markdown,json",
        )

        temp_markdown = temp_path / f"{pdf_path.stem}.md"
        temp_json = temp_path / f"{pdf_path.stem}.json"

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

    _write_conversion_registry_entry(
        run_command=run_command,
        source_relative_path=registry_source_relative_path or _repo_relative_string(pdf_path, repo_root),
        logical_source_relative_path=logical_relative_source_path,
        source_extension=registry_source_extension,
        source_size_bytes=registry_source_size_bytes,
        source_modified_utc=registry_source_modified_utc,
        top_category=registry_top_category,
        detected_pdf_type=detected_pdf_type,
        processing_route=processing_route,
        status="SUCCESS",
        output_markdown_relative_path=_conversion_layer_relative_string(markdown_rel),
        output_json_relative_path=_conversion_layer_relative_string(json_rel),
        output_ocr_pdf_relative_path=output_ocr_pdf_relative_path,
        error_message="",
    )

    return {
        "logical_source_relative_path": logical_relative_source_path,
        "source_pdf_path": str(pdf_path),
        "markdown_output": str(markdown_abs),
        "json_output": str(json_abs),
        "markdown_output_relative": markdown_rel.as_posix(),
        "json_output_relative": json_rel.as_posix(),
        "status": "converted",
    }


def convert_text_pdf(
    relative_pdf_path: str,
    sample_pages: int = 5,
    detection_override: dict[str, Any] | None = None,
    run_command: str = "convert",
) -> dict[str, Any]:
    metadata = _source_metadata_from_raw(relative_pdf_path)
    source_pdf = metadata["source_path"]

    if source_pdf.suffix.lower() != ".pdf":
        raise ValueError("convert_text_pdf only accepts PDF files.")

    detection = detection_override or detect_pdf_type(source_pdf, sample_pages=sample_pages)
    if detection["result"] != "TEXT_PDF":
        raise ValueError(
            f"PDF is not text-based. Route required: {detection['recommended_route']}"
        )

    converted = convert_pdf_at_path(
        source_pdf,
        relative_pdf_path,
        run_command=run_command,
        registry_source_relative_path=metadata["source_relative_path"],
        registry_source_extension=metadata["source_extension"],
        registry_source_size_bytes=metadata["source_size_bytes"],
        registry_source_modified_utc=metadata["source_modified_utc"],
        registry_top_category=metadata["top_category"],
        detected_pdf_type=detection["result"],
        processing_route="OPENDATALOADER_DIRECT",
        output_ocr_pdf_relative_path="",
    )

    return {
        "source_relative_path": relative_pdf_path,
        "source_absolute_path": str(source_pdf),
        "detection_result": detection["result"],
        "recommended_route": detection["recommended_route"],
        "markdown_output": converted["markdown_output"],
        "json_output": converted["json_output"],
        "markdown_output_relative": converted["markdown_output_relative"],
        "json_output_relative": converted["json_output_relative"],
        "status": "converted",
    }


def convert_office_source(
    relative_source_path: str,
    *,
    run_command: str = "convert",
) -> dict[str, Any]:
    office_result = convert_office_to_pdf(relative_source_path)
    office_pdf_path = Path(office_result["office_pdf_output"])

    detection = detect_pdf_type(office_pdf_path)
    if detection["result"] != "TEXT_PDF":
        raise ValueError(
            "Office-derived PDF did not produce a text-based PDF. "
            f"Detected route required: {detection['recommended_route']}"
        )

    converted = convert_pdf_at_path(
        office_pdf_path,
        relative_source_path,
        run_command=run_command,
        registry_source_relative_path=_raw_layer_relative_string(relative_source_path),
        registry_source_extension=office_result["source_extension"],
        registry_source_size_bytes=office_result["source_size_bytes"],
        registry_source_modified_utc=office_result["source_modified_utc"],
        registry_top_category=office_result["top_category"],
        detected_pdf_type=detection["result"],
        processing_route="OFFICE_TO_PDF_THEN_OPENDATALOADER",
        output_ocr_pdf_relative_path="",
    )

    return {
        "source_relative_path": relative_source_path,
        "source_absolute_path": office_result["source_absolute_path"],
        "detection_result": detection["result"],
        "recommended_route": detection["recommended_route"],
        "office_pdf_output": office_result["office_pdf_output"],
        "office_pdf_output_relative": office_result["office_pdf_output_relative"],
        "markdown_output": converted["markdown_output"],
        "json_output": converted["json_output"],
        "markdown_output_relative": converted["markdown_output_relative"],
        "json_output_relative": converted["json_output_relative"],
        "status": "converted",
    }


def run_convert_one(relative_pdf_path: str, sample_pages: int = 5) -> int:
    repo_root = get_repo_root()
    registry_dir = ensure_registry_dir(repo_root)
    runs_dir = ensure_runs_dir(repo_root)
    ensure_conversion_registry_exists(registry_dir)

    source_path = repo_root / RAW_LAYER_NAME / relative_pdf_path
    source_ext = source_path.suffix.lower()

    if not source_path.exists():
        print(f"ERROR: File not found: {source_path}")
        return 1

    if source_ext not in SUPPORTED_DIRECT_INPUT_EXTENSIONS:
        print("ERROR: convert-one only accepts .pdf, .docx, or .pptx files.")
        return 1

    if source_ext == ".pdf":
        try:
            detection = detect_pdf_type(source_path, sample_pages=sample_pages)
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
                run_command="convert-one",
            )
        except Exception as exc:
            metadata = _source_metadata_from_raw(relative_pdf_path)
            _write_conversion_registry_entry(
                run_command="convert-one",
                source_relative_path=metadata["source_relative_path"],
                logical_source_relative_path=metadata["logical_source_relative_path"],
                source_extension=metadata["source_extension"],
                source_size_bytes=metadata["source_size_bytes"],
                source_modified_utc=metadata["source_modified_utc"],
                top_category=metadata["top_category"],
                detected_pdf_type=detection["result"],
                processing_route="OPENDATALOADER_DIRECT",
                status="FAILED",
                output_markdown_relative_path="",
                output_json_relative_path="",
                output_ocr_pdf_relative_path="",
                error_message=str(exc),
            )
            stamp = utc_now_stamp()
            snapshot_conversion_registry(registry_dir, stamp)
            print(f"ERROR: {exc}")
            return 1

    else:
        try:
            report = convert_office_source(
                relative_source_path=relative_pdf_path,
                run_command="convert-one",
            )
        except Exception as exc:
            metadata = _source_metadata_from_raw(relative_pdf_path)
            _write_conversion_registry_entry(
                run_command="convert-one",
                source_relative_path=metadata["source_relative_path"],
                logical_source_relative_path=metadata["logical_source_relative_path"],
                source_extension=metadata["source_extension"],
                source_size_bytes=metadata["source_size_bytes"],
                source_modified_utc=metadata["source_modified_utc"],
                top_category=metadata["top_category"],
                detected_pdf_type="UNKNOWN",
                processing_route="OFFICE_TO_PDF_THEN_OPENDATALOADER",
                status="FAILED",
                output_markdown_relative_path="",
                output_json_relative_path="",
                output_ocr_pdf_relative_path="",
                error_message=str(exc),
            )
            stamp = utc_now_stamp()
            snapshot_conversion_registry(registry_dir, stamp)
            print(f"ERROR: {exc}")
            return 1

    stamp = utc_now_stamp()
    safe_stem = safe_name_for_report(source_path.stem)

    latest_json = runs_dir / "latest_convert_one_report.json"
    timestamped_json = runs_dir / f"{stamp}_{safe_stem}_convert_one_report.json"

    latest_txt = runs_dir / "latest_convert_one_report.txt"
    timestamped_txt = runs_dir / f"{stamp}_{safe_stem}_convert_one_report.txt"

    report_payload = {
        "project": "Vitruvius",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        **report,
    }

    text_lines = [
        "Vitruvius Convert One Report",
        "",
        f"Source: {relative_pdf_path}",
    ]

    if "office_pdf_output" in report:
        text_lines.append(f"Office PDF output: {report['office_pdf_output']}")

    text_lines.extend(
        [
            f"Detection result: {report['detection_result']}",
            f"Recommended route: {report['recommended_route']}",
            f"Markdown output: {report['markdown_output']}",
            f"JSON output: {report['json_output']}",
            "",
            "STATUS: converted",
        ]
    )

    report_text = "\n".join(text_lines) + "\n"

    write_json(latest_json, report_payload)
    write_json(timestamped_json, report_payload)
    write_text(latest_txt, report_text)
    write_text(timestamped_txt, report_text)

    snapshot_conversion_registry(registry_dir, stamp)

    print("Convert-one complete.")
    print(f"Source file: {source_path}")
    if "office_pdf_output" in report:
        print(f"Office PDF output: {report['office_pdf_output']}")
    print(f"Detection result: {report['detection_result']}")
    print(f"Markdown output: {report['markdown_output']}")
    print(f"JSON output: {report['json_output']}")
    print(f"Latest convert-one JSON: {latest_json}")
    print(f"Latest convert-one TXT: {latest_txt}")

    return 0


def run_convert() -> int:
    repo_root = get_repo_root()
    registry_dir = ensure_registry_dir(repo_root)
    runs_dir = ensure_runs_dir(repo_root)
    ensure_conversion_registry_exists(registry_dir)

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
    office_candidates = [p for p in candidates if is_supported_office_file(p)]
    skipped_non_supported = [
        p for p in candidates
        if Path(p).suffix.lower() not in SUPPORTED_DIRECT_INPUT_EXTENSIONS
    ]

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
                run_command="convert",
                source_relative_path=_raw_layer_relative_string(rel_path),
                logical_source_relative_path=rel_path,
                source_extension=source_extension,
                source_size_bytes=source_size_bytes,
                source_modified_utc=source_modified_utc,
                top_category=top_category,
                detected_pdf_type="UNKNOWN",
                processing_route="FAILED_PRECHECK",
                status="FAILED",
                output_markdown_relative_path="",
                output_json_relative_path="",
                output_ocr_pdf_relative_path="",
                error_message=str(exc),
            )
            continue

        queue_items.append(
            {
                "source_relative_path": rel_path,
                "source_type": "pdf",
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
                    run_command="convert",
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

                stat = source_pdf.stat()
                logical_parts = Path(rel_path).parts
                top_category = logical_parts[0] if logical_parts else ""

                _write_conversion_registry_entry(
                    run_command="convert",
                    source_relative_path=_raw_layer_relative_string(rel_path),
                    logical_source_relative_path=rel_path,
                    source_extension=source_pdf.suffix.lower(),
                    source_size_bytes=stat.st_size,
                    source_modified_utc=datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).isoformat(),
                    top_category=top_category,
                    detected_pdf_type=detection["result"],
                    processing_route="OPENDATALOADER_DIRECT",
                    status="FAILED",
                    output_markdown_relative_path="",
                    output_json_relative_path="",
                    output_ocr_pdf_relative_path="",
                    error_message=str(exc),
                )
        else:
            ocr_needed_items.append(
                {
                    "source_relative_path": rel_path,
                    "source_type": "pdf",
                    "planned_markdown_output": markdown_rel.as_posix(),
                    "planned_sidecar_output": json_rel.as_posix(),
                    "detection_result": detection["result"],
                    "recommended_route": detection["recommended_route"],
                    "status": "ocr_required",
                }
            )

            stat = source_pdf.stat()
            logical_parts = Path(rel_path).parts
            top_category = logical_parts[0] if logical_parts else ""

            _write_conversion_registry_entry(
                run_command="convert",
                source_relative_path=_raw_layer_relative_string(rel_path),
                logical_source_relative_path=rel_path,
                source_extension=source_pdf.suffix.lower(),
                source_size_bytes=stat.st_size,
                source_modified_utc=datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).isoformat(),
                top_category=top_category,
                detected_pdf_type=detection["result"],
                processing_route="OCR_THEN_OPENDATALOADER",
                status="QUEUED_FOR_OCR",
                output_markdown_relative_path="",
                output_json_relative_path="",
                output_ocr_pdf_relative_path="",
                error_message="",
            )

    for rel_path in office_candidates:
        markdown_rel, json_rel = build_conversion_relative_paths(rel_path)

        queue_items.append(
            {
                "source_relative_path": rel_path,
                "source_type": "office",
                "planned_markdown_output": markdown_rel.as_posix(),
                "planned_sidecar_output": json_rel.as_posix(),
                "detection_result": "PENDING_OFFICE_CONVERSION",
                "recommended_route": "OFFICE_TO_PDF_THEN_OPENDATALOADER",
            }
        )

        try:
            converted = convert_office_source(
                relative_source_path=rel_path,
                run_command="convert",
            )
            converted_items.append(converted)
        except Exception as exc:
            failed_items.append(
                {
                    "source_relative_path": rel_path,
                    "status": "failed_office_conversion",
                    "error": str(exc),
                }
            )

            metadata = _source_metadata_from_raw(rel_path)
            _write_conversion_registry_entry(
                run_command="convert",
                source_relative_path=metadata["source_relative_path"],
                logical_source_relative_path=metadata["logical_source_relative_path"],
                source_extension=metadata["source_extension"],
                source_size_bytes=metadata["source_size_bytes"],
                source_modified_utc=metadata["source_modified_utc"],
                top_category=metadata["top_category"],
                detected_pdf_type="UNKNOWN",
                processing_route="OFFICE_TO_PDF_THEN_OPENDATALOADER",
                status="FAILED",
                output_markdown_relative_path="",
                output_json_relative_path="",
                output_ocr_pdf_relative_path="",
                error_message=str(exc),
            )

    queue_report = {
        "project": "Vitruvius",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "status_source": str(latest_status_json),
        "summary": {
            "candidate_count": len(candidates),
            "queued_pdf_count": len(pdf_candidates),
            "queued_office_count": len(office_candidates),
            "queued_supported_count": len(queue_items),
            "skipped_non_supported_count": len(skipped_non_supported),
        },
        "queued_items": queue_items,
        "skipped_non_supported": skipped_non_supported,
    }

    batch_report = {
        "project": "Vitruvius",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "status_source": str(latest_status_json),
        "summary": {
            "candidate_count": len(candidates),
            "pdf_candidate_count": len(pdf_candidates),
            "office_candidate_count": len(office_candidates),
            "converted_count": len(converted_items),
            "ocr_required_count": len(ocr_needed_items),
            "failed_count": len(failed_items),
            "skipped_non_supported_count": len(skipped_non_supported),
        },
        "converted_items": converted_items,
        "ocr_required_items": ocr_needed_items,
        "failed_items": failed_items,
        "skipped_non_supported": skipped_non_supported,
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
        f"Queued PDF files: {len(pdf_candidates)}",
        f"Queued Office files: {len(office_candidates)}",
        f"Total queued supported files: {len(queue_items)}",
        f"Skipped non-supported files: {len(skipped_non_supported)}",
        "",
        "QUEUED ITEMS:",
    ]

    if queue_items:
        for item in queue_items:
            queue_text_lines.append("  ---")
            queue_text_lines.append(f"  source: {item['source_relative_path']}")
            queue_text_lines.append(f"  source_type: {item['source_type']}")
            queue_text_lines.append(f"  markdown: {item['planned_markdown_output']}")
            queue_text_lines.append(f"  sidecar: {item['planned_sidecar_output']}")
            queue_text_lines.append(f"  detection: {item['detection_result']}")
            queue_text_lines.append(f"  route: {item['recommended_route']}")
    else:
        queue_text_lines.append("  None")

    queue_text_lines.extend(["", "SKIPPED NON-SUPPORTED:"])
    if skipped_non_supported:
        for item in skipped_non_supported:
            queue_text_lines.append(f"  {item}")
    else:
        queue_text_lines.append("  None")

    queue_text = "\n".join(queue_text_lines) + "\n"

    batch_text_lines = [
        "Vitruvius Convert Batch Report",
        "",
        f"Candidate files: {len(candidates)}",
        f"PDF candidates: {len(pdf_candidates)}",
        f"Office candidates: {len(office_candidates)}",
        f"Converted: {len(converted_items)}",
        f"OCR required: {len(ocr_needed_items)}",
        f"Failed: {len(failed_items)}",
        f"Skipped non-supported: {len(skipped_non_supported)}",
        "",
        "CONVERTED ITEMS:",
    ]

    if converted_items:
        for item in converted_items:
            batch_text_lines.append("  ---")
            batch_text_lines.append(f"  source: {item['source_relative_path']}")
            if "office_pdf_output_relative" in item:
                batch_text_lines.append(f"  office_pdf: {item['office_pdf_output_relative']}")
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
            text_lines_route = item["recommended_route"]
            ocr_text_lines.append(f"  route: {text_lines_route}")
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

    snapshot_conversion_registry(registry_dir, stamp)

    print("Batch convert complete.")
    print(f"Candidate files: {len(candidates)}")
    print(f"PDF candidates: {len(pdf_candidates)}")
    print(f"Office candidates: {len(office_candidates)}")
    print(f"Converted: {len(converted_items)}")
    print(f"OCR required: {len(ocr_needed_items)}")
    print(f"Failed: {len(failed_items)}")
    print(f"Skipped non-supported files: {len(skipped_non_supported)}")
    print(f"Latest queue JSON: {latest_queue_json}")
    print(f"Latest batch JSON: {latest_batch_json}")
    print(f"Latest OCR-needed JSON: {latest_ocr_json}")

    return 0