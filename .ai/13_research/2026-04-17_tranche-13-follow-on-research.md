---
task: laws-tranche-13-follow-on
created: 2026-04-17
status: complete
---

# Research — Tranche-13 follow-on

## Problem
Tranche-13 executes, but:
- `CHED` remains outside staged execution because its curriculum-standard PDF still needs OCR-first prep
- `UAP Document Standards of Professional Practice` triggers the shallow-representation guardrail for the `UAP` lane

## Smallest truthful fixes
1. rerun tranche-13 source prep with `--allow-ocr` to bring `CHED` into staged admission
2. admit a bounded UAP concept-fit slice using directly evidenced professional-standard concepts:
   - `code-of-ethics`
   - `standards-of-professional-practice`
   - `general-conditions-of-contract`
