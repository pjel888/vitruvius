# Vitruvius — Codebase Optimization Audit

**Date:** 2026-04-19  
**Auditor:** Codebase agent (automated + manual verification)  
**Scope:** `scripts/vitruvius/` (236 Python files, ~44,500 LOC), `scripts/pipeline_cli.py`, `scripts/tests/`  
**Method:** Import-time profiling, dead-code analysis, duplicate-function detection, regex compilation audit, test runtime analysis, Rust kernel verification  
**Baseline:** 2044 passed, 17 skipped, 7 pre-existing unrelated failures; full suite in 60.2s

---

## 1. Executive Summary

**Verdict: HEALTHY with minor optimization opportunities.**

The codebase is well-architected for performance:
- Lazy CLI imports are correctly implemented (0.03s `pipeline_cli.py` import)
- All 3 Rust polyglot kernels are built, available, and enabled by default
- RocksDB backends are live-by-default and measured 18.7×/24.3× faster than SQLite
- Module-level regex compilation dominates (85 module-level vs 16 function-level)
- Feature-flag framework keeps 100+ advanced modules off the critical path

**No critical performance issues found.** The remaining opportunities are low-risk refactors and test-suite hygiene.

---

## 2. Import Time Analysis

| Module | Import Time | Assessment |
|---|---|---|
| `pipeline_cli.py` | 0.03s | ✅ Excellent — lazy imports verified |
| `vitruvius.scanner` | 0.06s | ✅ Fast |
| `vitruvius.conversion` | 0.12s | ✅ Acceptable |
| `vitruvius.canonicalize` | <0.01s | ✅ Fast |
| `vitruvius.ollama_review` | 0.04s | ✅ Fast |
| `vitruvius.graph.physics` | 0.25s | ⚠️ Slow — imports numpy/scipy/networkx at module level. However, **gated by `features.phys_*` flags** in all callers, so it never loads on the default path. |
| `vitruvius.parsers.factory` | 0.30–0.40s | ⚠️ Slowest. Does lazy imports inside `build_default_orchestrator()`, but the module-level import of `vitruvius.parsers.orchestrator` and `vitruvius.parsers.base_parser` still pulls the parser ecosystem. |
| `vitruvius.kg.*` modules | <0.02s each | ✅ Fast — Pydantic models, no heavy deps |

**Observation:** The only slow imports are behind feature flags or on non-default code paths. The default `run`/`scan`/`convert` pipeline loads in well under 0.5s total.

---

## 3. Hotspot Analysis

### 3.1 O(n²) Python Loops (with Rust Escape Hatches)

| Location | Pattern | Rust Override | Status |
|---|---|---|---|
| `spatial/spatial_edge_builder.py:164` | Nested AABB intersection loop | `build_spatial_adjacency_edges_rs` | ✅ Rust path active (200× speedup, flag `rust_mig_spatial_kernels: true`) |
| `spatial/proximity_jump.py` | Distance-weighted edge decay | `weight_by_distance_rs` | ✅ Rust path active (12.18× speedup, flag `rust_mig_spatial_kernels: true`) |
| `normalization/outlier_detector.py` | Mahalanobis distance | `mahalanobis_distance_rs` | ✅ Rust path active (2.73× speedup, flag `rust_mig_stats_kernels: true`) |
| `kg/merge_adjudicator.py:53` | Pairwise exact-match dedup | None | ⚠️ O(n²) on group size. Groups are typically small (<20), but large batches could be slow. Consider LSH or sorting pre-pass if batch sizes grow. |

**Verdict:** The three performance-critical kernels are already ported to Rust. The remaining O(n²) loop (`merge_adjudicator`) operates on small groups and is not a current bottleneck.

### 3.2 Regex Compilation

- **Module-level (good):** 85 instances — compiled once at import time
- **Function-level (suboptimal):** 16 instances — recompiled on every call

**Function-level candidates for hoisting:**
- `canonical_diff.py:66` — compiles patterns inside a function from `VOLATILE_FIELDS`
- `canonicalize.py:339-340` — two patterns compiled inside `extract_section_title()`
- `promotion/__init__.py` — `slugify()` compiles regex on every call
- `concepts/__init__.py` — `slugify()` compiles regex on every call

**Impact:** Low. These are not on the hot path of the default pipeline. But hoisting them is a trivial win.

### 3.3 File I/O Patterns

- **98 file-read call sites** across the codebase
- **59 JSON parse call sites**
- Config loading uses `lru_cache` in `_load_features_cached()` — ✅ correct
- No repeated reading of the same large file detected in hot paths

---

## 4. Code Duplication

### 4.1 Utility Functions (3+ copies)

| Function | Copies | Locations | Recommendation |
|---|---|---|---|
| `slugify()` | 3 | `canonicalize.py`, `concepts/__init__.py`, `promotion/__init__.py` | Extract to `utils.py` |
| `normalize_text()` | 2 | `utils.py`, `relationships_sections.py` | Use `utils.normalize_text` in relationships_sections |
| `get_ollama_url()` | 3 | `config.py`, `discovery_weaver.py`, `identity_provisioner.py` | Use `config.get_ollama_url` in the weaver/provisioner modules |
| `get_ollama_default_model()` | 3 | `config.py`, `discovery_weaver.py`, `identity_provisioner.py` | Same as above |
| `utc_now_stamp()` | 3 | `utils.py`, `discovery_weaver.py`, `identity_provisioner.py` | Same as above |

### 4.2 Interface Pattern Duplicates (expected)

Multiple modules define `close()`, `count()`, `parse()`, `write_snapshot()` — this is the expected interface pattern for pluggable backends (SQLite ↔ RocksDB, v1 ↔ v2 builders, etc.). These are **not debt**.

---

## 5. Dead Code Candidates

Functions defined but never called in tests or main code paths:

| Function | Module | Risk | Action |
|---|---|---|---|
| `is_kg_enabled()` | `config.py` | Low | Used only when KG flags are queried; may be called by future CLI handlers |
| `is_kg_assertion_layer()` | `config.py` | Low | Same as above |
| `get_kg_neo4j_uri()` | `config.py` | Low | Used when Neo4j backend is enabled |
| `add_candidates()` | `kg/canonical_graph_builder.py` | Low | Graph builder API surface; may be used by future callers |
| `n_entities()`, `n_relations()` | `extraction/kg_link_predictor.py` | Low | Helper properties on link predictor; may be used by downstream eval |
| `is_line_inside_table()` | `normalization/table_detector.py` | Medium | Defined but no callers found. May be stale from Tier C table work. |

**Verdict:** No urgent dead code to remove. Most "unused" functions are API surface area for future callers or feature-flag-gated paths.

---

## 6. Test Suite Performance

**Full suite:** 2044 passed, 17 skipped in **60.2 seconds**

### 6.1 Slowest Tests

| Test | Time | Root Cause |
|---|---|---|
| `test_embedding_chunker.py::test_each_chunk_has_384_dim_vector` | 6.76s (setup) | Loads `nomic-embed-text` model into memory |
| `test_ollama_retry.py::test_falls_back_to_review_further_after_all_retries` | 6.01s | 3 retries × 2s backoff = enforced wait |
| `test_ollama_retry.py::test_retries_up_to_three_times_on_transient_error` | 6.01s | Same retry/backoff logic |
| `test_embedding_chunker.py::test_different_text_produces_different_vectors` | 5.98s | Model loading |
| `test_priming_context_vector.py::test_identity_is_deterministic_for_identical_frontmatter` | 5.92s | Likely Ollama/model call |
| `test_kg_embeddings.py::test_ollama_failure_falls_back` | 5.63s | Ollama timeout fallback |

**Top 6 tests = 36.3s** — that's **60% of total suite time**.

### 6.2 Optimization Opportunities for Tests

1. **Ollama retry tests (12s total)** — Use `pytest.mark.slow` and skip in fast mode. The retry logic is deterministic; mocking the HTTP client would cut these to <0.1s each.
2. **Embedding model loading (12.7s total)** — Load the model once per session with a `pytest.fixture(scope="session")` instead of per-test setup.
3. **Ollama timeout fallback (5.6s)** — Mock the Ollama client; the timeout logic is in the wrapper, not the network layer.

**Estimated speedup if optimized:** 60s → ~35s (**~40% faster suite**).

---

## 7. Dependency & Memory Analysis

### 7.1 Heavy Dependencies (Lazy-Loaded)

| Dependency | Load Cost | Where Loaded | Gated? |
|---|---|---|---|
| `torch` (via sentence-transformers) | ~1GB disk, ~400MB RAM | `concepts/contrastive_adapter.py`, `graph/graphsage.py` | ✅ `features.*` flags |
| `docling` | ~500MB+ | `parsers/docling_parser.py` | ✅ `p1b_docling_parser: false` |
| `spacy` | ~200MB | `extraction/crf_extractor.py` | ✅ `features.e_spacy_svo: false` |
| `rocksdict` | ~50MB | `graph/rocksdb_event_store.py` | ✅ Default true but only on first store access |
| `numpy` | ~50MB | `graph/physics.py`, `graph/pq_codebook.py`, etc. | ✅ Mostly flag-gated |

**Verdict:** No heavy dependency loads on the default pipeline path. The lazy-import discipline is working.

### 7.2 8GB M2 Model Assignment Policy

The `kg_transition` config block explicitly assigns RAM-safe models:

| Task | Model | Peak RAM | Safe? |
|---|---|---|---|
| Embeddings | `nomic-embed-text` | ~0.5 GB | ✅ Yes |
| Classification / JSON extraction | `qwen2.5:3b` | ~1.8 GB | ✅ Yes |
| Complex inference | `llama3.1:8b` | ~5.0 GB | ⚠️ Will swap |
| Synthesis | `gemma4:e4b` | ~6.5 GB | ⚠️ Risky |

The default review pipeline uses `gemma4:31b` (not the e4b variant) which is even larger. The `m2-8gb-safe` preset forces `qwen2.5:7b` (~4.4 GB) for review.

**Recommendation:** Update the default review model for 8GB M2 users, or add a startup warning when `gemma4:31b` is selected on ≤16GB machines.

---

## 8. Optimization Recommendations (Prioritized)

### High Impact / Low Effort

1. **Hoist 16 function-level regex compilations to module level**
   - Files: `canonicalize.py`, `promotion/__init__.py`, `concepts/__init__.py`, `canonical_diff.py`
   - Effort: ~15 minutes
   - Risk: Near zero

2. **Deduplicate `slugify()` into `utils.py`**
   - Replace 3 copies with one canonical implementation
   - Effort: ~10 minutes
   - Risk: Low — function semantics are identical

3. **Mock Ollama retry/timeout tests**
   - Cut 12s from suite time
   - Effort: ~30 minutes
   - Risk: Low — test behavior is deterministic

### Medium Impact / Medium Effort

4. **Session-scoped embedding model fixture**
   - Cut 12.7s from suite time
   - Effort: ~20 minutes
   - Risk: Low — fixture isolation is well-understood

5. **Add `pytest.mark.slow` to integration tests**
   - Allow `pytest -m "not slow"` for 20s feedback loop
   - Effort: ~15 minutes
   - Risk: Near zero

### Low Impact / Future Work

6. **Consider LSH pre-filter for `merge_adjudicator` exact-match dedup**
   - Only matters if batch sizes grow >100
   - Effort: Medium
   - Risk: Low — LSH already ships in `relationships/lsh_dedup.py`

7. **Investigate `parsers.factory` import decomposition**
   - Split factory into sub-factories by document class to reduce import surface
   - Effort: Medium
   - Risk: Medium — touches parser orchestration logic

---

## 9. Blast Radius of Proposed Changes

| Change | Files Touched | Test Impact | Backward Compatibility |
|---|---|---|---|
| Regex hoisting | 4 files | None | ✅ Preserved |
| `slugify` dedup | 3 files + `utils.py` | None | ✅ Preserved |
| Mock retry tests | 2 test files | Faster | ✅ Same assertions |
| Session fixture | 2 test files | Faster | ✅ Same assertions |
| `pytest.mark.slow` | ~10 test files | None | ✅ Optional flag |

**All proposed changes are additive or internal refactor. No API breakage, no feature-flag changes, no schema changes.**

---

## 10. Verified Claims

- [x] Rust kernels available: `build_spatial_adjacency_edges_rs`, `weight_by_distance_rs`, `mahalanobis_distance_rs`
- [x] Rust kernels enabled by default: `rust_mig_spatial_kernels: true`, `rust_mig_stats_kernels: true`
- [x] RocksDB backends enabled by default: `hp_rocksdb_event_store: true`, `hp_rocksdb_verdict_cache: true`
- [x] Lazy imports in `pipeline_cli.py`: verified — 0.03s import time
- [x] Config loading cached: `lru_cache` on `_load_features_cached()`
- [x] No heavy deps on default path: `torch`, `docling`, `spacy` are flag-gated
- [x] Feature flags: 100+ flags, only 4 default to `true`

---

*Audit conclusion: The codebase is performance-healthy. The highest-value optimization is test-suite hygiene (mocking Ollama waits + session-scoped fixtures), which would cut suite time by ~40%. Code-level optimizations (regex hoisting, deduplication) are trivial and low-risk.*
