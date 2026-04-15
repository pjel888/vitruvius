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

## Vitruvius: Compound AI System Definition

Vitruvius operates as a **Compound AI System**. It abandons the
monolithic LLM approach — where a single model is trusted to read,
reason, and calculate — in favor of a multi-component engine. The
generative AI is **subordinated to deterministic mathematical and
logical constraints**: it is a modular piece within a larger,
verifiable pipeline, never the final authority on a compliance
decision.

### 1. The Semantic Extractor (Generative Component)

- **Engine:** Local LLM via Ollama, default `gemma4:e4b`.
- **Function:** Natural language understanding and unstructured-input
  parsing. Translates messy human input (scanned LGU ordinances,
  fragmented client briefs, IRR text) into formal intermediate
  representations — JSON verdicts for the Tier-1/Tier-2 review layer,
  or `<logic>` Datalog fact sets when the Sprint Z
  `z_neuro_symbolic` flag is on.
- **Constraint:** Subordinated to deterministic verifiers. Every LLM
  verdict is cross-checked by:
  - the **pre-review filter** (`pre_review_filter.py`, 8 deterministic
    rules) — typically auto-accepts or auto-rejects ~78% of PD 1096
    candidates before the LLM sees them;
  - the **17-rule Phase 7 promotion validator**
    (`promotion_validator.py`) — rejects records that violate the
    closed predicate vocabulary, schema, audit integrity, or
    compatibility pairs regardless of what the LLM said;
  - optionally the **Sprint Z Rust Datalog evaluator**
    (`datalog_rs/` crate, `z_neuro_symbolic` flag) — rejects the
    LLM's verdict when the `<logic>` block fails to parse or fails to
    derive the conclusion from the facts.

### 2. The Mathematical Verifier (Deterministic Component)

- **Engine:** Z3 Theorem Prover + Rust/Wasm spatial kernels.
- **Function:** Geometric and logical verification of parametric
  constraints.
- **Components:**
  - **Z3 inequality compiler**
    (`scripts/vitruvius/geometric/inequality_compiler.py`) — compiles
    extracted parametric rules into a Z3 incremental solver and
    returns a `ComplianceVerdict` with the specific violating
    parameters.
  - **Z3 spatial constraint solver**
    (`scripts/vitruvius/spatial/constraint_solver.py`, Sprint H
    Stream L.5) — evaluates parametric spatial constraints against
    observed values.
  - **Rust Datalog evaluator**
    (`scripts/vitruvius/datalog_rs/`) — a pyo3 crate with a
    hand-rolled Datalog engine (shipped in Sprint Z S1.2 after
    `crepe` proved too fragile) that verifies the `<logic>` fact
    sets emitted by the LLM.
  - **Wasm spatial kernels**
    (`scripts/vitruvius/engine_rs/` workspace, compiled to
    `wasm32-unknown-unknown`, loaded via `wasmtime` in
    `compound/wasm_kernel.py`) — run geometric primitives
    (`aabb_intersects`) in a hermetic Wasm sandbox, suitable for
    constrained environments.
- **Constraint:** When the verifier returns `unsat`, the LLM's
  assumption is rejected. The `check_compliance` function in
  `inequality_compiler.py` collects every violating parameter, and
  the Datalog bridge in the ontology prompt directive rejects the
  verdict when the `<logic>` block cannot derive its stated
  conclusion. Both paths are live behind feature flags today.
- **Geometry representation:** 3D polyhedral meshes via `trimesh`
  + `manifold3d` (not strict CAD B-Rep — shipped in Sprint GEOM
  Stream GEOM.3). The mesh level-of-detail is sufficient for
  architectural envelope checks under PD 1096.

### 3. The Immutable Vault (Topological Component)

- **Engine:** RocksDB (via the `rocksdict 0.3.29` binding) +
  event-sourced graph + differential dataflow.
- **Function:** Maintains the persistent, uncorrupted state of
  Philippine architectural laws (PD 1096, its IRR) and historical
  precedents.
- **Components:**
  - **RocksDB-backed event store**
    (`scripts/vitruvius/graph/rocksdb_event_store.py`) — append-only
    log with primary (`event:{event_id}`) + secondary time-index
    (`ts:{timestamp}:{event_id}`) key layout. O(1) count via a
    reserved `meta:event_count` key. Flag
    `hp_rocksdb_event_store` defaults true as of AD-029.
  - **RocksDB-backed verdict cache**
    (`scripts/vitruvius/review/rocksdb_stateful_registry.py`) —
    keyed on `(source_hash, relationship_hash, model_version)` for
    Phase 6A Resume gap closure. Flag `hp_rocksdb_verdict_cache`
    defaults true as of AD-029.
  - **Differential dataflow**
    (`scripts/vitruvius/compound/differential_propagator.py` +
    `dependency_tracker.py`, Sprint Z Stream S3) — `propagate(deltas)`
    walks the `DependencyTracker` once per `Delta` batch, so
    downstream invalidation runs in **O(Δ)** in the size of the
    changed set, not in the total graph size. Amendments to PD 1096
    no longer require a full re-inference pass.
- **Constraint:** The vault's state is updated exclusively via the
  append-only event log; generative LLM inference is never invoked
  during graph mutation. Migration from the older SQLite backends
  is supported by `ple-kv-migrate --store {event,registry}`
  (idempotent, dry-run capable).

### 4. The Orchestrator (Control Component)

- **Engine:** Python control plane in `scripts/pipeline_cli.py` +
  `scripts/vitruvius/`.
- **Function:** Routes data streams between the Generative,
  Deterministic, and Topological components. Every stage is a
  re-runnable `run_*` handler with lazy imports (AD-015) so the CLI
  stays usable in minimal environments.
- **Constraint:** Enforces ingestion-layer invariants before state
  can transition between layers:
  - **Merkle directory hash** (`scripts/vitruvius/merkle_fs.py`,
    Sprint HP.1) — content-addressable lock over directory state;
    makes structural drift cheap to detect.
  - **SHA-256 file hash**
    (`scripts/vitruvius/scanner.py::_sha256_of_file`, RI-009 closed)
    — every file entry carries an immutable content hash.
  - **Z3 admission check** (`spatial/constraint_solver.py`,
    `geometric/inequality_compiler.py`) — parametric constraints
    must be SAT-checkable before they enter the canonical layer.
  - **Monte Carlo dropout uncertainty utility**
    (`scripts/vitruvius/graph/mc_dropout.py::compute_epistemic_uncertainty`,
    Sprint GT Stream GT.5.3) — computes the epistemic uncertainty
    of a Bayesian model head as the sample variance of MC-dropout
    predictions. The utility ships; wiring it into the ingestion
    gate as a hard admission threshold is follow-up work.

### Feature-flag map

All generative-vs-deterministic trade-offs are gated behind feature
flags in `config/vitruvius.yaml`. Flag-OFF behaviour is
byte-identical to the pre-Sprint-Q pipeline.

| Component | Flag | Default |
|---|---|---|
| Neuro-symbolic Datalog verification | `z_neuro_symbolic` | false |
| Adversarial reviewer swarm | `z_adversarial_swarm` | false |
| Differential dataflow | `z_differential_dataflow` | false |
| Wasm spatial kernel | `hp_wasm_kernels` | false |
| RocksDB event store | `hp_rocksdb_event_store` | **true** (AD-029) |
| RocksDB verdict cache | `hp_rocksdb_verdict_cache` | **true** (AD-029) |
| Merkle fs hash | `hp_merkle_fs` | false |
| Z3 inequality compiler | `geom_csp_compiler` | false |
| 3D envelope | `geom_envelope_3d` | false |
| Spatial constraint solver | `l_z3_constraint_solver` | false |

See `.ai/10_state/decisions.md` AD-028 (nine-sprint closure) and
AD-029 (RocksDB migration) for the per-sprint ledgers.

---

## Table of contents

- [Compound AI System Definition](#vitruvius-compound-ai-system-definition)
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
| [`.ai/09_archive/`](./.ai/09_archive/) | **Completed plans** — Phases 7/1C/2/6A/6B/3C/polish plus the 10 sprints closed this session: Q (live wiring), R (per-layer embeddings + agentic), PHYS (graph physics), H (3D spatial), GEOM (constraint engine), WIKI (synthesis), GT (geo-topological), HP (performance), Z (compound AI), HP.3-R (RocksDB KV migration). Also: research briefs under `.ai/09_archive/research/`. |
| [`.ai/10_state/`](./.ai/10_state/) | Live state: `active_context.md`, `decisions.md`, `known_issues.md`, `system_state.json`, `pipeline_state.json` |

**If you only read one file**: `.ai/01_roadmap/master-roadmap.md` (v2.0.0) is
the authoritative roadmap and contains the honest status matrix (§4) and
governance contracts (§3).

**If you're looking for "why"**: `.ai/10_state/decisions.md` has the complete
architectural decision log (AD-001 through AD-029 as of 2026-04-15). AD-024 through AD-029 cover the Sprint Q→Z→HP.3-R closure arc and the RocksDB migration bench ledger.

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

### Post-Sprint-D Compound AI stack

Six new subpackages layered on top of the Phase 0-7 modules above.
All are gated behind `features.*` flags in `config/vitruvius.yaml`
and default off (except `hp_rocksdb_*` per AD-029).

- `compound/` — Sprint Z reactive neuro-symbolic OS:
  - `adversarial.py` — Proposer/Inspector/Adjudicator swarm (S2)
  - `dspy_compiler.py` — metric-driven prompt compiler (S5)
  - `dependency_tracker.py` + `differential_propagator.py` — incremental dataflow (S3)
  - `logic_schema.py` — Pydantic envelope for `<logic>` Datalog fact sets (S1)
  - `wasm_kernel.py` — wasmtime loader for the `engine_rs` Wasm build
- `wiki/` — Sprint WIKI autonomous knowledge synthesis:
  - `docling_parser.py`, `kuzu_store.py`, `delta_tracker.py`, `synthesis_loop.py`, `ego_linter.py`, `ollama_client.py`, `llm_client.py`
- `geometric/` — Sprint GEOM buildable-envelope engine:
  - `inequality_compiler.py` (Z3), `envelope_2d.py` (shapely), `envelope_3d.py` (trimesh + manifold3d), `pareto_optimizer.py` (cvxpy)
- `foraging/` — Sprint GT Stream GT.5.2 Bloom filter foraging
- `priming/` — Sprint R Stream Y1 contextual priming (source identity vector, prompt prefix injector, drift detector)
- `bench/` — Sprint Q W4 + Sprint HP.3-R benchmark harnesses (live PD 1096 wall-clock + peak RSS; KV backend comparison)

Additions to existing subpackages:

- `graph/` — new modules: `contract.py` (GraphNode/Edge/TemporalEdge), `event_store.py` + `rocksdb_event_store.py` (event log + RocksDB variant), `graphsage.py` (HP.5 embeddings + loopholes detector), `temporal_query.py` (GT.3.2 versioned retrieval), `parquet_archiver.py` (GT.3.3), `mc_dropout.py` (GT.5.3 epistemic uncertainty), `physics.py` (Sprint PHYS), `merkle_fs.py` (HP.1, single-file module at package root)
- `review/` — new modules: `stateful_registry.py` + `rocksdb_stateful_registry.py` (Y4.1), `ontology_prompt_builder.py` (S1.3 neuro-symbolic directive), `cot_audit.py` (Y3), `slm_router.py`, `conformal.py`, `tension_analyzer.py`, `reflection_parser.py`, `choquet.py`
- `promotion/` — new modules: `bayesian_fusion.py`, `stringency_matrix.py`, `temporal_edges.py`
- `pre_review/` — new module: `nb_filter.py` (NB prefilter)
- `spatial/` — new modules: `spatial_edge_builder.py` (GT.4 decay-weighted edges), `proximity_jump.py` (GT.4), `constraint_solver.py` (L.5 Z3 SMT evaluator)
- `parsers/` — Phase 1B Foundation (`base_parser.py`, `document_taxonomy.py`, `quality_gates.py`, `orchestrator.py`, `opendataloader_parser.py`) shipped in Sprint C. Phase 1B Modernization Tranche 1 (`docling_parser.py`, `libreoffice_preprocessor.py`, `GATE-005`) is a TDD plan at `.ai/03_plans/2026-04-15-phase-1b-modernization-tdd-plan.md` ready to execute.

### Rust data plane

- `scripts/vitruvius/engine_rs/` — Cargo workspace (Sprint GT.1 + HP.4)
  - `core/` — pure Rust; compiles for native + `wasm32-unknown-unknown`; exports `SpatialPoint`, `LinearOctree`, and the Wasm `aabb_intersects` C-ABI function
  - `pyo3_shim/` — pyo3 bindings consumed by `scripts/vitruvius/compound/wasm_kernel.py` and the spatial modules
- `scripts/vitruvius/datalog_rs/` — pyo3 crate shipping a hand-rolled Datalog evaluator for Sprint Z Stream S1.2. Entry point: `evaluate_datalog(facts, rules)`. 7 Rust unit tests.

### TypeScript sibling subproject

- `spatial-daemon/` — Node.js 25 + vitest subproject at repo root (not inside `scripts/vitruvius/`). Implements GJK collision detection, AABB overlap, and a filesystem contract writer that the Python side consumes. Entry point: `spatial-daemon/src/cli.ts`. 20/20 vitest tests.

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

**As of 2026-04-15: 1396 Python tests passing, 1 skipped** — grew from 177 (pre-Sprint-D) via the Sprint D Streams A-I expansion and the subsequent 10 governing-plan sprints + the Sprint HP.3-R RocksDB KV migration. Also: **20 TypeScript tests passing** in the `spatial-daemon/` sibling subproject (vitest), and **10 Rust unit tests** across `scripts/vitruvius/engine_rs/core` and `scripts/vitruvius/datalog_rs/`.

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
  `config/vitruvius.yaml`) with `gemma4:e4b` (or another model in the
  pool) pulled. The review layer is fully opt-in via the
  `review-relationships-ollama*` commands.

**Compound AI stack (post-Sprint-Z, all optional / flag-gated except RocksDB):**
- `rocksdict==0.3.29` — RocksDB Python binding for the event store and
  verdict cache (Sprint HP.3-R, flags `hp_rocksdb_event_store` and
  `hp_rocksdb_verdict_cache` default **true** per AD-029)
- `z3-solver` — Z3 Theorem Prover for parametric constraint verification
  (Sprint GEOM + Sprint H Stream L.5)
- `trimesh` + `mapbox-earcut` + `manifold3d` — 3D polyhedral envelope
  (Sprint GEOM Stream GEOM.3)
- `shapely` — 2D envelope (Sprint GEOM Stream GEOM.2)
- `cvxpy` — Pareto optimizer (Sprint GEOM Stream GEOM.4)
- `wasmtime` — Wasm spatial kernel loader (Sprint HP.4, flag `hp_wasm_kernels`)
- `pyarrow` — Parquet archiver (Sprint GT Stream GT.3.3)
- `docling` — structured PDF parser (Sprint WIKI + Phase 1B Modernization Tranche 1)
- `kuzu` — hybrid graph store (Sprint WIKI)
- `sentence-transformers` — contextual priming embeddings (Sprint R Y1)

**Rust toolchain (optional, for the Rust data plane):**
- `rustc` / `cargo` 1.94+ via `~/.cargo/env`
- `maturin` for building pyo3 extensions
- Target `wasm32-unknown-unknown` for the Wasm spatial kernel build

Two Rust crates live in-tree:
- `scripts/vitruvius/engine_rs/` — Cargo workspace with `core/` (pure
  Rust, compiles for native + wasm32) and `pyo3_shim/` (pyo3 bindings
  that ship `SpatialPoint` + `LinearOctree` to Python).
- `scripts/vitruvius/datalog_rs/` — hand-rolled Datalog evaluator
  (Sprint Z Stream S1.2) with pyo3 bindings.

**TypeScript sibling subproject:**
- `spatial-daemon/` — Node.js 25 + vitest subproject implementing GJK
  collision detection, AABB overlap, and a filesystem contract
  writer that the Python side consumes.

Install the everyday path:
```bash
pip3 install -r requirements.txt PyYAML pytest
```

Install minimal (CLI + tests, no PDF/OCR deps):
```bash
pip3 install PyYAML pytest
```

---

## Feature-flag operation

The Compound AI stack landed behind feature flags over ten sprints
(Q, R, PHYS, H, GEOM, WIKI, GT, HP, Z, HP.3-R). Every capability is
opt-in by default except the two RocksDB KV backends
(`hp_rocksdb_event_store`, `hp_rocksdb_verdict_cache`), which were
flipped to `true` on 2026-04-15 after a bench measured them at
18.7× / 24.3× the SQLite baseline (see AD-029).

Flag-off behaviour is byte-identical to the pre-Sprint-Q baseline.
The regression gate for this invariant is
`scripts/tests/test_wiring_backcompat.py`.

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
  # Sprint Q — Live Wiring & 8GB Hardening
  w_llm_model_pool: true
  w_llm_num_ctx_enforcement: true
  w_llm_context_budget_guard: true
  w_review_nb_prefilter: true
  w_review_ontology_prompt: true
  w_review_slm_routing: true
  w_review_conformal_routing: true
  w_review_tension_reflection: true
  w_review_choquet_aggregator: true
  w_promotion_stringency_gate: true

  # Sprint Z — Compound AI (neuro-symbolic verification + adversarial + differential dataflow)
  z_neuro_symbolic: true
  z_adversarial_swarm: true
  z_differential_dataflow: true

  # Sprint HP — High-performance optimizations
  hp_merkle_fs: true
  hp_wasm_kernels: true
  hp_graphsage: true

  # Sprint GT — Geo-topological graph
  gt_temporal_graph: true
  gt_proximity_jump: true
  gt_spatial_edges: true

  # Sprint GEOM — Geometric constraint engine
  geom_csp_compiler: true
  geom_envelope_3d: true
```

The authoritative flag registry lives in
`scripts/tests/test_features.py::EXPECTED_FLAGS` — CI fails if a
flag is added to `config/vitruvius.yaml` without a corresponding
test-registry entry. See `.ai/10_state/decisions.md` AD-024 through
AD-029 for per-sprint ledgers including commit SHAs and bench
numbers.

## Current status

As of 2026-04-15 — after closing ten governing-plan sprints this session (Q, R, PHYS, H, GEOM, WIKI, GT, HP, Z, HP.3-R) plus a Phase 1B Modernization Tranche 1 TDD plan ready to execute. The authoritative status is `.ai/01_roadmap/master-roadmap.md` §4, and the per-sprint ledgers live in `.ai/10_state/decisions.md` AD-024 through AD-029 (AD-031 when Tranche 1 ships).

| Phase / Sprint | Status | Notes |
|---|---|---|
| 0. Foundation | ✅ Complete | — |
| 1A. Baseline Ingestion | ✅ Complete | SHA-256 file hashing closed RI-009; OCR parallelization tracked in Phase 1B §11 |
| 1B. Multi-Parser Integration | 🟡 Foundation shipped; Tranche 1 TDD plan ready | Parsers subpackage + `FileEntry.sha256` + orchestrator skeleton. Modernization Tranche 1 (Docling + LibreOffice preprocessor + GATE-005) plan at `.ai/03_plans/2026-04-15-phase-1b-modernization-tdd-plan.md`. Tranche 2 (Marker/Surya/ProcessPool/Golden Corpus) deferred until 8 GB M2 ML-dep feasibility is verified. |
| 1C. Centralized Normalization | ✅ MVP Complete | 8 Tier A/B rules + manifest; Tier C semantic rules deferred |
| 2. Canonicalization | ✅ Complete | Structured sections restored, diff-before-write |
| 3C. Concept Enrichment | ✅ 20/20 | All PD 1096 concepts carry `stringency_vector` frontmatter after Sprint Q W3 |
| 4. Identity Cleanup | ✅ Complete | — |
| 5. Relationship Extraction | 🟡 Regex + Stream E augmentation | spaCy SVO, CRF, TransE link predictor shipped in Sprint D Stream E; LLM-assisted extraction still future |
| 6A. Local LLM Review | ✅ Complete | Retry, resume, parallel, pre-review filter, Sprint R stateful verdict cache |
| 6B. Second-Pass Review | ✅ Complete | Tier-2 orchestrator + agreement matrix + Sprint Q Choquet fusion |
| 7. Promotion Governance | ✅ Complete | 17-rule validator, audit log, rollback; Sprint Q stringency-matrix gate live |
| 8. Graph Contract & Indexing | ✅ Subsumed by Sprint D Stream H | Extended by Sprint GT (temporal edges, Parquet archiver, spatial GraphRAG, Rust octree) |
| 9. Query & AI Layer | ✅ Subsumed by Sprint D Stream I | Streams J (query integration) + K (docs+CI) externally gated on Ranger dashboard + 2nd jurisdiction corpus |
| Sprint Q — Live Wiring & 8GB Hardening | ✅ Closed (tag `sprint-q-closed`) | Wired Stream F + G scaffolds live; 8GB LLM survival mode; stringency matrix rollout |
| Sprint R — Per-Layer Embeddings & Agentic | ✅ Closed (tag `sprint-r-closed`) | Contextual priming, MoE domain routing, thinking-mode CoT audit, stateful registry, vision OCR |
| Sprint PHYS — Graph Physics | ✅ Closed (tag `sprint-phys-closed`) | PageRank, Boltzmann stability, VF2 motif matcher, Shannon entropy, eigenvector cascade |
| Sprint H — 3D Spatial Intelligence | ✅ Closed (tag `sprint-h-closed`) | Spatial ingest, Z3 solver, IFC registry + OWL exporter, TypeScript sibling at `spatial-daemon/` |
| Sprint GEOM — Geometric Constraint Engine | ✅ Closed (tag `sprint-geom-closed`) | Z3 CSP, shapely 2D envelope, trimesh 3D envelope, cvxpy Pareto optimizer |
| Sprint WIKI — Autonomous Knowledge Synthesis | ✅ Closed (tag `sprint-wiki-closed`) | Docling parser, Kuzu store, delta tracker, synthesis loop, ego linter, Ollama client |
| Sprint GT — Geo-Topological Knowledge Graph | ✅ Closed (tag `sprint-gt-closed`) | pyo3 Rust `engine_rs` workspace, linear octree, temporal graph, Parquet archiver, spatial GraphRAG, MC dropout, Bloom foraging |
| Sprint HP — High-Performance Optimizations | ✅ Closed (tag `sprint-hp-closed`) | Merkle fs, SQLite event store (pivoted from RocksDB at the time), Wasm spatial kernels, GraphSAGE loopholes |
| Sprint Z — Compound AI Evolution | ✅ Closed (tag `sprint-z-closed`) | Neuro-symbolic Datalog bridge (`datalog_rs/` crate), adversarial swarm, differential dataflow, DSPy prompt compiler |
| **Sprint HP.3-R — RocksDB KV Migration** | ✅ **Closed (tag `sprint-hp3r-closed`)** | Completes HP.3 spec: `RocksDBEventStore` + `RocksDBStatefulReviewRegistry` + factory dispatch + `ple-kv-migrate` CLI + O(1) count optimization. Bench at n=10000: **18.7× faster event store, 24.3× faster verdict cache**. Flag defaults flipped to true per AD-029. |

**Current AI usage on PD 1096 corpus (unchanged by the Compound AI upgrades — the deterministic-first design predates them):**
- Tier-1 review calls: ~2 (pre-review filter handles the rest)
- Tier-2 review calls: ~1-2 (only uncertain Tier-1 output)
- Concept enrichment calls: 0 (fully deterministic)
- Sprint Z neuro-symbolic verification: 0 runtime cost (flag-off by default)
- **Total: ~4 Ollama calls per full pipeline run**

**Test suite as of 2026-04-15:** Python **1396 passed / 1 skipped**; TypeScript **20 passed** (`spatial-daemon/`); Rust unit tests **10 passed** (`engine_rs` + `datalog_rs`).

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
