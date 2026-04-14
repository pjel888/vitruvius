---
plan_id: governing-implementation
phase: "Meta — Orchestration of All Active Plans"
title: "Governing Implementation Plan: Sprint Execution Order & Dependency Graph"
status: active
priority: highest
sprint: "Meta (Sprint Q → R ⟂ H → Sprint-D residuals → GT → HP → WIKI → GEOM → PHYS → Z)"
version: 1.0.0
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

## 1. Current Ground Truth (2026-04-15)

### 1.1 What has shipped
- Sprints A, B, C **CLOSED**. Phases 0, 1A, 1B Foundation, 1C MVP, 2, 3C (16/20 deterministic), 4, 5 (regex + dedup + pre-review filter), 6A, 6B, 7 all shipped.
- **Statistical & Architectural Intelligence Upgrade** — Streams A through I **CLOSED** on 2026-04-14. That bundle shipped Phase 8 base graph contract and Phase 9 base query engine as a byproduct of Streams H and I respectively, so `phase-8-graph-contract-indexing` and `phase-9-query-ai-layer` are now *subsumed* (not separately executable).
- Test suite: **297/297 passing** on branch `feat/sprint-d-intelligence-upgrade`.

### 1.2 The single most important blocker: dead scaffolds
Streams F (review) and G (promotion) of the statistical upgrade shipped **Python modules that nothing imports**. Specifically:
- `pre_review/nb_filter.py`
- `review/ontology_prompt.py`, `review/slm_router.py`, `review/conformal.py`, `review/tension_analyzer.py`, `review/reflection_parser.py`, `review/choquet.py`
- `promotion/bayesian_fusion.py`, `promotion/stringency_matrix.py`, `promotion/temporal_edges.py`

These are tested in isolation but never imported by `ollama_review.py` or `promotion.py`. The `live-wiring-and-8gb-hardening-plan` exists specifically to close this gap. **No downstream plan delivers value until that wiring lands.** This is why Sprint Q is the first sprint.

### 1.3 Streams that are still pending inside the statistical upgrade plan
- **J — Active Learning** (2 tasks). Gated on a Ranger dashboard that lives outside this repo.
- **K — CLUP Scaling** (3 tasks). Gated on a second jurisdiction being ingested.
- **L_conf, M, N, O (research doc v3 streams)** — added to the statistical plan on 2026-04-14 via plan revision v1.0.8. These are TDD-expanded *design spec* entries that overlap with other plans (see §4).

### 1.4 Plans created on 2026-04-15 that need TDD expansion
Seven plans were created as `plan_type: design_spec` on 2026-04-15: phase-8B, phase-12, phase-13, phase-14, phase-15, phase-16, ultimate-architecture-upgrade. They cannot be executed as-is — they need a plan-expansion pass before dispatch (see Task 6).

---

## 2. Plan Inventory (all 16 active files in `.ai/03_plans/`)

| # | Plan ID | Type | Owning Sprint | Status |
|---|---------|------|---------------|--------|
| 1 | `statistical-architectural-upgrade` | implementation_tdd | Sprint D (Streams A–I ✓; J–K deferred; L_conf–O superseded) | In progress |
| 2 | `live-wiring-8gb-hardening` | implementation_tdd | **Sprint Q (HIGHEST PRIORITY)** | Planned |
| 3 | `per-layer-embeddings-agentic-upgrade` | implementation_tdd | Sprint R | Planned |
| 4 | `3d-spatial-intelligence-upgrade` | implementation_tdd | Sprint H | Planned |
| 5 | `phase-1b-multi-parser-integration` | design_spec | Sprint C continuation (Modernization §11 Phase 2/3) | In progress (Foundation shipped) |
| 6 | `phase-8-graph-contract-indexing` | design_spec | **Subsumed by Stream H** | Closed via subsumption |
| 7 | `phase-9-query-ai-layer` | design_spec | **Subsumed by Stream I** | Closed via subsumption |
| 8 | `phase-8b-geo-topological-graph` | design_spec | Sprint GT | Planned |
| 9 | `ultimate-architecture-upgrade` | design_spec | — | **Superseded** (see §4.6) |
| 10 | `phase-12-compound-ai-evolution` | design_spec | Sprint Z | Planned (stretch) |
| 11 | `phase-13-high-performance-optimizations` | design_spec | Sprint HP | Planned |
| 12 | `phase-14-autonomous-knowledge-synthesis` | design_spec | Sprint WIKI | Planned |
| 13 | `phase-15-geometric-constraint-engine` | design_spec | Sprint GEOM | Planned |
| 14 | `phase-16-statistical-mechanics-graph-physics` | design_spec | Sprint PHYS | Planned |
| 15 | `ingestion-refinement-contract` | contract | — | Frozen |
| 16 | `INDEX.md` | (index) | — | Needs Task 1 reconciliation |

---

## 3. Execution Order & Gate Matrix

### 3.1 Sprint dependency diagram

```
Sprint Q  — Live Wiring & 8GB Hardening        [START HERE]
   │
   ├───► Sprint R  — Per-Layer Embeddings & Agentic   (parallel w/ H if capacity)
   │        │
   │        └───► (Sprint R closure)
   │
   ├───► Sprint H  — 3D Spatial Intelligence          (parallel w/ R if capacity)
   │        │
   │        └───► Sprint GT  — Geo-Topological Rust Vault
   │                 │
   │                 └───► Sprint HP  — High-Performance Optimizations
   │                          │
   │                          └───► Sprint WIKI — Autonomous Knowledge Synthesis
   │                                   │
   │                                   └───► Sprint GEOM — Geometric Constraint Engine
   │                                            │
   │                                            └───► Sprint PHYS — Graph Physics
   │                                                     │
   │                                                     └───► Sprint Z — Compound AI Evolution (stretch)
   │
   └───► Sprint D residuals (J active learning / K CLUP scaling)   [conditional — skip if gates unmet]
```

### 3.2 Gate matrix

| Sprint | Entry Gate | Exit Gate |
|--------|-----------|-----------|
| **Q** | None — execute immediately | All 8 Stream F review modules + 3 Stream G promotion modules imported into live paths; all 20 canonical concept files have `stringency_vector`; `test_livewiring_e2e.py` green on PD 1096; peak RSS ≤ 5 GB under `gemma4:e4b`; byte-identical output with every `features.livewiring_*` flag OFF |
| **R** | `sprint-q-closed` tag exists | Y0–Y4 shipped; Y5 shipped iff `ple-vision-probe` passes (RSS headroom under concurrent Ollama + vision inference ≤ 5 GB); backward-compat regression green with all `features.y_*` OFF |
| **H** | `sprint-q-closed` tag exists AND `≥25` verified relationships present under `003_Canonical-Knowledge-Layer/shared/relationships/` | Stream L (Z3) + M (IFC/OWL) + N (TS daemon) + O (foraging scaffold) CLOSED; `spatial_instance` nodes invisible to legacy `GraphSnapshot` iterators when `features.l_spatial=false` |
| **D-residual J** | Ranger dashboard exists externally | J.1 + J.2 tasks closed |
| **D-residual K** | ≥1 non-PD-1096 jurisdiction fully ingested (≥20 verified relationships in corpus 2) | K.1–K.3 tasks closed |
| **GT** | `sprint-h-closed` AND Rust toolchain installed (`rustup` + `maturin`) AND FlatBuffers schema review complete | `engine_rs` crate shipped via `pyo3`; octree point query benchmarked at <1 ms for 100k nodes; `10k node read` roundtrip <5 ms |
| **HP** | `sprint-gt-closed` (HP stream HP.3 event sourcing reuses GT RocksDB schema) | Merkle status check <100 ms on 10k files; AST chunker replaces whitespace chunker; Wasm spatial kernel loadable from Python via `wasmtime` |
| **WIKI** | `sprint-hp-closed` (WIKI uses HP.2 AST chunker + HP.3 event log) | Docling+Heron integrated; Kuzu-backed hybrid store queryable; bidirectional `[[link]]` linter green; SHA-256 delta tracking operational |
| **GEOM** | `sprint-h-closed` (GEOM reuses Stream L Z3 bridge) AND `sprint-wiki-closed` | ≥50 PD 1096 inequalities extracted; buildable envelope exports valid glTF; IoU audit runs on a user design |
| **PHYS** | Phase 8 graph stable (already true via Stream H closure) | PageRank authority + Boltzmann stability + Shannon sampler + eigenvector cascade shipped behind `features.phys_*`; Stream O orphan (VF2) folded into PHYS.2 |
| **Z** | `sprint-geom-closed` AND `sprint-phys-closed` | Neuro-symbolic Datalog bridge + adversarial swarm + differential dataflow shipped; hallucination rate measured <0.1% on a PD 1096 regression set |

### 3.3 Non-blocking parallel track: Phase 1B Modernization
`phase-1b-multi-parser-integration-plan.md` §11 Phase 2 (Modernization) and §11 Phase 3 (Scaling & Governance) are independent of every sprint above. They can execute in a side worktree whenever capacity allows. Treat as "background sprint C continuation" and do not let them block Sprint Q.

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

### Task 8: Continuous maintenance of `current-phase.md`

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

Sprint Q is immediate. When the user says "go", the next action is **Task 1 (reconcile) then Task 2 (Sprint Q dispatch)**, in that order, via `superpowers:subagent-driven-development`. Task 3 (Sprint R) and Task 4 (Sprint H) become runnable once Task 2 exits.
