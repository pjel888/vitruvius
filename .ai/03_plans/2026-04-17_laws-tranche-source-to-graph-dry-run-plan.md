---
task: laws-tranche-source-to-graph-dry-run
phase: 11
created: 2026-04-17
author: CODEX
status: DRAFT
supersedes: null
---

# 2026-04-17 Laws Tranche Source-to-Graph Dry-Run Plan

## Objective
Run a truthful tranche-local source→graph dry-run using only the admitted tranche members while keeping blocked members explicit and execute still gated.

## Required deliverables
1. derived tranche dataset manifest
2. tranche-local source→graph dry-run command
3. report showing staged vs blocked tranche members
4. validation log

## Execution order
1. derive a dataset manifest from the tranche source-admission state
2. stage only admitted tranche law units
3. preserve blocked law units outside the staged manifest but inside the outer report
4. delegate to `run_dataset_source_to_graph_pipeline(..., dry_run=True)`
5. keep execute readiness false

## Acceptance criteria
- `PD-957` and `PD-1185` stage successfully in the tranche-local dry-run
- `PD-1216` remains explicitly blocked
- duplicate/raw-alias guardrails remain visible
- no execute path is implied or unlocked
