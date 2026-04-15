---
plan_id: governing-implementation
phase: "Meta — Orchestration of All Active Plans"
title: "Governing Implementation Plan: Sprint Execution Order & Dependency Graph"
status: active
priority: highest
sprint: "Meta (Sprints Q/R/H/GT/HP/HP.3-R/WIKI/GEOM/PHYS/Z/1B-M1/1B-M2/RUST-PDF-1/1B-M3/DISTILL-1 CLOSED · 4 optimization plans QUEUED · Sprint D residuals J/K externally gated)"
version: 2.0.0
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

## 1. Current Ground Truth (2026-04-15, 14:19 local)

### 1.1 What has shipped this session (2026-04-14 → 2026-04-15)
This plan was written 2026-04-15 with Sprint Q as the next action item. Since then, **16 sprints have closed in a single sustained session**. The sprint list below is authoritative; the plan inventory in §2 has been updated to match.

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

**Test suite:** 1437 passing, 1 skipped (grew from 297 at session start).

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

### 1.5 New work queued 2026-04-15 — 4 optimization plans
Four new implementation plans were written during the session but have **not been executed**. They target low-spec (8 GB M2) RAM and scaling wins without quality loss. They are the **active work queue** for the next session.

| # | Plan file | Type | Expected win | Status |
|---|-----------|------|--------------|--------|
| 1 | `2026-04-15-advanced-tech-audit-plan.md` | audit | Identifies the next wave of statistical / mathematical optimizations the team should explore (beyond PQ / LSH) | 📝 Queued |
| 2 | `2026-04-15-pipeline-cli-integration-plan.md` | implementation_tdd | Wires the `p1b_*` deployment-readiness markers into `pipeline_cli.py` so flipping a flag actually routes documents through the new parsers (Docling, LibreOffice, OCRPreprocessor, RustPdfParser) end-to-end | 📝 Queued |
| 3 | `2026-04-15-graphsage-pq-embeddings-plan.md` (Sprint PQ-1) | implementation_tdd | **32× disk footprint reduction** on GraphSAGE structural embeddings via Product Quantization, negligible quality loss | 📝 Queued |
| 4 | `2026-04-15-lsh-dedup-plan.md` (Sprint LSH-1) | implementation_tdd | **O(n log n) replacement for pairwise dedup** (currently O(n²) in `dedupe_by_endpoints()` at `relationships_sections.py:246`) via MinHash LSH | 📝 Queued |

---

## 2. Plan Inventory (post-session reconciliation 2026-04-15 14:19)

**Active in `.ai/03_plans/`:** 5 files (governing, INDEX, ingestion contract, phase-1b, statistical-upgrade) + **4 queued optimization plans** awaiting execution.

**Archived in `.ai/09_archive/plans/`:** 16 closed sprints this session (see §1.1).

### 2.1 Active plans (drivers of next work)

| # | Plan ID | Type | Owning Sprint | Status |
|---|---------|------|---------------|--------|
| 1 | `governing-implementation` (this file) | orchestration | Meta | 🔥 Active |
| 2 | `statistical-architectural-upgrade` | implementation_tdd | Sprint D residuals J/K | 🔒 Externally gated (§1.3) |
| 3 | `phase-1b-multi-parser-integration` | design_spec | Sprint C continuation | 🔥 In progress (Foundation + Tranches 1/2/3 shipped; further modernization work available) |
| 4 | `contract-ingestion-refinement` | contract | — | ❄️ Frozen |
| 5 | `INDEX.md` | (index) | — | ✅ Reconciled 2026-04-15 |

### 2.2 Queued implementation plans (written 2026-04-15, unexecuted)

| # | Plan file | Type | Target | Status |
|---|-----------|------|--------|--------|
| 6 | `2026-04-15-advanced-tech-audit-plan.md` | audit | Next wave of optimizations | 📝 Queued (run first — identifies scope for #7–#10) |
| 7 | `2026-04-15-rust-migration-audit-plan.md` | audit_then_conditional_implementation | **Sprint RUST-MIG-1** — Python→Rust polyglot split. Ports S1 `build_spatial_adjacency_edges` (O(n²) → O(n log n)) + S2 `weight_by_distance` + N4 Mahalanobis core + N1 sliced Wasserstein. Extends existing `engine_rs` Cargo workspace with `spatial_kernels` + `stats_kernels` crates. Single largest wall-time win: S1. | 📝 Queued — dispatch immediately after Advanced Tech Audit |
| 8 | `2026-04-15-pipeline-cli-integration-plan.md` | implementation_tdd | Wire `p1b_*` flags into `pipeline_cli.py` end-to-end | 📝 Queued |
| 9 | `2026-04-15-graphsage-pq-embeddings-plan.md` | implementation_tdd | Sprint PQ-1 — 32× GraphSAGE embedding compression | 📝 Queued |
| 10 | `2026-04-15-lsh-dedup-plan.md` | implementation_tdd | Sprint LSH-1 — fuzzy near-duplicate dedup via MinHash (**NB:** AD-037 corrects the plan's "O(n²) → O(n log n)" premise — current dedup is already O(n log n) dict-grouped; LSH-1's actual value is semantic fuzzy matching, not a scaling fix) | 📝 Queued |

### 2.3 Closed sprints (archived in `.ai/09_archive/plans/` — reference only)

All 16 sprint plans listed in §1.1 are archived with `status: complete` frontmatter. They are cited by successor plans but never re-dispatched.

Also archived from the original inventory:
- `phase-8-graph-contract-indexing` — subsumed by Stream H (Sprint D)
- `phase-9-query-ai-layer` — subsumed by Stream I (Sprint D)
- `ultimate-architecture-upgrade` — superseded; all 15 streams distributed across successor plans that have now shipped

---

## 3. Execution Order & Gate Matrix

### 3.1 Sprint dependency diagram (post-session, 2026-04-15 14:19)

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
   └───► Sprint D residuals   🔒 externally gated (Ranger + second-jurisdiction)

📝 NEXT — 5 queued optimization plans (see §6 Task 8)
   ├───► Advanced Tech Audit         (audit — identifies next optimization scope)
   ├───► Sprint RUST-MIG-1           (Python→Rust polyglot split: S1/S2/N4/N1 kernels — single largest wall-time win)
   ├───► pipeline_cli.py integration (wire p1b_* flags into live routing)
   ├───► Sprint PQ-1                 (GraphSAGE Product Quantization, 32× compression)
   └───► Sprint LSH-1                (MinHash fuzzy near-duplicate dedup — reframed by RUST-MIG-1 AD-037)
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

### Task 8: Dispatch the 5 queued optimization plans (2026-04-15 post-session queue)

Five plans were written in this session but not executed. They are the **active work queue** for the next session. Dispatch in the order listed — the audit (#1) scopes the remaining four, and the Rust migration (#2) depends on the audit's RAM/wall-time findings.

**Sub-plans:**
- `.ai/03_plans/2026-04-15-advanced-tech-audit-plan.md`
- `.ai/03_plans/2026-04-15-rust-migration-audit-plan.md` (**Sprint RUST-MIG-1** — added 2026-04-15 14:40 after a fresh codebase audit; see §2.2 row 7)
- `.ai/03_plans/2026-04-15-pipeline-cli-integration-plan.md`
- `.ai/03_plans/2026-04-15-graphsage-pq-embeddings-plan.md` (Sprint PQ-1)
- `.ai/03_plans/2026-04-15-lsh-dedup-plan.md` (Sprint LSH-1)

- [ ] **Step 1: Dispatch Advanced Tech Audit first** — This is an audit-then-conditional-implementation plan that scans the codebase for statistical/mathematical optimization opportunities beyond PQ, LSH, and the Rust-migration candidates. It produces a structured report with GO/DEFER verdicts per candidate. Review the report before proceeding to #2–#5 so the queue can be re-ranked if the audit uncovers a higher-impact win.
- [ ] **Step 2: Dispatch Sprint RUST-MIG-1 (Python→Rust polyglot split)** — Entry gate: the Rust toolchain is installed (`rustup show` + `maturin --version`). Ports S1 `build_spatial_adjacency_edges` (O(n²) → O(n log n) via existing `LinearOctree::query_aabb`), S2 `weight_by_distance`, N4 Mahalanobis core, and N1 sliced Wasserstein into two new workspace-member crates (`spatial_kernels`, `stats_kernels`) inside the existing `scripts/vitruvius/engine_rs/` Cargo workspace. Target: the single largest RAM + wall-time win identified in the queue — S1 alone is expected to drop a 2k-node spatial snapshot's edge-build from ~1 second to ~5 ms and eliminate O(n²) scaling. Exit gate: parity tests green on every port, `rust_mig_spatial_kernels` + `rust_mig_stats_kernels` flags default true iff AD-038 clears the 2× bench threshold. Produces `AD-036`, `AD-037`, `AD-038`. **Also corrects Sprint LSH-1's O(n²) premise** (AD-037) — the audit found `dedupe_by_endpoints` is already O(n log n) dict-grouped, so Sprint LSH-1 must be reframed to "fuzzy near-duplicate dedup" before dispatch in Step 5.
- [ ] **Step 3: Dispatch pipeline_cli.py integration** — Entry gate: none. Wires the `p1b_docling_parser`, `p1b_libreoffice_preprocessor`, `p1b_ocr_preprocessor`, `p1b_process_pool_orchestration`, and `p1b_rust_pdf_parser` feature flags into `pipeline_cli.py` routing so flipping any of them actually changes which parser runs on an incoming document. Exit gate: end-to-end ingestion through each of the five parsers on a representative PD 1096 section, plus byte-identity test with every flag OFF. Produces `AD-039`.
- [ ] **Step 4: Dispatch Sprint PQ-1 (GraphSAGE PQ embeddings)** — Entry gate: none (GraphSAGE already ships via Sprint HP HP.5). Target: **32× disk footprint reduction** on structural embeddings via Product Quantization. Exit gate: cosine-similarity delta ≤ 0.02 on a held-out set vs the raw float32 embeddings; disk footprint measured end-to-end; no quality regression on downstream structural loopholes detector. Produces `AD-040`.
- [ ] **Step 5: Dispatch Sprint LSH-1 (MinHash near-duplicate dedup)** — Entry gate: Sprint RUST-MIG-1 Task 2 (AD-037) has landed and reframed this plan from "O(n²) → O(n log n) scaling fix" to "fuzzy near-duplicate detection for predicate variants". Uses Python `datasketch` — does NOT migrate to Rust. Exit gate: fuzzy-match hit rate ≥ 10% on the PD 1096 corpus for known predicate variants (e.g., "lot area ≥ 100 sqm" vs "minimum lot area of 100 square meters"); zero false positives on disjoint relationship pairs. Produces `AD-041`.
- [ ] **Step 6: Re-rank after the audit** — If the Advanced Tech Audit surfaces a candidate with a higher RAM/quality payoff than any of #2–#5, insert it as a new task between Step 1 and Step 2 with its own AD number. Do not silently replace the plans in the queue — add.
- [ ] **Step 7: Close the queue** — When all five plans are shipped (or explicitly deferred), update `.ai/01_roadmap/current-phase.md` to reflect the next active sprint (or "maintenance mode" if no new work is queued), archive each executed plan to `.ai/09_archive/plans/`, and update this §2 inventory table.

**Ordering rationale.** The Advanced Tech Audit is cheap (no code changes) and re-scopes the queue. Sprint RUST-MIG-1 goes next because (a) its own audit already identified S1 as the single largest wall-time win in the codebase, and (b) the AD-037 finding corrects Sprint LSH-1's premise, so LSH-1 must not dispatch until that correction lands. The pipeline_cli integration unblocks **user-facing** use of every parser Phase 1B shipped — without it, the three tranches are behind feature flags nobody can flip. PQ + LSH are the remaining scaling / quality unlocks.

**Parallelism.** Tasks #3 and #4 are independent — pipeline_cli touches CLI routing, PQ touches embedding storage. They can dispatch in parallel via `superpowers:dispatching-parallel-agents` after #2 lands. Task #2 (RUST-MIG-1) and Task #5 (LSH-1) must be sequenced because #2 corrects #5's premise. Commit each in its own sprint tag (`sprint-rust-mig-1-closed`, `sprint-pipeline-cli-closed`, `sprint-pq-1-closed`, `sprint-lsh-1-closed`).

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

**Session 2026-04-15 outcome:** Sprints Q → R → H → GT → HP → HP.3-R → WIKI → GEOM → PHYS → Z → 1B-M1 → 1B-M2 → RUST-PDF-1 → 1B-M3 → DISTILL-1 all closed. Test suite grew from 297 to 1437 passing. All commits pushed to `origin/main`. Working tree clean.

**Next session — pick up at Task 8.** Dispatch the 4 queued optimization plans in the order specified: (1) Advanced Tech Audit, (2) pipeline_cli.py integration, (3) Sprint PQ-1, (4) Sprint LSH-1. The audit may re-rank the queue. Tasks #2–#4 are independent and can run in parallel after the audit.

**Conditional work still parked:**
- Sprint D residuals J and K remain externally gated.
- Phase 6A Resume gap was closed at root by Sprint R Y4 (`stateful_review_registry.sqlite` / `.rocksdb` cache). A follow-up that actually populates the cache via a live LLM review run is the unblocker for re-dispatching Sprint DISTILL-1 Tasks 2–3.

**No unsolicited scope expansion.** New plans enter §2.2 via a separate writing-plans pass, not mid-sprint.
