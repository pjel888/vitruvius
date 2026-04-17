---
task: pd1216-ocr-first-preparation
phase: 11
created: 2026-04-17
author: CODEX
status: DRAFT
---

# 2026-04-17 PD-1216 OCR-First Preparation Research

## Question
What is the next truthful step required to unblock `PD-1216` for tranche graph work?

## Fresh evidence
- `PD-1216` remains:
  - `blocked_pending_ocr`
- latest tranche reports consistently show:
  - `detection_result = LIKELY_SCANNED_PDF`
  - `recommended_route = OCR_FIRST_THEN_OPENDATALOADER`
  - `prepared_count = 0`
  - `ocr_required_count = 1`
- current OCR stack is already present locally:
  - Python package: `ocrmypdf`
  - system binary: `tesseract 5.5.2`
  - system binary: `ghostscript 10.07.0`

## Meaning
The blocker is not missing OCR software.

The blocker is that the actual OCR-first preparation has not yet been executed for the `PD-1216` source file.

## Required outputs
To unblock the tranche, `PD-1216` needs:
1. OCR PDF output
2. raw markdown
3. refined markdown
4. sidecar JSON
5. rerun of:
   - tranche source admission
   - tranche source-to-graph dry-run

## Non-goal
- do not widen tranche execute yet
- do not pretend OCR readiness equals tranche execute readiness

## OCR quality acceptance criteria for `PD-1216`
`PD-1216` should only be treated as OCR-unblocked when both the pipeline state and the extracted content clear a minimal quality gate:

1. **Produced-data outputs exist**
   - OCR PDF exists under `002_Raw-Conversion-Layer/001-Laws/ocr_pdf/PD-1216/`
   - raw markdown exists under `002_Raw-Conversion-Layer/001-Laws/raw_markdown/PD-1216/`
   - refined markdown exists under `002_Raw-Conversion-Layer/001-Laws/refined_markdown/PD-1216/`
   - sidecar JSON exists under `002_Raw-Conversion-Layer/001-Laws/sidecar_json/PD-1216/`
2. **Tranche state flips truthfully**
   - tranche source-prep report shows `prepared_count = 1` and `ocr_required_count = 0` for `PD-1216`
   - tranche source-admission rerun no longer leaves `PD-1216` in `blocked_pending_ocr`
   - tranche source-to-graph dry-run no longer reports `PD-1216 remains blocked pending OCR-first processing`
3. **OCR text is materially usable**
   - extraction is no longer blank
   - core anchors survive OCR, at minimum:
     - `PRESIDENTIAL DECREE NO. 1216`
     - `SECTION 1.`
     - `SECTION 2.`
     - `SECTION 3.`
     - `RULE V`
     - `Section 12. Effectivity.`
   - decree text and implementing-rules text both appear in the OCR output
4. **Manual spot-check does not reveal a trust-breaking defect**
   - top-of-page stamp noise does not overwrite operative headings
   - numeric provisions / section numbering remain readable
   - signature blocks and footer noise do not spill into operative sections badly enough to mislead admission review

## Empirical OCR probe findings
I ran a temporary OCR probe to `/tmp/pd1216-ocr-probe.pdf` without touching repo outputs.

- raw source PDF characteristics:
  - 5 pages
  - extracted text before OCR: `0` chars on every page
  - each page is a single JPEG-like image with no font resources
  - approximate scan density is only ~`137–150 DPI`
- OCR probe result:
  - OCR completed successfully with `ocrmypdf 17.4.1`
  - Tesseract emitted `lots of diacritics - possibly poor OCR` warnings
  - extracted text after OCR: `10,843` chars total
  - all key anchors listed above were present in the OCR output
- visual spot-check:
  - page 1 is readable but has a prominent library / agency stamp in the header
  - pages 2 and 5 remain readable, but signatures and edge noise are present

## Likely failure modes
1. **Header-stamp pollution on page 1**
   - the top stamp already OCRs noisily (`HOUSING AND | LAND USE...`)
   - this could bleed junk into leading lines of raw/refined markdown
2. **Low-DPI character confusion**
   - at ~137–150 DPI, punctuation, apostrophes, and small capitals are vulnerable
   - likely examples: `No.` vs `No,`, `lots` vs `Jots`, stray diacritics / quote substitutions
3. **Hyphenation and line-wrap artifacts**
   - decree text contains wrapped legal prose and numbered provisions
   - OCR may preserve awkward line breaks that need refinement before downstream canonical use
4. **Signature / footer contamination**
   - page 5 signatures and footer marks may be captured as spurious text near the end of the implementing rules
5. **False confidence from text-only metrics**
   - once OCR succeeds, simple line-count / heading-count checks may look healthy even if stamp noise remains
   - manual spot-check is still required before trusting summaries

## Assessment
`PD-1216` looks like a **good candidate for OCR-first admission rerun**, not a hopeless scan.
The probe recovered the main decree and implementing-rules structure, but the scan quality is noisy enough that admission should remain **guarded/manual-review-oriented**, not unattended.
