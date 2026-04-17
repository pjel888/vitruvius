---
task: laws-tranche-source-to-graph-dry-run
phase: 11
created: 2026-04-17
author: CODEX
status: DRAFT
---

# 2026-04-17 Laws Tranche Source-to-Graph Dry-Run Audit

## Audit question
Can tranche-1 proceed directly into tranche source→graph execute now?

## Verdict
**No.**

## Why
- `PD-1216` is still blocked pending OCR.
- `PD-957` duplicate/raw-alias guardrails are now explicit, but they still need to survive a tranche-local source→graph dry-run.
- the tranche has never yet been staged through the existing bounded source→graph dry-run path as its own admitted-only slice.

## Audit recommendation
The next slice should be:
1. derive a tranche-local dataset manifest from the executed source-admission state
2. run tranche source→graph **dry-run only**
3. report:
   - staged admitted law units
   - blocked law units
   - duplicate/representation guardrails
4. keep execute gated until that dry-run evidence is accepted
