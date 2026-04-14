"""Vitruvius pipeline CLI entrypoint.

All handler imports are lazy (inside each `if args.command == "..."` branch)
so running, e.g., `promote --help` does NOT transitively import
`opendataloader_pdf`, `pypdf`, or `ocrmypdf`. This makes the CLI usable in
minimal environments without the full conversion dependency stack.

See AD-015 in .ai/10_state/decisions.md for the rationale.
"""

from __future__ import annotations

import argparse


def run_pipeline() -> int:
    from vitruvius.linting import run_lint
    from vitruvius.scanner import run_scan
    from vitruvius.status import run_status

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
    from vitruvius.config import get_ollama_default_model, get_ollama_default_timeout
    from vitruvius.conversion import run_convert
    from vitruvius.normalization.refine import run_refine
    from vitruvius.ollama_review import run_review_relationships_ollama

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

    second_pass_parser = subparsers.add_parser("review-relationships-ollama-second-pass")
    second_pass_parser.add_argument("--model", default=None,
                                    help="Tier-2 model (default: qwen3:30b)")
    second_pass_parser.add_argument("--timeout-seconds", type=int, default=None)

    enrich_one_parser = subparsers.add_parser("enrich-concept-one")
    enrich_one_parser.add_argument("concept_slug")
    enrich_one_parser.add_argument("--force", action="store_true",
                                   help="Re-enrich even if canonical_status is already enriched")

    enrich_parser = subparsers.add_parser("enrich-concepts")
    enrich_parser.add_argument("--force", action="store_true",
                               help="Re-enrich even already-enriched concepts")

    subparsers.add_parser("canonicalize")
    subparsers.add_parser("refine")
    subparsers.add_parser("run-with-review")
    refine_one_parser = subparsers.add_parser("refine-one")
    refine_one_parser.add_argument("relative_markdown_path")

    rotate_parser = subparsers.add_parser("rotate-registries")
    rotate_parser.add_argument("--keep", type=int, default=30,
                               help="Number of timestamped snapshots to retain per family (default: 30)")
    rotate_parser.add_argument("--dry-run", action="store_true",
                               help="Show what would be pruned without deleting")

    build_graph_parser = subparsers.add_parser("build-graph")
    build_graph_parser.add_argument("--dry-run", action="store_true",
                                    help="Run walker + integrity checks only; do not write files")

    query_graph_parser = subparsers.add_parser("query-graph")
    query_graph_parser.add_argument("--from", dest="from_id", required=True,
                                    help="Source node id")
    query_graph_parser.add_argument("--to", dest="to_id", required=True,
                                    help="Target node id")
    query_graph_parser.add_argument("--max-depth", type=int, default=3,
                                    help="Max path depth (default: 3)")

    export_graph_parser = subparsers.add_parser("export-graph-snapshot")
    export_graph_parser.add_argument("--format", dest="fmt", default="json",
                                     choices=["json"],
                                     help="Output format (default: json)")

    query_parser = subparsers.add_parser("query")
    query_parser.add_argument("question", help="Natural-language question")

    query_struct_parser = subparsers.add_parser("query-structured")
    query_struct_parser.add_argument(
        "--function", required=True,
        help="One of what_governs, what_requires, what_limits, what_defines, "
             "what_depends_on, what_affects, supersession_chain, neighbors, "
             "edges_between",
    )
    query_struct_parser.add_argument("--subject", default=None,
                                     help="Subject entity id")
    query_struct_parser.add_argument("--a", dest="a", default=None,
                                     help="Entity a (edges_between only)")
    query_struct_parser.add_argument("--b", dest="b", default=None,
                                     help="Entity b (edges_between only)")

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "scan":
        from vitruvius.scanner import run_scan
        return run_scan()

    if args.command == "status":
        from vitruvius.status import run_status
        return run_status()

    if args.command == "lint":
        from vitruvius.linting import run_lint
        return run_lint()

    if args.command == "convert":
        from vitruvius.conversion import run_convert
        return run_convert()

    if args.command == "reconcile":
        from vitruvius.reconcile import run_reconcile
        return run_reconcile()

    if args.command == "ocr-queue":
        from vitruvius.ocr import run_ocr_queue
        return run_ocr_queue()

    if args.command == "ocr-execute":
        from vitruvius.ocr import run_ocr_execute
        return run_ocr_execute(
            languages=args.languages,
            deskew=not args.no_deskew,
        )

    if args.command == "run":
        return run_pipeline()

    if args.command == "detect-one":
        from vitruvius.detection import run_detect_one
        return run_detect_one(
            relative_pdf_path=args.relative_pdf_path,
            sample_pages=args.sample_pages,
        )

    if args.command == "convert-one":
        from vitruvius.conversion import run_convert_one
        return run_convert_one(
            relative_pdf_path=args.relative_pdf_path,
            sample_pages=args.sample_pages,
        )

    if args.command == "convert-spreadsheet-one":
        from vitruvius.spreadsheets import run_convert_spreadsheet_one
        return run_convert_spreadsheet_one(
            relative_source_path=args.relative_source_path,
        )

    if args.command == "canonicalize-plan-one":
        from vitruvius.canonicalize import run_canonicalize_plan_one
        return run_canonicalize_plan_one(
            relative_markdown_path=args.relative_markdown_path,
        )

    if args.command == "canonicalize-one":
        from vitruvius.canonicalize import run_canonicalize_one
        return run_canonicalize_one(
            relative_markdown_path=args.relative_markdown_path,
        )

    if args.command == "canonicalize-concept-one":
        from vitruvius.concepts import run_canonicalize_concept_one
        return run_canonicalize_concept_one(
            concept_name=args.concept_name,
        )

    if args.command == "migrate-ids-plan":
        from vitruvius.migrations import run_migrate_ids_plan
        return run_migrate_ids_plan()

    if args.command == "migrate-ids-apply":
        from vitruvius.migrations import run_migrate_ids_apply
        return run_migrate_ids_apply()

    if args.command == "extract-relationships-one":
        from vitruvius.relationships import run_extract_relationships_one
        return run_extract_relationships_one(
            relative_markdown_path=args.relative_markdown_path,
        )

    if args.command == "extract-relationships-sections-one":
        from vitruvius.relationships_sections import run_extract_relationships_sections_one
        return run_extract_relationships_sections_one(
            relative_markdown_path=args.relative_markdown_path,
        )

    if args.command == "review-relationships-ollama":
        from vitruvius.ollama_review import run_review_relationships_ollama
        return run_review_relationships_ollama(
            model=args.model,
            timeout_seconds=args.timeout_seconds,
            parallelism=args.parallel,
        )

    if args.command == "promote":
        from vitruvius.promotion import run_promote
        return run_promote(
            execute=args.execute,
            rollback_batch_id=args.rollback_batch_id,
        )

    if args.command == "review-relationships-ollama-second-pass":
        from vitruvius.ollama_review_second_pass import run_second_pass
        return run_second_pass(
            model=args.model,
            timeout_seconds=args.timeout_seconds,
        )

    if args.command == "enrich-concept-one":
        from vitruvius.concept_enrichment import run_enrich_concept_one
        return run_enrich_concept_one(
            concept_slug=args.concept_slug,
            force=args.force,
        )

    if args.command == "enrich-concepts":
        from vitruvius.concept_enrichment import run_enrich_concepts
        return run_enrich_concepts(force=args.force)

    if args.command == "canonicalize":
        from vitruvius.canonicalize import run_canonicalize
        return run_canonicalize()

    if args.command == "refine":
        from vitruvius.normalization.refine import run_refine
        return run_refine()

    if args.command == "run-with-review":
        return run_pipeline_with_review()

    if args.command == "refine-one":
        from vitruvius.normalization.refine import run_refine_one
        return run_refine_one(relative_markdown_path=args.relative_markdown_path)

    if args.command == "rotate-registries":
        from vitruvius.registry_rotation import run_rotate_registries
        return run_rotate_registries(keep=args.keep, dry_run=args.dry_run)

    if args.command == "build-graph":
        from vitruvius.graph.cli import run_build_graph
        return run_build_graph(dry_run=args.dry_run)

    if args.command == "query-graph":
        from vitruvius.graph.cli import run_query_graph
        return run_query_graph(
            from_id=args.from_id,
            to_id=args.to_id,
            max_depth=args.max_depth,
        )

    if args.command == "export-graph-snapshot":
        from vitruvius.graph.cli import run_export_graph_snapshot
        return run_export_graph_snapshot(fmt=args.fmt)

    if args.command == "query":
        from vitruvius.query.cli import run_query
        return run_query(args.question)

    if args.command == "query-structured":
        from vitruvius.query.cli import run_query_structured
        return run_query_structured(
            function=args.function,
            subject=args.subject,
            a=args.a,
            b=args.b,
        )

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
