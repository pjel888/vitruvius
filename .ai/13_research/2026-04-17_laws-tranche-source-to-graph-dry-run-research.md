---
task: laws-tranche-source-to-graph-dry-run
phase: 11
created: 2026-04-17
author: CODEX
status: DRAFT
---

# 2026-04-17 Laws Tranche Source-to-Graph Dry-Run Research

## Question
After tranche-1 source admission and duplicate hardening, what is the next truthful step before any tranche source→graph execution?

## Fresh evidence
- tranche source admission is now executed for:
  - `PD-957`
  - `PD-1185`
- blocked tranche member remains:
  - `PD-1216`
- tranche duplicate guardrails now surface:
  - `PD-957`
- `run_dataset_source_to_graph_pipeline(..., dry_run=True)` already exists and validates:
  - admitted source anchors
  - refined markdown readiness
  - source-quality / representation guardrails

## Meaning
The next safe move is **not** tranche execute.

The next safe move is:
1. derive a tranche-local dataset manifest from the admitted tranche state
2. stage only admitted tranche members
3. keep blocked members explicit
4. run the existing bounded source→graph pipeline in `dry_run=True`

## Minimal desired behavior
- include:
  - `PD-957`
  - `PD-1185`
- exclude from staged law units:
  - `PD-1216`
- preserve blocked visibility in the outer report
- keep `source_to_graph_execute_ready = false`

## Non-goal
- do not unlock tranche execute
- do not silently absorb blocked or excluded variants into staged law units
