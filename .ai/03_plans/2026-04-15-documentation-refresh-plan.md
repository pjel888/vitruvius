# Vitruvius Documentation Refresh Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Bring 13 governance / reference / schema / audit documents (in `.ai/00_system/`, `.ai/06_specs/`, `.ai/02_audits/`) into alignment with post-2026-04-15 reality: 21 sprints closed, AD-042 ceiling, ten non-negotiable principles P1–P10, the RocksDB + Rust polyglot storage exception, the spatial integrity footer contract, and the current 41-subcommand CLI surface.

**Architecture:** Pure documentation edits. No code changes. Each task updates one file with a chain of `Edit` operations drawn verbatim from three separate gap reports (system / specs / audits) that were produced by parallel research agents against live truth sources (governing plan v3.0, master roadmap v2.2.0, decisions.md AD-001..AD-042, EXECUTION_LOOP.md v3.0, `config/vitruvius.yaml`, `scripts/pipeline_cli.py --help`, source code inspection). After file-level edits, Phase 4 runs cross-file consistency greps to verify no stale "ten sprints" / "AD-029 ceiling" / "P1..P9 only" strings remain.

**Tech Stack:** Markdown, YAML frontmatter, GitHub-flavored tables. No build step; no test suite changes (but principle I8 "test baseline monotonic" must hold — we verify `pytest` is at 1528 passed / 1 skipped at session close).

**Invariants this plan must honor** (from EXECUTION_LOOP.md v3.0):
- I1: AD append-only — any correction to an AD happens via a NEW AD, not by editing history.
- I3: Schema stability — if we touch any schema, we DO NOT break existing frontmatter shape.
- I7: Local-first AI — no external API keys, no cloud LLM references that weren't already there.
- I8: Test baseline monotonic — no test deletions. Running `pytest scripts/tests -q` at start and end of each phase confirms baseline is non-decreasing.
- I10: Idempotency — every task must be safely re-runnable (re-edits on already-edited sections are a noop or fail loud).

**Out of scope:** EXECUTION_LOOP.md v3.0 (already rewritten earlier today). The governing plan, master roadmap, decisions.md, known_issues.md, active_context.md, and current-phase.md (those are the TRUTH sources this plan pulls from, not targets).

---

## Self-Review Checklist (run after drafting; do NOT execute tasks without completing this)

- [ ] Every target file listed in the user request (`00_system` 4 files + `06_specs` 4 files + `02_audits` 5 files = 13 files) has at least one task in this plan.
- [ ] Every `Edit` old_string has ≥ 1 unique match in the target file (no ambiguity). If ambiguous, use `replace_all` OR expand context lines.
- [ ] No step says "update similarly" or references another step's code.
- [ ] Every cited AD number (AD-015, AD-022, AD-024, AD-027, AD-028, AD-029, AD-031, AD-032, AD-033, AD-034, AD-036, AD-038, AD-038a, AD-039, AD-040, AD-041, AD-042) has been verified to exist in `decisions.md`.
- [ ] Sprint count (21), AD ceiling (AD-042), test baseline (1528 passed / 1 skipped), and principle count (10) are consistent across every proposed edit.
- [ ] Principle renumbering in `principles.md` (Local-First AI: current P9 → P8; add new P9 + P10) is coordinated so no other file in this plan references "Principle 9 — Local-First AI" post-edit.

**Self-review result (filled by planner, 2026-04-15):**
- ✅ All 13 files have tasks (Tasks 1.1–1.4, 2.1–2.4, 3.1–3.5).
- ✅ Edits use sufficient context to be unique in each file (verified against the line numbers in the gap reports).
- ✅ No "update similarly" placeholders; all replacement text inline.
- ✅ Spot-checked ADs: AD-029 (HP.3-R, `hp_rocksdb_*`), AD-036 (Rust Line), AD-038 (RUST-MIG-1, `rust_mig_*`), AD-039 (AUDIT-1 spatial integrity footer), AD-041 (PQ-1 GraphSAGE PQ), AD-042 (LSH-1 MinHash). Audit agent confirmed AD-001..AD-042 span with sub-decision AD-038a.
- ✅ 21 sprints / AD-042 / 1528 / P1-P10 are consistent across all proposed replacements.
- ⚠️ **Open question OQ-1 from system agent:** renumbering `principles.md` Principle 9 → P8 could break grep-hits elsewhere in the repo. Task 1.4 includes a pre-edit grep step; if hits exist outside the plan's target files, stop and escalate.

---

## Phase 0: Baseline Verification (run FIRST)

### Task 0.1: Record pre-plan test baseline and commit SHA

**Files:** (no file edits; read-only)

- [ ] **Step 1: Verify we are on a clean branch.**

```bash
cd /Users/philiplewis/vitruvius
git status --short
```
Expected: clean working tree OR only the target files have M/A markers. If unrelated files are dirty, stash or commit them before starting.

- [ ] **Step 2: Capture the current commit SHA.**

```bash
git rev-parse HEAD
```
Record the SHA in your working notes — Phase 4 asserts that only the 13 target files changed between this SHA and HEAD at the end.

- [ ] **Step 3: Run the test baseline.**

```bash
cd /Users/philiplewis/vitruvius
pytest scripts/tests -q 2>&1 | tail -5
```
Expected: `1528 passed, 1 skipped` (± unrelated platform skips). Record the exact numbers; the session-end baseline check compares to this.

- [ ] **Step 4: Confirm the truth sources exist and are readable.**

```bash
ls -la /Users/philiplewis/vitruvius/.ai/01_roadmap/master-roadmap.md /Users/philiplewis/vitruvius/.ai/03_plans/00-governing-implementation-plan.md /Users/philiplewis/vitruvius/.ai/10_state/decisions.md /Users/philiplewis/vitruvius/.ai/10_state/known_issues.md /Users/philiplewis/vitruvius/.ai/00_system/EXECUTION_LOOP.md /Users/philiplewis/vitruvius/config/vitruvius.yaml
```
Expected: all exist. If any are missing, abort — the plan was drafted against specific truth sources and they must be in place.

- [ ] **Step 5: Confirm the current ceiling AD number.**

```bash
grep -n "^## AD-0" /Users/philiplewis/vitruvius/.ai/10_state/decisions.md | tail -5
```
Expected: highest heading is `## AD-042 …`. If the number has moved, update the plan's AD pointers accordingly (every reference to "AD-001 through AD-042" needs to become the new max).

---

## Phase 1: System Documentation (4 files, 8 + 6 + 6 + 8 = 28 gaps)

This phase is the most content-heavy. Each of the 4 files has at least one **foundational** gap (stale sprint count / stale AD / contradicted principle / missing invariant) and multiple structural gaps. Tasks are sequenced so that principle renumbering (Task 1.4) runs LAST in this phase — that way, if renumbering breaks something, the earlier files have already stabilized.

### Task 1.1: Update `.ai/00_system/architecture.md`

**Files:**
- Modify: `/Users/philiplewis/vitruvius/.ai/00_system/architecture.md` (238 lines pre-edit)

**Context:** This file has a recent (2026-04-15) "Post-Sprint-D Layered Additions" section that covers 10 of the 21 closed sprints but is missing 11 of them (1B-M1, 1B-M2, RUST-PDF-1, 1B-M3, DISTILL-1, RUST-MIG-1, AUDIT-1, PIPELINE-CLI, PQ-1, LSH-1, Meta). It also has stale "Planned (Roadmap)" entries listing Neo4j and embeddings — both now shipped. 8 gaps in total, plus one new section to append.

- [ ] **Step 1: Read the file to confirm line numbers match the gap report baseline.**

```bash
cat /Users/philiplewis/vitruvius/.ai/00_system/architecture.md | wc -l
```
Expected: `238`. If different, the file has drifted since the gap report was written (2026-04-15). Reconcile line numbers before applying edits.

- [ ] **Step 2: Gap 1.1 — replace the "ten sprints" sentence with a 21-sprint sentence (L127 area).**

Use the Edit tool with these exact strings:

old_string:
```
The **ten** sprints closed in 2026-04-15 (Q, R, PHYS, H, GEOM, WIKI, GT, HP, Z, and the follow-on Sprint HP.3-R RocksDB migration) added substantial capability on top of the pre-existing filesystem pipeline. The core ingestion/canonicalization layout above is unchanged; the additions below are **layered on top** and most are gated behind feature flags that default to `false` (the two `hp_rocksdb_*` flags default `true` as of AD-029).
```

new_string:
```
The **21** sprints closed on 2026-04-15 (Q, R, PHYS, H, GEOM, WIKI, GT, HP, Z, HP.3-R, 1B-M1, 1B-M2, RUST-PDF-1, 1B-M3, DISTILL-1, RUST-MIG-1, AUDIT-1, PIPELINE-CLI, PQ-1, LSH-1, and a Meta docs-cleanup sprint) added substantial capability on top of the pre-existing filesystem pipeline. The core ingestion/canonicalization layout above is unchanged; the additions below are **layered on top** and most are gated behind feature flags that default to `false` (the four flags `hp_rocksdb_event_store`, `hp_rocksdb_verdict_cache`, `rust_mig_spatial_kernels`, and `rust_mig_stats_kernels` default `true` per AD-029 and AD-038 respectively).
```

- [ ] **Step 3: Gap 1.1 continuation — replace the second "All ten sprints" occurrence.**

old_string:
```
All ten sprints added flag families under `features:` in `config/vitruvius.yaml`. Default is **false** for every new flag so pre-session behaviour is byte-identical until an operator opts in — except the two `hp_rocksdb_*` backend-switch flags, which default **true** per AD-029. The `EXPECTED_FLAGS` registry in `scripts/tests/test_features.py` enumerates every expected flag and fails CI if a flag is added to the YAML without a test entry.
```

new_string:
```
All 21 sprints added flag families under `features:` in `config/vitruvius.yaml`. Default is **false** for every new flag so pre-session behaviour is byte-identical until an operator opts in — except the four flags that have been promoted to live-by-default (see "Live-by-default flags" table below). The `EXPECTED_FLAGS` registry in `scripts/tests/test_features.py` enumerates every expected flag and fails CI if a flag is added to the YAML without a test entry.
```

- [ ] **Step 4: Gap 1.2 — fix AD range reference at L200.**

old_string:
```
For the authoritative per-sprint ledger see `.ai/10_state/decisions.md` AD-024 through AD-029.
```

new_string:
```
For the authoritative per-sprint ledger see `.ai/10_state/decisions.md` AD-024 through AD-042 (plus sub-decision AD-038a).
```

- [ ] **Step 5: Gap 1.3 — insert 11 missing sprint entries after the AD-024..AD-042 ledger pointer.**

The insert point is the line immediately after the `AD-024 through AD-042` pointer line from Step 4. Use Edit with this context to insert:

old_string:
```
For the authoritative per-sprint ledger see `.ai/10_state/decisions.md` AD-024 through AD-042 (plus sub-decision AD-038a).

---
```

new_string:
````
For the authoritative per-sprint ledger see `.ai/10_state/decisions.md` AD-024 through AD-042 (plus sub-decision AD-038a).

### Sprint RUST-PDF-1 — Rust PDF Ingestion (p1b_rust_pdf_parser, AD-033/034)

- `scripts/vitruvius/parsers/rust_pdf_parser.py` — `RustPdfParser(BaseParser)` pyo3 adapter wrapping `vitruvius_rust_pdf` (lopdf-based). 13.7 MB peak RSS, 0.05 s wall vs docling's 659 MB / 31 s (625× faster). GATE-006 `check_gate_006_min_chars_per_page` ships alongside.
- Flag `p1b_rust_pdf_parser` defaults **false** until real-corpus validation.

### Sprint RUST-MIG-1 — Python→Rust polyglot kernels (rust_mig_* flags, AD-036/AD-038)

Extends `scripts/vitruvius/engine_rs/` workspace with two new member crates — `spatial_kernels` and `stats_kernels`:

- `spatial_kernels` — S1 `build_spatial_adjacency_edges_rs` (200× raw kernel), S2 `weight_by_distance_rs` (12.18× raw / 2.84× end-to-end). Consumed via `scripts/vitruvius/spatial/spatial_edge_builder.py` and `scripts/vitruvius/spatial/proximity_jump.py`.
- `stats_kernels` — N4 `mahalanobis_distance_rs` (2.73× end-to-end). Consumed via `scripts/vitruvius/normalization/outlier_detector.py`.
- N1 (`wasserstein_merge_decision`) is DEFER_ALREADY_NATIVE — POT's `ot.emd2` backend is already native C++.
- Both `rust_mig_spatial_kernels` and `rust_mig_stats_kernels` default **true** per AD-038. Python fallback retained for each.

### Sprint AUDIT-1 — Advanced Tech Audit (AD-039)

Three-topic audit. FlatBuffers: NO_GO (5–10× slower than CPython `_json` at ~150-record payloads). Monte Carlo Dropout: PARK (0 viable injection sites). Numerical Integrity: GO_GAP — SHA-256 footer shipped:

- `scripts/vitruvius/spatial/contract_reader.py` — `parse_contract()` / `ContractParseResult` / `IntegrityError`. Reads `# sha256: <hex>` footer appended by the TypeScript writer.
- `spatial-daemon/src/contract_writer.ts` — `INTEGRITY_FOOTER_PREFIX` + `computeContractBodySha256()` + `writeContract()` footer append.
- `scripts/vitruvius/spatial/walker.py` now reads all contract files through `parse_contract()`, skipping on `IntegrityError`.

### Sprint PIPELINE-CLI — p1b_* live wiring (AD-040)

- New `convert-parsers-one` subcommand wired into `pipeline_cli.py`. Dispatches through `scripts/vitruvius/parsers/factory.py::build_default_orchestrator()` which resolves `p1b_*` flags to parser chains. Parallel to existing `convert-one` — byte-identity guarantee with all flags off.
- All five `p1b_*` flags stay **false** until real-corpus validation.

### Sprint PQ-1 — GraphSAGE Product Quantization (hp_graphsage_pq, AD-041)

- `scripts/vitruvius/graph/pq_codebook.py` — pure-numpy PQ implementation: `train_pq_codebook`, `encode_to_pq`, `decode_from_pq`, `adc_distance`. 32× compression (256 B → 8 B per node; M=8, k=256). Cosine delta 0.00017 on held-out set.
- `scripts/vitruvius/graph/graphsage_pq.py` — `compress_graphsage_report`.
- Flag `hp_graphsage_pq` defaults **false** pending an embedding-persistence layer.

### Sprint LSH-1 — MinHash LSH fuzzy dedup (w_lsh_dedup, AD-042)

- `scripts/vitruvius/relationships/minhash.py` — `compute_minhash_signature`, vectorized NumPy permutation.
- `scripts/vitruvius/relationships/lsh_index.py` — `LSHIndex` band-based bucketing (BLAKE2b-128 per band).
- `scripts/vitruvius/relationships/lsh_dedup.py` — `dedupe_by_endpoints_lsh` union-find collapse.
- Flag `w_lsh_dedup` defaults **false** per plan §1.3 non-breaking contract.

### Sprint 1B-M1 / M2 / M3 — Phase 1B Modernization Tranches (p1b_* flags, AD-031/032/034)

Library-level parser chain wiring. All flags default false. See "Phase 1B parser chain" in the Core Packages listing for the `parsers/` subpackage layout.

---
````

- [ ] **Step 6: Gap 1.4 — replace the Feature-flag governance flag-families table.**

old_string:
```
Flag families by sprint:

| Sprint | Prefix | Example |
|---|---|---|
| Q — Live Wiring | `w_*` | `w_nb_prefilter`, `w_slm_router`, `w_choquet_fusion` |
| R — Per-Layer Embeddings | `y_*` | `y_contextual_priming`, `y_domain_routing_moe`, `y_vision_ocr` |
| PHYS — Graph Physics | `phys_*` | `phys_pagerank`, `phys_boltzmann_gate` |
| HP — High-Performance | `hp_*` | `hp_merkle_fs`, `hp_event_sourced_graph`, `hp_wasm_kernels`, `hp_graphsage` |
| HP.3-R — RocksDB KV backends | `hp_rocksdb_*` (defaults **true**) | `hp_rocksdb_event_store`, `hp_rocksdb_verdict_cache` |
| GEOM — Constraint Engine | `geom_*` | `geom_csp_compiler`, `geom_envelope_3d` |
| WIKI — Knowledge Synthesis | `wiki_*` | `wiki_docling_parser`, `wiki_kuzu_store`, `wiki_ego_linter` |
| GT — Geo-Topological | `gt_*` | `gt_temporal_graph`, `gt_proximity_jump`, `gt_engine_rs` |
| Z — Compound AI | `z_*` | `z_neuro_symbolic`, `z_adversarial_swarm`, `z_dspy_compiler` |
```

new_string:
```
Flag families by sprint:

| Sprint | Prefix | Example |
|---|---|---|
| Q — Live Wiring | `w_*` | `w_nb_prefilter`, `w_slm_router`, `w_choquet_fusion`, `w_lsh_dedup` |
| R — Per-Layer Embeddings | `y_*` | `y_contextual_priming`, `y_domain_routing_moe`, `y_vision_ocr` |
| PHYS — Graph Physics | `phys_*` | `phys_pagerank`, `phys_boltzmann_gate` |
| HP — High-Performance | `hp_*` | `hp_merkle_fs`, `hp_event_sourced_graph`, `hp_wasm_kernels`, `hp_graphsage`, `hp_graphsage_pq` |
| HP.3-R — RocksDB KV backends | `hp_rocksdb_*` | `hp_rocksdb_event_store`, `hp_rocksdb_verdict_cache` |
| GEOM — Constraint Engine | `geom_*` | `geom_csp_compiler`, `geom_envelope_3d` |
| WIKI — Knowledge Synthesis | `wiki_*` | `wiki_docling_parser`, `wiki_kuzu_store`, `wiki_ego_linter` |
| GT — Geo-Topological | `gt_*` | `gt_temporal_graph`, `gt_proximity_jump`, `gt_engine_rs` |
| Z — Compound AI | `z_*` | `z_neuro_symbolic`, `z_adversarial_swarm`, `z_dspy_compiler` |
| 1B-M1/M2/M3 + PIPELINE-CLI — Phase 1B Parsers | `p1b_*` | `p1b_docling_parser`, `p1b_rust_pdf_parser`, `p1b_ocr_preprocessor`, `p1b_process_pool_orchestration`, `p1b_libreoffice_preprocessor` |
| RUST-MIG-1 — Rust polyglot kernels | `rust_mig_*` | `rust_mig_spatial_kernels`, `rust_mig_stats_kernels` |

**Live-by-default flags** (these four default `true` in `config/vitruvius.yaml`; all others default `false`):

| Flag | Default | AD | Rationale |
|---|---|---|---|
| `hp_rocksdb_event_store` | `true` | AD-029 | 18.7× faster than SQLite at n=10000 |
| `hp_rocksdb_verdict_cache` | `true` | AD-029 | 24.3× faster than SQLite at n=10000 |
| `rust_mig_spatial_kernels` | `true` | AD-038 | S1 200× / S2 12.18× raw kernel wins; both clear ≥2× gate |
| `rust_mig_stats_kernels` | `true` | AD-038 | N4 2.73× end-to-end win; N1 DEFER_ALREADY_NATIVE |
```

- [ ] **Step 7: Gap 1.5 — replace the Core Packages listing with the complete subpackage map.**

old_string:
```
  - `scripts/`: CLI entrypoints and utility scripts.
    - `pipeline_cli.py`: The primary system orchestrator.
    - `vitruvius/`: The main functional package.
      - `scanner.py`, `status.py`: Ingestion and state tracking.
      - `conversion.py`, `ocr.py`, `office.py`, `spreadsheets.py`: Data transformation and OCR.
      - `canonicalize.py`, `concepts.py`: Mapping to the canonical knowledge layer.
      - `relationships.py`, `relationships_sections.py`: Link extraction logic.
      - `ollama_review.py`: LLM-based review and verification.
      - `paths.py`, `constants.py`: Filesystem contract enforcement.
```

new_string:
```
  - `scripts/`: CLI entrypoints and utility scripts.
    - `pipeline_cli.py`: The primary system orchestrator.
    - `vitruvius/`: The main functional package.
      - `scanner.py`, `status.py`: Ingestion and state tracking (Sprint C added SHA-256 file hashing per AD-022).
      - `conversion.py`, `detection.py`, `ocr.py`, `office.py`, `spreadsheets.py`: Data transformation and OCR.
      - `canonicalize.py`, `concepts/`: Mapping to the canonical knowledge layer (Phase 3C deterministic enrichment).
      - `relationships/`, `relationships.py`, `relationships_sections.py`: Link extraction logic (includes MinHash LSH dedup via Sprint LSH-1).
      - `ollama_review.py`, `ollama_review_second_pass.py`, `review_routing.py`: LLM-based review and verification.
      - `normalization/`: Tier A/B/C normalization rules + AST chunker + refine (Sprint B, AD-007).
      - `extraction/`: CRF extractor, KG link predictor, TF-IDF concept matcher.
      - `pre_review/` and `review/`: NB prefilter, ontology prompt builder, SLM router, conformal gate, tension analyzer, Choquet aggregator, CoT audit, stateful registry, RocksDB stateful registry (Sprints Q + R + HP.3-R).
      - `promotion/`: Bayesian fusion, stringency matrix, temporal edges (Sprint A + Sprint Q + Sprint GT.3.1).
      - `priming/`: Source identity vector, prefix injector, drift detector (Sprint R Y1).
      - `graph/`: `GraphNode` / `GraphEdge` / `GraphSnapshot` / `TemporalEdge` contract, SQLite + RocksDB event stores, GraphSAGE embeddings, PQ codebook, temporal query, Parquet archiver, MC dropout utility, Wasserstein merge, physics kernels (PageRank / Boltzmann / VF2 / Shannon / eigenvector cascade).
      - `spatial/`: Spatial edge builder, proximity jump, Z3 constraint solver, contract reader (SHA-256 integrity), walker.
      - `geometric/`: Z3 CSP inequality compiler, 2D/3D buildable envelope, Pareto optimizer (Sprint GEOM).
      - `wiki/`: Docling parser, Kuzu store, delta tracker, LLM synthesis loop, ego linter, Ollama LLM client (Sprint WIKI).
      - `compound/`: Adversarial swarm, DSPy compiler, dependency tracker, differential propagator, Datalog logic schema, Wasm kernel wrapper (Sprint Z).
      - `foraging/`: Bloom filter foraging hints (Sprint GT.5.2).
      - `bench/`: Live wall-clock / peak-RSS benchmark harnesses + KV backend comparison + LSH dedup bench.
      - `ontology/`: OWL/Turtle exporter (rdflib 7.6), `export-graph-owl` CLI handler, IFC registry (`ifc_registry.py`).
      - `query/`: Natural-language and structured graph query handlers.
      - `parsers/`: `BaseParser`, `ParserOrchestrator`, document taxonomy, Shannon classifier, `DoclingParser`, `LibreOfficePreprocessor`, `OCRPreprocessor`, `OpenDataLoaderParser`, `RustPdfParser`, quality gates (GATE-005/006), factory, CLI handler (Phase 1B modernization).
      - `migrations/`: Registry migration helpers.
      - `merkle_fs.py`: HP.1 Merkle directory hash.
      - `kv_migrate.py`: Sprint HP.3-R one-shot SQLite → RocksDB migration CLI handler.
      - `features.py`, `config.py`: Feature-flag loader and config reader (Ollama URL / default model live here, not hardcoded).
      - `engine_rs/`: pyo3 workspace (Cargo) with `core/` (pure Rust + wasm32 target: `SpatialPoint` + `LinearOctree` + `aabb_intersects`), `pyo3_shim/` (Python bindings), `spatial_kernels/` (S1/S2 Rust ports), `stats_kernels/` (N4 Mahalanobis port).
      - `datalog_rs/`: Hand-rolled Rust Datalog evaluator (`evaluate_datalog(facts, rules)`).
      - `paths.py`, `constants.py`: Filesystem contract enforcement.
```

- [ ] **Step 8: Gap 1.6 — add `001B_Spatial-Source-Layer/` to the Root Layers listing.**

old_string:
```
- `001_Raw-Source-Layer/`: Entry point for all source documents.
- `002_Raw-Conversion-Layer/`: Intermediate artifacts (Markdown, Sidecar JSON) generated by the conversion subsystem.
```

new_string:
```
- `001_Raw-Source-Layer/`: Entry point for all source documents.
- `001B_Spatial-Source-Layer/`: Spatial contract files (GJK/AABB geometry JSON) produced by the `spatial-daemon` TypeScript subproject. Files carry a `# sha256: <hex>` integrity footer (AD-039); Python consumers read them through `scripts/vitruvius/spatial/contract_reader.py::parse_contract()`.
- `002_Raw-Conversion-Layer/`: Intermediate artifacts (Markdown, Sidecar JSON) generated by the conversion subsystem.
```

- [ ] **Step 9: Gap 1.7 — replace the stale "Planned (Roadmap)" bullet list.**

old_string:
```
- **Planned (Roadmap):** 
  - Graph Database integration (Neo4j or similar) in `005`.
  - Advanced chunking and embedding pipelines for RAG.
  - Multi-parser strategy for complex document layouts.
```

new_string:
```
- **Implemented (feature-flagged, defaults false unless noted):**
  - Graph store: Kuzu hybrid vector+graph store (`wiki_kuzu_store` in `scripts/vitruvius/wiki/kuzu_store.py`) + append-only event store (SQLite + RocksDB, `hp_rocksdb_event_store` defaults **true**).
  - Embedding pipeline: GraphSAGE structural embeddings (`hp_graphsage`) + Product Quantization 32× compression (`hp_graphsage_pq`). Both in `scripts/vitruvius/graph/`.
  - Multi-parser strategy: Phase 1B `parsers/` subpackage (`DoclingParser`, `LibreOfficePreprocessor`, `OCRPreprocessor`, `RustPdfParser`, `ParserOrchestrator`) gated by `p1b_*` flags, wired into CLI via `convert-parsers-one`.
- **Still deferred:**
  - Sprint D Stream J (active learning) — externally gated on Ranger dashboard surface.
  - Sprint D Stream K (CLUP multi-jurisdiction scaling) — externally gated on second jurisdiction corpus.
```

- [ ] **Step 10: Gap 1.8 — expand the Rust crate count from 2 to 3 in the "Rust data plane" subsection.**

old_string:
```
Vitruvius now ships two pyo3 Rust crates built via `maturin develop --release`:

- `scripts/vitruvius/engine_rs/` — **Cargo workspace** split into `core/` (pure Rust, compiles for both native and `wasm32-unknown-unknown`) and `pyo3_shim/` (pyo3 bindings). Exports `SpatialPoint` + `LinearOctree` to Python and an `aabb_intersects` C-ABI function to Wasm. Consumed by `scripts/vitruvius/compound/wasm_kernel.py` via wasmtime.
- `scripts/vitruvius/datalog_rs/` — Sprint Z Stream S1.2 Rust evaluator. Hand-rolled Datalog engine (crepe proved too fragile on our ruleset). Entry point: `evaluate_datalog(facts, rules)`. 7 Rust unit tests.
```

new_string:
```
Vitruvius now ships three pyo3 Rust crate families built via `maturin develop --release`:

- `scripts/vitruvius/engine_rs/` — **Cargo workspace** with four member crates:
  - `core/` — pure Rust, compiles for both native and `wasm32-unknown-unknown`. Exports `SpatialPoint` + `LinearOctree` + `aabb_intersects` C-ABI.
  - `pyo3_shim/` — pyo3 Python bindings. Re-exports `build_spatial_adjacency_edges_rs`, `weight_by_distance_rs`, `mahalanobis_distance_rs`.
  - `spatial_kernels/` — Sprint RUST-MIG-1 S1/S2 ports (AD-038). Depends on `core` + `ndarray`.
  - `stats_kernels/` — Sprint RUST-MIG-1 N4 port (AD-038). Depends on `nalgebra` + `ndarray`. N1 (Wasserstein) is DEFER_ALREADY_NATIVE per AD-038a.
- `scripts/vitruvius/datalog_rs/` — Sprint Z Stream S1.2 hand-rolled Datalog evaluator (`evaluate_datalog(facts, rules)`). 7 Rust unit tests.
- `scripts/vitruvius/parsers/` contains a further Rust crate `vitruvius_rust_pdf` (lopdf-based PDF text extractor, AD-033/034). Peak RSS 13.7 MB vs docling's 659 MB; 625× faster wall time. Exposed as `RustPdfParser(BaseParser)` in Python.
```

- [ ] **Step 11: New section — append "Spatial Contract Integrity (AD-039)" at end of file.**

old_string:
```
See AD-029 in `/.ai/10_state/decisions.md` for the full bench ledger
and the O(1) `count()` optimization story.
```

new_string:
````
See AD-029 in `/.ai/10_state/decisions.md` for the full bench ledger
and the O(1) `count()` optimization story.

---

## Spatial Contract Integrity (AD-039, 2026-04-15)

The TypeScript `spatial-daemon` writes `spatial-*.json` files into
`001B_Spatial-Source-Layer/`. As of Sprint AUDIT-1 (AD-039), every
written file carries a one-line integrity footer:

```
# sha256: <64-hex-digits>
```

The hash covers the JSON body only (everything before the footer line).
Python consumers MUST read spatial contracts through:

- `scripts/vitruvius/spatial/contract_reader.py::parse_contract(path)` —
  returns `ContractParseResult(body, footer_sha256)`. Raises `IntegrityError`
  if `require_footer=True` and the footer is absent or the digest does not
  match.
- `scripts/vitruvius/spatial/walker.py` — already enforces this; any corrupt
  file is logged and skipped so a single bad file never poisons a run.

The TypeScript writer is at `spatial-daemon/src/contract_writer.ts::writeContract()`.

**Backwards compatibility:** `require_footer` defaults `False` so existing
on-disk fixtures that predate this commit continue to load. New production
call sites should opt in to `require_footer=True`.
````

- [ ] **Step 12: Verify all edits landed.**

```bash
cd /Users/philiplewis/vitruvius
grep -n "ten sprints" .ai/00_system/architecture.md || echo "OK: no stale 'ten sprints'"
grep -n "AD-024 through AD-029" .ai/00_system/architecture.md || echo "OK: no stale AD-029 ceiling"
grep -c "21 sprints" .ai/00_system/architecture.md
grep -c "AD-042" .ai/00_system/architecture.md
grep -c "Spatial Contract Integrity" .ai/00_system/architecture.md
grep -c "001B_Spatial-Source-Layer" .ai/00_system/architecture.md
grep -c "Live-by-default flags" .ai/00_system/architecture.md
```
Expected: first two greps print "OK: ...". Remaining greps return ≥1.

- [ ] **Step 13: Commit.**

```bash
cd /Users/philiplewis/vitruvius
git add .ai/00_system/architecture.md
git commit -m "$(cat <<'EOF'
docs(system): refresh architecture.md for 21-sprint reality + AD-042 + spatial integrity

- Fix stale "ten sprints" / "AD-024 through AD-029" ceiling references
- Add 11 missing sprint descriptions (1B-M1..LSH-1)
- Expand feature-flag table with p1b_*, rust_mig_* + live-by-default section
- Rewrite Core Packages listing with current 18-subpackage layout
- Add 001B_Spatial-Source-Layer to root layers
- Replace stale "Planned (Roadmap)" section with shipped/deferred reality
- Add Spatial Contract Integrity (AD-039) section documenting SHA-256 footer contract
EOF
)"
```

---

### Task 1.2: Update `.ai/00_system/naming-conventions.md`

**Files:**
- Modify: `/Users/philiplewis/vitruvius/.ai/00_system/naming-conventions.md` (120 lines pre-edit)

**Context:** Names only 7 pipeline stages, but real CLI has 41 subcommands. Has no feature-flag naming rules at all. Missing `supersedes` predicate. No Rust crate or TypeScript naming conventions. 6 gaps.

- [ ] **Step 1: Verify file length.**

```bash
wc -l /Users/philiplewis/vitruvius/.ai/00_system/naming-conventions.md
```
Expected: `120`.

- [ ] **Step 2: Gap 2.1 — replace the 7-stage pipeline list with the 41-command surface.**

old_string:
```
## Pipeline Stage Naming
Stages must match the `run_` functions in `pipeline_cli.py`:
1. `scan`
2. `status`
3. `lint`
4. `convert`
5. `canonicalize`
6. `relationships`
7. `review`
```

new_string:
```
## Pipeline Stage Naming

Commands are kebab-case and match `subparsers.add_parser(...)` entries in `scripts/pipeline_cli.py`.
The complete command surface (41 commands as of AD-042) is grouped by functional area:

### Baseline pipeline
- `run` — Scan → Status → Lint composite.
- `run-with-review` — Full pipeline including LLM review.
- `scan` — Crawl `001_Raw-Source-Layer` and update file registry.
- `status` — Compare filesystem against registry.
- `lint` — Naming and structural integrity checks.
- `reconcile` — Detect orphaned/stale artifacts.

### Conversion
- `convert` — Batch convert new/changed files.
- `convert-one <rel_pdf_path>` — Convert a single PDF via legacy route.
- `convert-parsers-one <rel_pdf_path>` — Convert via Phase 1B `ParserOrchestrator` (`p1b_*` flags).
- `convert-spreadsheet-one <rel_path>` — Convert a single spreadsheet.
- `detect-one <rel_pdf_path>` — Classify PDF document type.
- `ocr-queue` — Identify scanned PDFs needing OCR.
- `ocr-execute` — Execute OCR on queued files.

### Canonicalization
- `canonicalize` — Batch canonicalize all unconverted files.
- `canonicalize-one <rel_md_path>` — Canonicalize a single markdown file.
- `canonicalize-plan-one <rel_md_path>` — Dry-run canonicalization plan.
- `canonicalize-concept-one <concept_slug>` — Create/update a single concept file.

### Refinement
- `refine` — Batch refinement pass (Sprint B NormalizationEngine).
- `refine-one <rel_md_path>` — Refine a single canonical file.

### Relationship extraction
- `extract-relationships-one <rel_md_path>` — Pattern-based extraction on a single source.
- `extract-relationships-sections-one <rel_md_path>` — Section-aware extraction (supports `w_lsh_dedup`).

### Concept enrichment
- `enrich-concept-one <concept_slug>` — LLM-driven enrichment of one concept.
- `enrich-concepts` — Batch concept enrichment.

### Review
- `review-relationships-ollama` — LLM review pass (supports all `w_*` / `y_*` flags).
- `review-relationships-ollama-second-pass` — Tier-2 model second-pass review.

### Promotion
- `promote` — Promote verified relationships to canonical layer (supports `--execute` / `--rollback`).

### Graph
- `build-graph` — Build graph snapshot from promoted relationships.
- `query-graph` — Walk graph from a source node to a target node.
- `export-graph-snapshot` — Export latest graph snapshot to JSON.
- `export-graph-owl` — Export graph as RDF Turtle via rdflib.

### Spatial
- `ingest-spatial` — Ingest geometry contracts from `001B_Spatial-Source-Layer`.
- `evaluate-spatial` — Run Z3 spatial constraint evaluation against named concepts.

### Registry and maintenance
- `rotate-registries` — Prune old timestamped registry snapshots (default: keep last 30).
- `migrate-ids-plan` — Dry-run ID migration plan.
- `migrate-ids-apply` — Apply an ID migration.
- `ple-kv-migrate` — Sprint HP.3-R: migrate SQLite KV store to RocksDB.

### Query (natural language)
- `query <question>` — Natural-language graph query.
- `query-structured` — Structured function-based graph query.

### Operator utilities (ple-* prefix)
- `ple-cotrace-dump` — Summarise a Chain-of-Thought audit trace directory.
- `ple-registry-purge` — Delete stale rows from the stateful review registry.
- `ple-vision-probe` — Pre-flight check for vision OCR RAM + model availability.

## Feature Flag Naming

Flags live under the `features:` key in `config/vitruvius.yaml`. Naming rules:

- Format: `<stream_prefix>_<snake_case_name>` (lowercase, underscores, no hyphens).
- Every new flag MUST be registered in `EXPECTED_FLAGS` inside `scripts/tests/test_features.py` before merging — CI fails otherwise.
- Every new flag MUST default `false` unless it has cleared a measured ≥2× performance gate and received an AD sign-off (see AD-029 and AD-038 for the two existing exceptions).

### Flag prefix registry

| Prefix | Sprint | Governs |
|---|---|---|
| `a_` … `k_` | Sprint D (Streams A–K) | Statistical & architectural upgrade streams |
| `l_` … `o_` | Sprint H (Streams L–O) | 3D spatial intelligence / epistemic foraging |
| `w_*` | Sprint Q + LSH-1 | Live wiring, 8GB LLM mode, LSH dedup |
| `y_*` | Sprint R | Per-layer embeddings, agentic reasoning |
| `phys_*` | Sprint PHYS | Graph physics (PageRank, Boltzmann, VF2, Shannon, eigenvector) |
| `hp_*` | Sprint HP + PQ-1 | High-performance optimizations (Merkle, event-sourced graph, Wasm, GraphSAGE, PQ) |
| `hp_rocksdb_*` | Sprint HP.3-R | RocksDB KV backends — default **true** (AD-029) |
| `geom_*` | Sprint GEOM | Geometric constraint engine |
| `wiki_*` | Sprint WIKI | Autonomous knowledge synthesis |
| `gt_*` | Sprint GT | Geo-topological graph + spatial GraphRAG |
| `z_*` | Sprint Z | Compound AI (adversarial swarm, DSPy, Datalog bridge, differential dataflow) |
| `p1b_*` | Sprints 1B-M1/M2/M3 + PIPELINE-CLI | Phase 1B multi-parser chain (deployment-readiness markers) |
| `rust_mig_*` | Sprint RUST-MIG-1 | Python→Rust polyglot kernels — default **true** (AD-038) |
```

- [ ] **Step 3: Gap 2.3 — expand Module/Package Naming to cover Rust crates.**

old_string:
```
### Module and Package Naming
- **Packages:** Lowercase, single word if possible, or use underscores (e.g., `vitruvius`).
- **Modules:** Lowercase with underscores (e.g., `canonicalize.py`, `ollama_review.py`).
- **Scripts:** Lowercase with underscores, often suffixed with `_cli` or `_one` (e.g., `pipeline_cli.py`, `Word-PPT-To-PDF.py` - *Note: The latter is a legacy inconsistency to be corrected*).
```

new_string:
```
### Module and Package Naming
- **Python packages:** Lowercase, single word if possible, or use underscores (e.g., `vitruvius`).
- **Python modules:** Lowercase with underscores (e.g., `canonicalize.py`, `ollama_review.py`).
- **Python scripts:** Lowercase with underscores, often suffixed with `_cli` or `_one` (e.g., `pipeline_cli.py`).
- **Rust crates (library name):** `vitruvius_<snake_case>` (e.g., `vitruvius_engine_rs`, `vitruvius_datalog_rs`, `vitruvius_rust_pdf`). The `pyo3_shim` member that bridges Python uses the same convention.
- **Rust workspace member directory names:** `<snake_case>` without the `vitruvius_` prefix (e.g., `engine_rs/core/`, `engine_rs/spatial_kernels/`, `engine_rs/stats_kernels/`). All members live under `scripts/vitruvius/engine_rs/` or a sibling workspace root.
- **pyo3-exported Python symbols:** Suffix `_rs` to distinguish from Python fallback functions in the same call site (e.g., `build_spatial_adjacency_edges_rs`, `weight_by_distance_rs`, `mahalanobis_distance_rs`). The Python fallback uses the bare name without `_rs`.

### TypeScript (spatial-daemon) Conventions
- **Source files:** Inside `spatial-daemon/src/`. Existing files use underscore_case (`contract_writer.ts`, `aabb.ts`); new files follow the same pattern for consistency with the existing directory layout.
- **Exported constants:** `UPPER_CASE_WITH_UNDERSCORES` (e.g., `INTEGRITY_FOOTER_PREFIX`).
- **Exported functions:** `camelCase` verbs (e.g., `writeContract`, `computeContractBodySha256`).
- **Schema files:** `types.ts` MUST mirror the corresponding Python `schema.py` byte-for-byte in structure (enforced by code review).
- **Test files:** `*.test.ts` co-located with source, run via `vitest`.
```

- [ ] **Step 4: Gap 2.5 — add `supersedes` to the Relationship Naming predicate list.**

old_string:
```
Relationships extracted between entities must use lowercase verbs:
- `requires`
- `defines`
- `depends_on`
- `limits`
- `affects`
- `governs` (Law → Concept)
```

new_string:
```
Relationships extracted between entities must use lowercase verbs (closed vocabulary — additions require a schema bump AND an AD per I4):
- `requires`
- `defines`
- `depends_on`
- `limits`
- `affects`
- `governs` (Law → Concept)
- `supersedes` (newer law/version → older)
```

- [ ] **Step 5: Gap 2.6 — add `ple-` operator-command prefix to CLI and Entrypoint Naming.**

old_string:
```
## CLI and Entrypoint Naming
- **Commands:** Lowercase with hyphens (kebab-case) (e.g., `scan`, `status`, `ocr-queue`, `canonicalize-one`).
- **Arguments:** Lowercase with underscores (snake_case) (e.g., `relative_pdf_path`).
- **Flags:** Lowercase with hyphens (kebab-case) (e.g., `--sample-pages`, `--no-deskew`).
```

new_string:
```
## CLI and Entrypoint Naming
- **Commands:** Lowercase with hyphens (kebab-case) (e.g., `scan`, `status`, `ocr-queue`, `canonicalize-one`).
- **Operator-utility commands:** Prefixed with `ple-` (e.g., `ple-kv-migrate`, `ple-cotrace-dump`, `ple-registry-purge`, `ple-vision-probe`). The `ple-` prefix marks commands that are not part of the standard pipeline run but are privileged operator tools for maintenance, migration, or diagnostics.
- **Arguments:** Lowercase with underscores (snake_case) (e.g., `relative_pdf_path`).
- **Flags:** Lowercase with hyphens (kebab-case) (e.g., `--sample-pages`, `--no-deskew`).
```

- [ ] **Step 6: Update the changelog footer.**

old_string:
```
## Changelog
- **2026-04-13:** Initial version established from codebase audit. Standardized timestamp formats, ID prefixes, and report naming patterns.
```

new_string:
```
## Changelog
- **2026-04-13:** Initial version established from codebase audit. Standardized timestamp formats, ID prefixes, and report naming patterns.
- **2026-04-15:** Expanded Pipeline Stage Naming from 7 to 41 commands (as of AD-042). Added Feature Flag Naming section with prefix registry. Added Rust crate and pyo3 symbol naming rules (AD-036). Added TypeScript (spatial-daemon) conventions. Added `supersedes` predicate. Added `ple-` operator-utility command prefix.
```

- [ ] **Step 7: Verify.**

```bash
cd /Users/philiplewis/vitruvius
grep -c "supersedes" .ai/00_system/naming-conventions.md
grep -c "Feature Flag Naming" .ai/00_system/naming-conventions.md
grep -c "ple-" .ai/00_system/naming-conventions.md
grep -c "rust_mig_" .ai/00_system/naming-conventions.md
grep -c "convert-parsers-one" .ai/00_system/naming-conventions.md
```
Expected: all return ≥1.

- [ ] **Step 8: Commit.**

```bash
cd /Users/philiplewis/vitruvius
git add .ai/00_system/naming-conventions.md
git commit -m "$(cat <<'EOF'
docs(system): refresh naming-conventions.md for 41-cmd CLI + flag/Rust/TS rules

- Expand Pipeline Stage Naming from 7 to 41 commands
- Add Feature Flag Naming section with 13-prefix registry
- Add Rust crate, pyo3 symbol, and TypeScript naming rules
- Add supersedes predicate to relationship vocabulary
- Add ple- operator-command prefix convention
EOF
)"
```

---

### Task 1.3: Update `.ai/00_system/pipeline-overview.md`

**Files:**
- Modify: `/Users/philiplewis/vitruvius/.ai/00_system/pipeline-overview.md` (230 lines pre-edit)

**Context:** The file says "Promotion: NOT IMPLEMENTED" and "Storage (Graph): NOT IMPLEMENTED" — both wrong. The "Post-Sprint-D Pipeline Additions" section covers only 10 of the 21 closed sprints. 6 gaps.

- [ ] **Step 1: Verify file length.**

```bash
wc -l /Users/philiplewis/vitruvius/.ai/00_system/pipeline-overview.md
```
Expected: `230`.

- [ ] **Step 2: Gap 3.2 — fix the Promotion stage status row.**

old_string:
```
| Promotion | NOT IMPLEMENTED | Moving from `draft` to `verified` is manual. |
```

new_string:
```
| Promotion | IMPLEMENTED | `run_promote()` in `scripts/vitruvius/promotion/`. Stringency matrix gate (`w_promotion_stringency_gate`), stateful registry (`y_stateful_registry`), RocksDB backend (`hp_rocksdb_verdict_cache`, default `true`). CLI: `promote --execute` / `promote --rollback <batch_id>`. |
```

- [ ] **Step 3: Gap 3.3 — fix the Storage (Graph) stage status row (replace one row with three more specific rows).**

old_string:
```
| Storage (Graph) | NOT IMPLEMENTED | Planned for Layer 005. |
```

new_string:
```
| Storage (Graph — Event Store) | IMPLEMENTED | Append-only SQLite event log (`graph/event_store.py`) with RocksDB backend (`graph/rocksdb_event_store.py`, `hp_rocksdb_event_store` defaults `true`). Factory: `make_event_store()`. |
| Storage (Graph — Knowledge Synthesis) | IMPLEMENTED (feature-flagged) | Kuzu hybrid vector+graph store (`wiki/kuzu_store.py`, `wiki_kuzu_store` flag). |
| Storage (Graph — Temporal) | IMPLEMENTED (feature-flagged) | `TemporalEdge` + `temporal_query.query_at()` + Parquet archiver (`gt_temporal_graph` flag). |
```

- [ ] **Step 4: Gap 3.5 — fix the Current Limitations bullet about state persistence.**

old_string:
```
- **State Persistence:** Entirely filesystem-based; no database for querying across files.
```

new_string:
```
- **State Persistence:** Primary state tracking is filesystem-based (registries in `006_System-Manifests`). Optional KV and graph persistence is available via `hp_rocksdb_event_store` (default on), `hp_rocksdb_verdict_cache` (default on), and `wiki_kuzu_store` (default off).
```

- [ ] **Step 5: Gap 3.4 — replace the Missing Stages section with externally-gated items only.**

old_string:
```
## Missing Stages
- **Automated Promotion:** No automated workflow to promote artifacts from conversion to canonical without manual ID verification.
- **Graph Ingestion:** No automatic sync to a graph database (e.g., Neo4j).
```

new_string:
```
## Externally-Gated Stages (deferred until external conditions met)
- **Sprint D Stream J — Active learning loop:** Requires the Ranger dashboard surface. Not dispatchable until that external dependency is available.
- **Sprint D Stream K — CLUP multi-jurisdiction scaling:** Requires a second jurisdiction corpus to benchmark against. Not dispatchable until that corpus is available.
```

- [ ] **Step 6: Gap 3.6 — append 5 missing sprint subsections to the Post-Sprint-D section. Insert after the Sprint HP subsection, before the Changelog.**

old_string:
```
See `.ai/10_state/decisions.md` AD-024 through AD-029 for the per-sprint ledger including commit SHAs and sprint tags.

## Changelog
```

new_string:
````
See `.ai/10_state/decisions.md` AD-024 through AD-042 for the per-sprint ledger including commit SHAs and sprint tags.

### Sprint RUST-PDF-1 / 1B-M1 / 1B-M2 / 1B-M3 — Phase 1B Parser Chain (p1b_* flags, AD-031–034)

New `convert-parsers-one` parallel command routes a single document through the Phase 1B `ParserOrchestrator`. Activated by `p1b_*` deployment-readiness flags (all default `false`):

- `p1b_docling_parser` — DoclingParser via Docling library
- `p1b_libreoffice_preprocessor` — LibreOffice PDF preprocessing
- `p1b_ocr_preprocessor` — OCRPreprocessor wrapping ocrmypdf
- `p1b_process_pool_orchestration` — `process_batch` sequential (pickle-safety deferred)
- `p1b_rust_pdf_parser` — RustPdfParser (lopdf, 625× faster / 48× less RAM than docling)

No change to existing `convert-one` path when all flags are off.

### Sprint RUST-MIG-1 — Rust polyglot kernels (rust_mig_* flags, AD-036/038, defaults TRUE)

Three Python compute kernels ported to Rust with Python fallback:

- `build_spatial_adjacency_edges` (S1) — 200× raw kernel speedup; called in `spatial/spatial_edge_builder.py`
- `weight_by_distance` (S2) — 12.18× raw / 2.84× end-to-end; called in `spatial/proximity_jump.py`
- `mahalanobis_distance` (N4) — 2.73× end-to-end; called in `normalization/outlier_detector.py`

Both `rust_mig_spatial_kernels` and `rust_mig_stats_kernels` default `true`. Flag-off restores pure Python behavior with byte-identical output.

### Sprint AUDIT-1 — Spatial contract integrity (AD-039)

Adds a SHA-256 integrity footer to all spatial contract files written by the TypeScript daemon. `spatial/walker.py` now reads all contract files through `contract_reader.parse_contract()`, skipping corrupted files. No change to pipeline flow; this is a correctness hardening of the spatial ingest stage.

### Sprint PIPELINE-CLI — p1b_* live wiring (AD-040)

Adds `convert-parsers-one` to `pipeline_cli.py` as a parallel conversion command. Wires all 5 `p1b_*` flags end-to-end through `parsers/factory.py::build_default_orchestrator()`. Byte-identity with all flags off verified by the `test_pipeline_cli_byte_identity.py` exit gate.

### Sprint PQ-1 — GraphSAGE Product Quantization (hp_graphsage_pq, AD-041)

32× compression of GraphSAGE embeddings (256 B → 8 B per node). Cosine reconstruction delta 0.00017. Flag `hp_graphsage_pq` defaults `false` pending an embedding-persistence layer. No impact on the main pipeline flow.

### Sprint LSH-1 — MinHash LSH fuzzy dedup (w_lsh_dedup, AD-042)

When `w_lsh_dedup` is `true`, `extract-relationships-sections-one` calls `dedupe_by_endpoints_lsh` instead of the baseline exact-endpoint dedup. Zero false positives on disjoint pairs measured; probabilistic collapse of near-duplicate pairs. Flag defaults `false` until a full PD 1096 operator run validates real-corpus behavior.

## Changelog
````

- [ ] **Step 7: Gap 3.1 — update the changelog entry to reflect 21 sprints, not 10.**

old_string:
```
- **2026-04-15:** Added **Post-Sprint-D Pipeline Additions** section covering all ten sprints (Q/R/PHYS/H/GEOM/WIKI/GT/HP/Z/HP.3-R) and their feature flags. Baseline flow documented above is unchanged.
```

new_string:
```
- **2026-04-15:** Added **Post-Sprint-D Pipeline Additions** section covering all 21 closed sprints (Q, R, PHYS, H, GEOM, WIKI, GT, HP, Z, HP.3-R, 1B-M1, 1B-M2, RUST-PDF-1, 1B-M3, DISTILL-1, RUST-MIG-1, AUDIT-1, PIPELINE-CLI, PQ-1, LSH-1, Meta) and their feature flags. Baseline flow documented above is unchanged. Promotion and Storage (Graph) stage status rows updated from NOT IMPLEMENTED to IMPLEMENTED — both shipped in Sprint Q / WIKI / HP / HP.3-R. Missing Stages section replaced with Externally-Gated Stages (Sprint D Streams J + K only).
```

- [ ] **Step 8: Verify.**

```bash
cd /Users/philiplewis/vitruvius
grep -n "NOT IMPLEMENTED" .ai/00_system/pipeline-overview.md || echo "OK: no NOT IMPLEMENTED stale claims"
grep -c "Sprint LSH-1" .ai/00_system/pipeline-overview.md
grep -c "21 closed sprints" .ai/00_system/pipeline-overview.md
```

- [ ] **Step 9: Commit.**

```bash
cd /Users/philiplewis/vitruvius
git add .ai/00_system/pipeline-overview.md
git commit -m "$(cat <<'EOF'
docs(system): refresh pipeline-overview.md for Promotion + Storage + 21 sprints

- Mark Promotion + Graph Event/Knowledge/Temporal Storage IMPLEMENTED
- Replace Missing Stages with Externally-Gated Stages (only Sprint D J/K)
- Add 5 new sprint subsections (1B-M*, RUST-MIG-1, AUDIT-1, PIPELINE-CLI, PQ-1, LSH-1)
- Update AD-029 pointer to AD-042 and sprint count 10 → 21
EOF
)"
```

---

### Task 1.4: Update `.ai/00_system/principles.md`

**Files:**
- Modify: `/Users/philiplewis/vitruvius/.ai/00_system/principles.md` (86 lines pre-edit)

**Context:** This is the most semantically loaded file. Principle 1 directly contradicts AD-029. Only 9 principles listed; EXECUTION_LOOP.md references P1–P10. Missing invariants I5/I6/I8/I9. Forbidden Patterns lists `.db` files which contradicts live SQLite/RocksDB stores. 8 gaps.

Before running any edits, verify the renumbering does NOT break references in other files.

- [ ] **Step 1: Pre-edit grep — check whether any other file references "Principle 9 — Local-First AI" by its current number.**

```bash
cd /Users/philiplewis/vitruvius
grep -rn --include="*.md" "Principle 9" . | grep -v ".ai/03_plans/2026-04-15-documentation-refresh-plan.md" || echo "OK: no external 'Principle 9' refs"
grep -rn --include="*.md" "P9 local" . | grep -v ".ai/03_plans/2026-04-15-documentation-refresh-plan.md" || echo "OK: no external 'P9 local' refs"
grep -rn --include="*.md" "P9 Local-First" . | grep -v ".ai/03_plans/2026-04-15-documentation-refresh-plan.md" || echo "OK: no external 'P9 Local-First' refs"
```
Expected: all print "OK: ...". If any hits exist outside this plan file, STOP and escalate — renumbering will break those references. Renumber cautiously or amend those references in a follow-up step.

- [ ] **Step 2: Gap 4.1 — rewrite Principle 1 to allow storage-layer KV exception.**

old_string:
```
### 1. The Filesystem is the Database
Vitruvius relies on a strict directory structure (`001` through `006`) rather than a hidden relational database to maintain state, track lineage, and store knowledge.
- **Enforcement:** Code MUST NOT introduce external databases (like SQLite, Postgres) for core document tracking.
- **Consequence:** If the filesystem structure defined in `constants.py` and `paths.py` is bypassed, the system will fail to track state.
```

new_string:
```
### 1. The Filesystem is the Database (for Document Lifecycle)
Vitruvius relies on a strict directory structure (`001` through `006`) and `006_System-Manifests` CSV registries to track document lineage, canonical state, and pipeline progress. These registries are the single source of truth for document lifecycle.
- **Enforcement:** Code MUST NOT introduce external databases (SQLite, Postgres, etc.) to replace or shadow the `006_System-Manifests` registries for document tracking. The canonical knowledge layer (`003`) and raw layer (`001`) MUST remain filesystem-only.
- **Storage-layer exception (AD-029):** The append-only event log (`graph/event_store.py`) and stateful review registry (`review/stateful_registry.py`) are performance-layer KV stores for graph events and LLM reviewer verdicts. These do NOT track document identity or pipeline state — they track graph mutation events and cached LLM decisions. They are accessed exclusively through factory functions (`make_event_store()` / `make_stateful_registry()`) that dispatch on feature flags, and both carry a filesystem fallback path.
- **Consequence:** If the filesystem structure defined in `constants.py` and `paths.py` is bypassed for document lifecycle tracking, the system will fail to track state. Storage-layer KV backends are additive performance wins, not replacements for the registry contract.
```

- [ ] **Step 3: Gap 4.2 — renumber "9. Local-First AI Review" to "8." and add P9, P10 afterward.**

old_string:
```
### 9. Local-First AI Review
Vitruvius prioritizes local, privacy-preserving AI processing.
- **Enforcement:** The review subsystem (`ollama_review.py`) MUST default to a local LLM runner (Ollama). External APIs (like OpenAI or Anthropic) are CONDITIONALLY ALLOWED only if explicitly configured as opt-in alternatives.
- **Consequence:** Forcing cloud dependencies breaks the system's ability to run air-gapped or on sensitive internal documents without review.
```

new_string:
```
### 8. Local-First AI Review
Vitruvius prioritizes local, privacy-preserving AI processing.
- **Enforcement:** The review subsystem (`ollama_review.py`) MUST default to a local LLM runner (Ollama) at `http://127.0.0.1:11434` (reads from `config/vitruvius.yaml` via `get_ollama_url()`, not hardcoded). External APIs (like OpenAI or Anthropic) are CONDITIONALLY ALLOWED only if explicitly configured as opt-in alternatives in `config/vitruvius.yaml`. Any new LLM integration that would break air-gap operation is XL-risk and requires explicit Philip consent (I7 in EXECUTION_LOOP.md).
- **Consequence:** Forcing cloud dependencies breaks the system's ability to run air-gapped or on sensitive internal documents without external review.

### 9. No Soft Output
Every pipeline stage must produce deterministic, verifiable artifacts. Probabilistic or "best-effort" output MUST carry an explicit confidence signal or be gated behind a review stage before promotion.
- **Enforcement:** Relationship candidates MUST NOT be promoted to the canonical layer (`003`) without passing through the review subsystem or a deterministic pre-review filter. Soft signals (scores, probabilities) that influence promotion MUST be written to `006_System-Manifests` as auditable artifacts.
- **Consequence:** Allowing unreviewed soft output to reach `003` produces an unauditable knowledge graph.

### 10. No Schema-less Growth
Every new structured artifact type (relationship predicates, canonical ID prefixes, flag names, report shapes) MUST be registered before deployment.
- **Enforcement:** New relationship predicates require a schema bump in `.ai/06_specs/relationship-schema.md` AND an AD. New canonical ID prefixes require an update to `naming-conventions.md` AND an AD. New feature flags require a `EXPECTED_FLAGS` entry in `scripts/tests/test_features.py` before merging (CI-enforced). See I3 and I4 in EXECUTION_LOOP.md.
- **Consequence:** Unregistered schema additions break graph lineage, cause test failures in `test_features.py`, and defeat the audit trail maintained by the AD ledger.
```

- [ ] **Step 4: Gap 4.7 — fix the Forbidden Patterns ".db" entry.**

old_string:
```
- **Hidden State:** Using `.pkl`, `.db`, or hidden configuration files to store pipeline progress outside of `006_System-Manifests`.
```

new_string:
```
- **Hidden State:** Using `.pkl` or hidden configuration files to store pipeline progress outside of `006_System-Manifests`. **Exception:** KV performance stores (SQLite `.db` event log and RocksDB directory in `005_Operational-Intelligence-Layer/`) are explicitly permitted per AD-029 when accessed through factory functions (`make_event_store()` / `make_stateful_registry()`). These stores do not track document identity or canonical state.
```

- [ ] **Step 5: Gap 4.3, 4.4, 4.5, 4.6 — add four new invariants (I5, I6, I8, I9) as a new section. Insert after the Conditional Patterns section and before the Enforcement Mechanisms section.**

old_string:
```
### Conditional Patterns
- **Manual Overrides:** Users can manually edit Canonical Markdown files in `003_Canonical-Knowledge-Layer`. However, if they break the YAML frontmatter schema, the `lint` stage must catch and flag it.

## Enforcement Mechanisms
```

new_string:
```
### Conditional Patterns
- **Manual Overrides:** Users can manually edit Canonical Markdown files in `003_Canonical-Knowledge-Layer`. However, if they break the YAML frontmatter schema, the `lint` stage must catch and flag it.

## Operational Invariants (from EXECUTION_LOOP.md v3.0)

These are BLOCK-level rules enforced by the daily execution loop. A plan that violates any of them is rejected before dispatch.

#### Lazy CLI Imports (AD-015, I5)
- **Rule:** Every `subparsers.add_parser(...)` dispatch branch in `scripts/pipeline_cli.py` MUST import its heavy dependencies INSIDE the `if args.command == "..."` branch, not at module top-level.
- **Enforcement:** `scripts/tests/test_cli_lazy_imports.py` asserts this automatically. Violation = BLOCK.
- **Consequence:** A top-level import of a heavy package (e.g., `docling`, `torch`, `rocksdict`) in `pipeline_cli.py` would add that package's load time to every CLI invocation, regardless of which command is run.

#### The Rust Line (AD-036, I6)
- **Rule:** Port a compute kernel to Rust only if the hot path is NOT already a single numpy/BLAS/C-native primitive call. Pure orchestration belongs in Python. Every Rust port MUST include a bench artifact demonstrating a ≥2× wall-time improvement on the measured kernel before the flag default is flipped to `true`.
- **Enforcement:** Any PR that ports a numpy hot loop to Rust without a bench artifact is BLOCK. Sprint PQ-1 and LSH-1 correctly recorded DEFER_ALREADY_NATIVE for numpy BLAS paths. Sprint RUST-MIG-1 (S1: 200×, S2: 12.18×, N4: 2.73×) cleared the gate.
- **Consequence:** Unnecessary Rust porting adds FFI overhead (pyo3 boundary cost) that can easily negate the kernel speedup. The ≥2× gate filters out false positives.

#### Test Baseline Monotonic (I8)
- **Rule:** The `pytest scripts/tests/` passing test count is monotonically non-decreasing across commits. The current baseline is **1528 passed / 1 skipped** (as of Sprint LSH-1 closure, AD-042).
- **Enforcement:** Any plan that reduces the passing-test count without replacing the deleted coverage with equivalent tests is BLOCK. A sprint that adds new behavior MUST add tests for that behavior; the net test delta must be ≥0.
- **Consequence:** Shrinking the test suite destroys the regression safety net that makes feature-flag defaults safe to flip.

#### Registry Single-Writer (I9)
- **Rule:** CSV registries under `006_System-Manifests/registries/` are single-writer per pipeline stage. Concurrent writes to the same registry from multiple processes or threads are FORBIDDEN without a lock design and an AD.
- **Enforcement:** Code review. Any plan that introduces parallel pipeline execution across stages (e.g., `ProcessPoolExecutor` at the stage level) must explicitly design a registry lock before dispatch.
- **Consequence:** Concurrent registry mutation produces corrupted CSV state that breaks `status.py` and `reconcile.py`.

## Enforcement Mechanisms
```

- [ ] **Step 6: Gap 4.8 — update the changelog footer.**

old_string:
```
## Changelog
- **2026-04-13:** Initial set of principles derived from codebase audit. Formally documented Filesystem-as-Database, Idempotency, and Traceability rules.
```

new_string:
```
## Changelog
- **2026-04-13:** Initial set of principles derived from codebase audit. Formally documented Filesystem-as-Database, Idempotency, and Traceability rules.
- **2026-04-15:** Updated to reflect 21 sprint closures. P1 enforcement clause amended to allow storage-layer KV backends per AD-029. Renumbered Local-First AI from P9 to P8. Added P9 (No Soft Output) and P10 (No Schema-less Growth) from EXECUTION_LOOP.md v3.0 canonical P-list. Added Operational Invariants section with I5 (Lazy CLI Imports / AD-015), I6 (Rust Line / AD-036), I8 (Test Baseline Monotonic), I9 (Registry Single-Writer). Updated Forbidden Patterns to permit `.db` KV stores per the AD-029 storage exception.
```

- [ ] **Step 7: Verify.**

```bash
cd /Users/philiplewis/vitruvius
grep -c "### 8. Local-First AI" .ai/00_system/principles.md
grep -c "### 9. No Soft Output" .ai/00_system/principles.md
grep -c "### 10. No Schema-less Growth" .ai/00_system/principles.md
grep -c "Lazy CLI Imports" .ai/00_system/principles.md
grep -c "Rust Line" .ai/00_system/principles.md
grep -c "Test Baseline Monotonic" .ai/00_system/principles.md
grep -c "Registry Single-Writer" .ai/00_system/principles.md
grep -c "Storage-layer exception" .ai/00_system/principles.md
grep -n "Code MUST NOT introduce external databases (like SQLite, Postgres)" .ai/00_system/principles.md || echo "OK: old contradictory clause removed"
```
Expected: all returns ≥1; last grep prints "OK: ...".

- [ ] **Step 8: Run the test baseline to confirm principle edits did not break anything (sanity check — this is a docs-only file so it shouldn't, but I8 says we always check).**

```bash
cd /Users/philiplewis/vitruvius
pytest scripts/tests -q 2>&1 | tail -3
```
Expected: `1528 passed, 1 skipped`.

- [ ] **Step 9: Commit.**

```bash
cd /Users/philiplewis/vitruvius
git add .ai/00_system/principles.md
git commit -m "$(cat <<'EOF'
docs(system): principles.md P1 storage exception + P9/P10 + I5/I6/I8/I9

- P1 updated with AD-029 storage-layer KV exception (SQLite/RocksDB allowed)
- Renumber Local-First AI P9 → P8
- Add P9 (No Soft Output) and P10 (No Schema-less Growth) from EXECUTION_LOOP v3.0
- Add Operational Invariants section: I5 lazy CLI imports, I6 Rust Line,
  I8 test baseline monotonic, I9 registry single-writer
- Remove .db from Forbidden Patterns with AD-029 exception note
EOF
)"
```

---

## Phase 2: Schema Specs (4 files, 6 + 8 + 5 + 6 = 25 gaps)

This phase refreshes `.ai/06_specs/` to match the actual frontmatter that production code writes. The main risk is that Phase 2 changes schema docs while the code keeps the old shape — verify each field is actually written by the code before adding it.

### Task 2.1: Update `.ai/06_specs/concept-schema.md`

**Files:**
- Modify: `/Users/philiplewis/vitruvius/.ai/06_specs/concept-schema.md` (186 lines pre-edit)

**Context:** Missing `stringency_vector` frontmatter field (actually written by the promotion stringency resolver). References a non-existent `ifc_validator.py` — real module is `ifc_registry.py`. References "Phase 7" as future when it has shipped. 6 gaps.

- [ ] **Step 1: Verify file length and key strings.**

```bash
cd /Users/philiplewis/vitruvius
wc -l .ai/06_specs/concept-schema.md
grep -c "ifc_validator.py" .ai/06_specs/concept-schema.md
grep -c "stringency_vector" .ai/06_specs/concept-schema.md
```
Expected: 186 lines, 1 match for `ifc_validator.py`, 0 matches for `stringency_vector` (it's missing).

- [ ] **Step 2: Verify the truth sources before editing.**

```bash
cd /Users/philiplewis/vitruvius
grep -n "stringency_vector" scripts/vitruvius/promotion/stringency_resolver.py | head -5
grep -n "stringency_vector" scripts/vitruvius/linting.py | head -5
grep -n "load_ifc_mapping\|ifc_class" scripts/vitruvius/ontology/ifc_registry.py | head -5
```
Expected: `stringency_resolver.py` has the field write; `linting.py` enforces it; `ifc_registry.py` is the real validator module.

- [ ] **Step 3: Gap 1.2 — fix the IFC validator module name (L59 area).**

old_string:
```
| `ifc_class` | string | *(Stream M.2)* IFC 4.3 class name that best models this concept (e.g., `IfcDoor`, `IfcWall`, `IfcSpace`). Must start with `Ifc`. Validated by `scripts/vitruvius/ontology/ifc_validator.py` against `scripts/vitruvius/ontology/ifc_mapping.yaml`. |
```

new_string:
```
| `ifc_class` | string | *(Stream M.2)* IFC 4.3 class name that best models this concept (e.g., `IfcDoor`, `IfcWall`, `IfcSpace`). Must start with `Ifc`. Loaded and validated by `scripts/vitruvius/ontology/ifc_registry.py` against `scripts/vitruvius/ontology/ifc_mapping.yaml`. |
```

- [ ] **Step 4: Gap 1.1 — add `stringency_vector` optional field row immediately after the `ifc_psets` row.**

old_string:
```
| `ifc_psets` | string[] | *(Stream M.2)* Optional list of IFC Property Set names paired with `ifc_class` (e.g., `[Pset_DoorCommon]`). Purely descriptive until Stream M.4 lint runs — no behaviour change if omitted. |
```

new_string:
```
| `ifc_psets` | string[] | *(Stream M.2)* Optional list of IFC Property Set names paired with `ifc_class` (e.g., `[Pset_DoorCommon]`). Purely descriptive until Stream M.4 lint runs — no behaviour change if omitted. |
| `stringency_vector` | enum | *(Sprint W3.1/W3.2)* Numeric conflict-resolution policy when two edges compete for the same `(from_entity, predicate, to_entity)` triplet. Allowed values: `maximize` \| `minimize` \| `qualitative`. Default: `qualitative`. Enforced by `run_lint` (`scripts/vitruvius/linting.py`); injected by migration at `scripts/vitruvius/migrations/add_stringency_vector.py`. |
```

- [ ] **Step 5: Gap 1.3 — update §9.3 cross-schema rule to reference shipped `validate_promotion_record`.**

old_string:
```
- Every concept ID used in a relationship's `from_entity` or `to_entity` MUST exist as a concept file with `canonical_status != "placeholder"` **at promotion time** (enforced by Promotion Validator in Phase 7).
```

new_string:
```
- Every concept ID used in a relationship's `from_entity` or `to_entity` MUST exist as a concept file with `canonical_status != "placeholder"` **at promotion time** (enforced by `validate_promotion_record` in `scripts/vitruvius/promotion_validator.py`, called by `run_promote`).
```

- [ ] **Step 6: Gap 1.4 — add `stringency_vector` to the placeholder worked example frontmatter.**

old_string:
```
---
id: concept-occupancy-classification
title: Occupancy Classification
page_type: concept
canonical_status: placeholder
concept_status: placeholder
last_canonicalized_utc: 2026-04-13T08:44:19.832285+00:00
---
```

new_string:
```
---
id: concept-occupancy-classification
title: Occupancy Classification
page_type: concept
canonical_status: placeholder
concept_status: placeholder
stringency_vector: qualitative
last_canonicalized_utc: 2026-04-13T08:44:19.832285+00:00
---
```

- [ ] **Step 7: Gap 1.4 — add `stringency_vector` to the enriched worked example frontmatter.**

old_string:
```
topic_tags:
  - building-code
  - occupancy
  - philippines
jurisdiction: philippines
language: en
regulatory_basis:
```

new_string:
```
topic_tags:
  - building-code
  - occupancy
  - philippines
jurisdiction: philippines
language: en
stringency_vector: qualitative
regulatory_basis:
```

- [ ] **Step 8: Gap 1.5 — remove the answered open question about placeholder vocabulary.**

old_string:
```
## 12. Open Questions
- Whether `placeholder` concepts should still be usable by the extractor as vocabulary. Current position: yes — vocabulary presence is the minimum bar for Phase 5 to match. The review layer catches any weak matches downstream.
- Whether `regulatory_basis` should support multi-source concepts with conflict resolution. Deferred until Phase 11 (dataset expansion).
```

new_string:
```
## 12. Open Questions
- Whether `regulatory_basis` should support multi-source concepts with conflict resolution. Deferred until Phase 11 (dataset expansion).
```

- [ ] **Step 9: Gap 1.6 — update changelog.**

old_string:
```
## Changelog
- **2026-04-14** — Initial schema published. Derived from current placeholder generator output + Phase 3C enrichment targets in the master roadmap.
```

new_string:
```
## Changelog
- **2026-04-14** — Initial schema published. Derived from current placeholder generator output + Phase 3C enrichment targets in the master roadmap.
- **2026-04-15** — Added `stringency_vector` optional field (Sprint W3.1/W3.2; `scripts/vitruvius/migrations/add_stringency_vector.py` + `linting.py`). Corrected IFC validator reference from `ifc_validator.py` to `ifc_registry.py`. Closed placeholder-vocabulary open question. Updated §9.3 to reference shipped `validate_promotion_record` instead of future Phase 7.
```

- [ ] **Step 10: Verify.**

```bash
cd /Users/philiplewis/vitruvius
grep -c "ifc_validator.py" .ai/06_specs/concept-schema.md || echo "OK: no ifc_validator.py"
grep -c "ifc_registry.py" .ai/06_specs/concept-schema.md
grep -c "stringency_vector" .ai/06_specs/concept-schema.md
grep -c "validate_promotion_record" .ai/06_specs/concept-schema.md
grep -n "placeholder concepts should still be usable" .ai/06_specs/concept-schema.md || echo "OK: answered open question removed"
```

- [ ] **Step 11: Commit.**

```bash
cd /Users/philiplewis/vitruvius
git add .ai/06_specs/concept-schema.md
git commit -m "docs(specs): concept-schema.md add stringency_vector, fix ifc_registry path"
```

---

### Task 2.2: Update `.ai/06_specs/relationship-schema.md`

**Files:**
- Modify: `/Users/philiplewis/vitruvius/.ai/06_specs/relationship-schema.md` (252 lines pre-edit)

**Context:** References `relationship_registry.yaml` as "to be created in Sprint A · A-2" — it exists. References Phase 7 Promotion Layer as future — it shipped. Missing `is_governing_standard`, `valid_from`/`valid_until`/`jurisdiction` temporal fields. 8 gaps.

- [ ] **Step 1: Verify file length and key strings.**

```bash
cd /Users/philiplewis/vitruvius
wc -l .ai/06_specs/relationship-schema.md
ls scripts/vitruvius/rules/relationship_registry.yaml
grep -c "is_governing_standard" scripts/vitruvius/graph/contract.py
grep -c "valid_from\|valid_until" scripts/vitruvius/promotion/temporal_edges.py || grep -c "valid_from\|valid_until" scripts/vitruvius/graph/contract.py
```
Expected: registry exists; `contract.py` has `is_governing_standard`; temporal fields present in one of the modules.

- [ ] **Step 2: Gap 2.1 — fix the "to be created" reference to relationship_registry.yaml.**

old_string:
```
Registry location (to be created in Sprint A · A-2): `scripts/vitruvius/rules/relationship_registry.yaml`.
```

new_string:
```
Registry location: `scripts/vitruvius/rules/relationship_registry.yaml`. Read at promotion time by `scripts/vitruvius/promotion_validator.py::load_registry()`.
```

- [ ] **Step 3: Gap 2.2 — update §1 to reflect shipped Promotion Layer and graph builder.**

old_string:
```
A Relationship is a promoted, evidence-bearing edge between two canonical entities (source↔concept or concept↔concept). It is the payload of the Phase 7 Promotion Layer and the unit of truth the Phase 8 graph is built from.
```

new_string:
```
A Relationship is a promoted, evidence-bearing edge between two canonical entities (source↔concept or concept↔concept). It is the payload of the Promotion Layer (`scripts/vitruvius/promotion/`) and the unit of truth the graph builder (`scripts/vitruvius/graph/builder.py`) consumes.
```

- [ ] **Step 4: Gap 2.6 — update §4.1 `verified` lifecycle bullet to drop "Phase 6B" label.**

old_string:
```
- **`verified`** — Reviewed by a human expert or by Tier-3 adjudication (Phase 6B).
```

new_string:
```
- **`verified`** — Reviewed by a human expert or by the tension-point adjudication path (`scripts/vitruvius/review/tension_analyzer.py`, flag `w_review_tension_reflection`).
```

- [ ] **Step 5: Gap 2.4 — add temporal edge fields to §4 Required Fields table.**

old_string:
```
| `last_promoted_utc` | ISO-8601 UTC | When the last promotion batch wrote this record. |
```

new_string:
```
| `last_promoted_utc` | ISO-8601 UTC | When the last promotion batch wrote this record. |
| `valid_from` | ISO-8601 date (YYYY-MM-DD) | *(Sprint GT.3.1, flag `g_temporal_edges`)* Start of the temporal validity interval for this edge. Required when `g_temporal_edges` is true. Open-ended intervals use `valid_until: null`. |
| `valid_until` | ISO-8601 date (YYYY-MM-DD) or null | *(Sprint GT.3.1, flag `g_temporal_edges`)* End of the temporal validity interval (exclusive). Null means the edge is still valid. Must be strictly after `valid_from`. |
| `jurisdiction` | string | *(Sprint GT.3.1, flag `g_temporal_edges`)* Jurisdictional scope of the edge (e.g., `national`, `manila`). Default: `national`. |
```

- [ ] **Step 6: Gap 2.4 continuation — add a §4.2 Temporal Edge Semantics subsection after §4.1.**

old_string:
```
- **`draft`** — Written by a manual curator but not yet processed by the Promotion Layer.
- **`promoted`** — Written or updated by `run_promote` after passing the validator.
- **`verified`** — Reviewed by a human expert or by the tension-point adjudication path (`scripts/vitruvius/review/tension_analyzer.py`, flag `w_review_tension_reflection`).
- **`superseded`** — Replaced by a newer edge. Retained for history. Not consumed by the graph builder.

## 5. Evidence Entry Shape
```

new_string:
```
- **`draft`** — Written by a manual curator but not yet processed by the Promotion Layer.
- **`promoted`** — Written or updated by `run_promote` after passing the validator.
- **`verified`** — Reviewed by a human expert or by the tension-point adjudication path (`scripts/vitruvius/review/tension_analyzer.py`, flag `w_review_tension_reflection`).
- **`superseded`** — Replaced by a newer edge. Retained for history. Not consumed by the graph builder.

### 4.2 Temporal Edge Semantics
When `g_temporal_edges` is enabled, `run_promote` stamps new edges with `valid_from` equal to the signing date of the governing source and `valid_until: null`. When a newer source supersedes the governing source, the predecessor edge is capped: `valid_until` is set to the effective date of the superseding source via `scripts/vitruvius/promotion/temporal_edges.py::cap_predecessor`. Temporal filtering is done by `filter_edges_valid_at(edges, query_date=...)` in the same module.

## 5. Evidence Entry Shape
```

- [ ] **Step 7: Gap 2.5 — replace the stale "Phase 6B" note in §5.2.**

old_string:
```
- `second_pass_*` — Populated if Phase 6B has run.
```

new_string:
```
- `second_pass_model` / `second_pass_decision` / `second_pass_confidence` — Reserved for a future second-pass adjudication step. Not written by any current pipeline stage; preserved for backward compatibility with files created before Sprint Q. The active second-pass mechanism for Sprint Q is the conformal gate (`w_review_conformal_routing`) and the Choquet aggregator (`w_review_choquet_aggregator`), whose outputs are persisted as operational signals in `005_Operational-Intelligence-Layer/` rather than in the relationship frontmatter.
```

- [ ] **Step 8: Gap 2.3 — add `is_governing_standard` to §5.2 Optional Evidence Fields.**

old_string:
```
### 5.2 Optional Evidence Fields
```

new_string:
```
### 5.2 Optional Evidence Fields
- `is_governing_standard` — Boolean or null. Set to `true` by `run_promote` when this evidence entry's edge won a stringency-resolver contest (`w_promotion_stringency_gate` flag). `false` means it lost and another edge for the same triplet is authoritative. `null` means the field predates Stream W3.4 and no contest has been run. Consumed by `scripts/vitruvius/graph/builder.py` when building `GraphEdge` objects.
```

- [ ] **Step 9: Gap 2.3 and 2.7 — update the evidence YAML example block and the worked example frontmatter. First add `is_governing_standard: null` to the evidence YAML example:**

old_string:
```
- source_id: law-national-building-code-of-the-philippines
  source_section_id: sec-701
  source_artifact: 002_Raw-Conversion-Layer/001-Laws/raw_markdown/PD-1096/PD 1096.md
  evidence_snippet: "Every building shall be classified in accordance with its use or occupancy…"
  snippet_start_line: 1423
  snippet_end_line: 1428
  review_decision: keep
  reviewer_model: gemma4:31b
  reviewer_confidence: 0.92
  reviewer_reason: "Evidence clearly supports governs relationship between occupancy and fire-resistive requirements."
  second_pass_model: null
  second_pass_decision: null
  second_pass_confidence: null
  extracted_at_utc: 2026-04-13T08:44:19Z
  reviewed_at_utc: 2026-04-13T09:01:02Z
```

new_string:
```
- source_id: law-national-building-code-of-the-philippines
  source_section_id: sec-701
  source_artifact: 002_Raw-Conversion-Layer/001-Laws/raw_markdown/PD-1096/PD 1096.md
  evidence_snippet: "Every building shall be classified in accordance with its use or occupancy…"
  snippet_start_line: 1423
  snippet_end_line: 1428
  review_decision: keep
  reviewer_model: gemma4:31b
  reviewer_confidence: 0.92
  reviewer_reason: "Evidence clearly supports governs relationship between occupancy and fire-resistive requirements."
  second_pass_model: null
  second_pass_decision: null
  second_pass_confidence: null
  is_governing_standard: null
  extracted_at_utc: 2026-04-13T08:44:19Z
  reviewed_at_utc: 2026-04-13T09:01:02Z
```

- [ ] **Step 10: Gap 2.7 — update the §9 worked example frontmatter to include the new temporal + is_governing_standard fields.**

old_string:
```
---
id: rel-occupancy-governs-fire-requirements
title: Occupancy Classification Governs Fire-Resistive Requirements
page_type: relationship
relationship_type: governs
from_entity: concept-occupancy-classification
to_entity: concept-fire-resistive-construction
trust_level: primary
canonical_status: promoted
confidence_score: 0.92
promotion_batch_id: 20260414T030000Z_a1b2c3d4
promotion_audit_log_ref: 006_System-Manifests/runs/20260414T030000Z_a1b2c3d4_promotion_audit.log
last_promoted_utc: 2026-04-14T03:00:00Z
evidence:
```

new_string:
```
---
id: rel-occupancy-governs-fire-requirements
title: Occupancy Classification Governs Fire-Resistive Requirements
page_type: relationship
relationship_type: governs
from_entity: concept-occupancy-classification
to_entity: concept-fire-resistive-construction
trust_level: primary
canonical_status: promoted
confidence_score: 0.92
promotion_batch_id: 20260414T030000Z_a1b2c3d4
promotion_audit_log_ref: 006_System-Manifests/runs/20260414T030000Z_a1b2c3d4_promotion_audit.log
last_promoted_utc: 2026-04-14T03:00:00Z
valid_from: null
valid_until: null
jurisdiction: null
evidence:
```

- [ ] **Step 11: Gap 2.7 continuation — add is_governing_standard to the worked-example evidence entry.**

old_string:
```
    reviewer_reason: "Evidence clearly supports a governs relationship."
    second_pass_model: null
    second_pass_decision: null
    second_pass_confidence: null
    extracted_at_utc: 2026-04-13T08:44:19Z
    reviewed_at_utc: 2026-04-13T09:01:02Z
---
```

new_string:
```
    reviewer_reason: "Evidence clearly supports a governs relationship."
    second_pass_model: null
    second_pass_decision: null
    second_pass_confidence: null
    is_governing_standard: null
    extracted_at_utc: 2026-04-13T08:44:19Z
    reviewed_at_utc: 2026-04-13T09:01:02Z
---
```

- [ ] **Step 12: Gap 2.8 — update the changelog.**

old_string:
```
## Changelog
- **2026-04-14** — Initial schema published. Aligned with master-roadmap §3.1 and §3.5. Derived from the existing draft relationship file plus Phase 7 Promotion Contract requirements.
```

new_string:
```
## Changelog
- **2026-04-14** — Initial schema published. Aligned with master-roadmap §3.1 and §3.5. Derived from the existing draft relationship file plus Phase 7 Promotion Contract requirements.
- **2026-04-15** — Registry now exists at `scripts/vitruvius/rules/relationship_registry.yaml` (Sprint A closed). Added `is_governing_standard` optional evidence field (Sprint W3.4). Added `valid_from`, `valid_until`, `jurisdiction` optional temporal fields (Sprint GT.3.1, flag `g_temporal_edges`). Clarified `second_pass_*` status. Updated phase-label references (Phase 6B → tension analyzer path, Phase 7 → shipped `run_promote`). Updated §1 framing.
```

- [ ] **Step 13: Verify.**

```bash
cd /Users/philiplewis/vitruvius
grep -c "is_governing_standard" .ai/06_specs/relationship-schema.md
grep -c "valid_from" .ai/06_specs/relationship-schema.md
grep -c "jurisdiction" .ai/06_specs/relationship-schema.md
grep -n "to be created in Sprint A" .ai/06_specs/relationship-schema.md || echo "OK: stale registry ref removed"
grep -n "Phase 6B" .ai/06_specs/relationship-schema.md || echo "OK: Phase 6B refs removed"
```

- [ ] **Step 14: Commit.**

```bash
cd /Users/philiplewis/vitruvius
git add .ai/06_specs/relationship-schema.md
git commit -m "docs(specs): relationship-schema.md adds is_governing_standard + temporal fields"
```

---

### Task 2.3: Update `.ai/06_specs/source-schema.md`

**Files:**
- Modify: `/Users/philiplewis/vitruvius/.ai/06_specs/source-schema.md` (170 lines pre-edit)

**Context:** Missing `document_type`, `issuing_body`, `issue_date` fields consumed by `priming/context_vector.py`. 5 gaps.

- [ ] **Step 1: Verify code truth.**

```bash
cd /Users/philiplewis/vitruvius
grep -n "document_type\|issuing_body\|issue_date" scripts/vitruvius/priming/context_vector.py | head -10
```
Expected: matches for all three field names.

- [ ] **Step 2: Gap 3.1 + 3.2 — add 4 new optional fields (`document_type`, `issuing_body`, `issue_date`, `identity_fingerprint`) after `effective_date`.**

old_string:
```
| `effective_date` | ISO-8601 date | When the source took legal effect. |
| `supersedes` | string[] | IDs of source documents this record replaces. |
```

new_string:
```
| `effective_date` | ISO-8601 date | When the source took legal effect. |
| `document_type` | string | *(Sprint R / Stream Y1.1)* Machine-readable document type for priming (e.g., `presidential_decree`, `implementing_rules`, `department_order`). Read by `scripts/vitruvius/priming/context_vector.py` to build the source-identity fingerprint. |
| `issuing_body` | string | *(Sprint R / Stream Y1.1)* Government body or agency that issued the document (e.g., `Office of the President`, `DPWH`). Read by `scripts/vitruvius/priming/context_vector.py`. |
| `issue_date` | ISO-8601 date | *(Sprint R / Stream Y1.1)* Date the document was signed or published (distinct from `effective_date`, which is when it took legal effect). Read by `scripts/vitruvius/priming/context_vector.py` to build the source-identity fingerprint. |
| `identity_fingerprint` | string | *(NEW — not yet persisted to source files)* SHA-256 hex digest (16-char prefix) of the tuple `(jurisdiction, document_type, issuing_body, issue_date, title)`. Computed at review time by `scripts/vitruvius/priming/context_vector.py::build_source_identity()` and injected into every LLM prompt as `SOURCE_IDENTITY[<fingerprint>]: ...`. Not currently written back to the source file — it is deterministic from the other fields and is recomputed on each call. May be persisted here for audit-log cross-referencing in a future sprint. |
| `supersedes` | string[] | IDs of source documents this record replaces. |
```

- [ ] **Step 3: Gap 3.3 — update the §11 `supersedes` open question to reflect shipped Promotion Layer.**

old_string:
```
- Whether `supersedes` / `superseded_by` links should generate automatic `supersedes` predicate edges. Deferred until Phase 7 Promotion Layer ships.
```

new_string:
```
- Whether `supersedes` / `superseded_by` links should generate automatic `supersedes` predicate edges. The Promotion Layer has shipped and the `supersedes` predicate is registered in `scripts/vitruvius/rules/relationship_registry.yaml`. Automatic edge generation from `superseded_by` frontmatter is not yet implemented in `run_promote` — deferred until a dedicated migration sprint.
```

- [ ] **Step 4: Gap 3.4 — add `document_type`, `issuing_body`, `issue_date` to the worked example frontmatter.**

old_string:
```
jurisdiction: philippines
effective_date: 1977-02-19
language: en
```

new_string:
```
jurisdiction: philippines
effective_date: 1977-02-19
document_type: presidential_decree
issuing_body: Office of the President
issue_date: 1977-02-19
language: en
```

- [ ] **Step 5: Gap 3.5 — update changelog.**

old_string:
```
## Changelog
- **2026-04-14** — Initial schema published. Derived from the existing hand-curated source file shape plus master-roadmap §3 contracts.
```

new_string:
```
## Changelog
- **2026-04-14** — Initial schema published. Derived from the existing hand-curated source file shape plus master-roadmap §3 contracts.
- **2026-04-15** — Added `document_type`, `issuing_body`, `issue_date` optional fields consumed by Sprint R / Stream Y1.1 source-identity priming (`scripts/vitruvius/priming/context_vector.py`). Added `identity_fingerprint` forward-compat field note. Updated §11 open question on `supersedes` to reflect Phase 7 shipped status.
```

- [ ] **Step 6: Verify and commit.**

```bash
cd /Users/philiplewis/vitruvius
grep -c "document_type" .ai/06_specs/source-schema.md
grep -c "identity_fingerprint" .ai/06_specs/source-schema.md
grep -n "Phase 7 Promotion Layer ships" .ai/06_specs/source-schema.md || echo "OK: deferred phrasing updated"
git add .ai/06_specs/source-schema.md
git commit -m "docs(specs): source-schema.md adds priming fields (document_type, issuing_body, issue_date)"
```

---

### Task 2.4: Update `.ai/06_specs/spatial-schema.md`

**Files:**
- Modify: `/Users/philiplewis/vitruvius/.ai/06_specs/spatial-schema.md` (122 lines pre-edit)

**Context:** Zero mention of the SHA-256 integrity footer shipped in AD-039. References "Stream N, future" when the spatial daemon exists. 6 gaps.

- [ ] **Step 1: Verify code truth — confirm the integrity footer contract.**

```bash
cd /Users/philiplewis/vitruvius
grep -n "INTEGRITY_FOOTER_PREFIX\|parse_contract\|IntegrityError" scripts/vitruvius/spatial/contract_reader.py | head -10
ls spatial-daemon/src/contract_writer.ts
```
Expected: `contract_reader.py` defines the integrity parsing; `contract_writer.ts` exists.

- [ ] **Step 2: Gap 4.2 — update §Purpose to reflect shipped spatial daemon.**

old_string:
```
JSON manifests that land in `001B_Spatial-Source-Layer/` carry geometric
metadata produced by an external spatial daemon (Stream N, future). Each
manifest describes one physical model: a set of tagged instances (doors,
walls, corridors) plus a set of spatial edges between them (clearance,
intersection, containment). The ingestion walker validates every file on
load and emits `SpatialCandidate` records downstream for constraint
evaluation.
```

new_string:
```
JSON manifests that land in `001B_Spatial-Source-Layer/` carry geometric
metadata produced by the Vitruvius spatial daemon (`spatial-daemon/src/`,
gated by feature flag `n_spatial_daemon_enabled`). Each manifest describes
one physical model: a set of tagged instances (doors, walls, corridors)
plus a set of spatial edges between them (clearance, intersection,
containment). The ingestion walker validates every file on load and emits
`SpatialCandidate` records downstream for constraint evaluation.
```

- [ ] **Step 3: Gap 4.5 — update the ## Sample section to reference `parse_contract()`.**

old_string:
```
A hand-authored fixture lives at
`scripts/tests/fixtures/spatial/sample_residential_01_spatial.json` and
exercises every required field plus optional bounding boxes. The
`sample_residential_01_expected_candidates.json` sibling is produced by
Task L.8 and locks the walker's output.
```

new_string:
````
A hand-authored fixture lives at
`scripts/tests/fixtures/spatial/sample_residential_01_spatial.json` and
exercises every required field plus optional bounding boxes. The
`sample_residential_01_expected_candidates.json` sibling is produced by
Task L.8 and locks the walker's output.

To read a spatial contract file in Python, use
`scripts/vitruvius/spatial/contract_reader.py::parse_contract(path)` rather
than calling `json.load()` directly. This verifies the SHA-256 integrity
footer (when present) and raises `IntegrityError` on corruption. Fixture
files that predate Sprint AUDIT-1 Task 5B have no footer and are still
parseable with the default `require_footer=False`.

## Integrity Footer

Every spatial contract file written by `spatial-daemon/src/contract_writer.ts` (Sprint AUDIT-1 Task 5B) carries an integrity footer appended after the JSON body:

```
<pretty-printed JSON body>\n
# sha256: <64 hex characters>\n
```

The footer is the SHA-256 hex digest of the exact UTF-8 bytes of the JSON body (including the trailing newline that follows the closing `}`). It is written by `computeContractBodySha256()` in `contract_writer.ts` using Node.js `crypto.createHash("sha256")`.

### Reading and verifying

Use `scripts/vitruvius/spatial/contract_reader.py::parse_contract(path)`. It:
1. Reads the raw file as UTF-8.
2. Splits on the last occurrence of `\n# sha256: ` to separate body from footer.
3. Recomputes `hashlib.sha256(body.encode("utf-8")).hexdigest()`.
4. Raises `IntegrityError` if the footer digest does not match.

The default is `require_footer=False` for backward compatibility with fixture files that predate Task 5B. Call sites that require a hard guarantee should pass `require_footer=True`.

### Legacy files

Files produced before Sprint AUDIT-1 Task 5B have no footer. They parse correctly with `require_footer=False` (the default). `ContractParseResult.has_footer` will be `False` for such files.

### Implementation constants

- Python: `contract_reader.INTEGRITY_FOOTER_PREFIX = "# sha256: "`
- TypeScript: `contract_writer.INTEGRITY_FOOTER_PREFIX = "# sha256: "`

Both constants are identical; any change to one requires a matching change to the other.

## Changelog

- **2026-04-14** — Initial schema published (Stream L.2). JSON schema frozen at v1.0.0. Authoritative validator: `scripts/vitruvius/spatial/schema.py`.
- **2026-04-15** — Added Integrity Footer section documenting SHA-256 footer contract written by `spatial-daemon/src/contract_writer.ts` and verified by `scripts/vitruvius/spatial/contract_reader.py` (Sprint AUDIT-1 Task 5B). Updated §Purpose: spatial daemon is shipped, no longer "future". Updated Sample section to reference `parse_contract()`.
````

- [ ] **Step 4: Verify and commit.**

```bash
cd /Users/philiplewis/vitruvius
grep -c "Integrity Footer" .ai/06_specs/spatial-schema.md
grep -c "parse_contract" .ai/06_specs/spatial-schema.md
grep -c "INTEGRITY_FOOTER_PREFIX" .ai/06_specs/spatial-schema.md
grep -n "Stream N, future" .ai/06_specs/spatial-schema.md || echo "OK: Stream N future reference removed"
git add .ai/06_specs/spatial-schema.md
git commit -m "docs(specs): spatial-schema.md adds Integrity Footer section (AD-039)"
```

---

## Phase 3: Historical Audits (5 files — banner + appendix updates)

All 5 audit files follow the same pattern: they are historical forensic snapshots from 2026-04-13, carry an outdated "HISTORICAL SNAPSHOT" banner, and have ≥1 actively misleading claim in the body. The fix per file is:
1. Replace the banner with a canonical updated banner (same banner across all 5 with minor per-file nuance).
2. Append a `## 2026-04-15 Post-Sprint Reality Check` appendix after the existing body content.

**Canonical banner template** (identical across all 5 files):

```markdown
> ⚠️ **HISTORICAL SNAPSHOT — SUPERSEDED 2026-04-15**
>
> This audit was written on 2026-04-13 against a pre-Sprint-A baseline.
> It is retained here as a frozen historical record of what the codebase
> looked like before 21 sprints shipped in a single session. Almost every
> "weakness" or "missing feature" flagged below has since been addressed.
>
> The 21 closed sprints (in execution order) are: Q · R · H · GT · HP ·
> HP.3-R · WIKI · GEOM · PHYS · Z · Meta-Docs · 1B-M1 · 1B-M2 ·
> RUST-PDF-1 · 1B-M3 · DISTILL-1 · RUST-MIG-1 · AUDIT-1 · PIPELINE-CLI ·
> PQ-1 · LSH-1. See the governing plan §1.1 for the full per-sprint ledger.
>
> Architecture decisions now span AD-001 through AD-042 (plus sub-decision
> AD-038a). The pointer "AD-001 through AD-029" in this file is outdated.
>
> **For the current state of the codebase, read these instead:**
> - `/.ai/03_plans/00-governing-implementation-plan.md` — authoritative sprint ledger (v3.0.0)
> - `/.ai/00_system/EXECUTION_LOOP.md` — v3.0 canonical operating contract
> - `/.ai/01_roadmap/master-roadmap.md` — roadmap v2.2.0
> - `/.ai/10_state/active_context.md` — current session state
> - `/.ai/10_state/decisions.md` — architecture decisions AD-001 through AD-042
> - `/.ai/10_state/known_issues.md` — open risks + closure timeline
> - `/.ai/01_roadmap/current-phase.md` — current sprint / phase
> - `/.ai/00_system/architecture.md` — current package layout
> - `/.ai/00_system/pipeline-overview.md` — current execution flow
> - `/.ai/00_system/naming-conventions.md` — naming rules
> - `/.ai/00_system/principles.md` — architectural principles
```

For each audit file, replace the existing 11-line banner block with this 27-line canonical banner, then append the per-file reality-check appendix.

---

### Task 3.1: Update `.ai/02_audits/codebase-roadmap-audit.md`

**Files:**
- Modify: `/Users/philiplewis/vitruvius/.ai/02_audits/codebase-roadmap-audit.md` (65 lines pre-edit)

- [ ] **Step 1: Replace the banner.**

old_string (the existing banner, including the trailing `---`):
```
> ⚠️ **HISTORICAL SNAPSHOT — SUPERSEDED 2026-04-15**
>
> This audit was written on 2026-04-13 against a pre-Sprint-A baseline. It is retained here as a frozen historical record of what the codebase looked like before Sprints A + B + C + D + Q + R + PHYS + H + GEOM + WIKI + GT + HP + Z + HP.3-R shipped. Almost every "weakness" or "missing feature" flagged below has since been addressed.
>
> **For the current state of the codebase, read these instead:**
> - `/.ai/10_state/active_context.md` — current session state
> - `/.ai/10_state/decisions.md` — architecture decisions AD-001 through AD-029
> - `/.ai/01_roadmap/current-phase.md` — current sprint / phase
> - `/.ai/00_system/architecture.md` — current package layout (including post-Sprint-D additions)
> - `/.ai/00_system/pipeline-overview.md` — current execution flow

---
```

new_string (paste the canonical banner template verbatim from above, followed by a blank line and `---`):
```
> ⚠️ **HISTORICAL SNAPSHOT — SUPERSEDED 2026-04-15**
>
> This audit was written on 2026-04-13 against a pre-Sprint-A baseline.
> It is retained here as a frozen historical record of what the codebase
> looked like before 21 sprints shipped in a single session. Almost every
> "weakness" or "missing feature" flagged below has since been addressed.
>
> The 21 closed sprints (in execution order) are: Q · R · H · GT · HP ·
> HP.3-R · WIKI · GEOM · PHYS · Z · Meta-Docs · 1B-M1 · 1B-M2 ·
> RUST-PDF-1 · 1B-M3 · DISTILL-1 · RUST-MIG-1 · AUDIT-1 · PIPELINE-CLI ·
> PQ-1 · LSH-1. See the governing plan §1.1 for the full per-sprint ledger.
>
> Architecture decisions now span AD-001 through AD-042 (plus sub-decision
> AD-038a). The pointer "AD-001 through AD-029" in this file is outdated.
>
> **For the current state of the codebase, read these instead:**
> - `/.ai/03_plans/00-governing-implementation-plan.md` — authoritative sprint ledger (v3.0.0)
> - `/.ai/00_system/EXECUTION_LOOP.md` — v3.0 canonical operating contract
> - `/.ai/01_roadmap/master-roadmap.md` — roadmap v2.2.0
> - `/.ai/10_state/active_context.md` — current session state
> - `/.ai/10_state/decisions.md` — architecture decisions AD-001 through AD-042
> - `/.ai/10_state/known_issues.md` — open risks + closure timeline
> - `/.ai/01_roadmap/current-phase.md` — current sprint / phase
> - `/.ai/00_system/architecture.md` — current package layout
> - `/.ai/00_system/pipeline-overview.md` — current execution flow
> - `/.ai/00_system/naming-conventions.md` — naming rules
> - `/.ai/00_system/principles.md` — architectural principles

---
```

- [ ] **Step 2: Append the per-file appendix at end of file.**

Read the current end of the file with `tail /Users/philiplewis/vitruvius/.ai/02_audits/codebase-roadmap-audit.md` to capture the exact last 2-3 lines, then use an Edit with the last paragraph as `old_string` and the same paragraph followed by a blank line + the appendix as `new_string`.

Example — if the file ends with:

```
**Audit result: PROJECT IS IN LATE INGESTION / EARLY EXTRACTION PHASE.**
*Claims of being "Starting Phase 7" are technically correct in terms of sequence, but the foundations (Phase 2, 3, 5) are much thinner than documented.*
```

Then the Edit is:

old_string:
```
**Audit result: PROJECT IS IN LATE INGESTION / EARLY EXTRACTION PHASE.**
*Claims of being "Starting Phase 7" are technically correct in terms of sequence, but the foundations (Phase 2, 3, 5) are much thinner than documented.*
```

new_string:
````
**Audit result: PROJECT IS IN LATE INGESTION / EARLY EXTRACTION PHASE.**
*Claims of being "Starting Phase 7" are technically correct in terms of sequence, but the foundations (Phase 2, 3, 5) are much thinner than documented.*

---

## 2026-04-15 Post-Sprint Reality Check

This appendix corrects four findings from the body above that are now factually wrong.
The body text is frozen as a historical record; this appendix is the delta.

### Promotion Layer — SHIPPED (Sprint A, 2026-04-14; Sprint Q, 2026-04-15)
Body §4 states "No code exists in `scripts/vitruvius/`." This is no longer true.
- `scripts/vitruvius/promotion/` subpackage ships `bayesian_fusion.py`,
  `stringency_resolver.py`, `temporal_edges.py`, `__init__.py`.
- The `promote` CLI command reads `latest_relationship_review_high_confidence.json`,
  runs a 17-rule validator, and writes records to
  `003_Canonical-Knowledge-Layer/shared/relationships/` with a full audit log.
- Sprint Q (AD-024) wired all 3 Stream G promotion modules into live paths.
  First 3 PD 1096 relationships were promoted on 2026-04-14.
- Risk RI-006 (Manual Promotion Gap) is formally CLOSED.

### Concept Enrichment — SUBSTANTIALLY SHIPPED (Phase 3C, AD-019, AD-020; 2026-04-14)
Body §3 states concepts.py "simply asserts that 'X is a concept'."
- 16/20 PD 1096 concepts now carry real definitions extracted via section-title
  anchors, alias mining, and compound-title matching — zero LLM calls.
- `scripts/vitruvius/concepts/` subpackage: `tfidf_matcher.py`, `pmi_alias_miner.py`,
  `fca_lattice.py`, `contrastive_adapter.py`.
- The 4 remaining concepts (`exit-width`, `parking-and-loading-spaces`, `setbacks`,
  `yards`) need a second corpus or manual curation — not an LLM issue.
- Risk RI-010 is 16/20 closed.

### Normalization Pipeline — SHIPPED (Sprint B, AD-007; 2026-04-14)
Body §4 states "No dedicated normalization logic beyond basic text cleaning."
- `scripts/vitruvius/normalization/` subpackage ships `engine.py` (NormalizationEngine),
  `rules_tier_a.py`, `rules_tier_b.py`, `rules_tier_c.py`, `ast_chunker.py`,
  `embedding_chunker.py`, `refine.py`.
- 8 Tier A/B rules run via the `refine` CLI stage, emitting `.refined.json` manifests.
  6 PD 1096 files refined with idempotency verified.
- Risk RI-007 (Normalization Fragmentation) is CLOSED.

### Hardcoded Ollama URL — FIXED (Sprint A, AD-003 sub-fix; 2026-04-14)
Body §6 states "Ollama URL is hardcoded to `127.0.0.1:11434`."
- The URL is now read from `config/vitruvius.yaml` via
  `scripts/vitruvius/config.py::get_ollama_url()`. The hardcoded value
  (`http://127.0.0.1:11434`) is retained only as a fallback default.
- Sprint B added bounded retries and graceful fallback on connection failure.
- Risk RI-003 (External Dependency — Ollama) is CLOSED.

### Current sprint count and AD ceiling
As of 2026-04-15: **21 sprints closed** in a single session (Q through LSH-1).
Architecture decisions span **AD-001 through AD-042** (plus sub-decision AD-038a).
See `/.ai/03_plans/00-governing-implementation-plan.md` §1.1 for the full ledger.
````

- [ ] **Step 3: Verify and commit.**

```bash
cd /Users/philiplewis/vitruvius
grep -c "21 closed sprints\|21 sprints closed" .ai/02_audits/codebase-roadmap-audit.md
grep -c "AD-001 through AD-042" .ai/02_audits/codebase-roadmap-audit.md
grep -c "Post-Sprint Reality Check" .ai/02_audits/codebase-roadmap-audit.md
grep -n "AD-001 through AD-029" .ai/02_audits/codebase-roadmap-audit.md || echo "OK: old AD ceiling removed"
git add .ai/02_audits/codebase-roadmap-audit.md
git commit -m "docs(audits): codebase-roadmap-audit.md banner + post-sprint appendix"
```

---

### Task 3.2: Update `.ai/02_audits/extraction-audit.md`

**Files:**
- Modify: `/Users/philiplewis/vitruvius/.ai/02_audits/extraction-audit.md` (766 lines pre-edit)

- [ ] **Step 1: Replace the banner** using the same old_string/new_string pair as Task 3.1 Step 1 (the banner block is identical across all 5 audit files).

- [ ] **Step 2: Append the appendix.** Find the end of the file (`tail -10 .ai/02_audits/extraction-audit.md`) and use Edit to append the appendix after the final paragraph.

Appendix text to paste after the existing body:

````markdown

---

## 2026-04-15 Post-Sprint Reality Check

### Machine context
The Windows-format "Audit Target" path in the body (`C:\Users\Philip Lewis\...`) is a
macOS audit run that was captured with a Windows-style path string. The canonical repo
path is `/Users/philiplewis/vitruvius/`. All subsequent development has been on macOS.

### Repository size: 19 files → 100+ modules
The 19-file table in §1 reflects the pre-Sprint-A baseline. As of 2026-04-15 the
`scripts/vitruvius/` package has grown to approximately 100+ Python modules across
18 subpackages, plus two pyo3 Rust crates and a TypeScript sibling subproject.
Major additions (subpackage level):

| Subpackage | Sprint that shipped it | Key modules |
|---|---|---|
| `normalization/` | Sprint B | `engine.py`, `rules_tier_{a,b,c}.py`, `ast_chunker.py`, `embedding_chunker.py`, `refine.py` |
| `parsers/` | Sprint C / 1B-M1/M2/M3 | `base_parser.py`, `docling_parser.py`, `rust_pdf_parser.py`, `orchestrator.py`, `factory.py`, `cli_handler.py`, `quality_gates.py`, `ocr_preprocessor.py`, `libreoffice_preprocessor.py` |
| `promotion/` | Sprint A / Sprint Q | `bayesian_fusion.py`, `stringency_resolver.py`, `temporal_edges.py` |
| `review/` | Sprint Q / Sprint R | `naive_bayes_filter.py`, `slm_router.py`, `choquet_aggregator.py`, `conformal_calibrator.py`, `tension_analyzer.py`, `reflection_parser.py`, `cot_audit.py`, `stateful_registry.py`, `rocksdb_stateful_registry.py` |
| `wiki/` | Sprint WIKI | `docling_parser.py`, `kuzu_store.py`, `delta_tracker.py`, `synthesis_loop.py`, `ego_linter.py`, `llm_client.py`, `ollama_client.py` |
| `compound/` | Sprint Z | `adversarial.py`, `dspy_compiler.py`, `logic_schema.py`, `dependency_tracker.py`, `differential_propagator.py`, `wasm_kernel.py` |
| `graph/` | Phase 8 / Sprint GT/HP/PHYS/HP.3-R | 24 modules including `builder.py`, `graphsage.py`, `graphsage_pq.py`, `pq_codebook.py`, `physics.py`, `event_store.py`, `rocksdb_event_store.py`, `wasserstein_merge.py` |
| `concepts/` | Sprint D / Phase 3C | `tfidf_matcher.py`, `pmi_alias_miner.py`, `fca_lattice.py`, `contrastive_adapter.py` |
| `relationships/` | Sprint LSH-1 | `lsh_index.py`, `lsh_dedup.py`, `minhash.py` |
| `spatial/` | Sprint H / Sprint GT | `schema.py`, `concept_mapper.py`, `constraint_solver.py`, `cli.py` |
| `query/` | Phase 9 / Sprint D | `engine.py`, `graphrag_router.py`, `ontology_prompt.py`, `mcmc_ranker.py`, `pipeline_hmm.py` |
| `geometric/` | Sprint GEOM | `inequality_compiler.py`, `envelope_2d.py`, `envelope_3d.py`, `pareto_optimizer.py` |
| `extraction/` | Sprint D | `crf_trainer.py`, `crf_extractor.py`, `kg_link_predictor.py` |
| `priming/` | Sprint R | contextual priming modules |
| `bench/` | Sprint Q / Sprint HP.3-R | bench harnesses |
| `merkle/` | Sprint HP | `directory_hash.py` |
| `engine_rs/` (Rust) | Sprint GT | pyo3 bridge — `SpatialPoint`, `LinearOctree`, AABB-intersects C-ABI |
| `datalog_rs/` (Rust) | Sprint Z | hand-rolled Datalog evaluator |

Single-file additions: `merkle_fs.py` (HP.1), `kv_migrate.py` (HP.3-R), `features.py`,
`config.py`, `registry_rotation.py`, `promotion_validator.py`, `concept_enrichment.py`,
`concept_definitions.py`, `concept_aliases.py`, `pre_review_filter.py`,
`ollama_review_second_pass.py`, `review_routing.py`, `canonical_diff.py`.

TypeScript sibling: `spatial-daemon/` (GJK, AABB, filesystem contract writer, 20/20 vitest tests).

### Layer 3→4 and Layer 4→5 — both SHIPPED
The closing conclusion in §17 ("Layer 3→4: NOT IMPLEMENTED / Layer 4→5: NOT IMPLEMENTED")
and the "Key Gaps" list are now wrong for every item.

- **Layer 3→4 (derived content + promotion):** Sprint A shipped the `promote` CLI command
  (17-rule validator, audit log). Sprint Q (AD-024) wired 3 Stream G promotion modules.
  Sprint WIKI (AD-030) shipped autonomous LLM knowledge synthesis. `promotion/` subpackage
  is fully operational. First 3 PD 1096 relationships promoted 2026-04-14.
- **Layer 4→5 (chunking, embeddings, graph):** `normalization/ast_chunker.py` (AST-based
  semantic chunking) and `normalization/embedding_chunker.py` shipped in Sprint B.
  `graph/graphsage.py` (GraphSAGE embeddings, Sprint HP) and `graph/graphsage_pq.py`
  (32× product-quantization compression, Sprint PQ-1 AD-041) ship the embedding layer.
  `wiki/kuzu_store.py` provides vector+graph hybrid storage. `graph/` contains 24 modules
  covering the full graph stack from construction to physics simulation.
- **Relationship extraction beyond regex:** `extraction/crf_trainer.py` and
  `extraction/crf_extractor.py` (Sprint D Stream E CRF-based extraction) plus the
  pre-review NaiveBayes filter (`review/naive_bayes_filter.py`, Sprint Q AD-024) reduce
  the effective rejection rate from 82% to approximately 10% on PD 1096.
- **OCR parallelization:** `parsers/orchestrator.py::process_batch()` has the API
  contract in place for `ProcessPoolExecutor` (flag `p1b_process_pool_orchestration`
  reserved, Sprint 1B-M2 AD-032). Full parallel activation is one flag-flip away once
  validated. Additionally, `parsers/rust_pdf_parser.py` (lopdf-backed, AD-034) runs at
  0.05s wall / 13.7 MB RSS (625× faster than docling), changing the batch-convert
  performance profile dramatically.

### Current sprint count and AD ceiling
As of 2026-04-15: **21 sprints closed**. Architecture decisions span **AD-001 through
AD-042** (plus sub-decision AD-038a). CLI command count has grown well beyond the 18
commands enumerated in §2 of this audit.
````

- [ ] **Step 3: Verify and commit.**

```bash
cd /Users/philiplewis/vitruvius
grep -c "Post-Sprint Reality Check" .ai/02_audits/extraction-audit.md
grep -c "100+ Python modules" .ai/02_audits/extraction-audit.md
git add .ai/02_audits/extraction-audit.md
git commit -m "docs(audits): extraction-audit.md banner + 100+ module appendix"
```

---

### Task 3.3: Update `.ai/02_audits/ingestion-audit.md`

**Files:**
- Modify: `/Users/philiplewis/vitruvius/.ai/02_audits/ingestion-audit.md` (394 lines pre-edit)

- [ ] **Step 1: Replace the banner** using the same old_string/new_string pair as Task 3.1 Step 1.

- [ ] **Step 2: Append the per-file appendix.** Find the end of the file (`tail -10 .ai/02_audits/ingestion-audit.md`) and use Edit to append this appendix:

````markdown

---

## 2026-04-15 Post-Sprint Reality Check

### Machine context
The "Audit Target" path in the body header uses Windows-format paths. The canonical
repo location is `/Users/philiplewis/vitruvius/` on macOS.

### File hashing — SHIPPED (Sprint C, AD-022; 2026-04-14)
Body §5 notes "No file hashes computed" and §12 marks file hashing as MISSING.
Sprint C Phase 1B Foundation (Task 0, commit `1386b32`) closed this gap completely:
- `scripts/vitruvius/scanner.py` line 17: `def _sha256_of_file(path: Path) -> str:`
  — streaming SHA-256 via `hashlib.sha256()`.
- `FileEntry` dataclass gained a `sha256: str` field.
- `latest_raw_file_registry.csv` gained a `sha256` column.
- 6-test regression suite in `scripts/tests/test_scanner_sha256.py`.
Risk RI-009 (No File Hashing in Ingestion) is **CLOSED**.

### Registry rotation — SHIPPED (Sprint C, AD-023; 2026-04-14)
Body §14 marks registry growth as MEDIUM risk with "no rotation."
Sprint C quality pass shipped `rotate-registries` CLI command:
- Deterministic retention policy (default keep=30 per timestamped registry family).
- `latest_*.csv` pointers and non-timestamped static registries are never touched.
- Supports `--dry-run` and `--keep N`. Pure `plan_rotation()` / `apply_rotation()` split.
Risk RI-008 (Registry Growth Without Rotation) is **CLOSED**.

### Parser modernization — SHIPPED (Sprints 1B-M1/M2/M3, AD-031/032/034; 2026-04-15)
The 25-file repository map in §1 is missing the entire `parsers/` subpackage (14 files),
which is the primary Phase 1B ingestion modernization:
- `parsers/base_parser.py` — `BaseParser` ABC with `parse(path) → ParseResult`
- `parsers/docling_parser.py` — Docling-backed parser (flag `p1b_docling_parser`)
- `parsers/rust_pdf_parser.py` — lopdf-backed Rust PDF parser via pyo3 (flag `p1b_rust_pdf_parser`); 13.7 MB peak RSS / 0.05s wall = 48× smaller, 625× faster than docling. Quality gate: LCS 0.9925 vs pypdf on real corpus.
- `parsers/ocr_preprocessor.py` — `OCRPreprocessor` (flag `p1b_ocr_preprocessor`)
- `parsers/libreoffice_preprocessor.py` — `LibreOfficePreprocessor` (flag `p1b_libreoffice_preprocessor`)
- `parsers/orchestrator.py` — `ParserOrchestrator` with `process_batch()` scaffolded for `ProcessPoolExecutor` (flag `p1b_process_pool_orchestration` reserved)
- `parsers/factory.py` — `build_default_orchestrator()` dispatches all 5 `p1b_*` flags
- `parsers/cli_handler.py` — `run_convert_parsers_one()` handler for `convert-parsers-one` subcommand (Sprint PIPELINE-CLI, AD-040)
- `parsers/quality_gates.py`, `parsers/shannon_classifier.py`, `parsers/document_taxonomy.py`, `parsers/parametric_ner.py`, `parsers/vision_ocr.py`, `parsers/table_graph_extractor.py`

### OCR parallelization — scaffolded, not yet active
Body §14 rates sequential OCR as HIGH severity with no parallelization.
`parsers/orchestrator.py::process_batch()` has `max_workers` reserved for
`ProcessPoolExecutor` upgrade and the `p1b_process_pool_orchestration` flag is
registered in the feature registry (defaults false, Sprint 1B-M2 AD-032). The
architecture is ready; activation is one flag-flip + validation away.

Additionally, the Rust PDF parser (`p1b_rust_pdf_parser`) handles text-based PDFs
at 625× the speed of the OpenDataLoader baseline, which dramatically reduces the
effective batch-convert wall time and shrinks the OCR queue on modern Philippine
building-code corpora (which are mostly text-based PDFs).

### Current sprint count and AD ceiling
As of 2026-04-15: **21 sprints closed**. Architecture decisions span **AD-001 through
AD-042** (plus sub-decision AD-038a).
````

- [ ] **Step 3: Verify and commit.**

```bash
cd /Users/philiplewis/vitruvius
grep -c "Post-Sprint Reality Check" .ai/02_audits/ingestion-audit.md
grep -c "_sha256_of_file" .ai/02_audits/ingestion-audit.md
git add .ai/02_audits/ingestion-audit.md
git commit -m "docs(audits): ingestion-audit.md banner + parser+hashing+rotation appendix"
```

---

### Task 3.4: Update `.ai/02_audits/normalization-audit.md`

**Files:**
- Modify: `/Users/philiplewis/vitruvius/.ai/02_audits/normalization-audit.md` (110 lines pre-edit)

- [ ] **Step 1: Replace the banner** using the same old_string/new_string pair as Task 3.1 Step 1.

- [ ] **Step 2: Append the per-file appendix.** Find the end of the file and use Edit to append:

````markdown

---

## 2026-04-15 Post-Sprint Reality Check

### The normalization layer now exists — SHIPPED (Sprint B, AD-007; 2026-04-14)
The central finding of this audit — "There is no formal normalization pipeline" — was the
precise motivation for Sprint B. Sprint B built exactly what was described as missing.

**`scripts/vitruvius/normalization/` subpackage** (6 files):
- `engine.py` — `NormalizationEngine` with phase-locked execution and scope routing.
  Accepts a `RefinementContext` (scope: `document`, `section`, or `token`), runs the
  applicable tier stack in order, and returns a `RefinedDocument`.
- `rules_tier_a.py` — Tier A structural rules: whitespace collapsing, line merging,
  JSON-fence stripping, page-number artifact removal, header/footer noise suppression.
- `rules_tier_b.py` — Tier B content rules: section-header normalization, bullet
  normalisation, trailing-punctuation cleanup.
- `rules_tier_c.py` — Tier C semantic rules: token normalization, abbreviation expansion
  (Philippine legal register).
- `ast_chunker.py` — AST-based semantic chunking for Layer 4/5 retrieval.
- `embedding_chunker.py` — Embedding-aware chunking for retrieval infrastructure.
- `refine.py` — CLI stage handler; emits `.refined.json` manifests per processed file.

**Transformation inventory corrections** (the "NOT IMPLEMENTED" rows in §Transformation
Inventory are now wrong):
- Header Normalization: **SHIPPED** — Tier B header-normalization rule.
- Noise Removal (Page Numbers, Headers/Footers): **SHIPPED** — Tier A artifact-removal rules.
- Token Normalization: **SHIPPED** — Tier C semantic rules.

**Import fragmentation corrected:**
Risk RI-007 flagged the 3-way duplication of `normalize_text` across `utils.py`,
`relationships_sections.py`, and `canonicalize.py`. Sprint B made the `NormalizationEngine`
the canonical authority. The inline duplicates are retained for backward compatibility but
new code routes through the engine.

**Pipeline position corrected:**
The audit noted normalization was "90% inline" with no standalone stage. The `refine` CLI
command now runs as an explicit pipeline step (`run-with-review` composite chains it after
`convert` and before `review`).

6 PD 1096 files were refined in the first Sprint B pass with idempotency verified.
Risk RI-007 (Normalization Fragmentation) is **CLOSED** for MVP scope. Tier C semantic
rules, full semantic chunking, and destructive-guard rollback are tracked as post-Sprint-B
follow-ups and are substantially shipped via the subpackage files above.

### Current sprint count and AD ceiling
As of 2026-04-15: **21 sprints closed**. Architecture decisions span **AD-001 through
AD-042** (plus sub-decision AD-038a).
````

- [ ] **Step 3: Verify and commit.**

```bash
cd /Users/philiplewis/vitruvius
grep -c "Post-Sprint Reality Check" .ai/02_audits/normalization-audit.md
grep -c "NormalizationEngine" .ai/02_audits/normalization-audit.md
git add .ai/02_audits/normalization-audit.md
git commit -m "docs(audits): normalization-audit.md banner + NormalizationEngine appendix"
```

---

### Task 3.5: Update `.ai/02_audits/review-layer-audit.md`

**Files:**
- Modify: `/Users/philiplewis/vitruvius/.ai/02_audits/review-layer-audit.md` (593 lines pre-edit)

- [ ] **Step 1: Replace the banner** using the same old_string/new_string pair as Task 3.1 Step 1.

- [ ] **Step 2: Append the per-file appendix.** Find the end of the file and use Edit to append:

````markdown

---

## 2026-04-15 Post-Sprint Reality Check

### Ollama URL — no longer hardcoded (Sprint A, AD-003 sub-fix; 2026-04-14)
Body §5 documents `OLLAMA_URL = "http://127.0.0.1:11434/api/generate"` as a hardcoded
module-level constant and §9 lists "Configuration file support" as NOT IMPLEMENTED.
Sprint A moved the URL to `config/vitruvius.yaml`. `scripts/vitruvius/config.py` line
17 (`def get_ollama_url()`) reads from the config with `http://127.0.0.1:11434` as a
fallback default. `scripts/vitruvius/ollama_review.py` imports `get_ollama_url` and
resolves it at startup. `OLLAMA_URL` as a module-level constant no longer exists.
Risk RI-003 (External Dependency — Ollama) is **CLOSED**.

### Default model note
The argparse default in the CLI registration (`--model default="gemma4:31b"`) is still
present in `scripts/pipeline_cli.py` line 128. However, at runtime `ollama_review.py`
line 21 resolves `DEFAULT_MODEL = get_ollama_default_model()` from `config/vitruvius.yaml`.
On the 8 GB M2 target machine, `gemma4:e4b` is the operator-intended default (used in all
bench scripts). `gemma4:31b` is retained as a config-file default for larger machines.

### Review layer now integrated into the pipeline (Sprint B, AD-008; 2026-04-14)
Body §2 states the review layer "is NOT automatically invoked in the pipeline."
Sprint B Phase 6A shipped the `run-with-review` composite command that chains:
`run → convert → refine → review-relationships-ollama`.
The default `run` command remains minimal (no Ollama call) so CI does not invoke
the LLM accidentally. Risk RI-012 (Review Layer Not in Default Pipeline) is **CLOSED**.

### Second-pass review — SHIPPED (Sprint B, Phase 6B; 2026-04-14)
Body §12 states second-pass review is NOT IMPLEMENTED.
`scripts/vitruvius/ollama_review_second_pass.py` shipped in Sprint B Phase 6B.
`pipeline_cli.py` registers `review-relationships-second-pass` with a Tier-2 model
argument (default `qwen3:30b`). Only candidates where Tier-1 returned `review_further`
with low confidence reach Tier-2.

### Confidence threshold enforcement — SHIPPED (Sprint Q, AD-024; 2026-04-15)
Body §9 lists "No confidence threshold enforcement" as NOT IMPLEMENTED.
- `scripts/vitruvius/review/conformal_calibrator.py` (Sprint Q W3) — conformal
  prediction calibrator that converts raw model confidence to calibrated p-values.
- `scripts/vitruvius/review/choquet_aggregator.py` (Sprint Q W3) — Choquet integral
  fusion of multi-criteria review scores (semantic, structural, co-occurrence).
Both are wired under feature flags (`w_conformal_calibrator`, `w_choquet_fusion`).

### Pre-review NaiveBayes filter and model routing — SHIPPED (Sprint Q, AD-024; 2026-04-15)
Body §9 lists "No model fallback" and "Sequential processing: HIGH" as NOT IMPLEMENTED.
- `scripts/vitruvius/review/naive_bayes_filter.py` — pre-review filter (flag `w_nb_prefilter`,
  rule R7 `endpoint_not_in_evidence`). Cuts LLM-bound candidates from ~9 to ~2 on PD 1096
  (78% reduction). The 100-minute sequential worst case drops to ~20 minutes on current corpus.
- `scripts/vitruvius/review/slm_router.py` — SLM-based domain routing with
  `complex → gemma4:31b` / `simple → <light model>` dispatch.
- `scripts/vitruvius/review/domain_classifier.py` — domain-aware routing.
All wired under `w_slm_router` / `w_domain_routing_moe` flags.

### Progress resume — SHIPPED (Sprint R Y4, AD-025; Sprint HP.3-R, AD-029; 2026-04-15)
Body §9 lists "No progress resume capability: PARTIAL" (partial saves but no resume).
- `scripts/vitruvius/review/stateful_registry.py` (Sprint R Y4) — SQLite-backed
  stateful review registry that persists all verdicts, supports vacuum/purge CLI,
  and provides Phase 6A Resume integration test (gap closed at root).
- `scripts/vitruvius/review/rocksdb_stateful_registry.py` (Sprint HP.3-R, AD-029) —
  RocksDB-backed registry (24.3× faster than SQLite at n=10000). Default-true via
  `hp_rocksdb_verdict_cache` flag. Factory `make_stateful_registry()` dispatches on flag.

### Retry logic — SHIPPED (Sprint B, Phase 6A; 2026-04-14)
Body §9 lists "No retry logic for individual candidates" as NOT IMPLEMENTED.
Sprint B Phase 6A added bounded retries with wall-clock cap and graceful fallback
to `review_further` on consecutive failure. Risk RI-003 sub-item resolved.

### What is NOT implemented list (body §14) — fully superseded
All 7 items in the unchecked list are now shipped. For completeness:
- [x] Automatic pipeline integration — `run-with-review` (Sprint B)
- [x] Second-pass review — `ollama_review_second_pass.py` (Sprint B Phase 6B)
- [x] Confidence threshold enforcement — `conformal_calibrator.py` + `choquet_aggregator.py` (Sprint Q)
- [x] Batch parallelization / LLM reduction — NaiveBayes pre-filter 78% reduction (Sprint Q)
- [x] Retry logic — bounded retries + wall-clock cap (Sprint B)
- [x] Model fallback / routing — `slm_router.py` + `domain_classifier.py` (Sprint Q / Sprint R)
- [x] Progress resume — `stateful_registry.py` (Sprint R) + RocksDB variant (Sprint HP.3-R)
- [x] Configuration file support — `config/vitruvius.yaml` (Sprint A)

### Current sprint count and AD ceiling
As of 2026-04-15: **21 sprints closed**. Architecture decisions span **AD-001 through
AD-042** (plus sub-decision AD-038a).
````

- [ ] **Step 3: Verify and commit.**

```bash
cd /Users/philiplewis/vitruvius
grep -c "Post-Sprint Reality Check" .ai/02_audits/review-layer-audit.md
grep -c "conformal_calibrator" .ai/02_audits/review-layer-audit.md
grep -c "stateful_registry" .ai/02_audits/review-layer-audit.md
git add .ai/02_audits/review-layer-audit.md
git commit -m "docs(audits): review-layer-audit.md banner + Sprint Q/R reality appendix"
```

---

## Phase 4: Cross-file Verification

This phase runs grep-based consistency checks across all 13 updated files. Any hit on the "stale patterns" greps must be resolved before the plan is considered complete.

### Task 4.1: Verify no stale sprint counts remain

- [ ] **Step 1: Grep for stale sprint-count phrases.**

```bash
cd /Users/philiplewis/vitruvius
grep -rn "ten sprints\|the 10 sprints\|ten closed sprints\|Sprints A + B + C + D" .ai/00_system/ .ai/06_specs/ .ai/02_audits/ || echo "OK: no stale sprint counts"
```
Expected: `OK: no stale sprint counts`.

- [ ] **Step 2: Confirm 21-sprint references are present where expected.**

```bash
grep -rln "21 sprints\|21 closed sprints" .ai/00_system/ .ai/02_audits/ | sort
```
Expected: `architecture.md`, `pipeline-overview.md`, and all 5 audit files.

### Task 4.2: Verify no stale AD ceilings remain

- [ ] **Step 1: Grep for stale AD-029 or AD-024..AD-029 pointers.**

```bash
cd /Users/philiplewis/vitruvius
grep -rn "AD-024 through AD-029\|AD-001 through AD-029" .ai/00_system/ .ai/06_specs/ .ai/02_audits/ || echo "OK: no stale AD ceilings"
```
Expected: `OK: no stale AD ceilings`.

- [ ] **Step 2: Confirm AD-042 references are present where expected.**

```bash
grep -rln "AD-042" .ai/00_system/ .ai/02_audits/ | sort
```
Expected: `architecture.md`, `principles.md`, and all 5 audit files.

### Task 4.3: Verify principle P1–P10 numbering

- [ ] **Step 1: Confirm principles.md has all 10 principles with correct numbering.**

```bash
cd /Users/philiplewis/vitruvius
grep -E "^### [0-9]+\." .ai/00_system/principles.md
```
Expected: 10 headings, numbered 1 through 10 in order.

- [ ] **Step 2: Verify no file refers to "Principle 9 — Local-First" (it's now P8).**

```bash
grep -rn "Principle 9.*Local\|P9 Local\|Principle.*9.*Local" .ai/00_system/ .ai/06_specs/ .ai/02_audits/ || echo "OK: no stale P9 Local-First references"
```
Expected: `OK: no stale P9 Local-First references`.

- [ ] **Step 3: Verify EXECUTION_LOOP.md still references P8 Local-First.**

```bash
grep -n "P8.*local\|P8 local\|P8 — Local" .ai/00_system/EXECUTION_LOOP.md
```
Expected: at least one hit.

### Task 4.4: Verify no Phase 7 / Phase 6B / "to be created" future references in schema specs

- [ ] **Step 1: Grep for stale future-tense references.**

```bash
cd /Users/philiplewis/vitruvius
grep -rn "Phase 7 Promotion Layer ships\|Phase 7 Promotion\|Phase 6B\|to be created in Sprint A · A-2\|ifc_validator.py" .ai/06_specs/ || echo "OK: no stale future refs in specs"
```
Expected: `OK: no stale future refs in specs`.

### Task 4.5: Verify test baseline and final commit inventory

- [ ] **Step 1: Run the test suite.**

```bash
cd /Users/philiplewis/vitruvius
pytest scripts/tests -q 2>&1 | tail -5
```
Expected: `1528 passed, 1 skipped` (no change from Phase 0 baseline — this plan is docs-only).

- [ ] **Step 2: Confirm exactly 13 files changed since the starting commit.**

```bash
cd /Users/philiplewis/vitruvius
git diff --name-only <STARTING_SHA>..HEAD
```
Expected (order doesn't matter):
```
.ai/00_system/architecture.md
.ai/00_system/naming-conventions.md
.ai/00_system/pipeline-overview.md
.ai/00_system/principles.md
.ai/02_audits/codebase-roadmap-audit.md
.ai/02_audits/extraction-audit.md
.ai/02_audits/ingestion-audit.md
.ai/02_audits/normalization-audit.md
.ai/02_audits/review-layer-audit.md
.ai/03_plans/2026-04-15-documentation-refresh-plan.md
.ai/06_specs/concept-schema.md
.ai/06_specs/relationship-schema.md
.ai/06_specs/source-schema.md
.ai/06_specs/spatial-schema.md
```
(14 files total including this plan file itself.)

If any additional files appear, investigate — the plan should only touch documentation.

- [ ] **Step 3: Append a closure entry to the governing plan's Task 8 / Task 9 retrospective (if the governing plan tracks meta-sprints).**

This is optional and only applies if the user/Philip confirms they want this documentation refresh recorded as a meta-sprint closure in the governing plan. If yes, add a short "Meta-Docs-2" sprint entry to `.ai/03_plans/00-governing-implementation-plan.md` pointing to this plan file and the 14 commits. If no, skip this step.

---

## Post-Plan Notes (read before executing)

1. **No new ADs are created by this plan.** This is intentional — the plan only documents existing state; it does not introduce new architectural decisions. Per I1 (AD append-only), any new invariant would require a new AD, but nothing here is new — `principles.md` is being updated to match EXECUTION_LOOP.md v3.0 which already codifies these invariants.

2. **The 4 live-by-default flags.** Confirm in each task before editing the architecture/principles/pipeline-overview tables: `hp_rocksdb_event_store`, `hp_rocksdb_verdict_cache`, `rust_mig_spatial_kernels`, `rust_mig_stats_kernels`. Read `config/vitruvius.yaml` to verify. If the list has changed since this plan was written, update the task replacement text.

3. **Edit ambiguity risk.** A few of the old_string blocks may occur more than once in their files. Before running each Edit, use a short local grep to confirm uniqueness: `grep -c "<first line of old_string>" <file>`. If the count > 1, expand the old_string with more context lines until the match is unique.

4. **Memory hint (from session briefing).** `smart_outline` cannot parse markdown. Use `wc -l` and `grep -n` for line-number discovery instead.

5. **If you hit Read dedupe.** The harness may refuse to re-read a file already registered as read (returning "Wasted call"). Fall back to `Bash cat <file>` — that is explicitly authorized for this plan.

6. **Commit cadence.** One commit per file (per task) gives a clean history. Avoid bundling multiple files into a single commit so that reverts stay surgical.

7. **Open questions escalated to planner** (from the gap reports):
   - **OQ-S1 (system):** Principle renumbering may break external references; the pre-edit grep in Task 1.4 Step 1 is the gate.
   - **OQ-S2 (system):** Whether to add a P11 (spatial integrity) principle is deferred — current plan treats AD-039 as a documented contract, not a numbered principle.
   - **OQ-SP1 (specs):** `last_promoted_utc` format discrepancy — real files use compact `20260414T234203Z`; spec shows extended ISO. Out of scope for this plan; log as RI if it matters.
   - **OQ-SP2 (specs):** Spatial predicate vocabulary vs. semantic predicate vocabulary — explicitly keep them separate, not merged. Add a short disclaimer to each file in a follow-up pass if necessary.
   - **OQ-A1 (audits):** Should the audit bodies keep their historical Windows paths? Plan says yes (frozen forensic record); appendix notes the machine context.
   - **OQ-A2 (audits):** AD-030 may be missing from `decisions.md`. Verify during Phase 0; if missing, do NOT fabricate — raise it as a question.
