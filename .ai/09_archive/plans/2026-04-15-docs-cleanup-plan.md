# Post-Sprint Docs Cleanup Plan (2026-04-15)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Bring every `.ai/` documentation surface back into sync with the codebase after the 2026-04-15 session closed nine governing-plan sprints (Q, R, PHYS, H, GEOM, WIKI, GT, HP, Z).

**Architecture:** Pure documentation cleanup, no code changes. Nine tasks organized into three waves. Wave A is six parallel-safe tasks that each touch a disjoint set of files. Wave B is a single INDEX.md + plan-archival task that must run after Wave A. Wave C is a single atomic commit executed by the orchestrator so parallel `git add` races can't happen.

**Tech Stack:** Markdown docs under `.ai/` + `git mv` for archival. No tests to write — docs don't have unit tests. "Verification" for each task is a read-back of the written file plus a scope check against the task spec.

---

## Dispatch Waves (Parallelism Map)

| Wave | Tasks | Touches | Can run in parallel? |
|---|---|---|---|
| A | 2, 3, 4, 5, 6, 7 | file-disjoint: 00_system/, 02_audits/, 10_state/, 01_roadmap/ | ✅ yes — dispatch all six at once |
| B | 1 (INDEX.md + `git mv`) | .ai/03_plans/INDEX.md + 3 plan files | ❌ must follow Wave A (no race on INDEX.md with Wave A tasks, but its own git ops must be atomic) |
| C | 9 (final commit) | orchestrator only | ❌ follows Wave B |

**Agents must NOT run `git add` or `git commit`.** They write files only. The orchestrator performs a single atomic commit at the end.

---

## Session Ground-Truth (what the docs need to reflect)

Orchestrator-supplied context that every subagent needs — do not make them re-derive:

- **9 sprints closed this session (2026-04-15):** Q, R, PHYS, H, GEOM, WIKI, GT, HP, Z
- **Git tags (9):** `sprint-q-closed`, `sprint-r-closed`, `sprint-phys-closed`, `sprint-h-closed`, `sprint-geom-closed`, `sprint-wiki-closed`, `sprint-gt-closed`, `sprint-hp-closed`, `sprint-z-closed`
- **Decision log:** AD-001 through AD-028 in `.ai/10_state/decisions.md`
- **Test suite:** Python 1364 / 1364 passing (1 skipped); TypeScript 20 / 20 (spatial-daemon); Rust 10 unit tests (engine_rs + datalog_rs)
- **Canonical relationships:** 31 verified (up from 7 via PD 1096 IRR ingest)
- **Branch:** `feat/sprint-r-per-layer-embeddings` (misnomer — carries all 9 sprints)
- **New Python packages shipped this session:** `scripts/vitruvius/compound/`, `scripts/vitruvius/wiki/`, `scripts/vitruvius/geometric/`, `scripts/vitruvius/foraging/`, additions to `scripts/vitruvius/graph/`, `scripts/vitruvius/spatial/`, `scripts/vitruvius/promotion/`, `scripts/vitruvius/review/`, `scripts/vitruvius/pre_review/`, `scripts/vitruvius/bench/`
- **New Rust crates:** `scripts/vitruvius/engine_rs/` (Cargo workspace: `core/` + `pyo3_shim/`, wasm32 target enabled), `scripts/vitruvius/datalog_rs/` (pyo3 crate, hand-rolled Datalog evaluator)
- **New TypeScript sibling:** `spatial-daemon/` (Node.js; GJK + AABB + contract writer + CLI; vitest)
- **Already closed (state-doc sync commit `37f0f62`):** `.ai/10_state/active_context.md`, `.ai/01_roadmap/current-phase.md`, AD-028 in `decisions.md`
- **9 plans already archived in `.ai/09_archive/plans/`:** phase-1c, phase-2, phase-3, phase-6a, phase-6b, phase-7, phase-8b, phase-12, phase-13, phase-14, phase-15, phase-16, sprint-b-polish, live-wiring-and-8gb-hardening, per-layer-embeddings-agentic-upgrade, 3d-spatial-intelligence-upgrade

---

## Task 1: Archive three superseded plans + reconcile INDEX.md (Wave B)

**Why:** `phase-8-graph-contract-indexing-plan.md` and `phase-9-query-ai-layer-plan.md` are marked "Subsumed by Stream H / Stream I" in the current INDEX.md — their base work shipped inside Sprint D Streams H and I respectively. `ultimate-architecture-upgrade-plan.md` has its frontmatter set to `status: superseded` already. All three belong in `.ai/09_archive/plans/`.

**Files:**
- Move: `.ai/03_plans/phase-8-graph-contract-indexing-plan.md` → `.ai/09_archive/plans/phase-8-graph-contract-indexing-plan.md`
- Move: `.ai/03_plans/phase-9-query-ai-layer-plan.md` → `.ai/09_archive/plans/phase-9-query-ai-layer-plan.md`
- Move: `.ai/03_plans/ultimate-architecture-upgrade-plan.md` → `.ai/09_archive/plans/ultimate-architecture-upgrade-plan.md`
- Modify: `.ai/03_plans/INDEX.md` — update the three rows to point at `../09_archive/plans/`, mark status ✅/❌, update the "Execution Order" narrative at the bottom

- [ ] **Step 1: Move the three plan files with `git mv`**

Run (sequentially, one command):
```bash
cd /Users/philiplewis/vitruvius && \
  git mv .ai/03_plans/phase-8-graph-contract-indexing-plan.md .ai/09_archive/plans/ && \
  git mv .ai/03_plans/phase-9-query-ai-layer-plan.md .ai/09_archive/plans/ && \
  git mv .ai/03_plans/ultimate-architecture-upgrade-plan.md .ai/09_archive/plans/
```

Expected: three `renamed:` entries in `git status`.

- [ ] **Step 2: Update INDEX.md row for phase-8**

Old row (Phase 8):
```
| 8 | `phase-8-graph-contract-indexing` | Graph Contract & Filesystem-Backed Indexing | 🧩 **Subsumed** by Stream H of statistical upgrade | — | design_spec | [phase-8-graph-contract-indexing-plan.md](phase-8-graph-contract-indexing-plan.md) |
```

New row:
```
| 8 | `phase-8-graph-contract-indexing` | Graph Contract & Filesystem-Backed Indexing | ✅ **Subsumed + archived** — base work shipped inside Sprint D Stream H (2026-04-14); original design spec moved to archive 2026-04-15 | Sprint D — closed | design_spec | [../09_archive/plans/phase-8-graph-contract-indexing-plan.md](../09_archive/plans/phase-8-graph-contract-indexing-plan.md) |
```

- [ ] **Step 3: Update INDEX.md row for phase-9**

Old row (Phase 9):
```
| 9 | `phase-9-query-ai-layer` | Query & AI Augmentation Layer | 🧩 **Subsumed** by Stream I of statistical upgrade | — | design_spec | [phase-9-query-ai-layer-plan.md](phase-9-query-ai-layer-plan.md) |
```

New row:
```
| 9 | `phase-9-query-ai-layer` | Query & AI Augmentation Layer | ✅ **Subsumed + archived** — base work shipped inside Sprint D Stream I (2026-04-14); original design spec moved to archive 2026-04-15 | Sprint D — closed | design_spec | [../09_archive/plans/phase-9-query-ai-layer-plan.md](../09_archive/plans/phase-9-query-ai-layer-plan.md) |
```

- [ ] **Step 4: Update INDEX.md row for ultimate-architecture-upgrade**

Old row:
```
| 9+ | `ultimate-architecture-upgrade` | Ultimate Architecture Upgrade (legacy superset covering Streams I–X) | ❌ **Superseded** — narrative retained, tasks distributed across 3D-Spatial / phase-8B / phase-13 / phase-16 / per-layer-embeddings (see governing plan §4.6) | — | design_spec | [ultimate-architecture-upgrade-plan.md](ultimate-architecture-upgrade-plan.md) |
```

New row:
```
| 9+ | `ultimate-architecture-upgrade` | Ultimate Architecture Upgrade (legacy superset covering Streams I–X) | ❌ **Superseded + archived** — narrative retained, successor plans all shipped and archived; moved to archive 2026-04-15 (see governing plan §4.6) | — | design_spec | [../09_archive/plans/ultimate-architecture-upgrade-plan.md](../09_archive/plans/ultimate-architecture-upgrade-plan.md) |
```

- [ ] **Step 5: Add a "2026-04-15 cleanup pass" note under the "Updated" line in INDEX.md**

After the `> **Updated:** 2026-04-15` line near the top, insert:
```
> **2026-04-15 cleanup pass:** Archived `phase-8-graph-contract-indexing`, `phase-9-query-ai-layer`, and `ultimate-architecture-upgrade` plans. All successor sprint plans have shipped and are listed as ✅ complete above. Active plan count is now **5** (governing, INDEX, ingestion contract, phase-1B, statistical-upgrade).
```

- [ ] **Step 6: Read-back verify**

Run: `grep -c '^| ' .ai/03_plans/INDEX.md`
Expected: the same row count as before (edits are in-place, no row added or removed).

Run: `ls .ai/03_plans/*.md | wc -l`
Expected: `5` (governing, INDEX, ingestion contract, phase-1B, statistical-upgrade) + this cleanup plan itself = **6** while this plan lives in `.ai/03_plans/`; once this cleanup plan self-archives at the end it drops back to 5.

Run: `ls .ai/09_archive/plans/phase-8-*.md .ai/09_archive/plans/phase-9-*.md .ai/09_archive/plans/ultimate-*.md`
Expected: all three files listed, no errors.

---

## Task 2: Refresh `.ai/00_system/architecture.md` (Wave A — parallel-safe)

**Why:** The current architecture doc (dated 2026-04-14) only describes the pre-Sprint-D package layout. It doesn't mention the Rust crates, the TypeScript sibling, or the ~10 new Python subpackages that shipped in this session's nine sprints. Any new engineer reading `architecture.md` today would think the codebase is Python-only.

**Files:**
- Modify: `.ai/00_system/architecture.md` — append a new `## Post-Sprint-D Layered Additions (2026-04-15)` section after the existing `### 2. Core Packages` block. Do **not** rewrite the pre-existing prose — the pre-Sprint-D layering is still authoritative for the ingestion/canonicalization core.

- [ ] **Step 1: Read the current file**

Run: `cat .ai/00_system/architecture.md`

Identify the end of the `### 2. Core Packages` block and confirm it ends with the `- `paths.py`, `constants.py`` bullet.

- [ ] **Step 2: Append the new section**

After the `### 2. Core Packages` block and its trailing horizontal rule (`---`), append:

````markdown
## Post-Sprint-D Layered Additions (2026-04-15)

The nine sprints closed in 2026-04-15 added substantial capability on top of the pre-existing filesystem pipeline. The core ingestion/canonicalization layout above is unchanged; the additions below are **layered on top** and most are gated behind feature flags that default to `false`.

### New Python subpackages

- `scripts/vitruvius/compound/` — Sprint Z reactive neuro-symbolic OS. Subcomponents:
  - `adversarial.py` — Proposer/Inspector/Adjudicator swarm (S2)
  - `dspy_compiler.py` — prompt compiler with metric-driven search (S5)
  - `dependency_tracker.py` + `differential_propagator.py` — incremental dataflow (S3)
  - `logic_schema.py` — Pydantic envelope for `<logic>` Datalog fact sets (S1)
  - `wasm_kernel.py` — lazy-import wrapper around the Wasm spatial kernel (S4)
- `scripts/vitruvius/wiki/` — Sprint WIKI autonomous knowledge synthesis:
  - `docling_parser.py`, `kuzu_store.py`, `delta_tracker.py`, `synthesis_loop.py`, `ego_linter.py`
  - `llm_client.py` (Protocol) + `ollama_client.py` (concrete adapter)
- `scripts/vitruvius/geometric/` — Sprint GEOM buildable-envelope engine:
  - `inequality_compiler.py` (Z3 CSP), `envelope_2d.py` (shapely), `envelope_3d.py` (trimesh + mapbox-earcut + manifold3d), `pareto_optimizer.py` (cvxpy)
- `scripts/vitruvius/foraging/` — Sprint GT.5.2 Bloom filter foraging hints
- `scripts/vitruvius/spatial/` — Sprint H / GT.4 spatial data plane:
  - `spatial_edge_builder.py` (decay-weighted edges), `proximity_jump.py` (Sprint GT.4)
- `scripts/vitruvius/graph/` — Phase 8 base plus Sprint GT/HP/PHYS additions:
  - `contract.py` — `GraphNode` / `GraphEdge` / `GraphSnapshot` / `TemporalEdge` (GT.3.1)
  - `event_store.py` — SQLite append-only event log (HP.3) + `Delta` wrapper (S3.1)
  - `graphsage.py` — HP.5 GraphSAGE embeddings + loopholes detector
  - `temporal_query.py` — GT.3.2 versioned retrieval (`query_at`)
  - `parquet_archiver.py` — GT.3.3 pyarrow round-trip
  - `mc_dropout.py` — GT.5.3 epistemic uncertainty
  - `physics.py` — Sprint PHYS PageRank / Boltzmann gate / VF2 / Shannon entropy / eigenvector centrality / cascade sim
- `scripts/vitruvius/pre_review/` + `review/` + `promotion/` — Sprint Q W2/W3 wiring:
  - `pre_review/nb_filter.py`, `review/ontology_prompt.py`, `review/slm_router.py`, `review/conformal.py`, `review/tension_analyzer.py`, `review/reflection_parser.py`, `review/choquet.py`, `review/ontology_prompt_builder.py`, `review/cot_audit.py`
  - `promotion/bayesian_fusion.py`, `promotion/stringency_matrix.py`, `promotion/temporal_edges.py`
- `scripts/vitruvius/priming/` — Sprint R Stream Y1 contextual priming (source identity vector, prefix injector, drift detector)
- `scripts/vitruvius/bench/` — Sprint Q W4 benchmark harness (live PD 1096 wall-clock + peak RSS)
- `scripts/vitruvius/merkle_fs.py` — HP.1 Merkle directory hash (single-file module)

### Rust data plane

Vitruvius now ships two pyo3 Rust crates built via `maturin develop --release`:

- `scripts/vitruvius/engine_rs/` — **Cargo workspace** split into `core/` (pure Rust, compiles for both native and `wasm32-unknown-unknown`) and `pyo3_shim/` (pyo3 bindings). Exports `SpatialPoint` + `LinearOctree` to Python and an `aabb_intersects` C-ABI function to Wasm. Consumed by `scripts/vitruvius/compound/wasm_kernel.py` via wasmtime.
- `scripts/vitruvius/datalog_rs/` — Sprint Z Stream S1.2 Rust evaluator. Hand-rolled Datalog engine (crepe proved too fragile on our ruleset). Entry point: `evaluate_datalog(facts, rules)`. 7 Rust unit tests.

Both crates are optional dependencies. Pure-Python paths remain intact and are exercised by the test suite when the Rust extension isn't built.

### TypeScript sibling subproject

- `spatial-daemon/` — Node.js 25 + vitest sibling subproject (not inside `scripts/vitruvius/`). Implements GJK collision detection, AABB overlap, and a filesystem contract writer that the Python side consumes. Entry point: `spatial-daemon/src/cli.ts`. 20/20 vitest tests. Used for 3D spatial verification when ingesting building geometries.

### Feature-flag governance

All nine sprints added flag families under `features:` in `config/vitruvius.yaml`. Default is **false** for every new flag so pre-session behaviour is byte-identical until an operator opts in. The `EXPECTED_FLAGS` registry in `scripts/tests/test_features.py` enumerates every expected flag and fails CI if a flag is added to the YAML without a test entry.

Flag families by sprint:

| Sprint | Prefix | Example |
|---|---|---|
| Q — Live Wiring | `w_*` | `w_nb_prefilter`, `w_slm_router`, `w_choquet_fusion` |
| R — Per-Layer Embeddings | `y_*` | `y_priming`, `y_domain_moe`, `y_vision_ocr` |
| PHYS — Graph Physics | `phys_*` | `phys_pagerank`, `phys_boltzmann_gate` |
| HP — High-Performance | `hp_*` | `hp_merkle_fs`, `hp_sqlite_events`, `hp_wasm_kernels`, `hp_graphsage` |
| GEOM — Constraint Engine | `geom_*` | `geom_inequality_compiler`, `geom_envelope_3d` |
| WIKI — Knowledge Synthesis | `wiki_*` | `wiki_docling`, `wiki_kuzu_store`, `wiki_ego_linter` |
| GT — Geo-Topological | `gt_*` | `gt_temporal_edges`, `gt_spatial_jump`, `gt_bloom_foraging` |
| Z — Compound AI | `z_*` | `z_neuro_symbolic`, `z_adversarial_swarm`, `z_dspy_compiler` |

### Deferred items

Two items remain externally gated:

- **Sprint D Streams J (query integration) + K (docs+CI)** — need the Ranger dashboard surface and a 2nd jurisdiction corpus to benchmark against.
- **Phase 1B Modernization §11 Phase 2 + Phase 3** — parser wrapping + Docling/Marker + ProcessPoolExecutor + Golden Corpus. Design spec exists at `.ai/03_plans/phase-1b-multi-parser-integration-plan.md` but needs a TDD expansion pass.

For the authoritative per-sprint ledger see `.ai/10_state/decisions.md` AD-024 through AD-028.
````

- [ ] **Step 3: Read-back verify**

Run: `grep -c '^## Post-Sprint-D' .ai/00_system/architecture.md`
Expected: `1`

Run: `grep -c 'engine_rs' .ai/00_system/architecture.md`
Expected: `≥2`

Run: `grep -c 'spatial-daemon' .ai/00_system/architecture.md`
Expected: `≥1`

---

## Task 3: Refresh `.ai/00_system/pipeline-overview.md` (Wave A — parallel-safe)

**Why:** Current pipeline-overview (dated 2026-04-14) still describes only the ingestion → convert → canonicalize → extract → review → promote path. It doesn't mention the Sprint Q live wiring (NB prefilter, SLM router, ontology prompt builder, conformal, Choquet, reflection), the Sprint R agentic registry / vision OCR / CoT audit layers, the Sprint Z compound AI loop, or the Sprint GT spatial GraphRAG path.

**Files:**
- Modify: `.ai/00_system/pipeline-overview.md` — append a new `## Post-Sprint-D Pipeline Additions (2026-04-15)` section after the existing `## End-to-End Execution Flow` block. Do **not** rewrite the pre-existing flow — it's still the authoritative default path.

- [ ] **Step 1: Read the current file**

Run: `cat .ai/00_system/pipeline-overview.md`

Identify the end of the numbered execution flow list and confirm it ends with a `Review` step.

- [ ] **Step 2: Append the new section**

After the existing `## End-to-End Execution Flow` block, append:

````markdown
## Post-Sprint-D Pipeline Additions (2026-04-15)

The baseline flow above is the authoritative default-off path. The nine sprints closed in this session layered additional optional stages on top, all gated behind `features.*` flags in `config/vitruvius.yaml`. When every flag is `false`, the pipeline is byte-identical to the pre-Sprint-D baseline described above.

### Sprint Q — Live Wiring (w_* flags)

The review stage (`run_review_ollama`) now has optional live hooks for the Stream F + G scaffolds that Sprint D shipped as dead code:

1. **NB prefilter** (`w_nb_prefilter`) — auto-rejects candidates a Naive Bayes head scores below threshold before any LLM call.
2. **Ontology prompt builder** (`w_ontology_prompt`) — renders 2-hop graph neighborhoods from the canonical relationships store into the reviewer prompt so the LLM can cross-reference prior decisions.
3. **SLM domain router** (`w_slm_router`) — picks between 1B / 3B / 8B local models by document class and candidate novelty.
4. **Conformal gate** (`w_conformal_gate`) — decorates every review decision with a p-value that drops anything above the calibrated α.
5. **Tension analyzer + Choquet fuzzy aggregation** (`w_choquet_fusion`) — fuses multiple reviewer votes when Tier 2 fires.
6. **Reflection parser** (`w_reflection_parser`) — extracts `<reflection>` blocks from the reviewer output and feeds them into the Sprint R CoT audit log.
7. **Binary mode + num_ctx cap + budget guard** (`w_8gb_survival`) — caps memory so `gemma4:e4b` fits on 8 GB M2.

Promotion (`run_promote`) gained a **stringency matrix gate** (`w_stringency_gate`) that compares each candidate edge against the governing standard in the 20-concept stringency vectors. Losing edges are marked `is_governing_standard=False`; the winner is marked `True`. This is a Sprint W3 addition.

### Sprint R — Per-Layer Embeddings & Agentic Reasoning (y_* flags)

Layered on top of the review stage:

1. **Source identity vector + prefix injector** (`y_priming`) — every reviewer prompt is prefixed with a deterministic `SOURCE_IDENTITY[fingerprint]: <prose>` block so the LLM sees the document's legal context for free.
2. **Domain classifier + MoE router** (`y_domain_moe`) — routes candidates to specialized reviewer models by detected domain (building-law vs. fire-code vs. sanitation, etc.).
3. **Thinking mode + CoT audit** (`y_cot_audit`) — enforces `<thinking>` / `<answer>` envelope in the reviewer output and dumps the trace to `005_Operational-Intelligence-Layer/cot_audit/`.
4. **Stateful agentic registry** (`y_agentic_registry`) — SQLite registry of every reviewer decision; consumed by Phase 6A Resume to avoid re-reviewing unchanged candidates.
5. **Vision OCR** (`y_vision_ocr`) — falls back to a vision LLM (moondream) when OCR confidence is below threshold. Operator-gated: requires `ple-vision-probe` activation.

### Sprint GT — Spatial GraphRAG (gt_* flags)

New optional stage between extraction and review:

- **Proximity jump + decay-weighted edges** (`gt_spatial_jump`) — when `spatial_edge_builder` has ingested a building's geometry, candidates are re-ranked so spatially adjacent sections boost each other's confidence before the LLM sees them.
- **Temporal edges** (`gt_temporal_edges`) — graph contract now supports `valid_from` / `valid_until` on every edge so rollback-aware queries work through `temporal_query.query_at(timestamp)`.
- **Parquet archiver** (`gt_parquet_archive`) — snapshots the graph to Parquet via pyarrow for cold-storage archival and off-session audit.
- **Bloom filter foraging** (`gt_bloom_foraging`) — Sprint GT.5.2 optimization that uses a Bloom filter to skip definitely-absent concept edges during retrieval.

### Sprint Z — Compound AI (z_* flags)

A new post-review stage that only activates on Tier 2 candidates:

- **Adversarial swarm** (`z_adversarial_swarm`) — Proposer generates candidates, Inspector argues against them, Adjudicator picks a winner.
- **Differential dataflow** (`z_differential_dataflow`) — `DependencyTracker` + `DifferentialPropagator` propagate deltas from the graph store to downstream consumers without re-evaluating the whole graph.
- **DSPy prompt compiler** (`z_dspy_compiler`) — metric-driven prompt optimization that compiles prompt templates against a held-out set of review decisions.
- **Neuro-symbolic Datalog bridge** (`z_neuro_symbolic`) — reviewer prompts are decorated with a `<logic-directive>` that forces the LLM to emit a `<logic>` Datalog block the Rust `datalog_rs` evaluator verifies. Rejects the verdict if the block fails to derive the conclusion from the facts.
- **Wasm spatial kernel** (`z_wasm_kernel`) — loads the `engine_rs` `aabb_intersects` function via wasmtime for hermetic spatial verification that can run in constrained environments.

### Sprint WIKI — Knowledge Synthesis (wiki_* flags)

Standalone side-pipeline (not in the main `run` chain):

- `wiki_docling` — Docling parser for PDF → structured markdown
- `wiki_kuzu_store` — Kuzu graph store (hybrid vector + graph)
- `wiki_delta_tracker` — SHA-256 delta tracker for incremental synthesis
- `wiki_synthesis_loop` — LLM-driven wiki synthesis loop (uses `OllamaLLMClient`)
- `wiki_ego_linter` — LLM ego-graph linter that rejects drafts with internal contradictions

### Sprint PHYS — Graph Physics (phys_* flags)

Post-promotion analytics layer:

- `phys_pagerank` — Sprint PHYS.1 PageRank over the canonical relationship graph
- `phys_boltzmann_gate` — Sprint PHYS.2 Boltzmann stability gate (absorbs Stream O orphan VF2 motif matcher)
- `phys_shannon_sampler` — Sprint PHYS.3 Shannon entropy sampler
- `phys_eigencascade` — Sprint PHYS.4 eigenvector centrality cascade sim

### Sprint GEOM — Geometric Constraint Engine (geom_* flags)

Standalone side-pipeline for buildable-envelope generation:

- `geom_inequality_compiler` — Z3 CSP compiler from canonical rules
- `geom_envelope_2d` — 2D envelope via shapely
- `geom_envelope_3d` — 3D envelope via trimesh + mapbox-earcut + manifold3d
- `geom_pareto_optimizer` — multimodal IoU audit via cvxpy

### Sprint HP — High-Performance Optimizations (hp_* flags)

Transparent perf wins:

- `hp_merkle_fs` — Sprint HP.1 Merkle directory hash (replaces brute-force reconcile walks)
- `hp_sqlite_events` — Sprint HP.3 SQLite append-only event log (pivoted from RocksDB — no wheel for Apple Silicon Python 3.11)
- `hp_wasm_kernels` — Sprint HP.4 Wasm spatial kernels (via `engine_rs` wasm32 target)
- `hp_graphsage` — Sprint HP.5 GraphSAGE embeddings + structural loopholes detector

See `.ai/10_state/decisions.md` AD-024 through AD-028 for the per-sprint ledger including commit SHAs and sprint tags.
````

- [ ] **Step 3: Read-back verify**

Run: `grep -c '^## Post-Sprint-D Pipeline' .ai/00_system/pipeline-overview.md`
Expected: `1`

Run: `grep -c 'Sprint [A-Z]' .ai/00_system/pipeline-overview.md`
Expected: `≥15` (at least one mention per sprint)

---

## Task 4: Add SUPERSEDED banners to 5 audit files (Wave A — parallel-safe)

**Why:** The 5 audits in `.ai/02_audits/` are dated 2026-04-13 (pre-everything). They represent a frozen historical snapshot of what the codebase looked like *before* Sprints A/B/C/D/Q/R/PHYS/H/GEOM/WIKI/GT/HP/Z. They are still useful as history but a reader today needs a pointer to where the current state lives. Do **not** rewrite them — only add a banner at the top of each.

**Files (5 files, all edited identically):**
- `.ai/02_audits/codebase-roadmap-audit.md`
- `.ai/02_audits/extraction-audit.md`
- `.ai/02_audits/ingestion-audit.md`
- `.ai/02_audits/normalization-audit.md`
- `.ai/02_audits/review-layer-audit.md`

- [ ] **Step 1: Prepend the SUPERSEDED banner to all 5 files**

For each file, insert this block at the **very top** (before the existing `# Vitruvius ...` heading):

```markdown
> ⚠️ **HISTORICAL SNAPSHOT — SUPERSEDED 2026-04-15**
>
> This audit was written on 2026-04-13 against a pre-Sprint-A baseline. It is retained here as a frozen historical record of what the codebase looked like before Sprints A + B + C + D + Q + R + PHYS + H + GEOM + WIKI + GT + HP + Z shipped. Almost every "weakness" or "missing feature" flagged below has since been addressed.
>
> **For the current state of the codebase, read these instead:**
> - `/.ai/10_state/active_context.md` — current session state
> - `/.ai/10_state/decisions.md` — architecture decisions AD-001 through AD-028
> - `/.ai/01_roadmap/current-phase.md` — current sprint / phase
> - `/.ai/00_system/architecture.md` — current package layout (including post-Sprint-D additions)
> - `/.ai/00_system/pipeline-overview.md` — current execution flow

---

```

**Important:** the `---` horizontal rule at the bottom of the banner ends the frontmatter and separates it from the original `# Vitruvius ...` heading that follows.

- [ ] **Step 2: Read-back verify**

Run: `grep -l 'HISTORICAL SNAPSHOT — SUPERSEDED 2026-04-15' .ai/02_audits/*.md`
Expected: all 5 files listed, no errors.

Run: `head -3 .ai/02_audits/codebase-roadmap-audit.md`
Expected: first line is `> ⚠️ **HISTORICAL SNAPSHOT — SUPERSEDED 2026-04-15**`.

---

## Task 5: Refresh `.ai/10_state/known_issues.md` (Wave A — parallel-safe)

**Why:** Current `known_issues.md` (dated 2026-04-14) covers RI-001 through RI-012. Several later sprints may have further closed or mitigated open risks, and none of the Sprint D+ sprints have added any new RI entries. The risk severity summary is also stale (still shows RI-002 as "MITIGATED (not formally closed)").

**Files:**
- Modify: `.ai/10_state/known_issues.md`

- [ ] **Step 1: Update the `> **Updated:** 2026-04-14` line**

Old:
```
> **Updated:** 2026-04-14
```

New:
```
> **Updated:** 2026-04-15 (post-Sprint-Z closure pass — 9 sprints closed this session)
```

- [ ] **Step 2: Update RI-002 status**

Old text (under `### RI-002: Regex Extraction Fragility (SUBSTANTIALLY MITIGATED 2026-04-14)`):
```
**Closure:** Phase 5E (LLM-assisted extraction) remains the long-term full fix for paragraph-boundary sensitivity. The 4 layers above make it non-urgent.
```

New text:
```
**Closure:** Phase 5E (LLM-assisted extraction) remains the long-term full fix for paragraph-boundary sensitivity. The 4 layers above made it non-urgent. Sprint D Stream E then shipped spaCy SVO parser + CRF trainer/extractor + TransE link predictor as a layered fallback; Sprint Q W2 wired the NB prefilter / SLM router / Choquet fusion / reflection parser live. On PD 1096 IRR the effective rejection rate is now ~10% reaching the Tier 2 LLM. The original regex path is still authoritative; Sprint D / Q additions run alongside it, never replacing it.
```

- [ ] **Step 3: Add closure note for RI-001**

Under `### RI-001: Filesystem Coupling`, the current "Closure" line reads:
```
- **Closure:** Permanent operating rule. Not a phase.
```

Leave this unchanged — RI-001 is still a permanent operating rule — but add a new line underneath the existing "Closure" bullet:
```
- **Sprint HP.1 note (2026-04-15):** the Merkle directory hash (`hp_merkle_fs` flag, `scripts/vitruvius/merkle_fs.py`) makes structural drift detectable in O(1) rather than requiring a full walk. The coupling stays; it's just cheaper to audit now.
```

- [ ] **Step 4: Update the Risk Severity Summary table**

Old table (at the bottom of the file):
```
## Risk Severity Summary (updated 2026-04-14 after Sprints A + B + Phase 3C + quality pass + Phase 1B Foundation + Sprint C quality pass)
| Severity | Count | IDs |
|---|---|---|
| HIGH | 1 | RI-001 (permanent operating rule) |
| MEDIUM | 1 | RI-010 (4/20 remaining) |
| LOW | 1 | RI-004 |
| MITIGATED (not formally closed) | 1 | RI-002 (pre-review filter cut false positives from 82% → ~22%) |
| CLOSED | 8 ✅ | RI-003, RI-005 (next pass), RI-006, RI-007, RI-008, RI-009, RI-011, RI-012 |
```

New table:
```
## Risk Severity Summary (updated 2026-04-15 after full 9-sprint session — Q + R + PHYS + H + GEOM + WIKI + GT + HP + Z closed)
| Severity | Count | IDs |
|---|---|---|
| HIGH | 1 | RI-001 (permanent operating rule — Sprint HP.1 made it cheaper to audit) |
| MEDIUM | 1 | RI-010 (4/20 remaining — awaiting corpus expansion, no LLM fallback) |
| LOW | 1 | RI-004 (environment / PYTHONPATH — still tolerable per AD-002) |
| MITIGATED (not formally closed) | 1 | RI-002 (pre-review filter + Sprint D Stream E + Sprint Q W2 wiring cut effective rejection to ~10%) |
| CLOSED | 8 ✅ | RI-003, RI-005 (next pass), RI-006, RI-007, RI-008, RI-009, RI-011, RI-012 |

**No new RI entries were opened by the 2026-04-15 sprint burst.** Every new capability shipped defaulted to `features.*: false` in `config/vitruvius.yaml` and was covered by a test registry entry in `scripts/tests/test_features.py`, so there's no silent surface area to track.
```

- [ ] **Step 5: Update the Closure Timeline table**

Old table:
```
## Closure Timeline
| When | Risks Closed |
|---|---|
| **Sprint A (2026-04-14)** | ✅ RI-006, ✅ RI-003 (partial) |
| **Sprint B (2026-04-14)** | ✅ RI-003 (full), ✅ RI-007 (MVP), ✅ RI-011, ✅ RI-012 |
| **Sprint C · Phase 1B Foundation (2026-04-14)** | ✅ RI-009 (Task 0 — SHA-256 file hashing) |
| **Sprint C · Quality Pass (2026-04-14)** | ✅ RI-008 (Q2 — rotate-registries CLI) |
| Future | RI-002 (Phase 5E), RI-010 (Phase 3C — 4 concepts need corpus expansion) |
| Permanent rule | RI-001, RI-004 |
```

New table:
```
## Closure Timeline
| When | Risks Closed / Mitigated |
|---|---|
| **Sprint A (2026-04-14)** | ✅ RI-006, ✅ RI-003 (partial) |
| **Sprint B (2026-04-14)** | ✅ RI-003 (full), ✅ RI-007 (MVP), ✅ RI-011, ✅ RI-012 |
| **Sprint C · Phase 1B Foundation (2026-04-14)** | ✅ RI-009 (Task 0 — SHA-256 file hashing) |
| **Sprint C · Quality Pass (2026-04-14)** | ✅ RI-008 (Q2 — rotate-registries CLI) |
| **Sprint D (2026-04-14)** | RI-002 further mitigated (Stream E spaCy/CRF/TransE) |
| **Sprint Q (2026-04-15)** | RI-002 further mitigated (W2 NB/SLM/Choquet/reflection wiring) |
| **Sprint HP (2026-04-15)** | RI-001 instrumentation win (Merkle fs makes drift detectable in O(1)) |
| Future | RI-002 (Phase 5E), RI-010 (4 concepts need corpus expansion) |
| Permanent rule | RI-001, RI-004 |
```

- [ ] **Step 6: Read-back verify**

Run: `grep -c '2026-04-15' .ai/10_state/known_issues.md`
Expected: `≥5`

Run: `grep -c '^### RI-' .ai/10_state/known_issues.md`
Expected: `12` (RI-001 through RI-012 — no new RIs added, no old RIs removed)

---

## Task 6: Update `.ai/01_roadmap/master-roadmap.md` (Wave A — parallel-safe)

**Why:** `master-roadmap.md` is v2.0.0 (dated 2026-04-14) and is explicitly the authoritative-for-phase-status source. Its §5 (Honest Position Statement), §6 (Phase Contracts), and §8 (90-Day Execution Sequence) are now materially wrong — Phase 8 and Phase 9 are still listed as "NOT STARTED" there, and §8 only has Sprints A + B marked closed.

Do **not** rewrite the vision/strategy/governance sections (§1-§4) — those are long-form policy and still valid. Focus edits on §5, §6 (Phase 8 + Phase 9 contracts only), §8, §11 (cadence), and §13 (reference index).

**Files:**
- Modify: `.ai/01_roadmap/master-roadmap.md`

- [ ] **Step 1: Update the version header**

Old:
```
> **Version:** 2.0.0 · **Last revised:** 2026-04-14 · **Next review due:** 2026-05-01
```

New:
```
> **Version:** 2.1.0 · **Last revised:** 2026-04-15 · **Next review due:** 2026-05-01
```

- [ ] **Step 2: Add a 2.1.0 changelog entry at the bottom of the file**

At the very bottom of the file, under the existing `## Changelog` section (which currently has a `2.0.0` entry), append a new `### 2.1.0 — 2026-04-15` subsection:

```markdown
### 2.1.0 — 2026-04-15

**Scope:** Reconcile §5 Honest Position, §6 Phase 8 + Phase 9 contracts, §8 90-Day Execution Sequence, §11 Cadence, and §13 Reference Index against the 2026-04-15 session (nine sprints closed).

- **§5 Honest Position** — rewritten to reflect all 9 sprints closed (Q, R, PHYS, H, GEOM, WIKI, GT, HP, Z) with 1364 / 1364 Python tests, 20 / 20 TypeScript tests, 10 Rust unit tests, 31 verified relationships.
- **§6 Phase 8 contract** — marked `✅ SUBSUMED` by Sprint D Stream H (shipped 2026-04-14) with a pointer to `phase-8b-geo-topological-graph-plan.md` (Sprint GT) for the extensions.
- **§6 Phase 9 contract** — marked `✅ SUBSUMED` by Sprint D Stream I (shipped 2026-04-14).
- **§8 90-Day Execution Sequence** — all 9 governing-plan sprints marked closed; "What's next" block rewritten to point at Phase 1B Modernization, Sprint D J/K externally gated items, and a fresh roadmap brainstorm as the open options.
- **§11 Cadence** — notes that the "large autonomous sprint burst" delivery model (9 sprints in 1 session via subagent-driven-development) has been validated and is the new working pattern.
- **§13 Reference Index** — added entries for the 3 newly-archived plans (phase-8, phase-9, ultimate-architecture) and for the governing plan.

No breaking changes to §1–§4 (vision, architecture map, governance contracts) or §9–§10 (KPIs, tech debt) — those remain authoritative as written in 2.0.0.
```

- [ ] **Step 3: Rewrite §5 Honest Position Statement**

Locate the `## 5. Honest Position Statement (updated 2026-04-14)` heading. Replace the entire section (up to but not including `## 6. Phase Contracts`) with:

```markdown
## 5. Honest Position Statement (updated 2026-04-15)

**What works end-to-end today:**
- Ingestion → conversion → refinement (Phase 1C MVP) → canonicalization → extraction → pre-review filter → Tier 1 LLM review → Tier 2 adjudication → promotion → canonical graph write.
- Sprint D Streams A–I shipped on 2026-04-14: dependency bootstrap, Shannon classifier, table-to-graph, parametric NER, Tier C OCR, AST chunker, TF-IDF/PMI/FCA, spaCy/CRF/TransE extraction, Bayesian fusion + stringency matrix + temporal edges (as scaffolds), Phase 8 base, Phase 9 base.
- Sprint Q (Live Wiring & 8GB Hardening) shipped on 2026-04-15: wired every Stream F + G scaffold into the live pipeline, rolled out the 20-concept stringency matrix gate, added the 8GB LLM survival mode, shipped the quality harness.
- Sprint R (Per-Layer Embeddings & Agentic) shipped on 2026-04-15: contextual priming, MoE domain routing, thinking-mode CoT audit, stateful agentic registry, vision OCR (operator-gated).
- Sprint PHYS (Statistical Mechanics & Graph Physics) shipped on 2026-04-15.
- Sprint H (3D Spatial Intelligence) shipped on 2026-04-15: all 20 tasks across Streams L/M/N/O; TypeScript sibling subproject at `spatial-daemon/`.
- Sprint GEOM (Geometric Constraint Engine) shipped on 2026-04-15: Z3 CSP, shapely/trimesh/cvxpy pipeline.
- Sprint WIKI (Autonomous Knowledge Synthesis) shipped on 2026-04-15: Docling + Kuzu + Ollama + ego linter.
- Sprint GT (Geo-Topological Knowledge Graph) shipped on 2026-04-15: pyo3 Rust crate + linear octree + temporal graph + spatial GraphRAG + hardware hardening.
- Sprint HP (High-Performance Optimizations) shipped on 2026-04-15: Merkle fs, SQLite event store (pivoted from RocksDB), Wasm spatial kernels, GraphSAGE loopholes.
- Sprint Z (Compound AI Evolution) shipped on 2026-04-15: neuro-symbolic Datalog bridge (Rust `datalog_rs` crate), adversarial swarm, differential dataflow, Wasm kernel, DSPy prompt compiler.

**Current hard numbers (as of 2026-04-15):**
- Python test suite: **1364 / 1364 passing**, 1 skipped
- TypeScript test suite: **20 / 20 passing** (spatial-daemon/)
- Rust unit tests: **10 passing** (engine_rs core + datalog_rs)
- Canonical relationships: **31 verified** (up from 7 via PD 1096 IRR ingest)
- Enriched concept files: **20 / 20** PD 1096 concepts (all carry `stringency_vector` frontmatter)
- Sprint tags: **9** — `sprint-q-closed`, `sprint-r-closed`, `sprint-phys-closed`, `sprint-h-closed`, `sprint-geom-closed`, `sprint-wiki-closed`, `sprint-gt-closed`, `sprint-hp-closed`, `sprint-z-closed`
- Decision log: **AD-001 through AD-028** in `.ai/10_state/decisions.md`
- Active branch: `feat/sprint-r-per-layer-embeddings` (misnomer — carries all 9 sprints; will be renamed on merge to main)

**What still needs doing:**
- **Sprint D Streams J (query integration) + K (docs+CI)** — externally gated on the Ranger dashboard surface (J) and a 2nd jurisdiction corpus (K). Will light up when their external unblockers land.
- **Phase 1B Modernization §11 Phase 2 + Phase 3** — parser wrapping + Docling/Marker/Surya + ProcessPoolExecutor + Golden Corpus. Design spec exists at `.ai/03_plans/phase-1b-multi-parser-integration-plan.md` but needs a TDD expansion pass before dispatch.
- **Merge + rename branch** — the current branch name is a misnomer. A clean merge to main with a rename is the natural next housekeeping step.
- **Fresh roadmap brainstorm** — the project is materially ahead of the v2.0.0 roadmap envelope. Next horizon is undefined; v2.1.0 extends only where the roadmap was visibly wrong, not where it was silent.

**Where to read the per-sprint ledger:** `.ai/10_state/decisions.md` AD-024 through AD-028 have the full commit SHAs, test counts, and exit gates for every sprint closed this session.

```

- [ ] **Step 4: Update §6 Phase 8 contract**

Locate the Phase 8 contract (under `## 6. Phase Contracts` → `### Phase 8 — ...`). Replace its current status line with:

Old (will vary by formatting but ends with something like):
```
**Status:** [ ] NOT STARTED
```

New:
```
**Status:** ✅ **SUBSUMED** — base work shipped inside Sprint D Stream H on 2026-04-14. Original design spec archived 2026-04-15 at `.ai/09_archive/plans/phase-8-graph-contract-indexing-plan.md`. Sprint GT (`sprint-gt-closed`) subsequently extended this with temporal edges, Parquet archiver, spatial GraphRAG bridge, and the `engine_rs` Rust data plane — see `phase-8b-geo-topological-graph-plan.md` (also archived).
```

- [ ] **Step 5: Update §6 Phase 9 contract**

Locate the Phase 9 contract. Replace its current status line with:

```
**Status:** ✅ **SUBSUMED** — base work shipped inside Sprint D Stream I on 2026-04-14. Original design spec archived 2026-04-15 at `.ai/09_archive/plans/phase-9-query-ai-layer-plan.md`. No follow-up sprint has extended it — Query/AI integration for external consumers is gated on Sprint D Stream J (Ranger dashboard surface), which is externally blocked.
```

- [ ] **Step 6: Rewrite §8 90-Day Execution Sequence**

Locate the `## 8. 90-Day Execution Sequence (Strict Order) — SPRINTS A + B CLOSED 2026-04-14` heading. Replace the heading and the entire section with:

```markdown
## 8. 90-Day Execution Sequence — ALL GOVERNING-PLAN SPRINTS CLOSED 2026-04-15

The strict execution order mandated by `00-governing-implementation-plan.md` has been **fully discharged** in this 2026-04-15 session via subagent-driven-development waves.

### Sprint chain (all closed)

| # | Sprint | Scope | Tag | AD ref |
|---|---|---|---|---|
| 1 | A — Phase 7 Promotion Governance | 17-rule validator, audit log, rollback | (pre-session) | AD-015 |
| 2 | B — Phase 1C + Phase 2 + Phase 6A/B | Normalization, canonicalizer, review gap closure | (pre-session) | AD-016/017 |
| 3 | C — Phase 1B Foundation + polish | Parsers subpackage, FileEntry.sha256, rotate-registries | (pre-session) | AD-022/023 |
| 4 | D — Statistical & Architectural Upgrade | Streams A-I (J/K deferred) | (pre-session) | AD-024 |
| 5 | Q — Live Wiring & 8GB Hardening | Wire F/G scaffolds live, 8GB LLM mode | `sprint-q-closed` | AD-024 |
| 6 | R — Per-Layer Embeddings & Agentic | Priming, MoE router, CoT audit, registry, vision OCR | `sprint-r-closed` | AD-025 |
| 7 | PHYS — Graph Physics | PageRank, Boltzmann gate, Shannon, eigenvector cascade | `sprint-phys-closed` | AD-026 |
| 8 | H — 3D Spatial Intelligence | Spatial ingest, Z3 solver, IFC/OWL, TS daemon | `sprint-h-closed` | AD-026 |
| 9 | GEOM — Geometric Constraint Engine | Z3 CSP, 2D/3D envelope, Pareto optimizer | `sprint-geom-closed` | AD-027 |
| 10 | WIKI — Autonomous Knowledge Synthesis | Docling, Kuzu, Ollama, ego linter | `sprint-wiki-closed` | AD-027 |
| 11 | GT — Geo-Topological Knowledge Graph | Rust crate, linear octree, temporal graph, spatial GraphRAG | `sprint-gt-closed` | AD-028 |
| 12 | HP — High-Performance Optimizations | Merkle fs, SQLite events, Wasm kernels, GraphSAGE | `sprint-hp-closed` | AD-028 |
| 13 | Z — Compound AI Evolution | Datalog bridge, adversarial swarm, differential dataflow, DSPy | `sprint-z-closed` | AD-028 |

### What's next (open options)

The governing plan's mandatory sprint chain is done. The remaining candidates are in priority order:

1. **Merge + rename branch** — `feat/sprint-r-per-layer-embeddings` carries all 9 sprints. Clean merge to main with a rename is the natural next housekeeping step. 30-minute task.
2. **Phase 1B Modernization (§11 Phase 2 + Phase 3)** — parser wrapping + Docling/Marker/Surya + ProcessPoolExecutor + Golden Corpus. Needs a TDD expansion pass on `phase-1b-multi-parser-integration-plan.md` first. Natural Sprint C continuation.
3. **Sprint D Streams J + K** — externally gated:
   - Stream J (query integration) needs the Ranger dashboard surface
   - Stream K (docs+CI) needs a 2nd jurisdiction corpus to benchmark against
4. **Fresh roadmap brainstorm** — project is materially ahead of the v2.0.0 envelope. Worth a fresh strategy pass before committing to a new sprint chain.

### Delivery pattern validation

The 2026-04-15 session validated **subagent-driven-development** as the working delivery pattern. Key parameters:
- Wave-parallel dispatch (up to 6 parallel implementers per wave with file-disjoint work)
- Two-stage review per task (spec compliance → code quality)
- Fresh subagent per task to avoid context pollution
- Single orchestrator-held commit at end of each wave to avoid `git add` races

Nine sprints closed in one session (test suite 297 → 1364 passing, 9 plans archived) is the delivery ceiling observed so far. Future planning can reasonably assume this cadence is repeatable when the plan specs are solid and the flag defaults are disciplined.
```

- [ ] **Step 7: Update §11 Cadence**

Locate `## 11. Cadence, Ownership, Review Process`. Append (do not replace) a new subsection at the bottom of §11:

```markdown
### 11.X — Subagent-Driven Wave Delivery (2026-04-15 addition)

Validated in the 2026-04-15 session that closed 9 sprints in a single working block. The pattern:

1. **Orchestrator extracts all tasks upfront** from the plan and creates a TodoWrite checklist (so parallel dispatches can be tracked).
2. **Wave-parallel dispatch** — up to ~6 parallel `Agent` calls per wave, each with file-disjoint work. More than 6 risks `git add` races and human-scale coordination errors.
3. **Per-task two-stage review** — spec compliance review first, then code quality review. Both are cheap model dispatches; both must pass before the task is marked complete.
4. **Orchestrator-held commits** — subagents write files but never run `git add` or `git commit`. The orchestrator stages and commits once per wave.
5. **Per-sprint AD ledger entry** — every sprint closure must produce an `AD-###` entry in `.ai/10_state/decisions.md` with commit SHAs, test deltas, sprint tag, and archival status.

Ceiling observed so far: **9 sprints per session**, **~1067 test delta**, **11 subagent dispatches** across 3 waves. Future sessions can use this as a planning baseline.
```

- [ ] **Step 8: Update §13 Reference Index**

Locate `## 13. Reference Index` and update the plan list to:
- Add an entry for `00-governing-implementation-plan.md` (active, meta doc)
- Mark `phase-8-graph-contract-indexing-plan.md` as archived
- Mark `phase-9-query-ai-layer-plan.md` as archived
- Mark `ultimate-architecture-upgrade-plan.md` as archived

Example edit — find any bullet list of plan references and append:

```
- `/.ai/03_plans/00-governing-implementation-plan.md` — governing orchestration plan (v1.0.0, 2026-04-15) — read this first before picking a plan to execute
- `/.ai/09_archive/plans/phase-8-graph-contract-indexing-plan.md` — ✅ subsumed by Sprint D Stream H, archived 2026-04-15
- `/.ai/09_archive/plans/phase-9-query-ai-layer-plan.md` — ✅ subsumed by Sprint D Stream I, archived 2026-04-15
- `/.ai/09_archive/plans/ultimate-architecture-upgrade-plan.md` — ❌ superseded, archived 2026-04-15
```

- [ ] **Step 9: Read-back verify**

Run: `grep -c '2.1.0' .ai/01_roadmap/master-roadmap.md`
Expected: `≥3`

Run: `grep -c 'sprint-z-closed\|sprint-hp-closed\|sprint-gt-closed' .ai/01_roadmap/master-roadmap.md`
Expected: `≥3`

Run: `grep -c 'SUBSUMED' .ai/01_roadmap/master-roadmap.md`
Expected: `≥2` (Phase 8 + Phase 9 contracts)

---

## Task 7: Extend `.ai/01_roadmap/milestone-tracker.md` (Wave A — parallel-safe)

**Why:** Milestone tracker currently stops at Phase 12 Gated (dated 2026-04-14). The 9 sprints closed this session need their own tracked sections appended at the bottom.

**Files:**
- Modify: `.ai/01_roadmap/milestone-tracker.md`

- [ ] **Step 1: Update the `**Revised:** 2026-04-14` line**

Old:
```
> **Revised:** 2026-04-14
```

New:
```
> **Revised:** 2026-04-15
```

- [ ] **Step 2: Update the Phase 8 and Phase 9 entries**

Old Phase 8 entry (line ~162):
```
## Phase 8 — Graph Contract & Indexing [ ] NOT STARTED
```

New:
```
## Phase 8 — Graph Contract & Indexing ✅ SUBSUMED (Sprint D Stream H, 2026-04-14)
Base work shipped inside Sprint D Stream H. Sprint GT (tag `sprint-gt-closed`) extended with temporal edges, Parquet archiver, spatial GraphRAG, pyo3 Rust crate + linear octree. See `.ai/09_archive/plans/phase-8-graph-contract-indexing-plan.md`.
```

Old Phase 9 entry (line ~172):
```
## Phase 9 — Query & AI Layer [ ] NOT STARTED
```

New:
```
## Phase 9 — Query & AI Layer ✅ SUBSUMED (Sprint D Stream I, 2026-04-14)
Base work shipped inside Sprint D Stream I. No follow-up sprint has extended this — Query/AI integration for external consumers is gated on Sprint D Stream J (Ranger dashboard surface), externally blocked. See `.ai/09_archive/plans/phase-9-query-ai-layer-plan.md`.
```

- [ ] **Step 3: Append Sprint Q-Z sections after `## References`**

At the very bottom of the file (after the `## References` section), append:

```markdown
---

# 2026-04-15 Session — All Governing-Plan Sprints Closed

The following nine sprints were delivered under subagent-driven-development in a single session and all produced `sprint-*-closed` git tags. Full ledgers live in `.ai/10_state/decisions.md` AD-024 through AD-028.

## Sprint Q — Live Wiring & 8GB Hardening ✅ CLOSED (tag `sprint-q-closed`)
- [x] W1 — 8GB LLM Survival Mode (model pool + num_ctx cap + budget guard + binary mode, +17 tests)
- [x] W2 — Review Pipeline Wiring (NB prefilter + ontology prompt + SLM router + conformal + tension/reflection + Choquet, +15 tests)
- [x] W3 — Stringency Matrix Live Gate (20-concept migration + lint rule + promotion hook + governing-standard field, +13 tests)
- [x] W4 — Quality Harness (e2e chain test + flag-OFF regression + bench harness + decision-log automation, +7 tests)
- [x] W5 — Docs Sync (bundled in docs commit)
- **Total:** +48 tests, 15 functional commits, archived at `.ai/09_archive/plans/live-wiring-and-8gb-hardening-plan.md`

## Sprint R — Per-Layer Embeddings & Agentic ✅ CLOSED (tag `sprint-r-closed`)
- [x] Y0 — Bootstrap & flags (priming/ shell, 5 y_* flags, backward-compat regression)
- [x] Y1 — Contextual priming (source identity vector, prompt prefix injector, drift detector, ontology wiring, extraction wiring)
- [x] Y2 — Domain-routing MoE (classifier, route_with_moe, policy file + loader, reviewer model hook)
- [x] Y3 — Thinking mode + CoT audit (parse_cot_strict, audit writer, enforcement, ple-cotrace-dump CLI)
- [x] Y4 — Stateful agentic registry (SQLite core, ollama_review wiring, vacuum/purge CLI, Phase 6A Resume integration)
- [x] Y5 — Vision OCR (wrapper with mocked tests, table_graph_extractor fallback, ple-vision-probe CLI, operator checklist)
- **Total:** 20/20 tasks, archived at `.ai/09_archive/plans/per-layer-embeddings-agentic-upgrade-plan.md`
- Note: Y5 requires operator activation (install psutil + Pillow + pull moondream + run probe + flip flag). Non-Y5 flags fully code-complete.

## Sprint PHYS — Graph Physics ✅ CLOSED (tag `sprint-phys-closed`)
- [x] PHYS.1 — PageRank over canonical relationship graph
- [x] PHYS.2 — Boltzmann stability gate (absorbs orphan Stream O VF2 motif matcher)
- [x] PHYS.3 — Shannon entropy sampler
- [x] PHYS.4 — Eigenvector centrality cascade sim
- **Total:** 4 streams + orphan absorption shipped atomically, archived at `.ai/09_archive/plans/phase-16-statistical-mechanics-graph-physics-plan.md`

## Sprint H — 3D Spatial Intelligence ✅ CLOSED (tag `sprint-h-closed`)
- [x] Streams L/M/N/O — 20/20 tasks shipped
- [x] TypeScript sibling subproject at `spatial-daemon/` (GJK + AABB + contract writer + CLI; 20/20 vitest tests)
- [x] Z3 solver integration for spatial constraints
- [x] IFC registry loader + OWL exporter (M.1/M.2)
- **Total:** 20/20 tasks, archived at `.ai/09_archive/plans/3d-spatial-intelligence-upgrade-plan.md`

## Sprint GEOM — Geometric Constraint Engine ✅ CLOSED (tag `sprint-geom-closed`)
- [x] GEOM.1 — Inequality compiler (Z3 CSP from canonical rules)
- [x] GEOM.2 — Envelope 2D (shapely)
- [x] GEOM.3 — Envelope 3D (trimesh + mapbox-earcut + manifold3d)
- [x] GEOM.4 — Multimodal IoU audit (cvxpy Pareto optimizer)
- **Total:** 4 streams shipped, archived at `.ai/09_archive/plans/phase-15-geometric-constraint-engine-plan.md`

## Sprint WIKI — Autonomous Knowledge Synthesis ✅ CLOSED (tag `sprint-wiki-closed`)
- [x] WIKI.1 — Docling parser + Kuzu hybrid store
- [x] WIKI.2 — Delta tracker + synthesis loop
- [x] WIKI.3 — SHA-256 delta linting + LLM ego-graph linter
- [x] WIKI.4 — Ollama client adapter for synthesis loop + ego linter
- **Total:** 4 streams shipped, archived at `.ai/09_archive/plans/phase-14-autonomous-knowledge-synthesis-plan.md`

## Sprint GT — Geo-Topological Knowledge Graph ✅ CLOSED (tag `sprint-gt-closed`)
- [x] GT.1 — pyo3 Rust crate scaffold (Cargo workspace, core + pyo3_shim)
- [x] GT.2 — Linear octree (SpatialPoint + LinearOctree exposed to Python)
- [x] GT.3 — Temporal knowledge graph (TemporalEdge + versioned query + Parquet archiver)
- [x] GT.4 — Spatial GraphRAG bridge (proximity jump + decay-weighted edges)
- [x] GT.5 — Hardware hardening (mmap + Bloom filter + MC dropout)
- **Total:** 5 streams shipped, archived at `.ai/09_archive/plans/phase-8b-geo-topological-graph-plan.md`

## Sprint HP — High-Performance Optimizations ✅ CLOSED (tag `sprint-hp-closed`)
- [x] HP.1 — Merkle directory hash
- [x] HP.2 — AST chunking (retroactively covered by Sprint D Stream C.2)
- [x] HP.3 — SQLite append-only event store (pivoted from RocksDB — no wheel for Apple Silicon Python 3.11)
- [x] HP.4 — Wasm spatial kernels (engine_rs workspace split)
- [x] HP.5 — GraphSAGE loopholes detector
- **Total:** 5 streams shipped, archived at `.ai/09_archive/plans/phase-13-high-performance-optimizations-plan.md`

## Sprint Z — Compound AI Evolution ✅ CLOSED (tag `sprint-z-closed`)
- [x] S1 — Neuro-symbolic Datalog bridge (Rust `datalog_rs` crate + pyo3 + prompt directive)
- [x] S2 — Proposer/Inspector/Adjudicator adversarial swarm
- [x] S3 — Differential dataflow (Delta + DependencyTracker + DifferentialPropagator)
- [x] S4 — Wasm kernel (workspace split + wasmtime loader)
- [x] S5 — DSPy prompt compiler
- **Total:** 5 streams shipped, archived at `.ai/09_archive/plans/phase-12-compound-ai-evolution-plan.md`

## Session-level totals
- **Test suite:** 297 → **1364 passing** (+1067 delta)
- **New Rust crates:** 2 (`engine_rs` workspace + `datalog_rs`)
- **New TypeScript sibling:** 1 (`spatial-daemon/`)
- **New Python subpackages:** 6 (`compound/`, `wiki/`, `geometric/`, `foraging/`, `priming/`, `bench/`)
- **Plans archived:** 9 in the sprint burst + 3 more in the 2026-04-15 cleanup pass (phase-8, phase-9, ultimate-architecture)
- **ADs added:** AD-024 through AD-028
- **Git tags:** 9 (all listed above)
```

- [ ] **Step 4: Read-back verify**

Run: `grep -c '^## Sprint [A-Z]\+ —' .ai/01_roadmap/milestone-tracker.md`
Expected: `≥9`

Run: `grep -c '2026-04-15' .ai/01_roadmap/milestone-tracker.md`
Expected: `≥10`

---

## Task 8: (Placeholder — merged into Task 1)

INDEX.md reconciliation is done as part of Task 1 since both operations touch the same file and serializing inside one task is cleaner than coordinating two.

---

## Task 9: Final atomic commit (Wave C — orchestrator only)

**Why:** Subagents write files but never run `git add` or `git commit`. The orchestrator performs one atomic commit after all of Task 1-7 have landed, so there are no `git add` races and the cleanup lands as a single reviewable changeset.

- [ ] **Step 1: Verify all expected file changes are present**

Run:
```bash
cd /Users/philiplewis/vitruvius && git status --short | grep -E '^(A|M|R|D) '
```

Expected output should include (exact order may vary):
```
M  .ai/00_system/architecture.md
M  .ai/00_system/pipeline-overview.md
M  .ai/01_roadmap/master-roadmap.md
M  .ai/01_roadmap/milestone-tracker.md
M  .ai/02_audits/codebase-roadmap-audit.md
M  .ai/02_audits/extraction-audit.md
M  .ai/02_audits/ingestion-audit.md
M  .ai/02_audits/normalization-audit.md
M  .ai/02_audits/review-layer-audit.md
M  .ai/03_plans/INDEX.md
R  .ai/03_plans/phase-8-graph-contract-indexing-plan.md -> .ai/09_archive/plans/phase-8-graph-contract-indexing-plan.md
R  .ai/03_plans/phase-9-query-ai-layer-plan.md -> .ai/09_archive/plans/phase-9-query-ai-layer-plan.md
R  .ai/03_plans/ultimate-architecture-upgrade-plan.md -> .ai/09_archive/plans/ultimate-architecture-upgrade-plan.md
M  .ai/10_state/known_issues.md
```

If any expected change is missing, report which task's output didn't land and re-dispatch.

- [ ] **Step 2: Stage the changes**

Run (explicit paths only — never `git add -A`):
```bash
cd /Users/philiplewis/vitruvius && \
  git add .ai/00_system/architecture.md \
          .ai/00_system/pipeline-overview.md \
          .ai/01_roadmap/master-roadmap.md \
          .ai/01_roadmap/milestone-tracker.md \
          .ai/02_audits/codebase-roadmap-audit.md \
          .ai/02_audits/extraction-audit.md \
          .ai/02_audits/ingestion-audit.md \
          .ai/02_audits/normalization-audit.md \
          .ai/02_audits/review-layer-audit.md \
          .ai/03_plans/INDEX.md \
          .ai/09_archive/plans/phase-8-graph-contract-indexing-plan.md \
          .ai/09_archive/plans/phase-9-query-ai-layer-plan.md \
          .ai/09_archive/plans/ultimate-architecture-upgrade-plan.md \
          .ai/10_state/known_issues.md
```

- [ ] **Step 3: Commit with a single explanatory message**

Run:
```bash
cd /Users/philiplewis/vitruvius && git commit -m "$(cat <<'EOF'
docs(cleanup): post-Sprint-Z docs reconciliation pass

Full 2026-04-15 docs cleanup after the 9-sprint session (Q/R/PHYS/
H/GEOM/WIKI/GT/HP/Z).

Archives three superseded plans:
- phase-8-graph-contract-indexing (subsumed by Sprint D Stream H)
- phase-9-query-ai-layer (subsumed by Sprint D Stream I)
- ultimate-architecture-upgrade (frontmatter already superseded)

Updates:
- .ai/00_system/architecture.md — post-Sprint-D layered additions
  (Rust crates, TS sibling, 6 new Python subpackages, feature flags)
- .ai/00_system/pipeline-overview.md — post-Sprint-D pipeline
  additions (w_*, y_*, gt_*, z_*, wiki_*, phys_*, geom_*, hp_*)
- .ai/01_roadmap/master-roadmap.md — v2.1.0 bump; §5 Honest Position
  rewritten; §6 Phase 8 + Phase 9 marked SUBSUMED; §8 90-day
  execution rewritten; §11 Cadence adds subagent-wave pattern; §13
  Reference Index refreshed
- .ai/01_roadmap/milestone-tracker.md — Phase 8/9 marked SUBSUMED;
  Sprint Q-Z sections appended
- .ai/02_audits/*.md — SUPERSEDED banners on all 5 audit files
  (pre-Sprint-A historical snapshots, retained but pointed to
  current state docs)
- .ai/03_plans/INDEX.md — 3 archival rows reconciled
- .ai/10_state/known_issues.md — 2026-04-15 pass; RI-001 HP.1 note;
  RI-002 Sprint D + Q mitigation notes; closure timeline extended

No code changes. No new risks opened. No AD-### entries added
(session closure already captured in AD-024 through AD-028 by the
state-doc sync commit 37f0f62).

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
EOF
)"
```

- [ ] **Step 4: Verify commit landed**

Run: `git log --oneline -1`
Expected: line starts with a SHA followed by `docs(cleanup): post-Sprint-Z docs reconciliation pass`.

Run: `git status --short`
Expected: no output for any file listed in Step 1 (the cleanup changes should all be committed).

- [ ] **Step 5 (optional): Self-archive this cleanup plan**

Once the commit lands, this plan itself has served its purpose. Move it to the archive in a follow-up commit:

```bash
cd /Users/philiplewis/vitruvius && \
  git mv .ai/03_plans/2026-04-15-docs-cleanup-plan.md \
         .ai/09_archive/plans/2026-04-15-docs-cleanup-plan.md && \
  git commit -m "$(cat <<'EOF'
chore(plans): archive 2026-04-15 docs cleanup plan

Plan delivered all tasks; moving to archive so the active plan
directory only shows things that still need attention.

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
EOF
)"
```

Also update `.ai/03_plans/INDEX.md` in the same commit to add a new row for the archived cleanup plan.

---

## Self-Review Checklist

**1. Spec coverage:** The user asked for updates to `.ai/00_system/`, `.ai/01_roadmap/`, `.ai/02_audits/`, `.ai/10_state/`, and an archival check on `.ai/03_plans/`. Coverage map:
- `.ai/00_system/` → Tasks 2 + 3 (architecture.md + pipeline-overview.md). `principles.md` and `naming-conventions.md` intentionally untouched — they are governance docs that still apply as written.
- `.ai/01_roadmap/` → Tasks 6 + 7 (master-roadmap.md + milestone-tracker.md). `current-phase.md` already updated in commit 37f0f62.
- `.ai/02_audits/` → Task 4 (all 5 files get SUPERSEDED banners).
- `.ai/10_state/` → Task 5 (known_issues.md). `active_context.md`, `decisions.md`, `current-phase.md` already updated in commit 37f0f62. JSON state files (`datasets.json`, `pipeline_state.json`, `system_state.json`) intentionally untouched — they are operational data, not docs.
- `.ai/03_plans/` archival → Task 1 (phase-8, phase-9, ultimate-architecture archived).

**2. Placeholder scan:** No "TBD", "add appropriate", "similar to", or bare "update X" instructions. Every task spells out the exact old and new text.

**3. Type consistency:** No code types to check — this is all docs. Cross-references between tasks (e.g., "see Task 1 for archival") are resolved.

**4. Parallelism map:** Wave A tasks are file-disjoint; none of them touch the same file. Task 1 is the only task that touches `.ai/03_plans/INDEX.md`, so it serializes naturally in Wave B. Task 9 is orchestrator-only and runs in Wave C.

**5. File paths verified:** All file paths were confirmed to exist via `ls` before writing the plan. Rust crate paths, TypeScript sibling path, and Python package paths are all consistent with the post-session tree.

---

## Execution Handoff

Plan complete and saved to `.ai/03_plans/2026-04-15-docs-cleanup-plan.md`. Two execution options:

**1. Subagent-Driven (recommended)** — I dispatch a fresh subagent per task in Waves A → B → C, review between waves, commit at end. Wave A runs six subagents in parallel.

**2. Inline Execution** — Execute tasks in this session using `superpowers:executing-plans`, batch execution with checkpoints for review. Slower but no subagent orchestration overhead.

Which approach?
