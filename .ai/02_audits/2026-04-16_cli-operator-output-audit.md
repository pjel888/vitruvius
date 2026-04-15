---
task: cli-operator-output-upgrade
phase: "04"
created: 2026-04-16
author: IMPLEMENTER
supersedes: null
status: DRAFT
---

# CLI Operator Output Audit — 2026-04-16

## Scope
Audit the current Vitruvius CLI output experience and identify the safest centralized design for a dual-layer operator interface that explains commands in human and technical terms without carelessly breaking automation.

## Authority + state alignment
- Read and aligned with: `AGENTS.md`, `.ai/00_system/EXECUTION_LOOP.md`, `.ai/00_system/principles.md`, `.ai/01_roadmap/master-roadmap.md`, `.ai/01_roadmap/current-phase.md`, `.ai/01_roadmap/milestone-tracker.md`, `.ai/03_plans/00-governing-implementation-plan.md`, `.ai/03_plans/INDEX.md`, `.ai/10_state/active_context.md`, `.ai/10_state/known_issues.md`.
- Current repo state is between implementation sprints, but this task is compatible with the active governance/maintenance lane because it improves a root operator surface (`scripts/pipeline_cli.py`) without crossing roadmap gates.

## Research notes
### Exploration method
- The repo instructions require `code-review-graph` / GitNexus first.
- Those graph surfaces were not available in this session, and `omx_code_intel` reference queries failed with transport-closed errors.
- Fallback used: direct source inspection, symbol listing, targeted ripgrep, and existing CLI tests.

### Files audited
- `scripts/pipeline_cli.py`
- `scripts/vitruvius/query/cli_formatter.py`
- `scripts/vitruvius/reports.py`
- `scripts/vitruvius/normalization/refine.py`
- `scripts/vitruvius/concept_enrichment.py`
- Representative CLI handlers discovered through `rg` across `scripts/vitruvius/`
- CLI tests under `scripts/tests/`

## Current CLI architecture
1. `scripts/pipeline_cli.py` is the single top-level entrypoint.
2. Commands are registered directly inside `build_parser()` via `subparsers.add_parser(...)`.
3. Dispatch is a long `if args.command == ...` chain in `main()`.
4. Handler imports are intentionally lazy inside dispatch branches.
5. Most handler functions return only an integer exit code and print their own summaries directly.
6. There is no shared command-metadata registry, no shared presentation layer, and no common pre-run/post-run explanation wrapper.

## Current command surface
### Core operator commands
- `scan`, `status`, `lint`, `convert`, `reconcile`, `ocr-queue`, `ocr-execute`, `run`, `run-with-review`

### Single-file / focused processing commands
- `detect-one`, `convert-one`, `convert-parsers-one`, `convert-spreadsheet-one`
- `canonicalize-plan-one`, `canonicalize-one`, `canonicalize-concept-one`
- `extract-relationships-one`, `extract-relationships-sections-one`
- `refine-one`, `enrich-concept-one`

### Batch knowledge-processing commands
- `canonicalize`, `refine`, `enrich-concepts`
- `review-relationships-ollama`, `review-relationships-ollama-second-pass`, `promote`
- `rotate-registries`, `migrate-ids-plan`, `migrate-ids-apply`, `ple-kv-migrate`

### Graph / query / specialist commands
- `build-graph`, `query-graph`, `export-graph-snapshot`, `export-graph-owl`
- `query`, `query-structured`
- `ingest-spatial`, `evaluate-spatial`
- `ple-cotrace-dump`, `ple-registry-purge`, `ple-vision-probe`

## Existing output behavior
### Strengths
- Many handlers already emit terse technical summaries.
- The CLI keeps lazy imports intact for `--help` and narrowly scoped command usage.
- Existing tests already protect lazy imports, top-level help command coverage, and some stdout behavior for query/graph/spatial paths.

### Gaps
1. Top-level `--help` is mostly a flat command list.
2. Many subcommands have no `help`, no description, and no epilog.
3. There is no human-oriented explanation of why a command exists.
4. There is no centralized technical explanation of touched layers/artifacts.
5. There is no shared success/failure/next-step guidance.
6. Output style differs per command and is duplicated inside handlers.
7. JSON / machine-readable commands are mixed with human-console commands, so careless global wrapping would break automation.

## Backcompat and automation constraints
1. `pipeline_cli.py` lazy imports are guarded by tests such as:
   - `scripts/tests/test_cli_lazy_imports.py`
   - `scripts/tests/test_pipeline_cli_byte_identity.py`
   - `scripts/tests/test_query_cli.py`
   - `scripts/tests/test_graph_cli.py`
2. Some commands emit JSON or structured stdout that existing tests parse directly:
   - `build-graph`
   - `query-graph`
   - `export-graph-snapshot`
   - `evaluate-spatial`
   - some query/spatial failure branches
3. Therefore the upgrade cannot blindly prepend prose to every command in every mode.

## Best insertion points
### Help-path insertion point
`build_parser()` is the correct place to centralize:
- short help text
- long description
- epilog guidance
- formatter class

### Run-path insertion point
`main()` is the correct place to centralize:
- pre-run operator explanation block
- post-run interpretation block
- output mode routing (`auto` vs concise vs operator)

### Existing handler boundary
Handler functions should mostly stay untouched because:
- they already own the command-specific technical execution
- touching dozens of handlers would duplicate copy and raise blast radius
- a wrapper around the handler return code is enough for human/technical framing

## Recommended design
### Design choice
Introduce a lightweight shared CLI presentation layer with:
1. a command metadata registry
2. a parser helper that injects consistent help/description/epilog text
3. an execution wrapper that prints pre-run and post-run explanation blocks only when appropriate
4. an output mode switch that preserves concise/non-interactive behavior

### Why this is the best fit
- centralized
- low-risk to existing handler logic
- compatible with lazy imports
- scalable to future subcommands
- allows human-first output without corrupting JSON-first commands

## Risk assessment
### Main risks
- **Duplication risk:** if metadata is not centralized, text will sprawl across `build_parser()` and handlers.
- **Noise risk:** if operator explanations print on every command unconditionally, the CLI becomes exhausting.
- **Automation risk:** if explanation blocks wrap JSON-oriented commands, tests and scripts will break.
- **Maintenance risk:** if metadata coverage is partial or inconsistent, the interface becomes uneven.

### Best mitigation
Use a registry + output-mode gate:
- `auto` default
- operator explanations only for human-facing commands on interactive terminals
- concise mode preserved elsewhere
- structured-output commands remain concise by default

## Audit conclusion
A centralized metadata-and-wrapper design is both necessary and feasible. The upgrade should focus on `scripts/pipeline_cli.py` plus a new lightweight CLI presentation helper module, with targeted tests covering help enrichment, operator pre/post blocks, and protection of concise/script-safe output paths.
