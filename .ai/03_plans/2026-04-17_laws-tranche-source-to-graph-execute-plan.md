---
task: laws-tranche-source-to-graph-execute
phase: 11
created: 2026-04-17
author: CODEX
status: DRAFT
supersedes: null
---

# 2026-04-17 Laws Tranche Source-to-Graph Execute Plan

## Objective
Add and run a bounded tranche-local source-to-graph execute wrapper now that the tranche dry-run stages all three laws truthfully.

## Required deliverables
1. `run-laws-tranche-source-to-graph`
2. derived tranche execute manifest/report paths
3. targeted CLI coverage
4. live execute evidence

## Execution order
1. implement execute wrapper by reusing `run_dataset_source_to_graph_pipeline(..., dry_run=False)`
2. keep derived manifest generation identical to dry-run staging
3. report staged law folders / duplicate visibility / graph outputs
4. run targeted tests
5. run the execute slice with `m2-8gb-safe`

## Acceptance criteria
- tranche execute wrapper runs successfully
- graph/report outputs are written
- duplicate/raw-alias visibility remains explicit
- no generic all-laws widening is implied
