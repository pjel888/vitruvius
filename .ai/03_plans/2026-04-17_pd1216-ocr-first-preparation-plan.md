---
task: pd1216-ocr-first-preparation
phase: 11
created: 2026-04-17
author: CODEX
status: DRAFT
supersedes: null
---

# 2026-04-17 PD-1216 OCR-First Preparation Plan

## Objective
Run the smallest truthful OCR-first preparation slice for `PD-1216` so the tranche can be re-evaluated with real produced-data outputs.

## Required deliverables
1. OCR PDF for `PD-1216`
2. converted markdown + sidecar JSON from the OCR PDF
3. refined markdown
4. validation log
5. rerun:
   - tranche source admission
   - tranche source-to-graph dry-run

## Execution order
1. verify OCR stack and file paths
2. run OCR-first preparation for `PD-1216`
3. verify OCR/conversion/refinement outputs exist
4. rerun tranche source admission
5. rerun tranche source-to-graph dry-run

## Acceptance criteria
- `PD-1216` is no longer blocked for lack of OCR outputs
- rerun reports reflect the new output state truthfully
- tranche execute still remains gated until the rerun evidence is reviewed
