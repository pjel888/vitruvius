# Vitruvius — Naming Conventions

## Purpose
This document serves as the single source of truth for all naming conventions within the Vitruvius system. Consistency in naming ensures traceability across the pipeline, prevents collisions in the canonical knowledge layer, and maintains codebase readability.

## Scope
These rules apply to all Python code, CLI interfaces, filesystem structures, and data artifacts (Markdown, JSON, CSV).

## Naming Principles
1.  **Explicitness:** Prefer descriptive names over abbreviations (e.g., `relative_path` instead of `rel_path`).
2.  **Traceability:** Names must reflect the origin or purpose of the entity (e.g., `law-national-building-code`).
3.  **Immutability:** Once a canonical ID is assigned, it should not change, as it acts as a permanent reference.
4.  **Consistency:** Use the same term for the same concept across all layers (e.g., "registry" for state-tracking files).

## Python Code Conventions
Follow [PEP 8](https://peps.python.org/pep-0008/) with the following system-specific refinements:

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

### Function and Method Naming
- **Entry Points:** Functions invoked by the CLI must start with `run_` (e.g., `run_scan()`, `run_canonicalize_one()`).
- **Internal Actions:** Use `snake_case` verbs (e.g., `build_file_entries()`, `detect_pdf_type()`).
- **Path Builders:** Functions generating filesystem paths must start with `build_` and specify the target type (e.g., `build_conversion_relative_paths()`).
- **Directory Enforcers:** Functions that ensure directory existence must start with `ensure_` (e.g., `ensure_snapshot_dir()`).

### Variable Naming
- **Paths:** Always suffix with `_path` (file) or `_dir` (directory) (e.g., `repo_root`, `registry_dir`).
- **Relative vs Absolute:** Prefix with `rel_` or `abs_` if both are present in the same scope, or use descriptive names like `relative_pdf_path`.
- **Constants:** `UPPER_CASE_WITH_UNDERSCORES` (e.g., `RAW_LAYER_NAME`).

### Class Naming
- **Data Models:** `PascalCase` (e.g., `FileEntry`).
- **Interfaces/Engines:** `PascalCase` (e.g., `PdfReader` - from external lib, follow local patterns for internal classes).

## CLI and Entrypoint Naming
- **Commands:** Lowercase with hyphens (kebab-case) (e.g., `scan`, `status`, `ocr-queue`, `canonicalize-one`).
- **Operator-utility commands:** Prefixed with `ple-` (e.g., `ple-kv-migrate`, `ple-cotrace-dump`, `ple-registry-purge`, `ple-vision-probe`). The `ple-` prefix marks commands that are not part of the standard pipeline run but are privileged operator tools for maintenance, migration, or diagnostics.
- **Arguments:** Lowercase with underscores (snake_case) (e.g., `relative_pdf_path`).
- **Flags:** Lowercase with hyphens (kebab-case) (e.g., `--sample-pages`, `--no-deskew`).

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

## File and Folder Naming

### Root Layers
Folders must be prefixed with a 3-digit index and use Pascal-Kebab-Case:
- `001_Raw-Source-Layer/`
- `002_Raw-Conversion-Layer/`
- `003_Canonical-Knowledge-Layer/`
- `004_Derived-Content-Layer/`
- `005_Operational-Intelligence-Layer/`
- `006_System-Manifests/`

### Sub-Directories
- Use lowercase with underscores or hyphens as established by the specific layer (e.g., `raw_markdown`, `sidecar_json`).

## Artifact Naming (Markdown, JSON, Reports)

### Reports and Logs
- **Latest Version:** `latest_<type>_report.<ext>` (e.g., `latest_status_report.json`).
- **Timestamped Version:** `<ISO8601Z_STAMP>_<safe_stem>_<type>_report.<ext>`.
  - Timestamp Format: `%Y%m%dT%H%M%SZ` (e.g., `20260413T120000Z`).
  - Example: `20260413T043540Z_PD_1096_detect_one_report.json`.

### Registries
- `latest_<type>_registry.csv` (e.g., `latest_conversion_registry.csv`).
- `<ISO8601Z_STAMP>_<type>_registry.csv`.

## Canonical Entity Naming
### ID Naming Standards
Canonical IDs follow the pattern: `<prefix>-<slugified-title>`
- **Valid Prefixes:** `law`, `irr`, `concept`, `glossary`, `relationship`, `handout`, `reviewer`, `law-section`, `source`.
- **Slugification:** Lowercase, alphanumeric, hyphens instead of spaces/special chars.
- **Example:** `law-national-building-code-of-the-philippines`.

### Concept Naming
- **Files:** `<slugified-concept>.md` (e.g., `occupancy-classification.md`).
- **ID:** `concept-<slugified-concept>` (e.g., `concept-occupancy-classification`).

### Source Naming
- **Files:** `<slugified-title>.md` (e.g., `national-building-code.md`).

## Relationship Naming
Relationships extracted between entities must use lowercase verbs (closed vocabulary — additions require a schema bump AND an AD per I4):
- `requires`
- `defines`
- `depends_on`
- `limits`
- `affects`
- `governs` (Law → Concept)
- `supersedes` (newer law/version → older)

## Registry and Manifest Naming
- Headers in CSV registries must use `snake_case` (e.g., `source_relative_path`, `timestamp_utc`).

## Anti-Patterns (Forbidden Naming)
- **Generic Names:** Avoid `data.json`, `process.py`, `tmp/`.
- **Mixed Casing in Files:** Avoid `MyFile.Md` or `data_Report.JSON`.
- **Spaces in Filenames:** Never use spaces; use hyphens for canonical files and underscores for internal reports.
- **Ambiguous Timestamps:** Never use local time; always use UTC with `Z` suffix.

## Migration Rules
When renaming legacy files (e.g., `Word-PPT-To-PDF.py` → `word_ppt_to_pdf_cli.py`), a `migrate-ids-plan` must be generated to ensure no breakage in the registry layer.

## Enforcement Rules
1.  **Linter:** `run_lint` stage in the pipeline checks for basic naming violations.
2.  **Pull Request Review:** All new modules and canonical entities must be verified against this document.
3.  **Automated Checks:** `canonicalize.py` enforces ID prefix validation.

## Changelog
- **2026-04-13:** Initial version established from codebase audit. Standardized timestamp formats, ID prefixes, and report naming patterns.
- **2026-04-15:** Expanded Pipeline Stage Naming from 7 to 41 commands (as of AD-042). Added Feature Flag Naming section with prefix registry. Added Rust crate and pyo3 symbol naming rules (AD-036). Added TypeScript (spatial-daemon) conventions. Added `supersedes` predicate. Added `ple-` operator-utility command prefix.
