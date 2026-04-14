<!-- Generated: 2026-04-13 | Updated: 2026-04-13 -->

# Vitruvius Root

## Purpose
Local-first knowledge pipeline for architectural board exam preparation. Processes raw documents through scanning, conversion, canonicalization, and derivation layers to produce machine-readable knowledge for AI-assisted study.

## Key Files
| File | Description |
|------|-------------|
| `README.md` | Full project documentation |
| `AGENTS.md` | This file - AI agent guidance |
| `CLAUDE.md` | Claude Code-specific instructions |
| `GEMINI.md` | Gemini CLI instructions |
| `config/vitruvius.yaml` | Project configuration |
| `init_vitruvius_structure.sh` | Directory structure initialization script |

## Subdirectories
| Directory | Purpose |
|-----------|---------|
| `scripts/` | Python pipeline CLI and core package (see `scripts/AGENTS.md`) |
| `config/` | Configuration files (see `config/AGENTS.md`) |
| `docs/` | Documentation files (see `docs/AGENTS.md`) |
| `001_Raw-Source-Layer/` | Original source documents (PDFs, scans) |
| `002_Raw-Conversion-Layer/` | Machine-extracted text outputs |
| `003_Canonical-Knowledge-Layer/` | Trusted, curated knowledge pages |
| `004_Derived-Content-Layer/` | Generated learning content |
| `005_Operational-Intelligence-Layer/` | Machine infrastructure (chunks, embeddings, graphs) |
| `006_System-Manifests/` | Pipeline control, audit logs, registries |

## For AI Agents

### Working In This Directory
- **ALWAYS use code-review-graph MCP tools** before using Grep/Glob/Read to explore the codebase
- **ALWAYS use gitnexus tools** for impact analysis before editing any symbol
- Run `npx gitnexus analyze` if the index becomes stale
- Follow the Content Trust Order: Canonical > Raw Conversion > Raw Source

### Pipeline Commands
```bash
# Full pipeline
python scripts/pipeline_cli.py run

# Convert PDFs
python scripts/pipeline_cli.py convert

# Detect PDF type
python scripts/pipeline_cli.py detect-one "path/to/file.pdf"

# Run OCR
python scripts/pipeline_cli.py ocr-execute
```

### Testing Requirements
- Test any pipeline modification with `test_pdf_text_detection.py` and `test_odl_one.py`
- Verify reports are written correctly to `006_System-Manifests/runs/`

### Common Patterns
- All pipeline modules are in `scripts/vitruvius/`
- Use the six-layer architecture consistently
- All outputs go to layer 6 for auditability

## Dependencies

### External
- `pypdf` - PDF text extraction for detection
- `opendataloader-pdf` - PDF-to-Markdown conversion
- `ocrmypdf` - OCR processing for scanned PDFs
- `PyYAML` - Configuration file parsing

### Internal
- `scripts/vitruvius/` - Core pipeline modules
- Six data layers for knowledge lifecycle

## Data Layers Overview

| Layer | Folder | Purpose |
|-------|--------|---------|
| 1 | `001_Raw-Source-Layer/` | Original source documents (git-ignored) |
| 2 | `002_Raw-Conversion-Layer/` | Machine-extracted text (Markdown, JSON, OCR PDFs) |
| 3 | `003_Canonical-Knowledge-Layer/` | Trusted, curated knowledge |
| 4 | `004_Derived-Content-Layer/` | Generated learning content |
| 5 | `005_Operational-Intelligence-Layer/` | Chunks, embeddings, graphs |
| 6 | `006_System-Manifests/` | Pipeline control and audit |

<!-- MANUAL: MCP tool configuration and GitNexus instructions are in the header above this file -->

<!-- code-review-graph MCP tools -->
## MCP Tools: code-review-graph

**IMPORTANT: This project has a knowledge graph. ALWAYS use the
code-review-graph MCP tools BEFORE using Grep/Glob/Read to explore
the codebase.** The graph is faster, cheaper (fewer tokens), and gives
you structural context (callers, dependents, test coverage) that file
scanning cannot.

### When to use graph tools FIRST

- **Exploring code**: `semantic_search_nodes` or `query_graph` instead of Grep
- **Understanding impact**: `get_impact_radius` instead of manually tracing imports
- **Code review**: `detect_changes` + `get_review_context` instead of reading entire files
- **Finding relationships**: `query_graph` with callers_of/callees_of/imports_of/tests_for
- **Architecture questions**: `get_architecture_overview` + `list_communities`

Fall back to Grep/Glob/Read **only** when the graph doesn't cover what you need.

### Key Tools

| Tool | Use when |
|------|----------|
| `detect_changes` | Reviewing code changes — gives risk-scored analysis |
| `get_review_context` | Need source snippets for review — token-efficient |
| `get_impact_radius` | Understanding blast radius of a change |
| `get_affected_flows` | Finding which execution paths are impacted |
| `query_graph` | Tracing callers, callees, imports, tests, dependencies |
| `semantic_search_nodes` | Finding functions/classes by name or keyword |
| `get_architecture_overview` | Understanding high-level codebase structure |
| `refactor_tool` | Planning renames, finding dead code |

### Workflow

1. The graph auto-updates on file changes (via hooks).
2. Use `detect_changes` for code review.
3. Use `get_affected_flows` to understand impact.
4. Use `query_graph` pattern="tests_for" to check coverage.

<!-- gitnexus:start -->
# GitNexus — Code Intelligence

This project is indexed by GitNexus as **vitruvius** (4384 symbols, 10482 relationships, 270 execution flows). Use the GitNexus MCP tools to understand code, assess impact, and navigate safely.

> If any GitNexus tool warns the index is stale, run `npx gitnexus analyze` in terminal first.

## Always Do

- **MUST run impact analysis before editing any symbol.** Before modifying a function, class, or method, run `gitnexus_impact({target: "symbolName", direction: "upstream"})` and report the blast radius (direct callers, affected processes, risk level) to the user.
- **MUST run `gitnexus_detect_changes()` before committing** to verify your changes only affect expected symbols and execution flows.
- **MUST warn the user** if impact analysis returns HIGH or CRITICAL risk before proceeding with edits.
- When exploring unfamiliar code, use `gitnexus_query({query: "concept"})` to find execution flows instead of grepping. It returns process-grouped results ranked by relevance.
- When you need full context on a specific symbol — callers, callees, which execution flows it participates in — use `gitnexus_context({name: "symbolName"})`.

## When Debugging

1. `gitnexus_query({query: "<error or symptom>"})` — find execution flows related to the issue
2. `gitnexus_context({name: "<suspect function>"})` — see all callers, callees, and process participation
3. `READ gitnexus://repo/vitruvius/process/{processName}` — trace the full execution flow step by step
4. For regressions: `gitnexus_detect_changes({scope: "compare", base_ref: "main"})` — see what your branch changed

## When Refactoring

- **Renaming**: MUST use `gitnexus_rename({symbol_name: "old", new_name: "new", dry_run: true})` first. Review the preview — graph edits are safe, text_search edits need manual review. Then run with `dry_run: false`.
- **Extracting/Splitting**: MUST run `gitnexus_context({name: "target"})` to see all incoming/outgoing refs, then `gitnexus_impact({target: "target", direction: "upstream"})` to find all external callers before moving code.
- After any refactor: run `gitnexus_detect_changes({scope: "all"})` to verify only expected files changed.

## Never Do

- NEVER edit a function, class, or method without first running `gitnexus_impact` on it.
- NEVER ignore HIGH or CRITICAL risk warnings from impact analysis.
- NEVER rename symbols with find-and-replace — use `gitnexus_rename` which understands the call graph.
- NEVER commit changes without running `gitnexus_detect_changes()` to check affected scope.

## Tools Quick Reference

| Tool | When to use | Command |
|------|-------------|---------|
| `query` | Find code by concept | `gitnexus_query({query: "auth validation"})` |
| `context` | 360-degree view of one symbol | `gitnexus_context({name: "validateUser"})` |
| `impact` | Blast radius before editing | `gitnexus_impact({target: "X", direction: "upstream"})` |
| `detect_changes` | Pre-commit scope check | `gitnexus_detect_changes({scope: "staged"})` |
| `rename` | Safe multi-file rename | `gitnexus_rename({symbol_name: "old", new_name: "new", dry_run: true})` |
| `cypher` | Custom graph queries | `gitnexus_cypher({query: "MATCH ..."})` |

## Impact Risk Levels

| Depth | Meaning | Action |
|-------|---------|--------|
| d=1 | WILL BREAK — direct callers/importers | MUST update these |
| d=2 | LIKELY AFFECTED — indirect deps | Should test |
| d=3 | MAY NEED TESTING — transitive | Test if critical path |

## Resources

| Resource | Use for |
|----------|---------|
| `gitnexus://repo/vitruvius/context` | Codebase overview, check index freshness |
| `gitnexus://repo/vitruvius/clusters` | All functional areas |
| `gitnexus://repo/vitruvius/processes` | All execution flows |
| `gitnexus://repo/vitruvius/process/{name}` | Step-by-step execution trace |

## Self-Check Before Finishing

Before completing any code modification task, verify:
1. `gitnexus_impact` was run for all modified symbols
2. No HIGH/CRITICAL risk warnings were ignored
3. `gitnexus_detect_changes()` confirms changes match expected scope
4. All d=1 (WILL BREAK) dependents were updated

## Keeping the Index Fresh

After committing code changes, the GitNexus index becomes stale. Re-run analyze to update it:

```bash
npx gitnexus analyze
```

If the index previously included embeddings, preserve them by adding `--embeddings`:

```bash
npx gitnexus analyze --embeddings
```

To check whether embeddings exist, inspect `.gitnexus/meta.json` — the `stats.embeddings` field shows the count (0 means no embeddings). **Running analyze without `--embeddings` will delete any previously generated embeddings.**

> Claude Code users: A PostToolUse hook handles this automatically after `git commit` and `git merge`.

## CLI

| Task | Read this skill file |
|------|---------------------|
| Understand architecture / "How does X work?" | `.claude/skills/gitnexus/gitnexus-exploring/SKILL.md` |
| Blast radius / "What breaks if I change X?" | `.claude/skills/gitnexus/gitnexus-impact-analysis/SKILL.md` |
| Trace bugs / "Why is X failing?" | `.claude/skills/gitnexus/gitnexus-debugging/SKILL.md` |
| Rename / extract / split / refactor | `.claude/skills/gitnexus/gitnexus-refactoring/SKILL.md` |
| Tools, resources, schema reference | `.claude/skills/gitnexus/gitnexus-guide/SKILL.md` |
| Index, status, clean, wiki CLI commands | `.claude/skills/gitnexus/gitnexus-cli/SKILL.md` |

<!-- gitnexus:end -->

## Active Sprint (2026-04-15)

**Sprint Q — Live Wiring & 8GB Hardening** is code-complete and
tagged `sprint-q-closed` at commit `c3eb939` on branch
`feat/sprint-q-live-wiring`. Live PD 1096 RSS/latency bench is
deferred to a manual operator run. See AD-024 for the ledger.

**Sprint R — Per-Layer Embeddings & Agentic** is code-complete on
branch `feat/sprint-r-per-layer-embeddings`:

- Stream Y0 — `features.y_*` flags + `priming/` subpackage shell.
- Stream Y1 — context vector builder (`all-MiniLM-L6-v2`),
  prompt prefix injector, cosine drift detector, ontology prompt
  identity propagation, SVO candidate fingerprint propagation.
- Stream Y2 — deterministic domain classifier, `route_with_moe`,
  MoE policy loader + `config/moe_routing.yaml`, flag-gated
  `select_review_model` hook.
- Stream Y3 — strict CoT parser (`parse_cot_strict`), append-only
  `cot_audit` writer, `adjudicate_with_cot` hook, `ple-cotrace-dump`
  CLI.
- Stream Y4 — SQLite stateful verdict registry (closes the Phase 6A
  Resume gap at root), flag-gated `review_with_cache`,
  `ple-registry-purge` CLI.
- Stream Y5 — Ollama vision OCR wrapper (mocked in tests),
  `extract_tables_with_vision_fallback` flag-gated hook in
  `table_graph_extractor`, `ple-vision-probe` hardware pre-flight CLI.

See AD-025 (in-progress) for the full commit ledger.

All `y_*` flags default false; with every flag off, the pipeline is
byte-identical to the pre-Sprint-R baseline.

### Stream Y5 manual activation checklist

Vision OCR never auto-activates. To turn it on:

1. Install `psutil`: `pip install psutil` (needed by `ple-vision-probe`).
2. Install `Pillow` if not present: `pip install pillow`.
3. Pull a ≤2B-param vision model on the local Ollama host:
   ```
   ollama pull moondream:latest   # ~1.8 GB Q4
   # OR
   ollama pull qwen2-vl:2b        # ~2.1 GB Q4
   ```
4. Run the pre-flight probe:
   ```
   python3 scripts/pipeline_cli.py ple-vision-probe \
       --required-free-gb 3.5 --model moondream:latest
   ```
   Exit 0 = PASS; 1 = not enough free RAM; 2 = model not pulled; 3 = psutil missing.
5. Only after the probe reports PASS, flip
   `features.y_vision_ocr: true` in `config/vitruvius.yaml`. The
   Stream B table extractor will then call the vision model as a
   last-resort fallback when CSV/XLSX extraction fails.

**Next gates:**

1. Archive `per-layer-embeddings-agentic-upgrade-plan.md` once this
   commit lands.
2. Start Sprint H (3D Spatial Intelligence) — blocked on ≥25 verified
   relationships; currently at 7. Run the live Ollama pipeline on PD
   1096 IRR to grow the count per governing plan Task 4a.
3. TDD-expand the design-spec plans (phase-13 HP, phase-14 WIKI,
   phase-15 GEOM, phase-16 PHYS, phase-12 Z, phase-8b GT) before
   dispatching their sprints, per governing plan Task 6.

If you are a subagent opening this repo fresh, read the governing
plan first (`.ai/03_plans/00-governing-implementation-plan.md`)
before choosing which task to execute.
