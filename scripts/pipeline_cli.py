from __future__ import annotations

import argparse

from vitruvius.canonicalize import run_canonicalize, run_canonicalize_one, run_canonicalize_plan_one
from vitruvius.concepts import run_canonicalize_concept_one
from vitruvius.conversion import run_convert, run_convert_one
from vitruvius.detection import run_detect_one
from vitruvius.linting import run_lint
from vitruvius.migrations import run_migrate_ids_apply, run_migrate_ids_plan
from vitruvius.ocr import run_ocr_execute, run_ocr_queue
from vitruvius.config import get_ollama_default_model, get_ollama_default_timeout
from vitruvius.normalization.refine import run_refine, run_refine_one
from vitruvius.ollama_review import run_review_relationships_ollama
from vitruvius.promotion import run_promote
from vitruvius.reconcile import run_reconcile
from vitruvius.relationships import run_extract_relationships_one
from vitruvius.relationships_sections import run_extract_relationships_sections_one
from vitruvius.scanner import run_scan
from vitruvius.spreadsheets import run_convert_spreadsheet_one
from vitruvius.status import run_status


def run_pipeline() -> int:
    scan_code = run_scan()
    if scan_code != 0:
        return scan_code

    status_code = run_status()
    if status_code != 0:
        return status_code

    return run_lint()


def run_pipeline_with_review() -> int:
    """Full pipeline ending with LLM review.

    Opt-in composite command. The default `run` stays minimal (scan +
    status + lint) so that CI and automation don't accidentally invoke
    Ollama. Users who want the full path call `run-with-review` explicitly.
    """
    rc = run_pipeline()
    if rc != 0:
        return rc
    rc = run_convert()
    if rc != 0:
        return rc
    rc = run_refine()
    if rc != 0:
        return rc
    return run_review_relationships_ollama(
        model=get_ollama_default_model(),
        timeout_seconds=get_ollama_default_timeout(),
    )


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
    subparsers.add_parser("migrate-ids-apply")

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

    rel_parser = subparsers.add_parser("extract-relationships-one")
    rel_parser.add_argument("relative_markdown_path")

    sec_parser = subparsers.add_parser("extract-relationships-sections-one")
    sec_parser.add_argument("relative_markdown_path")

    review_parser = subparsers.add_parser("review-relationships-ollama")
    review_parser.add_argument("--model", default="gemma4:31b")
    review_parser.add_argument("--timeout-seconds", type=int, default=600)
    review_parser.add_argument("--parallel", type=int, default=None,
                               help="Concurrent Ollama requests (default: config)")

    promote_parser = subparsers.add_parser("promote")
    promote_parser.add_argument("--execute", action="store_true",
                                help="Write changes (default: dry-run)")
    promote_parser.add_argument("--rollback", dest="rollback_batch_id",
                                default=None,
                                help="Rollback the given promotion batch ID")

    subparsers.add_parser("canonicalize")
    subparsers.add_parser("refine")
    subparsers.add_parser("run-with-review")
    refine_one_parser = subparsers.add_parser("refine-one")
    refine_one_parser.add_argument("relative_markdown_path")

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

    if args.command == "migrate-ids-apply":
        return run_migrate_ids_apply()

    if args.command == "extract-relationships-one":
        return run_extract_relationships_one(
            relative_markdown_path=args.relative_markdown_path,
        )

    if args.command == "extract-relationships-sections-one":
        return run_extract_relationships_sections_one(
            relative_markdown_path=args.relative_markdown_path,
        )

    if args.command == "review-relationships-ollama":
        return run_review_relationships_ollama(
            model=args.model,
            timeout_seconds=args.timeout_seconds,
            parallelism=args.parallel,
        )

    if args.command == "promote":
        return run_promote(
            execute=args.execute,
            rollback_batch_id=args.rollback_batch_id,
        )

    if args.command == "canonicalize":
        return run_canonicalize()

    if args.command == "refine":
        return run_refine()

    if args.command == "run-with-review":
        return run_pipeline_with_review()

    if args.command == "refine-one":
        return run_refine_one(relative_markdown_path=args.relative_markdown_path)

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())