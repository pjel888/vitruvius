---
task: laws-graph-quality-correction
phase: 05
created: 2026-04-16
author: CODER
status: ACCEPTED
---

# 2026-04-16 Laws Graph Quality Correction Plan

## Goal
Improve graph accuracy and meaning density by fixing source attribution and concept matching in the bounded laws pipeline.

## Scope
### In scope
- extraction source-id correction
- concept matching helper with better sanitization / ordering / alias support
- regression tests
- bounded reruns/evidence

### Out of scope
- mass automatic official-truth admission
- broad enrichment rewrite
- section/merge runtime work

## Execution order
1. add bounded research/audit artifacts
2. add reusable concept-matching helper
3. route canonicalize + extraction paths through the helper
4. fix extraction source-id derivation
5. add tests
6. rerun bounded evidence checks

## Success criteria
- non-PD refined laws show more truthful concept hits in bounded scans
- extraction paths stop attributing non-PD refined documents to PD-1096 by default
- existing graph/CLI tests remain green
- no broad truth-admission claims are made beyond the actual official manifest
