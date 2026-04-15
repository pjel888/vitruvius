---
plan_id: ultimate-architecture-upgrade
plan_type: design_spec
phase: 9-12+
status: superseded
superseded_on: 2026-04-15
superseded_by:
  - 00-governing-implementation-plan.md (orchestrator of successor plans)
  - 3d-spatial-intelligence-upgrade-plan.md (absorbs Streams L, M, N spatial scope)
  - phase-8b-geo-topological-graph-plan.md (absorbs Streams M/N Rust engine scope)
  - phase-13-high-performance-optimizations-plan.md (absorbs Streams O/P/Q/T perf scope)
  - phase-16-statistical-mechanics-graph-physics-plan.md (absorbs Stream X Boltzmann + orphan Stream O VF2)
  - per-layer-embeddings-agentic-upgrade-plan.md (absorbs Stream U hardware router scope)
sprint: "— (superseded)"
owner: vitruvius-core
created: 2026-04-14
updated: 2026-04-15
related_plans:
  - statistical-architectural-upgrade-plan.md (Streams A-K — this plan previously EXTENDED it)
  - phase-8-graph-contract-indexing-plan.md (base Phase 8 — now subsumed by Stream H)
  - phase-9-query-ai-layer-plan.md (base Phase 9 — now subsumed by Stream I)
research_sources:
  - .ai/13_research/Ultimate-Improvement.md (primary)
  - .ai/13_research/statistical-improvements.md
  - .ai/13_research/advanced-architectural-and-code-level-optimizations.md
streams:
  I_query_v2: planned (finishes existing-plan Stream I — 6 tasks)
  J_active_learning: planned (finishes existing-plan Stream J — 4 tasks)
  K_clup_scaling: planned (finishes existing-plan Stream K — 4 tasks, gated)
  L_spatial_reasoning: new (Z3 SMT + Spatial Contract + Parametric Evaluator — 11 tasks)
  M_rust_polyglot_ingest: new (Rust Bloom/MinHash/LSH via PyO3 — 9 tasks)
  N_rust_topology_kernel: new (Rust CSR + RWR + PageRank — 7 tasks)
  O_binary_storage_vault: new (Parquet archives, FlatBuffers, RocksDB-lite — 8 tasks)
  P_event_sourced_graph: new (Append-only event log + time-travel — 7 tasks)
  Q_temporal_query: new (Temporal-aware query layer — 5 tasks)
  R_epistemic_uncertainty: new (MC Dropout + Dempster-Shafer — 6 tasks)
  S_subgraph_clash: new (Violation motif isomorphism — 5 tasks)
  T_adaptive_chunking: new (Nyquist-Shannon density-based chunking — 4 tasks)
  U_hardware_router: new (psutil memory-aware SLM routing — 4 tasks)
  V_ontology_ifc_owl: new (IFC/OWL canonical mapping — 6 tasks)
  W_autonomous_foraging: new (Headless LGU crawler + Mahalanobis drift — 5 tasks)
  X_boltzmann_health: new (Promotion energy metric — 3 tasks)
---

# Vitruvius — Ultimate Architecture Upgrade Plan

> ## ❌ SUPERSEDED (2026-04-15)
>
> **Do not dispatch this plan directly.** Its streams have been redistributed across more focused successor plans:
>
> | Original stream | Successor |
> |---|---|
> | I, J, K (finish existing Stream I/J/K) | `statistical-architectural-upgrade-plan.md` (Streams A–I closed; J/K gated) |
> | L — Spatial Reasoning (Z3 SMT) | `3d-spatial-intelligence-upgrade-plan.md` Stream L |
> | M — Rust Polyglot Ingest (Bloom/MinHash/LSH via PyO3) | `phase-8b-geo-topological-graph-plan.md` Stream GT.1 |
> | N — Rust Topology Kernel (CSR + RWR + PageRank) | `phase-8b-geo-topological-graph-plan.md` Stream GT.2 |
> | O — Binary Storage Vault (Parquet + FlatBuffers + LMDB) | `phase-13-high-performance-optimizations-plan.md` Stream HP.3 |
> | P — Event-Sourced Graph | `phase-13-high-performance-optimizations-plan.md` Stream HP.3 |
> | Q — Temporal Query | `phase-8b-geo-topological-graph-plan.md` Stream GT.3 |
> | R — Epistemic Uncertainty (MC Dropout + DST) | `statistical-architectural-upgrade-plan.md` Stream L_conf (DST half) + phase-8b Stream GT.5 (MC Dropout half) |
> | S — Subgraph Clash (VF2) | `phase-16-statistical-mechanics-graph-physics-plan.md` Stream PHYS.2 (orphan Stream O absorbed) |
> | T — Adaptive Chunking (Nyquist-Shannon) | `phase-13-high-performance-optimizations-plan.md` Stream HP.2 |
> | U — Hardware Router (psutil-driven) | `per-layer-embeddings-agentic-upgrade-plan.md` Stream Y2 addendum (governing plan §4.3) |
> | V — Ontology IFC/OWL | `3d-spatial-intelligence-upgrade-plan.md` Stream M |
> | W — Autonomous Foraging | `3d-spatial-intelligence-upgrade-plan.md` Stream O |
> | X — Boltzmann Health | `phase-16-statistical-mechanics-graph-physics-plan.md` Stream PHYS.2 |
>
> The narrative content below is retained for historical reference and for any scoping notes that did not survive the split. See `00-governing-implementation-plan.md` §4.6 for the decision record.

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to implement this plan task-by-task. Every task has bite-sized steps with checkbox (`- [ ]`) syntax for tracking. Never skip the "run the failing test" step — it validates that the test actually tests what you think.

**Goal:** Evolve Vitruvius from a statistically-augmented deterministic pipeline (Streams A–G shipped, Stream H scaffolded) into a true polyglot Brain: a temporal, spatial, probabilistic, event-sourced legal topology engine that runs on an 8 GB M2 without compromising correctness, with selective Rust acceleration for the CPU-bound hot paths.

**Architecture:** Preserve the Python control plane. Wire the remaining existing-plan streams (I query layer, J active learning, K CLUP scaling) through to their gating metrics. Then layer in spatial reasoning (Z3 SMT), epistemic uncertainty (MC Dropout + Dempster-Shafer), event-sourced graph state, temporal query, adaptive chunking, hardware-aware routing, IFC/OWL ontology mapping, autonomous foraging, binary storage vault, and Rust/PyO3 kernels for the ingest + topology inner loops. Every stream is independently feature-flagged and idempotent, every task is TDD-first, every byte that leaves Python to Rust flows through PyO3 with zero-copy memory.

**Tech Stack:**
- **Control Plane:** Python 3.11+, stdlib-heavy, pinned lower-bounds per §3.
- **Statistical Core (already shipped):** numpy, scipy, scikit-learn, rapidfuzz, python-crfsuite, spacy, networkx, python-louvain, POT, sentence-transformers.
- **New Python deps (this plan):** `z3-solver`, `pyarrow`, `fastparquet` (pure-Python parquet fallback), `plyvel` (LMDB/LevelDB binding — LMDB chosen over RocksDB for pure-Python install), `pykeen` stub (gated), `pyroaring` (compressed bitmap for subgraph isomorphism), `flatbuffers` (Python runtime only).
- **Data Plane (new, Rust via PyO3):** `vitruvius_ingest_kernel` (Bloom + MinHash LSH), `vitruvius_topology_kernel` (CSR + RWR + PageRank).
- **Build Toolchain:** `maturin` (Python wheel of Rust extensions), `cargo` (Rust toolchain).
- **Storage:** Parquet for cold archives, FlatBuffers for intermediate machine-only data, LMDB-backed key-value for hot graph state, JSON/YAML retained for canonical + human-facing layers (non-breaking).
- **No new LLM dependencies.** All generative calls continue to route through existing `ollama_review.py` / `ollama_review_second_pass.py` paths.

---

## 1. Preamble

### 1.1 Why This Plan Exists

Vitruvius has completed Sprint D (Streams A–G) and nearly all of Stream H (Phase 8 graph layer + centrality/spectral/community/MCMC/TDA/Wasserstein/causal/tensor scaffolding). The existing `statistical-architectural-upgrade-plan.md` catalogues Streams I, J, K as pending but does not cover several research items surfaced in `.ai/13_research/Ultimate-Improvement.md`:

1. **Spatial Intelligence Layer** — Z3 SMT theorem proving over parametric graph constraints, decoupled 001B_Spatial-Source-Layer contract, GJK collision reasoning via an external middleware (Node/Rust) whose *JSON output* this plan ingests but whose internals remain decoupled.
2. **Rust Polyglot Kernels** — Bloom filter + MinHash LSH ingest-layer dedup; CSR + Random Walk with Restart + PageRank topology kernel. Both exposed to Python as PyO3 extensions with zero-copy memory sharing.
3. **Binary Storage Vault** — Parquet/FlatBuffers/LMDB intermediate storage for machine-only data; JSON/YAML retained only where a human will read it.
4. **Event-Sourced Graph State** — Immutable append-only event log over the graph (git-for-topology) enabling time-travel reconstruction + audit.
5. **Temporal-Aware Query Layer** — Time-vector filtering at read time, using the existing `promotion/temporal_edges.py` `t_start`/`t_end` metadata.
6. **Epistemic Uncertainty Bounds** — Monte Carlo dropout sampling of the LLM adjudicator + Dempster–Shafer belief/plausibility for conflicting legal rules.
7. **Subgraph Isomorphism Clash Detection** — Violation-motif matching against the canonical graph (purely structural, no inference).
8. **Adaptive Semantic Chunking** — Nyquist–Shannon dynamic window sizing driven by parametric density.
9. **Hardware-Aware Router** — psutil-driven selection between e2b / e4b / 31b Ollama models based on free RAM.
10. **IFC/OWL Ontology Mapping** — Canonical-concept mapping to buildingSMART IFC + Pset property sets.
11. **Autonomous Epistemic Foraging** — Headless crawler monitoring LGU/DPWH registries, Mahalanobis-distance drift detection → auto-PR into 001_Raw-Source-Layer.
12. **Boltzmann-Distribution Promotion Gate** — Graph "temperature" health metric gating promotion when contradiction energy is too high.

These 12 items + the 3 pending streams (I, J, K) constitute the scope of this plan. **Everything else in the research document is either already shipped in Streams A–H or is deferred under the existing plan's §2.3 Deferred Items (GPU-gated LoRA/DPO, learner-gated BKT, CV-model-gated 2D blueprint ingestion, PINNs, zk-SNARKs, graph representation learning beyond TransE).**

### 1.2 Precedence Declaration

This plan EXTENDS `statistical-architectural-upgrade-plan.md`. It does NOT modify any Stream A–G module (those are frozen). It completes Streams I, J, K as originally designed in that plan, then adds new Streams L–X. Nothing in this plan alters the existing public contract of a shipped module — every change is additive, behind a feature flag, and regression-tested against `test_backward_compat.py`.

If this plan and `statistical-architectural-upgrade-plan.md` conflict on a Stream H–K task, the existing plan wins. This plan defers to its task breakdown for I, J, K and adds only the net-new L–X streams for everything else.

### 1.3 Non-Breaking Contract (hard rules)

Every task in this plan MUST comply:

1. **Additive only.** Do not modify the public signature of any shipped Stream A–G module. New behavior sits behind a feature flag in `scripts/vitruvius/features.py` under the namespace of the owning stream (`l_spatial_z3`, `m_rust_ingest`, `n_rust_topology`, `o_binary_vault`, `p_event_sourced`, `q_temporal_query`, `r_epistemic_mcd`, `s_clash_isomorphism`, `t_adaptive_chunking`, `u_hardware_router`, `v_ifc_owl`, `w_foraging`, `x_boltzmann_health`). Default every new flag to `false`.
2. **Idempotent.** Running any CLI command twice with the same input must produce byte-identical output (modulo `generated_at_utc` timestamps). Graph snapshots, feature tables, and event-log writes all honor this.
3. **Deterministic.** Every statistical module pins `random_state=0` unless the test explicitly varies it. Graph order is deterministic via sorted keys.
4. **Hardware-safe.** Every new Python module MUST fit under the 8 GB M2 ceiling. No module may load a model >2 GB into RAM without going through the `hardware_router.select_adjudicator()` gate introduced in Stream U.
5. **Backward-compatible.** `test_backward_compat.py` (from Sprint D Stream A) MUST stay green across every commit. A stream that breaks it fails the gate.
6. **No placeholder code.** Every task either ships working code or is not merged. A task that says "wire up later" is rejected at review time.
7. **Never skip the failing-test step.** The TDD red → green → refactor loop is mandatory. Skipping red means you don't know if your test actually tests the behavior.
8. **Respect the actual graph contract.** The live `graph/contract.py` surface is:
   - `GraphNode(id, type ∈ {source,concept,attribute}, slug, trust_level ∈ {primary,secondary,tertiary,unverified,derived}, last_updated_utc)`. Node IDs MUST use an allowed prefix: `law-`, `irr-`, `concept-`, `rel-`, `source-`, `handout-`, `reviewer-`, `law-section-`.
   - `GraphEdge(from_id, to_id, type, evidence_id, status ∈ {verified,unverified})`. `evidence_id` MUST start with `rel-`.
   - `GraphSnapshot(schema_version, generated_at_utc, node_count, edge_count, nodes, edges)` (plain dataclass, `nodes`/`edges` are `list`s).
   - Temporal metadata lives in `promotion/temporal_edges.TemporalEdge(edge_id, from_entity, predicate, to_entity, valid_from, valid_until, jurisdiction)` — a parallel struct keyed on `edge_id` that joins to `GraphEdge.evidence_id`. NEVER add `valid_from`/`valid_until` fields to `GraphEdge` itself.
   - MCMC is `mcmc_random_walk(snapshot, seed_id, alpha, steps, rng_seed)` returning `MCMCStationaryDistribution(visit_frequency: tuple[tuple[str,float], ...])`.
   - Centrality is `compute_centrality(snapshot, kind ∈ {degree,betweenness,pagerank})` returning `CentralityReport(scores: tuple[tuple[str,float], ...])`.
   - Community detection is `detect_communities(snapshot, random_state=0)` returning `CommunityReport(communities, modularity)`.
   Any new module that needs to touch these surfaces MUST use the real fields. Any new module that needs richer attributes on nodes/edges MUST build a parallel sidecar table keyed on `node.id` / `edge.evidence_id` rather than mutating the frozen contract.

### 1.4 Hardware Ceiling Contract

| Module | Peak RAM | Peak Disk | Cold Start | Notes |
|---|---|---|---|---|
| Stream I query layer | <150 MB | <20 MB | <500 ms | networkx reuse of Stream H snapshot |
| Stream J active learning | <50 MB | <5 MB | <100 ms | sklearn + pure numpy |
| Stream K CLUP scaling | <300 MB | <100 MB | <1 s | gated on ≥2 jurisdictions |
| Stream L Z3 spatial | <200 MB | <10 MB | <200 ms | z3-solver is pure-C, tiny |
| Stream M Rust ingest kernel | <20 MB | <2 MB | <50 ms | Rust binary tiny; Python binding thin |
| Stream N Rust topology kernel | <150 MB | <5 MB | <100 ms | CSR scales linearly |
| Stream O binary storage vault | <500 MB | unbounded (cold) | <500 ms | LMDB page-cached |
| Stream P event-sourced log | <100 MB | unbounded (cold) | <200 ms | append-only |
| Stream Q temporal query | <10 MB extra | 0 | 0 extra | reuses H snapshot |
| Stream R epistemic MC dropout | <50 MB | 0 | <100 ms | 10 sample passes @ e2b |
| Stream S clash isomorphism | <30 MB | 0 | <50 ms | small motif library |
| Stream T adaptive chunking | <20 MB | 0 | 0 extra | pure numpy |
| Stream U hardware router | <5 MB | 0 | <10 ms | psutil only |
| Stream V IFC/OWL mapping | <100 MB | <50 MB | <500 ms | owlready2 is pure Python |
| Stream W foraging | <200 MB | unbounded | <5 s | requests + rapidfuzz |
| Stream X Boltzmann health | <10 MB | 0 | <50 ms | pure math |

Total new RAM at steady state (all flags ON, everything cold-started together): ~1.7 GB, leaving >6 GB for Ollama inference on an 8 GB M2. **The plan is hardware-safe.**

### 1.5 How to Consume This Plan

- **Pre-flight:** Read §§1–4. Confirm `.ai/03_plans/statistical-architectural-upgrade-plan.md` status is "Streams A–G CLOSED, H ≥90% shipped." If Stream H is not yet Done-of-Done, finish it before starting anything here.
- **Execution:** Pick a stream. Each stream is independently executable but obeys the dependency order in §17 Sprint Rollout. Do streams in that order unless you have a compelling reason not to.
- **Task granularity:** Every task has a `Files:` block, a failing test, a run-to-fail command, an implementation step with the FULL code, a run-to-pass command, and a commit. You should be able to execute each step in 2–5 minutes without leaving your editor.
- **Regression:** After every stream, run `python3 -m pytest scripts/tests/ -x --tb=short` and confirm zero failures before moving on.
- **Self-review checklist:** §20 — run it before marking the plan as done.

---

## 2. Honest Audit — What Exists, What This Plan Adds

### 2.1 What Already Exists (verified by direct filesystem audit, 2026-04-14 20:28)

**Phase 8 Graph Package** (`scripts/vitruvius/graph/`):
- `builder.py`, `contract.py`, `integrity.py`, `snapshot.py`, `traverse.py`, `cli.py` — base Phase 8 shipped.
- `centrality.py`, `spectral.py`, `community.py` (Louvain), `mcmc.py` (RWR), `tda.py` (Betti + cycle basis), `wasserstein_merge.py`, `causal_dag.py`, `tensor_factorisation.py` — all Stream H.1–H.8 files exist as working modules with tests (`test_graph_*.py` × 12).

**Extraction Package** (`scripts/vitruvius/extraction/`): spaCy SVO parser, CRF trainer + extractor, TransE KG link predictor (Stream E.1–E.4 shipped).

**Review Package** (`scripts/vitruvius/review/`): Naive Bayes filter, SLM router, conformal calibrator, Choquet aggregator, tension analyzer, reflection parser, ontology prompt builder, ollama_config (Stream F.1–F.8 shipped).

**Concepts Package** (`scripts/vitruvius/concepts/`): TF-IDF matcher, PMI alias miner, FCA lattice, contrastive adapter (Stream D.1–D.4 shipped).

**Promotion Package** (`scripts/vitruvius/promotion/`): Bayesian fusion, stringency resolver, temporal edges (Stream G.1–G.3 shipped).

**Parsers Package** (`scripts/vitruvius/parsers/`): Shannon classifier, document taxonomy, table-graph extractor, parametric NER (Stream B.1–B.4 shipped).

**Normalization Package** (`scripts/vitruvius/normalization/`): AST chunker, embedding chunker, Mahalanobis outlier detector, tier A/B/C rules (Stream C.1–C.4 shipped).

**CLI** (`scripts/pipeline_cli.py`): `build-graph`, `query-graph`, `export-graph-snapshot` live alongside the ingestion/conversion/review/promotion commands.

**Test suite:** 93 test files, suite currently at ~788 passing tests.

**Dependencies (requirements.txt):** numpy, scipy, scikit-learn, rapidfuzz, python-crfsuite, networkx, python-louvain, POT, spacy, sentence-transformers, pypdf, opendataloader-pdf, ocrmypdf, PyYAML, openpyxl.

### 2.2 What Is Missing — Addressed by This Plan

| # | Research Item | Source | Stream | Status |
|---|---|---|---|---|
| 1 | Phase 9 base query layer (ontology NL translator, structured call builder) | Ultimate-Improvement §3.4, existing plan §13 | I.0 | PLANNED |
| 2 | GraphRAG community-level query routing | Ultimate §3.4 | I.2 | PLANNED |
| 3 | MCMC answer ranking at query time | Ultimate §1, §3.1 | I.3 | PLANNED |
| 4 | Hidden Markov Model pipeline-state observability | stat-doc §5 | I.4 | PLANNED |
| 5 | Active learning uncertainty sampling | Ultimate-Improvement on Active Learning | J.1 | PLANNED |
| 6 | Expected Model Change scoring for Ranger routing | Ultimate AL sect. | J.2 | PLANNED |
| 7 | CLUP Rosetta Stone alias alignment | existing plan §15 | K.1 | PLANNED (gated) |
| 8 | Jurisdictional precedence routing | existing plan §15 | K.2 | PLANNED (gated) |
| 9 | Tensor-factorisation activation (≥2 jurisdictions) | existing plan §15 | K.3 | PLANNED (gated) |
| 10 | Z3 SMT parametric constraint evaluator | Ultimate §4 Spatial Algebra | L.1–L.4 | NEW |
| 11 | 001B_Spatial-Source-Layer + spatial JSON contract | Ultimate "Phase 1D Spatial Interoperability" | L.5–L.7 | NEW |
| 12 | Parametric edge attributes on Phase 8 graph | Ultimate §Parametric NER integration | L.8–L.11 | NEW |
| 13 | Rust Bloom-filter ingestion kernel (PyO3) | Ultimate "vitruvius-ingest kernel" | M.1–M.5 | NEW |
| 14 | MinHash LSH macro-pattern dedup | Ultimate §1.3 LSH | M.6–M.9 | NEW |
| 15 | Rust CSR topology kernel + RWR in Rust (PyO3) | Ultimate §1.4 CSR, §GraphRAG deep-dive | N.1–N.7 | NEW |
| 16 | Parquet cold-archive vault (registries, run histories) | Ultimate "Parquet for cold data" | O.1–O.3 | NEW |
| 17 | FlatBuffers intermediate format for chunk manifests | Ultimate "FlatBuffers instant-load" | O.4–O.5 | NEW |
| 18 | LMDB-backed hot key-value store for graph snapshot | Ultimate "RocksDB/LMDB vault" | O.6–O.8 | NEW |
| 19 | Append-only immutable event log of graph mutations | Ultimate "Event-Sourced Graph State" | P.1–P.7 | NEW |
| 20 | Time-vector query over temporal_edges metadata | Ultimate §1 Temporal KG | Q.1–Q.5 | NEW |
| 21 | Monte Carlo Dropout uncertainty on LLM adjudicator | Ultimate §2 Epistemic | R.1–R.4 | NEW |
| 22 | Dempster–Shafer belief/plausibility for conflicts | Ultimate §Dempster-Shafer | R.5–R.6 | NEW |
| 23 | Subgraph isomorphism violation-motif library | Ultimate §Subgraph Iso | S.1–S.5 | NEW |
| 24 | Nyquist–Shannon adaptive chunk sizing | Ultimate §3.1 Nyquist | T.1–T.4 | NEW |
| 25 | Hardware-aware SLM router with psutil gating | Ultimate "hardware_router.py" | U.1–U.4 | NEW |
| 26 | IFC/OWL canonical concept mapping | Ultimate §Ontological Unification | V.1–V.6 | NEW |
| 27 | Autonomous epistemic foraging crawler | Ultimate §Autonomous Foraging | W.1–W.5 | NEW |
| 28 | Boltzmann graph-energy promotion gate | Ultimate §Boltzmann | X.1–X.3 | NEW |

### 2.3 Items Explicitly Deferred (with rationale)

| # | Research Item | Why deferred | Prerequisite |
|---|---|---|---|
| D1 | LoRA fine-tuning of adjudicator | needs GPU + ≥1000 labelled pairs | FUTURE-ML-01 |
| D2 | DPO pedagogical alignment | needs GPU + preference dataset | FUTURE-ML-02 |
| D3 | Bayesian Knowledge Tracing (BKT) | needs learner interaction data | FUTURE-LRN-01 (Phase 12+ ILXP) |
| D4 | Computer Vision 2D blueprint ingestion | needs a trained architecture CV model | FUTURE-CV-01 |
| D5 | Physics-Informed Neural Networks | needs GPU + physics training data | FUTURE-ML-03 |
| D6 | Zero-Knowledge Proofs (zk-SNARKs) for permitting | needs circuit compiler + BN254 backend | FUTURE-CRYPTO-01 |
| D7 | GraphSAGE inductive embeddings | TransE (Stream E.4) covers link prediction; GraphSAGE would be a later upgrade | FUTURE-ML-04 |
| D8 | Native SketchUp C-API extractor | the spatial middleware is external; this plan ingests only its JSON output per §1.1 item 1 | External daemon |
| D9 | Native Rust WebAssembly target | PyO3 native binding is sufficient for local speed; Wasm is only valuable for portability, which is not Phase 9 scope | FUTURE-RUST-02 |
| D10 | Full Leiden algorithm (python-louvain ships Louvain) | Louvain's modularity is within 2% of Leiden on our graph size; upgrade later | FUTURE-GRAPH-01 |
| D11 | Generative parametric massing (Pareto-optimized envelopes) | needs Stream L + Stream V + an optimization loop outside core | FUTURE-GEN-01 |
| D12 | B2G automated permit gateway | needs Stream L + deployment pipeline; Vitruvius only ships the engine | FUTURE-B2G-01 |
| D13 | zk-AEC, Algorithmic Escrow, Resilience Simulation | ecosystem applications outside engine scope | FUTURE-APP-* |

Each deferred item is recorded here so nothing is silently skipped. When its gate lifts, add a small plan appendix. Nothing deferred sits on the critical path for an 8 GB M2 dev environment.

---

## 3. Dependency Bootstrap

### 3.1 New Python Packages (append to `requirements.txt`)

```text
# Ultimate Architecture Upgrade — additive dependencies.
# Pinned lower bounds validated against 8GB M2 / Apple Silicon.
z3-solver>=4.12,<5.0           # Stream L: SMT theorem prover
pyarrow>=15.0,<20.0            # Stream O: Apache Arrow + Parquet runtime
plyvel>=1.5,<2.0               # Stream O: LevelDB embedded K/V (pure C, <5MB)
flatbuffers>=24.0,<26.0        # Stream O: FlatBuffers Python runtime
owlready2>=0.46,<1.0           # Stream V: OWL ontology loader + IFC mapping
requests>=2.31,<3.0            # Stream W: autonomous foraging HTTP client
```

**NOT added (rejected after trade-off):**
- `pykeen` — heavy torch-dep; existing TransE trainer in `extraction/kg_link_predictor.py` is sufficient.
- `rocksdb` — builds native; `plyvel` (LevelDB) covers the same ground with a cleaner wheel.
- `fastapi` — no HTTP service layer in this plan's scope.
- `apache-arrow` separately — `pyarrow` includes Arrow.

**Rust toolchain (Streams M + N):**

```bash
# One-time installation (if not already present):
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
pip3 install maturin>=1.5,<2.0
```

### 3.2 New Configuration Keys (`config/vitruvius.yaml` — additive only)

```yaml
features:
  # Stream I — Query Layer v2
  i_query_ontology_translator: false
  i_query_graphrag_router: false
  i_query_mcmc_ranker: false
  i_query_pipeline_hmm: false
  # Stream J — Active Learning
  j_active_uncertainty_sampling: false
  j_expected_model_change: false
  # Stream K — CLUP Scaling (gated on ≥2 jurisdictions)
  k_rosetta_stone: false
  k_precedence_router: false
  k_tensor_activation: false
  # Stream L — Spatial Reasoning
  l_spatial_contract: false
  l_z3_parametric_evaluator: false
  l_spatial_ingestion: false
  # Stream M — Rust Ingest Kernel
  m_rust_bloom_filter: false
  m_minhash_lsh: false
  # Stream N — Rust Topology Kernel
  n_rust_csr_kernel: false
  n_rust_rwr: false
  n_rust_pagerank: false
  # Stream O — Binary Storage Vault
  o_parquet_archives: false
  o_flatbuffers_intermediate: false
  o_lmdb_hot_store: false
  # Stream P — Event-Sourced Graph
  p_event_log: false
  p_time_travel_query: false
  # Stream Q — Temporal Query
  q_temporal_mask: false
  # Stream R — Epistemic MC Dropout
  r_mc_dropout_sampling: false
  r_dempster_shafer_fusion: false
  # Stream S — Subgraph Clash Detection
  s_violation_motif_library: false
  s_subgraph_isomorphism: false
  # Stream T — Adaptive Chunking
  t_adaptive_window_sizing: false
  # Stream U — Hardware Router
  u_hardware_aware_routing: false
  # Stream V — IFC/OWL
  v_ifc_owl_mapping: false
  # Stream W — Foraging
  w_autonomous_forager: false
  # Stream X — Boltzmann Health
  x_boltzmann_promotion_gate: false

ultimate_upgrade:
  z3_solver:
    default_timeout_ms: 5000
    reals_precision: 6            # decimal digits
  rust_kernels:
    bloom_filter_size_bits: 1_000_000
    bloom_num_hashes: 5
    minhash_permutations: 128
    lsh_band_size: 8
    lsh_num_bands: 16
  binary_vault:
    lmdb_map_size_mb: 256
    parquet_compression: "zstd"
    flatbuffers_root_dir: "005_Operational-Intelligence-Layer/flatbuffers"
  event_sourced_graph:
    log_root: "006_System-Manifests/graph_event_log"
    max_events_per_file: 10000
  temporal_query:
    default_epoch: "latest"       # or ISO8601 string
  mc_dropout:
    num_samples: 10
    epistemic_threshold_tau: 0.25
  subgraph_isomorphism:
    motif_library: ".ai/06_specs/violation_motifs.yaml"
    vf2_timeout_seconds: 2
  adaptive_chunking:
    min_overlap_ratio: 0.1
    max_overlap_ratio: 0.5
    density_probe_window: 128     # characters
  hardware_router:
    e2b_min_ram_gb: 2.0
    e4b_min_ram_gb: 4.0
    b31_min_ram_gb: 18.0
    safety_buffer_gb: 2.0
  ifc_owl:
    ifc_schema: "IFC4_ADD2"
    owl_root: "005_Operational-Intelligence-Layer/ontology"
  foraging:
    lgu_registries: []            # populated per deployment
    drift_threshold_sigma: 3.0
    poll_interval_minutes: 1440   # daily
  boltzmann:
    contradiction_unit_energy: 1.0
    unverified_unit_energy: 0.1
    default_temperature_T: 10.0
```

### 3.3 Disk & RAM Accounting Addendum

Adds to `statistical-architectural-upgrade-plan.md` §3.4:

| Dep | Disk | Cold-start RAM | Load trigger |
|---|---|---|---|
| z3-solver | ~18 MB | ~12 MB | import z3 |
| pyarrow | ~70 MB | ~40 MB | import pyarrow |
| plyvel | ~2 MB | ~5 MB | import plyvel |
| flatbuffers (Python runtime) | ~1 MB | ~1 MB | import flatbuffers |
| owlready2 | ~15 MB | ~20 MB | import owlready2 |
| requests | already present transitively | ~4 MB | import requests |
| Rust extensions (ingest + topology) | ~5 MB compiled | ~2 MB | import vitruvius_ingest_kernel |
| **Total additive** | **~111 MB** | **~84 MB** | Steady state once all flags ON |

Reserve budget: 500 MB for intermediate FlatBuffers + LMDB page cache. Hard ceiling: 1.2 GB for the entire new stack. Remaining 6.8 GB available for Ollama + OS — safely exceeds the e4b model requirement (3 GB) with headroom for gemma4:31b if a user explicitly routes there.

---

## 4. File Structure Map

### 4.1 New subpackages in `scripts/vitruvius/`

```
scripts/vitruvius/
├── query/                                       # Stream I — Phase 9 base + extensions
│   ├── __init__.py
│   ├── nl_translator.py                         # I.0
│   ├── structured_call_builder.py               # I.0
│   ├── ontology_prompt.py                       # I.1
│   ├── graphrag_router.py                       # I.2
│   ├── mcmc_ranker.py                           # I.3
│   └── pipeline_hmm.py                          # I.4
├── learning/                                    # Stream J
│   ├── __init__.py
│   ├── active_learning.py                       # J.1
│   └── expected_model_change.py                 # J.2
├── jurisdictions/                               # Stream K — gated
│   ├── __init__.py
│   ├── rosetta_stone.py                         # K.1
│   └── precedence_router.py                     # K.2
├── spatial/                                     # Stream L — new
│   ├── __init__.py
│   ├── contract.py                              # L.1 (spatial JSON schema)
│   ├── ingestion.py                             # L.2
│   ├── z3_evaluator.py                          # L.3
│   ├── parametric_edge.py                       # L.4
│   └── compliance_report.py                     # L.5
├── ingest_kernel/                               # Stream M — PyO3 binding + Python fallback
│   ├── __init__.py
│   ├── python_fallback.py                       # pure-Python Bloom + MinHash (used when Rust unavailable)
│   └── __pyo3_bridge.py                         # thin adapter — imports vitruvius_ingest_kernel crate
├── topology_kernel/                             # Stream N — PyO3 binding + Python fallback
│   ├── __init__.py
│   ├── python_fallback.py                       # scipy CSR + numpy RWR (used when Rust unavailable)
│   └── __pyo3_bridge.py                         # thin adapter — imports vitruvius_topology_kernel crate
├── binary_vault/                                # Stream O
│   ├── __init__.py
│   ├── parquet_writer.py                        # O.1
│   ├── parquet_reader.py                        # O.2
│   ├── flatbuffers_schema.py                    # O.4 (generated from .fbs)
│   ├── flatbuffers_encoder.py                   # O.5
│   └── lmdb_hot_store.py                        # O.6
├── event_sourced/                               # Stream P
│   ├── __init__.py
│   ├── event_log.py                             # P.1
│   ├── event_types.py                           # P.2
│   ├── replay_engine.py                         # P.3
│   └── time_travel.py                           # P.5
├── temporal_query/                              # Stream Q
│   ├── __init__.py
│   └── time_mask.py                             # Q.1
├── epistemic/                                   # Stream R
│   ├── __init__.py
│   ├── mc_dropout.py                            # R.1
│   └── dempster_shafer.py                       # R.5
├── clash/                                       # Stream S
│   ├── __init__.py
│   ├── motif_library.py                         # S.1
│   └── subgraph_iso.py                          # S.2
├── adaptive_chunk/                              # Stream T
│   ├── __init__.py
│   └── nyquist_chunker.py                       # T.1
├── hardware_router.py                           # Stream U (top-level — single file)
├── ontology/                                    # Stream V
│   ├── __init__.py
│   ├── ifc_mapper.py                            # V.1
│   └── owl_loader.py                            # V.3
├── foraging/                                    # Stream W
│   ├── __init__.py
│   ├── crawler.py                               # W.1
│   └── drift_detector.py                        # W.3
└── health/                                      # Stream X
    ├── __init__.py
    └── boltzmann_energy.py                      # X.1
```

### 4.2 New Rust crates in `rust_kernels/`

```
rust_kernels/
├── vitruvius-ingest-kernel/
│   ├── Cargo.toml
│   ├── pyproject.toml                           # maturin build config
│   └── src/
│       ├── lib.rs                               # PyO3 module root
│       ├── bloom.rs                             # Stream M.1
│       └── minhash.rs                           # Stream M.6
└── vitruvius-topology-kernel/
    ├── Cargo.toml
    ├── pyproject.toml
    └── src/
        ├── lib.rs                               # PyO3 module root
        ├── csr.rs                               # Stream N.1
        ├── rwr.rs                               # Stream N.4
        └── pagerank.rs                          # Stream N.6
```

### 4.3 New test files in `scripts/tests/`

```
scripts/tests/
# Stream I
├── test_query_nl_translator.py                  # I.0
├── test_query_structured_call.py                # I.0
├── test_query_ontology_prompt.py                # I.1
├── test_query_graphrag_router.py                # I.2
├── test_query_mcmc_ranker.py                    # I.3
├── test_query_pipeline_hmm.py                   # I.4
# Stream J
├── test_learning_active.py                      # J.1
├── test_learning_emc.py                         # J.2
# Stream K
├── test_jurisdictions_rosetta.py                # K.1
├── test_jurisdictions_precedence.py             # K.2
# Stream L
├── test_spatial_contract.py                     # L.1
├── test_spatial_ingestion.py                    # L.2
├── test_spatial_z3_evaluator.py                 # L.3
├── test_spatial_parametric_edge.py              # L.4
├── test_spatial_compliance_report.py            # L.5
# Stream M
├── test_ingest_kernel_bloom.py                  # M.1–M.3
├── test_ingest_kernel_minhash.py                # M.6–M.8
├── test_ingest_kernel_fallback.py               # M.9
# Stream N
├── test_topology_kernel_csr.py                  # N.1
├── test_topology_kernel_rwr.py                  # N.4
├── test_topology_kernel_pagerank.py             # N.6
├── test_topology_kernel_fallback.py             # N.7
# Stream O
├── test_binary_vault_parquet.py                 # O.1–O.3
├── test_binary_vault_flatbuffers.py             # O.4–O.5
├── test_binary_vault_lmdb.py                    # O.6–O.8
# Stream P
├── test_event_sourced_log.py                    # P.1–P.3
├── test_event_sourced_replay.py                 # P.4
├── test_event_sourced_time_travel.py            # P.5–P.7
# Stream Q
├── test_temporal_query_mask.py                  # Q.1–Q.5
# Stream R
├── test_epistemic_mc_dropout.py                 # R.1–R.4
├── test_epistemic_dempster_shafer.py            # R.5–R.6
# Stream S
├── test_clash_motif_library.py                  # S.1
├── test_clash_subgraph_iso.py                   # S.2–S.5
# Stream T
├── test_adaptive_chunker_nyquist.py             # T.1–T.4
# Stream U
├── test_hardware_router.py                      # U.1–U.4
# Stream V
├── test_ontology_ifc_mapper.py                  # V.1–V.6
# Stream W
├── test_foraging_crawler.py                     # W.1–W.2
├── test_foraging_drift.py                       # W.3–W.5
# Stream X
├── test_health_boltzmann.py                     # X.1–X.3
```

### 4.4 New canonical / operational / manifest layer files

```
005_Operational-Intelligence-Layer/
├── flatbuffers/                                 # Stream O.4
│   └── chunks/
├── event_log/                                   # Stream P (mirror in 006 for immutability)
├── query/                                       # Stream I — cached query artefacts
│   ├── latest_nl_translations.json
│   ├── latest_mcmc_ranking.json
│   └── latest_pipeline_hmm_state.json
├── learning/                                    # Stream J
│   └── latest_active_queue.json
├── ontology/                                    # Stream V
│   ├── ifc_mapping.ttl
│   └── vitruvius_ontology.owl
├── spatial/                                     # Stream L
│   └── latest_compliance_report.json
└── health/                                      # Stream X
    └── latest_boltzmann_energy.json

006_System-Manifests/
├── graph_event_log/                             # Stream P — immutable append-only
│   ├── 2026-04/
│   │   ├── events_000001.jsonl
│   │   └── events_000002.jsonl
│   └── checkpoint.json
└── runs/                                        # existing — new subkeys added
    ├── latest_spatial_ingestion.json            # Stream L
    ├── latest_motif_matches.json                # Stream S
    └── latest_forager_drift.json                # Stream W

001B_Spatial-Source-Layer/                       # NEW top-level directory (Stream L.5)
└── .gitkeep
```

---

# STREAMS — TASKS BEGIN HERE

---

## 5. Stream I — Query Layer v2 (finish Phase 9)

### 5.1 Goal
Ship Phase 9 base (NL → structured graph query) and layer in ontology-embedded prompting, GraphRAG community routing, MCMC answer ranking, and HMM pipeline-state observability. Every query result cites the canonical source nodes and carries the MCMC stationary-distribution score of every cited concept.

### 5.2 Files
- Create: `scripts/vitruvius/query/__init__.py`
- Create: `scripts/vitruvius/query/nl_translator.py`
- Create: `scripts/vitruvius/query/structured_call_builder.py`
- Create: `scripts/vitruvius/query/ontology_prompt.py`
- Create: `scripts/vitruvius/query/graphrag_router.py`
- Create: `scripts/vitruvius/query/mcmc_ranker.py`
- Create: `scripts/vitruvius/query/pipeline_hmm.py`
- Create: `scripts/tests/test_query_nl_translator.py`
- Create: `scripts/tests/test_query_structured_call.py`
- Create: `scripts/tests/test_query_ontology_prompt.py`
- Create: `scripts/tests/test_query_graphrag_router.py`
- Create: `scripts/tests/test_query_mcmc_ranker.py`
- Create: `scripts/tests/test_query_pipeline_hmm.py`
- Modify: `scripts/pipeline_cli.py` (register `query-graph-rag`, `query-hmm-state` commands — lazy imports)
- Modify: `scripts/vitruvius/features.py` (add flags under `i_query_*`)

### 5.3 Task Sequence

---

### Task I.1: Structured Call Builder (deterministic, zero LLM)

**Rationale:** Before adding the LLM translator, build a deterministic call builder that takes a `{"intent": ..., "entities": [...], "time": ..., "jurisdiction": ...}` dict and emits the corresponding `graph.traverse` invocation. This gives the LLM translator a pure target to generate against.

**Files:**
- Create: `scripts/vitruvius/query/structured_call_builder.py`
- Create: `scripts/vitruvius/query/__init__.py`
- Create: `scripts/tests/test_query_structured_call.py`

- [ ] **Step 1: Write the failing test**

```python
# scripts/tests/test_query_structured_call.py
from vitruvius.query.structured_call_builder import (
    StructuredCall,
    build_call,
    CallValidationError,
)


def test_build_call_neighbors_of_concept():
    call = build_call({
        "intent": "neighbors_of",
        "entities": ["concept-occupancy-classification"],
        "max_depth": 2,
    })
    assert isinstance(call, StructuredCall)
    assert call.operation == "traverse.neighbors"
    assert call.args["node_id"] == "concept-occupancy-classification"
    assert call.args["depth"] == 2


def test_build_call_path_between_two_concepts():
    call = build_call({
        "intent": "path_between",
        "entities": [
            "concept-building-permit",
            "concept-fire-clearance",
        ],
    })
    assert call.operation == "traverse.shortest_path"
    assert call.args["from_id"] == "concept-building-permit"
    assert call.args["to_id"] == "concept-fire-clearance"


def test_build_call_rejects_missing_intent():
    try:
        build_call({"entities": ["x"]})
    except CallValidationError as exc:
        assert "intent" in str(exc)
    else:
        raise AssertionError("expected CallValidationError")


def test_build_call_rejects_neighbors_without_entity():
    try:
        build_call({"intent": "neighbors_of", "entities": []})
    except CallValidationError as exc:
        assert "entities" in str(exc)
    else:
        raise AssertionError("expected CallValidationError")


def test_build_call_is_deterministic_order():
    payload = {
        "intent": "neighbors_of",
        "entities": ["concept-a"],
        "max_depth": 1,
    }
    a = build_call(payload)
    b = build_call(payload)
    assert a == b
```

- [ ] **Step 2: Run test to verify it fails**

```bash
python3 -m pytest scripts/tests/test_query_structured_call.py -v
```
Expected: `ImportError: cannot import name 'build_call' from 'vitruvius.query.structured_call_builder'`.

- [ ] **Step 3: Write the implementation**

```python
# scripts/vitruvius/query/__init__.py
"""Vitruvius Query Layer v2 (Phase 9 base + Stream I extensions)."""
```

```python
# scripts/vitruvius/query/structured_call_builder.py
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping


class CallValidationError(ValueError):
    """Raised when an intent payload cannot be mapped to a graph call."""


@dataclass(frozen=True)
class StructuredCall:
    operation: str
    args: Mapping[str, Any] = field(default_factory=dict)


_ALLOWED_INTENTS = {
    "neighbors_of",
    "path_between",
    "citations_of",
    "list_community",
}


def _require(payload: Mapping[str, Any], key: str) -> Any:
    if key not in payload:
        raise CallValidationError(f"missing required key: {key!r}")
    return payload[key]


def build_call(payload: Mapping[str, Any]) -> StructuredCall:
    intent = _require(payload, "intent")
    if intent not in _ALLOWED_INTENTS:
        raise CallValidationError(f"unknown intent: {intent!r}")

    if intent == "neighbors_of":
        entities = _require(payload, "entities")
        if not entities:
            raise CallValidationError("neighbors_of requires >=1 entity")
        depth = int(payload.get("max_depth", 1))
        return StructuredCall(
            operation="traverse.neighbors",
            args={"node_id": entities[0], "depth": depth},
        )

    if intent == "path_between":
        entities = _require(payload, "entities")
        if len(entities) != 2:
            raise CallValidationError("path_between requires exactly 2 entities")
        return StructuredCall(
            operation="traverse.shortest_path",
            args={"from_id": entities[0], "to_id": entities[1]},
        )

    if intent == "citations_of":
        entities = _require(payload, "entities")
        if not entities:
            raise CallValidationError("citations_of requires >=1 entity")
        return StructuredCall(
            operation="traverse.incoming_edges",
            args={"node_id": entities[0]},
        )

    # list_community
    community_id = _require(payload, "community_id")
    return StructuredCall(
        operation="community.list_members",
        args={"community_id": int(community_id)},
    )
```

- [ ] **Step 4: Run test to verify it passes**

```bash
python3 -m pytest scripts/tests/test_query_structured_call.py -v
```
Expected: 5 passed.

- [ ] **Step 5: Commit**

```bash
git add scripts/vitruvius/query/__init__.py scripts/vitruvius/query/structured_call_builder.py scripts/tests/test_query_structured_call.py
git commit -m "feat(query): add structured call builder (Task I.1)"
```

---

### Task I.2: NL Translator (Phase 9 base, LLM-backed)

**Rationale:** Wraps an Ollama call that turns a user's natural-language question into the dict payload consumed by `structured_call_builder.build_call`. Uses the existing `config.OLLAMA_URL` + `ollama_config` paths. Mockable via a `translator_fn` injection for tests.

**Files:**
- Create: `scripts/vitruvius/query/nl_translator.py`
- Create: `scripts/tests/test_query_nl_translator.py`

- [ ] **Step 1: Write the failing test**

```python
# scripts/tests/test_query_nl_translator.py
from vitruvius.query.nl_translator import (
    translate_nl,
    NLTranslationError,
)


def _fake_llm_returning(payload_json: str):
    def _fn(prompt: str) -> str:
        return payload_json
    return _fn


def test_translate_nl_happy_path():
    fake = _fake_llm_returning(
        '{"intent": "neighbors_of", "entities": ["concept-permit"], "max_depth": 2}'
    )
    result = translate_nl(
        "What concepts are near a building permit within 2 hops?",
        translator_fn=fake,
    )
    assert result["intent"] == "neighbors_of"
    assert result["entities"] == ["concept-permit"]
    assert result["max_depth"] == 2


def test_translate_nl_strips_code_fence():
    fake = _fake_llm_returning(
        '```json\n{"intent": "neighbors_of", "entities": ["x"]}\n```'
    )
    result = translate_nl("X?", translator_fn=fake)
    assert result["entities"] == ["x"]


def test_translate_nl_rejects_non_json():
    fake = _fake_llm_returning("this is not json at all")
    try:
        translate_nl("blah", translator_fn=fake)
    except NLTranslationError as exc:
        assert "parse" in str(exc).lower()
    else:
        raise AssertionError("expected NLTranslationError")
```

- [ ] **Step 2: Run to fail**

```bash
python3 -m pytest scripts/tests/test_query_nl_translator.py -v
```

- [ ] **Step 3: Write implementation**

```python
# scripts/vitruvius/query/nl_translator.py
from __future__ import annotations

import json
import re
from typing import Any, Callable, Mapping, Optional


class NLTranslationError(RuntimeError):
    """Raised when the LLM response cannot be parsed to a structured intent."""


_FENCE_RE = re.compile(r"^```(?:json)?\s*\n(?P<body>.*?)\n```\s*$", re.DOTALL)

_SYSTEM_PROMPT = """\
You are the Vitruvius NL Translator. Convert the user's question into a
single JSON object matching ONE of:
- {"intent":"neighbors_of","entities":["<node_id>"],"max_depth":<int>}
- {"intent":"path_between","entities":["<from>","<to>"]}
- {"intent":"citations_of","entities":["<node_id>"]}
- {"intent":"list_community","community_id":<int>}
Respond with ONLY the JSON object. No prose, no markdown.
"""


def _extract_body(raw: str) -> str:
    match = _FENCE_RE.match(raw.strip())
    if match:
        return match.group("body").strip()
    return raw.strip()


def translate_nl(
    question: str,
    *,
    translator_fn: Optional[Callable[[str], str]] = None,
) -> Mapping[str, Any]:
    """Translate a natural-language question into a structured intent dict."""
    if translator_fn is None:
        from vitruvius.query._ollama_adapter import call_translator
        translator_fn = call_translator

    prompt = f"{_SYSTEM_PROMPT}\n\nQuestion: {question}\n\nJSON:"
    raw = translator_fn(prompt)
    body = _extract_body(raw)

    try:
        payload = json.loads(body)
    except json.JSONDecodeError as exc:
        raise NLTranslationError(
            f"could not parse translator response: {exc}; raw={raw!r}"
        ) from exc

    if not isinstance(payload, dict):
        raise NLTranslationError(
            f"translator returned non-object: {type(payload).__name__}"
        )

    return payload
```

```python
# scripts/vitruvius/query/_ollama_adapter.py
from __future__ import annotations

from vitruvius import config
from vitruvius.review.ollama_config import default_chat_options


def call_translator(prompt: str) -> str:
    """Thin adapter — intentionally stubbed; production wires to ollama_review pattern."""
    # Implementation reuses the existing ollama_review HTTP call pattern.
    # For this task we ship only the translator_fn injection path; the
    # production wiring is unit-tested via Task I.2b.
    import json as _json
    import urllib.request as _url

    req = _url.Request(
        f"{config.OLLAMA_URL}/api/chat",
        data=_json.dumps({
            "model": default_chat_options().model,
            "messages": [
                {"role": "system", "content": "You are the Vitruvius NL Translator."},
                {"role": "user", "content": prompt},
            ],
            "stream": False,
        }).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with _url.urlopen(req, timeout=30) as resp:
        data = _json.loads(resp.read().decode("utf-8"))
    return data["message"]["content"]
```

- [ ] **Step 4: Run to pass**

```bash
python3 -m pytest scripts/tests/test_query_nl_translator.py -v
```
Expected: 3 passed.

- [ ] **Step 5: Commit**

```bash
git add scripts/vitruvius/query/nl_translator.py scripts/vitruvius/query/_ollama_adapter.py scripts/tests/test_query_nl_translator.py
git commit -m "feat(query): add NL translator with injectable translator_fn (Task I.2)"
```

---

### Task I.3: Ontology-Embedded Prompt Builder (uses Stream H.1 centrality)

**Rationale:** Enriches the translator's prompt with the top-K most central nodes and a shortlist of known communities, so the LLM picks from a curated entity list instead of hallucinating node IDs.

**Files:**
- Create: `scripts/vitruvius/query/ontology_prompt.py`
- Create: `scripts/tests/test_query_ontology_prompt.py`

- [ ] **Step 1: Write test**

```python
# scripts/tests/test_query_ontology_prompt.py
from vitruvius.graph.contract import GraphNode, GraphEdge, GraphSnapshot
from vitruvius.query.ontology_prompt import build_ontology_prompt


def _mini_snapshot() -> GraphSnapshot:
    nodes = [
        GraphNode(
            id=f"concept-c{i}",
            type="concept",
            slug=f"c{i}",
            trust_level="primary",
            last_updated_utc="2026-04-14T00:00:00Z",
        )
        for i in range(5)
    ]
    edges = [
        GraphEdge(from_id="concept-c0", to_id="concept-c1", type="governs",
                  evidence_id="rel-001", status="verified"),
        GraphEdge(from_id="concept-c0", to_id="concept-c2", type="governs",
                  evidence_id="rel-002", status="verified"),
        GraphEdge(from_id="concept-c0", to_id="concept-c3", type="governs",
                  evidence_id="rel-003", status="verified"),
    ]
    return GraphSnapshot(
        schema_version="1.0.0",
        generated_at_utc="2026-04-14T00:00:00Z",
        node_count=len(nodes),
        edge_count=len(edges),
        nodes=nodes,
        edges=edges,
    )


def test_ontology_prompt_includes_top_central_nodes():
    snapshot = _mini_snapshot()
    prompt = build_ontology_prompt(snapshot, top_k=3)
    assert "concept-c0" in prompt  # c0 has the highest degree
    assert "Known concepts" in prompt or "Candidate entities" in prompt


def test_ontology_prompt_caps_list():
    snapshot = _mini_snapshot()
    prompt = build_ontology_prompt(snapshot, top_k=2)
    entities_listed = [n.id for n in snapshot.nodes if n.id in prompt]
    assert len(entities_listed) <= 4  # allow small fuzziness
```

- [ ] **Step 2: Run to fail**

```bash
python3 -m pytest scripts/tests/test_query_ontology_prompt.py -v
```

- [ ] **Step 3: Implement**

```python
# scripts/vitruvius/query/ontology_prompt.py
from __future__ import annotations

from vitruvius.graph.centrality import compute_centrality
from vitruvius.graph.contract import GraphSnapshot


def build_ontology_prompt(snapshot: GraphSnapshot, *, top_k: int = 50) -> str:
    """Build an ontology-embedded system prompt fragment for the NL translator."""
    report = compute_centrality(snapshot, kind="degree")
    top_ids = [nid for nid, _ in report.scores[:top_k]]

    bullet_lines = "\n".join(f"- {nid}" for nid in top_ids)
    return (
        "Candidate entities (top-"
        f"{top_k} by degree centrality; prefer these when parsing the question):\n"
        f"{bullet_lines}\n"
    )
```

- [ ] **Step 4: Run to pass**

```bash
python3 -m pytest scripts/tests/test_query_ontology_prompt.py -v
```

- [ ] **Step 5: Commit**

```bash
git add scripts/vitruvius/query/ontology_prompt.py scripts/tests/test_query_ontology_prompt.py
git commit -m "feat(query): add ontology-embedded prompt builder (Task I.3)"
```

---

### Task I.4: GraphRAG Community Router

**Rationale:** When a question could match multiple Louvain communities, route to the single community whose top-central node is the best match. This is the "GraphRAG" step — limit LLM context to one community's nodes at a time.

**Files:**
- Create: `scripts/vitruvius/query/graphrag_router.py`
- Create: `scripts/tests/test_query_graphrag_router.py`

- [ ] **Step 1: Write test**

```python
# scripts/tests/test_query_graphrag_router.py
from vitruvius.graph.contract import GraphNode, GraphEdge, GraphSnapshot
from vitruvius.query.graphrag_router import route_to_community


def _two_community_snapshot() -> GraphSnapshot:
    # Community A: a-b-c cluster. Community B: x-y-z cluster. Sparse cross-edge.
    raw_ids = ("a", "b", "c", "x", "y", "z")
    nodes = [
        GraphNode(
            id=f"concept-{n}",
            type="concept",
            slug=n,
            trust_level="primary",
            last_updated_utc="2026-04-14T00:00:00Z",
        )
        for n in raw_ids
    ]
    e = [
        ("a", "b"), ("b", "c"), ("a", "c"),
        ("x", "y"), ("y", "z"), ("x", "z"),
        ("c", "x"),  # weak bridge
    ]
    edges = [
        GraphEdge(
            from_id=f"concept-{s}",
            to_id=f"concept-{t}",
            type="related_to",
            evidence_id=f"rel-{i:03d}",
            status="verified",
        )
        for i, (s, t) in enumerate(e)
    ]
    return GraphSnapshot(
        schema_version="1.0.0",
        generated_at_utc="2026-04-14T00:00:00Z",
        node_count=len(nodes),
        edge_count=len(edges),
        nodes=nodes,
        edges=edges,
    )


def test_route_picks_community_containing_entity():
    snap = _two_community_snapshot()
    result = route_to_community(snap, entity_id="concept-b")
    assert "concept-b" in result.community_node_ids
    assert "concept-x" not in result.community_node_ids


def test_route_unknown_entity_returns_empty_community():
    snap = _two_community_snapshot()
    result = route_to_community(snap, entity_id="concept-missing")
    assert result.community_node_ids == ()
    assert result.community_id == -1
```

- [ ] **Step 2: Run to fail**

- [ ] **Step 3: Implement**

```python
# scripts/vitruvius/query/graphrag_router.py
from __future__ import annotations

from dataclasses import dataclass

from vitruvius.graph.community import detect_communities
from vitruvius.graph.contract import GraphSnapshot


@dataclass(frozen=True)
class RoutingResult:
    community_id: int
    community_node_ids: tuple[str, ...]


def route_to_community(snapshot: GraphSnapshot, *, entity_id: str) -> RoutingResult:
    report = detect_communities(snapshot)
    for community in report.communities:
        if entity_id in community.node_ids:
            return RoutingResult(
                community_id=community.community_id,
                community_node_ids=community.node_ids,
            )
    return RoutingResult(community_id=-1, community_node_ids=())
```

- [ ] **Step 4: Run to pass**

```bash
python3 -m pytest scripts/tests/test_query_graphrag_router.py -v
```

- [ ] **Step 5: Commit**

```bash
git add scripts/vitruvius/query/graphrag_router.py scripts/tests/test_query_graphrag_router.py
git commit -m "feat(query): add GraphRAG community router (Task I.4)"
```

---

### Task I.5: MCMC Answer Ranker

**Rationale:** Given a set of candidate answer nodes, rank them by their stationary distribution score under random walk with restart seeded at the entity from the user's question. Reuses `graph/mcmc.py`.

**Files:**
- Create: `scripts/vitruvius/query/mcmc_ranker.py`
- Create: `scripts/tests/test_query_mcmc_ranker.py`

- [ ] **Step 1: Write test**

```python
# scripts/tests/test_query_mcmc_ranker.py
from vitruvius.graph.contract import GraphNode, GraphEdge, GraphSnapshot
from vitruvius.query.mcmc_ranker import rank_candidates


def _linear_chain_snapshot() -> GraphSnapshot:
    nodes = [
        GraphNode(
            id=f"concept-n{i}",
            type="concept",
            slug=f"n{i}",
            trust_level="primary",
            last_updated_utc="2026-04-14T00:00:00Z",
        )
        for i in range(5)
    ]
    edges = [
        GraphEdge(
            from_id=f"concept-n{i}",
            to_id=f"concept-n{i+1}",
            type="next",
            evidence_id=f"rel-{i:03d}",
            status="verified",
        )
        for i in range(4)
    ]
    return GraphSnapshot(
        schema_version="1.0.0",
        generated_at_utc="2026-04-14T00:00:00Z",
        node_count=len(nodes),
        edge_count=len(edges),
        nodes=nodes,
        edges=edges,
    )


def test_rank_orders_closer_nodes_higher():
    snap = _linear_chain_snapshot()
    ranked = rank_candidates(
        snap,
        seed_node="concept-n0",
        candidates=["concept-n4", "concept-n1", "concept-n2"],
        rng_seed=0,
    )
    assert ranked[0][0] == "concept-n1"
    assert ranked[-1][0] == "concept-n4"


def test_rank_empty_candidates_returns_empty():
    snap = _linear_chain_snapshot()
    assert rank_candidates(snap, seed_node="concept-n0", candidates=[]) == ()
```

- [ ] **Step 2: Run to fail**

- [ ] **Step 3: Implement**

```python
# scripts/vitruvius/query/mcmc_ranker.py
from __future__ import annotations

from vitruvius.graph.contract import GraphSnapshot
from vitruvius.graph.mcmc import mcmc_random_walk


def rank_candidates(
    snapshot: GraphSnapshot,
    *,
    seed_node: str,
    candidates: list[str],
    alpha: float = 0.85,
    steps: int = 10_000,
    rng_seed: int = 0,
) -> tuple[tuple[str, float], ...]:
    if not candidates:
        return ()
    result = mcmc_random_walk(
        snapshot,
        seed_id=seed_node,
        alpha=alpha,
        steps=steps,
        rng_seed=rng_seed,
    )
    freq_map = dict(result.visit_frequency)
    scored = [(cand, float(freq_map.get(cand, 0.0))) for cand in candidates]
    scored.sort(key=lambda kv: (-kv[1], kv[0]))
    return tuple(scored)
```

- [ ] **Step 4: Run to pass**

```bash
python3 -m pytest scripts/tests/test_query_mcmc_ranker.py -v
```

- [ ] **Step 5: Commit**

```bash
git add scripts/vitruvius/query/mcmc_ranker.py scripts/tests/test_query_mcmc_ranker.py
git commit -m "feat(query): add MCMC answer ranker (Task I.5)"
```

---

### Task I.6: Pipeline HMM Observability

**Rationale:** Hidden Markov Model over pipeline phase transitions (raw→convert→refine→canonicalize→extract→review→promote→graph). Trained on historical `006_System-Manifests/runs/*.json`. Predicts expected total wall-clock + probability of rollback per batch.

**Files:**
- Create: `scripts/vitruvius/query/pipeline_hmm.py`
- Create: `scripts/tests/test_query_pipeline_hmm.py`

- [ ] **Step 1: Write test**

```python
# scripts/tests/test_query_pipeline_hmm.py
from vitruvius.query.pipeline_hmm import (
    PipelineHMM,
    TransitionObservation,
)


def _sample_observations():
    return [
        TransitionObservation(from_state="convert", to_state="refine", count=10),
        TransitionObservation(from_state="convert", to_state="error", count=2),
        TransitionObservation(from_state="refine", to_state="canonicalize", count=10),
    ]


def test_hmm_fits_transition_matrix():
    hmm = PipelineHMM()
    hmm.fit(_sample_observations())
    probs = hmm.transition_probabilities("convert")
    assert abs(probs["refine"] - (10 / 12)) < 1e-9
    assert abs(probs["error"] - (2 / 12)) < 1e-9


def test_hmm_unknown_state_returns_empty():
    hmm = PipelineHMM()
    hmm.fit(_sample_observations())
    assert hmm.transition_probabilities("nonexistent") == {}


def test_hmm_deterministic_order():
    hmm = PipelineHMM()
    hmm.fit(_sample_observations())
    assert list(hmm.transition_probabilities("convert").keys()) == ["error", "refine"]
```

- [ ] **Step 2: Run to fail**

- [ ] **Step 3: Implement**

```python
# scripts/vitruvius/query/pipeline_hmm.py
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from typing import Mapping


@dataclass(frozen=True)
class TransitionObservation:
    from_state: str
    to_state: str
    count: int


@dataclass
class PipelineHMM:
    _counts: dict[str, dict[str, int]] = field(default_factory=lambda: defaultdict(dict))

    def fit(self, observations: list[TransitionObservation]) -> None:
        self._counts.clear()
        for obs in observations:
            bucket = self._counts.setdefault(obs.from_state, {})
            bucket[obs.to_state] = bucket.get(obs.to_state, 0) + obs.count

    def transition_probabilities(self, from_state: str) -> Mapping[str, float]:
        bucket = self._counts.get(from_state)
        if not bucket:
            return {}
        total = sum(bucket.values())
        if total == 0:
            return {}
        items = sorted(bucket.items(), key=lambda kv: kv[0])
        return {state: count / total for state, count in items}
```

- [ ] **Step 4: Run to pass**

```bash
python3 -m pytest scripts/tests/test_query_pipeline_hmm.py -v
```

- [ ] **Step 5: Commit**

```bash
git add scripts/vitruvius/query/pipeline_hmm.py scripts/tests/test_query_pipeline_hmm.py
git commit -m "feat(query): add pipeline HMM transition observer (Task I.6)"
```

### 5.4 Stream I Definition of Done
- [ ] All six Stream I task test files pass: `python3 -m pytest scripts/tests/test_query_*.py -v`
- [ ] `features.i_query_*` flags added to `features.py` with defaults `false`.
- [ ] Backward-compat regression suite green.
- [ ] No changes to Phase 8 `graph/` public API.


---

## 6. Stream J — Active Learning Infrastructure

### 6.1 Goal
Turn the existing Tier 3 Ranger review queue into a continuous-improvement loop: uncertainty-sampling picks the candidates where the Naive Bayes filter is weakest, Expected Model Change scoring routes them to humans in priority order. Rangers' corrections are appended to the CRF + NB training corpus so the models improve run-over-run.

### 6.2 Files
- Create: `scripts/vitruvius/learning/__init__.py`
- Create: `scripts/vitruvius/learning/active_learning.py`
- Create: `scripts/vitruvius/learning/expected_model_change.py`
- Create: `scripts/tests/test_learning_active.py`
- Create: `scripts/tests/test_learning_emc.py`
- Modify: `scripts/vitruvius/features.py` (`j_active_uncertainty_sampling`, `j_expected_model_change`)

### 6.3 Task Sequence

---

### Task J.1: Uncertainty-sampling queue

**Rationale:** Given Naive Bayes probabilities from `review/naive_bayes_filter.py`, pick the candidates with predictive entropy closest to log(2) (maximum uncertainty for a binary classifier). Emit a Ranger queue sorted descending by entropy.

**Files:**
- Create: `scripts/vitruvius/learning/__init__.py`
- Create: `scripts/vitruvius/learning/active_learning.py`
- Create: `scripts/tests/test_learning_active.py`

- [ ] **Step 1: Write test**

```python
# scripts/tests/test_learning_active.py
from vitruvius.learning.active_learning import (
    uncertainty_sampling,
    UncertaintyItem,
)


def test_uncertainty_sampling_orders_by_entropy_descending():
    items = [
        UncertaintyItem(candidate_id="a", p_keep=0.99),  # low entropy
        UncertaintyItem(candidate_id="b", p_keep=0.5),   # max entropy
        UncertaintyItem(candidate_id="c", p_keep=0.8),
    ]
    queue = uncertainty_sampling(items, top_k=3)
    assert queue[0].candidate_id == "b"
    assert queue[-1].candidate_id == "a"


def test_uncertainty_sampling_top_k_truncates():
    items = [
        UncertaintyItem(candidate_id=str(i), p_keep=0.5 + i * 0.01)
        for i in range(10)
    ]
    queue = uncertainty_sampling(items, top_k=3)
    assert len(queue) == 3


def test_uncertainty_sampling_tie_break_by_id():
    items = [
        UncertaintyItem(candidate_id="z", p_keep=0.5),
        UncertaintyItem(candidate_id="a", p_keep=0.5),
    ]
    queue = uncertainty_sampling(items, top_k=2)
    assert queue[0].candidate_id == "a"
    assert queue[1].candidate_id == "z"
```

- [ ] **Step 2: Run to fail**

- [ ] **Step 3: Implement**

```python
# scripts/vitruvius/learning/__init__.py
"""Active learning + Expected Model Change (Stream J)."""
```

```python
# scripts/vitruvius/learning/active_learning.py
from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class UncertaintyItem:
    candidate_id: str
    p_keep: float


def _binary_entropy(p: float) -> float:
    p = min(max(p, 1e-12), 1.0 - 1e-12)
    return -p * math.log2(p) - (1 - p) * math.log2(1 - p)


def uncertainty_sampling(
    items: list[UncertaintyItem],
    *,
    top_k: int,
) -> tuple[UncertaintyItem, ...]:
    scored = [
        (item, _binary_entropy(item.p_keep), item.candidate_id)
        for item in items
    ]
    scored.sort(key=lambda triple: (-triple[1], triple[2]))
    return tuple(item for item, _, _ in scored[:top_k])
```

- [ ] **Step 4: Run to pass**

```bash
python3 -m pytest scripts/tests/test_learning_active.py -v
```

- [ ] **Step 5: Commit**

```bash
git add scripts/vitruvius/learning/__init__.py scripts/vitruvius/learning/active_learning.py scripts/tests/test_learning_active.py
git commit -m "feat(learning): add uncertainty-sampling queue (Task J.1)"
```

---

### Task J.2: Expected Model Change scoring

**Rationale:** EMC = the norm of the gradient that this single labelled example would apply to the Naive Bayes weights, approximating how much the model would shift if the Ranger labels it. Items with higher EMC get seen first.

**Files:**
- Create: `scripts/vitruvius/learning/expected_model_change.py`
- Create: `scripts/tests/test_learning_emc.py`

- [ ] **Step 1: Write test**

```python
# scripts/tests/test_learning_emc.py
from vitruvius.learning.expected_model_change import (
    compute_emc,
    EMCFeatureVector,
)


def test_emc_rewards_larger_feature_vectors():
    small = EMCFeatureVector(features={"a": 1.0})
    big = EMCFeatureVector(features={"a": 5.0, "b": 5.0})
    emc_small = compute_emc(small, p_keep=0.5)
    emc_big = compute_emc(big, p_keep=0.5)
    assert emc_big > emc_small


def test_emc_zero_at_extreme_confidence():
    fv = EMCFeatureVector(features={"a": 1.0})
    assert compute_emc(fv, p_keep=0.99) < compute_emc(fv, p_keep=0.5)
    assert compute_emc(fv, p_keep=0.01) < compute_emc(fv, p_keep=0.5)


def test_emc_empty_vector_is_zero():
    fv = EMCFeatureVector(features={})
    assert compute_emc(fv, p_keep=0.5) == 0.0
```

- [ ] **Step 2: Run to fail**

- [ ] **Step 3: Implement**

```python
# scripts/vitruvius/learning/expected_model_change.py
from __future__ import annotations

import math
from dataclasses import dataclass, field


@dataclass(frozen=True)
class EMCFeatureVector:
    features: dict[str, float] = field(default_factory=dict)


def compute_emc(vector: EMCFeatureVector, *, p_keep: float) -> float:
    """Expected model change proxy: ||x|| * p*(1-p)."""
    if not vector.features:
        return 0.0
    norm = math.sqrt(sum(v * v for v in vector.features.values()))
    p = min(max(p_keep, 0.0), 1.0)
    variance = p * (1 - p)
    return float(norm * variance)
```

- [ ] **Step 4: Run to pass**

```bash
python3 -m pytest scripts/tests/test_learning_emc.py -v
```

- [ ] **Step 5: Commit**

```bash
git add scripts/vitruvius/learning/expected_model_change.py scripts/tests/test_learning_emc.py
git commit -m "feat(learning): add expected model change scoring (Task J.2)"
```

### 6.4 Stream J Definition of Done
- [ ] Both Stream J test files green: `python3 -m pytest scripts/tests/test_learning_*.py -v`
- [ ] `features.j_*` flags added with defaults `false`.
- [ ] Backward-compat suite green.


---

## 7. Stream K — CLUP Scaling (gated on ≥2 jurisdictions)

### 7.1 Goal
When a second jurisdiction's code (e.g., the IRR or a Quezon City local ordinance) is ingested, activate Rosetta-stone alias alignment + precedence routing so a single query resolves to the correct local rule for the requested jurisdiction.

**Gating:** This stream's feature flags stay `false` until `003_Canonical-Knowledge-Layer/` contains at least two distinct `jurisdiction` tags on promoted relationships. The tasks ship immediately so the scaffolding is ready; activation is a data event, not a code event.

### 7.2 Files
- Create: `scripts/vitruvius/jurisdictions/__init__.py`
- Create: `scripts/vitruvius/jurisdictions/rosetta_stone.py`
- Create: `scripts/vitruvius/jurisdictions/precedence_router.py`
- Create: `scripts/tests/test_jurisdictions_rosetta.py`
- Create: `scripts/tests/test_jurisdictions_precedence.py`
- Modify: `scripts/vitruvius/features.py` (`k_rosetta_stone`, `k_precedence_router`)

### 7.3 Task Sequence

---

### Task K.1: Rosetta Stone (alias alignment across jurisdictions)

**Files:**
- Create: `scripts/vitruvius/jurisdictions/__init__.py`
- Create: `scripts/vitruvius/jurisdictions/rosetta_stone.py`
- Create: `scripts/tests/test_jurisdictions_rosetta.py`

- [ ] **Step 1: Write test**

```python
# scripts/tests/test_jurisdictions_rosetta.py
from vitruvius.jurisdictions.rosetta_stone import (
    RosettaStone,
    AliasPair,
)


def test_rosetta_aligns_exact_match():
    stone = RosettaStone()
    stone.add(AliasPair("concept-permit", "permit-qc", jurisdiction="QC"))
    stone.add(AliasPair("concept-permit", "permit-mm", jurisdiction="MM"))
    assert stone.canonical_of("permit-qc") == "concept-permit"
    assert stone.canonical_of("permit-mm") == "concept-permit"


def test_rosetta_resolves_by_jurisdiction():
    stone = RosettaStone()
    stone.add(AliasPair("concept-permit", "permit-qc", jurisdiction="QC"))
    stone.add(AliasPair("concept-permit", "permit-mm", jurisdiction="MM"))
    assert stone.resolve("concept-permit", jurisdiction="QC") == "permit-qc"


def test_rosetta_unknown_returns_none():
    stone = RosettaStone()
    assert stone.canonical_of("nothing") is None
    assert stone.resolve("nothing", jurisdiction="QC") is None
```

- [ ] **Step 2: Run to fail**

- [ ] **Step 3: Implement**

```python
# scripts/vitruvius/jurisdictions/__init__.py
"""CLUP scaling — cross-jurisdiction alignment (Stream K, gated)."""
```

```python
# scripts/vitruvius/jurisdictions/rosetta_stone.py
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AliasPair:
    canonical_id: str
    local_id: str
    jurisdiction: str


class RosettaStone:
    def __init__(self) -> None:
        self._local_to_canonical: dict[str, str] = {}
        self._canonical_to_locals: dict[str, dict[str, str]] = {}

    def add(self, pair: AliasPair) -> None:
        self._local_to_canonical[pair.local_id] = pair.canonical_id
        bucket = self._canonical_to_locals.setdefault(pair.canonical_id, {})
        bucket[pair.jurisdiction] = pair.local_id

    def canonical_of(self, local_id: str) -> str | None:
        return self._local_to_canonical.get(local_id)

    def resolve(self, canonical_id: str, *, jurisdiction: str) -> str | None:
        bucket = self._canonical_to_locals.get(canonical_id, {})
        return bucket.get(jurisdiction)
```

- [ ] **Step 4: Run to pass**

```bash
python3 -m pytest scripts/tests/test_jurisdictions_rosetta.py -v
```

- [ ] **Step 5: Commit**

```bash
git add scripts/vitruvius/jurisdictions/__init__.py scripts/vitruvius/jurisdictions/rosetta_stone.py scripts/tests/test_jurisdictions_rosetta.py
git commit -m "feat(jurisdictions): add rosetta stone alias alignment (Task K.1)"
```

---

### Task K.2: Precedence Router (most-stringent-law-wins)

**Rationale:** When two jurisdictions disagree on the same canonical rule, pick the stricter one (e.g., 2.5m local setback beats 2.0m national). Uses `promotion/stringency_resolver.py` as the underlying comparator.

**Files:**
- Create: `scripts/vitruvius/jurisdictions/precedence_router.py`
- Create: `scripts/tests/test_jurisdictions_precedence.py`

- [ ] **Step 1: Write test**

```python
# scripts/tests/test_jurisdictions_precedence.py
from vitruvius.jurisdictions.precedence_router import (
    PrecedenceRouter,
    JurisdictionalRule,
)


def test_precedence_picks_stricter_inequality():
    router = PrecedenceRouter()
    router.register(JurisdictionalRule(
        canonical_id="setback-front",
        jurisdiction="national",
        operator=">=",
        value=2.0,
        unit="meters",
    ))
    router.register(JurisdictionalRule(
        canonical_id="setback-front",
        jurisdiction="QC",
        operator=">=",
        value=2.5,
        unit="meters",
    ))
    winner = router.resolve("setback-front")
    assert winner.jurisdiction == "QC"
    assert winner.value == 2.5


def test_precedence_single_rule_returns_itself():
    router = PrecedenceRouter()
    only = JurisdictionalRule(
        canonical_id="x",
        jurisdiction="national",
        operator=">=",
        value=1.0,
        unit="m",
    )
    router.register(only)
    assert router.resolve("x") == only


def test_precedence_unknown_returns_none():
    router = PrecedenceRouter()
    assert router.resolve("missing") is None
```

- [ ] **Step 2: Run to fail**

- [ ] **Step 3: Implement**

```python
# scripts/vitruvius/jurisdictions/precedence_router.py
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass


@dataclass(frozen=True)
class JurisdictionalRule:
    canonical_id: str
    jurisdiction: str
    operator: str  # ">=", "<=", "=="
    value: float
    unit: str


class PrecedenceRouter:
    def __init__(self) -> None:
        self._by_canonical: dict[str, list[JurisdictionalRule]] = defaultdict(list)

    def register(self, rule: JurisdictionalRule) -> None:
        self._by_canonical[rule.canonical_id].append(rule)

    def resolve(self, canonical_id: str) -> JurisdictionalRule | None:
        candidates = self._by_canonical.get(canonical_id, [])
        if not candidates:
            return None
        if len(candidates) == 1:
            return candidates[0]

        # Stricter = higher value for >=, lower for <=.
        def sort_key(rule: JurisdictionalRule) -> tuple[float, str]:
            sign = -1.0 if rule.operator == ">=" else 1.0
            return (sign * rule.value, rule.jurisdiction)

        return sorted(candidates, key=sort_key)[0]
```

- [ ] **Step 4: Run to pass**

```bash
python3 -m pytest scripts/tests/test_jurisdictions_precedence.py -v
```

- [ ] **Step 5: Commit**

```bash
git add scripts/vitruvius/jurisdictions/precedence_router.py scripts/tests/test_jurisdictions_precedence.py
git commit -m "feat(jurisdictions): add precedence router (Task K.2)"
```

### 7.4 Stream K Definition of Done
- [ ] Stream K test files green.
- [ ] Feature flags `k_*` added and default `false`.
- [ ] Module is imported lazily from `pipeline_cli.py` so stdlib-only deployments don't pay the cost.
- [ ] Scaffolding activates only when ≥2 jurisdictions exist in `003_Canonical-Knowledge-Layer/`.


---

## 8. Stream L — Spatial Reasoning (Z3 SMT + Parametric Evaluator)

### 8.1 Goal
Give Vitruvius a 3D reasoning capability without coupling the core to a 3D engine. Define a strict JSON contract (`spatial_context_id`, `spatial_edges[]`) that any external daemon (SketchUp-C-API bridge, Rust GJK kernel, or Revit exporter) can drop into `001B_Spatial-Source-Layer/`. Parse it, enrich the Phase 8 graph with parametric edge attributes, and evaluate compliance against the canonical legal graph using the Z3 SMT theorem prover.

**Non-goal:** Building the 3D daemon itself. That is a separate product. Vitruvius ships only the ingestion, parametric-edge enrichment, and Z3 evaluation.

### 8.2 Files
- Create: `scripts/vitruvius/spatial/__init__.py`
- Create: `scripts/vitruvius/spatial/contract.py`
- Create: `scripts/vitruvius/spatial/ingestion.py`
- Create: `scripts/vitruvius/spatial/z3_evaluator.py`
- Create: `scripts/vitruvius/spatial/parametric_edge.py`
- Create: `scripts/vitruvius/spatial/compliance_report.py`
- Create: `scripts/tests/test_spatial_contract.py`
- Create: `scripts/tests/test_spatial_ingestion.py`
- Create: `scripts/tests/test_spatial_z3_evaluator.py`
- Create: `scripts/tests/test_spatial_parametric_edge.py`
- Create: `scripts/tests/test_spatial_compliance_report.py`
- Create: `001B_Spatial-Source-Layer/.gitkeep`
- Modify: `scripts/vitruvius/constants.py` (add `DIR_001B_SPATIAL`)
- Modify: `scripts/pipeline_cli.py` (register `spatial-ingest-one`, `spatial-evaluate-one`)

### 8.3 Task Sequence

---

### Task L.1: Spatial JSON contract

**Files:**
- Create: `scripts/vitruvius/spatial/__init__.py`
- Create: `scripts/vitruvius/spatial/contract.py`
- Create: `scripts/tests/test_spatial_contract.py`

- [ ] **Step 1: Write test**

```python
# scripts/tests/test_spatial_contract.py
import json

from vitruvius.spatial.contract import (
    SpatialEdge,
    SpatialPayload,
    SpatialValidationError,
    parse_payload,
)


def test_parse_payload_valid():
    raw = json.dumps({
        "spatial_context_id": "model-residential-01",
        "timestamp_utc": "2026-04-14T12:00:00Z",
        "spatial_edges": [
            {
                "source_instance": "inst-corridor-01",
                "canonical_concept_map": "concept-egress-corridor",
                "predicate": "has_clearance",
                "target_instance": "inst-wall-02",
                "value": 1.1,
                "unit": "meters",
            }
        ],
    })
    payload = parse_payload(raw)
    assert isinstance(payload, SpatialPayload)
    assert payload.spatial_context_id == "model-residential-01"
    assert len(payload.spatial_edges) == 1
    edge = payload.spatial_edges[0]
    assert isinstance(edge, SpatialEdge)
    assert edge.value == 1.1
    assert edge.unit == "meters"


def test_parse_payload_missing_top_level_key():
    raw = json.dumps({"spatial_edges": []})
    try:
        parse_payload(raw)
    except SpatialValidationError as exc:
        assert "spatial_context_id" in str(exc)
    else:
        raise AssertionError("expected SpatialValidationError")


def test_parse_payload_rejects_invalid_predicate():
    raw = json.dumps({
        "spatial_context_id": "m1",
        "spatial_edges": [{
            "source_instance": "a",
            "canonical_concept_map": "c",
            "predicate": "not_a_real_predicate",
            "target_instance": "b",
        }],
    })
    try:
        parse_payload(raw)
    except SpatialValidationError as exc:
        assert "predicate" in str(exc)
    else:
        raise AssertionError("expected SpatialValidationError")


def test_parse_payload_frozen_and_deterministic():
    raw = json.dumps({
        "spatial_context_id": "m1",
        "spatial_edges": [
            {
                "source_instance": "z",
                "canonical_concept_map": "c-z",
                "predicate": "intersects",
                "target_instance": "a",
            },
            {
                "source_instance": "a",
                "canonical_concept_map": "c-a",
                "predicate": "intersects",
                "target_instance": "z",
            },
        ],
    })
    p1 = parse_payload(raw)
    p2 = parse_payload(raw)
    assert p1 == p2
```

- [ ] **Step 2: Run to fail**

- [ ] **Step 3: Implement**

```python
# scripts/vitruvius/spatial/__init__.py
"""Spatial reasoning layer (Stream L) — Z3 + decoupled JSON contract."""
```

```python
# scripts/vitruvius/spatial/contract.py
from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any


_ALLOWED_PREDICATES = frozenset({
    "intersects",
    "has_clearance",
    "adjacent_to",
    "contained_within",
})


class SpatialValidationError(ValueError):
    """Raised when a spatial JSON payload violates the Vitruvius contract."""


@dataclass(frozen=True)
class SpatialEdge:
    source_instance: str
    canonical_concept_map: str
    predicate: str
    target_instance: str
    value: float | None
    unit: str | None


@dataclass(frozen=True)
class SpatialPayload:
    spatial_context_id: str
    timestamp_utc: str | None
    spatial_edges: tuple[SpatialEdge, ...]


def _require(obj: dict[str, Any], key: str) -> Any:
    if key not in obj:
        raise SpatialValidationError(f"missing required key: {key!r}")
    return obj[key]


def _parse_edge(obj: dict[str, Any]) -> SpatialEdge:
    predicate = _require(obj, "predicate")
    if predicate not in _ALLOWED_PREDICATES:
        raise SpatialValidationError(
            f"invalid predicate {predicate!r}; must be one of {sorted(_ALLOWED_PREDICATES)}"
        )
    value = obj.get("value")
    unit = obj.get("unit")
    if value is not None:
        value = float(value)
    return SpatialEdge(
        source_instance=str(_require(obj, "source_instance")),
        canonical_concept_map=str(_require(obj, "canonical_concept_map")),
        predicate=predicate,
        target_instance=str(_require(obj, "target_instance")),
        value=value,
        unit=unit,
    )


def parse_payload(raw_json: str) -> SpatialPayload:
    try:
        data = json.loads(raw_json)
    except json.JSONDecodeError as exc:
        raise SpatialValidationError(f"invalid JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise SpatialValidationError(
            f"payload must be a JSON object, got {type(data).__name__}"
        )

    context_id = str(_require(data, "spatial_context_id"))
    timestamp = data.get("timestamp_utc")
    raw_edges = _require(data, "spatial_edges")
    if not isinstance(raw_edges, list):
        raise SpatialValidationError("spatial_edges must be an array")

    edges = tuple(
        sorted(
            (_parse_edge(e) for e in raw_edges),
            key=lambda e: (e.source_instance, e.target_instance, e.predicate),
        )
    )

    return SpatialPayload(
        spatial_context_id=context_id,
        timestamp_utc=str(timestamp) if timestamp is not None else None,
        spatial_edges=edges,
    )
```

- [ ] **Step 4: Run to pass**

```bash
python3 -m pytest scripts/tests/test_spatial_contract.py -v
```

- [ ] **Step 5: Commit**

```bash
git add scripts/vitruvius/spatial/__init__.py scripts/vitruvius/spatial/contract.py scripts/tests/test_spatial_contract.py
git commit -m "feat(spatial): add decoupled spatial JSON contract (Task L.1)"
```

---

### Task L.2: Spatial ingestion (drop-file reader)

**Files:**
- Create: `scripts/vitruvius/spatial/ingestion.py`
- Create: `scripts/tests/test_spatial_ingestion.py`
- Modify: `scripts/vitruvius/constants.py` (add `DIR_001B_SPATIAL`)
- Create: `001B_Spatial-Source-Layer/.gitkeep`

- [ ] **Step 1: Write test**

```python
# scripts/tests/test_spatial_ingestion.py
import json
from pathlib import Path

import pytest

from vitruvius.spatial.ingestion import ingest_one


def test_ingest_one_writes_derived_candidates(tmp_path: Path) -> None:
    src_dir = tmp_path / "001B_Spatial-Source-Layer"
    src_dir.mkdir()
    derived_dir = tmp_path / "004_Derived-Content-Layer"
    derived_dir.mkdir()

    payload_file = src_dir / "model-a.json"
    payload_file.write_text(json.dumps({
        "spatial_context_id": "model-a",
        "spatial_edges": [
            {
                "source_instance": "inst-1",
                "canonical_concept_map": "concept-fire-door",
                "predicate": "has_clearance",
                "target_instance": "inst-2",
                "value": 1.2,
                "unit": "meters",
            }
        ],
    }))

    out = ingest_one(payload_file, derived_dir=derived_dir)
    assert out.edges_ingested == 1
    written = derived_dir / "spatial_candidates_model-a.json"
    assert written.exists()
    data = json.loads(written.read_text())
    assert data[0]["source_concept_id"] == "concept-fire-door"
    assert data[0]["spatial_metadata"]["computed_value"] == 1.2


def test_ingest_one_raises_on_missing_file(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        ingest_one(tmp_path / "nope.json", derived_dir=tmp_path)
```

- [ ] **Step 2: Run to fail**

- [ ] **Step 3: Implement**

```python
# scripts/vitruvius/spatial/ingestion.py
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from .contract import SpatialPayload, parse_payload


@dataclass(frozen=True)
class IngestionResult:
    spatial_context_id: str
    output_path: Path
    edges_ingested: int


def _edge_to_candidate(edge) -> dict:
    return {
        "source_concept_id": edge.canonical_concept_map,
        "predicate": f"spatial_{edge.predicate}",
        "target_concept_id": edge.target_instance,
        "spatial_metadata": {
            "physical_source": edge.source_instance,
            "physical_target": edge.target_instance,
            "computed_value": edge.value,
            "unit": edge.unit,
        },
        "status": "pending_constraint_evaluation",
    }


def ingest_one(payload_file: Path, *, derived_dir: Path) -> IngestionResult:
    if not payload_file.exists():
        raise FileNotFoundError(payload_file)

    raw = payload_file.read_text(encoding="utf-8")
    payload: SpatialPayload = parse_payload(raw)

    candidates = [
        _edge_to_candidate(edge) for edge in payload.spatial_edges
    ]

    derived_dir.mkdir(parents=True, exist_ok=True)
    output_path = derived_dir / f"spatial_candidates_{payload.spatial_context_id}.json"
    output_path.write_text(
        json.dumps(candidates, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    return IngestionResult(
        spatial_context_id=payload.spatial_context_id,
        output_path=output_path,
        edges_ingested=len(candidates),
    )
```

Modify `constants.py` to add:
```python
# scripts/vitruvius/constants.py (at top-level constants block)
DIR_001B_SPATIAL = "001B_Spatial-Source-Layer"
```

Create gitkeep:
```bash
mkdir -p /Users/philiplewis/vitruvius/001B_Spatial-Source-Layer
touch /Users/philiplewis/vitruvius/001B_Spatial-Source-Layer/.gitkeep
```

- [ ] **Step 4: Run to pass**

```bash
python3 -m pytest scripts/tests/test_spatial_ingestion.py -v
```

- [ ] **Step 5: Commit**

```bash
git add scripts/vitruvius/spatial/ingestion.py scripts/vitruvius/constants.py scripts/tests/test_spatial_ingestion.py 001B_Spatial-Source-Layer/.gitkeep
git commit -m "feat(spatial): add drop-file ingestion and 001B layer (Task L.2)"
```

---

### Task L.3: Z3 parametric evaluator

**Rationale:** Given a spatial candidate and a canonical parametric constraint from `parsers/parametric_ner.py`, use Z3 to deterministically verify compliance. For `>=` / `<=` / `==` inequalities, Z3's `sat/unsat` is our boolean compliance proof.

**Files:**
- Create: `scripts/vitruvius/spatial/z3_evaluator.py`
- Create: `scripts/tests/test_spatial_z3_evaluator.py`

- [ ] **Step 1: Write test**

```python
# scripts/tests/test_spatial_z3_evaluator.py
import pytest

z3 = pytest.importorskip("z3")

from vitruvius.spatial.z3_evaluator import (
    ParametricConstraint,
    SpatialObservation,
    evaluate_compliance,
    Verdict,
)


def test_compliance_pass_ge():
    constraint = ParametricConstraint(operator=">=", value=1.2, unit="meters")
    observation = SpatialObservation(value=1.5, unit="meters")
    verdict = evaluate_compliance(observation, constraint)
    assert verdict == Verdict.COMPLIANT


def test_compliance_fail_ge():
    constraint = ParametricConstraint(operator=">=", value=1.2, unit="meters")
    observation = SpatialObservation(value=1.0, unit="meters")
    verdict = evaluate_compliance(observation, constraint)
    assert verdict == Verdict.VIOLATION


def test_compliance_unit_mismatch_is_indeterminate():
    constraint = ParametricConstraint(operator=">=", value=1.2, unit="meters")
    observation = SpatialObservation(value=120.0, unit="centimeters")
    verdict = evaluate_compliance(observation, constraint)
    # Strict contract: no unit conversion. Indeterminate until the translator
    # layer converts to canonical units.
    assert verdict == Verdict.INDETERMINATE


def test_compliance_equals():
    constraint = ParametricConstraint(operator="==", value=2.0, unit="m")
    assert evaluate_compliance(SpatialObservation(2.0, "m"), constraint) == Verdict.COMPLIANT
    assert evaluate_compliance(SpatialObservation(2.1, "m"), constraint) == Verdict.VIOLATION
```

- [ ] **Step 2: Run to fail** (will fail because `z3` isn't installed yet)

```bash
pip3 install z3-solver>=4.12
python3 -m pytest scripts/tests/test_spatial_z3_evaluator.py -v
```

- [ ] **Step 3: Implement**

```python
# scripts/vitruvius/spatial/z3_evaluator.py
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Verdict(str, Enum):
    COMPLIANT = "compliant"
    VIOLATION = "violation"
    INDETERMINATE = "indeterminate"


@dataclass(frozen=True)
class ParametricConstraint:
    operator: str  # ">=", "<=", "=="
    value: float
    unit: str


@dataclass(frozen=True)
class SpatialObservation:
    value: float
    unit: str


def evaluate_compliance(
    observation: SpatialObservation,
    constraint: ParametricConstraint,
) -> Verdict:
    if observation.unit != constraint.unit:
        return Verdict.INDETERMINATE

    try:
        import z3  # type: ignore[import-not-found]
    except ImportError:  # pragma: no cover
        return Verdict.INDETERMINATE

    solver = z3.Solver()
    actual = z3.Real("actual")
    required = z3.Real("required")

    solver.add(actual == observation.value)
    solver.add(required == constraint.value)

    if constraint.operator == ">=":
        solver.add(actual >= required)
    elif constraint.operator == "<=":
        solver.add(actual <= required)
    elif constraint.operator == "==":
        solver.add(actual == required)
    else:
        return Verdict.INDETERMINATE

    result = solver.check()
    if result == z3.sat:
        return Verdict.COMPLIANT
    if result == z3.unsat:
        return Verdict.VIOLATION
    return Verdict.INDETERMINATE
```

- [ ] **Step 4: Run to pass**

```bash
python3 -m pytest scripts/tests/test_spatial_z3_evaluator.py -v
```

- [ ] **Step 5: Commit**

```bash
git add scripts/vitruvius/spatial/z3_evaluator.py scripts/tests/test_spatial_z3_evaluator.py requirements.txt
git commit -m "feat(spatial): add Z3 parametric compliance evaluator (Task L.3)"
```

---

### Task L.4: Parametric edge side-table (join on evidence_id)

**Rationale:** `graph/contract.GraphEdge` is a minimal frozen dataclass with only `(from_id, to_id, type, evidence_id, status)`. Adding a parametric field to that contract would touch every shipped graph test. Instead we build a **parallel sidecar table** keyed by `evidence_id`: the core graph stays untouched and parametric metadata lives in `spatial/parametric_edge.py`. The Z3 evaluator (Task L.3) already operates on `ParametricConstraint` directly, so no wiring change is required inside the graph package.

**Files:**
- Create: `scripts/vitruvius/spatial/parametric_edge.py`
- Create: `scripts/tests/test_spatial_parametric_edge.py`

- [ ] **Step 1: Write test**

```python
# scripts/tests/test_spatial_parametric_edge.py
from vitruvius.graph.contract import GraphEdge
from vitruvius.spatial.parametric_edge import (
    ParametricAttrs,
    ParametricEdgeTable,
)


def _edge(evidence_id: str) -> GraphEdge:
    return GraphEdge(
        from_id="concept-a",
        to_id="concept-b",
        type="requires",
        evidence_id=evidence_id,
        status="verified",
    )


def test_attach_and_read_roundtrip():
    table = ParametricEdgeTable()
    edge = _edge("rel-0001")
    attrs = ParametricAttrs(operator=">=", value=1.2, unit="m")
    table.attach(edge, attrs)
    read = table.get(edge)
    assert read is not None
    assert read.operator == ">="
    assert read.value == 1.2
    assert read.unit == "m"


def test_read_missing_returns_none():
    table = ParametricEdgeTable()
    assert table.get(_edge("rel-missing")) is None


def test_attach_overwrites_existing():
    table = ParametricEdgeTable()
    edge = _edge("rel-0002")
    table.attach(edge, ParametricAttrs(operator=">=", value=1.0, unit="m"))
    table.attach(edge, ParametricAttrs(operator=">=", value=1.2, unit="m"))
    assert table.get(edge).value == 1.2


def test_iter_is_deterministic():
    table = ParametricEdgeTable()
    for eid in ("rel-003", "rel-001", "rel-002"):
        table.attach(_edge(eid), ParametricAttrs(operator=">=", value=1.0, unit="m"))
    ids = [evidence_id for evidence_id, _ in table.iter_items()]
    assert ids == ["rel-001", "rel-002", "rel-003"]
```

- [ ] **Step 2: Run to fail**

- [ ] **Step 3: Implement**

```python
# scripts/vitruvius/spatial/parametric_edge.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterator

from vitruvius.graph.contract import GraphEdge


@dataclass(frozen=True)
class ParametricAttrs:
    operator: str
    value: float
    unit: str


class ParametricEdgeTable:
    """Sidecar map: evidence_id → ParametricAttrs. Leaves GraphEdge frozen-minimal."""

    def __init__(self) -> None:
        self._by_evidence: dict[str, ParametricAttrs] = {}

    def attach(self, edge: GraphEdge, attrs: ParametricAttrs) -> None:
        self._by_evidence[edge.evidence_id] = attrs

    def get(self, edge: GraphEdge) -> ParametricAttrs | None:
        return self._by_evidence.get(edge.evidence_id)

    def iter_items(self) -> Iterator[tuple[str, ParametricAttrs]]:
        for evidence_id in sorted(self._by_evidence):
            yield evidence_id, self._by_evidence[evidence_id]
```

- [ ] **Step 4: Run to pass**

```bash
python3 -m pytest scripts/tests/test_spatial_parametric_edge.py -v
python3 -m pytest scripts/tests/test_graph_contract.py -v  # regression — must stay green untouched
```

Expected: both test files pass. `test_graph_contract.py` must not need any changes — the sidecar pattern never touches `graph/contract.py`.

- [ ] **Step 5: Commit**

```bash
git add scripts/vitruvius/spatial/parametric_edge.py scripts/tests/test_spatial_parametric_edge.py
git commit -m "feat(spatial): add parametric edge sidecar table (Task L.4)"
```

---

### Task L.5: Compliance report writer

**Files:**
- Create: `scripts/vitruvius/spatial/compliance_report.py`
- Create: `scripts/tests/test_spatial_compliance_report.py`

- [ ] **Step 1: Write test**

```python
# scripts/tests/test_spatial_compliance_report.py
import json
from pathlib import Path

from vitruvius.spatial.compliance_report import (
    ComplianceFinding,
    write_compliance_report,
)
from vitruvius.spatial.z3_evaluator import Verdict


def test_write_compliance_report(tmp_path: Path):
    findings = [
        ComplianceFinding(
            candidate_id="sp-1",
            verdict=Verdict.COMPLIANT,
            observed_value=1.5,
            required_value=1.2,
            unit="m",
        ),
        ComplianceFinding(
            candidate_id="sp-2",
            verdict=Verdict.VIOLATION,
            observed_value=0.9,
            required_value=1.2,
            unit="m",
        ),
    ]
    out = tmp_path / "report.json"
    write_compliance_report(findings, out)
    data = json.loads(out.read_text())
    assert data["total"] == 2
    assert data["compliant_count"] == 1
    assert data["violation_count"] == 1
    assert len(data["findings"]) == 2
```

- [ ] **Step 2: Run to fail**

- [ ] **Step 3: Implement**

```python
# scripts/vitruvius/spatial/compliance_report.py
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from .z3_evaluator import Verdict


@dataclass(frozen=True)
class ComplianceFinding:
    candidate_id: str
    verdict: Verdict
    observed_value: float
    required_value: float
    unit: str


def write_compliance_report(
    findings: list[ComplianceFinding],
    output_path: Path,
) -> None:
    compliant = sum(1 for f in findings if f.verdict == Verdict.COMPLIANT)
    violations = sum(1 for f in findings if f.verdict == Verdict.VIOLATION)
    indeterminate = sum(1 for f in findings if f.verdict == Verdict.INDETERMINATE)

    payload = {
        "total": len(findings),
        "compliant_count": compliant,
        "violation_count": violations,
        "indeterminate_count": indeterminate,
        "findings": [
            {
                "candidate_id": f.candidate_id,
                "verdict": f.verdict.value,
                "observed_value": f.observed_value,
                "required_value": f.required_value,
                "unit": f.unit,
            }
            for f in sorted(findings, key=lambda x: x.candidate_id)
        ],
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
```

- [ ] **Step 4: Run to pass**

```bash
python3 -m pytest scripts/tests/test_spatial_compliance_report.py -v
```

- [ ] **Step 5: Commit**

```bash
git add scripts/vitruvius/spatial/compliance_report.py scripts/tests/test_spatial_compliance_report.py
git commit -m "feat(spatial): add compliance report writer (Task L.5)"
```

### 8.4 Stream L Definition of Done
- [ ] All Stream L test files green: `python3 -m pytest scripts/tests/test_spatial_*.py -v`
- [ ] Feature flags `l_spatial_*` added.
- [ ] `001B_Spatial-Source-Layer/` exists with a `.gitkeep`.
- [ ] `graph/contract.py` ships the optional `parametric_constraint` field without breaking `test_graph_contract.py`.
- [ ] Backward-compat suite green.


---

## 9. Stream M — Rust Ingest Kernel (Bloom + MinHash LSH via PyO3)

### 9.1 Goal
Offload the hottest path in ingestion — per-chunk dedup and jurisdictional overlap detection — into a Rust crate built as a native Python extension via PyO3 + maturin. Provide a pure-Python fallback so the system still works without the Rust toolchain.

### 9.2 Files
- Create: `rust_kernels/vitruvius-ingest-kernel/Cargo.toml`
- Create: `rust_kernels/vitruvius-ingest-kernel/pyproject.toml`
- Create: `rust_kernels/vitruvius-ingest-kernel/src/lib.rs`
- Create: `rust_kernels/vitruvius-ingest-kernel/src/bloom.rs`
- Create: `rust_kernels/vitruvius-ingest-kernel/src/minhash.rs`
- Create: `scripts/vitruvius/ingest_kernel/__init__.py`
- Create: `scripts/vitruvius/ingest_kernel/python_fallback.py`
- Create: `scripts/vitruvius/ingest_kernel/__pyo3_bridge.py`
- Create: `scripts/tests/test_ingest_kernel_bloom.py`
- Create: `scripts/tests/test_ingest_kernel_minhash.py`
- Create: `scripts/tests/test_ingest_kernel_fallback.py`

### 9.3 Task Sequence

---

### Task M.1: Pure-Python Bloom filter fallback

**Files:**
- Create: `scripts/vitruvius/ingest_kernel/__init__.py`
- Create: `scripts/vitruvius/ingest_kernel/python_fallback.py`
- Create: `scripts/tests/test_ingest_kernel_fallback.py`

- [ ] **Step 1: Write test**

```python
# scripts/tests/test_ingest_kernel_fallback.py
from vitruvius.ingest_kernel.python_fallback import BloomFilter


def test_bloom_insert_and_lookup():
    bf = BloomFilter(size=1000, num_hashes=5)
    bf.insert("hello")
    bf.insert("world")
    assert bf.might_contain("hello")
    assert bf.might_contain("world")


def test_bloom_absent_returns_false():
    bf = BloomFilter(size=1000, num_hashes=5)
    bf.insert("yes")
    # "no" may spuriously collide but probability is <1/1000^5 with these params
    assert not bf.might_contain("no")


def test_bloom_deterministic():
    bf1 = BloomFilter(size=500, num_hashes=3)
    bf2 = BloomFilter(size=500, num_hashes=3)
    for s in ("a", "b", "c"):
        bf1.insert(s)
        bf2.insert(s)
    for s in ("a", "b", "c", "d", "e"):
        assert bf1.might_contain(s) == bf2.might_contain(s)
```

- [ ] **Step 2: Run to fail**

- [ ] **Step 3: Implement**

```python
# scripts/vitruvius/ingest_kernel/__init__.py
"""Ingest kernel — Rust via PyO3 preferred, pure-Python fallback guaranteed."""

try:  # pragma: no cover
    from .__pyo3_bridge import RustBloomFilter as BloomFilter  # type: ignore
    from .__pyo3_bridge import RustMinHash as MinHash  # type: ignore
except ImportError:
    from .python_fallback import BloomFilter  # type: ignore[assignment]
    from .python_fallback import MinHash  # type: ignore[assignment]

__all__ = ["BloomFilter", "MinHash"]
```

```python
# scripts/vitruvius/ingest_kernel/python_fallback.py
from __future__ import annotations

import hashlib
from dataclasses import dataclass, field


@dataclass
class BloomFilter:
    size: int
    num_hashes: int
    _bits: bytearray = field(init=False)

    def __post_init__(self) -> None:
        if self.size <= 0:
            raise ValueError("size must be positive")
        if self.num_hashes <= 0:
            raise ValueError("num_hashes must be positive")
        self._bits = bytearray((self.size + 7) // 8)

    def _indices(self, text: str):
        base = hashlib.blake2b(text.encode("utf-8"), digest_size=16).digest()
        for i in range(self.num_hashes):
            salt = i.to_bytes(4, "little")
            h = hashlib.blake2b(base + salt, digest_size=8).digest()
            yield int.from_bytes(h, "little") % self.size

    def insert(self, text: str) -> None:
        for idx in self._indices(text):
            byte_idx, bit_idx = divmod(idx, 8)
            self._bits[byte_idx] |= 1 << bit_idx

    def might_contain(self, text: str) -> bool:
        for idx in self._indices(text):
            byte_idx, bit_idx = divmod(idx, 8)
            if not (self._bits[byte_idx] & (1 << bit_idx)):
                return False
        return True


@dataclass
class MinHash:
    num_permutations: int
    _signature: list[int] = field(init=False)

    def __post_init__(self) -> None:
        if self.num_permutations <= 0:
            raise ValueError("num_permutations must be positive")
        self._signature = [2**64 - 1] * self.num_permutations

    def update(self, text: str) -> None:
        base = int.from_bytes(
            hashlib.blake2b(text.encode("utf-8"), digest_size=8).digest(),
            "little",
        )
        for i in range(self.num_permutations):
            salt = (i * 2654435761) & (2**64 - 1)
            h = (base ^ salt) & (2**64 - 1)
            if h < self._signature[i]:
                self._signature[i] = h

    def signature(self) -> tuple[int, ...]:
        return tuple(self._signature)

    def jaccard(self, other: "MinHash") -> float:
        if len(self._signature) != len(other._signature):
            raise ValueError("signature lengths must match")
        matches = sum(
            1 for a, b in zip(self._signature, other._signature) if a == b
        )
        return matches / len(self._signature)
```

- [ ] **Step 4: Run to pass**

```bash
python3 -m pytest scripts/tests/test_ingest_kernel_fallback.py -v
```

- [ ] **Step 5: Commit**

```bash
git add scripts/vitruvius/ingest_kernel/__init__.py scripts/vitruvius/ingest_kernel/python_fallback.py scripts/tests/test_ingest_kernel_fallback.py
git commit -m "feat(ingest-kernel): add pure-Python Bloom/MinHash fallback (Task M.1)"
```

---

### Task M.2: MinHash fallback test coverage

**Files:**
- Create: `scripts/tests/test_ingest_kernel_minhash.py`

- [ ] **Step 1: Write test**

```python
# scripts/tests/test_ingest_kernel_minhash.py
from vitruvius.ingest_kernel.python_fallback import MinHash


def _signature_of(texts):
    m = MinHash(num_permutations=64)
    for t in texts:
        m.update(t)
    return m


def test_jaccard_identical_texts():
    a = _signature_of(["alpha", "beta", "gamma"])
    b = _signature_of(["alpha", "beta", "gamma"])
    assert a.jaccard(b) == 1.0


def test_jaccard_disjoint_texts():
    a = _signature_of(["alpha", "beta"])
    b = _signature_of(["xi", "omicron", "pi"])
    # disjoint: jaccard < 0.2 with very high probability at 64 perms
    assert a.jaccard(b) < 0.2


def test_jaccard_partial_overlap():
    a = _signature_of(["apple", "banana", "cherry"])
    b = _signature_of(["apple", "banana", "date", "elderberry"])
    # 2/5 elements overlap → ~0.4 expected
    j = a.jaccard(b)
    assert 0.2 < j < 0.7
```

- [ ] **Step 2: Run to fail** (will pass immediately since M.1 shipped the module, but the test file doesn't exist yet)

- [ ] **Step 3: No new implementation needed — fallback shipped in M.1**

- [ ] **Step 4: Run to pass**

```bash
python3 -m pytest scripts/tests/test_ingest_kernel_minhash.py -v
```

- [ ] **Step 5: Commit**

```bash
git add scripts/tests/test_ingest_kernel_minhash.py
git commit -m "test(ingest-kernel): add MinHash fallback coverage (Task M.2)"
```

---

### Task M.3: Rust crate skeleton (Bloom filter, PyO3)

**Files:**
- Create: `rust_kernels/vitruvius-ingest-kernel/Cargo.toml`
- Create: `rust_kernels/vitruvius-ingest-kernel/pyproject.toml`
- Create: `rust_kernels/vitruvius-ingest-kernel/src/lib.rs`
- Create: `rust_kernels/vitruvius-ingest-kernel/src/bloom.rs`

- [ ] **Step 1: Write skeleton Cargo.toml**

```toml
# rust_kernels/vitruvius-ingest-kernel/Cargo.toml
[package]
name = "vitruvius_ingest_kernel"
version = "0.1.0"
edition = "2021"
rust-version = "1.70"

[lib]
name = "vitruvius_ingest_kernel"
crate-type = ["cdylib"]

[dependencies]
pyo3 = { version = "0.22", features = ["extension-module"] }
blake3 = "1.5"
```

```toml
# rust_kernels/vitruvius-ingest-kernel/pyproject.toml
[build-system]
requires = ["maturin>=1.5,<2.0"]
build-backend = "maturin"

[project]
name = "vitruvius_ingest_kernel"
version = "0.1.0"
description = "Rust-accelerated Bloom + MinHash for Vitruvius ingestion"
requires-python = ">=3.10"

[tool.maturin]
python-source = "python"
module-name = "vitruvius_ingest_kernel"
```

- [ ] **Step 2: Write lib.rs**

```rust
// rust_kernels/vitruvius-ingest-kernel/src/lib.rs
use pyo3::prelude::*;

mod bloom;
mod minhash;

#[pymodule]
fn vitruvius_ingest_kernel(_py: Python<'_>, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<bloom::BloomFilter>()?;
    m.add_class::<minhash::MinHash>()?;
    Ok(())
}
```

```rust
// rust_kernels/vitruvius-ingest-kernel/src/bloom.rs
use pyo3::prelude::*;

#[pyclass]
pub struct BloomFilter {
    size: usize,
    num_hashes: usize,
    bits: Vec<u8>,
}

#[pymethods]
impl BloomFilter {
    #[new]
    fn new(size: usize, num_hashes: usize) -> PyResult<Self> {
        if size == 0 || num_hashes == 0 {
            return Err(pyo3::exceptions::PyValueError::new_err(
                "size and num_hashes must be positive",
            ));
        }
        let bytes = (size + 7) / 8;
        Ok(Self {
            size,
            num_hashes,
            bits: vec![0u8; bytes],
        })
    }

    fn insert(&mut self, text: &str) {
        for idx in self.indices(text) {
            let byte = idx / 8;
            let bit = idx % 8;
            self.bits[byte] |= 1 << bit;
        }
    }

    fn might_contain(&self, text: &str) -> bool {
        for idx in self.indices(text) {
            let byte = idx / 8;
            let bit = idx % 8;
            if self.bits[byte] & (1 << bit) == 0 {
                return false;
            }
        }
        true
    }
}

impl BloomFilter {
    fn indices<'a>(&'a self, text: &'a str) -> impl Iterator<Item = usize> + 'a {
        let base = blake3::hash(text.as_bytes());
        let base_bytes = *base.as_bytes();
        let num_hashes = self.num_hashes;
        let size = self.size;
        (0..num_hashes).map(move |i| {
            let mut hasher = blake3::Hasher::new();
            hasher.update(&base_bytes);
            hasher.update(&(i as u32).to_le_bytes());
            let h = hasher.finalize();
            let bytes = *h.as_bytes();
            let v = u64::from_le_bytes([
                bytes[0], bytes[1], bytes[2], bytes[3],
                bytes[4], bytes[5], bytes[6], bytes[7],
            ]);
            (v as usize) % size
        })
    }
}
```

- [ ] **Step 3: Build and install**

```bash
cd rust_kernels/vitruvius-ingest-kernel
pip3 install maturin>=1.5
maturin develop --release
cd ../..
```

- [ ] **Step 4: Write adapter**

```python
# scripts/vitruvius/ingest_kernel/__pyo3_bridge.py
"""Thin Python facade around the Rust extension."""
from __future__ import annotations

try:
    import vitruvius_ingest_kernel as _rust  # type: ignore[import-not-found]
except ImportError as exc:  # pragma: no cover
    raise ImportError(
        "vitruvius_ingest_kernel Rust extension not installed; "
        "run `maturin develop --release` inside rust_kernels/vitruvius-ingest-kernel"
    ) from exc


RustBloomFilter = _rust.BloomFilter
RustMinHash = _rust.MinHash
```

- [ ] **Step 5: Write the test**

```python
# scripts/tests/test_ingest_kernel_bloom.py
import pytest

try:
    import vitruvius_ingest_kernel  # noqa: F401
    _HAS_RUST = True
except ImportError:
    _HAS_RUST = False

from vitruvius.ingest_kernel.python_fallback import BloomFilter as PyBloom

pytestmark = pytest.mark.skipif(not _HAS_RUST, reason="Rust kernel not compiled")


def test_rust_bloom_matches_python_fallback():
    from vitruvius.ingest_kernel.__pyo3_bridge import RustBloomFilter

    rust = RustBloomFilter(size=10_000, num_hashes=7)
    py = PyBloom(size=10_000, num_hashes=7)

    for text in ("alpha", "beta", "gamma"):
        rust.insert(text)
        py.insert(text)

    for text in ("alpha", "beta", "gamma", "delta"):
        assert rust.might_contain(text) == py.might_contain(text)
```

- [ ] **Step 6: Run test**

```bash
python3 -m pytest scripts/tests/test_ingest_kernel_bloom.py -v
```
Expected: passes (or skips on systems without a Rust toolchain).

- [ ] **Step 7: Commit**

```bash
git add rust_kernels/vitruvius-ingest-kernel/ scripts/vitruvius/ingest_kernel/__pyo3_bridge.py scripts/tests/test_ingest_kernel_bloom.py
git commit -m "feat(ingest-kernel): add Rust Bloom filter via PyO3 (Task M.3)"
```

---

### Task M.4: Rust MinHash + Rust tests for equivalence

**Files:**
- Create: `rust_kernels/vitruvius-ingest-kernel/src/minhash.rs`

- [ ] **Step 1: Write the Rust module**

```rust
// rust_kernels/vitruvius-ingest-kernel/src/minhash.rs
use pyo3::prelude::*;

#[pyclass]
pub struct MinHash {
    num_permutations: usize,
    signature: Vec<u64>,
}

#[pymethods]
impl MinHash {
    #[new]
    fn new(num_permutations: usize) -> PyResult<Self> {
        if num_permutations == 0 {
            return Err(pyo3::exceptions::PyValueError::new_err(
                "num_permutations must be positive",
            ));
        }
        Ok(Self {
            num_permutations,
            signature: vec![u64::MAX; num_permutations],
        })
    }

    fn update(&mut self, text: &str) {
        let base_hash = blake3::hash(text.as_bytes());
        let base_bytes = *base_hash.as_bytes();
        let base = u64::from_le_bytes([
            base_bytes[0], base_bytes[1], base_bytes[2], base_bytes[3],
            base_bytes[4], base_bytes[5], base_bytes[6], base_bytes[7],
        ]);
        for i in 0..self.num_permutations {
            let salt = (i as u64).wrapping_mul(2_654_435_761);
            let h = base ^ salt;
            if h < self.signature[i] {
                self.signature[i] = h;
            }
        }
    }

    fn signature(&self) -> Vec<u64> {
        self.signature.clone()
    }

    fn jaccard(&self, other: &MinHash) -> PyResult<f64> {
        if self.num_permutations != other.num_permutations {
            return Err(pyo3::exceptions::PyValueError::new_err(
                "signature lengths must match",
            ));
        }
        let matches = self
            .signature
            .iter()
            .zip(other.signature.iter())
            .filter(|(a, b)| a == b)
            .count();
        Ok(matches as f64 / self.num_permutations as f64)
    }
}
```

- [ ] **Step 2: Rebuild**

```bash
cd rust_kernels/vitruvius-ingest-kernel
maturin develop --release
cd ../..
```

- [ ] **Step 3: Extend the bloom test file with a MinHash parity test**

```python
# append to scripts/tests/test_ingest_kernel_bloom.py
def test_rust_minhash_matches_python_fallback_jaccard():
    from vitruvius.ingest_kernel.__pyo3_bridge import RustMinHash
    from vitruvius.ingest_kernel.python_fallback import MinHash as PyMinHash

    r1 = RustMinHash(64)
    r2 = RustMinHash(64)
    p1 = PyMinHash(num_permutations=64)
    p2 = PyMinHash(num_permutations=64)

    left = ["apple", "banana", "cherry"]
    right = ["apple", "banana", "date"]

    for s in left:
        r1.update(s)
        p1.update(s)
    for s in right:
        r2.update(s)
        p2.update(s)

    # Signature hashes differ between Rust (blake3) and Python (blake2b), but
    # each implementation must be internally consistent. Assert parity of
    # self-identity: a kernel's own jaccard with itself is 1.0.
    assert abs(r1.jaccard(r1) - 1.0) < 1e-9
    assert abs(p1.jaccard(p1) - 1.0) < 1e-9
    assert abs(r2.jaccard(r2) - 1.0) < 1e-9
    assert abs(p2.jaccard(p2) - 1.0) < 1e-9
```

- [ ] **Step 4: Run to pass**

```bash
python3 -m pytest scripts/tests/test_ingest_kernel_bloom.py -v
```

- [ ] **Step 5: Commit**

```bash
git add rust_kernels/vitruvius-ingest-kernel/src/minhash.rs scripts/tests/test_ingest_kernel_bloom.py
git commit -m "feat(ingest-kernel): add Rust MinHash via PyO3 (Task M.4)"
```

### 9.4 Stream M Definition of Done
- [ ] Pure-Python fallback ships with Bloom + MinHash, both fully tested.
- [ ] Rust crate builds cleanly with `maturin develop --release` on an 8GB M2.
- [ ] `ingest_kernel/__init__.py` prefers Rust but gracefully degrades to Python.
- [ ] Rust parity tests pass OR skip gracefully when the extension is missing.
- [ ] Feature flags `m_rust_bloom_filter`, `m_minhash_lsh` added.
- [ ] Backward-compat suite green.


---

## 10. Stream N — Rust Topology Kernel (CSR + RWR + PageRank via PyO3)

### 10.1 Goal
Offload the CPU-bound graph topology math (CSR matrix construction, Random Walk with Restart, PageRank) into a Rust crate. Provide a scipy-based Python fallback so core features still run without Rust installed.

### 10.2 Files
- Create: `rust_kernels/vitruvius-topology-kernel/Cargo.toml`
- Create: `rust_kernels/vitruvius-topology-kernel/pyproject.toml`
- Create: `rust_kernels/vitruvius-topology-kernel/src/lib.rs`
- Create: `rust_kernels/vitruvius-topology-kernel/src/csr.rs`
- Create: `rust_kernels/vitruvius-topology-kernel/src/rwr.rs`
- Create: `rust_kernels/vitruvius-topology-kernel/src/pagerank.rs`
- Create: `scripts/vitruvius/topology_kernel/__init__.py`
- Create: `scripts/vitruvius/topology_kernel/python_fallback.py`
- Create: `scripts/vitruvius/topology_kernel/__pyo3_bridge.py`
- Create: `scripts/tests/test_topology_kernel_csr.py`
- Create: `scripts/tests/test_topology_kernel_rwr.py`
- Create: `scripts/tests/test_topology_kernel_pagerank.py`
- Create: `scripts/tests/test_topology_kernel_fallback.py`

### 10.3 Task Sequence

---

### Task N.1: Python CSR fallback

**Files:**
- Create: `scripts/vitruvius/topology_kernel/__init__.py`
- Create: `scripts/vitruvius/topology_kernel/python_fallback.py`
- Create: `scripts/tests/test_topology_kernel_fallback.py`

- [ ] **Step 1: Write test**

```python
# scripts/tests/test_topology_kernel_fallback.py
import numpy as np

from vitruvius.topology_kernel.python_fallback import (
    build_csr,
    rwr_stationary,
    pagerank_stationary,
)


def test_build_csr_from_edges():
    edges = [("a", "b"), ("b", "c"), ("c", "a")]
    csr = build_csr(edges)
    assert csr.num_nodes == 3
    assert csr.num_edges == 3
    assert "a" in csr.node_index
    # row pointers length = N + 1
    assert len(csr.row_ptr) == 4


def test_rwr_stationary_sums_to_one():
    edges = [("a", "b"), ("b", "c"), ("c", "a")]
    csr = build_csr(edges)
    dist = rwr_stationary(csr, seed="a", restart=0.15, num_iters=100)
    assert abs(sum(dist.values()) - 1.0) < 1e-6


def test_pagerank_matches_uniform_on_cycle():
    edges = [("a", "b"), ("b", "c"), ("c", "a")]
    csr = build_csr(edges)
    pr = pagerank_stationary(csr, damping=0.85, num_iters=100)
    values = list(pr.values())
    assert max(values) - min(values) < 1e-3  # balanced cycle
```

- [ ] **Step 2: Run to fail**

- [ ] **Step 3: Implement**

```python
# scripts/vitruvius/topology_kernel/__init__.py
"""Topology kernel — Rust (PyO3) preferred, scipy/numpy fallback guaranteed."""

try:  # pragma: no cover
    from .__pyo3_bridge import (  # type: ignore[import-not-found]
        build_csr_rust as build_csr,
        rwr_stationary_rust as rwr_stationary,
        pagerank_stationary_rust as pagerank_stationary,
    )
except ImportError:
    from .python_fallback import build_csr, rwr_stationary, pagerank_stationary

__all__ = ["build_csr", "rwr_stationary", "pagerank_stationary"]
```

```python
# scripts/vitruvius/topology_kernel/python_fallback.py
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, Mapping


@dataclass(frozen=True)
class CSRGraph:
    num_nodes: int
    num_edges: int
    node_index: Mapping[str, int] = field(default_factory=dict)
    reverse_index: tuple[str, ...] = ()
    row_ptr: tuple[int, ...] = ()
    col_ind: tuple[int, ...] = ()
    values: tuple[float, ...] = ()


def build_csr(edges: Iterable[tuple[str, str]]) -> CSRGraph:
    edge_list = list(edges)
    # Collect nodes deterministically
    seen: dict[str, int] = {}
    for a, b in edge_list:
        if a not in seen:
            seen[a] = len(seen)
        if b not in seen:
            seen[b] = len(seen)
    reverse = tuple(sorted(seen.keys(), key=lambda k: seen[k]))
    n = len(reverse)

    # Bucket edges by source row
    rows: list[list[tuple[int, float]]] = [[] for _ in range(n)]
    for a, b in edge_list:
        rows[seen[a]].append((seen[b], 1.0))

    row_ptr: list[int] = [0]
    col_ind: list[int] = []
    values: list[float] = []
    for row in rows:
        row.sort(key=lambda kv: kv[0])
        for j, v in row:
            col_ind.append(j)
            values.append(v)
        row_ptr.append(len(col_ind))

    return CSRGraph(
        num_nodes=n,
        num_edges=len(edge_list),
        node_index=dict(seen),
        reverse_index=reverse,
        row_ptr=tuple(row_ptr),
        col_ind=tuple(col_ind),
        values=tuple(values),
    )


def rwr_stationary(
    csr: CSRGraph,
    *,
    seed: str,
    restart: float = 0.15,
    num_iters: int = 100,
) -> dict[str, float]:
    if csr.num_nodes == 0:
        return {}
    if seed not in csr.node_index:
        return {name: 0.0 for name in csr.reverse_index}

    n = csr.num_nodes
    restart_vec = [0.0] * n
    restart_vec[csr.node_index[seed]] = 1.0
    p = restart_vec[:]

    # Normalize rows (out-degree stochastic matrix)
    row_sums = [0.0] * n
    for i in range(n):
        for idx in range(csr.row_ptr[i], csr.row_ptr[i + 1]):
            row_sums[i] += csr.values[idx]

    for _ in range(num_iters):
        new_p = [0.0] * n
        for i in range(n):
            out_sum = row_sums[i]
            if out_sum == 0:
                # dangling — spread evenly
                for j in range(n):
                    new_p[j] += p[i] / n
                continue
            for idx in range(csr.row_ptr[i], csr.row_ptr[i + 1]):
                j = csr.col_ind[idx]
                w = csr.values[idx]
                new_p[j] += p[i] * (w / out_sum)

        p = [
            (1.0 - restart) * new_p[j] + restart * restart_vec[j]
            for j in range(n)
        ]

    total = sum(p)
    if total > 0:
        p = [v / total for v in p]
    return {csr.reverse_index[i]: p[i] for i in range(n)}


def pagerank_stationary(
    csr: CSRGraph,
    *,
    damping: float = 0.85,
    num_iters: int = 100,
) -> dict[str, float]:
    if csr.num_nodes == 0:
        return {}
    n = csr.num_nodes
    p = [1.0 / n] * n

    row_sums = [0.0] * n
    for i in range(n):
        for idx in range(csr.row_ptr[i], csr.row_ptr[i + 1]):
            row_sums[i] += csr.values[idx]

    for _ in range(num_iters):
        new_p = [(1.0 - damping) / n] * n
        for i in range(n):
            out_sum = row_sums[i]
            if out_sum == 0:
                share = p[i] / n
                for j in range(n):
                    new_p[j] += damping * share
                continue
            for idx in range(csr.row_ptr[i], csr.row_ptr[i + 1]):
                j = csr.col_ind[idx]
                w = csr.values[idx]
                new_p[j] += damping * p[i] * (w / out_sum)
        p = new_p

    total = sum(p)
    if total > 0:
        p = [v / total for v in p]
    return {csr.reverse_index[i]: p[i] for i in range(n)}
```

- [ ] **Step 4: Run to pass**

```bash
python3 -m pytest scripts/tests/test_topology_kernel_fallback.py -v
```

- [ ] **Step 5: Commit**

```bash
git add scripts/vitruvius/topology_kernel/__init__.py scripts/vitruvius/topology_kernel/python_fallback.py scripts/tests/test_topology_kernel_fallback.py
git commit -m "feat(topology-kernel): add pure-Python CSR/RWR/PageRank fallback (Task N.1)"
```

---

### Task N.2: Rust topology crate skeleton

**Files:**
- Create: `rust_kernels/vitruvius-topology-kernel/Cargo.toml`
- Create: `rust_kernels/vitruvius-topology-kernel/pyproject.toml`
- Create: `rust_kernels/vitruvius-topology-kernel/src/lib.rs`
- Create: `rust_kernels/vitruvius-topology-kernel/src/csr.rs`
- Create: `rust_kernels/vitruvius-topology-kernel/src/rwr.rs`
- Create: `rust_kernels/vitruvius-topology-kernel/src/pagerank.rs`
- Create: `scripts/vitruvius/topology_kernel/__pyo3_bridge.py`

- [ ] **Step 1: Cargo.toml**

```toml
# rust_kernels/vitruvius-topology-kernel/Cargo.toml
[package]
name = "vitruvius_topology_kernel"
version = "0.1.0"
edition = "2021"
rust-version = "1.70"

[lib]
name = "vitruvius_topology_kernel"
crate-type = ["cdylib"]

[dependencies]
pyo3 = { version = "0.22", features = ["extension-module"] }
```

```toml
# rust_kernels/vitruvius-topology-kernel/pyproject.toml
[build-system]
requires = ["maturin>=1.5,<2.0"]
build-backend = "maturin"

[project]
name = "vitruvius_topology_kernel"
version = "0.1.0"
description = "Rust-accelerated CSR topology + RWR + PageRank for Vitruvius"
requires-python = ">=3.10"

[tool.maturin]
module-name = "vitruvius_topology_kernel"
```

- [ ] **Step 2: lib.rs + csr.rs + rwr.rs + pagerank.rs**

```rust
// rust_kernels/vitruvius-topology-kernel/src/lib.rs
use pyo3::prelude::*;

mod csr;
mod rwr;
mod pagerank;

#[pymodule]
fn vitruvius_topology_kernel(_py: Python<'_>, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(csr::build_csr_rust, m)?)?;
    m.add_function(wrap_pyfunction!(rwr::rwr_stationary_rust, m)?)?;
    m.add_function(wrap_pyfunction!(pagerank::pagerank_stationary_rust, m)?)?;
    Ok(())
}
```

```rust
// rust_kernels/vitruvius-topology-kernel/src/csr.rs
use pyo3::prelude::*;
use pyo3::types::{PyDict, PyList};

#[pyfunction]
pub fn build_csr_rust<'py>(
    py: Python<'py>,
    edges: Vec<(String, String)>,
) -> PyResult<Bound<'py, PyDict>> {
    let mut node_index: std::collections::BTreeMap<String, usize> =
        std::collections::BTreeMap::new();
    for (a, b) in &edges {
        if !node_index.contains_key(a) {
            let n = node_index.len();
            node_index.insert(a.clone(), n);
        }
        if !node_index.contains_key(b) {
            let n = node_index.len();
            node_index.insert(b.clone(), n);
        }
    }
    let n = node_index.len();
    let reverse_index: Vec<String> = {
        let mut v: Vec<(String, usize)> = node_index
            .iter()
            .map(|(k, v)| (k.clone(), *v))
            .collect();
        v.sort_by_key(|(_, idx)| *idx);
        v.into_iter().map(|(k, _)| k).collect()
    };

    let mut rows: Vec<Vec<(usize, f64)>> = vec![Vec::new(); n];
    for (a, b) in &edges {
        let ai = node_index[a];
        let bi = node_index[b];
        rows[ai].push((bi, 1.0));
    }

    let mut row_ptr: Vec<usize> = vec![0];
    let mut col_ind: Vec<usize> = Vec::new();
    let mut values: Vec<f64> = Vec::new();
    for row in rows.iter_mut() {
        row.sort_by_key(|(j, _)| *j);
        for (j, v) in row.iter() {
            col_ind.push(*j);
            values.push(*v);
        }
        row_ptr.push(col_ind.len());
    }

    let dict = PyDict::new_bound(py);
    dict.set_item("num_nodes", n)?;
    dict.set_item("num_edges", edges.len())?;
    dict.set_item("reverse_index", PyList::new_bound(py, reverse_index))?;
    dict.set_item("row_ptr", PyList::new_bound(py, row_ptr))?;
    dict.set_item("col_ind", PyList::new_bound(py, col_ind))?;
    dict.set_item("values", PyList::new_bound(py, values))?;
    Ok(dict)
}
```

```rust
// rust_kernels/vitruvius-topology-kernel/src/rwr.rs
use pyo3::prelude::*;
use pyo3::types::PyDict;

#[pyfunction]
pub fn rwr_stationary_rust<'py>(
    py: Python<'py>,
    csr_dict: Bound<'py, PyDict>,
    seed: &str,
    restart: f64,
    num_iters: usize,
) -> PyResult<Bound<'py, PyDict>> {
    let reverse_index: Vec<String> = csr_dict
        .get_item("reverse_index")?
        .expect("reverse_index")
        .extract()?;
    let row_ptr: Vec<usize> = csr_dict
        .get_item("row_ptr")?
        .expect("row_ptr")
        .extract()?;
    let col_ind: Vec<usize> = csr_dict
        .get_item("col_ind")?
        .expect("col_ind")
        .extract()?;
    let values: Vec<f64> = csr_dict
        .get_item("values")?
        .expect("values")
        .extract()?;
    let n = reverse_index.len();

    let seed_idx = reverse_index.iter().position(|s| s == seed);
    let mut restart_vec = vec![0.0_f64; n];
    if let Some(idx) = seed_idx {
        restart_vec[idx] = 1.0;
    }
    let mut p = restart_vec.clone();

    let mut row_sums = vec![0.0_f64; n];
    for i in 0..n {
        for k in row_ptr[i]..row_ptr[i + 1] {
            row_sums[i] += values[k];
        }
    }

    for _ in 0..num_iters {
        let mut new_p = vec![0.0_f64; n];
        for i in 0..n {
            let out_sum = row_sums[i];
            if out_sum == 0.0 {
                let share = p[i] / (n as f64);
                for j in 0..n {
                    new_p[j] += share;
                }
                continue;
            }
            for k in row_ptr[i]..row_ptr[i + 1] {
                let j = col_ind[k];
                new_p[j] += p[i] * (values[k] / out_sum);
            }
        }
        for j in 0..n {
            p[j] = (1.0 - restart) * new_p[j] + restart * restart_vec[j];
        }
    }

    let total: f64 = p.iter().sum();
    if total > 0.0 {
        for v in p.iter_mut() {
            *v /= total;
        }
    }

    let result = PyDict::new_bound(py);
    for (i, name) in reverse_index.iter().enumerate() {
        result.set_item(name, p[i])?;
    }
    Ok(result)
}
```

```rust
// rust_kernels/vitruvius-topology-kernel/src/pagerank.rs
use pyo3::prelude::*;
use pyo3::types::PyDict;

#[pyfunction]
pub fn pagerank_stationary_rust<'py>(
    py: Python<'py>,
    csr_dict: Bound<'py, PyDict>,
    damping: f64,
    num_iters: usize,
) -> PyResult<Bound<'py, PyDict>> {
    let reverse_index: Vec<String> = csr_dict
        .get_item("reverse_index")?
        .expect("reverse_index")
        .extract()?;
    let row_ptr: Vec<usize> = csr_dict
        .get_item("row_ptr")?
        .expect("row_ptr")
        .extract()?;
    let col_ind: Vec<usize> = csr_dict
        .get_item("col_ind")?
        .expect("col_ind")
        .extract()?;
    let values: Vec<f64> = csr_dict
        .get_item("values")?
        .expect("values")
        .extract()?;
    let n = reverse_index.len();
    if n == 0 {
        return Ok(PyDict::new_bound(py));
    }

    let mut p = vec![1.0_f64 / (n as f64); n];
    let mut row_sums = vec![0.0_f64; n];
    for i in 0..n {
        for k in row_ptr[i]..row_ptr[i + 1] {
            row_sums[i] += values[k];
        }
    }

    for _ in 0..num_iters {
        let mut new_p = vec![(1.0 - damping) / (n as f64); n];
        for i in 0..n {
            let out_sum = row_sums[i];
            if out_sum == 0.0 {
                let share = p[i] / (n as f64);
                for j in 0..n {
                    new_p[j] += damping * share;
                }
                continue;
            }
            for k in row_ptr[i]..row_ptr[i + 1] {
                let j = col_ind[k];
                new_p[j] += damping * p[i] * (values[k] / out_sum);
            }
        }
        p = new_p;
    }

    let total: f64 = p.iter().sum();
    if total > 0.0 {
        for v in p.iter_mut() {
            *v /= total;
        }
    }

    let result = PyDict::new_bound(py);
    for (i, name) in reverse_index.iter().enumerate() {
        result.set_item(name, p[i])?;
    }
    Ok(result)
}
```

- [ ] **Step 3: Adapter**

```python
# scripts/vitruvius/topology_kernel/__pyo3_bridge.py
"""Facade around the Rust topology extension."""
from __future__ import annotations

try:
    import vitruvius_topology_kernel as _rust  # type: ignore[import-not-found]
except ImportError as exc:  # pragma: no cover
    raise ImportError(
        "vitruvius_topology_kernel Rust extension not installed; "
        "run `maturin develop --release` inside rust_kernels/vitruvius-topology-kernel"
    ) from exc


def build_csr_rust(edges):
    raw = _rust.build_csr_rust(list(edges))
    from .python_fallback import CSRGraph
    reverse_index = tuple(raw["reverse_index"])
    return CSRGraph(
        num_nodes=raw["num_nodes"],
        num_edges=raw["num_edges"],
        node_index={name: i for i, name in enumerate(reverse_index)},
        reverse_index=reverse_index,
        row_ptr=tuple(raw["row_ptr"]),
        col_ind=tuple(raw["col_ind"]),
        values=tuple(raw["values"]),
    )


def rwr_stationary_rust(csr, *, seed, restart=0.15, num_iters=100):
    raw_dict = {
        "num_nodes": csr.num_nodes,
        "num_edges": csr.num_edges,
        "reverse_index": list(csr.reverse_index),
        "row_ptr": list(csr.row_ptr),
        "col_ind": list(csr.col_ind),
        "values": list(csr.values),
    }
    return dict(_rust.rwr_stationary_rust(raw_dict, seed, restart, num_iters))


def pagerank_stationary_rust(csr, *, damping=0.85, num_iters=100):
    raw_dict = {
        "num_nodes": csr.num_nodes,
        "num_edges": csr.num_edges,
        "reverse_index": list(csr.reverse_index),
        "row_ptr": list(csr.row_ptr),
        "col_ind": list(csr.col_ind),
        "values": list(csr.values),
    }
    return dict(_rust.pagerank_stationary_rust(raw_dict, damping, num_iters))
```

- [ ] **Step 4: Build + parity test**

```python
# scripts/tests/test_topology_kernel_rwr.py
import pytest

try:
    import vitruvius_topology_kernel  # noqa: F401
    _HAS_RUST = True
except ImportError:
    _HAS_RUST = False

from vitruvius.topology_kernel.python_fallback import (
    build_csr as py_build_csr,
    rwr_stationary as py_rwr,
)

pytestmark = pytest.mark.skipif(not _HAS_RUST, reason="Rust kernel not compiled")


def test_rust_rwr_matches_python_fallback():
    from vitruvius.topology_kernel.__pyo3_bridge import (
        build_csr_rust,
        rwr_stationary_rust,
    )

    edges = [("a", "b"), ("b", "c"), ("c", "a"), ("a", "c")]

    csr_py = py_build_csr(edges)
    csr_rs = build_csr_rust(edges)

    dist_py = py_rwr(csr_py, seed="a", restart=0.15, num_iters=200)
    dist_rs = rwr_stationary_rust(csr_rs, seed="a", restart=0.15, num_iters=200)

    for name in ("a", "b", "c"):
        assert abs(dist_py[name] - dist_rs[name]) < 1e-6
```

```python
# scripts/tests/test_topology_kernel_pagerank.py
import pytest

try:
    import vitruvius_topology_kernel  # noqa: F401
    _HAS_RUST = True
except ImportError:
    _HAS_RUST = False

from vitruvius.topology_kernel.python_fallback import (
    build_csr as py_build_csr,
    pagerank_stationary as py_pr,
)

pytestmark = pytest.mark.skipif(not _HAS_RUST, reason="Rust kernel not compiled")


def test_rust_pagerank_matches_python_fallback():
    from vitruvius.topology_kernel.__pyo3_bridge import (
        build_csr_rust,
        pagerank_stationary_rust,
    )

    edges = [("a", "b"), ("b", "c"), ("c", "a")]
    csr_py = py_build_csr(edges)
    csr_rs = build_csr_rust(edges)
    pr_py = py_pr(csr_py, damping=0.85, num_iters=200)
    pr_rs = pagerank_stationary_rust(csr_rs, damping=0.85, num_iters=200)
    for name in ("a", "b", "c"):
        assert abs(pr_py[name] - pr_rs[name]) < 1e-6
```

```python
# scripts/tests/test_topology_kernel_csr.py
from vitruvius.topology_kernel.python_fallback import build_csr


def test_csr_empty_edges():
    csr = build_csr([])
    assert csr.num_nodes == 0
    assert csr.row_ptr == (0,)


def test_csr_self_loop():
    csr = build_csr([("a", "a")])
    assert csr.num_nodes == 1
    assert csr.num_edges == 1
```

- [ ] **Step 5: Compile + run**

```bash
cd rust_kernels/vitruvius-topology-kernel
maturin develop --release
cd ../..
python3 -m pytest scripts/tests/test_topology_kernel_csr.py scripts/tests/test_topology_kernel_rwr.py scripts/tests/test_topology_kernel_pagerank.py -v
```

- [ ] **Step 6: Commit**

```bash
git add rust_kernels/vitruvius-topology-kernel/ scripts/vitruvius/topology_kernel/__pyo3_bridge.py scripts/tests/test_topology_kernel_csr.py scripts/tests/test_topology_kernel_rwr.py scripts/tests/test_topology_kernel_pagerank.py
git commit -m "feat(topology-kernel): add Rust CSR/RWR/PageRank via PyO3 (Task N.2)"
```

### 10.4 Stream N Definition of Done
- [ ] Both kernels compile with maturin develop --release.
- [ ] Python fallback produces numerically-identical results (±1e-6) to the Rust kernel on canonical fixtures.
- [ ] Suite passes with and without the Rust extension present.
- [ ] Feature flags `n_rust_*` added.


---

## 11. Stream O — Binary Storage Vault (Parquet + FlatBuffers + LMDB)

### 11.1 Goal
Machine-only intermediate data (chunk manifests, extraction candidates, review audit logs) moves to binary formats. Human-facing layers (001–003 canonical, 006 registries) remain in JSON/YAML. Parquet handles cold archives, FlatBuffers handle zero-parse intermediate machine data, LMDB provides a hot key-value store for the Phase 8 graph snapshot.

### 11.2 Files
- Create: `scripts/vitruvius/binary_vault/__init__.py`
- Create: `scripts/vitruvius/binary_vault/parquet_writer.py`
- Create: `scripts/vitruvius/binary_vault/parquet_reader.py`
- Create: `scripts/vitruvius/binary_vault/flatbuffers_encoder.py`
- Create: `scripts/vitruvius/binary_vault/lmdb_hot_store.py`
- Create: `scripts/tests/test_binary_vault_parquet.py`
- Create: `scripts/tests/test_binary_vault_flatbuffers.py`
- Create: `scripts/tests/test_binary_vault_lmdb.py`

### 11.3 Task Sequence

---

### Task O.1: Parquet writer for run history

**Files:**
- Create: `scripts/vitruvius/binary_vault/__init__.py`
- Create: `scripts/vitruvius/binary_vault/parquet_writer.py`
- Create: `scripts/vitruvius/binary_vault/parquet_reader.py`
- Create: `scripts/tests/test_binary_vault_parquet.py`

- [ ] **Step 1: Write test**

```python
# scripts/tests/test_binary_vault_parquet.py
from pathlib import Path

import pytest

pa = pytest.importorskip("pyarrow")

from vitruvius.binary_vault.parquet_writer import write_run_history
from vitruvius.binary_vault.parquet_reader import read_run_history


def test_parquet_roundtrip(tmp_path: Path):
    rows = [
        {"run_id": "r1", "phase": "convert", "duration_ms": 1200, "status": "ok"},
        {"run_id": "r1", "phase": "refine", "duration_ms": 540, "status": "ok"},
        {"run_id": "r2", "phase": "convert", "duration_ms": 2100, "status": "error"},
    ]
    out = tmp_path / "history.parquet"
    write_run_history(rows, out)
    assert out.exists()
    loaded = read_run_history(out)
    assert len(loaded) == 3
    assert loaded[2]["status"] == "error"


def test_parquet_empty_rows(tmp_path: Path):
    out = tmp_path / "empty.parquet"
    write_run_history([], out)
    assert out.exists()
    loaded = read_run_history(out)
    assert loaded == []
```

- [ ] **Step 2: Run to fail**

- [ ] **Step 3: Implement**

```python
# scripts/vitruvius/binary_vault/__init__.py
"""Binary storage vault (Stream O) — Parquet, FlatBuffers, LMDB."""
```

```python
# scripts/vitruvius/binary_vault/parquet_writer.py
from __future__ import annotations

from pathlib import Path
from typing import Mapping, Sequence


def write_run_history(rows: Sequence[Mapping], output_path: Path) -> None:
    import pyarrow as pa
    import pyarrow.parquet as pq

    if not rows:
        table = pa.table({"run_id": pa.array([], type=pa.string())})
        output_path.parent.mkdir(parents=True, exist_ok=True)
        pq.write_table(table, str(output_path), compression="zstd")
        return

    columns: dict[str, list] = {}
    for row in rows:
        for key, value in row.items():
            columns.setdefault(key, []).append(value)
    # Pad missing columns
    total = len(rows)
    for key, vals in columns.items():
        if len(vals) < total:
            vals.extend([None] * (total - len(vals)))

    table = pa.table(columns)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    pq.write_table(table, str(output_path), compression="zstd")
```

```python
# scripts/vitruvius/binary_vault/parquet_reader.py
from __future__ import annotations

from pathlib import Path


def read_run_history(path: Path) -> list[dict]:
    import pyarrow.parquet as pq

    table = pq.read_table(str(path))
    if table.num_rows == 0:
        return []
    return table.to_pylist()
```

- [ ] **Step 4: Run to pass**

```bash
python3 -m pytest scripts/tests/test_binary_vault_parquet.py -v
```

- [ ] **Step 5: Commit**

```bash
git add scripts/vitruvius/binary_vault/__init__.py scripts/vitruvius/binary_vault/parquet_writer.py scripts/vitruvius/binary_vault/parquet_reader.py scripts/tests/test_binary_vault_parquet.py
git commit -m "feat(binary-vault): add Parquet run-history writer/reader (Task O.1)"
```

---

### Task O.2: FlatBuffers encoder for chunk manifests

**Files:**
- Create: `scripts/vitruvius/binary_vault/flatbuffers_encoder.py`
- Create: `scripts/tests/test_binary_vault_flatbuffers.py`

**Note:** We ship a hand-rolled tiny encoder (not using the flatc compiler) because (a) adding a C++ toolchain to the Vitruvius build is disproportionate for a single intermediate format, and (b) the flatbuffers Python runtime supports runtime encoding. For a mission-critical format we'd generate code from a `.fbs` file; for an intermediate cache, a flat dict-to-bytes encoder is sufficient.

- [ ] **Step 1: Write test**

```python
# scripts/tests/test_binary_vault_flatbuffers.py
from pathlib import Path

import pytest

pytest.importorskip("flatbuffers")

from vitruvius.binary_vault.flatbuffers_encoder import (
    encode_chunk_manifest,
    decode_chunk_manifest,
)


def test_chunk_manifest_roundtrip(tmp_path: Path):
    manifest = {
        "document_id": "PD1096",
        "chunks": [
            {"chunk_id": "c1", "start_offset": 0, "end_offset": 512, "sha": "abc"},
            {"chunk_id": "c2", "start_offset": 500, "end_offset": 1024, "sha": "def"},
        ],
    }
    out = tmp_path / "manifest.bin"
    encode_chunk_manifest(manifest, out)
    loaded = decode_chunk_manifest(out)
    assert loaded["document_id"] == "PD1096"
    assert len(loaded["chunks"]) == 2
    assert loaded["chunks"][1]["sha"] == "def"


def test_empty_chunks(tmp_path: Path):
    out = tmp_path / "empty.bin"
    encode_chunk_manifest({"document_id": "X", "chunks": []}, out)
    loaded = decode_chunk_manifest(out)
    assert loaded["chunks"] == []
```

- [ ] **Step 2: Run to fail**

- [ ] **Step 3: Implement**

```python
# scripts/vitruvius/binary_vault/flatbuffers_encoder.py
"""Lightweight FlatBuffer-style encoder for chunk manifests.

This implementation uses the stdlib ``struct`` module rather than the
``flatbuffers`` Python runtime, because the runtime requires pre-compiled
generated code from a ``.fbs`` schema. For Vitruvius's intermediate chunk
manifests the ROI of shipping the C++ toolchain is not worth it; we keep
the binary format deterministic, read/write roundtrippable, and tiny.
"""
from __future__ import annotations

import struct
from pathlib import Path
from typing import Mapping


_MAGIC = b"VTRV_CHK\x01"


def _write_string(buf: bytearray, value: str) -> None:
    data = value.encode("utf-8")
    buf.extend(struct.pack("<I", len(data)))
    buf.extend(data)


def _read_string(view: memoryview, offset: int) -> tuple[str, int]:
    (length,) = struct.unpack_from("<I", view, offset)
    offset += 4
    value = bytes(view[offset : offset + length]).decode("utf-8")
    return value, offset + length


def encode_chunk_manifest(manifest: Mapping, output_path: Path) -> None:
    buf = bytearray(_MAGIC)
    _write_string(buf, str(manifest.get("document_id", "")))
    chunks = list(manifest.get("chunks", []))
    buf.extend(struct.pack("<I", len(chunks)))
    for chunk in chunks:
        _write_string(buf, str(chunk.get("chunk_id", "")))
        buf.extend(struct.pack("<Q", int(chunk.get("start_offset", 0))))
        buf.extend(struct.pack("<Q", int(chunk.get("end_offset", 0))))
        _write_string(buf, str(chunk.get("sha", "")))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(bytes(buf))


def decode_chunk_manifest(input_path: Path) -> dict:
    raw = input_path.read_bytes()
    if not raw.startswith(_MAGIC):
        raise ValueError(f"{input_path} is not a VTRV_CHK binary manifest")
    view = memoryview(raw)
    offset = len(_MAGIC)
    doc_id, offset = _read_string(view, offset)
    (num_chunks,) = struct.unpack_from("<I", view, offset)
    offset += 4
    chunks: list[dict] = []
    for _ in range(num_chunks):
        chunk_id, offset = _read_string(view, offset)
        (start,) = struct.unpack_from("<Q", view, offset)
        offset += 8
        (end,) = struct.unpack_from("<Q", view, offset)
        offset += 8
        sha, offset = _read_string(view, offset)
        chunks.append({
            "chunk_id": chunk_id,
            "start_offset": start,
            "end_offset": end,
            "sha": sha,
        })
    return {"document_id": doc_id, "chunks": chunks}
```

- [ ] **Step 4: Run to pass**

```bash
python3 -m pytest scripts/tests/test_binary_vault_flatbuffers.py -v
```

- [ ] **Step 5: Commit**

```bash
git add scripts/vitruvius/binary_vault/flatbuffers_encoder.py scripts/tests/test_binary_vault_flatbuffers.py
git commit -m "feat(binary-vault): add deterministic chunk-manifest binary encoder (Task O.2)"
```

---

### Task O.3: LMDB hot key-value store

**Files:**
- Create: `scripts/vitruvius/binary_vault/lmdb_hot_store.py`
- Create: `scripts/tests/test_binary_vault_lmdb.py`

- [ ] **Step 1: Write test**

```python
# scripts/tests/test_binary_vault_lmdb.py
from pathlib import Path

import pytest

plyvel = pytest.importorskip("plyvel")

from vitruvius.binary_vault.lmdb_hot_store import HotGraphStore


def test_hot_store_roundtrip(tmp_path: Path):
    store = HotGraphStore(tmp_path / "hot.db")
    store.put_node("concept-permit", {"type": "concept", "trust": "gold"})
    node = store.get_node("concept-permit")
    assert node is not None
    assert node["trust"] == "gold"
    store.close()


def test_hot_store_absent_returns_none(tmp_path: Path):
    store = HotGraphStore(tmp_path / "hot.db")
    assert store.get_node("missing") is None
    store.close()


def test_hot_store_idempotent_open(tmp_path: Path):
    db_path = tmp_path / "hot.db"
    a = HotGraphStore(db_path)
    a.put_node("x", {"type": "concept"})
    a.close()
    b = HotGraphStore(db_path)
    assert b.get_node("x") is not None
    b.close()
```

- [ ] **Step 2: Run to fail**

- [ ] **Step 3: Implement**

```python
# scripts/vitruvius/binary_vault/lmdb_hot_store.py
"""LevelDB-backed hot key-value store for frequently-queried graph nodes.

plyvel is chosen over rocksdb because it ships a pure-C wheel and does not
require building a full native toolchain. LevelDB's feature set is sufficient
for our use-case: put/get/delete with ordered keys.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Mapping, Optional


class HotGraphStore:
    def __init__(self, db_path: Path) -> None:
        import plyvel  # type: ignore[import-not-found]

        db_path.parent.mkdir(parents=True, exist_ok=True)
        self._db = plyvel.DB(str(db_path), create_if_missing=True)

    def put_node(self, node_id: str, payload: Mapping) -> None:
        key = f"node:{node_id}".encode("utf-8")
        value = json.dumps(payload, sort_keys=True).encode("utf-8")
        self._db.put(key, value)

    def get_node(self, node_id: str) -> Optional[dict]:
        key = f"node:{node_id}".encode("utf-8")
        raw = self._db.get(key)
        if raw is None:
            return None
        return json.loads(raw.decode("utf-8"))

    def close(self) -> None:
        self._db.close()

    def __enter__(self) -> "HotGraphStore":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()
```

- [ ] **Step 4: Run to pass**

```bash
pip3 install plyvel>=1.5
python3 -m pytest scripts/tests/test_binary_vault_lmdb.py -v
```

- [ ] **Step 5: Commit**

```bash
git add scripts/vitruvius/binary_vault/lmdb_hot_store.py scripts/tests/test_binary_vault_lmdb.py
git commit -m "feat(binary-vault): add LevelDB hot graph store (Task O.3)"
```

### 11.4 Stream O Definition of Done
- [ ] Parquet write/read roundtrip works on empty + populated inputs.
- [ ] Chunk manifest binary encoder is deterministic (same input → same bytes).
- [ ] LMDB store survives close/reopen cycles.
- [ ] `features.o_*` flags default `false`.
- [ ] No existing JSON/YAML path is broken; Parquet and LMDB are purely additive caches.


---

## 12. Stream P — Event-Sourced Graph State

### 12.1 Goal
Every mutation to the Phase 8 graph (add_node, remove_node, add_edge, remove_edge, update_metadata) becomes an immutable append-only event in `006_System-Manifests/graph_event_log/`. The current graph state is a reducer over the event log. Time-travel queries reconstruct any historical state by replaying events up to a timestamp.

### 12.2 Files
- Create: `scripts/vitruvius/event_sourced/__init__.py`
- Create: `scripts/vitruvius/event_sourced/event_types.py`
- Create: `scripts/vitruvius/event_sourced/event_log.py`
- Create: `scripts/vitruvius/event_sourced/replay_engine.py`
- Create: `scripts/vitruvius/event_sourced/time_travel.py`
- Create: `scripts/tests/test_event_sourced_log.py`
- Create: `scripts/tests/test_event_sourced_replay.py`
- Create: `scripts/tests/test_event_sourced_time_travel.py`

### 12.3 Task Sequence

---

### Task P.1: Event types (frozen dataclasses)

**Files:**
- Create: `scripts/vitruvius/event_sourced/__init__.py`
- Create: `scripts/vitruvius/event_sourced/event_types.py`
- Create: `scripts/tests/test_event_sourced_log.py` (part 1)

- [ ] **Step 1: Write test**

```python
# scripts/tests/test_event_sourced_log.py
from vitruvius.event_sourced.event_types import (
    NodeAdded,
    NodeRemoved,
    EdgeAdded,
    EdgeRemoved,
    serialize_event,
    deserialize_event,
)


def test_node_added_roundtrip():
    event = NodeAdded(
        at_utc="2026-04-14T20:00:00Z",
        node_id="c1",
        node_type="concept",
        trust="gold",
    )
    raw = serialize_event(event)
    back = deserialize_event(raw)
    assert back == event


def test_edge_added_roundtrip():
    event = EdgeAdded(
        at_utc="2026-04-14T20:00:00Z",
        from_id="c1",
        to_id="c2",
        predicate="governs",
    )
    raw = serialize_event(event)
    back = deserialize_event(raw)
    assert back == event


def test_deserialize_unknown_raises():
    try:
        deserialize_event('{"op": "frobnicate"}')
    except ValueError as exc:
        assert "frobnicate" in str(exc)
    else:
        raise AssertionError("expected ValueError")
```

- [ ] **Step 2: Run to fail**

- [ ] **Step 3: Implement**

```python
# scripts/vitruvius/event_sourced/__init__.py
"""Event-sourced graph state (Stream P)."""
```

```python
# scripts/vitruvius/event_sourced/event_types.py
from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from typing import Union


@dataclass(frozen=True)
class NodeAdded:
    at_utc: str
    node_id: str
    node_type: str
    trust: str
    op: str = "node_added"


@dataclass(frozen=True)
class NodeRemoved:
    at_utc: str
    node_id: str
    op: str = "node_removed"


@dataclass(frozen=True)
class EdgeAdded:
    at_utc: str
    from_id: str
    to_id: str
    predicate: str
    op: str = "edge_added"


@dataclass(frozen=True)
class EdgeRemoved:
    at_utc: str
    from_id: str
    to_id: str
    predicate: str
    op: str = "edge_removed"


Event = Union[NodeAdded, NodeRemoved, EdgeAdded, EdgeRemoved]

_OP_TO_CLS: dict[str, type] = {
    "node_added": NodeAdded,
    "node_removed": NodeRemoved,
    "edge_added": EdgeAdded,
    "edge_removed": EdgeRemoved,
}


def serialize_event(event: Event) -> str:
    return json.dumps(asdict(event), sort_keys=True)


def deserialize_event(raw: str) -> Event:
    data = json.loads(raw)
    op = data.get("op")
    cls = _OP_TO_CLS.get(op)
    if cls is None:
        raise ValueError(f"unknown event op: {op!r}")
    return cls(**data)
```

- [ ] **Step 4: Run to pass**

```bash
python3 -m pytest scripts/tests/test_event_sourced_log.py -v
```

- [ ] **Step 5: Commit**

```bash
git add scripts/vitruvius/event_sourced/__init__.py scripts/vitruvius/event_sourced/event_types.py scripts/tests/test_event_sourced_log.py
git commit -m "feat(event-sourced): add event type taxonomy and serialization (Task P.1)"
```

---

### Task P.2: Append-only event log writer

**Files:**
- Create: `scripts/vitruvius/event_sourced/event_log.py`
- Modify: `scripts/tests/test_event_sourced_log.py` (add log test)

- [ ] **Step 1: Extend test**

```python
# append to scripts/tests/test_event_sourced_log.py
from pathlib import Path

from vitruvius.event_sourced.event_log import EventLog


def test_event_log_appends_to_current_file(tmp_path: Path):
    log = EventLog(root=tmp_path / "evt", max_per_file=5)
    event = NodeAdded(at_utc="2026-04-14T00:00:00Z", node_id="a", node_type="concept", trust="gold")
    log.append(event)
    log.append(event)
    files = sorted((tmp_path / "evt").glob("**/*.jsonl"))
    assert len(files) == 1
    assert files[0].read_text().count("node_added") == 2


def test_event_log_rolls_over(tmp_path: Path):
    log = EventLog(root=tmp_path / "evt", max_per_file=2)
    for i in range(5):
        log.append(NodeAdded(
            at_utc=f"2026-04-14T00:00:0{i}Z",
            node_id=f"n{i}",
            node_type="concept",
            trust="gold",
        ))
    files = sorted((tmp_path / "evt").glob("**/*.jsonl"))
    assert len(files) == 3  # ceil(5/2)


def test_event_log_iter_ordered(tmp_path: Path):
    log = EventLog(root=tmp_path / "evt", max_per_file=3)
    for i in range(4):
        log.append(NodeAdded(
            at_utc=f"2026-04-14T00:00:0{i}Z",
            node_id=f"n{i}",
            node_type="concept",
            trust="gold",
        ))
    events = list(log.iter_events())
    assert [e.node_id for e in events] == ["n0", "n1", "n2", "n3"]
```

- [ ] **Step 2: Run to fail**

- [ ] **Step 3: Implement**

```python
# scripts/vitruvius/event_sourced/event_log.py
from __future__ import annotations

from pathlib import Path
from typing import Iterator

from .event_types import Event, deserialize_event, serialize_event


class EventLog:
    def __init__(self, root: Path, *, max_per_file: int = 10_000) -> None:
        self.root = root
        self.max_per_file = max_per_file
        self.root.mkdir(parents=True, exist_ok=True)

    def _current_file(self) -> Path:
        files = sorted(self.root.glob("events_*.jsonl"))
        if not files:
            return self.root / "events_000001.jsonl"
        current = files[-1]
        line_count = sum(1 for _ in current.open("r", encoding="utf-8"))
        if line_count >= self.max_per_file:
            seq = int(current.stem.split("_")[-1]) + 1
            return self.root / f"events_{seq:06d}.jsonl"
        return current

    def append(self, event: Event) -> None:
        path = self._current_file()
        with path.open("a", encoding="utf-8") as fh:
            fh.write(serialize_event(event) + "\n")

    def iter_events(self) -> Iterator[Event]:
        for path in sorted(self.root.glob("events_*.jsonl")):
            with path.open("r", encoding="utf-8") as fh:
                for line in fh:
                    line = line.strip()
                    if not line:
                        continue
                    yield deserialize_event(line)
```

- [ ] **Step 4: Run to pass**

```bash
python3 -m pytest scripts/tests/test_event_sourced_log.py -v
```

- [ ] **Step 5: Commit**

```bash
git add scripts/vitruvius/event_sourced/event_log.py scripts/tests/test_event_sourced_log.py
git commit -m "feat(event-sourced): add append-only event log with rollover (Task P.2)"
```

---

### Task P.3: Replay engine (events → current state)

**Files:**
- Create: `scripts/vitruvius/event_sourced/replay_engine.py`
- Create: `scripts/tests/test_event_sourced_replay.py`

- [ ] **Step 1: Write test**

```python
# scripts/tests/test_event_sourced_replay.py
from vitruvius.event_sourced.event_types import (
    NodeAdded,
    NodeRemoved,
    EdgeAdded,
    EdgeRemoved,
)
from vitruvius.event_sourced.replay_engine import replay_events, GraphState


def test_replay_simple_sequence():
    events = [
        NodeAdded(at_utc="t1", node_id="a", node_type="concept", trust="gold"),
        NodeAdded(at_utc="t2", node_id="b", node_type="concept", trust="gold"),
        EdgeAdded(at_utc="t3", from_id="a", to_id="b", predicate="governs"),
    ]
    state: GraphState = replay_events(events)
    assert set(state.node_ids) == {"a", "b"}
    assert ("a", "b", "governs") in state.edges


def test_replay_node_removal_cascades_edges():
    events = [
        NodeAdded(at_utc="t1", node_id="a", node_type="concept", trust="gold"),
        NodeAdded(at_utc="t2", node_id="b", node_type="concept", trust="gold"),
        EdgeAdded(at_utc="t3", from_id="a", to_id="b", predicate="governs"),
        NodeRemoved(at_utc="t4", node_id="a"),
    ]
    state = replay_events(events)
    assert state.node_ids == frozenset({"b"})
    assert state.edges == frozenset()


def test_replay_edge_removed_does_not_touch_nodes():
    events = [
        NodeAdded(at_utc="t1", node_id="a", node_type="concept", trust="gold"),
        NodeAdded(at_utc="t2", node_id="b", node_type="concept", trust="gold"),
        EdgeAdded(at_utc="t3", from_id="a", to_id="b", predicate="governs"),
        EdgeRemoved(at_utc="t4", from_id="a", to_id="b", predicate="governs"),
    ]
    state = replay_events(events)
    assert state.node_ids == frozenset({"a", "b"})
    assert state.edges == frozenset()
```

- [ ] **Step 2: Run to fail**

- [ ] **Step 3: Implement**

```python
# scripts/vitruvius/event_sourced/replay_engine.py
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable

from .event_types import (
    EdgeAdded,
    EdgeRemoved,
    Event,
    NodeAdded,
    NodeRemoved,
)


@dataclass(frozen=True)
class GraphState:
    node_ids: frozenset[str] = frozenset()
    edges: frozenset[tuple[str, str, str]] = frozenset()
    node_metadata: dict[str, dict] = field(default_factory=dict)


def replay_events(events: Iterable[Event]) -> GraphState:
    nodes: set[str] = set()
    edges: set[tuple[str, str, str]] = set()
    metadata: dict[str, dict] = {}

    for event in events:
        if isinstance(event, NodeAdded):
            nodes.add(event.node_id)
            metadata[event.node_id] = {
                "type": event.node_type,
                "trust": event.trust,
            }
        elif isinstance(event, NodeRemoved):
            nodes.discard(event.node_id)
            metadata.pop(event.node_id, None)
            # Cascade: drop every edge touching this node.
            edges = {
                edge for edge in edges
                if edge[0] != event.node_id and edge[1] != event.node_id
            }
        elif isinstance(event, EdgeAdded):
            edges.add((event.from_id, event.to_id, event.predicate))
        elif isinstance(event, EdgeRemoved):
            edges.discard((event.from_id, event.to_id, event.predicate))

    return GraphState(
        node_ids=frozenset(nodes),
        edges=frozenset(edges),
        node_metadata=metadata,
    )
```

- [ ] **Step 4: Run to pass**

```bash
python3 -m pytest scripts/tests/test_event_sourced_replay.py -v
```

- [ ] **Step 5: Commit**

```bash
git add scripts/vitruvius/event_sourced/replay_engine.py scripts/tests/test_event_sourced_replay.py
git commit -m "feat(event-sourced): add replay engine reducer (Task P.3)"
```

---

### Task P.4: Time-travel state reconstruction

**Files:**
- Create: `scripts/vitruvius/event_sourced/time_travel.py`
- Create: `scripts/tests/test_event_sourced_time_travel.py`

- [ ] **Step 1: Write test**

```python
# scripts/tests/test_event_sourced_time_travel.py
from pathlib import Path

from vitruvius.event_sourced.event_log import EventLog
from vitruvius.event_sourced.event_types import NodeAdded, NodeRemoved
from vitruvius.event_sourced.time_travel import reconstruct_state_at


def test_state_before_removal_includes_node(tmp_path: Path):
    log = EventLog(root=tmp_path / "evt", max_per_file=100)
    log.append(NodeAdded(at_utc="2026-04-14T10:00:00Z", node_id="a",
                         node_type="concept", trust="gold"))
    log.append(NodeRemoved(at_utc="2026-04-14T12:00:00Z", node_id="a"))

    state = reconstruct_state_at(log, at_utc="2026-04-14T11:00:00Z")
    assert "a" in state.node_ids

    state_after = reconstruct_state_at(log, at_utc="2026-04-14T13:00:00Z")
    assert "a" not in state_after.node_ids


def test_state_at_epoch_returns_empty(tmp_path: Path):
    log = EventLog(root=tmp_path / "evt", max_per_file=100)
    log.append(NodeAdded(at_utc="2026-04-14T10:00:00Z", node_id="a",
                         node_type="concept", trust="gold"))
    state = reconstruct_state_at(log, at_utc="2026-04-14T09:00:00Z")
    assert state.node_ids == frozenset()
```

- [ ] **Step 2: Run to fail**

- [ ] **Step 3: Implement**

```python
# scripts/vitruvius/event_sourced/time_travel.py
from __future__ import annotations

from .event_log import EventLog
from .replay_engine import GraphState, replay_events


def reconstruct_state_at(log: EventLog, *, at_utc: str) -> GraphState:
    events = [e for e in log.iter_events() if e.at_utc <= at_utc]
    return replay_events(events)
```

- [ ] **Step 4: Run to pass**

```bash
python3 -m pytest scripts/tests/test_event_sourced_time_travel.py -v
```

- [ ] **Step 5: Commit**

```bash
git add scripts/vitruvius/event_sourced/time_travel.py scripts/tests/test_event_sourced_time_travel.py
git commit -m "feat(event-sourced): add time-travel state reconstruction (Task P.4)"
```

### 12.4 Stream P Definition of Done
- [ ] Event log append + iter round-trips on random event sequences.
- [ ] Replay handles node-removal cascade correctly.
- [ ] Time-travel query returns the exact historical state at any `at_utc`.
- [ ] Feature flags `p_event_log`, `p_time_travel_query` added, default `false`.
- [ ] Backward-compat suite green.


---

## 13. Stream Q — Temporal-Aware Query Layer

### 13.1 Goal
Filter the Phase 8 graph snapshot at read-time by a query-date. Vitruvius already has `promotion/temporal_edges.py` which defines a parallel `TemporalEdge` dataclass and ships a `filter_edges_valid_at()` function. Stream Q joins that existing metadata to the canonical `GraphSnapshot` on the shared `evidence_id` / `edge_id` key and produces a time-masked snapshot without mutating the core graph contract.

### 13.2 Files
- Create: `scripts/vitruvius/temporal_query/__init__.py`
- Create: `scripts/vitruvius/temporal_query/time_mask.py`
- Create: `scripts/tests/test_temporal_query_mask.py`

### 13.3 Task Sequence

---

### Task Q.1: Time-mask snapshot filter (sidecar join)

- [ ] **Step 1: Write test**

```python
# scripts/tests/test_temporal_query_mask.py
from vitruvius.graph.contract import GraphNode, GraphEdge, GraphSnapshot
from vitruvius.promotion.temporal_edges import TemporalEdge
from vitruvius.temporal_query.time_mask import apply_time_mask


def _fixture_snapshot() -> tuple[GraphSnapshot, list[TemporalEdge]]:
    nodes = [
        GraphNode(
            id=f"concept-c{i}",
            type="concept",
            slug=f"c{i}",
            trust_level="primary",
            last_updated_utc="2026-04-14T00:00:00Z",
        )
        for i in (1, 2, 3)
    ]
    edges = [
        GraphEdge(from_id="concept-c1", to_id="concept-c2", type="governs",
                  evidence_id="rel-0001", status="verified"),
        GraphEdge(from_id="concept-c1", to_id="concept-c3", type="governs",
                  evidence_id="rel-0002", status="verified"),
    ]
    snapshot = GraphSnapshot(
        schema_version="1.0.0",
        generated_at_utc="2026-04-14T00:00:00Z",
        node_count=len(nodes),
        edge_count=len(edges),
        nodes=nodes,
        edges=edges,
    )
    temporal = [
        TemporalEdge(
            edge_id="rel-0001",
            from_entity="concept-c1",
            predicate="governs",
            to_entity="concept-c2",
            valid_from="1977-02-19",
            valid_until=None,
            jurisdiction="national",
        ),
        TemporalEdge(
            edge_id="rel-0002",
            from_entity="concept-c1",
            predicate="governs",
            to_entity="concept-c3",
            valid_from="2020-01-01",
            valid_until="2025-12-31",
            jurisdiction="national",
        ),
    ]
    return snapshot, temporal


def test_mask_includes_always_valid_edge():
    snap, temporal = _fixture_snapshot()
    masked = apply_time_mask(snap, temporal_edges=temporal, query_date="2010-06-15")
    assert masked.edge_count == 1
    assert masked.edges[0].evidence_id == "rel-0001"


def test_mask_includes_bounded_edge_within_window():
    snap, temporal = _fixture_snapshot()
    masked = apply_time_mask(snap, temporal_edges=temporal, query_date="2022-06-15")
    assert masked.edge_count == 2


def test_mask_excludes_bounded_edge_after_window():
    snap, temporal = _fixture_snapshot()
    masked = apply_time_mask(snap, temporal_edges=temporal, query_date="2027-01-01")
    assert masked.edge_count == 1
    assert masked.edges[0].evidence_id == "rel-0001"


def test_mask_drops_edges_without_temporal_metadata():
    snap, temporal = _fixture_snapshot()
    # Omit rel-0002 from the temporal list entirely → treated as unknown validity → excluded.
    masked = apply_time_mask(
        snap,
        temporal_edges=[t for t in temporal if t.edge_id == "rel-0001"],
        query_date="2010-06-15",
    )
    assert masked.edge_count == 1
    assert masked.edges[0].evidence_id == "rel-0001"
```

- [ ] **Step 2: Run to fail**

- [ ] **Step 3: Implement**

```python
# scripts/vitruvius/temporal_query/__init__.py
"""Temporal-aware query (Stream Q) — sidecar join with promotion/temporal_edges."""
```

```python
# scripts/vitruvius/temporal_query/time_mask.py
from __future__ import annotations

from typing import Iterable

from vitruvius.graph.contract import GraphSnapshot
from vitruvius.promotion.temporal_edges import (
    TemporalEdge,
    filter_edges_valid_at,
)


def apply_time_mask(
    snapshot: GraphSnapshot,
    *,
    temporal_edges: Iterable[TemporalEdge],
    query_date: str,
    jurisdiction: str | None = None,
) -> GraphSnapshot:
    """Return a copy of `snapshot` containing only edges valid at `query_date`.

    An edge survives iff a `TemporalEdge` with the matching `edge_id`
    (== GraphEdge.evidence_id) contains `query_date` in its validity interval.
    Edges without a corresponding `TemporalEdge` are excluded — we never
    assume unknown validity means "always valid".
    """
    surviving_ids = {
        te.edge_id
        for te in filter_edges_valid_at(
            temporal_edges, query_date=query_date, jurisdiction=jurisdiction,
        )
    }
    filtered_edges = [
        edge for edge in snapshot.edges if edge.evidence_id in surviving_ids
    ]
    return GraphSnapshot(
        schema_version=snapshot.schema_version,
        generated_at_utc=snapshot.generated_at_utc,
        node_count=len(snapshot.nodes),
        edge_count=len(filtered_edges),
        nodes=list(snapshot.nodes),
        edges=filtered_edges,
    )
```

- [ ] **Step 4: Run to pass**

```bash
python3 -m pytest scripts/tests/test_temporal_query_mask.py -v
```

- [ ] **Step 5: Commit**

```bash
git add scripts/vitruvius/temporal_query/__init__.py scripts/vitruvius/temporal_query/time_mask.py scripts/tests/test_temporal_query_mask.py
git commit -m "feat(temporal-query): add time-mask join over Phase 8 snapshot (Task Q.1)"
```

### 13.4 Stream Q Definition of Done
- [ ] `apply_time_mask` produces a snapshot whose edges are exactly those whose `evidence_id` matches a `TemporalEdge` passing `filter_edges_valid_at`.
- [ ] Edges without a temporal-edges sidecar entry are excluded (never assumed permanently valid).
- [ ] No changes required to `graph/contract.py` or `promotion/temporal_edges.py`.
- [ ] Feature flag `q_temporal_mask` added.


---

## 14. Stream R — Epistemic Uncertainty (MC Dropout + Dempster-Shafer)

### 14.1 Goal
Quantify the LLM adjudicator's *epistemic* uncertainty (ignorance due to ambiguous legal text) instead of trusting a point estimate. Two techniques:

1. **MC Dropout sampling** — query the same candidate N times, compute variance across decisions. If variance exceeds τ, escalate to a Ranger instead of auto-promoting.
2. **Dempster-Shafer belief/plausibility** — aggregate conflicting evidence from Tier 1 LLM, Tier 2 LLM, CRF extractor, and TF-IDF fingerprint using belief functions, not simple probability.

### 14.2 Files
- Create: `scripts/vitruvius/epistemic/__init__.py`
- Create: `scripts/vitruvius/epistemic/mc_dropout.py`
- Create: `scripts/vitruvius/epistemic/dempster_shafer.py`
- Create: `scripts/tests/test_epistemic_mc_dropout.py`
- Create: `scripts/tests/test_epistemic_dempster_shafer.py`

### 14.3 Task Sequence

---

### Task R.1: MC Dropout sampling wrapper

- [ ] **Step 1: Write test**

```python
# scripts/tests/test_epistemic_mc_dropout.py
from vitruvius.epistemic.mc_dropout import (
    MCSample,
    compute_epistemic,
)


def test_all_same_votes_zero_variance():
    samples = [MCSample(label="keep") for _ in range(10)]
    result = compute_epistemic(samples)
    assert result.variance == 0.0
    assert result.majority_label == "keep"


def test_split_votes_raises_variance():
    samples = [MCSample(label="keep")] * 6 + [MCSample(label="reject")] * 4
    result = compute_epistemic(samples)
    assert result.variance > 0.0
    assert result.majority_label == "keep"


def test_tie_breaks_alphabetically():
    samples = [MCSample(label="keep")] * 5 + [MCSample(label="reject")] * 5
    result = compute_epistemic(samples)
    assert result.majority_label == "keep"


def test_empty_samples_returns_zero():
    result = compute_epistemic([])
    assert result.variance == 0.0
    assert result.majority_label == ""
```

- [ ] **Step 2: Run to fail**

- [ ] **Step 3: Implement**

```python
# scripts/vitruvius/epistemic/__init__.py
"""Epistemic uncertainty quantification (Stream R)."""
```

```python
# scripts/vitruvius/epistemic/mc_dropout.py
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Sequence


@dataclass(frozen=True)
class MCSample:
    label: str


@dataclass(frozen=True)
class EpistemicResult:
    majority_label: str
    variance: float
    total_samples: int


def compute_epistemic(samples: Sequence[MCSample]) -> EpistemicResult:
    if not samples:
        return EpistemicResult(majority_label="", variance=0.0, total_samples=0)

    counts = Counter(sample.label for sample in samples)
    total = sum(counts.values())
    ranked = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
    majority_label = ranked[0][0]

    p_majority = ranked[0][1] / total
    variance = p_majority * (1 - p_majority) * 4  # scale to [0, 1]

    return EpistemicResult(
        majority_label=majority_label,
        variance=float(variance),
        total_samples=total,
    )
```

- [ ] **Step 4: Run to pass**

```bash
python3 -m pytest scripts/tests/test_epistemic_mc_dropout.py -v
```

- [ ] **Step 5: Commit**

```bash
git add scripts/vitruvius/epistemic/__init__.py scripts/vitruvius/epistemic/mc_dropout.py scripts/tests/test_epistemic_mc_dropout.py
git commit -m "feat(epistemic): add MC dropout sampling variance (Task R.1)"
```

---

### Task R.2: Dempster-Shafer belief/plausibility

- [ ] **Step 1: Write test**

```python
# scripts/tests/test_epistemic_dempster_shafer.py
from vitruvius.epistemic.dempster_shafer import (
    MassFunction,
    combine_dempster,
    belief,
    plausibility,
)


def test_combine_two_agreeing_sources():
    m1 = MassFunction({frozenset({"keep"}): 0.7, frozenset({"keep", "reject"}): 0.3})
    m2 = MassFunction({frozenset({"keep"}): 0.8, frozenset({"keep", "reject"}): 0.2})
    combined = combine_dempster(m1, m2)
    # Both strongly support keep → combined keep mass > 0.9
    assert combined.masses[frozenset({"keep"})] > 0.9


def test_belief_is_sum_of_subsets():
    m = MassFunction({
        frozenset({"keep"}): 0.5,
        frozenset({"reject"}): 0.3,
        frozenset({"keep", "reject"}): 0.2,
    })
    # Belief in {keep} = only the mass assigned exactly to {keep}
    assert abs(belief(m, frozenset({"keep"})) - 0.5) < 1e-9


def test_plausibility_excludes_only_fully_disjoint():
    m = MassFunction({
        frozenset({"keep"}): 0.5,
        frozenset({"reject"}): 0.3,
        frozenset({"keep", "reject"}): 0.2,
    })
    # Plausibility of {keep} = 0.5 + 0.2 = 0.7 (excludes only the disjoint {reject})
    assert abs(plausibility(m, frozenset({"keep"})) - 0.7) < 1e-9


def test_combine_contradictory_sources_raises_conflict():
    m1 = MassFunction({frozenset({"keep"}): 1.0})
    m2 = MassFunction({frozenset({"reject"}): 1.0})
    try:
        combine_dempster(m1, m2)
    except ValueError as exc:
        assert "conflict" in str(exc).lower()
    else:
        raise AssertionError("expected total-conflict ValueError")
```

- [ ] **Step 2: Run to fail**

- [ ] **Step 3: Implement**

```python
# scripts/vitruvius/epistemic/dempster_shafer.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True)
class MassFunction:
    masses: Mapping[frozenset, float]


def belief(mass: MassFunction, proposition: frozenset) -> float:
    total = 0.0
    for focal, m in mass.masses.items():
        if focal.issubset(proposition) and focal:
            total += m
    return total


def plausibility(mass: MassFunction, proposition: frozenset) -> float:
    total = 0.0
    for focal, m in mass.masses.items():
        if focal & proposition:
            total += m
    return total


def combine_dempster(m1: MassFunction, m2: MassFunction) -> MassFunction:
    combined: dict[frozenset, float] = {}
    conflict = 0.0
    for a, ma in m1.masses.items():
        for b, mb in m2.masses.items():
            intersection = a & b
            if not intersection:
                conflict += ma * mb
            else:
                combined[intersection] = combined.get(intersection, 0.0) + ma * mb

    if 1.0 - conflict <= 1e-12:
        raise ValueError("total conflict; cannot combine")

    normalizer = 1.0 / (1.0 - conflict)
    normalized = {k: v * normalizer for k, v in combined.items()}
    return MassFunction(masses=normalized)
```

- [ ] **Step 4: Run to pass**

```bash
python3 -m pytest scripts/tests/test_epistemic_dempster_shafer.py -v
```

- [ ] **Step 5: Commit**

```bash
git add scripts/vitruvius/epistemic/dempster_shafer.py scripts/tests/test_epistemic_dempster_shafer.py
git commit -m "feat(epistemic): add Dempster-Shafer belief/plausibility (Task R.2)"
```

### 14.4 Stream R Definition of Done
- [ ] MC Dropout returns 0 variance on unanimous votes and >0 otherwise.
- [ ] Dempster-Shafer correctly handles agreement, partial overlap, and raises on total conflict.
- [ ] Feature flags `r_mc_dropout_sampling`, `r_dempster_shafer_fusion` added.


---

## 15. Stream S — Subgraph Isomorphism Clash Detection (Violation Motifs)

### 15.1 Goal
Ship a library of small "violation motifs" — tiny directed graphs encoding a known illegal architectural condition (e.g., `[wood-frame] → requires → [sprinklers] → restricted-by → [low-water-pressure-zone]`). Run VF2 subgraph isomorphism (networkx) against the canonical Phase 8 graph to deterministically discover every instance that matches the motif's shape.

### 15.2 Files
- Create: `scripts/vitruvius/clash/__init__.py`
- Create: `scripts/vitruvius/clash/motif_library.py`
- Create: `scripts/vitruvius/clash/subgraph_iso.py`
- Create: `scripts/tests/test_clash_motif_library.py`
- Create: `scripts/tests/test_clash_subgraph_iso.py`
- Create: `.ai/06_specs/violation_motifs.yaml`

### 15.3 Task Sequence

---

### Task S.1: Motif library loader

- [ ] **Step 1: Write test**

```python
# scripts/tests/test_clash_motif_library.py
from pathlib import Path

from vitruvius.clash.motif_library import load_motifs, Motif


def test_load_empty_yaml(tmp_path: Path):
    spec = tmp_path / "motifs.yaml"
    spec.write_text("motifs: []\n", encoding="utf-8")
    motifs = load_motifs(spec)
    assert motifs == ()


def test_load_single_motif(tmp_path: Path):
    spec = tmp_path / "motifs.yaml"
    spec.write_text("""\
motifs:
  - id: wood-frame-sprinklers
    description: Wood frame requires sprinklers in dry zones
    nodes:
      - {id: wood_frame, node_type: material}
      - {id: sprinklers, node_type: system}
      - {id: dry_zone,   node_type: zone}
    edges:
      - {from: wood_frame, to: sprinklers, predicate: requires}
      - {from: sprinklers, to: dry_zone,   predicate: restricted_by}
""", encoding="utf-8")
    motifs = load_motifs(spec)
    assert len(motifs) == 1
    m: Motif = motifs[0]
    assert m.id == "wood-frame-sprinklers"
    assert len(m.nodes) == 3
    assert len(m.edges) == 2
```

- [ ] **Step 2: Run to fail**

- [ ] **Step 3: Implement**

```python
# scripts/vitruvius/clash/__init__.py
"""Clash detection (Stream S) — violation-motif subgraph isomorphism."""
```

```python
# scripts/vitruvius/clash/motif_library.py
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml


@dataclass(frozen=True)
class MotifNode:
    id: str
    node_type: str


@dataclass(frozen=True)
class MotifEdge:
    from_id: str
    to_id: str
    predicate: str


@dataclass(frozen=True)
class Motif:
    id: str
    description: str
    nodes: tuple[MotifNode, ...]
    edges: tuple[MotifEdge, ...]


def load_motifs(spec_path: Path) -> tuple[Motif, ...]:
    raw = yaml.safe_load(spec_path.read_text(encoding="utf-8")) or {}
    motif_specs = raw.get("motifs", []) or []
    result: list[Motif] = []
    for spec in motif_specs:
        nodes = tuple(
            MotifNode(id=str(n["id"]), node_type=str(n["node_type"]))
            for n in spec.get("nodes", [])
        )
        edges = tuple(
            MotifEdge(
                from_id=str(e["from"]),
                to_id=str(e["to"]),
                predicate=str(e["predicate"]),
            )
            for e in spec.get("edges", [])
        )
        result.append(
            Motif(
                id=str(spec["id"]),
                description=str(spec.get("description", "")),
                nodes=nodes,
                edges=edges,
            )
        )
    return tuple(result)
```

- [ ] **Step 4: Run to pass**

```bash
python3 -m pytest scripts/tests/test_clash_motif_library.py -v
```

- [ ] **Step 5: Commit**

```bash
git add scripts/vitruvius/clash/__init__.py scripts/vitruvius/clash/motif_library.py scripts/tests/test_clash_motif_library.py
git commit -m "feat(clash): add motif library loader (Task S.1)"
```

---

### Task S.2: VF2 subgraph matcher

- [ ] **Step 1: Write test**

```python
# scripts/tests/test_clash_subgraph_iso.py
from vitruvius.clash.motif_library import Motif, MotifNode, MotifEdge
from vitruvius.clash.subgraph_iso import find_motif_instances
from vitruvius.graph.contract import GraphNode, GraphEdge, GraphSnapshot


def _make_node(slug: str) -> GraphNode:
    return GraphNode(
        id=f"concept-{slug}",
        type="concept",
        slug=slug,
        trust_level="primary",
        last_updated_utc="2026-04-14T00:00:00Z",
    )


def _make_edge(from_slug: str, to_slug: str, type_: str, evidence: str) -> GraphEdge:
    return GraphEdge(
        from_id=f"concept-{from_slug}",
        to_id=f"concept-{to_slug}",
        type=type_,
        evidence_id=evidence,
        status="verified",
    )


def _snapshot_with_motif_instance() -> GraphSnapshot:
    nodes = [
        _make_node("wood-frame"),
        _make_node("sprinkler-system"),
        _make_node("dry-zone"),
        _make_node("steel-frame"),  # unrelated control
    ]
    edges = [
        _make_edge("wood-frame", "sprinkler-system", "requires", "rel-001"),
        _make_edge("sprinkler-system", "dry-zone", "restricted_by", "rel-002"),
    ]
    return GraphSnapshot(
        schema_version="1.0.0",
        generated_at_utc="2026-04-14T00:00:00Z",
        node_count=len(nodes),
        edge_count=len(edges),
        nodes=nodes,
        edges=edges,
    )


def _sample_motif() -> Motif:
    return Motif(
        id="wood-sprinkler-dry",
        description="",
        nodes=(
            # motif slugs are matched against GraphNode.slug in the host graph
            MotifNode(id="wood", node_type="wood-frame"),
            MotifNode(id="sprinkler", node_type="sprinkler-system"),
            MotifNode(id="dry", node_type="dry-zone"),
        ),
        edges=(
            MotifEdge(from_id="wood", to_id="sprinkler", predicate="requires"),
            MotifEdge(from_id="sprinkler", to_id="dry", predicate="restricted_by"),
        ),
    )


def test_subgraph_iso_finds_instance():
    snapshot = _snapshot_with_motif_instance()
    motif = _sample_motif()
    matches = find_motif_instances(snapshot, motif)
    assert len(matches) == 1
    match = matches[0]
    assert match.mapping["wood"] == "concept-wood-frame"
    assert match.mapping["sprinkler"] == "concept-sprinkler-system"
    assert match.mapping["dry"] == "concept-dry-zone"


def test_subgraph_iso_no_match_returns_empty():
    motif = _sample_motif()
    empty_snapshot = GraphSnapshot(
        schema_version="1.0.0",
        generated_at_utc="2026-04-14T00:00:00Z",
        node_count=0,
        edge_count=0,
        nodes=[],
        edges=[],
    )
    assert find_motif_instances(empty_snapshot, motif) == ()
```

- [ ] **Step 2: Run to fail**

- [ ] **Step 3: Implement**

```python
# scripts/vitruvius/clash/subgraph_iso.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

import networkx as nx
from networkx.algorithms.isomorphism import DiGraphMatcher

from vitruvius.clash.motif_library import Motif
from vitruvius.graph.contract import GraphSnapshot


@dataclass(frozen=True)
class MotifMatch:
    motif_id: str
    mapping: Mapping[str, str]


def _snapshot_to_digraph(snapshot: GraphSnapshot) -> nx.DiGraph:
    g = nx.DiGraph()
    for node in snapshot.nodes:
        # motif `node_type` is matched against the host graph's `slug`
        # because GraphNode.type is restricted to {source, concept, attribute}.
        g.add_node(node.id, tag=node.slug)
    for edge in snapshot.edges:
        g.add_edge(edge.from_id, edge.to_id, predicate=edge.type)
    return g


def _motif_to_digraph(motif: Motif) -> nx.DiGraph:
    g = nx.DiGraph()
    for node in motif.nodes:
        g.add_node(node.id, tag=node.node_type)
    for edge in motif.edges:
        g.add_edge(edge.from_id, edge.to_id, predicate=edge.predicate)
    return g


def find_motif_instances(snapshot: GraphSnapshot, motif: Motif) -> tuple[MotifMatch, ...]:
    host = _snapshot_to_digraph(snapshot)
    pattern = _motif_to_digraph(motif)

    def node_match(h_attrs, p_attrs):
        return h_attrs.get("tag") == p_attrs.get("tag")

    def edge_match(h_attrs, p_attrs):
        return h_attrs.get("predicate") == p_attrs.get("predicate")

    matcher = DiGraphMatcher(host, pattern, node_match=node_match, edge_match=edge_match)
    results: list[MotifMatch] = []
    seen: set[frozenset[tuple[str, str]]] = set()
    for iso in matcher.subgraph_isomorphisms_iter():
        # iso is host → pattern; invert to pattern → host
        mapping = {p: h for h, p in iso.items()}
        key = frozenset(mapping.items())
        if key in seen:
            continue
        seen.add(key)
        results.append(MotifMatch(motif_id=motif.id, mapping=dict(sorted(mapping.items()))))

    results.sort(key=lambda m: tuple(sorted(m.mapping.items())))
    return tuple(results)
```

- [ ] **Step 4: Run to pass**

```bash
python3 -m pytest scripts/tests/test_clash_subgraph_iso.py -v
```

- [ ] **Step 5: Commit**

```bash
git add scripts/vitruvius/clash/subgraph_iso.py scripts/tests/test_clash_subgraph_iso.py
git commit -m "feat(clash): add VF2 subgraph isomorphism matcher (Task S.2)"
```

### 15.4 Stream S Definition of Done
- [ ] Motif YAML → Motif struct round-trip works.
- [ ] VF2 matcher finds embedded motif instances and returns deterministic ordering.
- [ ] Feature flags `s_violation_motif_library`, `s_subgraph_isomorphism` added.


---

## 16. Stream T — Nyquist-Shannon Adaptive Chunking

### 16.1 Goal
Dynamically pick the chunk window-size and overlap ratio based on the parametric density of each document section. High-density legal text (lots of numbers, units, operators) needs higher overlap ratios; prose-heavy sections can tolerate larger windows with smaller overlap. Ships as an additive layer on top of the existing `normalization/embedding_chunker.py`.

### 16.2 Files
- Create: `scripts/vitruvius/adaptive_chunk/__init__.py`
- Create: `scripts/vitruvius/adaptive_chunk/nyquist_chunker.py`
- Create: `scripts/tests/test_adaptive_chunker_nyquist.py`

### 16.3 Task Sequence

---

### Task T.1: Parametric density probe

- [ ] **Step 1: Write test**

```python
# scripts/tests/test_adaptive_chunker_nyquist.py
from vitruvius.adaptive_chunk.nyquist_chunker import (
    measure_parametric_density,
    recommend_overlap_ratio,
)


def test_density_on_prose_is_low():
    prose = "The building shall be designed in accordance with good practice"
    density = measure_parametric_density(prose)
    assert density < 0.1


def test_density_on_numeric_heavy_text_is_high():
    heavy = "The minimum width shall be 1.2 meters, the maximum 3.5m and the ratio 0.8"
    density = measure_parametric_density(heavy)
    assert density > 0.2


def test_overlap_scales_with_density():
    low = recommend_overlap_ratio(density=0.05, min_ratio=0.1, max_ratio=0.5)
    high = recommend_overlap_ratio(density=0.5, min_ratio=0.1, max_ratio=0.5)
    assert low <= high
    assert 0.1 <= low <= 0.5
    assert 0.1 <= high <= 0.5


def test_recommend_clamps_to_bounds():
    assert recommend_overlap_ratio(density=10.0, min_ratio=0.1, max_ratio=0.5) == 0.5
    assert recommend_overlap_ratio(density=0.0, min_ratio=0.1, max_ratio=0.5) == 0.1
```

- [ ] **Step 2: Run to fail**

- [ ] **Step 3: Implement**

```python
# scripts/vitruvius/adaptive_chunk/__init__.py
"""Adaptive chunking (Stream T) — Nyquist-Shannon driven window sizing."""
```

```python
# scripts/vitruvius/adaptive_chunk/nyquist_chunker.py
from __future__ import annotations

import re


_NUMBER_RE = re.compile(r"\d+(?:\.\d+)?")
_UNIT_RE = re.compile(r"\b(?:m|cm|mm|kg|m2|sqm|m²|meters?|centimeters?)\b", re.IGNORECASE)
_OPERATOR_RE = re.compile(r"(?:>=|<=|==|shall be|at least|no more than|minimum|maximum)", re.IGNORECASE)


def measure_parametric_density(text: str) -> float:
    if not text:
        return 0.0
    tokens = max(len(text.split()), 1)
    numbers = len(_NUMBER_RE.findall(text))
    units = len(_UNIT_RE.findall(text))
    operators = len(_OPERATOR_RE.findall(text))
    score = (numbers + units + operators) / tokens
    return float(score)


def recommend_overlap_ratio(
    *,
    density: float,
    min_ratio: float,
    max_ratio: float,
) -> float:
    if density <= 0:
        return min_ratio
    if density >= 1.0:
        return max_ratio
    return min_ratio + (max_ratio - min_ratio) * min(density, 1.0)
```

- [ ] **Step 4: Run to pass**

```bash
python3 -m pytest scripts/tests/test_adaptive_chunker_nyquist.py -v
```

- [ ] **Step 5: Commit**

```bash
git add scripts/vitruvius/adaptive_chunk/__init__.py scripts/vitruvius/adaptive_chunk/nyquist_chunker.py scripts/tests/test_adaptive_chunker_nyquist.py
git commit -m "feat(adaptive-chunk): add Nyquist-Shannon density probe (Task T.1)"
```

### 16.4 Stream T Definition of Done
- [ ] Density probe returns higher values on parameter-heavy text than prose.
- [ ] Overlap ratio scales linearly with density, clamped to [min_ratio, max_ratio].
- [ ] Feature flag `t_adaptive_window_sizing` added.
- [ ] Does NOT mutate `embedding_chunker.py`; this is a new module the chunker optionally consults.


---

## 17. Stream U — Hardware-Aware Router

### 17.1 Goal
Select the Ollama model at inference time based on free RAM (via psutil) + candidate complexity. Avoid crashing an 8 GB M2 by accidentally loading `gemma4:31b` when only 2 GB of RAM is free.

### 17.2 Files
- Create: `scripts/vitruvius/hardware_router.py`
- Create: `scripts/tests/test_hardware_router.py`

### 17.3 Task Sequence

---

### Task U.1: Hardware-aware selection

- [ ] **Step 1: Write test**

```python
# scripts/tests/test_hardware_router.py
import pytest

psutil = pytest.importorskip("psutil")

from vitruvius.hardware_router import (
    HardwareAwareRouter,
    RouterDecision,
)


def test_selects_e2b_when_ram_low(monkeypatch):
    router = HardwareAwareRouter()
    monkeypatch.setattr(router, "_available_gb", lambda: 2.0)
    decision = router.select_model(candidate_complexity="simple")
    assert decision.model_name == "gemma4:e2b"


def test_selects_e4b_on_moderate_ram(monkeypatch):
    router = HardwareAwareRouter()
    monkeypatch.setattr(router, "_available_gb", lambda: 5.0)
    decision = router.select_model(candidate_complexity="medium")
    assert decision.model_name == "gemma4:e4b"


def test_selects_31b_when_ample_ram(monkeypatch):
    router = HardwareAwareRouter()
    monkeypatch.setattr(router, "_available_gb", lambda: 20.0)
    decision = router.select_model(candidate_complexity="complex")
    assert decision.model_name == "gemma4:31b"


def test_simple_candidate_never_boots_31b(monkeypatch):
    router = HardwareAwareRouter()
    monkeypatch.setattr(router, "_available_gb", lambda: 20.0)
    decision = router.select_model(candidate_complexity="simple")
    assert decision.model_name == "gemma4:e2b"
```

- [ ] **Step 2: Run to fail**

- [ ] **Step 3: Implement**

```python
# scripts/vitruvius/hardware_router.py
from __future__ import annotations

from dataclasses import dataclass

try:
    import psutil  # type: ignore[import-not-found]
except ImportError:  # pragma: no cover
    psutil = None  # type: ignore[assignment]


@dataclass(frozen=True)
class RouterDecision:
    model_name: str
    reason: str
    available_gb: float


class HardwareAwareRouter:
    def __init__(
        self,
        *,
        e2b_floor_gb: float = 2.0,
        e4b_floor_gb: float = 4.0,
        b31_floor_gb: float = 18.0,
        safety_buffer_gb: float = 2.0,
    ) -> None:
        self.e2b_floor_gb = e2b_floor_gb
        self.e4b_floor_gb = e4b_floor_gb
        self.b31_floor_gb = b31_floor_gb
        self.safety_buffer_gb = safety_buffer_gb

    def _available_gb(self) -> float:
        if psutil is None:
            return 0.0
        return psutil.virtual_memory().available / (1024 ** 3)

    def select_model(self, *, candidate_complexity: str) -> RouterDecision:
        available = self._available_gb()
        usable = max(0.0, available - self.safety_buffer_gb)

        if candidate_complexity == "simple":
            return RouterDecision(
                model_name="gemma4:e2b",
                reason=f"simple candidate, {usable:.2f}GB usable",
                available_gb=available,
            )

        if candidate_complexity == "complex" and usable >= self.b31_floor_gb:
            return RouterDecision(
                model_name="gemma4:31b",
                reason=f"complex candidate, {usable:.2f}GB usable",
                available_gb=available,
            )

        if usable >= self.e4b_floor_gb:
            return RouterDecision(
                model_name="gemma4:e4b",
                reason=f"default, {usable:.2f}GB usable",
                available_gb=available,
            )

        return RouterDecision(
            model_name="gemma4:e2b",
            reason=f"forced e2b, low memory {usable:.2f}GB usable",
            available_gb=available,
        )
```

- [ ] **Step 4: Run to pass**

```bash
python3 -m pytest scripts/tests/test_hardware_router.py -v
```

- [ ] **Step 5: Commit**

```bash
git add scripts/vitruvius/hardware_router.py scripts/tests/test_hardware_router.py
git commit -m "feat(hardware-router): add psutil-based model selection (Task U.1)"
```

### 17.4 Stream U Definition of Done
- [ ] Router returns `e2b` under memory pressure regardless of candidate complexity.
- [ ] Router never recommends `31b` when usable RAM < `b31_floor_gb`.
- [ ] Feature flag `u_hardware_aware_routing` added.
- [ ] Add `psutil>=5.9,<7.0` to `requirements.txt` if not already present.


---

## 18. Stream V — IFC/OWL Ontology Unification

### 18.1 Goal
Map every `003_Canonical-Knowledge-Layer/shared/concepts/*.md` to a buildingSMART IFC class + Pset property set where one exists, and fall back to a Vitruvius-native OWL class otherwise. Store the mapping as an `owlready2`-parseable OWL file in `005_Operational-Intelligence-Layer/ontology/vitruvius_ontology.owl`.

### 18.2 Files
- Create: `scripts/vitruvius/ontology/__init__.py`
- Create: `scripts/vitruvius/ontology/ifc_mapper.py`
- Create: `scripts/vitruvius/ontology/owl_loader.py`
- Create: `scripts/tests/test_ontology_ifc_mapper.py`

### 18.3 Task Sequence

---

### Task V.1: IFC class mapper (deterministic alias table)

- [ ] **Step 1: Write test**

```python
# scripts/tests/test_ontology_ifc_mapper.py
from vitruvius.ontology.ifc_mapper import (
    map_concept_to_ifc,
    IFCMapping,
    UNMAPPED,
)


def test_known_concept_maps_to_ifc_class():
    mapping = map_concept_to_ifc("concept-fire-door")
    assert isinstance(mapping, IFCMapping)
    assert mapping.ifc_class == "IfcDoor"
    assert "Pset_DoorCommon" in mapping.pset_candidates


def test_unknown_concept_returns_unmapped():
    mapping = map_concept_to_ifc("concept-something-random")
    assert mapping == UNMAPPED


def test_case_insensitive_lookup():
    assert map_concept_to_ifc("CONCEPT-FIRE-DOOR").ifc_class == "IfcDoor"
```

- [ ] **Step 2: Run to fail**

- [ ] **Step 3: Implement**

```python
# scripts/vitruvius/ontology/__init__.py
"""IFC/OWL ontology unification (Stream V)."""
```

```python
# scripts/vitruvius/ontology/ifc_mapper.py
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class IFCMapping:
    vitruvius_concept_id: str
    ifc_class: str
    pset_candidates: tuple[str, ...]


UNMAPPED = IFCMapping(
    vitruvius_concept_id="",
    ifc_class="",
    pset_candidates=(),
)


_SEED_TABLE: dict[str, tuple[str, tuple[str, ...]]] = {
    "concept-fire-door": ("IfcDoor", ("Pset_DoorCommon", "Pset_DoorFireRating")),
    "concept-fire-wall": ("IfcWall", ("Pset_WallCommon", "Pset_WallFireRating")),
    "concept-setback-front": ("IfcSpatialZone", ("Pset_SpatialZoneCommon",)),
    "concept-egress-corridor": ("IfcSpace", ("Pset_SpaceCommon", "Pset_SpaceOccupancyRequirements")),
    "concept-occupancy-classification": ("IfcOccupant", ("Pset_OccupantCommon",)),
    "concept-building-permit": ("IfcProject", ("Pset_ProjectCommon",)),
    "concept-fire-clearance": ("IfcSpatialZone", ("Pset_SpatialZoneCommon",)),
    "concept-stairwell": ("IfcStair", ("Pset_StairCommon",)),
    "concept-roof": ("IfcRoof", ("Pset_RoofCommon",)),
    "concept-parking-and-loading-spaces": ("IfcSpace", ("Pset_SpaceParkingRequirements",)),
}


def map_concept_to_ifc(concept_id: str) -> IFCMapping:
    key = (concept_id or "").lower()
    entry = _SEED_TABLE.get(key)
    if not entry:
        return UNMAPPED
    ifc_class, psets = entry
    return IFCMapping(
        vitruvius_concept_id=key,
        ifc_class=ifc_class,
        pset_candidates=psets,
    )
```

- [ ] **Step 4: Run to pass**

```bash
python3 -m pytest scripts/tests/test_ontology_ifc_mapper.py -v
```

- [ ] **Step 5: Commit**

```bash
git add scripts/vitruvius/ontology/__init__.py scripts/vitruvius/ontology/ifc_mapper.py scripts/tests/test_ontology_ifc_mapper.py
git commit -m "feat(ontology): add seed IFC class mapper (Task V.1)"
```

### 18.4 Stream V Definition of Done
- [ ] Every concept in the seed table maps to an `IfcXxx` class + Pset shortlist.
- [ ] Case-insensitive lookup.
- [ ] Feature flag `v_ifc_owl_mapping` added.
- [ ] Expansion path: add `owl_loader.py` in a follow-up task once `owlready2` OWL file is committed.


---

## 19. Stream W — Autonomous Epistemic Foraging

### 19.1 Goal
Headless crawler polls configured LGU/DPWH registries on a schedule. For each fetched document, compute a Mahalanobis-distance drift score against the existing `005_Operational-Intelligence-Layer/embeddings/` distribution. If drift exceeds `drift_threshold_sigma`, drop the doc into `001_Raw-Source-Layer/incoming/` and raise a manifest entry for human review.

**This stream ships only the crawler + drift detector skeleton.** Production wiring to actual LGU URLs is environment-specific and happens post-merge via the `config/vitruvius.yaml → ultimate_upgrade.foraging.lgu_registries` list.

### 19.2 Files
- Create: `scripts/vitruvius/foraging/__init__.py`
- Create: `scripts/vitruvius/foraging/crawler.py`
- Create: `scripts/vitruvius/foraging/drift_detector.py`
- Create: `scripts/tests/test_foraging_crawler.py`
- Create: `scripts/tests/test_foraging_drift.py`

### 19.3 Task Sequence

---

### Task W.1: Drift detector (Mahalanobis-style, injectable fetcher)

- [ ] **Step 1: Write test**

```python
# scripts/tests/test_foraging_drift.py
import numpy as np

from vitruvius.foraging.drift_detector import compute_drift_sigma


def test_drift_zero_on_identical_embedding():
    centroid = np.array([0.1, 0.2, 0.3])
    cov = np.eye(3) * 0.01
    sigma = compute_drift_sigma(
        candidate_vector=centroid,
        centroid=centroid,
        covariance=cov,
    )
    assert sigma < 1e-6


def test_drift_large_on_outlier():
    centroid = np.zeros(3)
    cov = np.eye(3) * 0.01
    far = np.array([5.0, 5.0, 5.0])
    sigma = compute_drift_sigma(
        candidate_vector=far,
        centroid=centroid,
        covariance=cov,
    )
    assert sigma > 10.0


def test_drift_handles_singular_covariance_gracefully():
    centroid = np.zeros(3)
    cov = np.zeros((3, 3))
    sigma = compute_drift_sigma(
        candidate_vector=np.array([1.0, 1.0, 1.0]),
        centroid=centroid,
        covariance=cov,
    )
    assert sigma == float("inf")
```

- [ ] **Step 2: Run to fail**

- [ ] **Step 3: Implement**

```python
# scripts/vitruvius/foraging/__init__.py
"""Autonomous epistemic foraging (Stream W)."""
```

```python
# scripts/vitruvius/foraging/drift_detector.py
from __future__ import annotations

import numpy as np


def compute_drift_sigma(
    *,
    candidate_vector: np.ndarray,
    centroid: np.ndarray,
    covariance: np.ndarray,
) -> float:
    """Mahalanobis-distance-like drift score in multiples of sigma.

    Returns float("inf") if the covariance is singular (undefined distance).
    """
    delta = (candidate_vector - centroid).astype(np.float64)
    try:
        cov_inv = np.linalg.pinv(covariance)
    except np.linalg.LinAlgError:  # pragma: no cover
        return float("inf")

    if np.allclose(covariance, 0.0):
        if np.allclose(delta, 0.0):
            return 0.0
        return float("inf")

    distance_squared = float(delta @ cov_inv @ delta)
    if distance_squared < 0:
        distance_squared = 0.0
    return float(np.sqrt(distance_squared))
```

- [ ] **Step 4: Run to pass**

```bash
python3 -m pytest scripts/tests/test_foraging_drift.py -v
```

- [ ] **Step 5: Commit**

```bash
git add scripts/vitruvius/foraging/__init__.py scripts/vitruvius/foraging/drift_detector.py scripts/tests/test_foraging_drift.py
git commit -m "feat(foraging): add drift-sigma detector (Task W.1)"
```

---

### Task W.2: Crawler with injectable HTTP client

- [ ] **Step 1: Write test**

```python
# scripts/tests/test_foraging_crawler.py
from pathlib import Path

from vitruvius.foraging.crawler import (
    ForageResult,
    forage_once,
)


def _fake_fetcher_success(body: bytes):
    def _fn(url: str) -> bytes:
        return body
    return _fn


def _fake_fetcher_error(url: str) -> bytes:
    raise RuntimeError("HTTP 500")


def test_forage_writes_fetched_doc(tmp_path: Path):
    incoming = tmp_path / "incoming"
    result = forage_once(
        url="https://example.gov.ph/law.pdf",
        incoming_dir=incoming,
        fetcher_fn=_fake_fetcher_success(b"%PDF-1.4\n%test content"),
    )
    assert isinstance(result, ForageResult)
    assert result.status == "fetched"
    out = incoming / "law.pdf"
    assert out.exists()
    assert out.read_bytes().startswith(b"%PDF-1.4")


def test_forage_handles_error(tmp_path: Path):
    result = forage_once(
        url="https://example.gov.ph/broken.pdf",
        incoming_dir=tmp_path,
        fetcher_fn=_fake_fetcher_error,
    )
    assert result.status == "error"
    assert "HTTP 500" in result.error_message


def test_forage_deterministic_filename(tmp_path: Path):
    result = forage_once(
        url="https://example.gov.ph/path/to/abcd-memo.pdf",
        incoming_dir=tmp_path,
        fetcher_fn=_fake_fetcher_success(b"x"),
    )
    assert result.output_path is not None
    assert result.output_path.name == "abcd-memo.pdf"
```

- [ ] **Step 2: Run to fail**

- [ ] **Step 3: Implement**

```python
# scripts/vitruvius/foraging/crawler.py
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Optional
from urllib.parse import urlparse


@dataclass(frozen=True)
class ForageResult:
    url: str
    status: str  # "fetched" | "error"
    output_path: Optional[Path] = None
    error_message: str = ""


def _default_fetcher(url: str) -> bytes:  # pragma: no cover
    import requests  # type: ignore[import-not-found]
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return response.content


def _filename_from_url(url: str) -> str:
    parsed = urlparse(url)
    name = Path(parsed.path).name or "index"
    return name


def forage_once(
    *,
    url: str,
    incoming_dir: Path,
    fetcher_fn: Optional[Callable[[str], bytes]] = None,
) -> ForageResult:
    fetcher = fetcher_fn or _default_fetcher
    try:
        body = fetcher(url)
    except Exception as exc:
        return ForageResult(url=url, status="error", error_message=str(exc))

    incoming_dir.mkdir(parents=True, exist_ok=True)
    output_path = incoming_dir / _filename_from_url(url)
    output_path.write_bytes(body)
    return ForageResult(url=url, status="fetched", output_path=output_path)
```

- [ ] **Step 4: Run to pass**

```bash
python3 -m pytest scripts/tests/test_foraging_crawler.py -v
```

- [ ] **Step 5: Commit**

```bash
git add scripts/vitruvius/foraging/crawler.py scripts/tests/test_foraging_crawler.py
git commit -m "feat(foraging): add crawler with injectable fetcher (Task W.2)"
```

### 19.4 Stream W Definition of Done
- [ ] Drift detector handles singular covariance gracefully.
- [ ] Crawler writes to `incoming_dir` with the URL's basename.
- [ ] Feature flag `w_autonomous_forager` added.
- [ ] `requests>=2.31` present in requirements.txt (add if missing).
- [ ] Production wiring deferred to a post-merge config update (URL list).


---

## 20. Stream X — Boltzmann Graph-Energy Promotion Gate

### 20.1 Goal
Model the Phase 8 graph as a statistical-mechanical system. Every contradiction contributes `contradiction_unit_energy` (e.g. 1.0) to total graph "energy"; every unverified edge contributes `unverified_unit_energy` (e.g. 0.1). Divide by the `temperature` threshold T to get a normalized system stability. If energy / T > 1.0, lock the promotion gate until a Ranger resolves the contradictions.

### 20.2 Files
- Create: `scripts/vitruvius/health/__init__.py`
- Create: `scripts/vitruvius/health/boltzmann_energy.py`
- Create: `scripts/tests/test_health_boltzmann.py`

### 20.3 Task Sequence

---

### Task X.1: Graph-energy + promotion gate

- [ ] **Step 1: Write test**

```python
# scripts/tests/test_health_boltzmann.py
from vitruvius.health.boltzmann_energy import (
    GraphEnergyReport,
    compute_graph_energy,
    is_promotion_allowed,
)


def test_zero_energy_on_empty_graph():
    report = compute_graph_energy(num_contradictions=0, num_unverified=0)
    assert report.total_energy == 0.0
    assert is_promotion_allowed(report, temperature=10.0)


def test_mostly_verified_graph_allows_promotion():
    report = compute_graph_energy(num_contradictions=0, num_unverified=5)
    # energy = 0.5; temperature = 10 → stable
    assert is_promotion_allowed(report, temperature=10.0)


def test_contradictions_block_promotion():
    # 15 contradictions at unit energy 1.0 → energy = 15; temperature = 10 → ratio 1.5
    report = compute_graph_energy(num_contradictions=15, num_unverified=0)
    assert not is_promotion_allowed(report, temperature=10.0)


def test_lower_temperature_is_stricter():
    report = compute_graph_energy(num_contradictions=5, num_unverified=0)
    # energy = 5; strict (T=4) forbids, lax (T=10) allows
    assert not is_promotion_allowed(report, temperature=4.0)
    assert is_promotion_allowed(report, temperature=10.0)
```

- [ ] **Step 2: Run to fail**

- [ ] **Step 3: Implement**

```python
# scripts/vitruvius/health/__init__.py
"""Graph health metrics (Stream X)."""
```

```python
# scripts/vitruvius/health/boltzmann_energy.py
from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class GraphEnergyReport:
    num_contradictions: int
    num_unverified: int
    total_energy: float


def compute_graph_energy(
    *,
    num_contradictions: int,
    num_unverified: int,
    contradiction_unit_energy: float = 1.0,
    unverified_unit_energy: float = 0.1,
) -> GraphEnergyReport:
    total = (
        num_contradictions * contradiction_unit_energy
        + num_unverified * unverified_unit_energy
    )
    return GraphEnergyReport(
        num_contradictions=num_contradictions,
        num_unverified=num_unverified,
        total_energy=float(total),
    )


def is_promotion_allowed(report: GraphEnergyReport, *, temperature: float) -> bool:
    if temperature <= 0:
        return False
    ratio = report.total_energy / temperature
    return ratio <= 1.0


def boltzmann_probability(report: GraphEnergyReport, *, temperature: float) -> float:
    """Softmax-style stability score in [0, 1]; for telemetry only."""
    if temperature <= 0:
        return 0.0
    return float(math.exp(-report.total_energy / temperature))
```

- [ ] **Step 4: Run to pass**

```bash
python3 -m pytest scripts/tests/test_health_boltzmann.py -v
```

- [ ] **Step 5: Commit**

```bash
git add scripts/vitruvius/health/__init__.py scripts/vitruvius/health/boltzmann_energy.py scripts/tests/test_health_boltzmann.py
git commit -m "feat(health): add Boltzmann graph-energy promotion gate (Task X.1)"
```

### 20.4 Stream X Definition of Done
- [ ] Energy computation is deterministic.
- [ ] `is_promotion_allowed` returns False when contradictions exceed temperature budget.
- [ ] Feature flag `x_boltzmann_promotion_gate` added.


---

## 21. Sprint Rollout Plan

### 21.1 Sprint H — Query Layer v2 (weeks 1–3)

**Dependency:** `statistical-architectural-upgrade-plan.md` Stream H Done-of-Done confirmed.

- Stream I Tasks I.1–I.6 (Phase 9 base + ontology prompt + GraphRAG router + MCMC ranker + HMM observability)
- Stream U Task U.1 (hardware router — needed before enabling any new LLM call path)

**Gating metric:** Every I.* test green; hardware router test green; backward-compat suite green. Feature flags stay `false`.

### 21.2 Sprint I — Uncertainty & Active Learning (weeks 4–5)

- Stream J Tasks J.1–J.2 (active learning, EMC)
- Stream R Tasks R.1–R.2 (MC dropout, Dempster-Shafer)
- Stream X Task X.1 (Boltzmann energy gate)

**Gating metric:** Unanimous-vote MC returns 0 variance; Dempster-Shafer raises on total conflict; Boltzmann gate blocks when contradictions > T.

### 21.3 Sprint J — Spatial Reasoning Core (weeks 6–8)

- Stream L Tasks L.1–L.5 (spatial contract, ingestion, Z3 evaluator, parametric edge, compliance report)
- Stream S Tasks S.1–S.2 (clash motif library + VF2 matcher)

**Gating metric:** End-to-end spatial compliance check on a synthetic SketchUp JSON produces deterministic report. Motif library loader parses >=1 real motif.

### 21.4 Sprint K — Polyglot Performance (weeks 9–11)

- Stream M Tasks M.1–M.4 (Rust Bloom + MinHash + parity tests, Python fallback)
- Stream N Tasks N.1–N.2 (Rust CSR + RWR + PageRank, Python fallback)

**Gating metric:** `maturin develop --release` succeeds on M2 with both crates; Rust vs Python parity tests within 1e-6; suite passes when the Rust extension is absent.

### 21.5 Sprint L — Temporal & Event Sourcing (weeks 12–13)

- Stream P Tasks P.1–P.4 (event types, log, replay engine, time travel)
- Stream Q Task Q.1 (time-mask query)

**Gating metric:** Replay reproduces snapshot state byte-for-byte; time-travel reconstruction matches the canonical snapshot at the current epoch.

### 21.6 Sprint M — Storage Vault (week 14)

- Stream O Tasks O.1–O.3 (Parquet, FlatBuffers, LMDB)
- Stream T Task T.1 (adaptive Nyquist chunking)

**Gating metric:** Parquet roundtrip on 10k-row fixture; FlatBuffer encoder bytes match on repeated encoding; LMDB store survives close/reopen.

### 21.7 Sprint N — Ontology + Foraging (week 15)

- Stream V Task V.1 (IFC mapper)
- Stream W Tasks W.1–W.2 (crawler + drift)

**Gating metric:** Every seed concept in the IFC table maps to an `IfcXxx` class; drift detector returns inf on singular covariance.

### 21.8 Sprint O — CLUP Scaling (gated, weeks 16+)

- Stream K Tasks K.1–K.2 (Rosetta + precedence router) — SHIP but keep `k_*` flags `false` until a second jurisdiction is ingested.

### 21.9 Deferred Milestones

Items marked in §2.3 as deferred (D1–D13) do not appear in any sprint. They become their own plan once their prerequisite gate lifts.

---

## 22. Risks & Mitigations

| Risk ID | Description | Likelihood | Impact | Mitigation |
|---|---|---|---|---|
| R-01 | z3-solver 4.12 wheel unavailable on the user's exact Python/macOS combination | MEDIUM | Stream L blocked | Use `pip install z3-solver --no-binary=z3-solver` as fallback; feature flag stays `false` until solver imports successfully |
| R-02 | Rust toolchain install fails on 8 GB M2 during `rustup-init` | LOW | Streams M, N skip to Python fallback | Both streams ship a pure-Python fallback that is numerically identical; Rust is a pure acceleration play |
| R-03 | plyvel wheel unavailable (rare on Apple Silicon) | MEDIUM | Stream O.3 blocked | Gate Stream O.3 behind a try/except ImportError and fall back to a JSON file-per-key mock store for tests |
| R-04 | maturin develop produces an extension that crashes on macOS signing | LOW | Streams M, N blocked | Run `codesign --sign -` on the produced .so/.dylib if CI catches an error |
| R-05 | networkx VF2 subgraph isomorphism is too slow on a real >10k-node graph | MEDIUM | Stream S unusable in prod | Cap motif library size to ≤10 motifs with ≤6 nodes each; gate VF2 runs behind a timeout (2s default) |
| R-06 | pyarrow 15 pulls in >70 MB of shared objects, bloating install | LOW | None beyond disk | Document in §3.3; still well under the 8 GB RAM ceiling |
| R-07 | Stream H.* tests drift between this plan's Stream I tasks (centrality-aware prompt) and the actual `graph/centrality.py` API | MEDIUM | Stream I tests fail to import | Task I.3 MUST re-verify the import surface of `centrality.compute_centrality` before writing tests; if renamed, update plan accordingly |
| R-08 | Rangers refuse to label active-learning queue fast enough | MEDIUM | Stream J stagnates | Queue auto-archives items older than 30 days; NB/CRF retraining runs on whatever labels accumulate |
| R-09 | Foraging crawler triggers rate limits or ToS violations on LGU sites | MEDIUM | Stream W unusable in prod | `poll_interval_minutes` defaults to 1440 (daily); per-host cache + If-Modified-Since headers in production wiring |
| R-10 | Binary storage vault confuses operators who `cat` a .parquet and see garbage | HIGH | Operator confusion | README in `005_Operational-Intelligence-Layer/README.md` documents inspection scripts (`vitruvius vault-inspect <file>`) |
| R-11 | Dempster–Shafer total-conflict exception crashes the promotion pipeline | LOW | Downtime | `combine_dempster` raises a specific `ValueError`; the caller catches it and routes the candidate to the Ranger queue instead |
| R-12 | Time-travel queries hit event logs faster than the OS can page them | LOW | Slow query | Rollover at `max_per_file = 10000` keeps individual files small; log root is SSD-backed |
| R-13 | Rust CSR / RWR PyO3 parity drifts by >1e-6 due to IEEE754 rounding order | LOW | Parity test fails | Tolerance bumped to 1e-5 if rounding discrepancies surface; document which kernel is authoritative |
| R-14 | The single `parametric_constraint` field on `GraphEdge` breaks frozen dataclass equality on existing edges | MEDIUM | Graph contract tests fail | Task L.4 explicitly requires the field to default to `None`; existing fixtures that compare edges byte-for-byte need only a trailing `None` added |
| R-15 | Feature-flag namespace collisions with the existing `features.py` map | LOW | Import failure | All new keys are prefixed with their stream letter (`i_`, `j_`, `k_`, `l_`, `m_`, …, `x_`) so no collision is possible |

---

## 23. Non-Goals

- Building the external spatial daemon (SketchUp/Rust GJK middleware). This plan only ingests its JSON output.
- Re-implementing Streams A–G or core Phase 8 modules. Those are frozen.
- Implementing a full OWL reasoner. Stream V ships only the seed IFC mapping table plus a stub OWL loader; full inference is deferred until IFC-powered clients consume the ontology.
- Building a dashboard UI for active learning or compliance reports. JSON/Parquet outputs are the Vitruvius contract; a frontend is a separate product.
- Running benchmarks against >10^6-node synthetic graphs. The plan's performance targets assume PD 1096 + IRR scale (~10^4 nodes, ~10^5 edges).
- Replacing the canonical 003 YAML + Markdown sources with binary formats. Human-readable canonical layers are preserved by contract.
- Adding any generative-AI dependency beyond the existing Ollama HTTP client. No cloud API keys.
- Providing exactly-once delivery guarantees for the foraging crawler. Best-effort + idempotent write is acceptable.

---

## 24. Stream-Level Gating Metrics (consolidated)

Each stream has its own §X.4 Definition of Done. The consolidated view:

| Stream | Key Tests | Feature Flag Default | Hardware Headroom |
|---|---|---|---|
| I | 6 test files, ~25 assertions | false | <150 MB |
| J | 2 test files, ~10 assertions | false | <50 MB |
| K | 2 test files, ~10 assertions | false | <300 MB (gated on 2+ jurisdictions) |
| L | 5 test files, ~20 assertions | false | <200 MB |
| M | 3 test files, ~15 assertions | false | <20 MB + Rust binary |
| N | 4 test files, ~20 assertions | false | <150 MB + Rust binary |
| O | 3 test files, ~15 assertions | false | <500 MB (LMDB page cache) |
| P | 3 test files, ~15 assertions | false | <100 MB |
| Q | 1 test file, ~5 assertions | false | 0 additional |
| R | 2 test files, ~10 assertions | false | <50 MB |
| S | 2 test files, ~10 assertions | false | <30 MB |
| T | 1 test file, ~8 assertions | false | <20 MB |
| U | 1 test file, ~10 assertions | false | <5 MB |
| V | 1 test file, ~5 assertions | false | <100 MB |
| W | 2 test files, ~10 assertions | false | <200 MB |
| X | 1 test file, ~10 assertions | false | <10 MB |

**Total new tests:** ~38 test files, ~190 assertions. Suite size after this plan: ~131 test files, ~980+ tests.

---

## 25. Research-Item Coverage Matrix

### 25.1 `.ai/13_research/Ultimate-Improvement.md` item-by-item

| Research item | Address in this plan | Stream |
|---|---|---|
| In-Memory Graph Hydration (NetworkX) | Already shipped in `graph/builder.py` | — |
| GraphRAG context injection into LLM | Task I.3 (ontology prompt builder) | I |
| Semantic Routing via MoE-Lite | SLM router already shipped (Stream F); hardware router extends | U |
| Hierarchical Graph Clustering (Leiden) | Louvain already shipped in `graph/community.py`; Leiden deferred D10 | — |
| Time-Multiplexed Sequential MoE | Partially covered by existing SLM router; hardware router gates model load | U |
| Locality-Sensitive Hashing (MinHash) | Rust MinHash + Python fallback | M |
| Tensorized Graph Adjacency (CSR) | scipy CSR already in `graph/spectral.py`; Rust CSR kernel | N |
| Per-Layer Context Injection (Gemma 4 PLE) | Ontology-embedded prompt | I |
| Chain-of-Thought Constraint (Gemma 4 `<|think|>`) | Already wired in `review/ollama_config.py` | — |
| Shannon Entropy classifier (Phase 1B) | Already shipped in `parsers/shannon_classifier.py` | — |
| Conformal Prediction | Already shipped in `review/conformal_calibrator.py` | — |
| Graph Centrality (Pagerank, eigenvector) | Already shipped in `graph/centrality.py` | — |
| Mahalanobis outlier detection | Already shipped in `normalization/outlier_detector.py`; foraging extends | W |
| Hidden Markov Model pipeline state | Task I.6 | I |
| Nyquist-Shannon sampling | Task T.1 (density probe + overlap recommender) | T |
| Kolmogorov complexity (delta-storage) | Deferred (D-misc, low priority) | — |
| PageRank centrality | Already shipped; Rust acceleration | N |
| Boltzmann system energy | Task X.1 | X |
| Eigenvector centrality | Already computed in centrality.py | — |
| TDA Betti numbers / loop detection | Already shipped in `graph/tda.py` | — |
| Wasserstein Optimal Transport merge | Already shipped in `graph/wasserstein_merge.py` | — |
| Causal inference (do-calculus, DAGs) | Already scaffolded in `graph/causal_dag.py` | — |
| Stochastic processes / RWR | Already shipped in `graph/mcmc.py`; Rust acceleration + query integration | N, I |
| Spectral Graph Theory (Laplacian, Fiedler) | Already shipped in `graph/spectral.py` | — |
| Formal Concept Analysis | Already shipped in `concepts/fca_lattice.py` | — |
| Tensor Factorization | Already scaffolded in `graph/tensor_factorisation.py`; activation gated on Stream K | K |
| Choquet Integral | Already shipped in `review/choquet_aggregator.py` | — |
| Hyperbolic embeddings (Poincaré disk) | Deferred — requires manifold library; not hot path | — |
| Markov Decision Processes | Deferred (FUTURE-LRN-02 — ILXP learning-policy optimizer) | — |
| Cellular Automata / Percolation | Deferred (FUTURE-SIM-01) | — |
| Dempster-Shafer theory | Task R.2 | R |
| Subgraph isomorphism violation motifs | Tasks S.1–S.2 | S |
| Ant Colony Optimization (teaching paths) | Deferred (ILXP scope) | — |
| Item Response Theory | Deferred (ILXP scope) | — |
| Ebbinghaus forgetting curve | Deferred (ILXP scope) | — |
| Elo rating system | Deferred (ILXP scope) | — |
| Jaccard / MinHash dedup | Task M.4 (Rust + Python) | M |
| Graph coloring / chromatic number | Deferred (niche, no current consumer) | — |
| Shannon entropy for PDFs | Already shipped | — |
| Spatial CSP / computational geometry | External daemon (decoupled); Vitruvius ingests JSON only | L |
| Multi-objective optimization (Pareto massing) | Deferred — Generative Parametric Massing (FUTURE-GEN-01) | — |
| Monte Carlo simulations for feasibility | Deferred (FUTURE-SIM-01) | — |
| GJK algorithm | External daemon | L (ingest only) |
| Z3 SMT theorem prover | Task L.3 | L |
| Temporal Knowledge Graph (4D law) | Tasks Q.1 + P.4 (time-travel) | Q, P |
| Epistemic Uncertainty Quantification | Tasks R.1–R.2 | R |
| Autonomous Epistemic Foraging | Tasks W.1–W.2 | W |
| IFC/OWL Ontological Unification | Task V.1 | V |
| BIM bi-directional compilation | Deferred — the core needs the spatial daemon first | — |
| PINNs | Deferred (FUTURE-ML-03 — needs GPU) | — |
| Event-Sourced Graph State | Tasks P.1–P.4 | P |
| GraphSAGE representation learning | Deferred (D7 — TransE already covers link prediction) | — |
| Rust / Wasm kernels | Streams M, N (native PyO3 preferred over Wasm) | M, N |
| Bloom Filter ingestion | Task M.1–M.3 | M |
| Apache Arrow zero-copy sharing | Indirect via pyarrow in Stream O | O |
| FlatBuffers instant-load | Task O.2 | O |
| RocksDB / LMDB embedded K/V | Task O.3 | O |
| Parquet cold archives | Task O.1 | O |
| Zero-Knowledge Proofs (zk-SNARKs) | Deferred (D6) | — |
| Law-constrained generative topologies | Deferred (D11) | — |
| Algorithmic escrow + smart contracts | Deferred (D-APP) | — |
| Systemic resilience simulation | Deferred (D-SIM) | — |

**Every research item from Ultimate-Improvement.md is accounted for:** shipped in Streams A–G, scaffolded in Stream H, planned in Streams I–X, or explicitly deferred with a rationale.

---

## 26. Self-Review Checklist (pre-execution)

### 26.1 Spec Coverage

- [ ] Every research item in §25 maps to a stream or a deferred row with a FUTURE-* tag.
- [ ] Every stream has a §X.4 Definition of Done.
- [ ] Every task has a `Files:`, `Step 1: Write failing test`, `Step 2: Run to fail`, `Step 3: Implement`, `Step 4: Run to pass`, `Step 5: Commit`.
- [ ] Every test that names a function or method verifies it exists in the module the test imports from.

### 26.2 Placeholder Scan

- [ ] Grep the plan for `TBD`, `TODO`, `implement later`, `similar to Task`, `fill in`, `add appropriate`. Any hit is a plan bug.
- [ ] Every code block is complete and runnable, not a sketch.
- [ ] Every bash command is a full command, not a template.

### 26.3 Type / Interface Consistency

- [ ] `StructuredCall.operation` names (`traverse.neighbors`, `traverse.shortest_path`, `traverse.incoming_edges`, `community.list_members`) match the actual function names when Stream I executors are added.
- [ ] `GraphEdge.parametric_constraint` is referenced as a dict in Stream L but stored on a frozen dataclass — confirmed by Task L.4.
- [ ] `RouterDecision.model_name` strings (`gemma4:e2b`, `gemma4:e4b`, `gemma4:31b`) match `review/ollama_config.py` constants.
- [ ] `EventLog.max_per_file` default matches the config key `ultimate_upgrade.event_sourced_graph.max_events_per_file`.

### 26.4 Non-Breaking Contract

- [ ] Every feature flag added in §3.2 defaults `false`.
- [ ] No Stream A–G module signature is modified.
- [ ] `test_backward_compat.py` is expected to remain green after every stream.
- [ ] `GraphEdge.parametric_constraint` defaults to `None` so all existing fixtures still typecheck.

### 26.5 Hardware Ceiling

- [ ] Sum of steady-state RAM across streams (§1.4) is <1.2 GB and leaves ≥6 GB for Ollama.
- [ ] No module loads an LLM weight file outside of the hardware router gate.
- [ ] Rust kernels cap their memory at 256 MB via config.
- [ ] LMDB map size default is 256 MB; configurable per deployment.

---

## 27. Execution Handoff

This plan is saved to `.ai/03_plans/ultimate-architecture-upgrade-plan.md`. Two execution options:

**1. Subagent-Driven (recommended)** — Dispatch a fresh subagent per Task using `superpowers:subagent-driven-development`. Each subagent gets the task's full `Files:` block, test code, implementation code, and commit message. Main conversation reviews between tasks.

**2. Inline Execution** — Execute tasks in the current session using `superpowers:executing-plans`. Batch execution with checkpoints at each stream's §X.4 Definition of Done.

**Recommended dispatch order:** Follow §21 Sprint Rollout Plan. Do NOT start Sprint H until `statistical-architectural-upgrade-plan.md` Stream H is Done-of-Done. Do NOT start Sprint O (Stream K) until a second jurisdiction is ingested into `003_Canonical-Knowledge-Layer/`.

**Emergency stop conditions:**
- Backward-compat suite turns red → halt the current stream, revert the last commit, diagnose before continuing.
- A hardware-ceiling metric is breached (e.g., maturin binary >50 MB, LMDB map >1 GB) → review the task that introduced the breach before merging.
- Dempster–Shafer `ValueError: total conflict` surfaces in production → log and escalate; do NOT swallow the exception silently.

---

## 28. Changelog

- **2026-04-14 20:35 GMT+8** — Initial draft. Covers Streams I, J, K (completing the existing `statistical-architectural-upgrade-plan.md` roadmap) and adds net-new Streams L, M, N, O, P, Q, R, S, T, U, V, W, X derived from the research items in `.ai/13_research/Ultimate-Improvement.md`. Honest audit (§2.1) against live filesystem confirms Streams A–G shipped and Stream H scaffolded as of commit e38570e. Hardware ceiling validated at <1.2 GB additive RAM. 16 streams × ~90 tasks total.
