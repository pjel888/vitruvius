from __future__ import annotations

import argparse

from vitruvius.conversion import run_convert, run_convert_one
from vitruvius.detection import run_detect_one
from vitruvius.linting import run_lint
from vitruvius.ocr import run_ocr_execute, run_ocr_queue
from vitruvius.reconcile import run_reconcile
from vitruvius.scanner import run_scan
from vitruvius.status import run_status
from vitruvius.spreadsheets import run_convert_spreadsheet_one


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

    subparsers.add_parser(
        "convert",
        help="Convert all queued supported files from latest status (.pdf, .docx, .pptx)",
    )

    subparsers.add_parser(
        "reconcile",
        help="Report missing raw files and stale derived outputs (pdf, office, ocr, spreadsheet)",
    )

    subparsers.add_parser(
        "ocr-queue",
        help="Build a report-only OCR queue from the latest OCR-needed report",
    )

    subparsers.add_parser("run", help="Run scan, status, and lint")

    detect_one_parser = subparsers.add_parser(
        "detect-one",
        help="Detect whether one PDF is text-based or likely scanned",
    )
    detect_one_parser.add_argument(
        "relative_pdf_path",
        help="PDF path relative to 001_Raw-Source-Layer",
    )
    detect_one_parser.add_argument(
        "--sample-pages",
        type=int,
        default=5,
        help="How many pages to sample",
    )

    convert_one_parser = subparsers.add_parser(
        "convert-one",
        help="Convert one supported document file (.pdf, .docx, .pptx, .doc, .ppt)",
    )
    convert_one_parser.add_argument(
        "relative_pdf_path",
        help="Path relative to 001_Raw-Source-Layer",
    )
    convert_one_parser.add_argument(
        "--sample-pages",
        type=int,
        default=5,
        help="How many pages to sample for text detection",
    )

    spreadsheet_one_parser = subparsers.add_parser(
        "convert-spreadsheet-one",
        help="Convert one spreadsheet (.xlsx, .xls) into CSV + JSON + manifest",
    )
    spreadsheet_one_parser.add_argument(
        "relative_source_path",
        help="Spreadsheet path relative to 001_Raw-Source-Layer",
    )

    ocr_execute_parser = subparsers.add_parser(
        "ocr-execute",
        help="Run OCRmyPDF on queued PDFs, then convert OCR outputs",
    )
    ocr_execute_parser.add_argument(
        "--languages",
        nargs="+",
        default=["eng"],
        help="Tesseract language codes",
    )
    ocr_execute_parser.add_argument(
        "--no-deskew",
        action="store_true",
        help="Disable deskew during OCR",
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

    if args.command == "reconcile":
        return run_reconcile()

    if args.command == "ocr-queue":
        return run_ocr_queue()

    if args.command == "ocr-execute":
        return run_ocr_execute(
            languages=args.languages,
            deskew=not args.no_deskew,
        )

    if args.command == "run":
        return run_pipeline()

    if args.command == "detect-one":
        return run_detect_one(
            relative_pdf_path=args.relative_pdf_path,
            sample_pages=args.sample_pages,
        )

    if args.command == "convert-one":
        return run_convert_one(
            relative_pdf_path=args.relative_pdf_path,
            sample_pages=args.sample_pages,
        )

    if args.command == "convert-spreadsheet-one":
        return run_convert_spreadsheet_one(
            relative_source_path=args.relative_source_path,
        )

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())