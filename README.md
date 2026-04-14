# Vitruvius

**Local-first knowledge engine** that transforms Philippine building laws and
regulations into a validated, queryable knowledge graph.

Vitruvius is not a RAG wrapper. It enforces a hard boundary between raw text,
candidate signals, and canonical truth — and treats every transformation as
auditable. The pipeline is **deterministic-first**: AI is the exception, not
the rule. On the active PD 1096 corpus, a full end-to-end run touches the
local LLM (Ollama / `gemma4:e4b`) roughly **4 times** — vs. ~25 in the
pre-deterministic-filter era.

> **Looking for the deep docs?** The knowledge base lives in
> [`.ai/`](./.ai/). Start with
> [`.ai/01_roadmap/master-roadmap.md`](./.ai/01_roadmap/master-roadmap.md)
> for the authoritative phase contract. This README is the tourist map;
> `.ai/` is the terrain.

---

## Table of contents

- [Quick start](#quick-start)
- [Architecture at a glance](#architecture-at-a-glance)
- [Filesystem layers](#filesystem-layers)
- [Pipeline stages](#pipeline-stages)
- [CLI commands](#cli-commands)
- [Deterministic-first design](#deterministic-first-design)
- [The `.ai/` knowledge base](#the-ai-knowledge-base)
- [Module map](#module-map)
- [Testing](#testing)
- [Dependencies](#dependencies)
- [Current status](#current-status)
- [Principles](#principles)

---

## Quick start

```bash
# 1. Install dependencies (minimal path — CLI works without PDF/OCR deps)
pip3 install PyYAML pytest

# 2. Install ingestion deps only if you need to run scan/convert/ocr
pip3 install -r requirements.txt

# 3. Run the test suite
PYTHONPATH=scripts python3 -m pytest scripts/tests/ -v

# 4. Inspect a single CLI command
PYTHONPATH=scripts python3 scripts/pipeline_cli.py --help

# 5. Run a real stage — refine all raw markdown through Tier A/B rules
PYTHONPATH=scripts python3 scripts/pipeline_cli.py refine

# 6. Enrich all placeholder concepts (zero LLM calls)
PYTHONPATH=scripts python3 scripts/pipeline_cli.py enrich-concepts
```

**Note on the CLI:** `pipeline_cli.py` uses lazy imports (AD-015), so
`promote --help` and similar commands work without `opendataloader_pdf`,
`pypdf`, or `ocrmypdf` installed. Only commands that actually touch those
libraries will require them at call time.

---

## Architecture at a glance

```
┌─────────────────────────────────────────────────────────────┐
│ 001_Raw-Source-Layer        immutable input (PDF/DOCX/XLSX) │
│         │                                                   │
│         ▼   scan → status → lint                            │
│ 006_System-Manifests        registries, runs, snapshots    │
│         │                                                   │
│         ▼   convert / ocr / office / spreadsheets           │
│ 002_Raw-Conversion-Layer    raw_markdown + sidecar_json    │
│         │                                                   │
│         ▼   refine (Phase 1C, deterministic)                │
│         │   → refined_markdown + .refined.json              │
│         │                                                   │
│         ▼   canonicalize / concepts / enrich-concepts      │
│ 003_Canonical-Knowledge-Layer                               │
│   ├── shared/sources/       canonical source records        │
│   ├── shared/concepts/      Knowledge Nodes (enriched)      │
│   └── shared/relationships/ promoted edges w/ audit trail   │
│         │                                                   │
│         ▼   extract-relationships-sections + dedup          │
│         ▼   pre-review filter (deterministic)               │
│         │                                                   │
│         ├─→ auto_accept → Phase 7 promote (no LLM)          │
│         ├─→ auto_reject → audit log (no LLM)                │
│         └─→ needs_review → Tier-1 LLM review (Phase 6A)     │
│                         └─→ uncertain → Tier-2 (Phase 6B)  │
│                                     └─→ human review       │
└─────────────────────────────────────────────────────────────┘
```

Every deterministic box on the left is **zero LLM**. The only AI involvement
is Tier-1 + Tier-2 review of the `needs_review` bucket (typically 22% of
post-dedup candidates, thanks to the pre-review filter — see AD-018 and AD-021).

---

## Filesystem layers

The project's state lives entirely in numbered directories. There is no
hidden database. This is **Principle P1: the filesystem is the database**.

| Layer | Folder | Role |
|---|---|---|
| 1 | `001_Raw-Source-Layer/` | Immutable input. Original PDFs, Office docs, spreadsheets. Git-ignored. |
| 2 | `002_Raw-Conversion-Layer/` | Machine extracts. `raw_markdown/`, `refined_markdown/`, `sidecar_json/`, `ocr_pdf/`. |
| 3 | `003_Canonical-Knowledge-Layer/` | Trusted knowledge. `shared/sources/`, `shared/concepts/`, `shared/relationships/`. |
| 4 | `004_Derived-Content-Layer/` | Learner-facing output (articles, flashcards). Not yet active. |
| 5 | `005_Operational-Intelligence-Layer/` | Graph, chunks, embeddings, indices. Reserved for Phase 8+. |
| 6 | `006_System-Manifests/` | Registries, run reports, audit logs. The audit trail. |

---

## Pipeline stages

The pipeline is a sequence of idempotent `run_*` stages. Each stage reads
from the previous layer(s) and writes to one or more output layers. Every
stage is re-runnable without producing duplicates (Principle P3).

| Stage | CLI | Module | AI? |
|---|---|---|---|
| Scan | `scan` | `scripts/vitruvius/scanner.py` | No |
| Status | `status` | `scripts/vitruvius/status.py` | No |
| Lint | `lint` | `scripts/vitruvius/linting.py` | No |
| Convert | `convert` / `convert-one` | `scripts/vitruvius/conversion.py` | No |
| OCR | `ocr-queue` / `ocr-execute` | `scripts/vitruvius/ocr.py` | No |
| Reconcile | `reconcile` | `scripts/vitruvius/reconcile.py` | No |
| Refine | `refine` / `refine-one` | `scripts/vitruvius/normalization/refine.py` | No |
| Canonicalize | `canonicalize` / `canonicalize-one` | `scripts/vitruvius/canonicalize.py` | No |
| Concept seed | `canonicalize-concept-one` | `scripts/vitruvius/concepts.py` | No |
| Concept enrichment | `enrich-concept-one` / `enrich-concepts` | `scripts/vitruvius/concept_enrichment.py` | No |
| Relationship extraction | `extract-relationships-one` / `extract-relationships-sections-one` | `scripts/vitruvius/relationships*.py` | No |
| Pre-review filter | (automatic inside review) | `scripts/vitruvius/pre_review_filter.py` | No |
| Tier-1 review | `review-relationships-ollama` | `scripts/vitruvius/ollama_review.py` | **Yes** |
| Tier-2 review | `review-relationships-ollama-second-pass` | `scripts/vitruvius/ollama_review_second_pass.py` | **Yes** |
| Promote | `promote` | `scripts/vitruvius/promotion.py` | No |
| Migrate IDs | `migrate-ids-plan` / `migrate-ids-apply` | `scripts/vitruvius/migrations.py` | No |

---

## CLI commands

All commands flow through `scripts/pipeline_cli.py`. Run `--help` on any
command for its flags.

### Ingestion stages
- `scan` — build the raw-file registry and tree snapshot
- `status` — diff the two latest registries
- `lint` — check raw-layer hygiene
- `run` — scan + status + lint (minimal default, no Ollama)
- `run-with-review` — full pipeline ending with Tier-1 review (opt-in)
- `convert` / `convert-one` — PDF → Markdown via OpenDataLoader
- `convert-spreadsheet-one` — XLSX → CSV/JSON via openpyxl
- `detect-one` — classify a PDF as TEXT_PDF or LIKELY_SCANNED_PDF
- `ocr-queue` / `ocr-execute` — queue and run OCRmyPDF
- `reconcile` — detect stale outputs

### Refinement, canonicalization, concepts
- `refine` / `refine-one` — run Tier A/B normalization rules (Phase 1C)
- `canonicalize` / `canonicalize-one` / `canonicalize-plan-one` — generate canonical source records
- `canonicalize-concept-one` — create a new placeholder concept file
- `enrich-concept-one` / `enrich-concepts [--force]` — promote placeholder concepts to Knowledge Nodes (Phase 3C, zero-LLM)

### Extraction, review, promotion
- `extract-relationships-one` — regex extraction over canonical markdown
- `extract-relationships-sections-one` — section-anchored extraction (preferred)
- `review-relationships-ollama [--model M] [--parallel N]` — Tier-1 LLM review with built-in pre-review triage (Phase 6A)
- `review-relationships-ollama-second-pass [--model M]` — Tier-2 adjudication (Phase 6B)
- `promote [--execute] [--rollback BATCH_ID]` — Phase 7 governance layer; dry-run default

### ID migration
- `migrate-ids-plan` — compute ID migration plan from `id_migration_map.yaml`
- `migrate-ids-apply` — apply the plan

---

## Deterministic-first design

The project's defining principle is that **LLMs are a last resort, not a
first pass**. Every stage that can be done with regex, rules, or schema
validation is done without LLM involvement. The LLM is reserved for the
residual cases where deterministic logic cannot decide.

Concrete mechanisms that enforce this:

1. **Pre-review filter** (`pre_review_filter.py`) — triages regex-extracted
   candidates into `auto_accept` / `auto_reject` / `needs_review` buckets
   before any LLM call. Rules: registry compatibility, self-reference check,
   evidence length, structural governs pattern, definitional anchor, high
   recurrence, concept→concept requires pattern, endpoint-in-evidence check.
   Real-data impact on PD 1096: **78% of candidates bypass the LLM entirely**.

2. **Deterministic definition extraction** (`concept_definitions.py`) —
   anchor-based (`shall mean`, `is defined as`, etc.) + section-title-based
   with a 14-entry alias dictionary. **16 out of 20 PD 1096 concepts enriched
   with zero LLM calls.**

3. **Phase 7 Promotion Validator** (`promotion_validator.py`) — 17 rules
   including closed predicate vocabulary, compatibility pairs, evidence
   integrity, trust propagation, audit integrity. Rejects bad records
   without asking the LLM.

4. **Registry-aware regex dedup** (`relationships_sections.py::dedupe_by_endpoints`) —
   collapses 5 predicate variants per edge into 1 before the reviewer sees
   them. On refined PD 1096: 23 candidates → 9 candidates (−61%).

5. **Lazy CLI imports** (`pipeline_cli.py`) — the CLI doesn't even import
   PDF libraries unless you're running a PDF stage. A minimal install can
   run `promote`, `refine`, `enrich-concepts` without heavyweight deps.

---

## The `.ai/` knowledge base

This project's long-form documentation lives in `.ai/`. It is authoritative
and version-controlled alongside the code.

| Path | Contents |
|---|---|
| [`.ai/00_system/`](./.ai/00_system/) | Architecture, principles, pipeline overview, naming conventions |
| [`.ai/01_roadmap/`](./.ai/01_roadmap/) | **Master roadmap**, milestone tracker, current sprint |
| [`.ai/02_audits/`](./.ai/02_audits/) | Code-forensic audits (2026-04-13 pack covers ingestion, extraction, normalization, review) |
| [`.ai/03_plans/`](./.ai/03_plans/) | Active phase plans + `INDEX.md` |
| [`.ai/06_specs/`](./.ai/06_specs/) | Schemas: source, concept, relationship |
| [`.ai/07_experiments/`](./.ai/07_experiments/) | Experiment writeups with real-data findings |
| [`.ai/08_prompts/`](./.ai/08_prompts/) | LLM prompt reference files (Tier-1 Gemma, Tier-2 Qwen design) |
| [`.ai/09_archive/`](./.ai/09_archive/) | **Completed plans** (Phase 7, 1C, 2, 6A, 6B, 3C, polish) |
| [`.ai/10_state/`](./.ai/10_state/) | Live state: `active_context.md`, `decisions.md`, `known_issues.md`, `system_state.json`, `pipeline_state.json` |

**If you only read one file**: `.ai/01_roadmap/master-roadmap.md` (v2.0.0) is
the authoritative roadmap and contains the honest status matrix (§4) and
governance contracts (§3).

**If you're looking for "why"**: `.ai/10_state/decisions.md` has the complete
architectural decision log (AD-001 through AD-021 as of 2026-04-14).

---

## Module map

All core logic lives in `scripts/vitruvius/`. The package is organized by
pipeline stage, not technical layer.

### Foundation
- `constants.py` — layer name constants
- `paths.py` — path resolution helpers (`get_repo_root`, `ensure_*`, `build_*_relative_path`)
- `utils.py` — timestamp + legacy normalization helpers (the `normalize_text` / `normalize_filename` are deprecated; see `normalization/`)
- `reports.py` — JSON/CSV/TXT writers, registry readers
- `models.py` — `FileEntry` dataclass
- `config.py` — central config loader for `config/vitruvius.yaml`

### Ingestion
- `scanner.py` — raw-layer file discovery
- `status.py` — registry diff
- `linting.py` — raw-layer hygiene
- `detection.py` — PDF text vs. scanned classification
- `conversion.py` — PDF → Markdown via OpenDataLoader
- `office.py` — DOCX/PPTX → PDF via LibreOffice
- `spreadsheets.py` — XLSX → CSV/JSON via openpyxl
- `ocr.py` — OCRmyPDF queue + execution
- `reconcile.py` — stale-output detection

### Refinement (Phase 1C)
- `normalization/__init__.py`
- `normalization/engine.py` — `NormalizationEngine` + `NormalizationRule` protocol
- `normalization/rules_tier_a.py` — 5 lossless rules (NFC, control-char strip, CRLF, whitespace, blank-line collapse)
- `normalization/rules_tier_b.py` — 3 structural rules (Setext→ATX, SEC.→SECTION, heading whitespace)
- `normalization/refine.py` — `run_refine`, `run_refine_one`, manifest writer

### Canonicalization
- `canonicalize.py` — rules-engine-driven source-record generator with structured sections, diff-before-write
- `canonical_diff.py` — `should_overwrite` with volatile-field stripping
- `concepts.py` — placeholder concept file generator

### Concept enrichment (Phase 3C)
- `concept_definitions.py` — regex anchor + section-title extractors with alias dict
- `concept_aliases.py` — parenthetical abbreviation + "also known as" miners
- `concept_enrichment.py` — orchestrator for the deterministic enrichment pipeline

### Extraction, review, promotion
- `relationships.py` — regex extractor (simpler, older)
- `relationships_sections.py` — section-anchored extractor + `dedupe_by_endpoints`
- `pre_review_filter.py` — deterministic triage (A1/A2/A3/A4, R1/R2/R5/R7)
- `review_routing.py` — entry-criteria filter + post-Tier-2 decision router
- `ollama_review.py` — Tier-1 LLM review with retry/resume/parallel support
- `ollama_review_second_pass.py` — Tier-2 adjudication orchestrator
- `promotion_validator.py` — 17-rule validator + canonical index builder
- `promotion.py` — `run_promote` with dry-run, merge, audit log, rollback

### Rules data
- `rules/canonical_rules.yaml` — path-to-ID mapping for canonicalization
- `rules/relationship_registry.yaml` — closed predicate vocabulary + compatibility

---

## Testing

```bash
# Run the full suite
PYTHONPATH=scripts python3 -m pytest scripts/tests/

# Run a single test file
PYTHONPATH=scripts python3 -m pytest scripts/tests/test_pre_review_filter.py -v

# Run only integration tests
PYTHONPATH=scripts python3 -m pytest scripts/tests/test_integration_e2e.py -v
```

The test suite is organized by module, with one `test_<module>.py` per
vitruvius module plus a dedicated `test_integration_e2e.py` that exercises
multi-module flows (extract → dedup → pre-filter → promote → enrich).

**As of 2026-04-14: 177 tests passing**, 2 intentional deprecation warnings
from `utils.normalize_*` usage in their own test file.

The integration tests include:
- Full-pipeline determinism check (byte-identical outputs on re-run modulo
  timestamps)
- Dedup composition closure (`dedupe(dedupe(x)) == dedupe(x)`)
- Pre-review filter composition closure

These catch cross-module regressions that unit tests would miss.

---

## Dependencies

The CLI is designed to work with only the dependencies you actually use.

**Always required:**
- `PyYAML` — config + YAML frontmatter parsing
- `pytest` — test runner

**Only required for ingestion / conversion:**
- `pypdf` — PDF page reading for detection
- `opendataloader-pdf` — PDF → Markdown conversion
- `ocrmypdf` — OCR processing of scanned PDFs
- `openpyxl` — XLSX parsing
- `pandas` — CSV handling (via `reports.py`)

**For review stages:**
- **Ollama** running locally at `http://127.0.0.1:11434` (configurable in
  `config/vitruvius.yaml`) with at least `gemma4:e4b` pulled. The review
  layer is fully opt-in via the `review-relationships-ollama*` commands.

Install everything:
```bash
pip3 install -r requirements.txt PyYAML pytest
```

Install minimal (CLI + tests, no PDF/OCR deps):
```bash
pip3 install PyYAML pytest
```

---

## Sprint Q — Live Wiring & 8GB Hardening

Sprint Q (shipped 2026-04-15) wires the Sprint D Stream F / G scaffolds
into the live review + promotion paths behind twelve `w_*` feature
flags that default **false**. With every flag off the pipeline is
byte-identical to the pre-Sprint-Q baseline (regression test at
`scripts/tests/test_wiring_backcompat.py`).

To enable the full wired chain on an 8 GB M2 machine (requires
`qwen2.5:7b` or smaller already pulled in Ollama):

```yaml
# config/vitruvius.yaml
review:
  ollama:
    num_ctx_cap: 4096            # hard cap enforced by w_llm_num_ctx_enforcement
    model_pool:
      tier_0_draft: phi3:mini
      tier_1_default: qwen2.5:7b
      tier_2_heavy: gemma4:31b
features:
  w_llm_model_pool: true
  w_llm_num_ctx_enforcement: true
  w_llm_context_budget_guard: true
  w_llm_binary_mode: false        # optional — compact True/False prompt
  w_review_nb_prefilter: true     # short-circuit LLM on obvious accepts/rejects
  w_review_ontology_prompt: true  # prepend Phase 8 neighborhood to the prompt
  w_review_slm_routing: true      # route simple candidates to the draft model
  w_review_conformal_routing: true
  w_review_tension_reflection: true
  w_review_choquet_aggregator: true
  w_promotion_stringency_gate: true
  w_graph_governing_standard: true
```

Any flag can be left off individually to disable that capability
without redeploying. The authoritative task list, stream-by-stream
gates, and AD-024 decision ledger live in
`.ai/03_plans/live-wiring-and-8gb-hardening-plan.md` and
`.ai/10_state/decisions.md`.

## Current status

As of 2026-04-14 (the authoritative status is `.ai/01_roadmap/master-roadmap.md` §4):

| Phase | Status | Notes |
|---|---|---|
| 0. Foundation | ✅ Complete | — |
| 1A. Baseline Ingestion | ✅ Complete | Known gaps: no file hashing, sequential OCR |
| 1B. Multi-Parser Integration | 📝 Planned | Detailed plan in `.ai/03_plans/` |
| 1C. Centralized Normalization | ✅ MVP Complete | 8 Tier A/B rules + manifest, deferred: Tier C semantic rules |
| 2. Canonicalization | ✅ Complete | Structured sections restored, diff-before-write |
| 3C. Concept Enrichment | ✅ 16/20 (80%) | Deterministic, zero LLM |
| 4. Identity Cleanup | ✅ Complete | — |
| 5. Relationship Extraction | 🟡 Regex-grade | Section-aware + registry-aware dedup |
| 6A. Local LLM Review | ✅ Complete | Config-driven, retry, resume, parallel, pre-review filter |
| 6B. Second-Pass Review | ✅ Complete | Tier-2 orchestrator + agreement matrix + human worklist |
| 7. Promotion Governance | ✅ Complete | 17-rule validator, audit log, rollback |
| 8. Graph Contract & Indexing | 🔒 Gated | Needs ≥50 verified relationships (currently 6) |
| 9. Query & AI Layer | 🔒 Gated | Post-Phase-8 |
| 11. Dataset Expansion | 🔒 Gated | Post-Phase-7 stable |
| 12. AI-Augmented Reasoning | 🔒 Gated | Long-term |

**Current AI usage on PD 1096 corpus:**
- Tier-1 review calls: ~2 (pre-review filter handles the rest)
- Tier-2 review calls: ~1-2 (only uncertain Tier-1 output)
- Concept enrichment calls: 0 (fully deterministic)
- **Total: ~4 Ollama calls per full pipeline run**

---

## Principles

The project operates under ten non-negotiable principles, formalized in
`.ai/00_system/principles.md`:

1. **Filesystem is the database** — no hidden SQLite/pickle state
2. **Raw layer is immutable** — the pipeline never modifies `001_Raw-Source-Layer/`
3. **Idempotent stages** — every `run_*` command is safe to re-run
4. **Path-based traceability** — `001` → `002` → `003` paths mirror structurally
5. **Deterministic canonicalization** — IDs come from `canonical_rules.yaml`
6. **Immutable canonical IDs** — changes go through `migrate-ids-plan`
7. **Explicit concept vocabulary** — extraction only uses concepts in `003/shared/concepts/`
8. **Local-first AI** — cloud LLMs are opt-in only; the core review loop runs air-gapped
9. **No soft output** — any extracted candidate without `source_section_id` is rejected
10. **No schema-less growth** — new laws wait until Phase 7 validates existing PD 1096 data

---

## License & attribution

This project is meant to become the knowledge foundation for architecture
board-exam preparation tooling in the Philippines. Source documents (PD 1096,
the National Building Code, its IRR) are public-domain Philippine law.
Derived work and code are the author's.

---

## Further reading

- [`.ai/01_roadmap/master-roadmap.md`](./.ai/01_roadmap/master-roadmap.md) — authoritative roadmap (v2.0.0)
- [`.ai/00_system/architecture.md`](./.ai/00_system/architecture.md) — deeper architecture write-up
- [`.ai/06_specs/source-schema.md`](./.ai/06_specs/source-schema.md) — canonical source file schema
- [`.ai/06_specs/concept-schema.md`](./.ai/06_specs/concept-schema.md) — concept file schema
- [`.ai/06_specs/relationship-schema.md`](./.ai/06_specs/relationship-schema.md) — relationship file schema
- [`.ai/10_state/decisions.md`](./.ai/10_state/decisions.md) — architectural decision log
- [`.ai/07_experiments/2026-04-14-sprint-b-end-to-end-rerun.md`](./.ai/07_experiments/2026-04-14-sprint-b-end-to-end-rerun.md) — the end-to-end experiment that motivated AD-014 through AD-021
