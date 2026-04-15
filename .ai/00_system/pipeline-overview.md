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
| Promotion | NOT IMPLEMENTED | Moving from `draft` to `verified` is manual. |
| Storage (Graph) | NOT IMPLEMENTED | Planned for Layer 005. |

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
- **State Persistence:** Entirely filesystem-based; no database for querying across files.

## Missing Stages
- **Automated Promotion:** No automated workflow to promote artifacts from conversion to canonical without manual ID verification.
- **Graph Ingestion:** No automatic sync to a graph database (e.g., Neo4j).

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
4. **Stateful agentic registry** (`y_stateful_registry`) — persistent cache of every reviewer decision keyed on `(source_hash, relationship_hash, model_version)`. Consumed by Phase 6A Resume to avoid re-reviewing unchanged candidates. Sprint HP.3-R added a RocksDB backend behind this, routed via `make_stateful_registry()`.
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
- **Neuro-symbolic Datalog bridge** (`z_neuro_symbolic`) — reviewer prompts are decorated with a `<logic-directive>` that forces the LLM to emit a `<logic>` Datalog block the Rust `datalog_rs` evaluator verifies. Rejects the verdict if the block fails to parse or fails to derive the conclusion from the facts.
- **Wasm spatial kernel** (`hp_wasm_kernels`) — loads the `engine_rs` `aabb_intersects` function via wasmtime for hermetic spatial verification that can run in constrained environments.

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

See `.ai/10_state/decisions.md` AD-024 through AD-029 for the per-sprint ledger including commit SHAs and sprint tags.

## Changelog
- **2026-04-13:** Initial Pipeline Overview document created from codebase audit. Traced all `run_` commands and artifact flows.
- **2026-04-15:** Added **Post-Sprint-D Pipeline Additions** section covering all ten sprints (Q/R/PHYS/H/GEOM/WIKI/GT/HP/Z/HP.3-R) and their feature flags. Baseline flow documented above is unchanged.
