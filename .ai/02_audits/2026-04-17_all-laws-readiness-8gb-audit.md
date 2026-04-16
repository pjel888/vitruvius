---
task: all-laws-readiness-8gb
phase: 11
created: 2026-04-17
author: CODEX
status: DRAFT
---

# 2026-04-17 All-Laws Readiness & 8GB Audit

## Audit question
Is the repo ready to run a whole-dataset / all-laws source→graph execution on an M2 MacBook Pro with 8GB RAM?

## Verdict
**No — not yet.**

The current system is ready for:
- bounded pilot execution
- broader readiness scanning
- all-laws dry-run planning
- 8GB-safe preset work

It is **not ready** for:
- generic all-laws execute with the current `gemma4:31b` review default

## Evidence

### Governance risk
- broader all-laws work remains gated in current roadmap/state docs
- a fresh accepted slice is required before generic expansion

### Memory / model risk
- current review default is `gemma4:31b`
- current context cap is `8192`
- current timeout is `600s`
- these defaults are not a safe assumed baseline for 8GB whole-dataset execution

### Corpus growth risk
- 48 top-level law folders / 183 PDFs is far beyond the 4-law pilot
- no accepted all-laws manifest or all-laws dry-run surface exists yet

### Artifact churn risk
- repeated bounded pilot verification already creates many dataset-local run artifacts
- a full all-laws execute path without a readiness-first design would create even more disk churn and make rollback/inspection harder

## Safe / unsafe split

### Safe now
- whole-dataset planning artifacts
- all-laws dry-run command path
- explicit 8GB-safe review preset
- manifest-driven widening in small batches later

### Unsafe now
- whole-dataset execute path with current review defaults
- claiming generic all-laws readiness from pilot success alone
- allowing broad expansion by momentum instead of accepted scope

## Audit recommendation
Proceed with a **three-part next slice**:
1. all-laws readiness plan + acceptance gate
2. 8GB-safe review preset
3. all-laws dry-run command path

Do not implement a full all-laws execute path in this slice.
