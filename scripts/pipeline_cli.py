"""Vitruvius pipeline CLI entrypoint.

All handler imports are lazy (inside each `if args.command == "..."` branch)
so running, e.g., `promote --help` does NOT transitively import
`opendataloader_pdf`, `pypdf`, or `ocrmypdf`. This makes the CLI usable in
minimal environments without the full conversion dependency stack.

See AD-015 in .ai/10_state/decisions.md for the rationale.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from vitruvius.cli_experience import (
    RAW_HELP_FORMATTER,
    ROOT_PARSER_DESCRIPTION,
    ROOT_PARSER_EPILOG,
    add_command_parser,
    execute_with_cli_experience,
)


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
    parser = argparse.ArgumentParser(
        description=ROOT_PARSER_DESCRIPTION,
        epilog=ROOT_PARSER_EPILOG,
        formatter_class=RAW_HELP_FORMATTER,
    )
    parser.add_argument(
        "--output-mode",
        choices=["auto", "operator", "concise"],
        default="auto",
        help="How much operator framing to print around command output (default: auto).",
    )
    subparsers = parser.add_subparsers(dest="command")

    add_command_parser(subparsers, "scan")
    add_command_parser(subparsers, "status")
    add_command_parser(subparsers, "lint")
    add_command_parser(subparsers, "convert")
    add_command_parser(subparsers, "reconcile")
    add_command_parser(subparsers, "ocr-queue")
    add_command_parser(subparsers, "run")
    add_command_parser(subparsers, "migrate-ids-plan")
    add_command_parser(subparsers, "migrate-ids-apply")

    p_kv_migrate = add_command_parser(
        subparsers,
        "ple-kv-migrate",
    )
    p_kv_migrate.add_argument("--store", choices=["event", "registry"], required=True)
    p_kv_migrate.add_argument("--source", type=Path, required=True)
    p_kv_migrate.add_argument("--dest", type=Path, required=True)
    p_kv_migrate.add_argument("--dry-run", action="store_true")

    detect_parser = add_command_parser(subparsers, "detect-one")
    detect_parser.add_argument("relative_pdf_path")
    detect_parser.add_argument("--sample-pages", type=int, default=5)

    convert_one_parser = add_command_parser(subparsers, "convert-one")
    convert_one_parser.add_argument("relative_pdf_path")
    convert_one_parser.add_argument("--sample-pages", type=int, default=5)

    # Sprint PIPELINE-CLI Task 3 — Phase 1B parser-chain CLI.
    # Parallel command to convert-one; routes through
    # ParserOrchestrator + the p1b_* feature flags. See
    # scripts/vitruvius/parsers/cli_handler.py for the handler and
    # scripts/vitruvius/parsers/factory.py for the flag dispatch.
    convert_parsers_one_parser = add_command_parser(
        subparsers,
        "convert-parsers-one",
    )
    convert_parsers_one_parser.add_argument("relative_pdf_path")

    spreadsheet_parser = add_command_parser(subparsers, "convert-spreadsheet-one")
    spreadsheet_parser.add_argument("relative_source_path")

    ocr_parser = add_command_parser(subparsers, "ocr-execute")
    ocr_parser.add_argument("--languages", nargs="+", default=["eng"])
    ocr_parser.add_argument("--no-deskew", action="store_true")

    plan_parser = add_command_parser(subparsers, "canonicalize-plan-one")
    plan_parser.add_argument("relative_markdown_path")

    execute_parser = add_command_parser(subparsers, "canonicalize-one")
    execute_parser.add_argument("relative_markdown_path")

    concept_parser = add_command_parser(subparsers, "canonicalize-concept-one")
    concept_parser.add_argument("concept_name")

    rel_parser = add_command_parser(subparsers, "extract-relationships-one")
    rel_parser.add_argument("relative_markdown_path")

    sec_parser = add_command_parser(subparsers, "extract-relationships-sections-one")
    sec_parser.add_argument("relative_markdown_path")
    sec_parser.add_argument("--json-out", dest="json_output_path", default=None,
                            help="Optional explicit JSON output path")
    sec_parser.add_argument("--txt-out", dest="txt_output_path", default=None,
                            help="Optional explicit TXT output path")
    sec_parser.add_argument("--source-id", dest="source_id_override", default=None,
                            help="Optional explicit source node id override")
    sec_parser.add_argument("--concept-path", dest="concept_paths", action="append", default=None,
                            help="Optional concept markdown path to whitelist (repeatable)")

    review_parser = add_command_parser(subparsers, "review-relationships-ollama")
    review_parser.add_argument("--model", default="gemma4:31b")
    review_parser.add_argument("--timeout-seconds", type=int, default=600)
    review_parser.add_argument("--parallel", type=int, default=None,
                               help="Concurrent Ollama requests (default: config)")
    review_parser.add_argument("--input-report", dest="extraction_report_path", default=None,
                               help="Optional explicit extraction report JSON path")
    review_parser.add_argument("--review-json-out", dest="review_json_path", default=None,
                               help="Optional explicit review JSON output path")
    review_parser.add_argument("--review-txt-out", dest="review_txt_path", default=None,
                               help="Optional explicit review TXT output path")
    review_parser.add_argument("--triage-out", dest="triage_report_path", default=None,
                               help="Optional explicit triage JSON output path")
    review_parser.add_argument("--high-confidence-out", dest="high_confidence_output_path", default=None,
                               help="Optional explicit high-confidence JSON output path")

    promote_parser = add_command_parser(subparsers, "promote")
    promote_parser.add_argument("--execute", action="store_true",
                                help="Write changes (default: dry-run)")
    promote_parser.add_argument("--rollback", dest="rollback_batch_id",
                                default=None,
                                help="Rollback the given promotion batch ID")
    promote_parser.add_argument("--input-report", dest="high_confidence_input_path", default=None,
                                help="Optional explicit high-confidence review JSON path")
    promote_parser.add_argument("--relationships-out-dir", dest="relationships_output_dir", default=None,
                                help="Optional explicit relationship output directory")
    promote_parser.add_argument("--audit-log-path", dest="audit_log_path", default=None,
                                help="Optional explicit promotion audit log path")

    second_pass_parser = add_command_parser(subparsers, "review-relationships-ollama-second-pass")
    second_pass_parser.add_argument("--model", default=None,
                                    help="Tier-2 model (default: qwen3:30b)")
    second_pass_parser.add_argument("--timeout-seconds", type=int, default=None)
    second_pass_parser.add_argument("--input-review-report", dest="tier_one_report_path", default=None,
                                    help="Optional explicit tier-one review JSON path")
    second_pass_parser.add_argument("--merged-out", dest="merged_report_path", default=None,
                                    help="Optional explicit merged review output path")
    second_pass_parser.add_argument("--worklist-out", dest="worklist_path", default=None,
                                    help="Optional explicit human worklist output path")

    enrich_one_parser = add_command_parser(subparsers, "enrich-concept-one")
    enrich_one_parser.add_argument("concept_slug")
    enrich_one_parser.add_argument("--force", action="store_true",
                                   help="Re-enrich even if canonical_status is already enriched")

    enrich_parser = add_command_parser(subparsers, "enrich-concepts")
    enrich_parser.add_argument("--force", action="store_true",
                               help="Re-enrich even already-enriched concepts")

    add_command_parser(subparsers, "canonicalize")
    add_command_parser(subparsers, "refine")
    add_command_parser(subparsers, "run-with-review")
    dataset_graph_parser = add_command_parser(subparsers, "run-dataset-graph")
    dataset_graph_parser.add_argument("--dataset-manifest", required=True,
                                      help="Dataset manifest to orchestrate")
    dataset_graph_parser.add_argument("--structured-check", action="append", default=None,
                                      help="Repeatable FUNCTION:SUBJECT structured check against the final snapshot")
    dataset_graph_parser.add_argument("--skip-export-owl", action="store_true",
                                      help="Skip dataset-local OWL/Turtle export")
    dataset_source_to_graph_parser = add_command_parser(subparsers, "run-dataset-source-to-graph")
    dataset_source_to_graph_parser.add_argument("--dataset-manifest", required=True,
                                               help="Dataset manifest to orchestrate")
    dataset_source_to_graph_parser.add_argument("--structured-check", action="append", default=None,
                                               help="Repeatable FUNCTION:SUBJECT structured check against the final snapshot")
    dataset_source_to_graph_parser.add_argument("--skip-export-owl", action="store_true",
                                               help="Skip dataset-local OWL/Turtle export")
    dataset_source_to_graph_parser.add_argument("--dry-run", action="store_true",
                                               help="Validate/plans stages without executing writes")
    dataset_source_to_graph_parser.add_argument("--review-model", default="gemma4:31b",
                                               help="Tier-1 review model for dataset-local review")
    dataset_source_to_graph_parser.add_argument("--review-timeout-seconds", type=int, default=600,
                                               help="Tier-1 review timeout seconds")
    dataset_source_to_graph_parser.add_argument("--review-parallel", type=int, default=None,
                                               help="Tier-1 review parallelism override")
    dataset_source_to_graph_parser.add_argument("--visualize", action="store_true",
                                               help="Render an HTML graph visualization after a successful non-dry-run execution")
    dataset_source_to_graph_parser.add_argument("--open-browser", action="store_true",
                                               help="Open the rendered HTML graph visualization in the default browser after a successful non-dry-run execution")
    dataset_source_to_graph_parser.add_argument("--visualization-out", default=None,
                                               help="Optional output HTML path for the post-run visualization")
    laws_pilot_parser = add_command_parser(subparsers, "run-laws-pilot")
    laws_pilot_parser.add_argument("--structured-check", action="append", default=None,
                                   help="Repeatable FUNCTION:SUBJECT structured check against the final snapshot")
    laws_pilot_parser.add_argument("--skip-export-owl", action="store_true",
                                   help="Skip dataset-local OWL/Turtle export")
    laws_pilot_parser.add_argument("--dry-run", action="store_true",
                                   help="Validate/plans stages without executing writes")
    laws_pilot_parser.add_argument("--review-model", default="gemma4:31b",
                                   help="Tier-1 review model for dataset-local review")
    laws_pilot_parser.add_argument("--review-timeout-seconds", type=int, default=600,
                                   help="Tier-1 review timeout seconds")
    laws_pilot_parser.add_argument("--review-parallel", type=int, default=None,
                                   help="Tier-1 review parallelism override")
    laws_pilot_parser.add_argument("--visualize", action="store_true",
                                   help="Explicitly keep visualization enabled (default for non-dry-run pilot runs)")
    laws_pilot_parser.add_argument("--open-browser", action="store_true",
                                   help="Open the rendered HTML graph visualization in the default browser after a successful non-dry-run execution")
    laws_pilot_parser.add_argument("--visualization-out", default=None,
                                   help="Optional output HTML path for the post-run visualization")
    refine_one_parser = add_command_parser(subparsers, "refine-one")
    refine_one_parser.add_argument("relative_markdown_path")

    rotate_parser = add_command_parser(subparsers, "rotate-registries")
    rotate_parser.add_argument("--keep", type=int, default=30,
                               help="Number of timestamped snapshots to retain per family (default: 30)")
    rotate_parser.add_argument("--dry-run", action="store_true",
                               help="Show what would be pruned without deleting")

    build_graph_parser = add_command_parser(subparsers, "build-graph")
    build_graph_parser.add_argument("--dry-run", action="store_true",
                                    help="Run walker + integrity checks only; do not write files")
    build_graph_parser.add_argument(
        "--dataset-manifest",
        default=None,
        help="Optional dataset manifest for scoped graph output",
    )

    query_graph_parser = add_command_parser(subparsers, "query-graph")
    query_graph_parser.add_argument("--from", dest="from_id", required=True,
                                    help="Source node id")
    query_graph_parser.add_argument("--to", dest="to_id", required=True,
                                    help="Target node id")
    query_graph_parser.add_argument("--max-depth", type=int, default=3,
                                    help="Max path depth (default: 3)")
    query_graph_parser.add_argument(
        "--snapshot",
        dest="snapshot_path",
        default=None,
        help="Optional explicit snapshot path",
    )

    export_graph_parser = add_command_parser(subparsers, "export-graph-snapshot")
    export_graph_parser.add_argument("--format", dest="fmt", default="json",
                                     choices=["json"],
                                     help="Output format (default: json)")
    export_graph_parser.add_argument(
        "--snapshot",
        dest="snapshot_path",
        default=None,
        help="Optional explicit snapshot path",
    )

    # Stream M.4 — export-graph-owl
    export_graph_owl_parser = add_command_parser(
        subparsers,
        "export-graph-owl",
    )
    export_graph_owl_parser.add_argument(
        "--snapshot",
        dest="snapshot_path",
        default=None,
        help="Optional explicit snapshot path",
    )
    export_graph_owl_parser.add_argument(
        "--out",
        dest="out_path",
        default=None,
        help="Optional output Turtle path",
    )

    visualize_graph_parser = add_command_parser(subparsers, "visualize-graph")
    visualize_graph_parser.add_argument(
        "--snapshot",
        dest="snapshot_path",
        default=None,
        help="Optional explicit snapshot path",
    )
    visualize_graph_parser.add_argument(
        "--out",
        dest="out_path",
        default=None,
        help="Optional output HTML path",
    )

    add_command_parser(subparsers, "ingest-spatial")

    evaluate_spatial_parser = add_command_parser(subparsers, "evaluate-spatial")
    evaluate_spatial_parser.add_argument(
        "--concepts",
        required=True,
        help="Comma-separated concept slugs to evaluate",
    )
    evaluate_spatial_parser.add_argument(
        "--observations",
        dest="observations_path",
        required=True,
        help="Path to JSON observation file (dict: variable -> value)",
    )
    evaluate_spatial_parser.add_argument(
        "--rules",
        dest="rules_path",
        default=None,
        help="Optional path to JSON rules file (concept_id -> rule)",
    )

    # Stream Y3.4 — ple-cotrace-dump
    ple_cotrace_parser = add_command_parser(
        subparsers,
        "ple-cotrace-dump",
    )
    ple_cotrace_parser.add_argument(
        "--cot-dir",
        dest="cot_dir",
        required=True,
        help="Directory containing <utc-ts>_<hash>.json CoT trace files",
    )

    # Stream Y4.3 — ple-registry-purge
    ple_purge_parser = add_command_parser(
        subparsers,
        "ple-registry-purge",
    )
    ple_purge_parser.add_argument(
        "--db",
        dest="registry_db",
        required=True,
        help="Path to the SQLite registry file",
    )
    ple_purge_parser.add_argument(
        "--days",
        type=int,
        default=30,
        help="Retention window in days (default: 30)",
    )

    # Stream Y5.3 — ple-vision-probe
    ple_vision_probe_parser = add_command_parser(
        subparsers,
        "ple-vision-probe",
    )
    ple_vision_probe_parser.add_argument(
        "--required-free-gb",
        type=float,
        default=3.5,
        dest="required_free_gb",
        help="Minimum free RAM to require (default: 3.5 GB)",
    )
    ple_vision_probe_parser.add_argument(
        "--model",
        default="moondream:latest",
        help="Vision model family to check for (default: moondream:latest)",
    )

    query_parser = add_command_parser(subparsers, "query")
    query_parser.add_argument("question", help="Natural-language question")
    query_parser.add_argument(
        "--snapshot",
        dest="snapshot_path",
        default=None,
        help="Optional explicit snapshot path",
    )

    query_struct_parser = add_command_parser(subparsers, "query-structured")
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
    query_struct_parser.add_argument(
        "--snapshot",
        dest="snapshot_path",
        default=None,
        help="Optional explicit snapshot path",
    )

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    def _run(command_name: str, handler) -> int:
        return execute_with_cli_experience(
            command_name,
            output_mode=args.output_mode,
            handler=handler,
        )

    if args.command == "scan":
        from vitruvius.scanner import run_scan
        return _run("scan", run_scan)

    if args.command == "status":
        from vitruvius.status import run_status
        return _run("status", run_status)

    if args.command == "lint":
        from vitruvius.linting import run_lint
        return _run("lint", run_lint)

    if args.command == "convert":
        from vitruvius.conversion import run_convert
        return _run("convert", run_convert)

    if args.command == "reconcile":
        from vitruvius.reconcile import run_reconcile
        return _run("reconcile", run_reconcile)

    if args.command == "ocr-queue":
        from vitruvius.ocr import run_ocr_queue
        return _run("ocr-queue", run_ocr_queue)

    if args.command == "ocr-execute":
        from vitruvius.ocr import run_ocr_execute
        return _run(
            "ocr-execute",
            lambda: run_ocr_execute(
            languages=args.languages,
            deskew=not args.no_deskew,
            ),
        )

    if args.command == "run":
        return _run("run", run_pipeline)

    if args.command == "detect-one":
        from vitruvius.detection import run_detect_one
        return _run(
            "detect-one",
            lambda: run_detect_one(
            relative_pdf_path=args.relative_pdf_path,
            sample_pages=args.sample_pages,
            ),
        )

    if args.command == "convert-one":
        from vitruvius.conversion import run_convert_one
        return _run(
            "convert-one",
            lambda: run_convert_one(
            relative_pdf_path=args.relative_pdf_path,
            sample_pages=args.sample_pages,
            ),
        )

    if args.command == "convert-parsers-one":
        # Sprint PIPELINE-CLI Task 3. Lazy-import — see AD-015.
        from vitruvius.parsers.cli_handler import run_convert_parsers_one
        return _run(
            "convert-parsers-one",
            lambda: run_convert_parsers_one(
            relative_pdf_path=args.relative_pdf_path,
            ),
        )

    if args.command == "convert-spreadsheet-one":
        from vitruvius.spreadsheets import run_convert_spreadsheet_one
        return _run(
            "convert-spreadsheet-one",
            lambda: run_convert_spreadsheet_one(
            relative_source_path=args.relative_source_path,
            ),
        )

    if args.command == "canonicalize-plan-one":
        from vitruvius.canonicalize import run_canonicalize_plan_one
        return _run(
            "canonicalize-plan-one",
            lambda: run_canonicalize_plan_one(
            relative_markdown_path=args.relative_markdown_path,
            ),
        )

    if args.command == "canonicalize-one":
        from vitruvius.canonicalize import run_canonicalize_one
        return _run(
            "canonicalize-one",
            lambda: run_canonicalize_one(
            relative_markdown_path=args.relative_markdown_path,
            ),
        )

    if args.command == "canonicalize-concept-one":
        from vitruvius.concepts import run_canonicalize_concept_one
        return _run(
            "canonicalize-concept-one",
            lambda: run_canonicalize_concept_one(
            concept_name=args.concept_name,
            ),
        )

    if args.command == "migrate-ids-plan":
        from vitruvius.migrations import run_migrate_ids_plan
        return _run("migrate-ids-plan", run_migrate_ids_plan)

    if args.command == "migrate-ids-apply":
        from vitruvius.migrations import run_migrate_ids_apply
        return _run("migrate-ids-apply", run_migrate_ids_apply)

    if args.command == "ple-kv-migrate":
        from vitruvius.kv_migrate import run_kv_migrate
        return _run(
            "ple-kv-migrate",
            lambda: run_kv_migrate(
            store=args.store,
            source=args.source,
            dest=args.dest,
            dry_run=args.dry_run,
            ),
        )

    if args.command == "extract-relationships-one":
        from vitruvius.relationships import run_extract_relationships_one
        return _run(
            "extract-relationships-one",
            lambda: run_extract_relationships_one(
            relative_markdown_path=args.relative_markdown_path,
            ),
        )

    if args.command == "extract-relationships-sections-one":
        from vitruvius.relationships_sections import run_extract_relationships_sections_one
        return _run(
            "extract-relationships-sections-one",
            lambda: run_extract_relationships_sections_one(
            relative_markdown_path=args.relative_markdown_path,
            json_output_path=Path(args.json_output_path) if args.json_output_path else None,
            txt_output_path=Path(args.txt_output_path) if args.txt_output_path else None,
            source_id_override=args.source_id_override,
            concept_paths=[Path(p) for p in args.concept_paths] if args.concept_paths else None,
            ),
        )

    if args.command == "review-relationships-ollama":
        from vitruvius.ollama_review import run_review_relationships_ollama
        return _run(
            "review-relationships-ollama",
            lambda: run_review_relationships_ollama(
            model=args.model,
            timeout_seconds=args.timeout_seconds,
            parallelism=args.parallel,
            extraction_report_path=Path(args.extraction_report_path) if args.extraction_report_path else None,
            review_json_path=Path(args.review_json_path) if args.review_json_path else None,
            review_txt_path=Path(args.review_txt_path) if args.review_txt_path else None,
            triage_report_path=Path(args.triage_report_path) if args.triage_report_path else None,
            high_confidence_output_path=Path(args.high_confidence_output_path) if args.high_confidence_output_path else None,
            ),
        )

    if args.command == "promote":
        from vitruvius.promotion import run_promote
        return _run(
            "promote",
            lambda: run_promote(
            execute=args.execute,
            rollback_batch_id=args.rollback_batch_id,
            high_confidence_input_path=Path(args.high_confidence_input_path) if args.high_confidence_input_path else None,
            relationships_output_dir=Path(args.relationships_output_dir) if args.relationships_output_dir else None,
            audit_log_path=Path(args.audit_log_path) if args.audit_log_path else None,
            ),
        )

    if args.command == "review-relationships-ollama-second-pass":
        from vitruvius.ollama_review_second_pass import run_second_pass
        return _run(
            "review-relationships-ollama-second-pass",
            lambda: run_second_pass(
            model=args.model,
            timeout_seconds=args.timeout_seconds,
            tier_one_report_path=Path(args.tier_one_report_path) if args.tier_one_report_path else None,
            merged_report_path=Path(args.merged_report_path) if args.merged_report_path else None,
            worklist_path=Path(args.worklist_path) if args.worklist_path else None,
            ),
        )

    if args.command == "enrich-concept-one":
        from vitruvius.concept_enrichment import run_enrich_concept_one
        return _run(
            "enrich-concept-one",
            lambda: run_enrich_concept_one(
            concept_slug=args.concept_slug,
            force=args.force,
            ),
        )

    if args.command == "enrich-concepts":
        from vitruvius.concept_enrichment import run_enrich_concepts
        return _run(
            "enrich-concepts",
            lambda: run_enrich_concepts(force=args.force),
        )

    if args.command == "canonicalize":
        from vitruvius.canonicalize import run_canonicalize
        return _run("canonicalize", run_canonicalize)

    if args.command == "refine":
        from vitruvius.normalization.refine import run_refine
        return _run("refine", run_refine)

    if args.command == "run-with-review":
        return _run("run-with-review", run_pipeline_with_review)

    if args.command == "run-dataset-graph":
        from vitruvius.dataset_pipeline import (
            DatasetPipelineError,
            parse_structured_check,
            run_dataset_graph_pipeline,
        )
        try:
            structured_checks = [
                parse_structured_check(raw) for raw in (args.structured_check or [])
            ]
        except DatasetPipelineError as exc:
            print(json.dumps({"error": str(exc)}, indent=2))
            return 2
        return _run(
            "run-dataset-graph",
            lambda: run_dataset_graph_pipeline(
                dataset_manifest=args.dataset_manifest,
                structured_checks=structured_checks,
                export_owl=not args.skip_export_owl,
            ),
        )

    if args.command == "run-dataset-source-to-graph":
        from vitruvius.dataset_pipeline import (
            DatasetPipelineError,
            parse_structured_check,
            run_dataset_source_to_graph_pipeline,
        )
        try:
            structured_checks = [
                parse_structured_check(raw) for raw in (args.structured_check or [])
            ]
        except DatasetPipelineError as exc:
            print(json.dumps({"error": str(exc)}, indent=2))
            return 2
        return _run(
            "run-dataset-source-to-graph",
            lambda: run_dataset_source_to_graph_pipeline(
                dataset_manifest=args.dataset_manifest,
                structured_checks=structured_checks,
                export_owl=not args.skip_export_owl,
                dry_run=args.dry_run,
                review_model=args.review_model,
                review_timeout_seconds=args.review_timeout_seconds,
                review_parallelism=args.review_parallel,
                visualize_graph=args.visualize or args.open_browser,
                open_browser=args.open_browser,
                visualization_out_path=args.visualization_out,
            ),
        )

    if args.command == "run-laws-pilot":
        from vitruvius.dataset_pipeline import (
            DatasetPipelineError,
            parse_structured_check,
            run_dataset_source_to_graph_pipeline,
        )
        try:
            structured_checks = [
                parse_structured_check(raw) for raw in (args.structured_check or [])
            ]
        except DatasetPipelineError as exc:
            print(json.dumps({"error": str(exc)}, indent=2))
            return 2
        return _run(
            "run-laws-pilot",
            lambda: run_dataset_source_to_graph_pipeline(
                dataset_manifest="config/datasets/laws-core-bundle-m1.yaml",
                structured_checks=structured_checks,
                export_owl=not args.skip_export_owl,
                dry_run=args.dry_run,
                review_model=args.review_model,
                review_timeout_seconds=args.review_timeout_seconds,
                review_parallelism=args.review_parallel,
                visualize_graph=(not args.dry_run) or args.visualize or args.open_browser,
                open_browser=args.open_browser,
                visualization_out_path=args.visualization_out,
            ),
        )

    if args.command == "refine-one":
        from vitruvius.normalization.refine import run_refine_one
        return _run(
            "refine-one",
            lambda: run_refine_one(relative_markdown_path=args.relative_markdown_path),
        )

    if args.command == "rotate-registries":
        from vitruvius.registry_rotation import run_rotate_registries
        return _run(
            "rotate-registries",
            lambda: run_rotate_registries(keep=args.keep, dry_run=args.dry_run),
        )

    if args.command == "build-graph":
        from vitruvius.graph.cli import run_build_graph
        return _run(
            "build-graph",
            lambda: run_build_graph(
                dry_run=args.dry_run,
                dataset_manifest=args.dataset_manifest,
            ),
        )

    if args.command == "query-graph":
        from vitruvius.graph.cli import run_query_graph
        return _run(
            "query-graph",
            lambda: run_query_graph(
            from_id=args.from_id,
            to_id=args.to_id,
            max_depth=args.max_depth,
            snapshot_path=args.snapshot_path,
            ),
        )

    if args.command == "export-graph-snapshot":
        from vitruvius.graph.cli import run_export_graph_snapshot
        return _run(
            "export-graph-snapshot",
            lambda: run_export_graph_snapshot(
                fmt=args.fmt,
                snapshot_path=args.snapshot_path,
            ),
        )

    if args.command == "export-graph-owl":
        from vitruvius.ontology.cli import run_export_graph_owl
        return _run(
            "export-graph-owl",
            lambda: run_export_graph_owl(
                snapshot_path=args.snapshot_path,
                out_path=args.out_path,
            ),
        )

    if args.command == "visualize-graph":
        from vitruvius.graph.visualize import run_visualize_graph
        return _run(
            "visualize-graph",
            lambda: run_visualize_graph(
                snapshot_path=args.snapshot_path,
                out_path=args.out_path,
            ),
        )

    if args.command == "ingest-spatial":
        from vitruvius.spatial.cli import run_ingest_spatial
        return _run("ingest-spatial", run_ingest_spatial)

    if args.command == "evaluate-spatial":
        from vitruvius.spatial.cli import run_evaluate_spatial
        return _run(
            "evaluate-spatial",
            lambda: run_evaluate_spatial(
            concepts=args.concepts,
            observations_path=args.observations_path,
            rules_path=args.rules_path,
            ),
        )

    if args.command == "ple-cotrace-dump":
        from vitruvius.review.cot_audit import run_ple_cotrace_dump
        return _run(
            "ple-cotrace-dump",
            lambda: run_ple_cotrace_dump(cot_dir=Path(args.cot_dir)),
        )

    if args.command == "ple-registry-purge":
        from vitruvius.review.stateful_registry import run_ple_registry_purge
        return _run(
            "ple-registry-purge",
            lambda: run_ple_registry_purge(
            db_path=Path(args.registry_db),
            days=args.days,
            ),
        )

    if args.command == "ple-vision-probe":
        from vitruvius.parsers.vision_ocr import run_ple_vision_probe
        return _run(
            "ple-vision-probe",
            lambda: run_ple_vision_probe(
            required_free_gb=args.required_free_gb,
            model=args.model,
            ),
        )

    if args.command == "query":
        from vitruvius.query.cli import run_query
        return _run(
            "query",
            lambda: run_query(args.question, snapshot_path=args.snapshot_path),
        )

    if args.command == "query-structured":
        from vitruvius.query.cli import run_query_structured
        return _run(
            "query-structured",
            lambda: run_query_structured(
            function=args.function,
            subject=args.subject,
            a=args.a,
            b=args.b,
            snapshot_path=args.snapshot_path,
            ),
        )

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
