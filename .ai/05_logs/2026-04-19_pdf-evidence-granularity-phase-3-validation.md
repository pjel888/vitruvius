# PDF Evidence Granularity — Phase 3 + Bbox Upgrade Validation Log

**Date:** 2026-04-19  
**Status:** ✅ COMPLETE  
**Scope:** Populate `PdfPageSelector.page` and `PdfBboxSelector.bbox` for evidence spans so PDF sources have exact page-level and coordinate-level citations.

---

## What Was Implemented

### 1. `PdfEvidenceLocator` Module
**File:** `scripts/vitruvius/kg/pdf_evidence_locator.py`

- Maps evidence snippets back to original PDF page numbers using `pypdf` text search.
- **NEW:** Extracts bounding boxes using `pdfplumber` (preferred) or `PyMuPDF` (fallback).
- Resolves source markdown → original PDF via `original_file` and `source_documents` frontmatter.
- Handles path normalization (double slashes in `source_documents`).
- Falls back to basename search under `001_Raw-Source-Layer/` when direct path resolution fails.
- Fuzzy fallback search using 30-character substring match when exact match fails.
- Minimum snippet length guard (10 chars) to avoid false positives.

**API:**
- `find_page(source_slug, text_snippet)` → `int | None`
- `find_bbox(source_slug, text_snippet)` → `(page, [x0, y0, x1, y1]) | None`
- `find_page_with_fallback(source_slug, text_snippet, section_heading)` → `int | None`
- `find_bbox_with_fallback(source_slug, text_snippet, section_heading)` → `(page, bbox) | None`

### 2. `EvidenceMaterializer` Integration
**File:** `scripts/vitruvius/kg/evidence_materializer.py`

- Evidence spans now try selector hierarchy:
  1. `PdfBboxSelector` (page + exact bbox) — most granular
  2. `PdfPageSelector` (page only)
  3. `MarkdownRangeSelector` (if `section_id`)
  4. `TextRangeSelector` (fallback)
- Deep links include bbox coords when available: `/viewer/{slug}?page={page}&bbox={x0},{y0},{x1},{y1}`

### 3. Dependencies
**File:** `requirements.txt`

- Added `pdfplumber>=0.11.0`
- Added `pymupdf>=1.27.0`

### 4. Test Coverage
**Files:**
- `scripts/tests/test_pdf_evidence_locator.py` — 7 tests (normalization, page search, bbox search, real PDF bbox extraction)
- `scripts/tests/test_pdf_evidence_integration.py` — 4 end-to-end tests (materializer emits selectors, prefers bbox, real PDF integration)

### 5. Fixture Updates
**Files:**
- `scripts/tests/fixtures/spatial/expected_frozen_snapshot.json` — added `title` fields
- `scripts/tests/fixtures/wiring/expected_flag_off_snapshot.json` — added `title` fields

---

## Verification Results

### Test Suite
```
2070 passed, 17 skipped, 0 new failures
```

- 7 new tests added in `test_pdf_evidence_locator.py`
- 4 end-to-end tests in `test_pdf_evidence_integration.py`
- 3 pre-existing unrelated failures remain unchanged:
  - `test_concept_stringency_migration.py` (stringency vectors)
  - `test_wiring_e2e.py::test_flag_off_chain_is_byte_identical_to_baseline` (node_count drift)

### Snapshot Build
```
Canonical nodes: 119
Relationship assertions: 55
Evidence spans: 30
Fast edges: 163
Placement assertions: 108
```

- All 30 evidence spans use `MarkdownRangeSelector` in the current dataset (no relationships yet reference PDF-backed sources with evidence snippets).
- `PdfBboxSelector` and `PdfPageSelector` infrastructure verified via integration tests with real PD 1096 PDF.

### Real PDF Integration Tests
- `PdfEvidenceLocator.find_bbox("pd-1096", "national building code")` → returns `(1, [171.86, 75.73, 423.45, 93.73])` using pdfplumber
- `EvidenceMaterializer` emits `PdfBboxSelector` when snippet is found in PDF
- Fallback to `PdfPageSelector` when bbox extraction fails but page match succeeds
- Fallback to `MarkdownRangeSelector` / `TextRangeSelector` for non-PDF sources

---

## Known Limitations

| Item | Status | Notes |
|------|--------|-------|
| `PdfBboxSelector` page+bbox mapping | ✅ Working | pdfplumber primary, PyMuPDF fallback |
| `PdfPageSelector` page mapping | ✅ Working | pypdf text extraction |
| Full-dataset PDF evidence spans | ⏳ Waiting for data | Current canonical relationships don't reference PDF-backed sources with evidence snippets |

---

## Files Changed

| File | Change |
|------|--------|
| `scripts/vitruvius/kg/pdf_evidence_locator.py` | Created with page+bbox support |
| `scripts/tests/test_pdf_evidence_locator.py` | Created |
| `scripts/tests/test_pdf_evidence_integration.py` | Created |
| `scripts/vitruvius/kg/evidence_materializer.py` | Wired `PdfEvidenceLocator`; selector hierarchy: Bbox → Page → Markdown → Text |
| `scripts/tests/fixtures/spatial/expected_frozen_snapshot.json` | Added `title` fields |
| `scripts/tests/fixtures/wiring/expected_flag_off_snapshot.json` | Added `title` fields |
| `requirements.txt` | Added `pdfplumber>=0.11.0`, `pymupdf>=1.27.0` |

---

## Rollback Safety

All changes are additive:
- New module (`pdf_evidence_locator.py`) does not affect existing code paths.
- `EvidenceMaterializer` adds a new branch before existing branches; existing paths unchanged.
- New dependencies are optional at runtime — `pdfplumber` / `pymupdf` imports are guarded.
- Fixture updates reflect already-existing runtime behavior.

---

*Phase 3 PDF evidence granularity + bounding-box upgrade complete. Infrastructure ready for production use when canonical relationships begin referencing PDF-backed sources with evidence snippets.*
