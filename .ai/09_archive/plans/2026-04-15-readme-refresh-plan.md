# README Refresh — Post-Sprint-HP.3-R Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Update `README.md` to accurately reflect the post-Sprint-HP.3-R state of Vitruvius (1396/1 tests, 10 sprints closed, Compound AI architecture) and add a verified-against-codebase **Compound AI System Definition** section.

**Architecture:** Single-file plan. README.md is a tourist map for the project; the authoritative docs live in `.ai/`. We update the README's stats, status table, module map, dependencies, and add the Compound AI section — all in one subagent dispatch with per-section specs that can be reviewed individually.

**Tech Stack:** Markdown (GitHub-flavored). No code changes. No test updates (this is a docs-only refresh). Verification is a read-back + rendering check.

---

## Why this plan exists

The user asked two things:

1. **Update the README** — the current `README.md` is stale. It reports 177 tests (reality: 1396), decision log AD-001 through AD-021 (reality: AD-001 through AD-029), Phase 8 gated (reality: ✅ subsumed by Sprint D Stream H + extended by Sprint GT), no mention of Rust crates or TypeScript sibling, no mention of RocksDB, no mention of the 10 sprints closed this session.

2. **Add a "Compound AI System Definition" section — *if it holds true*.** The user provided a 4-component framing (Semantic Extractor, Mathematical Verifier, Immutable Vault, Orchestrator). I verified each sub-claim against the codebase at plan-write time. **11 of 13 sub-claims hold; two do not.** See the verification ledger in §Pre-Task Evidence below. The plan adds the section with honest wording that removes the unsupported claims and tones down the overstated ones.

---

## Pre-Task Evidence (verified at plan-write time)

This is the ground truth the README update must respect. Any drift between these findings and the README copy is a spec violation.

### Evidence ledger

| Claim in the user's proposed definition | Evidence | Verdict |
|---|---|---|
| "Local LLM (e.g., Gemma 4)" | `scripts/vitruvius/ollama_review.py` + `config/vitruvius.yaml` default `gemma4:e4b` | ✅ true |
| "Strictly barred from making final compliance decisions" | Phase 7 `promotion_validator.py` has 17 deterministic rules; Sprint Z `z_neuro_symbolic` flag forces `<logic>` Datalog verification via `datalog_rs/` crate; BUT LLM still produces `keep`/`reject` verdicts that the validators check | ⚠️ partially true — reality is "subordinated to deterministic verifiers, not replaced by them" |
| "Translates messy input into Datalog / JSON IR" | Sprint Z S1 `ontology_prompt_builder.py` appends a `<logic-directive>` that forces `<logic>` Datalog output when `z_neuro_symbolic=true`; `compound/logic_schema.py` provides the Pydantic envelope | ✅ true (flag-gated, default false) |
| "Z3 Theorem Prover" | `geometric/inequality_compiler.py:85` `z3.Solver()` + `check() == z3.unsat`; `spatial/constraint_solver.py` is Stream L.5 Z3 SMT evaluator | ✅ true |
| "Rust/Wasm Spatial Kernels" | `scripts/vitruvius/engine_rs/` Cargo workspace (core + pyo3_shim); `engine_rs/core/src/wasm_api.rs` exports `aabb_intersects` as C-ABI; `compound/wasm_kernel.py` loads via `wasmtime` | ✅ true |
| "If the spatial engine returns `unsat`, the LLM's assumption is instantly destroyed" | `check_compliance` returns `ComplianceVerdict` with violations on UNSAT; Sprint Z S1 `datalog_rs` crate rejects Datalog derivations that don't parse/derive | ✅ true (flag-gated) |
| "Physical 3D B-Rep geometry" | `geometric/envelope_3d.py` uses `trimesh` + `manifold3d` (triangle/polyhedral mesh, not strict B-Rep) | ⚠️ **close but not strict B-Rep** — `trimesh` is a polyhedral/triangle representation. For CAD purists "B-Rep" implies bounded analytic surfaces (NURBS, b-spline). The README must not claim B-Rep — use "3D polyhedral mesh" instead |
| "RocksDB" | Just shipped Sprint HP.3-R (commit tag `sprint-hp3r-closed`); `scripts/vitruvius/graph/rocksdb_event_store.py` + `review/rocksdb_stateful_registry.py`; `rocksdict 0.3.29` Python binding | ✅ true |
| "FlatBuffers" | **ZERO hits in `scripts/` or any Python/Rust source.** Only mentioned in 8 archived research / plan files under `.ai/09_archive/research/` and `.ai/03_plans/` design specs. **Never shipped.** | ❌ **FALSE — must be removed from the README section** |
| "Event-Sourced Graph" | `graph/event_store.py::EventStore` + `rocksdb_event_store.py::RocksDBEventStore` (both append-only) | ✅ true |
| "Differential Dataflow to update graph dependencies in O(Δ) time" | `compound/differential_propagator.py::DifferentialPropagator.propagate(deltas)` walks `compound/dependency_tracker.py::DependencyTracker` per delta batch — O(Δ) in the changed set by construction | ✅ true |
| "Python Control Plane" | `scripts/pipeline_cli.py` + `scripts/vitruvius/` | ✅ true |
| "Numerical lock algorithms" | **No match for that phrase.** Real content-locking mechanisms: Merkle fs directory hash (Sprint HP.1, `scripts/vitruvius/merkle_fs.py`), SHA-256 file hash (RI-009 closed, `scripts/vitruvius/scanner.py::_sha256_of_file`), Z3 SAT admission check in `constraint_solver.py` | ⚠️ the CONCEPT holds but the user's phrasing is not a term used in the codebase. Rewrite to "Merkle directory hashes + SHA-256 file hashes + Z3 admission checks" |
| "Monte Carlo Dropout uncertainty thresholds before committing" | `graph/mc_dropout.py::compute_epistemic_uncertainty` exists as a utility. **Zero production call sites** — only imported from `scripts/tests/test_mc_dropout.py`. Not yet wired into an ingestion gate. | ⚠️ **utility ships; gate wiring is aspirational.** README must say "utility ships; ingestion-gate wiring is a follow-up" |

### Resulting honest section wording

The README section must use **this exact wording** (no drift allowed), derived from the evidence above:

```markdown
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
```

**Critical:** The subagent writing this section MUST copy the text block above verbatim. No rewording, no reordering, no "improving" the prose. The wording is the result of careful verification against the codebase and any drift re-introduces the claims the evidence rejected.

---

## File Structure

Single file:

| Path | Responsibility |
|---|---|
| `/Users/philiplewis/vitruvius/README.md` | Tourist-map-level README. Post-update: accurate stats, 10-sprint status table, refreshed module map, Compound AI section, updated dependencies. |

No other file is touched.

---

## Task 1: Full README refresh (single subagent)

**Rationale for a single-task plan:** The README changes are all in one file and are semantically interdependent (the quick stats, the status table, the Compound AI definition, and the module map must all agree on which sprints shipped). Splitting this into multiple subagent dispatches risks inconsistency and is overkill for a docs-only pass.

**Files:**
- Modify: `/Users/philiplewis/vitruvius/README.md`

### Subsection A — Stats in the opening paragraph

- [ ] **Step A1: Update the opening paragraph stats**

The current opening paragraph (lines 9-11) reads:

```markdown
the rule. On the active PD 1096 corpus, a full end-to-end run touches the
local LLM (Ollama / `gemma4:e4b`) roughly **4 times** — vs. ~25 in the
pre-deterministic-filter era.
```

This statement is still accurate — **do not touch it.** The ~4 calls per PD 1096 run is still the current AI budget.

### Subsection B — Add the Compound AI System Definition section

- [ ] **Step B1: Insert the Compound AI System Definition immediately after the opening blockquote ("the knowledge base lives in `.ai/`")**

Locate the blockquote at the top of the file (around lines 13-17):

```markdown
> **Looking for the deep docs?** The knowledge base lives in
> [`.ai/`](./.ai/). Start with
> [`.ai/01_roadmap/master-roadmap.md`](./.ai/01_roadmap/master-roadmap.md)
> for the authoritative phase contract. This README is the tourist map;
> `.ai/` is the terrain.

---
```

Immediately after the `---` separator that follows this blockquote, insert the entire **"## Vitruvius: Compound AI System Definition"** section from the Pre-Task Evidence block above (**copy it verbatim — do not reword**), followed by a new `---` separator.

The insertion lands BEFORE the existing "## Table of contents" section.

- [ ] **Step B2: Add a "Compound AI System" entry to the Table of Contents**

The current TOC starts at line ~21 with:

```markdown
## Table of contents

- [Quick start](#quick-start)
- [Architecture at a glance](#architecture-at-a-glance)
```

Insert a new first entry:

```markdown
## Table of contents

- [Compound AI System Definition](#vitruvius-compound-ai-system-definition)
- [Quick start](#quick-start)
- [Architecture at a glance](#architecture-at-a-glance)
```

### Subsection C — Refresh the Current Status table

- [ ] **Step C1: Replace the entire "## Current status" section body**

Locate the "## Current status" section (around line 406). Replace the opening line:

```markdown
As of 2026-04-14 (the authoritative status is `.ai/01_roadmap/master-roadmap.md` §4):
```

with:

```markdown
As of 2026-04-15 — after closing ten governing-plan sprints this session (Q, R, PHYS, H, GEOM, WIKI, GT, HP, Z, HP.3-R). The authoritative status is `.ai/01_roadmap/master-roadmap.md` §4, and the per-sprint ledgers live in `.ai/10_state/decisions.md` AD-024 through AD-029.
```

Then replace the **entire status table** (the one that currently ends with Phase 12 Gated) with:

```markdown
| Phase / Sprint | Status | Notes |
|---|---|---|
| 0. Foundation | ✅ Complete | — |
| 1A. Baseline Ingestion | ✅ Complete | SHA-256 file hashing closed RI-009; OCR parallelization tracked in Phase 1B §11 |
| 1B. Multi-Parser Integration | 🟡 Foundation shipped | Parsers subpackage + `FileEntry.sha256` + orchestrator skeleton; Modernization (Docling/Marker/Surya) pending |
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
```

Then replace the "Current AI usage on PD 1096 corpus" block (immediately after the table) with:

```markdown
**Current AI usage on PD 1096 corpus (unchanged by the Compound AI upgrades — the deterministic-first design predates them):**
- Tier-1 review calls: ~2 (pre-review filter handles the rest)
- Tier-2 review calls: ~1-2 (only uncertain Tier-1 output)
- Concept enrichment calls: 0 (fully deterministic)
- Sprint Z neuro-symbolic verification: 0 runtime cost (flag-off by default)
- **Total: ~4 Ollama calls per full pipeline run**

**Test suite as of 2026-04-15:** Python **1396 passed / 1 skipped**; TypeScript **20 passed** (`spatial-daemon/`); Rust unit tests **10 passed** (`engine_rs` + `datalog_rs`).
```

### Subsection D — Refresh the Testing section

- [ ] **Step D1: Update the test count in the "## Testing" section**

The current testing section (around line 320) says:

```markdown
**As of 2026-04-14: 177 tests passing**, 2 intentional deprecation warnings
from `utils.normalize_*` usage in their own test file.
```

Replace with:

```markdown
**As of 2026-04-15: 1396 Python tests passing, 1 skipped** — grew from 177 (pre-Sprint-D) via the Sprint D Streams A-I expansion and the subsequent 10 governing-plan sprints + the Sprint HP.3-R RocksDB KV migration. Also: **20 TypeScript tests passing** in the `spatial-daemon/` sibling subproject (vitest), and **10 Rust unit tests** across `scripts/vitruvius/engine_rs/core` and `scripts/vitruvius/datalog_rs/`.
```

### Subsection E — Refresh the Dependencies section

- [ ] **Step E1: Expand the "## Dependencies" section**

The current section lists PyYAML/pytest + pypdf/opendataloader/ocrmypdf/openpyxl/pandas + Ollama. Replace the entire section body (between `## Dependencies` and `---`) with:

```markdown
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
- `docling` — structured PDF parser (Sprint WIKI)
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
```

### Subsection F — Refresh the Module Map

- [ ] **Step F1: Append new subpackages to the "## Module map" section**

The current module map lists modules through Phase 7 (promotion). The session's 10 sprints added 6 new Python subpackages + 2 Rust crates + 1 TypeScript sibling. Append a new subsection AT THE END of the `## Module map` section, immediately before the `## Testing` section header:

```markdown
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

### Rust data plane

- `scripts/vitruvius/engine_rs/` — Cargo workspace (Sprint GT.1 + HP.4)
  - `core/` — pure Rust; compiles for native + `wasm32-unknown-unknown`; exports `SpatialPoint`, `LinearOctree`, and the Wasm `aabb_intersects` C-ABI function
  - `pyo3_shim/` — pyo3 bindings consumed by `scripts/vitruvius/compound/wasm_kernel.py` and the spatial modules
- `scripts/vitruvius/datalog_rs/` — pyo3 crate shipping a hand-rolled Datalog evaluator for Sprint Z Stream S1.2. Entry point: `evaluate_datalog(facts, rules)`. 7 Rust unit tests.

### TypeScript sibling subproject

- `spatial-daemon/` — Node.js 25 + vitest subproject at repo root (not inside `scripts/vitruvius/`). Implements GJK collision detection, AABB overlap, and a filesystem contract writer that the Python side consumes. Entry point: `spatial-daemon/src/cli.ts`. 20/20 vitest tests.
```

### Subsection G — Refresh the `.ai/` knowledge base reference

- [ ] **Step G1: Update the archive row in the `.ai/` knowledge base table**

Find the row in the `.ai/` table that reads:

```markdown
| [`.ai/09_archive/`](./.ai/09_archive/) | **Completed plans** (Phase 7, 1C, 2, 6A, 6B, 3C, polish) |
```

Replace with:

```markdown
| [`.ai/09_archive/`](./.ai/09_archive/) | **Completed plans** — Phases 7/1C/2/6A/6B/3C/polish plus the 10 sprints closed this session: Q (live wiring), R (per-layer embeddings + agentic), PHYS (graph physics), H (3D spatial), GEOM (constraint engine), WIKI (synthesis), GT (geo-topological), HP (performance), Z (compound AI), HP.3-R (RocksDB KV migration). Also: research briefs under `.ai/09_archive/research/`. |
```

- [ ] **Step G2: Update the decision log reference at the bottom of the `.ai/` section**

Find and replace:

```markdown
**If you're looking for "why"**: `.ai/10_state/decisions.md` has the complete
architectural decision log (AD-001 through AD-021 as of 2026-04-14).
```

with:

```markdown
**If you're looking for "why"**: `.ai/10_state/decisions.md` has the complete
architectural decision log (AD-001 through AD-029 as of 2026-04-15). AD-024 through AD-029 cover the Sprint Q→Z→HP.3-R closure arc and the RocksDB migration bench ledger.
```

### Subsection H — Replace the Sprint Q dedicated section

- [ ] **Step H1: Replace the "Sprint Q — Live Wiring & 8GB Hardening" dedicated section**

The current README has a dedicated "## Sprint Q — Live Wiring & 8GB Hardening" section (around lines 365-404) with a YAML flag config example. Sprint Q is now one of ten closed sprints; singling it out in its own section is stale.

Replace the entire section (from `## Sprint Q — Live Wiring & 8GB Hardening` down to just before `## Current status`) with:

```markdown
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
```

### Step I — Verify the edits

- [ ] **Step I1: Read the updated file and count sections**

```bash
cd /Users/philiplewis/vitruvius && grep -c '^## ' README.md
```

Expected: the section count grew by 1 (the new "Compound AI System Definition" section) and Sprint Q was replaced in place (so net +1 vs baseline).

- [ ] **Step I2: Verify no placeholder strings leaked through**

```bash
cd /Users/philiplewis/vitruvius && grep -n 'TBD\|<this commit>\|FIXME\|XXX\|TODO:' README.md
```

Expected: empty output. If any hits, that's a drift from the spec.

- [ ] **Step I3: Verify the banned terms are absent**

```bash
cd /Users/philiplewis/vitruvius && grep -n 'FlatBuffer\|flatbuffer\|B-Rep\|BRep\|numerical lock' README.md
```

Expected: empty output. FlatBuffers was removed from the Compound AI claims, "B-Rep" was replaced with "3D polyhedral mesh", and "numerical lock algorithms" was replaced with specific named mechanisms.

- [ ] **Step I4: Verify the required terms are present**

```bash
cd /Users/philiplewis/vitruvius && grep -c 'Compound AI\|rocksdict\|engine_rs\|datalog_rs\|spatial-daemon\|1396' README.md
```

Expected: ≥6 total hits (each term at least once).

- [ ] **Step I5: Render-check the markdown**

```bash
cd /Users/philiplewis/vitruvius && /opt/homebrew/opt/python@3.11/bin/python3.11 -c "
import re
with open('README.md') as f:
    content = f.read()
# Check for unclosed code fences
fence_count = content.count('\`\`\`')
assert fence_count % 2 == 0, f'unclosed code fence: {fence_count} markers'
# Check for unclosed tables (every table row starts with |)
lines = content.split('\n')
in_table = False
table_col_count = 0
for i, line in enumerate(lines, 1):
    stripped = line.strip()
    if stripped.startswith('|') and stripped.endswith('|'):
        if not in_table:
            table_col_count = stripped.count('|') - 1
            in_table = True
    elif in_table and stripped:
        in_table = False
print('markdown structural checks passed')
"
```

Expected: `markdown structural checks passed` with no assertion errors.

### Step J — Commit

- [ ] **Step J1: Stage and commit**

```bash
cd /Users/philiplewis/vitruvius && git add README.md
```

Verify:

```bash
cd /Users/philiplewis/vitruvius && git diff --cached --stat
```

Expected: 1 file changed, ~200-400 lines changed (mostly additions).

Commit:

```bash
cd /Users/philiplewis/vitruvius && git commit -m "$(cat <<'EOF'
docs(readme): refresh post-Sprint-HP.3-R + Compound AI System Definition

Updates README.md to reflect the 2026-04-15 state of the project
after closing 10 governing-plan sprints (Q, R, PHYS, H, GEOM, WIKI,
GT, HP, Z, HP.3-R):

- Adds a "Vitruvius: Compound AI System Definition" section at the
  top of the README. The section was requested by the user with a
  proposed 4-component framing; every sub-claim was verified
  against the codebase at plan-write time. Two claims were removed
  (FlatBuffers — not shipped; "B-Rep" — we use trimesh polyhedral
  meshes) and two were softened (LLM "subordinated to" rather than
  "strictly barred from" deterministic verifiers; "numerical lock
  algorithms" replaced with Merkle + SHA-256 + Z3 admission
  checks). MC Dropout is described as a shipped utility with
  aspirational ingestion-gate wiring.
- Refreshes the Current Status table to cover all 10 closed
  sprints plus Phase 8/9 subsumption.
- Updates the test count from 177 → 1396 (Python) + 20 (TypeScript)
  + 10 (Rust), and the decision log reference from AD-021 → AD-029.
- Adds Rust data plane (engine_rs + datalog_rs) and TypeScript
  sibling (spatial-daemon) to the Module Map and Dependencies
  sections.
- Replaces the dedicated "Sprint Q" section with a generalised
  "Feature-flag operation" section showing the full flag config
  for the Compound AI stack.
- Adds the Compound AI Definition to the Table of Contents.

No code changes. Authoritative state remains in
.ai/01_roadmap/master-roadmap.md and .ai/10_state/decisions.md
(AD-001 through AD-029).

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
EOF
)"
```

- [ ] **Step J2: Verify commit landed**

```bash
cd /Users/philiplewis/vitruvius && git log --oneline -1
```

Expected: the new SHA with the Task 1 subject line.

---

## Self-Review Checklist

**1. Spec coverage**
- ✅ Compound AI System Definition — added as Subsection B, with verified wording
- ✅ Test count refresh — Subsection D
- ✅ Decision log range refresh — Subsection G Step G2
- ✅ Current status table with all 10 sprints — Subsection C
- ✅ Module map with new subpackages — Subsection F
- ✅ Dependencies with rocksdict + Rust + TypeScript — Subsection E
- ✅ `.ai/` knowledge base archive note refresh — Subsection G Step G1
- ✅ Sprint Q section replaced with generalised feature-flag operation — Subsection H

**2. Placeholder scan**
- No "TBD", no "implement later", no "similar to".
- The only verbatim-copy directive is the Compound AI wording block in the Pre-Task Evidence section, which is presented in full inside this plan (no "fill in later").

**3. Type / term consistency**
- "Compound AI System" (not "Compound AI Platform" or similar) — used consistently.
- "1396 passed, 1 skipped" — stated consistently across the test-count updates.
- "rocksdict 0.3.29" — pinned consistently.
- "AD-029" — referenced consistently for the RocksDB bench decision; AD-028 for the 9-sprint closure.
- FlatBuffers absent from all sections (no leak from old drafts).
- "B-Rep" absent; "3D polyhedral mesh" used consistently.

**4. Honesty check vs the evidence ledger**
- LLM "subordinated to" NOT "strictly barred" — ✅ used in the spec block
- FlatBuffers removed — ✅ absent from the spec block
- "3D polyhedral mesh" instead of "B-Rep" — ✅ used
- "Merkle + SHA-256 + Z3 admission checks" instead of "numerical lock algorithms" — ✅ used
- MC Dropout marked as "utility ships; gate wiring is follow-up" — ✅ used
- All four components correctly cite shipped file paths — ✅

---

## Execution Handoff

Plan complete and saved to `.ai/03_plans/2026-04-15-readme-refresh-plan.md`. Two execution options:

**1. Subagent-Driven (recommended)** — I dispatch a fresh subagent with the full task text, two-stage review after (spec compliance first, then code quality / rendering check), commit lands inside the subagent's turn.

**2. Inline Execution** — I make all the edits directly in this session and commit. Faster, but skips the review gate that caught the `<this commit>` placeholder and `flush()` parity bug in the RocksDB migration plan.

Which approach?
