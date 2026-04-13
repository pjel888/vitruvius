from __future__ import annotations

import argparse

from vitruvius.canonicalize import run_canonicalize_one, run_canonicalize_plan_one
from vitruvius.conversion import run_convert, run_convert_one
from vitruvius.detection import run_detect_one
from vitruvius.linting import run_lint
from vitruvius.ocr import run_ocr_execute, run_ocr_queue
from vitruvius.reconcile import run_reconcile
from vitruvius.scanner import run_scan
from vitruvius.spreadsheets import run_convert_spreadsheet_one
from vitruvius.status import run_status
from vitruvius.concepts import run_canonicalize_concept_one
from vitruvius.migrations import run_migrate_ids_plan

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

    subparsers.add_parser("scan")
    subparsers.add_parser("status")
    subparsers.add_parser("lint")
    subparsers.add_parser("convert")
    subparsers.add_parser("reconcile")
    subparsers.add_parser("ocr-queue")
    subparsers.add_parser("run")
    subparsers.add_parser("migrate-ids-plan")

    detect_parser = subparsers.add_parser("detect-one")
    detect_parser.add_argument("relative_pdf_path")
    detect_parser.add_argument("--sample-pages", type=int, default=5)

    convert_one_parser = subparsers.add_parser("convert-one")
    convert_one_parser.add_argument("relative_pdf_path")
    convert_one_parser.add_argument("--sample-pages", type=int, default=5)

    spreadsheet_parser = subparsers.add_parser("convert-spreadsheet-one")
    spreadsheet_parser.add_argument("relative_source_path")

    ocr_parser = subparsers.add_parser("ocr-execute")
    ocr_parser.add_argument("--languages", nargs="+", default=["eng"])
    ocr_parser.add_argument("--no-deskew", action="store_true")

    plan_parser = subparsers.add_parser("canonicalize-plan-one")
    plan_parser.add_argument("relative_markdown_path")

    execute_parser = subparsers.add_parser("canonicalize-one")
    execute_parser.add_argument("relative_markdown_path")

    concept_parser = subparsers.add_parser("canonicalize-concept-one")
    concept_parser.add_argument("concept_name")

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

    if args.command == "canonicalize-plan-one":
        return run_canonicalize_plan_one(
            relative_markdown_path=args.relative_markdown_path,
        )

    if args.command == "canonicalize-one":
        return run_canonicalize_one(
            relative_markdown_path=args.relative_markdown_path,
        )

    if args.command == "canonicalize-concept-one":
        return run_canonicalize_concept_one(
            concept_name=args.concept_name,
        )

    if args.command == "migrate-ids-plan":
        return run_migrate_ids_plan()

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())