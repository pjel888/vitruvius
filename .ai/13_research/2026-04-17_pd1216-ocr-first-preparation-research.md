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
