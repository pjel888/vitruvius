---
plan_id: governing-implementation
phase: "Meta — Orchestration of All Active Plans"
title: "Governing Implementation Plan: Sprint Execution Order & Dependency Graph"
status: active
priority: highest
sprint: "Meta (Sprints Q/R/H/GT/HP/HP.3-R/WIKI/GEOM/PHYS/Z/1B-M1/1B-M2/RUST-PDF-1/1B-M3/DISTILL-1/RUST-MIG-1/AUDIT-1/PIPELINE-CLI/PQ-1/LSH-1 ALL CLOSED · queue empty · Sprint D residuals J/K externally gated)"
version: 3.0.0
plan_type: orchestration
created: 2026-04-15
last_updated: 2026-04-15
owner: Senior Systems Architect
takes_precedence_over:
  - "Any execution-order claim in any other plan — this document is the single source of truth for sprint order"
dependencies:
  - .ai/01_roadmap/master-roadmap.md
  - .ai/03_plans/INDEX.md
  - .ai/10_state/active_context.md
  - .ai/10_state/decisions.md
  - .ai/10_state/known_issues.md
---

# Governing Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL — Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` when dispatching a sprint. Steps use checkbox (`- [ ]`) syntax for tracking. This plan never writes code directly; it dispatches sub-plans.

**Goal:** Orchestrate execution of the 16 active sub-plans in `.ai/03_plans/` into a single dependency-correct, quality-gated sequence. Any agent reads this file first to decide what to work on, then opens the referenced sub-plan for the actual TDD steps.

**Architecture:** Meta-orchestration over the existing plan set. Each sprint dispatches one or more sub-plans. Sub-plans own their own TDD tasks; this plan owns the order, entry/exit gates, conflict resolutions, and sprint handoffs. Nothing in this plan duplicates sub-plan task detail.

**Tech Stack:** No new code is introduced by this plan. It consumes existing plan files and state snapshots.

---

## 1. Current Ground Truth (2026-04-15, 19:00 local)

### 1.1 What has shipped this session (2026-04-14 → 2026-04-15)
This plan was written 2026-04-15 with Sprint Q as the next action item. Since then, **21 sprints have closed in a single sustained session**. The sprint list below is authoritative; the plan inventory in §2 has been updated to match.

**Sprint closures (in execution order):**

| # | Sprint | Tag | AD | Headline result |
|---|--------|-----|----|-----------------|
| 1 | **Sprint Q** — Live Wiring & 8GB Hardening | `sprint-q-closed` | AD-024 | All 8 Stream F review modules + 3 Stream G promotion modules wired into live paths; 20/20 canonical concepts carry `stringency_vector` |
| 2 | **Sprint R** — Per-Layer Embeddings & Agentic Reasoning | `sprint-r-closed` | AD-025 | Y0–Y5 all shipped; Phase 6A Resume gap closed at root via Y4 stateful registry |
| 3 | **Sprint H** — 3D Spatial Intelligence Upgrade | `sprint-h-closed` | AD-026 | Streams L/M/N/O all 20 tasks shipped; `spatial_instance` nodes invisible under `features.l_spatial=false` |
| 4 | **Sprint GT** — Geo-Topological Rust Engine | `sprint-gt-closed` | AD-027 | GT.1 pyo3 bridge + GT.2 linear octree + GT.3 temporal graph + GT.4 spatial GraphRAG + GT.5 hardware hardening |
| 5 | **Sprint HP** — High-Performance Optimizations | `sprint-hp-closed` | AD-028 | HP.1 Merkle fs + HP.3 SQLite event sourcing + HP.4 Wasm kernels + HP.5 GraphSAGE loopholes; HP.2 AST chunking was absorbed by Stream C.2 earlier |
| 6 | **Sprint HP.3-R** — RocksDB KV Backend Migration | `sprint-hp3r-closed` | AD-029 | RocksDB 18.7× faster on event store, 24.3× faster on verdict cache at n=10000; defaults flipped to true |
| 7 | **Sprint WIKI** — Autonomous Knowledge Synthesis | `sprint-wiki-closed` | AD-030 | Docling parser + Kuzu store + delta tracker + LLM synthesis loop + ego-graph linter all shipped |
| 8 | **Sprint GEOM** — Geometric Constraint Engine | `sprint-geom-closed` | AD-030 | GEOM.1 inequality compiler + GEOM.3 2D+3D envelope + GEOM.4 IoU audit + Pareto optimizer |
| 9 | **Sprint PHYS** — Statistical Mechanics & Graph Physics | `sprint-phys-closed` | AD-030 | PHYS.1–PHYS.4 + orphan Stream O VF2 motif absorbed |
| 10 | **Sprint Z** — Compound AI Evolution | `sprint-z-closed` | AD-030 | S1 Datalog bridge + S2 adversarial swarm + S3 differential dataflow + S4 Wasm kernel + S5 DSPy compiler |
| 11 | **Meta — Docs Cleanup Sprint** | — | — | `.ai/00_system/` + `.ai/01_roadmap/` + `.ai/02_audits/` + `.ai/10_state/known_issues.md` all refreshed post-Sprint-Z |
| 12 | **Sprint 1B-M1** — Phase 1B Modernization Tranche 1 | `sprint-1b-m1-closed` | AD-031 | DoclingParser + LibreOfficePreprocessor + GATE-005 + orchestrator preprocessor wiring |
| 13 | **Sprint 1B-M2** — Phase 1B Modernization Tranche 2 (scoped) | `sprint-1b-m2-closed` | AD-032 | OCRPreprocessor + ParserOrchestrator.process_batch + GoldenCorpusBenchmark; marker/surya DEFERRED (disk at 95.2%, RAM 2.03 GB) |
| 14 | **Sprint RUST-PDF-1** — Rust PDF Ingestion Audit | `sprint-rust-pdf-1-closed` | AD-033 | **GO verdict.** lopdf-based `vitruvius_rust_pdf` crate measured at **13.7 MB peak RSS (48× smaller than docling) and 0.05s wall (625× faster)**. Unlocks low-spec target. |
| 15 | **Sprint 1B-M3** — Phase 1B Modernization Tranche 3 | `sprint-1b-m3-closed` | AD-034 | `RustPdfParser(BaseParser)` + GATE-006 min-chars-per-page + real-PDF quality rollback gate (LCS 0.9925 vs pypdf) |
| 16 | **Sprint DISTILL-1** — LLM Reviewer Distillation Audit | — | AD-035 | **DEFER_NO_DATA.** Audit harness committed for re-run; Sprint R Y4 verdict cache is empty (needs ≥50 live verdicts). Unblocker: run live review with `y_stateful_registry=true`. |
| 17 | **Sprint RUST-MIG-1** — Python→Rust Polyglot Split | `sprint-rust-mig-1-closed` | AD-036 + AD-037 + AD-038 + AD-038a | S1 `build_spatial_adjacency_edges` 200× raw kernel (O(n²) → O(n log n) via existing `LinearOctree`), S2 `weight_by_distance` 12.18× raw / 2.84× end-to-end, N4 Mahalanobis core 2.73× end-to-end via nalgebra. N1 Wasserstein DEFER_ALREADY_NATIVE (AD-038a) — thin POT wrapper over native C++ LP. Both `rust_mig_*` flags flipped to `true`. |
| 18 | **Sprint AUDIT-1** — Advanced Tech Audit | `sprint-audit-1-closed` | AD-039 | FlatBuffers NO_GO (5-10× SLOWER than CPython `_json` at ~150B records), Monte Carlo Dropout PARK (GraphSAGE is `torch.no_grad()` by design — no viable sites), Numerical Integrity GO_GAP (shipped SHA-256 integrity footer for spatial contracts via `spatial/contract_reader.py` + `spatial-daemon/src/contract_writer.ts`). Zero new Rust candidates surfaced. |
| 19 | **Sprint PIPELINE-CLI** — Phase 1B Flag Integration | `sprint-pipeline-cli-closed` | AD-040 | New `convert-parsers-one` subcommand wires all 5 `p1b_*` flags end-to-end via `parsers/factory.py::build_default_orchestrator()` and `parsers/cli_handler.py::run_convert_parsers_one()`. Parallel command pattern ensures byte-identity with flags OFF. Side-fix: `RustPdfParser` was in `__all__` but never imported (broken since AD-034). |
| 20 | **Sprint PQ-1** — GraphSAGE Product Quantization | `sprint-pq-1-closed` | AD-041 | 32× exact compression (256B/node → 8B/node, M=8, k=256, sub_dim=8 over 64-d float32). **0.00017 cosine similarity delta** (117× under the 0.02 gate). Pure numpy — zero Rust escalation. `hp_graphsage_pq` stays false pending embedding persistence layer. |
| 21 | **Sprint LSH-1** — MinHash Fuzzy Near-Duplicate Dedup | `sprint-lsh-1-closed` | AD-042 | Vectorized Carter-Wegman MinHash (70× faster than initial nested-loop — 8s → 108ms at n=1000). 14.17% fuzzy hit rate at 20% injection (>10% gate), 0 false positives on 200-candidate disjoint audit. Plan's `num_bands=4` was underpowered — tuned to `num_perm=256, num_bands=32, r=8` for 99% recall at J≥0.78. `w_lsh_dedup` stays false pending PD 1096 operator validation. |

**Test suite:** 1528 passing, 1 skipped (grew from 297 at session start — +1231 delta).

**Branch state:** Everything landed on `main`. Feature branch `feat/sprint-d-intelligence-upgrade` was merged and deleted along with 3 other stale branches during the docs cleanup sprint.

**Git remote:** Fixed `gh auth setup-git`; `origin` now authenticates and all sprint tags + closing commits are pushed. Most recent push: `d119604..3df5753`.

### 1.2 Dead-scaffold blocker — RESOLVED
Sprint Q closed the dead-scaffold problem that originally motivated this plan. All 8 Stream F review modules + 3 Stream G promotion modules now have live importers. No module is dead-coded anymore.

### 1.3 Sprint D residuals — still externally gated
- **J — Active Learning** (2 tasks). Still blocked on a Ranger dashboard outside this repo.
- **K — CLUP Scaling** (3 tasks). Still blocked on a second jurisdiction being ingested with ≥20 verified relationships.

Status unchanged from 2026-04-15 morning. No action until the external gate flips.

### 1.4 Plans that originally needed TDD expansion — all shipped
The seven `plan_type: design_spec` plans flagged in the original governing plan (phase-8B, phase-12, phase-13, phase-14, phase-15, phase-16, ultimate-architecture-upgrade) have all either **shipped** (12/13/14/15/16/8b) or been **archived as superseded** (ultimate-architecture). Task 6 ("TDD-expansion passes") is closed.

### 1.5 Queue status — fully closed 2026-04-15
Task 8 queue is fully closed. **5 of 5 optimization plans shipped** during the same session they were written in. See §2.2 for the archive roll-up and per-plan AD references. The Advanced Tech Audit (Sprint AUDIT-1) was re-ordered ahead of Sprint RUST-MIG-1 in the as-executed sequence relative to the plan, but both closed; the re-order had no downstream impact since RUST-MIG-1 surfaced zero Rust candidates from the audit anyway (AD-039). Next action is a **fresh roadmap brainstorm** — no plans are queued (see §10).

---

## 2. Plan Inventory (post-session reconciliation 2026-04-15 19:00)

**Active in `.ai/03_plans/`:** 2 files (governing + INDEX). All other previously-active plans (statistical-architectural-upgrade, phase-1b-multi-parser-integration, ingestion-refinement-contract) were archived on 2026-04-15 once their owning sprints closed or externally-gated residuals were preserved with defer notes.

**Archived in `.ai/09_archive/plans/`:** 21 closed sprints this session (see §1.1) + the 3 active-plan archivals landed 2026-04-15 19:00.

**Queue:** empty.

### 2.1 Active plans (drivers of next work)

| # | Plan ID | Type | Owning Sprint | Status |
|---|---------|------|---------------|--------|
| 1 | `governing-implementation` (this file) | orchestration | Meta | 🔥 Active — v3.0.0 |
| 2 | `INDEX.md` | (index) | — | ✅ Reconciled 2026-04-15 19:00 |

As of the 2026-04-15 19:00 cleanup pass, only the governing plan + INDEX remain in `.ai/03_plans/`. Every implementation / design_spec / contract plan has either shipped (and been archived) or been archived with a frozen defer note (statistical-architectural-upgrade's Streams J/K are externally gated — Ranger dashboard + second jurisdiction corpus).

### 2.2 Queued implementation plans — QUEUE FULLY CLOSED 2026-04-15

All 5 plans written 2026-04-15 have shipped. Table below is the authoritative sprint-by-sprint roll-up:

| # | Plan file | Type | Sprint | Tag | AD | Status | Archive path |
|---|-----------|------|--------|-----|----|--------|--------------|
| 1 | `2026-04-15-advanced-tech-audit-plan.md` | audit_then_conditional_implementation | **Sprint AUDIT-1** | `sprint-audit-1-closed` | AD-039 | ✅ Closed | `.ai/09_archive/plans/2026-04-15-advanced-tech-audit-plan.md` |
| 2 | `2026-04-15-rust-migration-audit-plan.md` | audit_then_conditional_implementation | **Sprint RUST-MIG-1** | `sprint-rust-mig-1-closed` | AD-036 + AD-037 + AD-038 + AD-038a | ✅ Closed | `.ai/09_archive/plans/2026-04-15-rust-migration-audit-plan.md` |
| 3 | `2026-04-15-pipeline-cli-integration-plan.md` | implementation_tdd | **Sprint PIPELINE-CLI** | `sprint-pipeline-cli-closed` | AD-040 | ✅ Closed | `.ai/09_archive/plans/2026-04-15-pipeline-cli-integration-plan.md` |
| 4 | `2026-04-15-graphsage-pq-embeddings-plan.md` | implementation_tdd | **Sprint PQ-1** | `sprint-pq-1-closed` | AD-041 | ✅ Closed | `.ai/09_archive/plans/2026-04-15-graphsage-pq-embeddings-plan.md` |
| 5 | `2026-04-15-lsh-dedup-plan.md` | implementation_tdd | **Sprint LSH-1** | `sprint-lsh-1-closed` | AD-042 (premise: AD-037) | ✅ Closed | `.ai/09_archive/plans/2026-04-15-lsh-dedup-plan.md` |

### 2.3 Closed sprints (archived in `.ai/09_archive/plans/` — reference only)

All 21 sprint plans listed in §1.1 are archived with `status: complete` frontmatter. They are cited by successor plans but never re-dispatched.

Also archived from the original inventory:
- `phase-8-graph-contract-indexing` — subsumed by Stream H (Sprint D)
- `phase-9-query-ai-layer` — subsumed by Stream I (Sprint D)
- `ultimate-architecture-upgrade` — superseded; all 15 streams distributed across successor plans that have now shipped
- `phase-1b-multi-parser-integration` — ✅ fully shipped via Foundation (Sprint C) + Tranches 1/2/3 (Sprints 1B-M1/M2/M3, AD-031/032/034) + §11 Phase 3 Scaling (Sprint PIPELINE-CLI, AD-040), archived 2026-04-15 19:00
- `statistical-architectural-upgrade` — Streams A–I all closed 2026-04-14; Streams J (active learning) + K (CLUP scaling) **externally gated** on Ranger dashboard + second-jurisdiction corpus (may never land). Archived 2026-04-15 19:00 with `archived_with_open_streams: "J,K"` frontmatter field preserving the defer status.
- `ingestion-refinement-contract` — frozen interface between Phase 1B ↔ Phase 1C; both sides shipped. Archived 2026-04-15 19:00 per user instruction to leave only governing plan + INDEX in the active plans folder.

---

## 3. Execution Order & Gate Matrix

### 3.1 Sprint dependency diagram (post-session, 2026-04-15 19:00)

```
Sprint Q   ✅ Live Wiring & 8GB Hardening
   │
   ├───► Sprint R   ✅ Per-Layer Embeddings & Agentic
   │
   ├───► Sprint H   ✅ 3D Spatial Intelligence
   │        │
   │        └───► Sprint GT   ✅ Geo-Topological Rust Vault
   │                 │
   │                 └───► Sprint HP   ✅ High-Performance Optimizations
   │                          │
   │                          ├───► Sprint HP.3-R  ✅ RocksDB KV Migration
   │                          │
   │                          └───► Sprint WIKI  ✅ Autonomous Knowledge Synthesis
   │                                   │
   │                                   └───► Sprint GEOM  ✅ Geometric Constraint Engine
   │                                            │
   │                                            └───► Sprint PHYS  ✅ Graph Physics
   │                                                     │
   │                                                     └───► Sprint Z  ✅ Compound AI Evolution
   │
   ├───► Meta Docs Cleanup Sprint   ✅ reconciled
   │
   ├───► Phase 1B Modernization (parallel track)
   │        ├───► Sprint 1B-M1   ✅ Tranche 1 (Docling + LibreOffice + GATE-005)
   │        ├───► Sprint 1B-M2   ✅ Tranche 2 scoped (OCR + process pool + GoldenCorpus)
   │        ├───► Sprint RUST-PDF-1  ✅ Rust PDF audit — GO verdict
   │        └───► Sprint 1B-M3   ✅ Tranche 3 (RustPdfParser + GATE-006 + 0.9925 quality)
   │
   ├───► Sprint DISTILL-1  ✅ LLM Distillation Audit — DEFER_NO_DATA (audit harness committed)
   │
   ├───► Task 8 queue (all five plans shipped in the same session)
   │        ├───► Sprint RUST-MIG-1       ✅ Python→Rust polyglot split (AD-036/037/038/038a)
   │        ├───► Sprint AUDIT-1          ✅ Advanced Tech Audit — FlatBuffers NO_GO + MC Dropout PARK + SHA-256 integrity GO (AD-039)
   │        ├───► Sprint PIPELINE-CLI     ✅ convert-parsers-one + p1b_* flag integration (AD-040)
   │        ├───► Sprint PQ-1             ✅ GraphSAGE PQ 32× compression, 0.00017 cosine delta (AD-041)
   │        └───► Sprint LSH-1            ✅ MinHash fuzzy dedup 14.17% hit / 0 FP (AD-042)
   │
   └───► Sprint D residuals   🔒 externally gated (Ranger + second-jurisdiction)

NEXT — (queue empty; see §10)
```

### 3.2 Gate matrix (historical — all closed except residuals + queued work)

Every sprint gate below has been satisfied. This table is retained for audit, so a future engineer can verify the pre-committed exit criteria were met for each closed sprint. For the **new** queued work, see §6 Task 8's per-plan entry/exit gates.

| Sprint | Entry Gate | Exit Gate | Status |
|--------|-----------|-----------|--------|
| **Q** | None — execute immediately | 8 Stream F + 3 Stream G modules imported into live paths; 20/20 concepts have `stringency_vector`; `test_livewiring_e2e.py` green; byte-identical output with flags OFF | ✅ closed (AD-024) |
| **R** | `sprint-q-closed` tag | Y0–Y5 shipped; Phase 6A Resume gap closed at root | ✅ closed (AD-025) |
| **H** | `sprint-q-closed` AND ≥25 verified relationships | L + M + N + O closed; backward-compat green with `features.l_*=false` | ✅ closed (AD-026) |
| **GT** | `sprint-h-closed` AND Rust toolchain | `engine_rs` crate shipped via pyo3; octree point query <1 ms/100k nodes | ✅ closed (AD-027) |
| **HP** | `sprint-gt-closed` | Merkle status <100 ms on 10k files; Wasm spatial kernel loadable from Python | ✅ closed (AD-028) |
| **HP.3-R** | `sprint-hp-closed` | RocksDB 18.7×/24.3× faster than SQLite at n=10000 (rocksdb_wins bucket); defaults flipped | ✅ closed (AD-029) |
| **WIKI** | `sprint-hp-closed` | Docling + Kuzu + delta tracker + LLM synthesis loop + ego-graph linter | ✅ closed (AD-030) |
| **GEOM** | `sprint-h-closed` AND `sprint-wiki-closed` | Inequality compiler + 2D/3D envelope + IoU audit + Pareto optimizer | ✅ closed (AD-030) |
| **PHYS** | Phase 8 stable | PageRank + Boltzmann + Shannon + eigenvector + VF2 orphan absorbed | ✅ closed (AD-030) |
| **Z** | `sprint-geom-closed` AND `sprint-phys-closed` | S1 Datalog + S2 adversarial swarm + S3 differential dataflow + S4 Wasm + S5 DSPy | ✅ closed (AD-030) |
| **1B-M1** | None | DoclingParser + LibreOfficePreprocessor + GATE-005 + orchestrator wiring | ✅ closed (AD-031) |
| **1B-M2** | `sprint-1b-m1-closed` | OCRPreprocessor + process_batch + GoldenCorpusBenchmark (marker/surya DEFERRED on evidence) | ✅ closed (AD-032) |
| **RUST-PDF-1** | None (audit) | Rust PDF parser ≥40× smaller RSS than docling on synthetic PDFs | ✅ GO verdict (AD-033) — 48× smaller, 625× faster |
| **1B-M3** | AD-033 GO verdict | RustPdfParser(BaseParser) + GATE-006 + quality rollback LCS ≥0.99 on real PDF | ✅ closed (AD-034) — LCS 0.9925 |
| **DISTILL-1** | None (audit) | ≥50 verdicts in cache → GO; <50 → DEFER_NO_DATA | ✅ DEFER_NO_DATA (AD-035) — verdict cache empty |
| **RUST-MIG-1** | Rust toolchain present (`rustup show` + `maturin --version`) | S1/S2/N4 ports land with ≥2× bench threshold; N1 either ports or DEFERs with rationale; `rust_mig_*` flags flipped true on passing ports | ✅ closed (AD-036+037+038+038a) — S1 200× raw, S2 12.18× raw / 2.84× end-to-end, N4 2.73× end-to-end; N1 DEFER_ALREADY_NATIVE (POT is native C++ LP) |
| **AUDIT-1** | None (audit) | FlatBuffers, MC Dropout, Numerical Integrity each produce GO / DEFER / NO_GO per pre-committed gates | ✅ closed (AD-039) — FlatBuffers NO_GO (5-10× slower than `_json`), MC Dropout PARK (GraphSAGE is deterministic), Integrity GO_GAP (SHA-256 footer shipped) |
| **PIPELINE-CLI** | None | End-to-end ingestion through each of the 5 `p1b_*`-flagged parsers on a representative PD 1096 section; byte-identity test with every flag OFF | ✅ closed (AD-040) — `convert-parsers-one` subcommand wires all 5 flags via `parsers/factory.py::build_default_orchestrator()` + `parsers/cli_handler.py::run_convert_parsers_one()`; parallel command pattern preserves byte-identity |
| **PQ-1** | None (GraphSAGE already ships via Sprint HP HP.5) | Cosine-similarity delta ≤ 0.02 on held-out set vs raw float32; 32× disk-footprint reduction measured end-to-end | ✅ closed (AD-041) — 0.00017 cosine delta (117× under gate); 256B→8B/node exact 32× compression; pure numpy |
| **LSH-1** | Sprint RUST-MIG-1 closed (AD-037 reframes plan premise) | Fuzzy hit rate ≥10% at 20% injection; 0 false positives on disjoint candidate audit | ✅ closed (AD-042) — 14.17% fuzzy hit rate at 20% injection (>10% gate); 0 FP on 200-candidate audit; vectorized Carter-Wegman MinHash 70× faster than nested-loop baseline |
| **D-residual J** | Ranger dashboard exists externally | J.1 + J.2 tasks closed | 🔒 externally gated |
| **D-residual K** | ≥1 non-PD-1096 jurisdiction fully ingested | K.1–K.3 tasks closed | 🔒 externally gated |

### 3.3 Non-blocking parallel track: Phase 1B Modernization — SHIPPED
`phase-1b-multi-parser-integration-plan.md` §11 Phase 2 (Modernization) landed in three tranches this session: Tranche 1 (Docling + LibreOffice), Tranche 2 scoped (OCR + process pool + GoldenCorpus; marker/surya deferred), and Tranche 3 (Rust PDF parser via lopdf with 0.9925 quality similarity). §11 Phase 3 (Scaling & Governance) is still open and is one of the drivers behind the pipeline_cli integration plan (§2.2 #7).

---

## 4. Cross-Plan Conflicts & Resolutions

### 4.1 Stream L naming collision (MUST fix before any Sprint H work)
- `statistical-architectural-upgrade-plan.md` — Stream L = Constraint Conflict Engine (CSP + Dempster-Shafer, 2 tasks).
- `ultimate-architecture-upgrade-plan.md` — Stream L = Spatial Reasoning (Z3 SMT, 11 tasks).
- `3d-spatial-intelligence-upgrade-plan.md` — Stream L = Spatial Ingestion + Z3 Solver.

**Resolution:**
1. **Canonical owner of the label `Stream L` = `3d-spatial-intelligence-upgrade-plan.md`** (Z3 spatial ingest).
2. Rename statistical plan's Stream L → **`Stream L_conf`** (constraint-conflict engine) everywhere in that file.
3. The ultimate plan's Stream L is strictly duplicative of 3d-spatial Stream L. Do not re-implement.

Task 1 applies this rename.

### 4.2 Stream N duplication (spatial daemon)
- `3d-spatial-intelligence-upgrade-plan.md` — Stream N = TypeScript/Node.js AABB+GJK daemon.
- `phase-8b-geo-topological-graph-plan.md` — Stream GT.2 = Rust linear octree via `pyo3`.

**Resolution:** Ship TS daemon first in Sprint H (fast to build, decouples geometry concerns). Sprint GT then *replaces* the TS daemon with the Rust engine. `phase-8b` already declares `takes_precedence_over: Stream N` — honor that. No code duplication because the TS daemon is a disposable scaffold.

### 4.3 Stream U (hardware router) overlaps Live-Wiring W1
- `ultimate-architecture-upgrade-plan.md` Stream U = psutil-driven model selection (`e2b` / `e4b` / `31b`).
- `live-wiring-and-8gb-hardening-plan.md` W1 = config-driven model pool + context budget enforcement.

**Resolution:** W1 closes first (it defines the config-driven pool). Stream U then slots into Sprint R alongside Y2 (domain routing MoE) as an additional router dimension: `(domain, complexity, free_ram) → model`. Do not execute Stream U in Sprint Q.

### 4.4 Orphan Stream O (VF2 + Boltzmann) in statistical plan
- Statistical plan lists Stream O (VF2 motif matcher + Boltzmann promotion gate) as PENDING, but no sprint in the original plan owns it.
- `phase-16-statistical-mechanics-graph-physics-plan.md` already owns PHYS.2 (Boltzmann stability).

**Resolution:** Fold orphan Stream O tasks into Sprint PHYS. Add a task to Sprint PHYS's TDD expansion (Task 6) that copies the VF2 motif matcher task from the statistical plan into `PHYS.2`. Mark statistical plan's Stream O as `moved_to: Sprint PHYS`.

### 4.5 Vision OCR double-install (Y5 vs WIKI.1.2)
- `per-layer-embeddings-agentic-upgrade-plan.md` — Y5 wraps a ≤2B-param vision model as an Ollama fallback for table/chart extraction in the spreadsheet path.
- `phase-14-autonomous-knowledge-synthesis-plan.md` — WIKI.1.2 uses Qwen2-VL for multimodal figure captions during PDF ingestion.

**Resolution:** Y5 ships first as a narrow fallback; WIKI.1.2 reuses the exact model registration (same `models.yaml` entry, same Ollama tag). No double install. WIKI.1.2 task list must reference Y5's model registration path.

### 4.6 `ultimate-architecture-upgrade-plan.md` is a legacy superset
Its 15 streams are now distributed across: 3D-Spatial (L, M, N), Sprint GT (M/N Rust engine), Sprint HP (O, P, Q, T), Sprint R (U router), Sprint PHYS (X). Its narrative is useful but its task list duplicates successors.

**Resolution:** Mark `ultimate-architecture-upgrade-plan.md` frontmatter `status: superseded` with a `successors:` list cross-referencing every target plan. Do **not** delete — it has useful scoping notes. Never dispatch it directly.

### 4.7 Phase 12 (Sprint Z) Neuro-Symbolic vs Live-Wiring ontology prompt
Phase 12 Stream S1 tells the LLM to output Datalog/Prolog rather than JSON. This contradicts Live-Wiring Stream W2 which wires the existing `review/ontology_prompt.py` (JSON-shaped). Sprint Z changes the output contract of `ollama_review.py`.

**Resolution:** Sprint Z must land behind a separate `features.z_neuro_symbolic` flag that *replaces* the review pipeline entry point, not edits it. Do not refactor `ollama_review.py`. Stream S1 introduces `ollama_datalog_review.py` as a sibling module. Live-Wiring remains authoritative unless the flag is flipped on.

---

## 5. Plans Requiring TDD Expansion Before Execution

These are `plan_type: design_spec` and **must be expanded to `implementation_tdd`** inside their own file before the owning sprint starts. Expansion is Task 6 below and is itself a sprint-0 activity for the owning sprint.

| Plan | Owning Sprint | Rough expansion size | Expansion trigger |
|------|---------------|---------------------|-------------------|
| `phase-1b-multi-parser-integration` (§11 Phase 2 & 3) | Parallel-track (any time) | ~22 tasks | Immediate — ready now |
| `phase-8b-geo-topological-graph` | Sprint GT | ~25 tasks | Before GT entry gate |
| `phase-13-high-performance-optimizations` | Sprint HP | ~20 tasks | Before HP entry gate |
| `phase-14-autonomous-knowledge-synthesis` | Sprint WIKI | ~18 tasks | Before WIKI entry gate |
| `phase-15-geometric-constraint-engine` | Sprint GEOM | ~18 tasks | Before GEOM entry gate |
| `phase-16-statistical-mechanics-graph-physics` | Sprint PHYS | ~14 tasks (+VF2 orphan) | Before PHYS entry gate |
| `phase-12-compound-ai-evolution` | Sprint Z | ~35 tasks | Before Z entry gate (stretch) |

`live-wiring-and-8gb-hardening`, `per-layer-embeddings-agentic-upgrade`, `3d-spatial-intelligence-upgrade`, and `statistical-architectural-upgrade` are already TDD-ready — dispatch directly.

---

## 6. Governing Execution Tasks

Each task below is at the "sprint dispatch" level, not line-level TDD. TDD tasks live in the sub-plan file each task references. Every task ends with a commit.

### ✅ Tasks 1–7 — CLOSED (all sprint dispatches shipped)

| Task | What it dispatched | Status |
|------|--------------------|--------|
| Task 1 — Reconcile plans, INDEX, roadmap | Plan + roadmap reconciliation | ✅ closed |
| Task 2 — Sprint Q dispatch | `live-wiring-and-8gb-hardening-plan.md` | ✅ closed (AD-024) |
| Task 3 — Sprint R dispatch | `per-layer-embeddings-agentic-upgrade-plan.md` | ✅ closed (AD-025) |
| Task 4 — Sprint H dispatch | `3d-spatial-intelligence-upgrade-plan.md` | ✅ closed (AD-026) |
| Task 5 — Sprint D residuals J/K | Conditional dispatch | 🔒 externally gated; no action |
| Task 6 — TDD expansion passes | Seven design_spec plans | ✅ closed (all expanded and shipped: phase-8b, 12, 13, 14, 15, 16; ultimate-architecture superseded) |
| Task 7 — GT → HP → WIKI → GEOM → PHYS → Z | Six downstream sprints | ✅ closed (all six shipped) |

**Plus** five sprints NOT anticipated by the original plan but executed this session:
- Sprint HP.3-R (RocksDB KV migration, AD-029)
- Sprint 1B-M1, 1B-M2, RUST-PDF-1, 1B-M3 (Phase 1B Modernization Tranches 1–3 + Rust PDF audit, AD-031–AD-034)
- Sprint DISTILL-1 (LLM reviewer distillation audit, AD-035 — DEFER_NO_DATA)

Historic Task 1 body is retained below for audit.

### Task 1: Reconcile plans, INDEX, and roadmap

**Files:**
- Modify: `.ai/03_plans/INDEX.md`
- Modify: `.ai/03_plans/statistical-architectural-upgrade-plan.md` (rename Stream L → Stream L_conf; mark Stream O as `moved_to: Sprint PHYS`)
- Modify: `.ai/03_plans/ultimate-architecture-upgrade-plan.md` (frontmatter `status: superseded` + `successors:` list)
- Modify: `.ai/01_roadmap/current-phase.md` (rewrite for Sprint Q active)
- Modify: `.ai/01_roadmap/master-roadmap.md` §8 (add §8.x sprint ordering table referencing this plan)

- [ ] **Step 1: Update `INDEX.md` plan table** — Add rows for phase-12, phase-13, phase-14, phase-15, phase-16, phase-8b, 3d-spatial-intelligence, live-wiring, per-layer-embeddings, ultimate-architecture, and this governing plan. Mark phase-8/9 as `Subsumed by Stream H/I`. Mark ultimate-architecture as `Superseded`.
- [ ] **Step 2: Replace `INDEX.md` execution-order diagram** with the Sprint diagram in §3.1 above.
- [ ] **Step 3: Apply Stream L rename in statistical plan** — every heading, TOC entry, cross-reference, and §2.3 mention of "Stream L" in `statistical-architectural-upgrade-plan.md` becomes "Stream L_conf". Bump version to v1.0.9.
- [ ] **Step 4: Mark Stream O as moved in statistical plan** — edit the Stream O section header to append `(moved_to: Sprint PHYS — see phase-16 plan)` and insert a `> **Note:**` block pointing to Sprint PHYS.
- [ ] **Step 5: Supersede ultimate-architecture** — set frontmatter `status: superseded`, add `successors:` list (3d-spatial, phase-8b, phase-13, phase-16, per-layer-embeddings), and prepend a `> **Superseded:**` banner pointing at the governing plan.
- [ ] **Step 6: Rewrite `.ai/01_roadmap/current-phase.md`** — active sprint is "Sprint Q · Live Wiring & 8GB Hardening"; list Streams W1–W5 as the active work; reference this governing plan as the authoritative entry point.
- [ ] **Step 7: Append §8.X to master-roadmap.md** — new subsection "Sprint Order (post-2026-04-15)" linking to `.ai/03_plans/00-governing-implementation-plan.md` §3. Do not edit existing sections; append only.
- [ ] **Step 8: Commit** — `docs(roadmap): add governing implementation plan and reconcile plan inventory`

### Task 2: Sprint Q — Live Wiring & 8GB Hardening

**Sub-plan:** `.ai/03_plans/live-wiring-and-8gb-hardening-plan.md`

- [ ] **Step 1: Worktree** — Create `feat/sprint-q-live-wiring` worktree via `superpowers:using-git-worktrees`
- [ ] **Step 2: Dispatch** — Hand the plan to `superpowers:subagent-driven-development`. Stream order: W1 → W2 → W3 → W4 → W5. Review between each Stream.
- [ ] **Step 3: Exit gate checks**
  - `grep -r "from scripts.vitruvius.review" scripts/vitruvius/ollama_review.py` returns ≥6 imports
  - `grep -r "stringency_vector" 003_Canonical-Knowledge-Layer/shared/concepts/ | wc -l` returns 20
  - `pytest tests/ -v` returns 297+ passing (count increases; never decreases)
  - `pytest tests/test_livewiring_e2e.py -v` returns green
  - `python -c "import resource; ..."` or `psutil` measurement confirms peak RSS ≤ 5 GB
  - `features.livewiring_*=false` byte-identity test passes (`run-with-review` produces identical output files vs pre-Sprint-Q baseline on PD 1096)
- [ ] **Step 4: Record decision** — Append `AD-024` to `.ai/10_state/decisions.md` with measured RSS, latency deltas, and LLM-savings numbers.
- [ ] **Step 5: Merge** — Open PR, merge, tag `sprint-q-closed`. Update `.ai/01_roadmap/milestone-tracker.md` and `current-phase.md` (Sprint Q → closed; next active sprint = R or H).

### Task 3: Sprint R — Per-Layer Embeddings & Agentic (parallelizable with Task 4)

**Sub-plan:** `.ai/03_plans/per-layer-embeddings-agentic-upgrade-plan.md`

- [ ] **Step 1: Entry gate** — Assert tag `sprint-q-closed` exists. Block if absent.
- [ ] **Step 2: Vision probe** — Execute `ple-vision-probe` (defined in Y5 pre-flight of the plan). Record outcome in `AD-025`. If probe fails, mark Y5 as `deferred` and continue with Y0–Y4 only.
- [ ] **Step 3: Dispatch** — Subagent chain Y0 → Y1 → Y2 → Y3 → Y4 → (Y5 conditionally).
- [ ] **Step 4: Stream U absorption** — During Y2 dispatch, include the "psutil model-selection router" task from `ultimate-architecture-upgrade-plan.md` Stream U as an addendum to Y2. Cite the governing plan §4.3 in the commit message.
- [ ] **Step 5: Exit gate** — Backward-compat regression green with all `features.y_*=false`; peak RSS ≤ 5 GB (or ≤ 6.5 GB if Y5 flipped on, behind explicit 8 GB ceiling override).
- [ ] **Step 6: Merge + tag `sprint-r-closed`.**

### Task 4: Sprint H — 3D Spatial Intelligence (parallelizable with Task 3)

**Sub-plan:** `.ai/03_plans/3d-spatial-intelligence-upgrade-plan.md`

- [ ] **Step 1: Entry gate A** — Assert tag `sprint-q-closed` exists.
- [ ] **Step 2: Entry gate B** — Run: `ls 003_Canonical-Knowledge-Layer/shared/relationships/*.yaml | wc -l`. Abort if < 25. If the count is below 25, detour into Task 4a (below) before continuing.
- [ ] **Step 3: Dispatch** — Subagent chain L → M → N → O.
- [ ] **Step 4: Name collision check** — Verify rename from §4.1 Task 1 has landed before L begins. `grep -n "Stream L_conf" .ai/03_plans/statistical-architectural-upgrade-plan.md` must return ≥1 hit.
- [ ] **Step 5: Backward-compat** — `GraphSnapshot` iterator ignores `spatial_instance` nodes when `features.l_spatial=false`; legacy tests stay green.
- [ ] **Step 6: Merge + tag `sprint-h-closed`.**

#### Task 4a (detour): Grow verified relationships to ≥25

**Trigger:** Sprint H entry gate B fails.

- [ ] Step 1: Run full pipeline on PD 1096 IRR (second corpus already present under `002_Raw-Conversion-Layer/001-Laws/`). Use `run-with-review` composite command.
- [ ] Step 2: Promote any high-confidence candidates via `pipeline_cli.py promote`.
- [ ] Step 3: Recount; loop until ≥25 or until a human declares corpus exhausted.
- [ ] Step 4: If still < 25 and corpus exhausted, escalate to user for corpus expansion decision; do not proceed to Sprint H.

### Task 5: Sprint D residuals — conditional

**Sub-plan section:** `.ai/03_plans/statistical-architectural-upgrade-plan.md` §Streams J and K.

- [ ] **Step 1: Check gate J** — Does a Ranger dashboard exist outside this repo? If no, mark J as `deferred` in statistical plan frontmatter and skip.
- [ ] **Step 2: Check gate K** — Is there ≥1 non-PD-1096 jurisdiction ingested with ≥20 verified relationships? If no, mark K as `deferred` and skip.
- [ ] **Step 3: Execute** — Dispatch only the streams whose gates are satisfied.
- [ ] **Step 4: Commit & update decisions.** Record whichever streams shipped; record the deferral reason for any that didn't.

### Task 6: TDD-expansion passes (run once per design-spec plan before its owning sprint)

For each plan in §5, do the following **before** its sprint's Task 2-style dispatch:

- [ ] **Step 1: Open the plan file** (e.g. `phase-13-high-performance-optimizations-plan.md`)
- [ ] **Step 2: Invoke `superpowers:writing-plans`** — Expand every stream's narrative tasks into `implementation_tdd` form: exact file paths, failing test shown, run-to-fail step, minimal implementation shown, run-to-pass step, commit step. No placeholders. Include the self-review section from the skill.
- [ ] **Step 3: Bump frontmatter** — `plan_type: implementation_tdd`, `version: bump`, `last_updated: <today>`.
- [ ] **Step 4: Self-review** — Spec coverage scan, placeholder scan, type-consistency scan (per the `writing-plans` skill self-review checklist).
- [ ] **Step 5: Commit** — `plan: expand <plan-id> to TDD form`
- [ ] **Step 6: Only then proceed** to the sprint's dispatch task.

### Task 7: Sprint GT → HP → WIKI → GEOM → PHYS → Z

Each of these sprints follows the same template once its entry gate from §3.2 is satisfied:

- [ ] **Step 1: Entry gate check** — Assert the prerequisite sprint tag exists; assert any external toolchain (e.g. `rustup`/`maturin` for GT) is installed.
- [ ] **Step 2: Run Task 6** for the owning plan (TDD expansion).
- [ ] **Step 3: Dispatch** via `superpowers:subagent-driven-development` in stream order defined by the owning plan. Review between streams.
- [ ] **Step 4: Honor conflict resolutions** — PHYS must absorb the orphan VF2 task (§4.4); Z must ship as a sibling module (§4.7); WIKI must reuse the Y5 vision registration (§4.5).
- [ ] **Step 5: Exit gate** — Record metrics into an `AD-###` entry, update `milestone-tracker.md`, tag `sprint-<name>-closed`.
- [ ] **Step 6: Hand off to the next sprint** by rewriting `current-phase.md`.

### Task 8: Dispatch the 5 queued optimization plans (2026-04-15 post-session queue) — ✅ CLOSED

All 5 plans shipped during the same session they were written in. Closure commit: `58161bd` (working-tree sweep) on top of the Sprint LSH-1 closure at `2926851`. Every step below was completed.

**Sub-plans (all archived to `.ai/09_archive/plans/` 2026-04-15 after their owning sprints closed):**
- `2026-04-15-advanced-tech-audit-plan.md` → Sprint AUDIT-1
- `2026-04-15-rust-migration-audit-plan.md` → Sprint RUST-MIG-1
- `2026-04-15-pipeline-cli-integration-plan.md` → Sprint PIPELINE-CLI
- `2026-04-15-graphsage-pq-embeddings-plan.md` → Sprint PQ-1
- `2026-04-15-lsh-dedup-plan.md` → Sprint LSH-1

- [x] **Step 1: Dispatch Advanced Tech Audit first** — Executed as Sprint AUDIT-1. FlatBuffers NO_GO (5-10× SLOWER than CPython `_json` at ~150B records — runtime gate not met); Monte Carlo Dropout PARK (GraphSAGE is `torch.no_grad()` by design — no viable sites); Numerical Integrity GO_GAP (shipped SHA-256 integrity footer for spatial contracts via `spatial/contract_reader.py` + `spatial-daemon/src/contract_writer.ts`). Zero new Rust candidates surfaced. Closure at `4258877`. Produces `AD-039`.
- [x] **Step 2: Dispatch Sprint RUST-MIG-1 (Python→Rust polyglot split)** — Entry gate passed (`rustup` + `maturin` both present). Ports S1 `build_spatial_adjacency_edges` (200× raw kernel speedup; existing `LinearOctree::query_aabb` used for the O(n²) → O(n log n) reduction), S2 `weight_by_distance` (12.18× raw / 2.84× end-to-end via nalgebra vectorized exp kernel at n=10000), N4 Mahalanobis core (2.73× end-to-end via nalgebra covariance invert at n=1000, 64-dim) into `spatial_kernels` + `stats_kernels` workspace-member crates inside `scripts/vitruvius/engine_rs/`. N1 sliced Wasserstein DEFERred per **AD-038a** — POT's `wasserstein_distance` is already a thin Python wrapper over a native C++ LP solver; Rust port would add marshalling overhead without a speed gain. Both `rust_mig_spatial_kernels` + `rust_mig_stats_kernels` flags flipped to `true` in the same sprint after parity bench clearing the ≥2× threshold. Closure at `1840c08`. Produces `AD-036`, `AD-037`, `AD-038`, `AD-038a`. AD-037 also corrected Sprint LSH-1's "O(n²) → O(n log n)" premise — audit found `dedupe_by_endpoints` is already O(n log n) dict-grouped.
- [x] **Step 3: Dispatch pipeline_cli.py integration** — Executed as Sprint PIPELINE-CLI. Wires `p1b_docling_parser`, `p1b_libreoffice_preprocessor`, `p1b_ocr_preprocessor`, `p1b_process_pool_orchestration`, `p1b_rust_pdf_parser` via new `convert-parsers-one` subcommand + `parsers/factory.py::build_default_orchestrator()` + `parsers/cli_handler.py::run_convert_parsers_one()`. Parallel command pattern (not a replacement of the existing `convert-one` dispatch) guarantees byte-identity with all flags OFF. Side-fix: `RustPdfParser` was in `parsers.__all__` but never imported (broken since AD-034) — re-exported correctly. Closure at `724c19a`. Produces `AD-040`.
- [x] **Step 4: Dispatch Sprint PQ-1 (GraphSAGE PQ embeddings)** — Executed as Sprint PQ-1. 32× exact compression on GraphSAGE structural embeddings (256 B/node → 8 B/node; M=8 sub-spaces, k=256 centroids, sub_dim=8 over 64-d float32). **0.00017 cosine similarity delta** on held-out set (117× under the 0.02 gate). Pure numpy — zero new dependencies, zero Rust escalation. `hp_graphsage_pq` feature flag stays `false` pending an embedding persistence layer that actually consumes the PQ codes. Closure at `1c52505`. Produces `AD-041`.
- [x] **Step 5: Dispatch Sprint LSH-1 (MinHash near-duplicate dedup)** — Executed as Sprint LSH-1 after AD-037 reframed the premise from "O(n²) scaling fix" to "fuzzy near-duplicate detection for predicate variants". Vectorized Carter-Wegman MinHash (70× faster than the initial nested-loop implementation — 8s → 108ms at n=1000). 14.17% fuzzy hit rate at 20% injection (clears the ≥10% gate); 0 false positives on 200-candidate disjoint audit. The plan's proposed `num_bands=4` was underpowered — tuned to `num_perm=256, num_bands=32, r=8` for 99% recall at Jaccard ≥ 0.78. Uses pure numpy (no `datasketch` dep needed). `w_lsh_dedup` flag stays `false` pending full-PD-1096 operator run to confirm live-data gates. Closure at `2926851`. Produces `AD-042` (premise: AD-037).
- [x] **Step 6: Re-rank after the audit** — Sprint AUDIT-1 surfaced zero new Rust candidates. Original queue order preserved; AUDIT-1 simply slotted in ahead of the rest of the queue without downstream impact.
- [x] **Step 7: Close the queue** — All 5 executed plans archived to `.ai/09_archive/plans/`. `.ai/03_plans/` active folder now contains only `00-governing-implementation-plan.md` + `INDEX.md` per the 2026-04-15 19:00 archival pass (phase-1b-multi-parser-integration, statistical-architectural-upgrade, ingestion-refinement-contract also archived in the same pass — the first because it fully shipped via 1B-M1/M2/M3 + PIPELINE-CLI, the second with `archived_with_open_streams` frontmatter for externally-gated J/K, the third per user instruction to leave only governing plan + INDEX active). `.ai/01_roadmap/current-phase.md` next action is a fresh roadmap brainstorm.

**Ordering rationale (as-executed vs planned).** The planned order was Audit → RUST-MIG-1 → pipeline_cli → PQ-1 → LSH-1. In practice, RUST-MIG-1 and AUDIT-1 ran back-to-back in a different order without downstream impact — AUDIT-1 surfaced zero Rust candidates, so the re-order had no effect on the queue. All 5 plans shipped within the same session at the cadence the 2026-04-15 session established.

**Parallelism (retrospective).** The plans ended up being dispatched sequentially rather than in parallel — the session operator chose to run them back-to-back via subagent-driven-development rather than coordinating parallel wave dispatches for the last five. Total wall-time per sprint held steady at ~30-45 min each. Commit tags: `sprint-rust-mig-1-closed`, `sprint-audit-1-closed`, `sprint-pipeline-cli-closed`, `sprint-pq-1-closed`, `sprint-lsh-1-closed`.

### Task 9: Continuous maintenance of `current-phase.md`

- [ ] Whenever a sprint opens, pauses, or closes, rewrite `.ai/01_roadmap/current-phase.md` to name the active sprint and the next entry/exit gate. This document is the single file a cold agent reads first to orient itself.

---

## 7. Quality Bar & Acceptance Criteria

A sprint is only "closed" when every one of these holds:

1. **Tests** — Full test suite green under strict `-W error::DeprecationWarning`.
2. **Byte-identity baseline** — With every new feature flag set to its default (OFF for new features), the pipeline's output on PD 1096 is byte-identical to the prior sprint's output. No silent behavior drift.
3. **RSS ceiling** — Peak resident set size ≤ 5 GB under `gemma4:e4b` on the 8 GB M2 host. Sprint R Y5 may temporarily raise this to 6.5 GB behind a named flag, documented in the AD entry.
4. **Decision log** — An `AD-###` entry exists with measured numbers: RSS, latency delta, LLM-call count delta.
5. **Plan hygiene** — The sub-plan's frontmatter is updated to `status: complete`; `INDEX.md` reflects the closure; `milestone-tracker.md` checkboxes are ticked.
6. **Governing plan hygiene** — This plan's §2 inventory table is updated to show the sprint as closed. `current-phase.md` points to the next sprint.

---

## 8. Non-Goals of This Plan

- **No new code.** This plan never authorizes writing production code directly. All code lands via a sub-plan.
- **No duplication** of sub-plan TDD steps. Every "Step" here is orchestration, not implementation.
- **No skipping** of sub-plan self-review, gate checks, or decision logging.
- **No unblocking** of items that are externally gated: Phase 11 dataset expansion (needs user direction), GPU-gated LoRA/DPO, learner-gated BKT, CV-model-gated 2D blueprint OCR, PINNs, zk-SNARKs.
- **No refactors** of `ollama_review.py` during Sprint Q — Sprint Q is pure wiring.
- **No new plans** are created by this document. If a new plan is needed, it goes in `.ai/03_plans/` and this plan is updated in the next reconciliation pass.

---

## 9. Self-Review (run after writing this plan)

- [x] **Spec coverage** — Every plan in `.ai/03_plans/` appears in §2; every sprint has entry and exit gates in §3.2; every conflict in §4 has a named resolution.
- [x] **Placeholder scan** — No "TBD", "implement later", "add error handling" patterns. Tasks reference concrete file paths or commands.
- [x] **Type / naming consistency** — Stream L / L_conf split is called out once in §4.1 and used consistently in §6 Task 1. Tag names `sprint-q-closed`, `sprint-r-closed`, etc. are used consistently in §3.2, §6 Task 2–4, and §6 Task 7.
- [x] **Subsumption correctness** — `phase-8-graph-contract-indexing` and `phase-9-query-ai-layer` are marked subsumed; the engineer is told explicitly not to dispatch them separately.
- [x] **Gate check realism** — Every entry gate is either a grep-testable condition or a tag-existence check, not vibes.
- [x] **No code duplication** — Zero TDD steps copy-pasted from sub-plans.

---

## 10. Execution Handoff

**Session 2026-04-15 outcome (final, 19:00 local):** Session closed with **21 optimization / implementation sprints all done**. Chain: Q → R → H → GT → HP → HP.3-R → WIKI → GEOM → PHYS → Z → Meta Docs Cleanup → 1B-M1 → 1B-M2 → RUST-PDF-1 → 1B-M3 → DISTILL-1 → RUST-MIG-1 → AUDIT-1 → PIPELINE-CLI → PQ-1 → LSH-1. Test suite grew from **1437 → 1528 passing** across the 5 optimization sprints alone (+91 delta; pre-session 297 → 1528 cumulative delta of +1231). **9 new ADs** shipped this closure block: AD-036, AD-037, AD-038, AD-038a, AD-039, AD-040, AD-041, AD-042 (one per sprint + AD-038a for the N1 Wasserstein DEFER_ALREADY_NATIVE rationale). All commits pushed to `origin/main` (HEAD at `58161bd` — working-tree sweep on top of the Sprint LSH-1 closure at `2926851`). Working tree clean. 5 new sprint tags published to origin: `sprint-rust-mig-1-closed`, `sprint-audit-1-closed`, `sprint-pipeline-cli-closed`, `sprint-pq-1-closed`, `sprint-lsh-1-closed`.

**Active plans folder state (post Task 34 archival pass, 2026-04-15 19:00):** `.ai/03_plans/` now contains exactly **2 files** — `00-governing-implementation-plan.md` (this file) and `INDEX.md`. Everything else is archived under `.ai/09_archive/plans/`. This is the minimal "queue empty" state.

**Next action — fresh roadmap brainstorm.** Task 8 is fully closed. The **queue is empty** — there are no plans to dispatch. Before the next sprint, the next operator should:

1. Run `superpowers:brainstorming` to define the next horizon. The project is materially ahead of the v2.0.0 master-roadmap envelope and is producing 5–6 sprints per session; the next horizon (Phase 12+ / corpus expansion / real-world evaluation against board-exam prep use case) is undefined and should not be guessed at.
2. Based on the brainstorm output, use `superpowers:writing-plans` to land new plans into `.ai/03_plans/`.
3. Update this plan's §2 inventory + §6 Task table, bump `version:` to `4.0.0`, and begin dispatch.

**Conditional work still parked (unchanged from prior handoff):**
- Sprint D residuals J (active learning) and K (CLUP scaling) remain externally gated on a Ranger dashboard surface and a second-jurisdiction corpus respectively. The statistical-architectural-upgrade plan has been archived with `archived_with_open_streams: "J,K"` frontmatter so future readers see the defer status without having to grep.
- Sprint DISTILL-1 re-dispatch is still gated on a populated Sprint R Y4 verdict cache (needs ≥50 live LLM review verdicts). Unblocker: run live review with `y_stateful_registry=true` + `w_review_nb_prefilter=true` + `w_review_choquet_aggregator=true` on ≥20 PD 1096 sections.
- Sprint PQ-1 embedding persistence layer is a known follow-on — the `hp_graphsage_pq` flag stays false until a consumer exists.
- Sprint LSH-1 `w_lsh_dedup` flag stays false until a full PD 1096 operator run validates the fuzzy layer on live data.

**No unsolicited scope expansion.** New plans enter §2.2 via a separate writing-plans pass, not mid-sprint.
