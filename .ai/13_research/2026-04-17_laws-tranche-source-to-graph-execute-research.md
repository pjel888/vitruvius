---
task: laws-tranche-source-to-graph-execute
phase: 11
created: 2026-04-17
author: CODEX
status: DRAFT
---

# 2026-04-17 Laws Tranche Source-to-Graph Execute Research

## Question
What is the next truthful step now that the tranche stages all three laws through source-to-graph dry-run?

## Fresh evidence
- latest tranche source-to-graph dry-run:
  - `staged_law_folders = [PD-957, PD-1216, PD-1185]`
  - `blocked_law_folders = []`
  - `planned_stage_count = 3`
  - `shallow_representation_count = 0`
- duplicate visibility remains explicit:
  - `duplicate_law_folders = [PD-957]`
- `source_to_graph_execute_ready` is still held false only because no tranche-local execute wrapper exists yet.

## Meaning
The next safe slice is the **tranche source-to-graph execute wrapper**:
1. derive the admitted tranche manifest
2. run the existing bounded source-to-graph pipeline in execute mode
3. keep the broader Phase 11 gate explicit
4. collect real graph/run evidence

## Non-goal
- do not open generic all-laws execution
- do not remove duplicate/raw-alias guardrails
