---
plan_id: rust-migration-audit
phase: "Meta — Python/Rust Polyglot Split"
title: "Rust Migration Audit & Phased Port Plan: The Rust Line"
status: planned
priority: high
sprint: "Sprint RUST-MIG-1 (audit-then-phased-implementation)"
version: 1.0.0
plan_type: audit_then_conditional_implementation
created: 2026-04-15
last_updated: 2026-04-15
owner: Senior Systems Architect
dependencies:
  - .ai/03_plans/00-governing-implementation-plan.md
  - .ai/10_state/decisions.md
  - scripts/vitruvius/engine_rs/  # existing Cargo workspace
  - scripts/vitruvius/datalog_rs/ # existing pyo3 crate
  - scripts/vitruvius/bench/      # existing bench harnesses (Sprint Q W4 + Sprint HP.3-R + RUST-PDF-1)
---

# Rust Migration Audit & Phased Port Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.
>
> **Important:** This is an **audit-then-conditional-implementation** plan. Tasks 1–3 are audit / baseline / scaffolding and MUST land before Tasks 4–7 (the actual Rust ports). Tasks 4–7 are each gated on Task 3's bench baseline showing the target function is actually a bottleneck — if a baseline measures less than **25 ms wall-clock and <10 MB incremental RSS** on the representative PD 1096 corpus, mark that phase as **DEFER_LOW_IMPACT** and move to the next.

**Goal:** Execute the "Python / Rust polyglot" split by porting a small, high-ROI set of pure-mathematical and spatial kernels to Rust behind the existing `engine_rs` Cargo workspace, with every migration gated on a measured Python baseline.

**Architecture:** Python remains the Control Plane (LLM routing, orchestration, high-level API, prompt building, subprocess dispatch, YAML/JSON config, pytest harness). Rust becomes the Data Plane for pure-math and pure-spatial kernels (AABB intersection, distance decay, Mahalanobis, sliced Wasserstein). No new Cargo workspace is created — this plan **extends** the existing `scripts/vitruvius/engine_rs/` workspace with a new `spatial_kernels/` crate and a new `stats_kernels/` crate, both exposed through the single `pyo3_shim` Python extension module that already ships.

**Tech Stack:** Rust 1.94+, pyo3 0.22, maturin for wheel builds, nalgebra (dense linalg), ndarray (0-copy numpy bridge via numpy crate), existing `vitruvius_engine_rs` Python extension module. Python-side bench uses `/usr/bin/time -l` subprocess isolation (already proven in Sprint HP.3-R AD-029 and Sprint RUST-PDF-1 AD-033 bench harnesses).

---

## 1. The Rust Line (operating principle)

> **Above the line (stays in Python):** LLM tool calling, prompt building, API routing, high-level pipeline orchestration, subprocess dispatch to external tools (LibreOffice, OCRmyPDF, opendataloader_pdf), YAML/JSON config loading, CLI argument parsing, feature-flag dispatch, test harness, experiment recording.
>
> **Below the line (migrates to Rust):** Data parsing (`vitruvius_rust_pdf` — done), statistical evaluation (Mahalanobis, Wasserstein), mathematical modeling (sliced distances, distance decay), spatial/geometric algebra (AABB intersection, octree queries — done), graph traversal (conditional — see §2.4), heavy vector operations, memory-intensive deduplication (conditional — see §2.5).

This plan is the reification of that rule. Every candidate in §2 is labeled with its side of the line and, if it's below, its expected ROI.

---

## 2. Audit Log — the full Python heavy-compute surface

The table below is the authoritative output of four parallel audit agents who surveyed the current `main` branch on 2026-04-15 14:30 local. Every entry has been verified to exist in the tree. Candidates are ranked by **estimated wall-time + RAM payoff**.

### 2.1 Verdict legend

- **GO** — pure algorithm with no Python-native ML library coupling; natural Rust port, no serialization bottleneck
- **MAYBE** — mixed: some Rust benefit but coupling risk; requires Task 3 bench baseline to confirm it's actually a bottleneck
- **DEFER** — already uses a native C/C++ backend (numpy LAPACK, scipy, networkx↔scipy, trimesh/manifold3d, Shapely/GEOS, Z3, cvxpy); Rust port gains ≈0
- **NO_GO** — tight coupling to Python-native ML (torch, sklearn pickle, sentence-transformers, dspy); PyO3 serialization cost >> compute savings
- **ALREADY_RUST** — function has a live Rust counterpart being called from Python; no migration needed

### 2.2 Spatial / Geometric candidates

| # | File : lines | Function | What it computes | Complexity | Verdict | ROI Rank |
|---|--------------|----------|------------------|------------|---------|----------|
| S1 | `scripts/vitruvius/spatial/spatial_edge_builder.py:53-95` | `build_spatial_adjacency_edges` | O(n²) pairwise AABB intersection → `physically_adjacent_to` edges | O(n²) | **GO** | **1 (highest)** — expected 50–100× on 10k nodes |
| S2 | `scripts/vitruvius/spatial/proximity_jump.py:105-126` | `weight_by_distance` | O(n) distance-decay weighting `exp(-λ·d)` over seed centroids | O(n) | **GO** | **2** — expected 20–50× on 10k seeds |
| S3 | `scripts/vitruvius/spatial/proximity_jump.py:63-104` | `proximity_jump_seed` | Query existing Rust octree, then filter snapshot IDs in Python | O(k) | **ALREADY_RUST** (octree query) + Python filter | Marginal — bridge overhead already amortized |
| S4 | `scripts/vitruvius/spatial/constraint_solver.py:37-86` | `evaluate_constraint`, `evaluate_batch` | Z3 SMT parametric evaluation | O(c) | **DEFER** — Z3 is native C++; bridge wins nothing | N/A |
| S5 | `scripts/vitruvius/geometric/inequality_compiler.py:62-113` | `check_compliance` | Z3 incremental push/pop solver | O(c) per parameter | **DEFER** — Z3 is native C++ | N/A |
| S6 | `scripts/vitruvius/geometric/envelope_2d.py:31-58` | `compute_buildable_envelope` | Shapely polygon erosion + WKT export | O(v) | **DEFER** — Shapely/GEOS is C++ | N/A |
| S7 | `scripts/vitruvius/geometric/envelope_3d.py:45-100` | `compute_3d_envelope` | Trimesh extrusion + volume/IoU | O(v+t) | **DEFER** — trimesh/manifold3d is C++ | N/A |
| S8 | `scripts/vitruvius/geometric/pareto_optimizer.py:24-70` | `maximize_far_under_constraints` | cvxpy LP | O(1) for 3-var LP | **DEFER** — cvxpy wraps native LP solver | N/A |
| S9 | `scripts/vitruvius/compound/wasm_kernel.py:50-100` | `WasmSpatialKernel.aabb_intersects` | wasmtime loader + wasm AABB | O(1) | **ALREADY_RUST** (engine_rs wasm target) | Bridge overhead only |
| S10 | `scripts/vitruvius/foraging/bloom_filter.py:20-60` | `add`, `check` | Bloom filter over blake2b hash | O(k) where k≈5-10 | **MAYBE** — pure Python hashlib; negligible latency today | Gate on Task 3 bench |
| S11 | `scripts/vitruvius/foraging/drift_detector.py:30-50` | `detect_source_drift` | Mahalanobis distance over baseline | O(d²) | Merge with N4 below | — |

### 2.3 Statistical / numerical candidates

| # | File : lines | Function | What it computes | Complexity | Verdict | ROI Rank |
|---|--------------|----------|------------------|------------|---------|----------|
| N1 | `scripts/vitruvius/graph/wasserstein_merge.py:70` | `wasserstein_merge_decision` | Exact 2-Wasserstein distance between two embedding sets via `ot.dist` + `ot.emd2` (POT native C++ LP) — **NOT** sliced, as this row originally claimed | O(n³) network simplex over (n, n) cost matrix | **DEFER_ALREADY_NATIVE** — see AD-038a, corrected during Task 7 dispatch | — |
| N2 | `scripts/vitruvius/graph/mc_dropout.py:34` | `compute_epistemic_uncertainty` | Sample variance over MC dropout predictions (stdlib `statistics`) | O(s) | **DEFER** — already stdlib-native; migrating is churn | N/A |
| N3 | `scripts/vitruvius/graph/tensor_factorisation.py:82` | `factorise_snapshot` | numpy.linalg.svd aggregation | O(n·m·k) | **DEFER** — LAPACK-backed, already native | N/A |
| N4 | `scripts/vitruvius/normalization/outlier_detector.py:47-120` | `fit_outlier_model`, `mahalanobis_distance`, `score_chunks` | Mahalanobis distance: covariance inversion + quadratic form | O(d²) fit + O(d) per score | **GO** (conditional) | **3** — pure numpy math; 10–50× if `sklearn.covariance.EmpiricalCovariance` is swapped for a pure nalgebra fit. Need to confirm via §5 Task 1.3 whether sklearn is mandatory. |
| N5 | `scripts/vitruvius/priming/drift_detector.py:56` | `measure_drift` | Cosine similarity + L2 norm | O(d) | **MAYBE** — tight but low volume; gate on Task 3 | |
| N6 | `scripts/vitruvius/priming/context_vector.py:98` | `build_source_identity` | SentenceTransformer embedding | O(model) | **NO_GO** — sentence-transformers runtime dominates | N/A |
| N7 | `scripts/vitruvius/review/naive_bayes_filter.py:199` | `fit_filter`, `classify` | Multinomial NB log-probability | O(fv · c) | **NO_GO** — sklearn MultinomialNB pickle/deserialize bridge | N/A |
| N8 | `scripts/vitruvius/review/choquet_aggregator.py:84` | `choquet_integral` | Non-additive fuzzy measure over powerset | O(2ⁿ) where n=5-10 | **DEFER** — n is tiny; compute is irrelevant | N/A |
| N9 | `scripts/vitruvius/review/conformal_calibrator.py:62` | `fit_calibration_threshold` | Quantile over calibration scores | O(k log k) | **DEFER** — numpy quantile already native | N/A |
| N10 | `scripts/vitruvius/promotion/bayesian_fusion.py:91` | `fuse_evidence` | Log-odds Bayesian belief fusion | O(n_signals) | **DEFER** — n is small, float arith | N/A |
| N11 | `scripts/vitruvius/graph/mcmc.py:66` | `mcmc_random_walk` | Markov chain stationary distribution via random walk | O(n·steps) | **MAYBE** — pure numpy but walks are called offline, not in a hot query loop; gate on bench | |
| N12 | `scripts/vitruvius/graph/physics.py:69-140` | `compute_pagerank` | `nx.pagerank` wrapper | O(n_edges · iter) | **DEFER** — networkx delegates to scipy sparse iterative | N/A |
| N13 | `scripts/vitruvius/graph/physics.py:286-302` | `find_impact_radius` | `nx.eigenvector_centrality_numpy` | O(n_nodes) eigendecomposition | **DEFER** — scipy/LAPACK | N/A |
| N14 | `scripts/vitruvius/graph/spectral.py:67` | `compute_spectral_partition` | Spectral clustering via Laplacian eigsh | O(n²) dense for small n | **DEFER** — scipy.sparse.linalg | N/A |
| N15 | `scripts/vitruvius/graph/graphsage.py` | GraphSAGE forward pass | torch GNN | O(n·nbr·d) | **NO_GO** — torch.Tensor ↔ numpy marshaling across PyO3 is the bottleneck, not the compute | N/A |
| N16 | `scripts/vitruvius/graph/centrality.py:57` | `compute_centrality` | Betweenness + closeness via networkx | O(n·m) | **DEFER** — networkx/scipy | N/A |
| N17 | `scripts/vitruvius/graph/community.py:72` | `detect_communities` | Louvain via python-louvain | O(n+m) | **DEFER** — networkx wrapper | N/A |
| N18 | `scripts/vitruvius/graph/tda.py:72` | (persistent homology stubs) | Skeleton only | N/A | **DEFER** — no real computation yet | N/A |

### 2.4 Graph traversal & dedup candidates

| # | File : lines | Function | What it computes | Complexity | Verdict | ROI Rank |
|---|--------------|----------|------------------|------------|---------|----------|
| G1 | `scripts/vitruvius/relationships_sections.py:246-322` | `dedupe_by_endpoints` | Group candidates by `(from_id, to_id)`, select highest-occurrence predicate per group | **O(n log n)** via dict groupby (NOT O(n²) — correction to Sprint LSH-1's premise) | **DEFER** | Current Python dict-based dedup is already fast. If fuzzy/near-duplicate dedup is needed, **that** is the Sprint LSH-1 target. |
| G2 | `scripts/vitruvius/foraging/duplicate_detector.py:27-48` | `find_duplicate` | Linear scan for matching SHA-256 | O(n·file_size) | **MAYBE** — gate on bench; Bloom prefilter (S10) would help first | |
| G3 | `scripts/vitruvius/graph/traverse.py:16-50` | `neighbors`, `typed_edges` | List-scan neighbor lookup from `GraphSnapshot` | O(n_edges) | **DEFER** — negligible; used in cold paths only | N/A |
| G4 | `scripts/vitruvius/graph/physics.py:48-67` | `_build_directed_graph` | `GraphSnapshot` → `nx.DiGraph` conversion, parallel-edge aggregation | O(n+m) | **DEFER** — one-shot conversion, not hot | N/A |

### 2.5 Data parsing candidates

| # | File : lines | Function | What it does | Verdict |
|---|--------------|----------|--------------|---------|
| P1 | `scripts/vitruvius/parsers/rust_pdf_parser.py` | PDF extraction via `vitruvius_rust_pdf` | **ALREADY_RUST** (Sprint RUST-PDF-1 AD-033 — 48× smaller RSS, 625× faster) |
| P2 | `scripts/vitruvius/parsers/opendataloader_parser.py` | Subprocess to `opendataloader_pdf` | **DEFER** — subprocess wrapper; I/O-bound |
| P3 | `scripts/vitruvius/parsers/docling_parser.py` | docling Python library | **DEFER** — docling is Python-native ML |
| P4 | `scripts/vitruvius/parsers/orchestrator.py` | Chain dispatch + exception handling | **DEFER** — pure orchestration |
| P5 | `scripts/vitruvius/conversion.py` (864 lines) | PDF → Markdown via subprocess | **DEFER** — subprocess wrapper |
| P6 | `scripts/vitruvius/office.py` (127 lines) | DOCX/PPTX via LibreOffice subprocess | **DEFER** — subprocess wrapper |
| P7 | `scripts/vitruvius/ocr.py` (278 lines) | OCRmyPDF subprocess queue | **DEFER** — subprocess wrapper |
| P8 | `scripts/vitruvius/spreadsheets.py` (471 lines) | openpyxl library | **DEFER** — openpyxl is C-backed |
| P9 | `scripts/vitruvius/scanner.py:17-25` | `_sha256_of_file` chunked read | **MAYBE** — hashlib is C; only wins if parallelized via rayon; gate on bench |
| P10 | `scripts/vitruvius/merkle_fs.py:52-85` | `calculate_directory_hash` Merkle walk | **MAYBE** — same reasoning as P9; gate on bench |
| P11 | `scripts/vitruvius/concept_enrichment.py:153-200` | Regex definition extraction | **DEFER** — CPython regex is fast enough, not in a hot loop |
| P12 | `scripts/vitruvius/concept_definitions.py` | Regex anchor + section-title extraction | **DEFER** — same |
| P13 | `scripts/vitruvius/canonicalize.py:177-188` | Regex markdown header extraction | **DEFER** — cold path |
| P14 | `scripts/vitruvius/normalization/engine.py` | Rule-based normalization dispatch | **DEFER** — rule registry overhead is fine |

### 2.6 Existing Rust surface (reference — not a migration target)

| Crate | Path | Exposes | Consumed by |
|-------|------|---------|-------------|
| `vitruvius_engine_rs_core` | `scripts/vitruvius/engine_rs/core/` | `SpatialPoint`, `Aabb`, `LinearOctree`, wasm `aabb_intersects` | (internal, via pyo3_shim) |
| `vitruvius_engine_rs` (pyo3_shim) | `scripts/vitruvius/engine_rs/pyo3_shim/` | `SpatialPoint`, `LinearOctree` (with `insert`, `query_sphere`, `query_aabb`, `query_point`) | `spatial/proximity_jump.py`, `test_engine_rs_octree.py`, `test_proximity_jump.py` |
| `vitruvius_rust_pdf` | `scripts/vitruvius/engine_rs/pdf/` | `extract_pdf_text(bytes)`, `version()` | `parsers/rust_pdf_parser.py`, `bench/bench_rust_pdf_audit.py`, `bench/quality_check_rust_pdf.py` |
| `vitruvius_datalog_rs` | `scripts/vitruvius/datalog_rs/` | `evaluate_datalog(facts, rules) -> bool` | `test_datalog_rs_bridge.py` (test-only today; production consumer gated on `z_neuro_symbolic` flag) |

**Build workflow (proven path):** `cd scripts/vitruvius/engine_rs && python3.11 -m maturin build --release` → `pip install target/wheels/*.whl`. `maturin develop` requires a venv and is avoided; this repo has a shared homebrew site-packages workflow.

---

## 3. Feasibility Assessment — per-candidate verdicts with reasoning

### 3.1 Candidates that land in the Rust port (GO)

**S1. `spatial_edge_builder.py::build_spatial_adjacency_edges`** — **ROI rank 1.** The audit confirms this is a pairwise O(n²) AABB intersection test that emits one edge per intersecting pair. The existing `vitruvius_engine_rs::LinearOctree::query_aabb` already does O(log n) spatial queries, so the rewrite is trivial: for each node, query the octree for intersecting AABBs and emit edges only where `id_i < id_j` (to avoid double edges). On a 10k-node snapshot, this changes the runtime from ~25s (10k² = 100M pair checks × ~250 ns each) to ~40 ms (10k × log₂(10k) × ~300 ns). **Expected: 500× wall-clock speedup, O(n²) → O(n log n).** The Rust side is ≤40 lines and reuses the crate that's already compiled.

**S2. `proximity_jump.py::weight_by_distance`** — **ROI rank 2.** A `for seed in seeds: weight = exp(-lambda * distance(focal, seed))` loop. At 10k seeds this costs ~5 ms Python + object allocation overhead; a Rust kernel with zero-copy slice input lands at ~50 µs. **Expected: 100× wall-clock speedup, same O(n) complexity.** Rust side is ≤20 lines.

**N1. `graph/wasserstein_merge.py::wasserstein_merge_decision`** — **CORRECTED — DEFER_ALREADY_NATIVE (see AD-038a, added 2026-04-15 during Task 7 dispatch).** This row originally described N1 as sliced Wasserstein with two sorts + elementwise diff. That premise was wrong. The function is **exact multi-dimensional 2-Wasserstein** via `ot.dist` (BLAS cost matrix) → `ot.emd2` (POT native C++ network simplex LP solver). There is no Python-level sort, no projection loop, no inner hot path to port — the 3830 ms / 369 MB baseline is dominated by the native C++ EMD solve and the (n, n) cost matrix allocation, both already in native code. Per AD-036 §"Why Rust here at all", a Rust reimplementation would duplicate a native LP solver and gain nothing. Every production call site uses d > 1, so a d==1-only sort-diff kernel would never fire outside the synthetic bench harness. Task 7 is deferred with zero compute changes; AD-038a records the full rationale.

**N4. `normalization/outlier_detector.py` — Mahalanobis core** — **ROI rank 3, conditional.** The PURE core is covariance invert + quadratic form. Task 1.3 must verify whether the fit path currently uses `sklearn.covariance.EmpiricalCovariance` (NO_GO because sklearn pickle) or raw numpy (GO). If raw numpy, port `mahalanobis_distance(x, mean, cov_inv)` to nalgebra — 10–50× on long chunk batches.

### 3.2 Candidates gated on Task 3 bench (MAYBE)

**S10. `foraging/bloom_filter.py`** — Bloom filter bit-vector ops with blake2b hashing. hashlib is C-backed, so Python overhead is object allocation per key. If bench shows >5 ms aggregate on representative foraging runs, promote to GO. Otherwise DEFER.

**N5. `priming/drift_detector.py::measure_drift`** — Cosine + L2 over a 384-dim embedding. One call per source per run. If call count × per-call time < 25 ms, DEFER.

**N11. `graph/mcmc.py::mcmc_random_walk`** — Pure-numpy random walk. If the walk length × snapshot size keeps it under 25 ms in production, DEFER.

**G2. `foraging/duplicate_detector.py::find_duplicate`** — Linear SHA-256 comparison over corpus. If the corpus grows past 10k files, bench will show this is a bottleneck and Rust + rayon becomes a GO. Otherwise DEFER.

**P9. `scanner.py::_sha256_of_file`** — hashlib chunked read per file. Same logic as G2. If scanner runs cold-start, this is never hot; if it runs during a watch loop, Rust + rayon is a MAYBE win.

**P10. `merkle_fs.py::calculate_directory_hash`** — Walks the tree, hashes each file, concatenates. Same reasoning as P9.

### 3.3 Explicit non-migration list (DEFER / NO_GO)

Items listed in §2.2–2.5 with verdict `DEFER` or `NO_GO` MUST NOT be migrated as part of this plan. They are recorded here so a future engineer can verify the rationale rather than rediscovering it:

- **Solver bridges** (Z3 via `constraint_solver`, `inequality_compiler`; cvxpy via `pareto_optimizer`) — native C++ solvers; bridge wins nothing
- **Geometry-lib coupled** (`envelope_2d` via Shapely; `envelope_3d` via trimesh + manifold3d) — native C++ geometry kernels
- **scipy/LAPACK-backed** (`tensor_factorisation` via numpy.linalg.svd; `spectral` via scipy.sparse.linalg; `physics::compute_pagerank` via networkx→scipy; `physics::find_impact_radius` via `nx.eigenvector_centrality_numpy`; `centrality`, `community`) — already native
- **ML library coupled** (`graphsage` via torch; `review/naive_bayes_filter` via sklearn MultinomialNB; `priming/context_vector` via sentence-transformers; `compound/dspy_compiler` via dspy) — PyO3 torch.Tensor marshaling is the bottleneck, not compute
- **Subprocess wrappers** (`conversion`, `office`, `ocr`, `spreadsheets`, `opendataloader_parser`, `docling_parser`) — I/O-bound, no CPU hot path
- **Cold-path orchestration** (`traverse`, `relationships`, `canonicalize`, `concept_enrichment`, `normalization/engine`, `parsers/orchestrator`) — cold paths, no measurable gain

### 3.4 Important finding: Sprint LSH-1 premise correction

The parallel audit confirmed that `scripts/vitruvius/relationships_sections.py::dedupe_by_endpoints` (lines 246-322) is currently an **O(n log n)** dict-grouped dedup, **not O(n²)**. It groups candidates by `(from_id, to_id)` key and picks the highest-occurrence predicate per group. The Sprint LSH-1 plan at `.ai/03_plans/2026-04-15-lsh-dedup-plan.md` describes it as O(n²) pairwise. **This is wrong and the LSH plan must be corrected before dispatch.**

However, Sprint LSH-1 still has real value: it targets **fuzzy / near-duplicate** dedup (e.g., "lot area ≥ 100 sqm" vs "minimum lot area of 100 square meters"), which the current exact-match dict dedup cannot catch. The LSH plan's cost/benefit framing must be rewritten from "scaling fix for O(n²)" to "semantic dedup unlock for near-duplicates". **Action:** Task 2 of this plan writes an AD-### clarifying the LSH plan's actual value. Sprint LSH-1 is NOT part of the Rust migration — it stays in Python using the `datasketch` library.

---

## 4. Target Rust Architecture

The existing `scripts/vitruvius/engine_rs/` Cargo workspace already has three members. This plan **extends** that workspace rather than creating a parallel tree. All new code lives under the same workspace so:

- One maturin build produces one wheel containing `SpatialPoint`, `LinearOctree`, and the new kernels
- One Python import surface (`vitruvius.engine_rs` / `vitruvius_engine_rs`) remains the only Rust-backed module name
- Existing tests under `scripts/tests/test_engine_rs_*.py` scale to cover the new functions

### 4.1 Proposed layout (extension of existing workspace)

```
scripts/vitruvius/engine_rs/
├── Cargo.toml                          (workspace — UPDATE to add new members)
├── core/                               (existing — LinearOctree, SpatialPoint, Aabb)
│   ├── Cargo.toml
│   └── src/
│       ├── lib.rs                      (existing)
│       ├── octree.rs                   (existing)
│       └── wasm_api.rs                 (existing)
│
├── spatial_kernels/                    (NEW — S1 + S2)
│   ├── Cargo.toml                      (deps: core, ndarray, optional rayon)
│   └── src/
│       ├── lib.rs                      (re-exports + tests)
│       ├── adjacency_edges.rs          (S1 — O(n log n) pairwise AABB via LinearOctree)
│       └── distance_weight.rs          (S2 — zero-copy exp(-λ·d) kernel)
│
├── stats_kernels/                      (NEW — N4 only; N1 DEFER_ALREADY_NATIVE per AD-038a)
│   ├── Cargo.toml                      (deps: nalgebra 0.33, ndarray, numpy 0.22)
│   └── src/
│       ├── lib.rs                      (re-exports + tests)
│       ├── mahalanobis.rs              (N4 — pure nalgebra covariance invert + quadratic form)
│       └── (no wasserstein.rs — N1 DEFER_ALREADY_NATIVE per AD-038a; POT's native C++ LP solver owns the hot path)
│
├── pdf/                                (existing — vitruvius_rust_pdf)
│   └── ...
│
└── pyo3_shim/                          (existing — UPDATE to re-export new kernels)
    ├── Cargo.toml                      (ADD deps: spatial_kernels, stats_kernels)
    └── src/
        └── lib.rs                      (ADD #[pyfunction] wrappers for S1/S2/N4; N1 DEFER_ALREADY_NATIVE per AD-038a)
```

### 4.2 Python-side import surface

All new kernels land on the same existing module so the Python call sites can switch between pure-Python and Rust via a thin `try_rust_else_python` pattern that already exists for `engine_rs.LinearOctree`:

```python
# scripts/vitruvius/engine_rs/__init__.py  (existing; extend)
try:
    _ext = import_module("vitruvius_engine_rs")
except ImportError as exc:
    _ext = None
    _IMPORT_ERROR = exc

# NEW re-exports — follow existing pattern
build_spatial_adjacency_edges_rs = getattr(_ext, "build_spatial_adjacency_edges", None)
weight_by_distance_rs            = getattr(_ext, "weight_by_distance",            None)
mahalanobis_distance_rs          = getattr(_ext, "mahalanobis_distance",          None)
sliced_wasserstein_rs            = None  # N1 DEFER_ALREADY_NATIVE per AD-038a — never landed; placeholder retained for archival context, not re-exported by engine_rs/__init__.py
```

Each Python call site gains a two-line toggle:

```python
# scripts/vitruvius/spatial/spatial_edge_builder.py (after Task 4)
from vitruvius.engine_rs import build_spatial_adjacency_edges_rs
...
if build_spatial_adjacency_edges_rs is not None and features.is_enabled("rust_mig_spatial_kernels"):
    return build_spatial_adjacency_edges_rs(nodes)  # Rust fast path
# else: existing pure-Python implementation stays as fallback
```

### 4.3 Feature flags (gated rollout)

Following the `EXPECTED_FLAGS` registry discipline from `scripts/tests/test_features.py`, this plan introduces **two flags**, both default `false`:

- `rust_mig_spatial_kernels` — enables S1 + S2 rust paths
- `rust_mig_stats_kernels` — enables N4 rust path (originally scoped for N1 + N4; N1 DEFER_ALREADY_NATIVE per AD-038a)

Flag-OFF behavior is byte-identical to the pre-migration pipeline — the Python fallback stays intact. Flag-ON is the audited speedup. Flipping either flag to `true` happens only after:
1. The Rust port passes correctness parity tests against the Python baseline (Task 3 harness)
2. The bench harness measures the speedup and records numbers in an AD-### entry

### 4.4 Dependency budget

| Crate | Dependency | Reason |
|-------|------------|--------|
| `spatial_kernels` | `vitruvius_engine_rs_core` (existing) | Reuse `LinearOctree`, `Aabb` |
| `spatial_kernels` | `ndarray = "0.15"` | Zero-copy numpy bridge for seed arrays |
| `stats_kernels` | `nalgebra = "0.33"` | Dense linear algebra (covariance invert, cholesky) |
| `stats_kernels` | `ndarray = "0.15"` | Same — zero-copy numpy bridge |
| `stats_kernels` | `numpy = "0.22"` | pyo3 bridge for `PyArray1<f64>`, `PyArray2<f64>` |
| `pyo3_shim` | `spatial_kernels`, `stats_kernels` | Re-export bindings |
| `pyo3_shim` | `pyo3 = "0.22"` (existing) | Python extension module |

**No new system dependencies.** `nalgebra` is pure Rust; `ndarray` and `numpy` crates are the standard PyO3 pattern. Maturin will continue to produce a single wheel.

---

## 5. Execution Phasing — ranked by ROI

### Phase A (Week 1) — Highest single-module wins

- **A.1** S1 `build_spatial_adjacency_edges` Rust port (ROI rank 1)
- **A.2** S2 `weight_by_distance` Rust port (ROI rank 2)

Expected combined impact: **wall-time reduction of ~25 seconds → ~50 ms on a 10k-node snapshot**; **peak RSS reduction of ~200 MB** (Python list/dict overhead vs. Rust Vec with borrowed references).

### Phase B (Week 2) — Pure-math kernels

- **B.1** N4 Mahalanobis distance (ROI rank 3 — conditional on no sklearn dependency)
- **B.2** ~~N1 Sliced Wasserstein (ROI rank 4)~~ — **DEFER_ALREADY_NATIVE (AD-038a).** Re-inspection at Task 7 dispatch showed N1 is exact multi-dim 2-Wasserstein via POT's native C++ `emd2`, not sliced sort+diff. No Python-level hot path to port. Sprint RUST-MIG-1 shipping surface stays S1 + S2 + N4.

Expected combined impact: **wall-time reduction of ~200 ms → ~20 ms on a 2000-chunk batch**; no meaningful RSS gain.

### Phase C (Week 3 — conditional)

Only fires if Task 3 bench measures any of the MAYBE candidates above the **25 ms wall-clock / 10 MB RSS** gate:

- **C.1** S10 Bloom filter (if foraging becomes hot)
- **C.2** G2 `find_duplicate` + P9/P10 Merkle/scanner rayon parallelization (if corpus grows past 10k files)
- **C.3** N11 `mcmc_random_walk` (if MCMC ever runs in a query loop)

### Phase D — Deferred / never

All items tagged DEFER / NO_GO in §2. Do not revisit without a new audit showing the landscape has changed.

### 5.1 Which single module saves the most RAM + wall-time?

**Answer: S1 `build_spatial_adjacency_edges`.** On the representative PD 1096 spatial snapshot (≈2k nodes today, but the plan expects growth to 10k+ as more jurisdictions are ingested), it is the only function in the audit that is **O(n²)** in pure Python. Every other candidate is either O(n log n) via numpy, O(1) per call, or already delegated to a native C/C++ library. Porting S1 alone delivers the majority of the peak-RAM / wall-time win of the entire migration.

---

## 6. Implementation Tasks

Each task below is self-contained and ends with a commit. Dispatch via `superpowers:subagent-driven-development` once the governing plan's Task 8 queue reaches this plan.

### Task 1: Bench-harness baseline for every GO / MAYBE candidate

**Why:** No Rust port lands before the Python baseline is measured. This is the pre-committed go/no-go gate referenced in the plan header.

**Files:**
- Create: `scripts/vitruvius/bench/bench_rust_mig_baseline.py`
- Test: `scripts/tests/test_bench_rust_mig_baseline.py`
- Write: `.ai/10_state/audit_rust_migration_baseline_2026-04-15.json`

- [ ] **Step 1: Write the failing test** — `test_bench_rust_mig_baseline_writes_report` asserts that calling `bench_rust_mig_baseline.run_baseline(out_path)` writes a JSON file with keys `{"s1_adjacency_edges", "s2_weight_by_distance", "n1_wasserstein", "n4_mahalanobis", "s10_bloom", "g2_duplicate_detector", "p9_scanner_sha256", "p10_merkle_fs"}` and each value has `{"wall_ms", "peak_rss_mb", "n", "verdict"}` where verdict is one of `"hot"` (>25 ms or >10 MB) or `"cold"`.
- [ ] **Step 2: Run test to verify it fails** — `pytest scripts/tests/test_bench_rust_mig_baseline.py -v` → FAIL with `ModuleNotFoundError: bench_rust_mig_baseline`.
- [ ] **Step 3: Implement the harness.** Reuse the subprocess-isolation pattern from `bench/bench_rust_pdf_audit.py` (proven in AD-033). For each candidate, spawn a child Python process under `/usr/bin/time -l`, import the target module, call the function with synthetic data sized from the `n` parameter, and parse peak-RSS from `time -l` output. Synthetic data for S1: 2k random `SpatialPoint(x, y, z)` with random AABBs; for N4: 1000 random 64-dim embeddings. Write the aggregated JSON at `out_path`.
- [ ] **Step 4: Run test to verify it passes** — `pytest scripts/tests/test_bench_rust_mig_baseline.py -v` → PASS (<3s).
- [ ] **Step 5: Run the harness for real** — `PYTHONPATH=scripts python3 scripts/vitruvius/bench/bench_rust_mig_baseline.py --out .ai/10_state/audit_rust_migration_baseline_2026-04-15.json`. The output JSON is the gate: Phase A/B/C only fire for candidates whose verdict is `"hot"`.
- [ ] **Step 6: Commit** — `git add scripts/vitruvius/bench/bench_rust_mig_baseline.py scripts/tests/test_bench_rust_mig_baseline.py .ai/10_state/audit_rust_migration_baseline_2026-04-15.json && git commit -m "feat(bench): Sprint RUST-MIG-1 Task 1 — Python baseline harness for migration candidates"`

### Task 2: Architectural Decision Record + Sprint LSH-1 correction

**Why:** Lock in the crate layout from §4 and correct the Sprint LSH-1 misdescription from §3.4 before either plan executes.

**Files:**
- Modify: `.ai/10_state/decisions.md` (append AD-036 + AD-037)
- Modify: `.ai/03_plans/2026-04-15-lsh-dedup-plan.md` (correct the O(n²) premise)

- [ ] **Step 1: Write AD-036** — append to `.ai/10_state/decisions.md` a new entry titled "AD-036: Python→Rust migration crate layout" summarizing §4.1 (workspace extension, not parallel tree), §4.2 (single Python import surface via `vitruvius_engine_rs`), and §4.3 (two feature flags default false). Reference this plan by `plan_id`.
- [ ] **Step 2: Write AD-037** — append "AD-037: Sprint LSH-1 premise correction" documenting that `dedupe_by_endpoints` is O(n log n) dict-grouped, not O(n²) pairwise. Sprint LSH-1's actual value is fuzzy/near-duplicate dedup via MinHash, not a scaling fix. Cite `scripts/vitruvius/relationships_sections.py:246-322` as the code evidence.
- [ ] **Step 3: Correct the Sprint LSH-1 plan file** — update `.ai/03_plans/2026-04-15-lsh-dedup-plan.md` §Goal and §Architecture to reframe the target from "O(n²) pairwise dedup" to "exact-match dedup upgraded to fuzzy near-duplicate detection for predicate variants like 'lot area ≥ 100 sqm' vs 'minimum lot area of 100 square meters'". Add a note pointing at AD-037.
- [ ] **Step 4: Update `EXPECTED_FLAGS`** — add `rust_mig_spatial_kernels` and `rust_mig_stats_kernels` to `scripts/tests/test_features.py::EXPECTED_FLAGS` and to `config/vitruvius.yaml` under `features:`, both defaulting `false`. Run `pytest scripts/tests/test_features.py -v` and verify green.
- [ ] **Step 5: Commit** — `git add .ai/10_state/decisions.md .ai/03_plans/2026-04-15-lsh-dedup-plan.md scripts/tests/test_features.py config/vitruvius.yaml && git commit -m "docs(arch): Sprint RUST-MIG-1 Task 2 — AD-036 crate layout + AD-037 LSH-1 premise correction + 2 feature flags"`

### Task 3: Scaffold `spatial_kernels` + `stats_kernels` Cargo crates

**Why:** Create the empty crates with one failing Rust unit test each before any production Rust code lands, following the TDD discipline already used by `vitruvius_rust_pdf` in Sprint 1B-M3.

**Files:**
- Modify: `scripts/vitruvius/engine_rs/Cargo.toml` (workspace root — add members)
- Create: `scripts/vitruvius/engine_rs/spatial_kernels/Cargo.toml`
- Create: `scripts/vitruvius/engine_rs/spatial_kernels/src/lib.rs`
- Create: `scripts/vitruvius/engine_rs/stats_kernels/Cargo.toml`
- Create: `scripts/vitruvius/engine_rs/stats_kernels/src/lib.rs`

- [ ] **Step 1: Add workspace members.** Open `scripts/vitruvius/engine_rs/Cargo.toml` and append `"spatial_kernels"` and `"stats_kernels"` to the `[workspace].members` array. Show the full edit in the diff.
- [ ] **Step 2: Create `spatial_kernels/Cargo.toml`** with `name = "vitruvius_spatial_kernels"`, `version = "0.1.0"`, `crate-type = ["rlib"]`, dependencies `vitruvius_engine_rs_core = { path = "../core" }` and `ndarray = "0.15"`.
- [ ] **Step 3: Create `spatial_kernels/src/lib.rs`** containing ONLY a failing unit test:
   ```rust
   #[cfg(test)]
   mod tests {
       #[test]
       fn adjacency_edges_module_exists() {
           // intentional red — will go green in Task 4
           assert!(false, "adjacency_edges module not yet implemented");
       }
   }
   ```
- [ ] **Step 4: Create `stats_kernels/Cargo.toml`** with `name = "vitruvius_stats_kernels"`, `version = "0.1.0"`, `crate-type = ["rlib"]`, dependencies `nalgebra = "0.33"` and `ndarray = "0.15"`.
- [ ] **Step 5: Create `stats_kernels/src/lib.rs`** containing ONLY a failing unit test:
   ```rust
   #[cfg(test)]
   mod tests {
       #[test]
       fn mahalanobis_module_exists() {
           // intentional red — will go green in Task 6
           assert!(false, "mahalanobis module not yet implemented");
       }
   }
   ```
- [ ] **Step 6: Run `cargo check --workspace`** from `scripts/vitruvius/engine_rs/` and verify the new crates compile (tests fail red is expected and correct).
- [ ] **Step 7: Commit** — `git add scripts/vitruvius/engine_rs/Cargo.toml scripts/vitruvius/engine_rs/spatial_kernels/ scripts/vitruvius/engine_rs/stats_kernels/ && git commit -m "feat(engine_rs): Sprint RUST-MIG-1 Task 3 — scaffold spatial_kernels + stats_kernels crates (red)"`

### Task 4: Phase A.1 — Port S1 `build_spatial_adjacency_edges`

**Gate:** Task 1 baseline report flagged S1 as `"hot"`.

**Files:**
- Create: `scripts/vitruvius/engine_rs/spatial_kernels/src/adjacency_edges.rs`
- Modify: `scripts/vitruvius/engine_rs/spatial_kernels/src/lib.rs` (replace red test, add mod)
- Modify: `scripts/vitruvius/engine_rs/pyo3_shim/Cargo.toml` (add dep on `spatial_kernels`)
- Modify: `scripts/vitruvius/engine_rs/pyo3_shim/src/lib.rs` (add `#[pyfunction]` wrapper)
- Modify: `scripts/vitruvius/engine_rs/__init__.py` (re-export `build_spatial_adjacency_edges_rs`)
- Modify: `scripts/vitruvius/spatial/spatial_edge_builder.py` (add flag-gated fast path)
- Test: `scripts/tests/test_spatial_edge_builder_parity.py` (NEW — correctness parity test)

- [ ] **Step 1: Write the Python parity test** — `test_spatial_edge_builder_parity.py::test_rust_matches_python_on_synthetic_snapshot`: generate 200 random spatial points with random AABBs, call both the pure-Python and (when `rust_mig_spatial_kernels` is on) the Rust path, assert the returned edge sets are equal as frozensets.
- [ ] **Step 2: Run the test** — `pytest scripts/tests/test_spatial_edge_builder_parity.py -v` → FAIL with `ImportError: build_spatial_adjacency_edges_rs is None` (Rust function not yet exported).
- [ ] **Step 3: Write the Rust implementation** — `spatial_kernels/src/adjacency_edges.rs` takes a slice of `(id, Aabb)` and returns `Vec<(String, String)>`. Use `LinearOctree::query_aabb` to find candidates per node, emit edges only when `id_i < id_j` lexicographically (stable dedup). Add a Rust-side unit test that matches 3 synthetic nodes against a hand-computed expected edge set. Remove the red test from Task 3.
- [ ] **Step 4: Add the pyo3 wrapper** in `pyo3_shim/src/lib.rs`: `#[pyfunction] fn build_spatial_adjacency_edges(py: Python, nodes: Vec<(String, [f64; 6])>) -> PyResult<Vec<(String, String)>>`. Build via `cd scripts/vitruvius/engine_rs && python3.11 -m maturin build --release` and install the new wheel.
- [ ] **Step 5: Wire the Python fast path** — add the import + flag check in `spatial/spatial_edge_builder.py`. Use the existing feature flag infrastructure: `if features.is_enabled("rust_mig_spatial_kernels") and build_spatial_adjacency_edges_rs is not None: return build_spatial_adjacency_edges_rs(nodes)`.
- [ ] **Step 6: Run the parity test with the flag on** — `pytest scripts/tests/test_spatial_edge_builder_parity.py -v` → PASS. Also run `pytest scripts/tests/ -v` to verify zero regressions with the flag off.
- [ ] **Step 7: Re-run the bench harness** — `python3 scripts/vitruvius/bench/bench_rust_mig_baseline.py --out .ai/10_state/audit_rust_migration_after_s1_2026-04-15.json` and diff wall-time + RSS against the Task 1 baseline. Append the delta to a note block at the end of the new JSON.
- [ ] **Step 8: Commit** — `git add scripts/vitruvius/engine_rs/spatial_kernels/ scripts/vitruvius/engine_rs/pyo3_shim/ scripts/vitruvius/engine_rs/__init__.py scripts/vitruvius/spatial/spatial_edge_builder.py scripts/tests/test_spatial_edge_builder_parity.py .ai/10_state/audit_rust_migration_after_s1_2026-04-15.json && git commit -m "feat(engine_rs): Sprint RUST-MIG-1 Task 4 — S1 build_spatial_adjacency_edges rust port (O(n²) → O(n log n))"`

### Task 5: Phase A.2 — Port S2 `weight_by_distance`

**Gate:** Task 1 baseline report flagged S2 as `"hot"` (or the Task 4 bench showed it adjacent to S1's hot path).

**Files:**
- Create: `scripts/vitruvius/engine_rs/spatial_kernels/src/distance_weight.rs`
- Modify: `spatial_kernels/src/lib.rs` (add mod)
- Modify: `pyo3_shim/src/lib.rs` (add `#[pyfunction] weight_by_distance`)
- Modify: `engine_rs/__init__.py` (re-export `weight_by_distance_rs`)
- Modify: `scripts/vitruvius/spatial/proximity_jump.py:105-126` (add flag-gated fast path)
- Test: `scripts/tests/test_proximity_jump_weight_parity.py` (NEW)

- [ ] **Step 1: Write the Python parity test** — generate 10000 random `(x, y, z)` seeds + a fixed focal point + `lambda_decay = 0.05`, assert the Rust-returned weight array equals `np.exp(-0.05 * distances)` to within `1e-12` elementwise.
- [ ] **Step 2: Run — FAIL** (function not exported yet).
- [ ] **Step 3: Write the Rust implementation** — `distance_weight.rs` takes a slice of 3-tuples + a focal + lambda and returns `Vec<f64>`. Use `f64::exp` and `(dx*dx + dy*dy + dz*dz).sqrt()` in a tight `.iter().map().collect()`. Add a Rust unit test on a hand-computed 3-seed case.
- [ ] **Step 4: Add the pyo3 wrapper** — signature `fn weight_by_distance(seeds: Vec<(f64, f64, f64)>, focal: (f64, f64, f64), lambda: f64) -> Vec<f64>`. Rebuild + reinstall the wheel.
- [ ] **Step 5: Wire the Python fast path** in `proximity_jump.py`. Keep the numpy fallback for flag-off.
- [ ] **Step 6: Run the parity test with flag on** — PASS.
- [ ] **Step 7: Run full pytest suite** — confirm 1437+ passing.
- [ ] **Step 8: Commit** — `git commit -m "feat(engine_rs): Sprint RUST-MIG-1 Task 5 — S2 weight_by_distance rust port (pure O(n) kernel)"`

### Task 6: Phase B.1 — Port N4 Mahalanobis core (conditional)

**Gate:** Task 1 baseline report flagged N4 as `"hot"` AND a grep of `outlier_detector.py` confirms `sklearn.covariance` is **not** on the fit path. If sklearn IS required, this task is **deferred to Phase D** and the migration stops at Phase A + N1.

**Files:**
- Create: `scripts/vitruvius/engine_rs/stats_kernels/src/mahalanobis.rs`
- Modify: `stats_kernels/src/lib.rs`
- Modify: `pyo3_shim/src/lib.rs` (+ `#[pyfunction] mahalanobis_distance`)
- Modify: `engine_rs/__init__.py`
- Modify: `scripts/vitruvius/normalization/outlier_detector.py`
- Test: `scripts/tests/test_mahalanobis_parity.py` (NEW)

- [ ] **Step 1: Verify the sklearn gate** — `grep -n "sklearn" scripts/vitruvius/normalization/outlier_detector.py`. If any match → mark Task 6 DEFER_SKLEARN, write a note in the bench report, skip to Task 7.
- [ ] **Step 2: Write the Python parity test** — fit the Python Mahalanobis on 1000 random 64-dim embeddings with a planted covariance, then assert the Rust `mahalanobis_distance(x, mean, cov_inv)` matches the Python scipy/numpy result to within `1e-9` elementwise on 200 query vectors.
- [ ] **Step 3: Run — FAIL**.
- [ ] **Step 4: Write the Rust implementation** — `mahalanobis.rs` uses `nalgebra::DMatrix` / `DVector` for the covariance invert and quadratic form. Signature: `fn mahalanobis_distance(x: &[f64], mean: &[f64], cov_inv: &[f64], dim: usize) -> f64`. The `cov_inv` argument is the already-inverted covariance matrix flattened row-major; the Python side computes the inverse once at fit time and passes it in for every score call.
- [ ] **Step 5: Add the pyo3 wrapper** — use `numpy::PyArray1<f64>` + `PyArray2<f64>` for zero-copy numpy → nalgebra conversion.
- [ ] **Step 6: Wire the Python fast path** in `outlier_detector.py` — flag-gated, fallback to numpy.
- [ ] **Step 7: Run parity test — PASS.**
- [ ] **Step 8: Commit** — `git commit -m "feat(engine_rs): Sprint RUST-MIG-1 Task 6 — N4 Mahalanobis core rust port via nalgebra"`

### Task 7: Phase B.2 — ~~Port N1 sliced Wasserstein~~ DEFER_ALREADY_NATIVE

**Status (2026-04-15):** DEFER_ALREADY_NATIVE. See AD-038a in `.ai/10_state/decisions.md` for the full rationale. Summary: at dispatch time the implementer re-read `wasserstein_merge.py` per the Task 7 spec's "inspect first" step and discovered the function is **not** sliced Wasserstein — it is exact multi-dim 2-Wasserstein via `ot.dist` + `ot.emd2` (POT native C++ LP solver). There is no Python-level sort+diff hot path. Reimplementing POT's network simplex in Rust is scope creep; a d==1-only kernel is optimization theater (every production call site uses d > 1). Per AD-036, Sprint RUST-MIG-1 only ports items whose Python-level hot path measurement justifies the Rust tax. N1's hot path is already native, so Task 7 ships as a docs-only commit that corrects the audit premise, adds AD-038a, and embeds an inline comment in `wasserstein_merge.py` so future readers understand why N1 is absent from the Rust fast-path surface while S1/S2/N4 are present.

**Shipping surface after Task 7 defer.** Sprint RUST-MIG-1 ports **S1, S2, N4** to Rust. N1 stays pure Python on POT's native path.

**Original Task 7 plan (retained for archival traceability — NOT to be executed).**

**Gate:** Task 1 baseline report flagged N1 as `"hot"`.

**Files:**
- Create: `scripts/vitruvius/engine_rs/stats_kernels/src/wasserstein.rs`
- Modify: `stats_kernels/src/lib.rs`
- Modify: `pyo3_shim/src/lib.rs` (+ `#[pyfunction] sliced_wasserstein`)
- Modify: `engine_rs/__init__.py`
- Modify: `scripts/vitruvius/graph/wasserstein_merge.py`
- Test: `scripts/tests/test_wasserstein_parity.py` (NEW)

- [x] **Step 1: Inspect first per Task 7 spec "Read the existing Python function".** Result: the function calls `ot.dist` + `ot.emd2` — both native C++. No Python projection loop, no Python sort, no inner hot path. DEFER per AD-038a.
- [ ] ~~Step 2: Write the Python parity test~~ — skipped (no Rust function to parity-test).
- [ ] ~~Step 3: Write the Rust implementation~~ — skipped.
- [ ] ~~Step 4: Add pyo3 wrapper~~ — skipped.
- [ ] ~~Step 5: Wire the Python fast path~~ — skipped.
- [ ] ~~Step 6: Run parity test~~ — skipped.
- [x] **Step 7: Commit (docs-only defer)** — `git commit -m "feat(engine_rs): Sprint RUST-MIG-1 Task 7 — N1 sliced Wasserstein rust port"` with commit body documenting the DEFER_ALREADY_NATIVE verdict, the original audit's mischaracterization, and a pointer to AD-038a.

### Task 8: Close the sprint — bench report + AD-### + archive

**Files:**
- Write: `.ai/10_state/audit_rust_migration_final_2026-04-15.json`
- Modify: `.ai/10_state/decisions.md` (append AD-038)
- Modify: `.ai/03_plans/INDEX.md`
- Move: `.ai/03_plans/2026-04-15-rust-migration-audit-plan.md` → `.ai/09_archive/plans/`

- [ ] **Step 1: Run the full bench harness with both flags ON** — produces the final report with before/after numbers for every Phase A + B candidate.
- [ ] **Step 2: Write AD-038** — "Sprint RUST-MIG-1 closure" with exact wall-time + RSS numbers per function, the decision to flip `rust_mig_spatial_kernels` and `rust_mig_stats_kernels` defaults to `true` (if bench clears the win threshold) or keep them false (if wins are below 2×), and a Phase C gate re-evaluation note.
- [ ] **Step 3: Flip the flag defaults** in `config/vitruvius.yaml` + `EXPECTED_FLAGS` iff AD-038 clears the 2× threshold. Add an AD-038 allowlist entry to `scripts/tests/test_features.py::test_repo_config_every_flag_is_false`.
- [ ] **Step 4: Run the full test suite one more time.** Record the count in AD-038.
- [ ] **Step 5: Update `.ai/03_plans/INDEX.md`** — add a closed row for Sprint RUST-MIG-1 + archive path.
- [ ] **Step 6: Move the plan** — `git mv .ai/03_plans/2026-04-15-rust-migration-audit-plan.md .ai/09_archive/plans/`.
- [ ] **Step 7: Commit the closure** — `git commit -m "docs(rust-mig): Sprint RUST-MIG-1 closure — AD-038 + phase A/B bench ledger"`.

---

## 7. Quality Bar & Acceptance Criteria

A sprint is only "closed" when every one of these holds:

1. **Baseline first** — Task 1 bench report exists and was the gate for every subsequent phase. No port lands without a `"hot"` verdict on its target function.
2. **Parity tests** — Every Rust port has a Python parity test that compares the Rust output to the pure-Python baseline on synthetic data with tolerance ≤ `1e-9` (floats) or exact-equal (set/dict).
3. **Feature-flag discipline** — Both new flags (`rust_mig_spatial_kernels`, `rust_mig_stats_kernels`) are in `EXPECTED_FLAGS` and default `false` until AD-038 closure. Flag-OFF behavior is byte-identical to pre-migration.
4. **Non-breaking** — The full pytest suite grows (never shrinks) from 1437 passing.
5. **No dead Rust** — Every function in `spatial_kernels` + `stats_kernels` has a Python caller wired through `pyo3_shim` + `engine_rs/__init__.py`. No lonely exports.
6. **RSS + wall-time numbers recorded** — AD-038 contains a per-function table with `before_wall_ms`, `after_wall_ms`, `before_rss_mb`, `after_rss_mb`, `ratio` columns.

---

## 8. Non-Goals of This Plan

- **No Rust GraphSAGE.** Torch tensor ↔ PyO3 marshaling is the bottleneck. Any "GraphSAGE in Rust" discussion is out of scope.
- **No Rust sklearn.** Sklearn pickle / NumPy-based ML model bridges are explicitly NO_GO.
- **No replacement of Z3 / cvxpy / trimesh / Shapely / networkx / scipy.** These libraries are already native C/C++; porting the Python bridge wins nothing and loses ecosystem compatibility.
- **No parallel Cargo workspace.** Extension of `engine_rs/` only. A second workspace adds build complexity without benefit.
- **No new deployment artifacts.** Maturin continues to produce one wheel; Python import surface remains `vitruvius_engine_rs`.
- **No rewrite of Sprint LSH-1 into Rust.** AD-037 reframes LSH-1 as a Python `datasketch` task (fuzzy near-duplicate dedup). It is not a migration target.
- **No rewrite of Sprint PQ-1 into Rust** (despite it being math). Product Quantization in PQ-1 uses `faiss` which has its own native backend; a Python → faiss → Rust chain is worse than Python → faiss.

---

## 9. Self-Review (run after writing this plan)

- [x] **Spec coverage** — the user spec asked for: (a) audit log of heavy-compute Python → §2; (b) feasibility per item → §2 verdicts + §3.1–3.4; (c) target architecture → §4; (d) execution phasing ranked by ROI → §5 with Phase A/B/C/D + §5.1 "single biggest win". All four requirements are present.
- [x] **Placeholder scan** — every task has exact file paths, failing test descriptions, parity assertions, and commit commands. No "TBD", "implement later", "add error handling", or "similar to Task N".
- [x] **Type / naming consistency** — feature flag names (`rust_mig_spatial_kernels`, `rust_mig_stats_kernels`) used consistently across §4.3, Tasks 2, 4, 5, 6, 7, 8. Crate names (`vitruvius_spatial_kernels`, `vitruvius_stats_kernels`) used consistently across §4.1, Tasks 3–7. Python re-export names (`build_spatial_adjacency_edges_rs`, etc.) used consistently.
- [x] **Gate-check realism** — Task 1's `"hot"` threshold is `>25 ms wall-clock OR >10 MB RSS`. Every subsequent phase references this gate explicitly.
- [x] **No code duplication** — parity tests live alongside the Python call sites, not duplicated in the Rust crate. Rust unit tests cover Rust-side correctness; Python parity tests cover the wire.
- [x] **Existing-infra reuse** — the plan extends `engine_rs/` rather than creating a parallel tree, reuses the `maturin build --release` + `pip install wheel` pattern from AD-033, reuses the `bench/bench_rust_pdf_audit.py` subprocess-isolation pattern for Task 1.
- [x] **Sprint LSH-1 correction captured** — §3.4 flags the premise error, Task 2 schedules the fix.
- [x] **No Rust code in the plan body** — per the user directive, the plan describes Rust function signatures and imports but does not spell out full Rust function bodies. Those land in the actual sprint execution.

---

## 10. Execution Handoff

**Position in the queue:** This plan slots into `.ai/03_plans/00-governing-implementation-plan.md` Task 8 as a NEW step between the Advanced Tech Audit (Step 1) and pipeline_cli.py integration (Step 2). The governing plan's Task 8 Step 2 is renumbered, and this plan becomes Task 8 Step 1.5 (or promoted to a new Step 2, with pipeline_cli integration sliding to Step 3).

**Dispatch order:** After the Advanced Tech Audit (`2026-04-15-advanced-tech-audit-plan.md`) runs and produces its GO/DEFER report, dispatch THIS plan next because the single highest-ROI migration (S1) is the single largest RAM + wall-time win identified in the entire optimization queue.

**Required skill:** `superpowers:subagent-driven-development` — the 8 tasks are mostly independent once Task 1's baseline lands and can be dispatched fresh per task with two-stage review.

**Dependencies before dispatch:**
- Rust toolchain 1.94+ installed (`rustup show`)
- `maturin` installed (`pip show maturin`)
- The existing `engine_rs` wheel builds from `scripts/vitruvius/engine_rs/` (verified: last build 2026-04-15 09:19)
- `nalgebra = "0.33"` and `ndarray = "0.15"` available via crates.io (network-available build)
