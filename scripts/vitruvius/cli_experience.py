from __future__ import annotations

import argparse
import os
import sys
from dataclasses import dataclass
from typing import Callable


RAW_HELP_FORMATTER = argparse.RawDescriptionHelpFormatter

ROOT_PARSER_DESCRIPTION = """Vitruvius pipeline entrypoint

Vitruvius exposes both operator-facing pipeline commands and specialist
maintenance/query commands.

Use `--output-mode operator` when you want the CLI to explain a command in
human and technical terms before and after it runs.
"""

ROOT_PARSER_EPILOG = """Output modes:
  auto      operator framing for interactive, human-facing commands; concise elsewhere
  operator  always show operator framing when the command is safe to wrap
  concise   suppress framing blocks and keep raw command output only
"""


@dataclass(frozen=True)
class CommandDoc:
    name: str
    help_text: str
    human_explanation: str | None = None
    technical_explanation: str | None = None
    success_meaning: str | None = None
    failure_meaning: str | None = None
    next_step: str | None = None
    operator_safe: bool = True

    @property
    def has_detail(self) -> bool:
        return any(
            [
                self.human_explanation,
                self.technical_explanation,
                self.success_meaning,
                self.failure_meaning,
                self.next_step,
            ]
        )


def _doc(
    name: str,
    help_text: str,
    *,
    human: str | None = None,
    technical: str | None = None,
    success: str | None = None,
    failure: str | None = None,
    next_step: str | None = None,
    operator_safe: bool = True,
) -> CommandDoc:
    return CommandDoc(
        name=name,
        help_text=help_text,
        human_explanation=human,
        technical_explanation=technical,
        success_meaning=success,
        failure_meaning=failure,
        next_step=next_step,
        operator_safe=operator_safe,
    )


COMMAND_DOCS: dict[str, CommandDoc] = {
    "scan": _doc(
        "scan",
        "Inventory raw source files into the registry and snapshot reports.",
        human="This checks what source documents exist right now so the pipeline knows what is available to process.",
        technical="Reads `001_Raw-Source-Layer`, builds `FileEntry` records, and writes tree snapshots plus raw-file registry artifacts under `006_System-Manifests`.",
        success="The raw layer was scanned and the latest JSON/TXT/CSV inventory artifacts were refreshed.",
        failure="The raw layer could not be read or the scan artifacts could not be written. Downstream status and lint runs may be stale.",
        next_step="Run `status` to compare snapshots or `run` for the standard scan → status → lint sequence.",
    ),
    "status": _doc(
        "status",
        "Compare recent raw-file registries and report what changed.",
        human="This tells an operator what is new, changed, missing, or unchanged since the previous scan.",
        technical="Reads timestamped raw-file registries in `006_System-Manifests/registries/`, computes diffs, and writes status reports to `006_System-Manifests/runs/`.",
        success="A healthy result shows clear counts for new, changed, missing, and unchanged files, plus fresh status report paths.",
        failure="There is not enough registry history yet, or the diff artifacts could not be produced. Change detection is blocked until scans are in place.",
        next_step="If history is missing, run `scan` again later. If counts look right, continue to `lint`, `convert`, or `run`.",
    ),
    "lint": _doc(
        "lint",
        "Check the raw corpus for hygiene issues before conversion.",
        human="This looks for file-level problems that could confuse the pipeline before deeper processing starts.",
        technical="Reads the latest raw-file registry and emits lint reports about suspicious extensions, duplicate-like filenames, and raw-layer hygiene.",
        success="A healthy result means the raw corpus was checked and the latest lint report paths were written.",
        failure="The registry or lint report path is missing, so hygiene status is unknown and pipeline confidence drops.",
        next_step="Fix flagged raw-layer issues or proceed to `convert` / `run` if the warnings are acceptable.",
    ),
    "convert": _doc(
        "convert",
        "Convert supported raw documents into machine-readable conversion outputs.",
        human="This turns source files into extracted text and sidecar artifacts so later stages can reason over them.",
        technical="Reads `001_Raw-Source-Layer`, routes files through the conversion stack, and writes markdown/JSON/OCR-sidecar outputs into `002_Raw-Conversion-Layer` plus registry entries.",
        success="A healthy run writes conversion outputs and registry rows without unexpected parsing failures.",
        failure="One or more documents could not be converted, so downstream refinement and canonicalization may be incomplete.",
        next_step="Run `refine` after successful conversion, or inspect the latest conversion reports if failures occurred.",
    ),
    "reconcile": _doc(
        "reconcile",
        "Check for missing raw files and stale derived outputs.",
        human="This asks whether the filesystem still lines up across the raw and derived layers.",
        technical="Compares status outputs and derived-layer artifacts to identify missing raw inputs, stale downstream outputs, and unsupported drift cases.",
        success="A healthy result gives an auditable list of missing/stale items and fresh reconcile report paths.",
        failure="Reconciliation inputs are missing or inconsistent, so lineage confidence is reduced.",
        next_step="Run `run` first if baseline reports are missing, or repair the listed files before further downstream work.",
    ),
    "ocr-queue": _doc(
        "ocr-queue",
        "Build the queue of files that likely need OCR.",
        human="This decides which files probably need text recovery before ordinary conversion can trust them.",
        technical="Reads the latest OCR-needed signals and writes queue reports under `006_System-Manifests/runs/`.",
        success="A healthy result identifies OCR candidates and writes fresh queue artifacts.",
        failure="The OCR-needed report is missing, so the pipeline cannot stage OCR work yet.",
        next_step="Run `convert` first if the source report does not exist, then run `ocr-execute` on the queue if needed.",
    ),
    "ocr-execute": _doc(
        "ocr-execute",
        "Run OCR on queued files and continue their conversion path.",
        human="This recovers text from scanned documents so the rest of the pipeline can work on usable content.",
        technical="Consumes the OCR queue, runs `ocrmypdf` with the requested options, and writes OCR PDFs, conversion outputs, and execution reports.",
        success="A healthy result shows OCR completions, conversion completions, and fresh report paths.",
        failure="Some queued items could not be OCRed or converted, which blocks trustworthy downstream text processing for those files.",
        next_step="Inspect the OCR execute report for failed items, then rerun targeted conversion or OCR after fixing prerequisites.",
    ),
    "run": _doc(
        "run",
        "Run the default baseline pipeline: scan, status, then lint.",
        human="This is the normal quick health-and-inventory pass for the corpus.",
        technical="Executes `run_scan()`, `run_status()`, and `run_lint()` in sequence, stopping on the first non-zero exit code.",
        success="Success means the baseline raw-layer audit path completed without blocking errors.",
        failure="One of the baseline stages failed, so the repo's current raw-layer state is not fully validated.",
        next_step="Inspect the failing stage output, fix the root issue, and rerun `run` or the failing subcommand directly.",
    ),
    "run-with-review": _doc(
        "run-with-review",
        "Run the baseline pipeline, convert, refine, and Tier-1 review in one operator path.",
        human="This is the longer walk-away path when you want the system to move from raw intake toward reviewed relationship candidates.",
        technical="Runs `run`, then `convert`, then `refine`, then `review-relationships-ollama` with config-driven model and timeout settings.",
        success="Success means the end-to-end path reached reviewed relationship output without blocking errors.",
        failure="A failure anywhere in the chain leaves downstream outputs partially updated, so review readiness is incomplete.",
        next_step="Inspect the stage that failed, rerun it directly if needed, then continue downstream from that checkpoint.",
    ),
    "detect-one": _doc(
        "detect-one",
        "Classify one PDF as text-usable or scan-like before conversion.",
        human="This is a spot-check to see which route a single PDF should take.",
        technical="Samples pages from one PDF, measures usable text density, and writes detect reports under `006_System-Manifests/runs/`.",
        success="A healthy result reports the detection verdict, recommended route, and report paths.",
        failure="The target file could not be read or was not a PDF, so routing confidence for that file is unknown.",
        next_step="Use the recommended route to decide whether to run ordinary conversion or OCR-related processing.",
    ),
    "convert-one": _doc(
        "convert-one",
        "Convert one source document through the legacy single-file path.",
        human="Use this when you want to inspect one file closely without running a broader batch.",
        technical="Runs the single-file conversion route for one PDF/Office document and writes the corresponding conversion-layer outputs and reports.",
        success="The file was converted and its output paths were written clearly.",
        failure="That file could not be parsed or routed safely, so no trustworthy downstream output exists for it.",
        next_step="Inspect the emitted detection/conversion details, then try OCR, parser-chain conversion, or source cleanup.",
    ),
    "convert-parsers-one": _doc(
        "convert-parsers-one",
        "Convert one document through the Phase 1B parser orchestrator chain.",
        human="This lets an operator test the newer parser-selection path on a single document.",
        technical="Routes one document through `ParserOrchestrator` and feature-flagged parser/preprocessor infrastructure under `scripts/vitruvius/parsers/`.",
        success="A healthy run shows which parser path was used and whether conversion artifacts were produced cleanly.",
        failure="The document could not be classified, routed, or parsed under the current parser-chain configuration.",
        next_step="Check parser flags/config and the handler summary, then retry with the right parser path or fall back to `convert-one`.",
    ),
    "convert-spreadsheet-one": _doc(
        "convert-spreadsheet-one",
        "Convert one spreadsheet into CSV/JSON layer outputs.",
        human="Use this to inspect how one workbook is being unpacked for downstream use.",
        technical="Reads one `.xlsx`/`.xls` file and writes per-sheet CSV/JSON plus a manifest and registry outputs under `002_Raw-Conversion-Layer`.",
        success="A healthy result shows workbook, manifest, and sheet-count details.",
        failure="The spreadsheet could not be opened or normalized, so downstream structured extraction is blocked for that workbook.",
        next_step="Inspect the workbook path used and error details, then repair the source or rerun the command.",
    ),
    "canonicalize-plan-one": _doc(
        "canonicalize-plan-one",
        "Preview how one refined markdown file would canonicalize.",
        human="This shows how Vitruvius intends to map one source into a canonical identity before it writes the final file.",
        technical="Builds a canonicalization plan for one markdown input, including ID, title, type, and referenced concept hints.",
        success="A healthy result yields a plausible title, canonical ID, source type, and concept list.",
        failure="The input file could not be interpreted into a valid canonical plan, so promotion into the canonical layer should not proceed.",
        next_step="Fix the source/refined markdown or adjust canonical rules before running `canonicalize-one` or `canonicalize`.",
    ),
    "canonicalize-one": _doc(
        "canonicalize-one",
        "Write one refined markdown file into the canonical knowledge layer.",
        human="This turns one refined source into a stable, governed canonical page.",
        technical="Reads one refined markdown file, applies canonical rules, respects diff guards, and writes into `003_Canonical-Knowledge-Layer`.",
        success="A healthy result writes or safely skips the canonical target according to the diff guard.",
        failure="The file could not be mapped or passed the write guard, so canonical truth was not updated.",
        next_step="Review the reported target path and reason, then rerun after fixing the underlying source or rules.",
    ),
    "canonicalize-concept-one": _doc(
        "canonicalize-concept-one",
        "Create one canonical concept page scaffold.",
        human="This gives a concept a formal home in the canonical layer so later enrichment and relationships have a stable target.",
        technical="Writes one concept markdown file with canonical frontmatter into `003_Canonical-Knowledge-Layer/shared/concepts/` unless it already exists.",
        success="A healthy result creates the concept file or clearly reports that it already exists.",
        failure="The concept file could not be created safely, so concept-level downstream work stays blocked.",
        next_step="Run `enrich-concept-one` or `enrich-concepts` after the concept scaffold exists.",
    ),
    "extract-relationships-one": _doc(
        "extract-relationships-one",
        "Extract candidate relationships from one canonical-ready markdown file.",
        human="This finds possible knowledge links in one document so they can be reviewed instead of being guessed later.",
        technical="Runs the regex-based relationship extractor on one markdown input and writes TXT/JSON candidate reports.",
        success="A healthy result writes unique candidate relationships and the report paths needed for review.",
        failure="Extraction failed or produced unusable output, so review/promote stages have nothing reliable to work with for that file.",
        next_step="Inspect the source markdown and reports, then retry or switch to the section-aware extractor.",
    ),
    "extract-relationships-sections-one": _doc(
        "extract-relationships-sections-one",
        "Extract section-aware candidate relationships from one markdown file.",
        human="This is the more context-aware single-file extractor when section lineage matters.",
        technical="Runs the section-aware extractor, keeps section IDs in evidence, deduplicates results, and writes TXT/JSON reports.",
        success="A healthy result produces deduplicated, section-aware candidates with clear report paths.",
        failure="The source markdown could not be parsed into a trustworthy section-aware candidate set.",
        next_step="Review the section output, fix malformed markdown, or move on to review if the candidate set looks sound.",
    ),
    "review-relationships-ollama": _doc(
        "review-relationships-ollama",
        "Run Tier-1 local LLM review on extracted relationship candidates.",
        human="This is where uncertain relationship candidates get judged before they can influence canonical truth.",
        technical="Loads candidate relationship reports, applies deterministic pre-review triage, then calls the configured Ollama model for remaining cases and writes merged review artifacts.",
        success="A healthy result writes the Tier-1 review outputs, including the high-confidence subset for promotion.",
        failure="The review pass could not complete, so relationship candidates remain unreviewed or partially reviewed.",
        next_step="Check Ollama/model availability and the saved review snapshots, then rerun review or resume from the in-progress state.",
    ),
    "review-relationships-ollama-second-pass": _doc(
        "review-relationships-ollama-second-pass",
        "Run Tier-2 adjudication on uncertain Tier-1 review results.",
        human="This is the disagreement-resolution pass for cases that still need a stronger judgment.",
        technical="Selects uncertain Tier-1 results, routes them through Tier-2 adjudication logic, and writes merged second-pass outputs plus escalation worklists.",
        success="A healthy result reports agreement/disagreement rates and writes the merged review artifacts.",
        failure="Tier-2 adjudication could not complete, leaving borderline cases unresolved.",
        next_step="Inspect the disagreement output or human escalation worklist before promotion.",
    ),
    "promote": _doc(
        "promote",
        "Move approved relationship reviews into canonical relationship records.",
        human="This is the truth-admission step: reviewed relationship results become canonical records only here.",
        technical="Reads the high-confidence review artifact, validates it against promotion rules, writes or rolls back canonical relationship files, and appends promotion audit logs.",
        success="A healthy run validates candidates cleanly and reports exactly what was written, skipped, or rolled back.",
        failure="Promotion validation failed or writes were blocked, so canonical relationship truth did not advance safely.",
        next_step="Review the validation details, fix the upstream review/promotion issue, then rerun promotion in dry-run or execute mode.",
    ),
    "enrich-concept-one": _doc(
        "enrich-concept-one",
        "Enrich one concept with deterministic definition and regulatory basis data.",
        human="This upgrades one concept from a placeholder into a usable knowledge node.",
        technical="Scans refined and canonical source text, selects the best deterministic definition candidate, mines aliases, applies diff guards, and writes the enriched concept file.",
        success="A healthy result records a definition source, section linkage, and any useful aliases for that concept.",
        failure="No safe definition was found or the diff guard blocked the write, so the concept stays un-enriched.",
        next_step="Inspect the reason, add better source material if needed, or rerun with `--force` only when appropriate.",
    ),
    "enrich-concepts": _doc(
        "enrich-concepts",
        "Batch-enrich concept pages with deterministic definitions and regulatory basis.",
        human="This fills concept pages with real meaning so operators and downstream systems can trust what a concept stands for.",
        technical="Walks canonical concept files, mines refined/canonical source text for definitions and aliases, applies the diff guard, and writes enriched concept markdown into `003_Canonical-Knowledge-Layer/shared/concepts/`.",
        success="A healthy result reports how many concepts were enriched versus skipped and why.",
        failure="Some concepts could not be enriched safely, so concept coverage remains partial and downstream relationship/query quality may stay uneven.",
        next_step="Review skipped reasons, improve source coverage if needed, and rerun `enrich-concepts` or `enrich-concept-one` selectively.",
    ),
    "canonicalize": _doc(
        "canonicalize",
        "Batch-write refined sources into canonical source pages.",
        human="This is the batch form of turning refined source text into governed canonical records.",
        technical="Scans the conversion layer for eligible markdown files, canonicalizes them, respects the diff guard, and reports processed/skipped/failed counts.",
        success="A healthy result writes or safely skips canonical targets without uncontrolled overwrites.",
        failure="Some files could not be canonicalized, so the canonical layer only partially reflects the refined inputs.",
        next_step="Inspect failed file paths, fix the underlying inputs or rules, and rerun the batch or the single-file path.",
    ),
    "refine": _doc(
        "refine",
        "Batch-clean raw conversion markdown into deterministic refined markdown.",
        human="This normalizes extracted text so it becomes easier to trust and easier for downstream stages to consume consistently.",
        technical="Reads `002_Raw-Conversion-Layer/*/raw_markdown/**`, runs the Phase 1C normalization engine, writes `refined_markdown` outputs, and emits `.refined.json` manifests.",
        success="A healthy result writes refined markdown and manifests with no parse or rule-application failures.",
        failure="One or more source markdown files could not be normalized safely, so downstream canonicalization and extraction may receive unreliable text.",
        next_step="Inspect the failed paths or warnings, then run `canonicalize`, `extract-relationships-*`, or `run-with-review` after refinement succeeds.",
    ),
    "refine-one": _doc(
        "refine-one",
        "Refine one markdown conversion output through the normalization engine.",
        human="Use this when you want to inspect normalization behavior on a single file before trusting a batch run.",
        technical="Runs the Phase 1C normalization engine on one `raw_markdown` file and writes the paired refined markdown plus manifest.",
        success="A healthy result writes one refined file and its manifest cleanly.",
        failure="That markdown file could not be normalized, so later stages should not rely on it yet.",
        next_step="Inspect the source path, warnings, and manifest details, then rerun after fixing the source or rules.",
    ),
    "rotate-registries": _doc(
        "rotate-registries",
        "Prune old timestamped registry snapshots while preserving latest pointers.",
        human="This keeps the registry area readable and bounded without destroying the latest operational state.",
        technical="Plans or applies retention against timestamped registry families in `006_System-Manifests/registries/`, leaving `latest_*.csv` and static registries untouched.",
        success="A healthy dry-run or execution clearly reports how many snapshots would be kept and pruned per family.",
        failure="Rotation could not inspect or prune the target registry families, so manifest hygiene remains stale.",
        next_step="Use `--dry-run` first, then rerun without it when the retention plan looks correct.",
    ),
    "migrate-ids-plan": _doc("migrate-ids-plan", "Plan a canonical ID migration without applying it."),
    "migrate-ids-apply": _doc("migrate-ids-apply", "Apply a previously planned canonical ID migration."),
    "ple-kv-migrate": _doc("ple-kv-migrate", "Migrate a review/event KV store between SQLite and RocksDB layouts."),
    "build-graph": _doc("build-graph", "Build the filesystem graph snapshot from canonical knowledge.", operator_safe=False),
    "query-graph": _doc("query-graph", "Return a graph path between two node IDs.", operator_safe=False),
    "export-graph-snapshot": _doc("export-graph-snapshot", "Print the latest graph snapshot in a structured export format.", operator_safe=False),
    "export-graph-owl": _doc("export-graph-owl", "Export the latest graph snapshot as RDF Turtle.", operator_safe=False),
    "ingest-spatial": _doc("ingest-spatial", "Ingest spatial artifacts into the spatial subsystem.", operator_safe=False),
    "evaluate-spatial": _doc("evaluate-spatial", "Evaluate spatial rules against supplied observations.", operator_safe=False),
    "ple-cotrace-dump": _doc("ple-cotrace-dump", "Summarize a Chain-of-Thought audit directory."),
    "ple-registry-purge": _doc("ple-registry-purge", "Purge old rows from the stateful review registry."),
    "ple-vision-probe": _doc("ple-vision-probe", "Check RAM headroom and Ollama model availability for vision OCR."),
    "query": _doc("query", "Ask a natural-language question against the latest graph snapshot.", operator_safe=False),
    "query-structured": _doc("query-structured", "Run a structured query function against the latest graph snapshot.", operator_safe=False),
}


def _indent(text: str | None) -> str:
    if not text:
        return "  (not specified)"
    return "\n".join(f"  {line}" for line in text.splitlines())


def _join_non_empty(parts: list[str | None]) -> str:
    return "\n".join(part for part in parts if part)


def render_help_description(doc: CommandDoc) -> str | None:
    if not doc.has_detail:
        return None
    return _join_non_empty(
        [
            f"{doc.name} — {doc.help_text}",
            "",
            "Human explanation:",
            _indent(doc.human_explanation),
            "",
            "Technical explanation:",
            _indent(doc.technical_explanation),
        ]
    )


def render_help_epilog(doc: CommandDoc) -> str | None:
    if not doc.has_detail:
        return None
    return _join_non_empty(
        [
            "Success means:",
            _indent(doc.success_meaning),
            "",
            "Failure means:",
            _indent(doc.failure_meaning),
            "",
            "Suggested next step:",
            _indent(doc.next_step),
        ]
    )


def add_command_parser(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
    name: str,
    **kwargs,
) -> argparse.ArgumentParser:
    doc = COMMAND_DOCS.get(name)
    if doc is not None:
        kwargs.setdefault("help", doc.help_text)
        description = render_help_description(doc)
        epilog = render_help_epilog(doc)
        if description is not None:
            kwargs.setdefault("description", description)
        if epilog is not None:
            kwargs.setdefault("epilog", epilog)
        kwargs.setdefault("formatter_class", RAW_HELP_FORMATTER)
    return subparsers.add_parser(name, **kwargs)


def resolve_output_mode(requested_mode: str, command_name: str | None) -> str:
    env_mode = os.getenv("VITRUVIUS_CLI_OUTPUT_MODE")
    mode = env_mode or requested_mode
    doc = COMMAND_DOCS.get(command_name or "")
    if mode == "auto":
        if doc is not None and doc.operator_safe and sys.stdout.isatty():
            return "operator"
        return "concise"
    if mode == "operator" and (doc is None or not doc.operator_safe):
        return "concise"
    return mode


def render_operator_preamble(command_name: str) -> str | None:
    doc = COMMAND_DOCS.get(command_name)
    if doc is None or not doc.has_detail:
        return None
    return _join_non_empty(
        [
            "-" * 60,
            f"Command: {doc.name}",
            f"Human explanation:\n{_indent(doc.human_explanation)}",
            f"Technical explanation:\n{_indent(doc.technical_explanation)}",
            f"Success means:\n{_indent(doc.success_meaning)}",
            f"Failure means:\n{_indent(doc.failure_meaning)}",
            f"Suggested next step:\n{_indent(doc.next_step)}",
            "-" * 60,
        ]
    )


def render_operator_summary(command_name: str, return_code: int) -> str | None:
    doc = COMMAND_DOCS.get(command_name)
    if doc is None or not doc.has_detail:
        return None
    status = "success" if return_code == 0 else f"failure (exit code {return_code})"
    interpretation = doc.success_meaning if return_code == 0 else doc.failure_meaning
    return _join_non_empty(
        [
            "-" * 60,
            f"Result summary: {status}",
            f"Interpretation:\n{_indent(interpretation)}",
            f"Suggested next step:\n{_indent(doc.next_step)}",
            "-" * 60,
        ]
    )


def execute_with_cli_experience(
    command_name: str,
    *,
    output_mode: str,
    handler: Callable[[], int],
) -> int:
    resolved_mode = resolve_output_mode(output_mode, command_name)
    if resolved_mode == "operator":
        preamble = render_operator_preamble(command_name)
        if preamble:
            print(preamble)
    return_code = handler()
    if resolved_mode == "operator":
        summary = render_operator_summary(command_name, return_code)
        if summary:
            print(summary)
    return return_code
