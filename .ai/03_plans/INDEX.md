# `.ai/03_plans/` — Plan Index

> **Purpose:** One-stop index of every implementation plan, design spec, and contract in this directory.
> **Authoritative execution order:** `00-governing-implementation-plan.md` (v1.0.0, 2026-04-15) — read this *before* picking a plan to execute.
> **Authoritative roadmap:** `/.ai/01_roadmap/master-roadmap.md`
> **Updated:** 2026-04-15
> **2026-04-15 cleanup pass:** Archived `phase-8-graph-contract-indexing`, `phase-9-query-ai-layer`, and `ultimate-architecture-upgrade` plans. All successor sprint plans have shipped and are listed as ✅ complete above. Active plan count is now **5** (governing, INDEX, ingestion contract, phase-1B, statistical-upgrade).

Each plan is a self-contained document keyed by a `plan_id` and a `phase` label in its YAML frontmatter. Plans are one of three types:

| Type | Definition | Example |
|---|---|---|
| `implementation_tdd` | Full bite-sized TDD task list with code in every step. Ready to execute. | `phase-7-promotion-governance-plan.md` |
| `design_spec` | Architecture + task sequence, expanded to TDD before execution. | `phase-1b-multi-parser-integration-plan.md` |
| `contract` | Frozen interface between phases. Changes require a version bump. | `ingestion-refinement-contract.md` |

## Plan Naming Convention

- **Phase plans:** `phase-<N>-<topic>-plan.md` (e.g. `phase-7-promotion-governance-plan.md`)
- **Contracts:** `<topic>-contract.md` (legacy; new contracts should use `contract-<topic>.md`)
- **Frontmatter `plan_id`** uniquely identifies the plan regardless of filename.

## Current Plans

| Phase | Plan ID | Title | Status | Sprint | Type | File |
|---|---|---|---|---|---|---|
| META | `governing-implementation` | **Governing Implementation Plan** (sprint order, gates, conflict resolutions) | 🔥 Active | Meta (all sprints) | orchestration | [00-governing-implementation-plan.md](00-governing-implementation-plan.md) |
| 1A→12 | `statistical-architectural-upgrade` | **Statistical & Architectural Intelligence Upgrade** | 🔥 Streams A–I CLOSED 2026-04-14; J–K deferred; Stream L_conf / O migrated (see governing plan §4) | Sprint D | implementation_tdd | [statistical-architectural-upgrade-plan.md](statistical-architectural-upgrade-plan.md) |
| 1B | `phase-1b-multi-parser-integration` | Multi-Parser Integration | 🔥 In progress (Foundation shipped) | Sprint C | design_spec | [phase-1b-multi-parser-integration-plan.md](phase-1b-multi-parser-integration-plan.md) |
| 1B↔1C | `contract-ingestion-refinement` | Ingestion → Refinement Handoff Contract | ❄️ Frozen | N/A | contract | [ingestion-refinement-contract.md](ingestion-refinement-contract.md) |
| 1C | `phase-1c-centralized-normalization` | Centralized Normalization — Text Refinement Layer | ✅ MVP Complete (archived 2026-04-14) | Sprint B — closed MVP scope | design_spec | [../09_archive/plans/phase-1c-centralized-normalization-plan.md](../09_archive/plans/phase-1c-centralized-normalization-plan.md) |
| 2 | `phase-2-canonicalizer-restoration` | Canonicalizer Restoration — Structured Section Generation | ✅ Complete (archived 2026-04-14) | Sprint B — closed | implementation_tdd | [../09_archive/plans/phase-2-canonicalizer-restoration-plan.md](../09_archive/plans/phase-2-canonicalizer-restoration-plan.md) |
| 3C | `phase-3-concept-enrichment` | Concept Enrichment — Placeholder to Knowledge Node | ✅ MVP Complete (13/20, archived 2026-04-14) | Post-Sprint-C — closed (deterministic) | design_spec | [../09_archive/plans/phase-3-concept-enrichment-plan.md](../09_archive/plans/phase-3-concept-enrichment-plan.md) |
| 6A | `phase-6a-review-gap-closure` | Review Layer Gap Closure | ✅ Complete (archived 2026-04-14) | Sprint A + B — closed | implementation_tdd | [../09_archive/plans/phase-6a-review-gap-closure-plan.md](../09_archive/plans/phase-6a-review-gap-closure-plan.md) |
| 6B | `phase-6b-second-pass-review` | Second-Pass Review (Two-Stage Adjudication) | ✅ Complete (archived 2026-04-14) | Sprint C — closed | implementation_tdd | [../09_archive/plans/phase-6b-second-pass-review-plan.md](../09_archive/plans/phase-6b-second-pass-review-plan.md) |
| 7 | `phase-7-promotion-governance` | Promotion Governance Layer | ✅ Complete (archived 2026-04-14) | Sprint A — closed | implementation_tdd | [../09_archive/plans/phase-7-promotion-governance-plan.md](../09_archive/plans/phase-7-promotion-governance-plan.md) |
| 8 | `phase-8-graph-contract-indexing` | Graph Contract & Filesystem-Backed Indexing | ✅ **Subsumed + archived** — base work shipped inside Sprint D Stream H (2026-04-14); original design spec moved to archive 2026-04-15 | Sprint D — closed | design_spec | [../09_archive/plans/phase-8-graph-contract-indexing-plan.md](../09_archive/plans/phase-8-graph-contract-indexing-plan.md) |
| 8B | `phase-8b-geo-topological-graph` | **Geo-Topological Knowledge Graph: Binary Vault & Octree Engine** (Rust Data Plane + Linear Octree + Temporal Graph + Spatial GraphRAG + Hardware Hardening) | ✅ Complete (archived 2026-04-15) — GT.1 pyo3 Rust crate + GT.2 linear octree + GT.3 temporal graph (SQLite event store + Parquet archiver) + GT.4 spatial GraphRAG bridge + GT.5 hardware hardening (mmap + Bloom + MC dropout) all shipped | Sprint GT — closed | implementation_tdd | [../09_archive/plans/phase-8b-geo-topological-graph-plan.md](../09_archive/plans/phase-8b-geo-topological-graph-plan.md) |
| 9 | `phase-9-query-ai-layer` | Query & AI Augmentation Layer | ✅ **Subsumed + archived** — base work shipped inside Sprint D Stream I (2026-04-14); original design spec moved to archive 2026-04-15 | Sprint D — closed | design_spec | [../09_archive/plans/phase-9-query-ai-layer-plan.md](../09_archive/plans/phase-9-query-ai-layer-plan.md) |
| 1D+6+8 | `3d-spatial-intelligence-upgrade` | 3D Spatial Intelligence Upgrade (Streams L-O: spatial ingest + Z3 solver + IFC/OWL + foraging scaffold + TS daemon) | ✅ Complete (archived 2026-04-15) — 20/20 tasks shipped across L/M/N/O; TS daemon at spatial-daemon/ | Sprint H — closed | implementation_tdd | [../09_archive/plans/3d-spatial-intelligence-upgrade-plan.md](../09_archive/plans/3d-spatial-intelligence-upgrade-plan.md) |
| 6+7+8 | `live-wiring-8gb-hardening` | **Live Wiring & 8GB Hardening** (Streams W1-W5: wire Stream F+G scaffolds into live pipeline + 8GB LLM hardening + stringency gate rollout + quality harness) | ✅ Complete (archived 2026-04-15) — all 20 tasks shipped; live RSS/latency bench deferred to post-closure operator run | Sprint Q — closed | implementation_tdd | [../09_archive/plans/live-wiring-and-8gb-hardening-plan.md](../09_archive/plans/live-wiring-and-8gb-hardening-plan.md) |
| 1A+5+6 | `per-layer-embeddings-agentic-upgrade` | **Per-Layer Embeddings & Agentic Reasoning Upgrade** (Streams Y0-Y5: contextual priming + MoE domain routing + thinking-mode CoT audit + stateful agentic registry + vision OCR) | ✅ Complete (archived 2026-04-15) — all 20 tasks shipped. Phase 6A Resume gap closed at root. Vision OCR gated behind operator probe. | Sprint R — closed | implementation_tdd | [../09_archive/plans/per-layer-embeddings-agentic-upgrade-plan.md](../09_archive/plans/per-layer-embeddings-agentic-upgrade-plan.md) |
| 9+ | `ultimate-architecture-upgrade` | Ultimate Architecture Upgrade (legacy superset covering Streams I–X) | ❌ **Superseded + archived** — narrative retained, successor plans all shipped and archived; moved to archive 2026-04-15 (see governing plan §4.6) | — | design_spec | [../09_archive/plans/ultimate-architecture-upgrade-plan.md](../09_archive/plans/ultimate-architecture-upgrade-plan.md) |
| 12 | `phase-12-compound-ai-evolution` | Compound AI Evolution: Reactive Neuro-Symbolic OS (Streams S1-S5: Datalog bridge + adversarial swarm + differential dataflow + Wasm kernel + DSPy prompt compilation) | ✅ Complete (archived 2026-04-15) — all 5 streams shipped: S1 neuro-symbolic Datalog (Rust `datalog_rs` crate + pyo3 bridge + prompt directive), S2 Proposer/Inspector/Adjudicator swarm, S3 differential dataflow (Delta + DependencyTracker + DifferentialPropagator), S4 Wasm spatial kernel (workspace split + wasmtime loader), S5 DSPy prompt compiler | Sprint Z — closed | implementation_tdd | [../09_archive/plans/phase-12-compound-ai-evolution-plan.md](../09_archive/plans/phase-12-compound-ai-evolution-plan.md) |
| 13 | `phase-13-high-performance-optimizations` | High-Performance Optimizations (Streams HP.1-HP.5: Merkle fs + AST chunking + event-sourced graph + Wasm spatial + GraphSAGE PQ) | ✅ Complete (archived 2026-04-15) — HP.1 Merkle fs + HP.3 SQLite event-sourced graph (pivoted from RocksDB) + HP.4 Wasm spatial kernels (workspace split) + HP.5 GraphSAGE loopholes detector all shipped. HP.2 AST chunking was already covered by Stream C.2 from the earlier Sprint D work. | Sprint HP — closed | implementation_tdd | [../09_archive/plans/phase-13-high-performance-optimizations-plan.md](../09_archive/plans/phase-13-high-performance-optimizations-plan.md) |
| 13-R | `rocksdb-kv-migration` | **SQLite → RocksDB KV backend migration** (Sprint HP.3 spec compliance: RocksDBEventStore + RocksDBStatefulReviewRegistry + factory dispatch + ple-kv-migrate CLI + O(1) count optimization) | ✅ Complete (archived 2026-04-15) — AD-029: RocksDB 18.7x faster on event store, 24.3x faster on verdict cache at n=10000; defaults flipped to true | Sprint HP.3-R — closed | implementation_tdd | [../09_archive/plans/2026-04-15-rocksdb-kv-migration-plan.md](../09_archive/plans/2026-04-15-rocksdb-kv-migration-plan.md) |
| META | `2026-04-15-docs-cleanup` | **Post-Sprint Docs Cleanup Plan** — refreshes `.ai/00_system/` architecture + pipeline, `.ai/01_roadmap/` master + milestone-tracker, `.ai/02_audits/` banners, `.ai/10_state/known_issues.md`, archives 3 superseded plans, reconciles INDEX.md | ✅ Complete (archived 2026-04-15) | Meta — closed | docs | [../09_archive/plans/2026-04-15-docs-cleanup-plan.md](../09_archive/plans/2026-04-15-docs-cleanup-plan.md) |
| 1B | `phase-1b-modernization-tranche-1` | **Phase 1B Modernization Tranche 1** — `DoclingParser(BaseParser)` + `LibreOfficePreprocessor` + `GATE-005` + orchestrator preprocessor wiring + 2 `p1b_*` flags. Marker/Surya/ProcessPool/Golden Corpus deferred to Tranche 2 pending 8 GB M2 ML-dep feasibility | ✅ Complete (archived 2026-04-15) — AD-031: 17 new tests, 4 task commits, 1 closure commit | Sprint 1B-M1 — closed | implementation_tdd | [../09_archive/plans/2026-04-15-phase-1b-modernization-tdd-plan.md](../09_archive/plans/2026-04-15-phase-1b-modernization-tdd-plan.md) |
| 1B | `phase-1b-modernization-tranche-2` | **Phase 1B Modernization Tranche 2 (scoped)** — `OCRPreprocessor` (wraps ocrmypdf) + `ParserOrchestrator.process_batch` + `GoldenCorpusBenchmark` + 2 `p1b_*` flags. Marker/Surya DEFERRED per AD-032 feasibility finding (disk at 95.2%, RAM 2.03 GB available) | ✅ Complete (archived 2026-04-15) — AD-032: 11 new tests, 4 task commits, 1 closure commit | Sprint 1B-M2 — closed | implementation_tdd | [../09_archive/plans/2026-04-15-phase-1b-modernization-tranche-2-plan.md](../09_archive/plans/2026-04-15-phase-1b-modernization-tranche-2-plan.md) |
| 1B | `rust-pdf-ingestion-audit` | **Rust PDF Ingestion Audit** — lopdf-based `vitruvius_rust_pdf` crate + pyo3 bindings + subprocess-isolated bench vs docling/opendataloader_pdf. **Verdict: GO.** Rust parser measured at **13.7 MB peak RSS (48× smaller than docling) and 0.05s wall (625× faster)** on synthetic PDFs. Unlocks the low-spec target. | ✅ Complete (archived 2026-04-15) — AD-033; Tranche 3 implementation plan next | Sprint RUST-PDF-1 — closed | audit_then_conditional_implementation | [../09_archive/plans/2026-04-15-rust-pdf-audit-plan.md](../09_archive/plans/2026-04-15-rust-pdf-audit-plan.md) |
| 1B | `phase-1b-modernization-tranche-3` | **Phase 1B Modernization Tranche 3** — `RustPdfParser(BaseParser)` + `GATE-006` min-chars-per-page + `p1b_rust_pdf_parser` flag + real-PDF quality rollback gate (LCS 0.9925 vs pypdf). Implementation of the AD-033 GO verdict. | ✅ Complete (archived 2026-04-15) — AD-034; 9 new tests, 4 task commits, 1 closure commit | Sprint 1B-M3 — closed | implementation_tdd | [../09_archive/plans/2026-04-15-phase-1b-modernization-tranche-3-plan.md](../09_archive/plans/2026-04-15-phase-1b-modernization-tranche-3-plan.md) |
| META | `llm-reviewer-distillation-audit` | **LLM Reviewer Distillation Audit** — classical ML student model on Sprint R Y4 stateful verdict cache. **Verdict: DEFER_NO_DATA** (verdict cache is empty; needs ≥50 live LLM review verdicts before training is meaningful). Audit harness committed for re-run when data exists. | ✅ Complete (archived 2026-04-15) — AD-035 | Sprint DISTILL-1 — closed (DEFER_NO_DATA) | audit_then_conditional_implementation | [../09_archive/plans/2026-04-15-llm-distillation-audit-plan.md](../09_archive/plans/2026-04-15-llm-distillation-audit-plan.md) |
| META | `rust-migration-audit` | **Python→Rust polyglot migration audit** — measurement-first port of hot pure-compute kernels behind `scripts/vitruvius/engine_rs/`. Shipped 3 kernels: S1 `build_spatial_adjacency_edges` (200× raw / 57% subprocess wall at n=2000), S2 `weight_by_distance` (12.18× raw / 2.84× end-to-end at n=10000), N4 `mahalanobis_distance` (2.73× end-to-end at n=1000 64-dim). N1 `wasserstein_merge_decision` DEFERred per AD-038a (POT backend already native C++ LP). Both `rust_mig_*` flags flipped to `true`. | ✅ Complete (archived 2026-04-15) — AD-038 (+ AD-036, AD-037, AD-038a); 23 new Rust unit tests + 19 new Python tests; 14 sprint commits | Sprint RUST-MIG-1 — closed | audit_then_conditional_implementation | [../09_archive/plans/2026-04-15-rust-migration-audit-plan.md](../09_archive/plans/2026-04-15-rust-migration-audit-plan.md) |
| META | `advanced-tech-audit-2026-04-15` | **Advanced Tech Audit** — FlatBuffers / numerical integrity / MC Dropout. Three audits with pre-committed numeric decision gates; conditional implementation. Verdicts: FlatBuffers NO_GO (5-10× slower than `_json` on small records); Integrity GO_GAP (BLAKE3 0.7× on Apple Silicon ARMv8 SHA extensions, but MEDIUM gap closed via SHA-256 footer on spatial contract files); MC Dropout PARK (0 of 5 neural sites viable — GraphSAGE is deterministic). One shipped fix: spatial-daemon contract integrity footer + Python `contract_reader.py` + walker hardening. | ✅ Complete (archived 2026-04-15) — AD-039; 15 new Python tests + 1 new TS test; 5 commits | Sprint AUDIT-1 — closed | audit_then_conditional_implementation | [../09_archive/plans/2026-04-15-advanced-tech-audit-plan.md](../09_archive/plans/2026-04-15-advanced-tech-audit-plan.md) |
| 1B | `pipeline-cli-parser-chain-integration` | **pipeline_cli.py Integration for Phase 1B Parser Chain** — new `convert-parsers-one` subcommand + `build_default_orchestrator()` factory + `run_convert_parsers_one` handler. Wires the 5 `p1b_*` flags from AD-031/032/034 into live CLI dispatch (deployment markers → live behaviour). All `p1b_*` defaults stay `false`; flipping any one now actually changes which parser runs. Existing `convert-one` dispatch byte-identical to pre-plan behaviour. | ✅ Complete (archived 2026-04-15) — AD-040; 23 new Python tests; 5 commits including byte-identity exit gate | Sprint PIPELINE-CLI — closed | implementation_tdd | [../09_archive/plans/2026-04-15-pipeline-cli-integration-plan.md](../09_archive/plans/2026-04-15-pipeline-cli-integration-plan.md) |
| META | `graphsage-pq-embeddings` | **Product Quantization for GraphSAGE Embeddings** — pure-numpy PQ codebook (`PQCodebook` + k-means in M sub-spaces) + `encode_to_pq` / `decode_from_pq` / `adc_distance` + npz persistence + `compress_graphsage_report` integration helper. **32× compression** (256 B → 8 B per node) at **0.00017 cosine delta** (target ≤ 0.02 — ~117× under gate). Zero new pip deps. `hp_graphsage_pq` stays `false` (no persistence layer to consume codes yet). | ✅ Complete (archived 2026-04-15) — AD-041; 11 new Python tests + reconstruction-error bench artifact; 6 task commits + 1 closure | Sprint PQ-1 — closed | implementation_tdd | [../09_archive/plans/2026-04-15-graphsage-pq-embeddings-plan.md](../09_archive/plans/2026-04-15-graphsage-pq-embeddings-plan.md) |
| META | `lsh-minhash-dedup` | **MinHash LSH Fuzzy Near-Duplicate Dedup** — fuzzy near-duplicate layer on top of the existing O(n log n) dict-grouped `dedupe_by_endpoints` (per AD-037 reframing). Vectorized Carter-Wegman MinHash (pure numpy, no `datasketch` needed) + band-based LSH index + union-find component walk + representative pick. Fuzzy hit rate measured at **14-18% at 20-30% injection rates** (AD-037 gate: ≥10%), **zero false positives** on 200-candidate disjoint audit. `w_lsh_dedup` stays `false` until full PD 1096 operator run confirms live-data gates. | ✅ Complete (archived 2026-04-15) — AD-042 (premise: AD-037); 23 new Python tests + fuzzy-layer bench artifact; 5 task commits + 1 closure | Sprint LSH-1 — closed | implementation_tdd | [../09_archive/plans/2026-04-15-lsh-dedup-plan.md](../09_archive/plans/2026-04-15-lsh-dedup-plan.md) |
| 14 | `phase-14-autonomous-knowledge-synthesis` | Autonomous Knowledge Synthesis: Persistent LLM Wiki (Streams WIKI.1-WIKI.4: Docling/Heron ingestion + synthesis loop + Kuzu hybrid store + SHA-256 delta linting + LLM ego-graph linter + Ollama client) | ✅ Complete (archived 2026-04-15) — Docling parser + Kuzu store + delta tracker + LLM synthesis loop + ego-graph linter + Ollama client adapter all shipped | Sprint WIKI — closed | implementation_tdd | [../09_archive/plans/phase-14-autonomous-knowledge-synthesis-plan.md](../09_archive/plans/phase-14-autonomous-knowledge-synthesis-plan.md) |
| 15 | `phase-15-geometric-constraint-engine` | Geometric Constraint Engine: Buildable Envelope (Streams GEOM.1-GEOM.4: inequality extraction + Z3 CSP solver + 3D envelope generator + multimodal IoU audit) | ✅ Complete (archived 2026-04-15) — GEOM.1 inequality compiler + GEOM.3 2D+3D envelope (trimesh) + GEOM.4 IoU audit + Pareto optimizer (cvxpy) all shipped | Sprint GEOM — closed | implementation_tdd | [../09_archive/plans/phase-15-geometric-constraint-engine-plan.md](../09_archive/plans/phase-15-geometric-constraint-engine-plan.md) |
| 16 | `phase-16-statistical-mechanics-graph-physics` | Statistical Mechanics & Graph Physics: Authority Engine (Streams PHYS.1-PHYS.4: PageRank + Boltzmann stability + Shannon sampling + eigenvector cascade; absorbs orphan Stream O VF2 from statistical plan) | ✅ Complete (archived 2026-04-15) — 4 streams + orphan Stream O absorption shipped in one atomic pass | Sprint PHYS — closed | implementation_tdd | [../09_archive/plans/phase-16-statistical-mechanics-graph-physics-plan.md](../09_archive/plans/phase-16-statistical-mechanics-graph-physics-plan.md) |
| — | `sprint-b-polish-improvements` | Sprint B Polish (extractor dedup, Ollama warmup, lazy CLI, timestamp-aware diff, utils deprecation, concept status) | ✅ Complete (archived 2026-04-14) | Sprint B follow-on — closed | implementation_tdd | [../09_archive/plans/sprint-b-polish-improvements-plan.md](../09_archive/plans/sprint-b-polish-improvements-plan.md) |

**Status legend:** ✅ complete · 🟡 partial · 🔥 in progress (active sprint) · 📝 planned · 🔒 gated (do not start) · ❄️ frozen (contract)

## Execution Order (Dependency-Correct)

> **2026-04-15 update:** Authoritative execution order now lives in `00-governing-implementation-plan.md` §3. The block below is a summary view. If this diagram and the governing plan diverge, the governing plan wins — update this file in the next reconciliation pass.
>
> **2026-04-14 update (retained for history):** `statistical-architectural-upgrade` previously took precedence over all other plans. Its Streams A–I closed 2026-04-14; Phase 8 base and Phase 9 base shipped inside Streams H and I respectively (so `phase-8-graph-contract-indexing` and `phase-9-query-ai-layer` are now **subsumed**, not separately dispatchable).

```
Sprint A-C (CLOSED 2026-04-14)
  ├── phase-7-promotion-governance          ✅ complete
  ├── phase-1c-centralized-normalization    ✅ complete (MVP)
  ├── phase-6a-review-gap-closure           ✅ complete
  ├── phase-6b-second-pass-review           ✅ complete
  ├── phase-2-canonicalizer-restoration     ✅ complete
  ├── phase-3-concept-enrichment            ✅ 16/20 complete (4 deferred to Stream D)
  └── phase-1b-multi-parser-integration     🔥 Foundation shipped (Modernization absorbed by Stream B)

Sprint D — Statistical & Architectural Upgrade (weeks 1-5) 🔥 [HIGHEST PRIORITY]
  ├── Stream A — Dependency Bootstrap + Merkle Hash + Feature Flags
  ├── Stream B — Shannon Classifier + Table-to-Graph + Parametric NER
  ├── Stream C — Tier C OCR + AST Chunker + Embedding Chunker + Mahalanobis
  └── Stream D — TF-IDF + PMI + FCA + Contrastive Adapter

Sprint E — Intelligence (weeks 6-11)
  ├── Stream E — spaCy + CRF + KG Link Prediction
  ├── Stream F — NB + SLM Swarm + Conformal + Choquet + Reflection + Ontology Prompting
  └── Stream G — Bayesian Fusion + Stringency Matrix + Temporal Edges

Sprint F — Graph & Query (weeks 12-18)
  ├── Stream H — Phase 8 base + Centrality + Spectral + Community + MCMC + TDA + Wasserstein + Causal + Tensor
  ├── Stream I — Phase 9 base + Ontology Translator + GraphRAG Router + MCMC Ranker + HMM
  └── Stream J — Active Learning + Expected Model Change scoring

Sprint G — Scaling (weeks 19+, gated on second jurisdiction)
  └── Stream K — Rosetta Stone + Precedence Router + Tensor activation

Sprint Q — Live Wiring & 8GB Hardening 🔥 [HIGHEST PRIORITY — QUALITY]
  ├── Stream W1 — 8GB LLM Survival Mode (model pool + num_ctx cap + context guard + binary mode)
  ├── Stream W2 — Review Pipeline Wiring (NB prefilter + ontology prompt + SLM router + conformal + tension + Choquet)
  ├── Stream W3 — Stringency Matrix Live Gate (migrate concepts + lint + promotion gate + graph surface)
  ├── Stream W4 — Quality Harness (e2e + backcompat + bench + decisions automation)
  └── Stream W5 — Docs & Decisions Sync (current-phase + README + AGENTS.md)

Sprint R — Per-Layer Embeddings & Agentic Reasoning (weeks 20+, gated on Sprint Q closure)
  ├── Stream Y0 — Bootstrap + features.y_* flags + backward-compat regression
  ├── Stream Y1 — Contextual Priming (PLE) — priming/ subpackage + inject_prefix
  ├── Stream Y2 — Domain-Routing MoE — domain_classifier + route_with_moe
  ├── Stream Y3 — Thinking Mode + CoT Audit — parse_cot_strict + cot_audit
  ├── Stream Y4 — Stateful Agentic Registry — SQLite verdict cache (closes Phase 6A Resume gap)
  └── Stream Y5 — Vision OCR Integration (GATED on ple-vision-probe pass)

Sprint H — 3D Spatial Intelligence Upgrade (weeks 20+, gated on Sprint Q closure)
  ├── Stream L — Spatial Ingestion + Z3 Solver (001B layer + JSON contract + walker + mapper + constraint evaluator + CLI)
  ├── Stream M — IFC/OWL Ontology Mapping (registry + frontmatter validator + OWL/Turtle exporter)
  ├── Stream N — Decoupled Spatial Daemon (TypeScript/Node.js: AABB + GJK + contract writer + CLI)
  └── Stream O — Epistemic Foraging Scaffold (watched-sources registry + Mahalanobis drift + duplicate detector; NO live scrapers)

Sprint HP — Performance & Scale (Weeks 25+, gated on Phase 8B/12)
  ├── Stream HP.1 — Merkle Tree Filesystem (Zero-RAM Status)
  ├── Stream HP.2 — AST-Based Semantic Chunking (Legal Precision)
  ├── Stream HP.3 — Event-Sourced Graph Engine (Auditability)
  ├── Stream HP.4 — Wasm-Compiled Spatial Kernels (Math Speed)
  └── Stream HP.5 — Knowledge Graph Representation Learning (GraphSAGE)

Sprint WIKI — Autonomous Knowledge Synthesis (The Compounding Asset)
  ├── Stream WIKI.1 — Structural Ingestion (Docling + Heron)
  ├── Stream WIKI.2 — The Maintainer (Synthesis Loop + Schema Invariants)
  ├── Stream WIKI.3 — Hybrid Storage (Kuzu + Markdown Sync)
  └── Stream WIKI.4 — Governance & Linting (SHA-256 Delta Tracking)

Sprint GEOM — Mathematical Truth (Dimensional Building Code)
  ├── Stream GEOM.1 — Inequality Extraction (Math-First NLP)
  ├── Stream GEOM.2 — The CSP Solver (Z3 SMT Integration)
  ├── Stream GEOM.3 — 3D Buildable Envelope Generator (Boolean Polygons)
  └── Stream GEOM.4 — Multimodal Compliance Auditing (Stochastic Simulations)

Sprint PHYS — Structural Physics (Graph Authority & Stability)
  ├── Stream PHYS.1 — Statutory Authority (PageRank Centrality)
  ├── Stream PHYS.2 — Graph Stability (Boltzmann Energy/Temperature)
  ├── Stream PHYS.3 — Information Density (Nyquist-Shannon Sampling)
  └── Stream PHYS.4 — Influence Mapping (Eigenvector Cascade)

Sprint Z — Compound Evolution (Future State)
  ├── Stream S1 — Neuro-Symbolic Logic Bridge (Rust + Datalog)
  ├── Stream S2 — Adversarial Swarm Topology (Proposer/Inspector/Adjudicator)
  ├── Stream S3 — Differential Dataflow Engine (O(Δ) Reactive Graph)
  ├── Stream S4 — Isomorphic Spatial Wasm Kernel (Shared Rust/Wasm Math)
  └── Stream S5 — Algorithmic Prompt Compilation (DSPy integration)

Deferred (prerequisites outside Vitruvius)
  ├── FUTURE-ML-01 — LoRA fine-tuning      (needs GPU)
  ├── FUTURE-ML-02 — DPO pedagogical align (needs GPU + Ranger dashboard)
  └── FUTURE-LRN-01 — Bayesian Knowledge Tracing (needs ILXP + learners)
```

## How to Consume a Plan

### Before execution
1. Open the plan file.
2. Confirm the frontmatter `status` matches the active sprint in `/.ai/01_roadmap/current-phase.md`.
3. Read the plan's §"Scope Boundary" section.
4. If `plan_type: design_spec`, first expand Task sequence into `implementation_tdd` style (bite-sized steps with code). Otherwise go straight to execution.

### During execution
- Follow the superpowers sub-skill referenced in the plan header (usually `subagent-driven-development`).
- Tick `- [ ]` checkboxes as steps complete.
- Never skip the "run the failing test" step — it validates that the test actually tests what you think.

### After execution
- Update the plan's frontmatter `status` to `complete`.
- Record an `AD-XXX` entry in `/.ai/10_state/decisions.md` summarizing the final shape.
- Update `/.ai/01_roadmap/master-roadmap.md` §4 status table.
- Tick boxes in `/.ai/01_roadmap/milestone-tracker.md`.

## Plan Types in Depth

### `implementation_tdd`
- Every task has at minimum: `Files` block, failing test, run-test-to-fail, implementation with full code, run-test-to-pass, commit.
- An engineer with zero context for the codebase should be able to execute each step mechanically.
- No "TBD", "implement later", "add validation", or "similar to Task N" — the plan fails self-review if these appear.
- Sprint-A-critical plans are always `implementation_tdd`.

### `design_spec`
- Architecture narrative + task sequence at the level of "what, not how".
- Expanded to `implementation_tdd` *before* execution starts, not during.
- Appropriate for phases that are weeks or months away — premature TDD detail rots.
- The expansion step is itself a task: "expand plan-X into TDD form".

### `contract`
- Frozen interface shape between two phases.
- Changes bump `contract_version` and require signed-off updates on both producer and consumer sides.
- Violating a contract is a build failure, not a warning.

## Relationship to Other `.ai` Directories

| Directory | Relationship |
|---|---|
| `.ai/01_roadmap/` | Sets priority. Plans here execute what the roadmap decides. |
| `.ai/02_audits/` | Historical state. Plans cite audits in their dependencies section. |
| `.ai/06_specs/` | Schemas the plans produce files matching. Plans reference `source-schema.md`, `concept-schema.md`, `relationship-schema.md`. |
| `.ai/07_experiments/` | Experimental protocols that *inform* plans (parser comparison, model comparison). Not themselves plans. |
| `.ai/08_prompts/` | LLM prompt reference files. Plans reference them verbatim. |
| `.ai/10_state/` | Live snapshot of project state. Update after executing any plan. |

## Changelog

- **2026-04-14** — Initial index. Added frontmatter headers to the 3 pre-existing plans (1B, 1C, contract). Created 7 new plans: Phase 2, 3C, 6A, 6B, 7, 8, 9. Phase 7 is the most detailed (`implementation_tdd`, Sprint A active).
after executing any plan. |

## Changelog

- **2026-04-14** — Initial index. Added frontmatter headers to the 3 pre-existing plans (1B, 1C, contract). Created 7 new plans: Phase 2, 3C, 6A, 6B, 7, 8, 9. Phase 7 is the most detailed (`implementation_tdd`, Sprint A active).
