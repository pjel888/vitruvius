from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from pypdf import PdfReader

from .constants import RAW_LAYER_NAME
from .paths import ensure_runs_dir, get_repo_root
from .reports import write_json, write_text
from .utils import safe_name_for_report, utc_now_stamp


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
        # Whitespace-collapse inline. Previously called utils.normalize_text()
        # which now emits a DeprecationWarning.
        text = " ".join(raw.split())
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
    safe_stem = safe_name_for_report(pdf_path.stem)

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