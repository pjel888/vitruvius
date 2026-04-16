# Vitruvius — Pipeline Overview

## Purpose
This document provides a code-grounded overview of the Vitruvius execution pipeline. It traces the data lifecycle from raw document ingestion through transformation, canonicalization, and relationship extraction to final review and output.

## Scope
The scope of this document is limited to the executable stages defined in `scripts/pipeline_cli.py` and implemented within the `scripts/vitruvius/` package.

## Pipeline Summary
The Vitruvius pipeline is a **sequential, file-driven workflow** that uses the filesystem as its primary state-tracking mechanism. It progresses through discovery, conversion, normalization into a canonical knowledge layer, and automated extraction of legal relationships.

## Entry Points
- **Main Entry Point:** `scripts/pipeline_cli.py`
  - This script acts as the primary orchestrator, dispatching commands to specific modules.
- **Key Commands:**
  - `run`: Executes the default baseline (Scan → Status → Lint).
  - `convert`: Batch processes new or changed files into Markdown/JSON.
  - `canonicalize-one`: Refines a specific converted file into the Canonical Knowledge Layer.
  - `extract-relationships-one`: Runs pattern-based extraction on a canonical source.
  - `review-relationships-ollama`: Performs LLM-based verification of extracted relationships.

## End-to-End Execution Flow
1.  **Ingestion (`run_scan`)**: Crawls `001_Raw-Source-Layer` to build a file registry.
2.  **State Analysis (`run_status`)**: Compares current scan against previous to find new/changed files.
3.  **Validation (`run_lint`)**: Checks for naming collisions and unsupported formats.
4.  **Transformation (`run_convert`)**:
    - Converts PDFs, Office, and Spreadsheets to Markdown.
    - Routes scanned PDFs to OCR if needed.
5.  **Reconciliation (`run_reconcile`)**: Identifies and flags stale or orphaned artifacts.
6.  **Canonicalization (`run_canonicalize_one`)**: Maps raw markdown to a strict ID and frontmatter schema in `003`.
7.  **Extraction (`run_extract_relationships_one`)**: Identifies legal links using regex patterns.
8.  **Review (`run_review_relationships_ollama`)**: Validates extractions using a local LLM.

## Stage Breakdown

### 1. Ingestion Stage
- **Module:** `scanner.py`
- **Action:** `rglob("*")` on `001_Raw-Source-Layer`.
- **Artifact:** `latest_raw_file_registry.csv` in `006/registries`.

### 2. Status & Lint Stage
- **Modules:** `status.py`, `linting.py`.
- **Action:** Identifies `new`, `changed`, or `missing` files.
- **Artifact:** `latest_status_report.json`, `latest_lint_report.json` in `006/runs`.

### 3. Conversion Stage (Multi-Route)
- **Module:** `conversion.py`.
- **Action:** 
  - **Route A (Text PDF):** `opendataloader_pdf`.
  - **Route B (Office):** `office.py` → PDF → `opendataloader_pdf`.
  - **Route C (Scanned PDF):** `ocr.py` (OCRmyPDF) → PDF → `opendataloader_pdf`.
  - **Route D (Spreadsheet):** `spreadsheets.py` → CSV/JSON.
- **Artifacts:** `.md` and `.json` in `002_Raw-Conversion-Layer`.

### 4. Canonicalization Stage
- **Modules:** `canonicalize.py`, `concepts.py`.
- **Action:** Applies rules from `canonical_rules.yaml`. Assigns IDs like `law-pd-1096`.
- **Artifact:** YAML-frontmatter Markdown files in `003_Canonical-Knowledge-Layer`.

### 5. Extraction Stage
- **Modules:** `relationships.py`, `relationships_sections.py`.
- **Action:** Pattern matching against concepts defined in `003/shared/concepts`.
- **Artifact:** `latest_relationship_extraction.json` in `006/runs`.

### 6. Review Stage
- **Module:** `ollama_review.py`.
- **Action:** Sends relationship candidates to Ollama (`gemma4:31b`) for `keep`/`reject` decision.
- **Artifact:** `latest_relationship_review_ollama.json` in `006/runs`.

## Stage Status (Implemented vs Missing)
| Stage | Status | Notes |
| :--- | :--- | :--- |
| Ingestion | IMPLEMENTED | File-registry based. |
| Status | IMPLEMENTED | Registry comparison logic. |
| Linting | IMPLEMENTED | Filename and extension checks. |
| Conversion | IMPLEMENTED | PDF, Office, Spreadsheet, and OCR routes. |
| Normalization | PARTIAL | Currently handled during Canonicalization. |
| Canonicalization | IMPLEMENTED | Strict ID system with rules engine. |
| Concept Generation | PARTIAL | Single-concept creation implemented. |
| Relationship Extraction | IMPLEMENTED | Regex pattern matching. |
| Review | IMPLEMENTED | Local LLM integration (Ollama). |
| Promotion | IMPLEMENTED | `run_promote()` in `scripts/vitruvius/promotion/`. Stringency matrix gate (`w_promotion_stringency_gate`), stateful registry (`y_stateful_registry`), RocksDB backend (`hp_rocksdb_verdict_cache`, default `true`). CLI: `promote --execute` / `promote --rollback <batch_id>`. |
| Storage (Graph — Event Store) | IMPLEMENTED | Append-only SQLite event log (`graph/event_store.py`) with RocksDB backend (`graph/rocksdb_event_store.py`, `hp_rocksdb_event_store` defaults `true`). Factory: `make_event_store()`. |
| Storage (Graph — Knowledge Synthesis) | IMPLEMENTED (feature-flagged) | Kuzu hybrid vector+graph store (`wiki/kuzu_store.py`, `wiki_kuzu_store` flag). |
| Storage (Graph — Temporal) | IMPLEMENTED (feature-flagged) | `TemporalEdge` + `temporal_query.query_at()` + Parquet archiver (`gt_temporal_graph` flag). |

## Data Flow
`Raw Source (.pdf/.docx)` → `Markdown (.md)` → `Canonical Markdown (ID/YAML)` → `Extraction JSON` → `Verified JSON`

## Artifact Generation
- **Operational:** CSV registries and JSON status reports in `006_System-Manifests`.
- **Knowledge:** Markdown files in `002` (raw) and `003` (canonical).
- **Execution:** Timestamped JSON/TXT reports in `006_System-Manifests/runs`.

## Module Mapping
- `pipeline_cli.py` → Orchestrator.
- `paths.py` → Path resolution logic (Contract).
- `constants.py` → System-wide directory and file names.
- `reports.py` → CSV/JSON/Text writing utilities.

## Current Limitations
- **Linearity:** The pipeline is mostly linear; branched processing is handled via manual CLI routing.
- **LLM Dependency:** Review stage requires active Ollama server.
- **State Persistence:** Primary state tracking is filesystem-based (registries in `006_System-Manifests`). Optional KV and graph persistence is available via `hp_rocksdb_event_store` (default on), `hp_rocksdb_verdict_cache` (default on), and `wiki_kuzu_store` (default off).

## Externally-Gated Stages (deferred until external conditions met)
- **Sprint D Stream J — Active learning loop:** Requires the Ranger dashboard surface. Not dispatchable until that external dependency is available.
- **Sprint D Stream K — CLUP multi-jurisdiction scaling:** Requires a second jurisdiction corpus to benchmark against. Not dispatchable until that corpus is available.

## Performance Risks
- **OCR:** Processing large scanned PDFs is slow and CPU-intensive.
- **LLM Review:** Reviewing thousands of relationship candidates via Ollama takes significant time.
- **Registry Size:** As the number of files in `001` grows, CSV-based registry comparisons will slow down.

## Post-Sprint-D Pipeline Additions (2026-04-15)

The baseline flow above is the authoritative default-off path. The **ten** sprints closed in this session (Q, R, PHYS, H, GEOM, WIKI, GT, HP, Z, and the follow-on Sprint HP.3-R RocksDB migration) layered additional optional stages on top, all gated behind `features.*` flags in `config/vitruvius.yaml`. When every non-RocksDB flag is `false`, the pipeline is byte-identical to the pre-Sprint-D baseline described above. (The `hp_rocksdb_*` flags default `true` per AD-029 because the RocksDB migration replaces only the storage layer under the `EventStore` / `StatefulReviewRegistry` API contracts — consumer code is unchanged.)

### Sprint Q — Live Wiring (w_* flags)

The review stage (`run_review_ollama`) now has optional live hooks for the Stream F + G scaffolds that Sprint D shipped as dead code:

1. **NB prefilter** (`w_review_nb_prefilter`) — auto-rejects candidates a Naive Bayes head scores below threshold before any LLM call.
2. **Ontology prompt builder** (`w_review_ontology_prompt`) — renders 2-hop graph neighborhoods from the canonical relationships store into the reviewer prompt so the LLM can cross-reference prior decisions.
3. **SLM domain router** (`w_review_slm_routing`) — picks between draft / default / heavy local models by document class and candidate novelty.
4. **Conformal gate** (`w_review_conformal_routing`) — decorates every review decision with a p-value that drops anything above the calibrated α.
5. **Tension analyzer + Choquet fuzzy aggregation** (`w_review_tension_reflection` + `w_review_choquet_aggregator`) — fuses multiple reviewer votes when Tier 2 fires.
6. **8GB LLM survival mode** (`w_llm_model_pool`, `w_llm_num_ctx_enforcement`, `w_llm_context_budget_guard`) — caps memory so small local models fit on 8 GB M2.

Promotion (`run_promote`) gained a **stringency matrix gate** (`w_promotion_stringency_gate`) that compares each candidate edge against the governing standard in the 20-concept stringency vectors. Losing edges are marked `is_governing_standard=False`; the winner is marked `True`.

### Sprint R — Per-Layer Embeddings & Agentic Reasoning (y_* flags)

Layered on top of the review stage:

1. **Source identity vector + prefix injector** (`y_contextual_priming`) — every reviewer prompt is prefixed with a deterministic `SOURCE_IDENTITY[fingerprint]: <prose>` block so the LLM sees the document's legal context for free.
2. **Domain classifier + MoE router** (`y_domain_routing_moe`) — routes candidates to specialized reviewer models by detected domain (building-law vs. fire-code vs. sanitation, etc.).
3. **Thinking mode + CoT audit** (`y_thinking_mode_cot`) — enforces `<thinking>` / `<answer>` envelope in the reviewer output and dumps the trace to `005_Operational-Intelligence-Layer/cot_audit/`.
4. **Stateful agentic registry** (`y_stateful_registry`) — persistent cache infrastructure keyed on `(source_hash, relationship_hash, model_version)`. The registry factory and RocksDB backend ship, but the dedicated `review_with_cache()` wrapper is still a follow-on wiring path rather than the default live review loop.
5. **Vision OCR** (`y_vision_ocr`) — falls back to a vision LLM (moondream) when OCR confidence is below threshold. Operator-gated: requires `ple-vision-probe` activation.

### Sprint GT — Spatial GraphRAG (gt_* flags)

New optional stage between extraction and review:

- **Proximity jump + decay-weighted edges** (`gt_proximity_jump`, `gt_spatial_edges`) — when `spatial_edge_builder` has ingested a building's geometry, candidates are re-ranked so spatially adjacent sections boost each other's confidence before the LLM sees them.
- **Temporal edges** (`gt_temporal_graph`) — graph contract now supports `valid_from` / `valid_until` on every edge so rollback-aware queries work through `temporal_query.query_at(timestamp)`. Data lives in the event store (Sprint HP.3 SQLite or Sprint HP.3-R RocksDB, selected via `hp_rocksdb_event_store`).
- **Parquet archiver** (Sprint GT.3.3) — snapshots the graph to Parquet via pyarrow for cold-storage archival.
- **Hardware hardening** (`gt_hardware_hardening`) — mmap + Bloom filter foraging + MC dropout uncertainty utility (GT.5.1/5.2/5.3).
- **Rust data plane** (`gt_engine_rs`) — linear octree + `SpatialPoint` shipped via the `engine_rs` pyo3 crate.

### Sprint Z — Compound AI (z_* flags)

A new post-review stage that only activates on Tier 2 candidates:

- **Adversarial swarm** (`z_adversarial_swarm`) — Proposer generates candidates, Inspector argues against them, Adjudicator picks a winner.
- **Differential dataflow** (`z_differential_dataflow`) — `DependencyTracker` + `DifferentialPropagator` propagate deltas from the graph store to downstream consumers without re-evaluating the whole graph. Walks the tracker per `Delta` batch, so amendments to PD 1096 run in O(Δ) in the changed set rather than in the total graph size.
- **DSPy prompt compiler** (`z_dspy_compiler`) — metric-driven prompt optimization that compiles prompt templates against a held-out set of review decisions.
- **Neuro-symbolic Datalog bridge** (`z_neuro_symbolic`) — experimental prompt/evaluator scaffolding. The Rust `datalog_rs` crate and prompt directives ship, but PASS 2 found no audited live review-loop caller proving this as an active enforcement path yet.
- **Wasm spatial kernel** (`hp_wasm_kernels`) — loads the `engine_rs` `aabb_intersects` function via wasmtime for hermetic spatial verification that can run in constrained environments.

### Sprint 1B-M1 — Phase 1B Modernization Tranche 1 (p1b_* flags)

Library-level wiring of the new parser chain. Defaults are **false**; pipeline_cli.py integration is deferred to a follow-up.

- `p1b_docling_parser` — marks `DoclingParser(BaseParser)` as deployed; ready to be registered in `ParserOrchestrator` chains for `hybrid_pdf` / `text_pdf_complex` classes
- `p1b_libreoffice_preprocessor` — marks `LibreOfficePreprocessor` as deployed; ready to be registered as the `office_doc` preprocessor in `ParserOrchestrator`

Both flags are **deployment-readiness markers**, not routing gates — they signal that the classes are available for library consumption without changing any pipeline behaviour. `GATE-005` (`check_gate_005_libreoffice_pdf`) ships alongside.

### Sprint 1B-M2 — Phase 1B Modernization Tranche 2 scoped (p1b_* flags cont.)

Additional library-level wiring. Feasibility audit (`.ai/10_state/feasibility_ml_deps_2026-04-15.json`) deferred marker-pdf + surya-ocr on the current 8 GB M2 environment (disk at 95.2%, RAM at 2.03 GB available). The scoped Tranche 2 shipped zero-new-heavy-dep deliverables instead:

- `p1b_ocr_preprocessor` — marks `OCRPreprocessor` as deployed. Wraps the already-installed `ocrmypdf` (tesseract-backed, ~200 MB RAM per scanned page, low-spec friendly). Ready to be registered as the preprocessor for `SCANNED_PDF_CLEAN` / `SCANNED_PDF_NOISY` classes.
- `p1b_process_pool_orchestration` — marks `ParserOrchestrator.process_batch` as deployed. Current implementation runs jobs sequentially because parsers are not pickle-safe; the `max_workers` kwarg is accepted for a future ProcessPoolExecutor upgrade once parser pickle-safety is verified.

**Deferred to Tranche 3 or later (pending environment unblock):** marker-pdf, surya-ocr, Dynamic Resource Allocation per §11 Phase 3. See AD-032 for full rationale.

### Sprint HP.3-R — RocksDB KV backends (hp_rocksdb_* flags, default TRUE)

Storage-layer swap for the two persistent KV stores. No change to pipeline flow — consumers go through `make_event_store()` / `make_stateful_registry()` factories that pick the backend from the flag:

- `hp_rocksdb_event_store` (default `true` per AD-029) — event store uses `RocksDBEventStore`. Bench at n=10000: **18.7× faster** than SQLite on append + count + project_graph_at. Fallback to SQLite by flipping to `false`.
- `hp_rocksdb_verdict_cache` (default `true` per AD-029) — verdict cache uses `RocksDBStatefulReviewRegistry`. Bench at n=10000: **24.3× faster** than SQLite on put + get-hit + get-miss. Fallback to SQLite by flipping to `false`.

Migration tool: `ple-kv-migrate --store {event,registry} --source SQLITE_PATH --dest ROCKSDB_DIR [--dry-run]`. Idempotent (event store catches duplicate `event_id` ValueError; registry does a pre-write existence check and reports skipped rows).

### Sprint WIKI — Knowledge Synthesis (wiki_* flags)

Standalone side-pipeline (not in the main `run` chain):

- `wiki_docling_parser` — Docling parser for PDF → structured markdown
- `wiki_kuzu_store` — Kuzu graph store (hybrid vector + graph)
- `wiki_delta_tracking` — SHA-256 delta tracker for incremental synthesis
- `wiki_synthesis_loop` — LLM-driven wiki synthesis loop (uses `OllamaLLMClient`)
- `wiki_ego_linter` — LLM ego-graph linter that rejects drafts with internal contradictions

### Sprint PHYS — Graph Physics (phys_* flags)

Post-promotion analytics layer:

- `phys_pagerank` — PageRank over the canonical relationship graph
- `phys_boltzmann_gate` — Boltzmann stability gate
- `phys_motif_matcher` — VF2 motif matcher (absorbs orphan Stream O)
- `phys_shannon_sampling` — Shannon entropy sampler
- `phys_eigenvector_cascade` — eigenvector centrality cascade simulation

### Sprint GEOM — Geometric Constraint Engine (geom_* flags)

Standalone side-pipeline for buildable-envelope generation:

- `geom_csp_compiler` — Z3 CSP compiler from canonical rules
- `geom_envelope_2d` — 2D envelope via shapely
- `geom_envelope_3d` — 3D polyhedral envelope via trimesh + mapbox-earcut + manifold3d
- `geom_iou_audit` — multimodal IoU audit
- `geom_pareto_optimizer` — Pareto optimizer via cvxpy

### Sprint HP — High-Performance Optimizations (hp_* flags)

Transparent perf wins:

- `hp_merkle_fs` — Merkle directory hash (replaces brute-force reconcile walks)
- `hp_event_sourced_graph` — turns on the append-only event log at all (defaults false; orthogonal to which backend is used)
- `hp_wasm_kernels` — Wasm spatial kernels (via `engine_rs` wasm32 target)
- `hp_graphsage` — GraphSAGE embeddings + structural loopholes detector

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
- **2026-04-13:** Initial Pipeline Overview document created from codebase audit. Traced all `run_` commands and artifact flows.
- **2026-04-15:** Added **Post-Sprint-D Pipeline Additions** section covering all 21 closed sprints (Q, R, PHYS, H, GEOM, WIKI, GT, HP, Z, HP.3-R, 1B-M1, 1B-M2, RUST-PDF-1, 1B-M3, DISTILL-1, RUST-MIG-1, AUDIT-1, PIPELINE-CLI, PQ-1, LSH-1, Meta) and their feature flags. Baseline flow documented above is unchanged. Promotion and Storage (Graph) stage status rows updated from NOT IMPLEMENTED to IMPLEMENTED — both shipped in Sprint Q / WIKI / HP / HP.3-R. Missing Stages section replaced with Externally-Gated Stages (Sprint D Streams J + K only).
