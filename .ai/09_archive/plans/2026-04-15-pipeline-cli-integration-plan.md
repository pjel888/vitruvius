---
plan_id: pipeline-cli-parser-chain-integration
phase: 1B
title: "pipeline_cli.py Integration for Phase 1B Parser Chain"
status: complete
priority: medium
sprint: "Sprint PIPELINE-CLI"
version: 1.0.0
plan_type: implementation_tdd
created: 2026-04-15
last_updated: 2026-04-15
owner: Senior Systems Architect
prerequisites:
  - Sprint 1B-M1 closed — DoclingParser + LibreOfficePreprocessor + orchestrator preprocessor kwarg
  - Sprint 1B-M2 closed — OCRPreprocessor + process_batch + Golden Corpus
  - (Optional) Sprint 1B-M3 closed — RustPdfParser (if Tranche 3 ships first, this plan registers it as primary; otherwise it's added in a follow-up)
---

# pipeline_cli.py Integration for Phase 1B Parser Chain

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a new CLI subcommand `convert-parsers-one <relative_pdf_path>` that classifies a single document via the Phase 1B taxonomy, dispatches it through `ParserOrchestrator` (with registered preprocessors + the full fallback chain), writes the output markdown + sidecar JSON to `002_Raw-Conversion-Layer/refined_markdown/` under the same path convention as the existing `convert-one` command, and prints the terminal status + telemetry summary. This moves the Phase 1B orchestrator from a library-only surface into the live pipeline.

**Architecture:** Thin CLI adapter. The subcommand handler (`run_convert_parsers_one`) builds a `ParserOrchestrator` with the registered parser chains and preprocessors based on feature flag state, calls `orchestrator.process()`, writes output through the existing `reports.py` sidecar writer, and exits with 0 on `AUTO_ACCEPTED` / `AUTO_REFINED` or 1 on `FALLBACK_EXHAUSTED`. No batch mode in this tranche — single-document CLI first, batch mode is a follow-up once we have a representative corpus.

**Tech Stack:**
- Existing Phase 1B types (`ParserOrchestrator`, `DoclingParser`, `LibreOfficePreprocessor`, `OCRPreprocessor`, optionally `RustPdfParser`)
- Existing `scripts/pipeline_cli.py` argparse dispatch pattern (lazy handler imports per AD-015)
- Existing `reports.py` / `paths.py` for output file routing

---

## Scope & Non-Goals

### In scope

1. **`convert-parsers-one` CLI subcommand** — register in `pipeline_cli.py::build_parser` and `main`, lazy-import the handler.
2. **`run_convert_parsers_one(relative_pdf_path)` handler** — new module `scripts/vitruvius/parsers/cli_handler.py`. Classifies the document via the existing `document_taxonomy.classify_document`, builds an orchestrator with the registered chains, calls `process()`, writes output.
3. **`build_default_orchestrator()` factory** — reads the `p1b_*` feature flags and returns a `ParserOrchestrator` with the right chains + preprocessors. This is the single source of truth for "which parsers are live for which doc classes".
4. **Output writer** — markdown goes to `002_Raw-Conversion-Layer/refined_markdown/<relative_path>` (matching the existing Phase 1C pattern); telemetry JSON goes to `006_System-Manifests/runs/latest_convert_parsers.json`.
5. **Three integration tests** — (a) end-to-end call on a fake PDF with mocked parsers, (b) verify telemetry sidecar written, (c) verify non-zero exit on FALLBACK_EXHAUSTED.
6. **Feature flag** — no new flag. The factory respects the existing `p1b_*` flags and only registers classes whose flags are on. Callers who run this CLI with all flags off get a clear error message: "no parsers registered for doc_class X; flip p1b_* flags in config/vitruvius.yaml".

### Out of scope

- **Batch mode CLI** (`convert-parsers`) — follow-up once single-document mode is proven
- **Replacing `run_convert`** — the existing opendataloader-based CLI path stays as the default. `convert-parsers-one` is a parallel command that runs the Phase 1B chain.
- **Automatic registration of tranche-3 `RustPdfParser`** — if Tranche 3 has shipped, the factory registers it as primary; otherwise it uses the existing Tranche 1 / Tranche 2 parsers.

---

## Tasks (condensed — full TDD expansion follows the Sprint HP.3-R + Sprint 1B-M1/M2 patterns)

### Task 1 — `build_default_orchestrator()` factory

Create `scripts/vitruvius/parsers/factory.py` with a `build_default_orchestrator() -> ParserOrchestrator` function that:

1. Reads `features._features_block()` once
2. Builds the parser_chains dict based on flag state:
   - If `p1b_rust_pdf_parser` is on (Tranche 3): `text_pdf_simple` → `[RustPdfParser, OpenDataLoaderParser]`, `hybrid_pdf` → `[RustPdfParser, DoclingParser]`
   - Else if `p1b_docling_parser` is on (Tranche 1): `text_pdf_simple` → `[OpenDataLoaderParser]`, `hybrid_pdf` → `[DoclingParser]`
   - Else: raise `ValueError("no p1b_* flags enabled; enable at least p1b_docling_parser in config/vitruvius.yaml")`
3. Builds the preprocessors dict:
   - If `p1b_libreoffice_preprocessor` is on: `office_doc` → `LibreOfficePreprocessor()`
   - If `p1b_ocr_preprocessor` is on: `scanned_pdf_clean` → `OCRPreprocessor()`, `scanned_pdf_noisy` → `OCRPreprocessor()`
4. Returns `ParserOrchestrator(parser_chains=..., preprocessors=...)`

Tests: 3 — flag off → ValueError, flag on (tranche 1) → correct chain shape, flag on (tranche 3 if Rust parser module importable) → Rust parser first.

### Task 2 — `run_convert_parsers_one` handler

Create `scripts/vitruvius/parsers/cli_handler.py::run_convert_parsers_one(relative_pdf_path: Path) -> int`. Handler:

1. Resolves `relative_pdf_path` against `paths.get_raw_source_root()` via the existing helpers
2. Classifies via `classify_document(source_path)`
3. Calls `build_default_orchestrator().process(source_path, doc_class, work_dir)`
4. On `AUTO_ACCEPTED` / `AUTO_REFINED`: writes markdown to `002_Raw-Conversion-Layer/refined_markdown/<relative>`, writes telemetry sidecar to `006_System-Manifests/runs/latest_convert_parsers.json`, prints a one-line summary, returns 0
5. On `FALLBACK_EXHAUSTED`: writes the attempt log to the sidecar, prints a clear error with the first AttemptRecord's error, returns 1

Tests: 3 — mock orchestrator for happy path, mock for FALLBACK_EXHAUSTED path, verify sidecar JSON shape.

### Task 3 — Register the subcommand in `pipeline_cli.py`

Add to `build_parser()`:

```python
    p_convert_parsers_one = sub.add_parser(
        "convert-parsers-one",
        help="Phase 1B — convert a single document through the ParserOrchestrator chain",
    )
    p_convert_parsers_one.add_argument("relative_pdf_path", type=Path)
```

Add to `main()` dispatch:

```python
    if args.command == "convert-parsers-one":
        from vitruvius.parsers.cli_handler import run_convert_parsers_one
        return run_convert_parsers_one(relative_pdf_path=args.relative_pdf_path)
```

Smoke test: `scripts/pipeline_cli.py convert-parsers-one --help` prints help text without ImportError.

### Task 4 — Docs + AD-036 + archival

Close the sprint with an AD-036 entry. Update INDEX.md + pipeline-overview.md. Archive this plan.

---

## Execution Handoff

Plan saved. Short, focused plan — estimated 1-2 hours of execution time. Ready to run whenever the user approves.
