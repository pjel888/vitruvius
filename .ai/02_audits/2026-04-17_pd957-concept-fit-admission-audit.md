---
task: pd957-concept-fit-admission
phase: 11
created: 2026-04-17
author: CODEX
status: DRAFT
---

# 2026-04-17 PD-957 Concept-Fit Admission Audit

## Audit question
What is the safest next fix after the tranche source-to-graph dry-run?

## Verdict
**A bounded PD-957 concept-fit admission slice.**

## Why
- `PD-1216` remains hard-blocked on OCR and must not be used to justify tranche execute.
- `PD-1185` is staged and admitted, but does not currently drive the shallow-representation failure.
- `PD-957` is the only staged law still failing the representation guardrail and already has explicit concept language in its admitted source.

## Audit recommendation
Admit the smallest law-appropriate concept/relationship slice for `PD-957`:
1. existing shared concepts only
2. dataset-scoped relationship files only
3. no tranche execute
4. rerun tranche source-to-graph dry-run immediately after

## Guardrails
- keep `PD-1216` blocked
- keep duplicate/raw-alias guardrails for `PD-957`
- do not widen into all-laws or broader tranche execute
