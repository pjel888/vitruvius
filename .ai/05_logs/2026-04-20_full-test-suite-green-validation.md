# Validation Report: Full Test Suite Green

**Date:** 2026-04-20  
**Commits:** `ab831ff`, `5da0061`  
**Scope:** Entire `scripts/tests/` suite  
**Result:** 2153 passed, 14 skipped, 5 warnings, 0 failures

---

## Summary

Resolved 6 categories of latent test failures across the suite. The failures were a mix of:
- Test fixture typos (`\\n` vs `\n`)
- Outdated assertions from before feature additions
- Incomplete data migrations (missing `stringency_vector`)
- Type mismatches between PostgreSQL `datetime` and Pydantic `str`
- Test isolation issues (stale database state)
- Assertion target mismatches (stdout vs stderr)

---

## Fixes Applied

### 1. PD-957/PD-1185 Source Admission — Escaped Newlines
**File:** `scripts/tests/test_dataset_pipeline_cli.py`  
**Root cause:** String literals used `\\n` (literal backslash-n) instead of `\n` (newline). `extract_title_from_content` included the trailing backslash in the extracted title; `slugify` converted it to `-n`, producing filenames like `revised-implementing-rules-and-regulations-for-pd-957-n.md`.  
**Fix:** Replaced `\\n` with `\n` in 3 payload strings.

### 2. Canonicalize Body — Outdated Title Assertion
**File:** `scripts/tests/test_canonicalize_body.py`  
**Root cause:** Test predated `extract_title_from_content` (commit `fe72db2`). After that feature, the extracted title legitimately appears in frontmatter and H1. The assertion `assert 'Revised Implementing Rules and Regulations' not in content` became invalid.  
**Fix:** Removed the outdated assertion. Structural header filtering is still validated by the remaining assertions.

### 3. Concept Stringency Migration — 24 Missing Vectors
**Files:** `003_Canonical-Knowledge-Layer/shared/concepts/*.md` (24 files)  
**Root cause:** Stream W3.1 migration test enforced `stringency_vector` on every concept file, but 24 descriptive/theory concepts never received it.  
**Fix:** Added `stringency_vector: qualitative` to all 24 missing concept files.

### 4. Evidence Ingestor — Idempotent Path Type Mismatch
**File:** `scripts/vitruvius/kg/evidence_ingestor.py`  
**Root cause:** `DocumentVersion.created_at` is typed `str`, but PostgreSQL `dict_row` returns `datetime` objects for timestamp columns. The idempotent ingest path (`existing` → `model_validate`) crashed with Pydantic validation error.  
**Fix:** Convert `datetime` to ISO string before `model_validate` in the idempotent path.

### 5. Evidence Ingestor — Test Isolation
**File:** `scripts/tests/test_evidence_ingestor.py`  
**Root cause:** `test_ingest_markdown` used deterministic content, so stale Postgres data from previous runs caused it to hit the idempotent path. Neo4j was reset but Postgres was not, so the Neo4j query returned no results.  
**Fix:** Added `TRUNCATE TABLE document_version CASCADE` at the start of `test_ingest_markdown`.

### 6. Graph Visualize CLI — Stdout vs Stderr
**File:** `scripts/tests/test_graph_visualize_cli.py`  
**Root cause:** The `visualize-graph` command outputs JSON errors to stdout, not stderr. The test asserted on `stderr`.  
**Fix:** Changed assertion to check `result.stdout`.

### 7. Wiring E2E — Concept Filtering Baseline
**File:** `scripts/tests/test_wiring_e2e.py`  
**Root cause:** `build_snapshot` filters out concepts that have no incident edges and no `regulatory_basis`. The minimal corpus concept (`setbacks`) was filtered, reducing `node_count` from expected 2 to 1.  
**Fix:** Added `regulatory_basis: [law-pd-1096]` to the concept fixture so it is retained in the snapshot.

---

## Validation

```bash
python3 -m pytest scripts/tests/ --tb=short
```

Result:
- **2153 passed**
- **14 skipped**
- **5 warnings** (unrelated SWIG deprecation warnings)
- **0 failures**

---

## Impact

- **Production code changes:** 1 file (`evidence_ingestor.py`) — minimal defensive conversion
- **Test code changes:** 5 files
- **Data layer changes:** 24 concept files
- **Blast radius:** Low — all changes are test-hardening, data-migration completion, or defensive type handling
- **Risk:** None
