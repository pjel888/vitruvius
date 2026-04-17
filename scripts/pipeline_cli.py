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


def _add_review_model_args(parser: argparse.ArgumentParser) -> None:
    from vitruvius.config import get_ollama_8gb_safe_model, get_ollama_default_model

    parser.add_argument(
        "--review-model",
        default=None,
        help=(
            "Tier-1 review model override. When omitted, the CLI resolves the model from "
            f"--review-model-preset (default model: {get_ollama_default_model()}, "
            f"8GB-safe preset: {get_ollama_8gb_safe_model()})."
        ),
    )
    parser.add_argument(
        "--review-model-preset",
        choices=["default", "8gb-safe"],
        default="default",
        help="Named review-model preset to use when --review-model is not set.",
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
    dataset_source_to_graph_parser.add_argument("--review-model", default=None,
                                               help="Tier-1 review model for dataset-local review")
    dataset_source_to_graph_parser.add_argument("--review-timeout-seconds", type=int, default=None,
                                               help="Tier-1 review timeout seconds")
    dataset_source_to_graph_parser.add_argument("--review-parallel", type=int, default=None,
                                               help="Tier-1 review parallelism override")
    dataset_source_to_graph_parser.add_argument("--review-preset", default=None,
                                               help="Optional review preset (for example: m2-8gb-safe)")
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
    laws_pilot_parser.add_argument("--review-model", default=None,
                                   help="Tier-1 review model for dataset-local review")
    laws_pilot_parser.add_argument("--review-timeout-seconds", type=int, default=None,
                                   help="Tier-1 review timeout seconds")
    laws_pilot_parser.add_argument("--review-parallel", type=int, default=None,
                                   help="Tier-1 review parallelism override")
    laws_pilot_parser.add_argument("--review-preset", default=None,
                                   help="Optional review preset (for example: m2-8gb-safe)")
    laws_pilot_parser.add_argument("--visualize", action="store_true",
                                   help="Explicitly keep visualization enabled (default for non-dry-run pilot runs)")
    laws_pilot_parser.add_argument("--open-browser", action="store_true",
                                   help="Open the rendered HTML graph visualization in the default browser after a successful non-dry-run execution")
    laws_pilot_parser.add_argument("--visualization-out", default=None,
                                   help="Optional output HTML path for the post-run visualization")
    all_laws_dry_run_parser = add_command_parser(subparsers, "run-laws-all-dry-run")
    all_laws_dry_run_parser.add_argument("--review-model", default=None,
                                         help="Optional review model override for readiness planning")
    all_laws_dry_run_parser.add_argument("--review-parallel", type=int, default=None,
                                         help="Optional review parallelism override for readiness planning")
    all_laws_dry_run_parser.add_argument("--review-preset", default=None,
                                         help="Optional review preset (for example: m2-8gb-safe)")
    tranche_dry_run_parser = add_command_parser(subparsers, "run-laws-tranche-dry-run")
    tranche_dry_run_parser.add_argument("--tranche-manifest", default="config/datasets/laws-tranche-1.yaml",
                                        help="Scoped tranche manifest to inspect without widening into execute mode")
    tranche_dry_run_parser.add_argument("--review-model", default=None,
                                        help="Optional review model override for tranche planning")
    tranche_dry_run_parser.add_argument("--review-timeout-seconds", type=int, default=None,
                                        help="Optional review timeout override for tranche planning")
    tranche_dry_run_parser.add_argument("--review-parallel", type=int, default=None,
                                        help="Optional review parallelism override for tranche planning")
    tranche_dry_run_parser.add_argument("--review-preset", default=None,
                                        help="Optional review preset (for example: m2-8gb-safe)")
    laws_duplicate_parser = add_command_parser(subparsers, "run-laws-duplicate-dry-run")
    laws_duplicate_parser.add_argument("--tranche-manifest", default=None,
                                       help="Optional tranche manifest to restrict duplicate reporting to a bounded slice")
    tranche_source_prep_parser = add_command_parser(subparsers, "run-laws-tranche-source-prep-dry-run")
    tranche_source_prep_parser.add_argument("--tranche-manifest", default="config/datasets/laws-tranche-1.yaml",
                                            help="Tranche manifest whose raw inputs should be inventoried for source preparation")
    tranche_source_prep_parser.add_argument("--sample-pages", type=int, default=5,
                                            help="Sample pages for per-PDF detection planning (default: 5)")
    tranche_source_prep_exec_parser = add_command_parser(subparsers, "run-laws-tranche-source-prep")
    tranche_source_prep_exec_parser.add_argument("--tranche-manifest", default="config/datasets/laws-tranche-1.yaml",
                                                 help="Tranche manifest whose raw inputs should be prepared into conversion/refinement outputs")
    tranche_source_prep_exec_parser.add_argument("--sample-pages", type=int, default=5,
                                                 help="Sample pages for per-PDF route detection (default: 5)")
    tranche_source_prep_exec_parser.add_argument("--allow-ocr", action="store_true",
                                                 help="When set, run OCR-first preparation for tranche PDFs that require OCR instead of only reporting them as blocked")
    tranche_source_admission_parser = add_command_parser(subparsers, "run-laws-tranche-source-admission-dry-run")
    tranche_source_admission_parser.add_argument("--tranche-manifest", default="config/datasets/laws-tranche-1.yaml",
                                                 help="Tranche manifest whose prepared outputs should be classified into ready-vs-blocked source admission state")
    tranche_source_admission_parser.add_argument("--source-prep-report", default=None,
                                                 help="Optional explicit tranche source-prep execute report to classify for source admission")
    tranche_source_admission_exec_parser = add_command_parser(subparsers, "run-laws-tranche-source-admission")
    tranche_source_admission_exec_parser.add_argument("--tranche-manifest", default="config/datasets/laws-tranche-1.yaml",
                                                      help="Tranche manifest whose selected prepared outputs should be admitted into canonical source pages")
    tranche_source_admission_exec_parser.add_argument("--source-prep-report", default=None,
                                                      help="Optional explicit tranche source-prep execute report to use during source admission")
    tranche_source_to_graph_dry_run_parser = add_command_parser(subparsers, "run-laws-tranche-source-to-graph-dry-run")
    tranche_source_to_graph_dry_run_parser.add_argument("--tranche-manifest", default="config/datasets/laws-tranche-1.yaml",
                                                        help="Tranche manifest whose admitted source state should be staged through the bounded source-to-graph dry-run")
    tranche_source_to_graph_dry_run_parser.add_argument("--review-preset", default=None,
                                                        help="Optional review preset override for the staged source-to-graph dry-run")
    tranche_source_to_graph_exec_parser = add_command_parser(subparsers, "run-laws-tranche-source-to-graph")
    tranche_source_to_graph_exec_parser.add_argument("--tranche-manifest", default="config/datasets/laws-tranche-1.yaml",
                                                     help="Tranche manifest whose admitted source state should be staged through the bounded source-to-graph execute wrapper")
    tranche_source_to_graph_exec_parser.add_argument("--review-preset", default=None,
                                                     help="Optional review preset override for the staged source-to-graph execute wrapper")
    aggregate_manifest_parser = add_command_parser(subparsers, "build-laws-completed-aggregate-manifest")
    aggregate_manifest_parser.add_argument("--out", default="config/datasets/laws-completed-aggregate.yaml",
                                          help="Output path for the generated completed-laws aggregate manifest")
    aggregate_run_parser = add_command_parser(subparsers, "run-laws-completed-aggregate")
    aggregate_run_parser.add_argument("--dry-run", action="store_true",
                                     help="Validate/plans stages without executing graph writes")
    aggregate_run_parser.add_argument("--review-model", default=None,
                                     help="Tier-1 review model for aggregate review")
    aggregate_run_parser.add_argument("--review-timeout-seconds", type=int, default=None,
                                     help="Tier-1 review timeout seconds")
    aggregate_run_parser.add_argument("--review-parallel", type=int, default=None,
                                     help="Tier-1 review parallelism override")
    aggregate_run_parser.add_argument("--review-preset", default=None,
                                     help="Optional review preset (for example: m2-8gb-safe)")
    aggregate_run_parser.add_argument("--skip-export-owl", action="store_true",
                                     help="Skip dataset-local OWL/Turtle export")
    generic_aggregate_manifest_parser = add_command_parser(subparsers, "build-completed-aggregate-manifest")
    generic_aggregate_manifest_parser.add_argument("--completed-ledger", required=True,
                                                  help="Completed-lanes ledger YAML path")
    generic_aggregate_manifest_parser.add_argument("--manifest-index", required=True,
                                                  help="Manifest index YAML path")
    generic_aggregate_manifest_parser.add_argument("--dataset-id", required=True)
    generic_aggregate_manifest_parser.add_argument("--dataset-kind", default="aggregate")
    generic_aggregate_manifest_parser.add_argument("--out", required=True,
                                                  help="Output dataset manifest path")
    generic_aggregate_manifest_parser.add_argument("--graph-output-root", required=True)
    generic_aggregate_manifest_parser.add_argument("--run-output-root", required=True)
    generic_aggregate_manifest_parser.add_argument("--query-snapshot-template", required=True)
    generic_aggregate_profile_build_parser = add_command_parser(subparsers, "build-completed-aggregate-from-profile")
    generic_aggregate_profile_build_parser.add_argument("--profile", required=True,
                                                       help="Aggregate profile YAML path")
    generic_aggregate_register_parser = add_command_parser(subparsers, "register-completed-aggregate-family")
    generic_aggregate_register_parser.add_argument("--family", required=True)
    generic_aggregate_register_parser.add_argument("--profile", required=True,
                                                  help="Profile YAML path to create or update")
    generic_aggregate_register_parser.add_argument("--catalog", default="config/datasets/dataset-mvp-profile-catalog.yaml",
                                                  help="Profile catalog YAML path")
    generic_aggregate_register_parser.add_argument("--dataset-id", required=True)
    generic_aggregate_register_parser.add_argument("--dataset-kind", default="aggregate")
    generic_aggregate_register_parser.add_argument("--completed-ledger", required=True)
    generic_aggregate_register_parser.add_argument("--manifest-index", required=True)
    generic_aggregate_register_parser.add_argument("--out-manifest", required=True)
    generic_aggregate_register_parser.add_argument("--graph-output-root", required=True)
    generic_aggregate_register_parser.add_argument("--run-output-root", required=True)
    generic_aggregate_register_parser.add_argument("--query-snapshot-template", required=True)
    generic_aggregate_register_parser.add_argument("--scope-note", action="append", default=[])
    generic_aggregate_register_parser.add_argument("--lane-note-template", default=None)
    generic_aggregate_register_parser.add_argument("--status", default="ready")
    generic_aggregate_register_parser.add_argument("--note", default=None)
    generic_aggregate_scaffold_parser = add_command_parser(subparsers, "scaffold-completed-aggregate-family")
    generic_aggregate_scaffold_parser.add_argument("--family", required=True)
    generic_aggregate_scaffold_parser.add_argument("--catalog", default="config/datasets/dataset-mvp-profile-catalog.yaml",
                                                  help="Profile catalog YAML path")
    generic_aggregate_scaffold_parser.add_argument("--dataset-id", default=None)
    generic_aggregate_scaffold_parser.add_argument("--dataset-kind", default="aggregate")
    generic_aggregate_scaffold_parser.add_argument("--profile", default=None)
    generic_aggregate_scaffold_parser.add_argument("--completed-ledger", default=None)
    generic_aggregate_scaffold_parser.add_argument("--manifest-index", default=None)
    generic_aggregate_scaffold_parser.add_argument("--out-manifest", default=None)
    generic_aggregate_scaffold_parser.add_argument("--graph-output-root", default=None)
    generic_aggregate_scaffold_parser.add_argument("--run-output-root", default=None)
    generic_aggregate_scaffold_parser.add_argument("--query-snapshot-template", default=None)
    generic_aggregate_scaffold_parser.add_argument("--scope-note", action="append", default=[])
    generic_aggregate_scaffold_parser.add_argument("--lane-note-template", default=None)
    generic_aggregate_scaffold_parser.add_argument("--status", default="scaffolded")
    generic_aggregate_scaffold_parser.add_argument("--note", default=None)
    generic_aggregate_admit_parser = add_command_parser(subparsers, "admit-completed-aggregate-manifest")
    generic_aggregate_admit_parser.add_argument("--family", required=True)
    generic_aggregate_admit_parser.add_argument("--catalog", default="config/datasets/dataset-mvp-profile-catalog.yaml",
                                               help="Profile catalog YAML path")
    generic_aggregate_admit_parser.add_argument("--lane-id", required=True)
    generic_aggregate_admit_parser.add_argument("--manifest", required=True,
                                               help="Completed manifest YAML path to admit into the family ledgers")
    generic_aggregate_check_parser = add_command_parser(subparsers, "check-completed-aggregate-family")
    generic_aggregate_check_parser.add_argument("--family", required=True)
    generic_aggregate_check_parser.add_argument("--catalog", default="config/datasets/dataset-mvp-profile-catalog.yaml",
                                               help="Profile catalog YAML path")
    generic_aggregate_lane_scaffold_parser = add_command_parser(subparsers, "scaffold-completed-aggregate-lane-manifest")
    generic_aggregate_lane_scaffold_parser.add_argument("--family", required=True)
    generic_aggregate_lane_scaffold_parser.add_argument("--catalog", default="config/datasets/dataset-mvp-profile-catalog.yaml",
                                                       help="Profile catalog YAML path")
    generic_aggregate_lane_scaffold_parser.add_argument("--lane-id", required=True)
    generic_aggregate_lane_scaffold_parser.add_argument("--raw-root", required=True,
                                                       help="Repo-relative raw root directory to inventory")
    generic_aggregate_lane_scaffold_parser.add_argument("--out-manifest", default=None)
    generic_aggregate_lane_scaffold_parser.add_argument("--max-files", type=int, default=5)
    generic_aggregate_lane_scaffold_parser.add_argument("--extension", action="append", default=[],
                                                       help="Allowed file extension (repeatable). Defaults to supported direct-input extensions")
    generic_aggregate_lane_scaffold_parser.add_argument("--raw-path", action="append", default=[],
                                                       help="Explicit repo-relative raw file path to include (repeatable)")
    generic_aggregate_lane_inspect_parser = add_command_parser(subparsers, "inspect-completed-aggregate-lane-sources")
    generic_aggregate_lane_inspect_parser.add_argument("--manifest", required=True)
    generic_aggregate_lane_inspect_parser.add_argument("--sample-pages", type=int, default=5)
    generic_aggregate_lane_prep_parser = add_command_parser(subparsers, "prepare-completed-aggregate-lane-sources")
    generic_aggregate_lane_prep_parser.add_argument("--manifest", required=True)
    generic_aggregate_lane_prep_parser.add_argument("--sample-pages", type=int, default=5)
    generic_aggregate_lane_prep_parser.add_argument("--allow-ocr", action="store_true")
    generic_aggregate_lane_prep_parser.add_argument("--dry-run", action="store_true")
    generic_aggregate_lane_admission_parser = add_command_parser(subparsers, "source-admit-completed-aggregate-lane-dry-run")
    generic_aggregate_lane_admission_parser.add_argument("--manifest", required=True)
    generic_aggregate_lane_admission_parser.add_argument("--source-prep-report", default=None)
    generic_aggregate_lane_admission_exec_parser = add_command_parser(subparsers, "source-admit-completed-aggregate-lane")
    generic_aggregate_lane_admission_exec_parser.add_argument("--manifest", required=True)
    generic_aggregate_lane_admission_exec_parser.add_argument("--source-prep-report", default=None)
    generic_aggregate_lane_rule_scaffold_parser = add_command_parser(subparsers, "scaffold-completed-aggregate-lane-canonical-rules")
    generic_aggregate_lane_rule_scaffold_parser.add_argument("--manifest", required=True)
    generic_aggregate_lane_rule_scaffold_parser.add_argument("--source-type", required=True)
    generic_aggregate_lane_rule_scaffold_parser.add_argument("--trust-level", required=True)
    generic_aggregate_lane_rule_scaffold_parser.add_argument("--output-rules", default=None)
    generic_aggregate_lane_rule_scaffold_parser.add_argument("--core-concept", action="append", default=[])
    generic_aggregate_lane_concept_scaffold_parser = add_command_parser(subparsers, "scaffold-completed-aggregate-lane-concepts")
    generic_aggregate_lane_concept_scaffold_parser.add_argument("--manifest", required=True)
    generic_aggregate_lane_concept_scaffold_parser.add_argument("--output-dir", default=None)
    generic_aggregate_lane_relationship_scaffold_parser = add_command_parser(subparsers, "scaffold-completed-aggregate-lane-relationships")
    generic_aggregate_lane_relationship_scaffold_parser.add_argument("--manifest", required=True)
    generic_aggregate_lane_relationship_scaffold_parser.add_argument("--predicate", default="covers")
    generic_aggregate_lane_relationship_scaffold_parser.add_argument("--output-dir", default=None)
    generic_aggregate_lane_relationship_promote_parser = add_command_parser(subparsers, "promote-completed-aggregate-lane-relationships")
    generic_aggregate_lane_relationship_promote_parser.add_argument("--manifest", required=True)
    generic_aggregate_lane_bootstrap_parser = add_command_parser(subparsers, "bootstrap-completed-aggregate-family-lane")
    generic_aggregate_lane_bootstrap_parser.add_argument("--family", required=True)
    generic_aggregate_lane_bootstrap_parser.add_argument("--lane-id", required=True)
    generic_aggregate_lane_bootstrap_parser.add_argument("--raw-root", required=True)
    generic_aggregate_lane_bootstrap_parser.add_argument("--catalog", default="config/datasets/dataset-mvp-profile-catalog.yaml")
    generic_aggregate_lane_bootstrap_parser.add_argument("--dataset-kind", default="aggregate")
    generic_aggregate_lane_bootstrap_parser.add_argument("--source-type", required=True)
    generic_aggregate_lane_bootstrap_parser.add_argument("--trust-level", required=True)
    generic_aggregate_lane_bootstrap_parser.add_argument("--core-concept", action="append", default=[])
    generic_aggregate_lane_bootstrap_parser.add_argument("--predicate", default="covers")
    generic_aggregate_lane_bootstrap_parser.add_argument("--family-note", default=None)
    generic_aggregate_lane_bootstrap_parser.add_argument("--max-files", type=int, default=5)
    generic_aggregate_lane_bootstrap_parser.add_argument("--extension", action="append", default=[])
    generic_aggregate_lane_bootstrap_parser.add_argument("--raw-path", action="append", default=[])
    generic_aggregate_lane_bootstrap_parser.add_argument("--sample-pages", type=int, default=5)
    generic_aggregate_lane_bootstrap_parser.add_argument("--allow-ocr", action="store_true")
    generic_aggregate_catalog_run_parser = add_command_parser(subparsers, "run-completed-aggregate-family")
    generic_aggregate_catalog_run_parser.add_argument("--family", required=True,
                                                     help="Registered dataset family name from the profile catalog")
    generic_aggregate_catalog_run_parser.add_argument("--catalog", default="config/datasets/dataset-mvp-profile-catalog.yaml",
                                                     help="Profile catalog YAML path")
    generic_aggregate_catalog_run_parser.add_argument("--dry-run", action="store_true")
    generic_aggregate_catalog_run_parser.add_argument("--review-model", default=None)
    generic_aggregate_catalog_run_parser.add_argument("--review-timeout-seconds", type=int, default=None)
    generic_aggregate_catalog_run_parser.add_argument("--review-parallel", type=int, default=None)
    generic_aggregate_catalog_run_parser.add_argument("--review-preset", default=None)
    generic_aggregate_catalog_run_parser.add_argument("--skip-export-owl", action="store_true")
    generic_aggregate_run_parser = add_command_parser(subparsers, "run-completed-aggregate")
    generic_aggregate_run_parser.add_argument("--completed-ledger", required=True)
    generic_aggregate_run_parser.add_argument("--manifest-index", required=True)
    generic_aggregate_run_parser.add_argument("--dataset-id", required=True)
    generic_aggregate_run_parser.add_argument("--dataset-kind", default="aggregate")
    generic_aggregate_run_parser.add_argument("--out", required=True)
    generic_aggregate_run_parser.add_argument("--graph-output-root", required=True)
    generic_aggregate_run_parser.add_argument("--run-output-root", required=True)
    generic_aggregate_run_parser.add_argument("--query-snapshot-template", required=True)
    generic_aggregate_run_parser.add_argument("--dry-run", action="store_true")
    generic_aggregate_run_parser.add_argument("--review-model", default=None)
    generic_aggregate_run_parser.add_argument("--review-timeout-seconds", type=int, default=None)
    generic_aggregate_run_parser.add_argument("--review-parallel", type=int, default=None)
    generic_aggregate_run_parser.add_argument("--review-preset", default=None)
    generic_aggregate_run_parser.add_argument("--skip-export-owl", action="store_true")
    generic_aggregate_profile_run_parser = add_command_parser(subparsers, "run-completed-aggregate-from-profile")
    generic_aggregate_profile_run_parser.add_argument("--profile", required=True,
                                                     help="Aggregate profile YAML path")
    generic_aggregate_profile_run_parser.add_argument("--dry-run", action="store_true")
    generic_aggregate_profile_run_parser.add_argument("--review-model", default=None)
    generic_aggregate_profile_run_parser.add_argument("--review-timeout-seconds", type=int, default=None)
    generic_aggregate_profile_run_parser.add_argument("--review-parallel", type=int, default=None)
    generic_aggregate_profile_run_parser.add_argument("--review-preset", default=None)
    generic_aggregate_profile_run_parser.add_argument("--skip-export-owl", action="store_true")
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
                review_preset=args.review_preset,
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
                review_preset=args.review_preset,
                visualize_graph=(not args.dry_run) or args.visualize or args.open_browser,
                open_browser=args.open_browser,
                visualization_out_path=args.visualization_out,
            ),
        )

    if args.command == "run-laws-all-dry-run":
        from vitruvius.laws_readiness import run_all_laws_dry_run
        return _run(
            "run-laws-all-dry-run",
            lambda: run_all_laws_dry_run(
                pilot_manifest="config/datasets/laws-core-bundle-m1.yaml",
                review_model=args.review_model,
                review_model_preset=args.review_preset,
            ),
        )

    if args.command == "run-laws-tranche-dry-run":
        from vitruvius.laws_readiness import run_laws_tranche_dry_run
        return _run(
            "run-laws-tranche-dry-run",
            lambda: run_laws_tranche_dry_run(
                tranche_manifest=args.tranche_manifest,
                pilot_manifest="config/datasets/laws-core-bundle-m1.yaml",
                review_model=args.review_model,
                review_model_preset=args.review_preset,
            ),
        )

    if args.command == "run-laws-duplicate-dry-run":
        from vitruvius.laws_readiness import run_laws_duplicate_dry_run
        return _run(
            "run-laws-duplicate-dry-run",
            lambda: run_laws_duplicate_dry_run(
                tranche_manifest=args.tranche_manifest,
            ),
        )

    if args.command == "run-laws-tranche-source-prep-dry-run":
        from vitruvius.laws_readiness import run_laws_tranche_source_prep_dry_run
        return _run(
            "run-laws-tranche-source-prep-dry-run",
            lambda: run_laws_tranche_source_prep_dry_run(
                tranche_manifest=args.tranche_manifest,
                sample_pages=args.sample_pages,
            ),
        )

    if args.command == "run-laws-tranche-source-prep":
        from vitruvius.laws_readiness import run_laws_tranche_source_prep
        return _run(
            "run-laws-tranche-source-prep",
            lambda: run_laws_tranche_source_prep(
                tranche_manifest=args.tranche_manifest,
                sample_pages=args.sample_pages,
                allow_ocr=args.allow_ocr,
            ),
        )

    if args.command == "run-laws-tranche-source-admission-dry-run":
        from vitruvius.laws_readiness import run_laws_tranche_source_admission_dry_run
        return _run(
            "run-laws-tranche-source-admission-dry-run",
            lambda: run_laws_tranche_source_admission_dry_run(
                tranche_manifest=args.tranche_manifest,
                source_prep_report=args.source_prep_report,
            ),
        )

    if args.command == "run-laws-tranche-source-admission":
        from vitruvius.laws_readiness import run_laws_tranche_source_admission
        return _run(
            "run-laws-tranche-source-admission",
            lambda: run_laws_tranche_source_admission(
                tranche_manifest=args.tranche_manifest,
                source_prep_report=args.source_prep_report,
            ),
        )

    if args.command == "run-laws-tranche-source-to-graph-dry-run":
        from vitruvius.laws_readiness import run_laws_tranche_source_to_graph_dry_run
        return _run(
            "run-laws-tranche-source-to-graph-dry-run",
            lambda: run_laws_tranche_source_to_graph_dry_run(
                tranche_manifest=args.tranche_manifest,
                review_preset=args.review_preset,
            ),
        )

    if args.command == "run-laws-tranche-source-to-graph":
        from vitruvius.laws_readiness import run_laws_tranche_source_to_graph
        return _run(
            "run-laws-tranche-source-to-graph",
            lambda: run_laws_tranche_source_to_graph(
                tranche_manifest=args.tranche_manifest,
                review_preset=args.review_preset,
            ),
        )

    if args.command == "build-completed-aggregate-manifest":
        from vitruvius.aggregate_manifest import build_generic_completed_aggregate_manifest, print_aggregate_manifest_summary
        def _run_generic():
            repo_root = Path.cwd().resolve()
            completed_ledger_path = Path(args.completed_ledger)
            if not completed_ledger_path.is_absolute():
                completed_ledger_path = repo_root / completed_ledger_path
            manifest_index_path = Path(args.manifest_index)
            if not manifest_index_path.is_absolute():
                manifest_index_path = repo_root / manifest_index_path
            out_manifest_path = Path(args.out)
            if not out_manifest_path.is_absolute():
                out_manifest_path = repo_root / out_manifest_path
            aggregate_payload = build_generic_completed_aggregate_manifest(
                repo_root=repo_root,
                completed_ledger_path=completed_ledger_path,
                manifest_index_path=manifest_index_path,
                out_manifest_path=out_manifest_path,
                dataset_id=args.dataset_id,
                dataset_kind=args.dataset_kind,
                graph_output_root=args.graph_output_root,
                run_output_root=args.run_output_root,
                query_snapshot_path_template=args.query_snapshot_template,
                scope_notes=[f"Aggregate graph input for completed lanes from {completed_ledger_path.name}."],
                lane_note_builder=lambda lane_id: f"Aggregate lane: {lane_id}",
                folder_name_resolver=lambda item: str(item.get('raw_folder_name') or item.get('folder_name') or ''),
            )
            print_aggregate_manifest_summary(
                repo_root=repo_root,
                out_manifest_path=out_manifest_path,
                aggregate_payload=aggregate_payload,
            )
            return 0
        return _run("build-completed-aggregate-manifest", _run_generic)

    if args.command == "build-completed-aggregate-from-profile":
        from vitruvius.aggregate_manifest import (
            build_generic_completed_aggregate_manifest_from_profile,
            print_aggregate_manifest_summary,
        )
        def _run_generic_from_profile():
            repo_root = Path.cwd().resolve()
            out_manifest_path, aggregate_payload, _profile = build_generic_completed_aggregate_manifest_from_profile(
                repo_root=repo_root,
                profile_path=Path(args.profile),
            )
            print_aggregate_manifest_summary(
                repo_root=repo_root,
                out_manifest_path=out_manifest_path,
                aggregate_payload=aggregate_payload,
            )
            return 0
        return _run("build-completed-aggregate-from-profile", _run_generic_from_profile)

    if args.command == "register-completed-aggregate-family":
        from vitruvius.aggregate_manifest import register_completed_aggregate_family
        def _run_register_generic_family():
            repo_root = Path.cwd().resolve()
            resolved_profile_path, resolved_catalog_path, profile_payload, catalog_entry = register_completed_aggregate_family(
                repo_root=repo_root,
                family=args.family,
                profile_path=Path(args.profile),
                catalog_path=Path(args.catalog),
                dataset_id=args.dataset_id,
                dataset_kind=args.dataset_kind,
                completed_ledger=args.completed_ledger,
                manifest_index=args.manifest_index,
                out_manifest=args.out_manifest,
                graph_output_root=args.graph_output_root,
                run_output_root=args.run_output_root,
                query_snapshot_template=args.query_snapshot_template,
                scope_notes=list(args.scope_note or []),
                lane_note_template=args.lane_note_template,
                status=args.status,
                note=args.note,
            )
            print(json.dumps({
                "action": "register-completed-aggregate-family",
                "family": args.family,
                "profile_path": str(resolved_profile_path.relative_to(repo_root)),
                "catalog_path": str(resolved_catalog_path.relative_to(repo_root)),
                "dataset_id": profile_payload["dataset_id"],
                "dataset_kind": profile_payload["dataset_kind"],
                "catalog_entry": catalog_entry,
            }, indent=2))
            return 0
        return _run("register-completed-aggregate-family", _run_register_generic_family)

    if args.command == "scaffold-completed-aggregate-family":
        from vitruvius.aggregate_manifest import scaffold_completed_aggregate_family
        def _run_scaffold_generic_family():
            repo_root = Path.cwd().resolve()
            scaffold_result = scaffold_completed_aggregate_family(
                repo_root=repo_root,
                family=args.family,
                catalog_path=Path(args.catalog),
                dataset_id=args.dataset_id,
                dataset_kind=args.dataset_kind,
                profile_path=Path(args.profile) if args.profile else None,
                completed_ledger_path=Path(args.completed_ledger) if args.completed_ledger else None,
                manifest_index_path=Path(args.manifest_index) if args.manifest_index else None,
                out_manifest=args.out_manifest,
                graph_output_root=args.graph_output_root,
                run_output_root=args.run_output_root,
                query_snapshot_template=args.query_snapshot_template,
                scope_notes=list(args.scope_note or []),
                lane_note_template=args.lane_note_template,
                status=args.status,
                note=args.note,
            )
            print(json.dumps({
                "action": "scaffold-completed-aggregate-family",
                "family": args.family,
                "profile_path": str(scaffold_result["profile_path"].relative_to(repo_root)),
                "catalog_path": str(scaffold_result["catalog_path"].relative_to(repo_root)),
                "completed_ledger_path": str(scaffold_result["completed_ledger_path"].relative_to(repo_root)),
                "manifest_index_path": str(scaffold_result["manifest_index_path"].relative_to(repo_root)),
                "dataset_id": scaffold_result["profile_payload"]["dataset_id"],
                "dataset_kind": scaffold_result["profile_payload"]["dataset_kind"],
                "catalog_entry": scaffold_result["catalog_entry"],
            }, indent=2))
            return 0
        return _run("scaffold-completed-aggregate-family", _run_scaffold_generic_family)

    if args.command == "admit-completed-aggregate-manifest":
        from vitruvius.aggregate_manifest import admit_completed_manifest_to_family
        def _run_admit_generic_manifest():
            repo_root = Path.cwd().resolve()
            result = admit_completed_manifest_to_family(
                repo_root=repo_root,
                family=args.family,
                catalog_path=Path(args.catalog),
                lane_id=args.lane_id,
                manifest_path=Path(args.manifest),
            )
            print(json.dumps({
                "action": "admit-completed-aggregate-manifest",
                "family": args.family,
                "lane_id": result["lane_id"],
                "manifest_path": str(result["manifest_path"].relative_to(repo_root)),
                "completed_ledger_path": str(result["completed_ledger_path"].relative_to(repo_root)),
                "manifest_index_path": str(result["manifest_index_path"].relative_to(repo_root)),
            }, indent=2))
            return 0
        return _run("admit-completed-aggregate-manifest", _run_admit_generic_manifest)

    if args.command == "check-completed-aggregate-family":
        from vitruvius.aggregate_manifest import check_completed_aggregate_family_readiness
        def _run_check_generic_family():
            repo_root = Path.cwd().resolve()
            readiness = check_completed_aggregate_family_readiness(
                repo_root=repo_root,
                family=args.family,
                catalog_path=Path(args.catalog),
            )
            print(json.dumps({
                "action": "check-completed-aggregate-family",
                **readiness,
            }, indent=2))
            return 0
        return _run("check-completed-aggregate-family", _run_check_generic_family)

    if args.command == "scaffold-completed-aggregate-lane-manifest":
        from vitruvius.aggregate_manifest import scaffold_completed_aggregate_lane_manifest
        def _run_scaffold_generic_lane():
            repo_root = Path.cwd().resolve()
            result = scaffold_completed_aggregate_lane_manifest(
                repo_root=repo_root,
                family=args.family,
                catalog_path=Path(args.catalog),
                lane_id=args.lane_id,
                raw_root=Path(args.raw_root),
                out_manifest_path=Path(args.out_manifest) if args.out_manifest else None,
                max_files=args.max_files,
                extensions=list(args.extension or []),
                raw_paths=[Path(path) for path in (args.raw_path or [])],
            )
            print(json.dumps({
                "action": "scaffold-completed-aggregate-lane-manifest",
                "family": args.family,
                "lane_id": result["lane_id"],
                "raw_root": str(result["raw_root"].relative_to(repo_root)),
                "out_manifest_path": str(result["out_manifest_path"].relative_to(repo_root)),
                "selected_file_count": len(result["selected_files"]),
                "selected_files": [str(path.relative_to(repo_root)) for path in result["selected_files"]],
            }, indent=2))
            return 0
        return _run("scaffold-completed-aggregate-lane-manifest", _run_scaffold_generic_lane)

    if args.command == "inspect-completed-aggregate-lane-sources":
        from vitruvius.aggregate_manifest import inspect_completed_aggregate_lane_sources
        def _run_inspect_generic_lane():
            repo_root = Path.cwd().resolve()
            inspection = inspect_completed_aggregate_lane_sources(
                repo_root=repo_root,
                manifest_path=Path(args.manifest),
                sample_pages=args.sample_pages,
            )
            print(json.dumps({
                "action": "inspect-completed-aggregate-lane-sources",
                **inspection,
            }, indent=2))
            return 0
        return _run("inspect-completed-aggregate-lane-sources", _run_inspect_generic_lane)

    if args.command == "prepare-completed-aggregate-lane-sources":
        from vitruvius.aggregate_manifest import prepare_completed_aggregate_lane_sources
        def _run_prepare_generic_lane():
            repo_root = Path.cwd().resolve()
            summary = prepare_completed_aggregate_lane_sources(
                repo_root=repo_root,
                manifest_path=Path(args.manifest),
                sample_pages=args.sample_pages,
                allow_ocr=args.allow_ocr,
                dry_run=args.dry_run,
            )
            print(json.dumps(summary, indent=2))
            return 0
        return _run("prepare-completed-aggregate-lane-sources", _run_prepare_generic_lane)

    if args.command == "source-admit-completed-aggregate-lane-dry-run":
        from vitruvius.aggregate_manifest import source_admit_completed_aggregate_lane_dry_run
        def _run_source_admit_generic_lane():
            repo_root = Path.cwd().resolve()
            summary = source_admit_completed_aggregate_lane_dry_run(
                repo_root=repo_root,
                manifest_path=Path(args.manifest),
                source_prep_report_path=Path(args.source_prep_report) if args.source_prep_report else None,
            )
            print(json.dumps(summary, indent=2))
            return 0
        return _run("source-admit-completed-aggregate-lane-dry-run", _run_source_admit_generic_lane)

    if args.command == "source-admit-completed-aggregate-lane":
        from vitruvius.aggregate_manifest import source_admit_completed_aggregate_lane_execute
        def _run_source_admit_generic_lane_execute():
            repo_root = Path.cwd().resolve()
            summary = source_admit_completed_aggregate_lane_execute(
                repo_root=repo_root,
                manifest_path=Path(args.manifest),
                source_prep_report_path=Path(args.source_prep_report) if args.source_prep_report else None,
            )
            print(json.dumps(summary, indent=2))
            return 0
        return _run("source-admit-completed-aggregate-lane", _run_source_admit_generic_lane_execute)

    if args.command == "scaffold-completed-aggregate-lane-canonical-rules":
        from vitruvius.aggregate_manifest import scaffold_completed_aggregate_lane_canonical_rules
        def _run_scaffold_generic_lane_rules():
            repo_root = Path.cwd().resolve()
            summary = scaffold_completed_aggregate_lane_canonical_rules(
                repo_root=repo_root,
                manifest_path=Path(args.manifest),
                source_type=args.source_type,
                trust_level=args.trust_level,
                output_rules_path=Path(args.output_rules) if args.output_rules else None,
                core_concepts=list(args.core_concept or []),
            )
            print(json.dumps({
                "action": "scaffold-completed-aggregate-lane-canonical-rules",
                **summary,
            }, indent=2))
            return 0
        return _run("scaffold-completed-aggregate-lane-canonical-rules", _run_scaffold_generic_lane_rules)

    if args.command == "scaffold-completed-aggregate-lane-concepts":
        from vitruvius.aggregate_manifest import scaffold_completed_aggregate_lane_concepts
        def _run_scaffold_generic_lane_concepts():
            repo_root = Path.cwd().resolve()
            summary = scaffold_completed_aggregate_lane_concepts(
                repo_root=repo_root,
                manifest_path=Path(args.manifest),
                output_dir=Path(args.output_dir) if args.output_dir else None,
            )
            print(json.dumps({
                "action": "scaffold-completed-aggregate-lane-concepts",
                **summary,
            }, indent=2))
            return 0
        return _run("scaffold-completed-aggregate-lane-concepts", _run_scaffold_generic_lane_concepts)

    if args.command == "scaffold-completed-aggregate-lane-relationships":
        from vitruvius.aggregate_manifest import scaffold_completed_aggregate_lane_relationships
        def _run_scaffold_generic_lane_relationships():
            repo_root = Path.cwd().resolve()
            summary = scaffold_completed_aggregate_lane_relationships(
                repo_root=repo_root,
                manifest_path=Path(args.manifest),
                predicate=args.predicate,
                output_dir=Path(args.output_dir) if args.output_dir else None,
            )
            print(json.dumps({
                "action": "scaffold-completed-aggregate-lane-relationships",
                **summary,
            }, indent=2))
            return 0
        return _run("scaffold-completed-aggregate-lane-relationships", _run_scaffold_generic_lane_relationships)

    if args.command == "promote-completed-aggregate-lane-relationships":
        from vitruvius.aggregate_manifest import promote_completed_aggregate_lane_relationships
        def _run_promote_generic_lane_relationships():
            repo_root = Path.cwd().resolve()
            summary = promote_completed_aggregate_lane_relationships(
                repo_root=repo_root,
                manifest_path=Path(args.manifest),
            )
            print(json.dumps({
                "action": "promote-completed-aggregate-lane-relationships",
                **summary,
            }, indent=2))
            return 0
        return _run("promote-completed-aggregate-lane-relationships", _run_promote_generic_lane_relationships)

    if args.command == "bootstrap-completed-aggregate-family-lane":
        from vitruvius.aggregate_manifest import bootstrap_completed_aggregate_family_lane
        def _run_bootstrap_generic_family_lane():
            repo_root = Path.cwd().resolve()
            summary = bootstrap_completed_aggregate_family_lane(
                repo_root=repo_root,
                family=args.family,
                lane_id=args.lane_id,
                raw_root=Path(args.raw_root),
                dataset_kind=args.dataset_kind,
                catalog_path=Path(args.catalog),
                source_type=args.source_type,
                trust_level=args.trust_level,
                core_concepts=list(args.core_concept or []),
                predicate=args.predicate,
                family_note=args.family_note,
                max_files=args.max_files,
                extensions=list(args.extension or []),
                raw_paths=[Path(path) for path in (args.raw_path or [])],
                sample_pages=args.sample_pages,
                allow_ocr=args.allow_ocr,
            )
            print(json.dumps({
                "action": "bootstrap-completed-aggregate-family-lane",
                **summary,
            }, indent=2))
            return 0
        return _run("bootstrap-completed-aggregate-family-lane", _run_bootstrap_generic_family_lane)

    if args.command == "run-completed-aggregate":
        from vitruvius.aggregate_manifest import build_generic_completed_aggregate_manifest, print_aggregate_manifest_summary
        from vitruvius.dataset_pipeline import run_dataset_source_to_graph_pipeline
        def _run_generic_aggregate():
            repo_root = Path.cwd().resolve()
            completed_ledger_path = Path(args.completed_ledger)
            if not completed_ledger_path.is_absolute():
                completed_ledger_path = repo_root / completed_ledger_path
            manifest_index_path = Path(args.manifest_index)
            if not manifest_index_path.is_absolute():
                manifest_index_path = repo_root / manifest_index_path
            out_manifest_path = Path(args.out)
            if not out_manifest_path.is_absolute():
                out_manifest_path = repo_root / out_manifest_path
            aggregate_payload = build_generic_completed_aggregate_manifest(
                repo_root=repo_root,
                completed_ledger_path=completed_ledger_path,
                manifest_index_path=manifest_index_path,
                out_manifest_path=out_manifest_path,
                dataset_id=args.dataset_id,
                dataset_kind=args.dataset_kind,
                graph_output_root=args.graph_output_root,
                run_output_root=args.run_output_root,
                query_snapshot_path_template=args.query_snapshot_template,
                scope_notes=[f"Aggregate graph input for completed lanes from {completed_ledger_path.name}."],
                lane_note_builder=lambda lane_id: f"Aggregate lane: {lane_id}",
                folder_name_resolver=lambda item: str(item.get('raw_folder_name') or item.get('folder_name') or ''),
            )
            print_aggregate_manifest_summary(
                repo_root=repo_root,
                out_manifest_path=out_manifest_path,
                aggregate_payload=aggregate_payload,
            )
            return run_dataset_source_to_graph_pipeline(
                dataset_manifest=str(out_manifest_path.relative_to(repo_root)),
                dry_run=args.dry_run,
                review_preset=args.review_preset,
                review_model=args.review_model,
                review_timeout_seconds=args.review_timeout_seconds,
                review_parallelism=args.review_parallel,
                export_owl=not args.skip_export_owl,
            )
        return _run("run-completed-aggregate", _run_generic_aggregate)

    if args.command == "run-completed-aggregate-from-profile":
        from vitruvius.aggregate_manifest import run_generic_completed_aggregate_from_profile
        return _run(
            "run-completed-aggregate-from-profile",
            lambda: run_generic_completed_aggregate_from_profile(
                repo_root=Path.cwd().resolve(),
                profile_path=Path(args.profile),
                dry_run=args.dry_run,
                review_preset=args.review_preset,
                review_model=args.review_model,
                review_timeout_seconds=args.review_timeout_seconds,
                review_parallelism=args.review_parallel,
                export_owl=not args.skip_export_owl,
            ),
        )

    if args.command == "run-completed-aggregate-family":
        from vitruvius.aggregate_manifest import (
            resolve_completed_aggregate_profile_path,
            run_generic_completed_aggregate_from_profile,
        )
        def _run_generic_family():
            repo_root = Path.cwd().resolve()
            resolved_profile_path = resolve_completed_aggregate_profile_path(
                repo_root=repo_root,
                family=args.family,
                catalog_path=Path(args.catalog),
            )
            return run_generic_completed_aggregate_from_profile(
                repo_root=repo_root,
                profile_path=resolved_profile_path,
                dry_run=args.dry_run,
                review_preset=args.review_preset,
                review_model=args.review_model,
                review_timeout_seconds=args.review_timeout_seconds,
                review_parallelism=args.review_parallel,
                export_owl=not args.skip_export_owl,
            )
        return _run("run-completed-aggregate-family", _run_generic_family)

    if args.command == "build-laws-completed-aggregate-manifest":
        from vitruvius.laws_readiness import build_laws_completed_aggregate_manifest
        return _run(
            "build-laws-completed-aggregate-manifest",
            lambda: build_laws_completed_aggregate_manifest(
                out_path=args.out,
            ),
        )

    if args.command == "run-laws-completed-aggregate":
        from vitruvius.laws_readiness import run_laws_completed_aggregate
        return _run(
            "run-laws-completed-aggregate",
            lambda: run_laws_completed_aggregate(
                dry_run=args.dry_run,
                review_preset=args.review_preset,
                review_model=args.review_model,
                review_timeout_seconds=args.review_timeout_seconds,
                review_parallelism=args.review_parallel,
                export_owl=not args.skip_export_owl,
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
