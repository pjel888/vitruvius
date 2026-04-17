---
task: pd1216-ocr-first-preparation
phase: 11
created: 2026-04-17
author: CODEX
status: DRAFT
---

# 2026-04-17 PD-1216 OCR-First Preparation Audit

## Audit question
Can tranche graph execution proceed without first running OCR for `PD-1216`?

## Verdict
**No.**

## Why
- `PD-1216` is still explicitly blocked in the tranche manifest and reports.
- the current tranche dry-run and source-to-graph dry-run remain truthful only because `PD-1216` is excluded from staged law units.
- the OCR stack is already available, so the next blocker is execution, not missing dependencies.

## Audit recommendation
The next safe slice is:
1. run OCR-first preparation for `PD-1216`
2. confirm OCR PDF + raw/refined/sidecar outputs exist
3. rerun tranche source admission
4. rerun tranche source-to-graph dry-run
5. only then reassess tranche execute
