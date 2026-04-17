---
task: laws-tranche-expansion
phase: 11
created: 2026-04-17
author: CODEX
status: DRAFT
---

# 2026-04-17 Laws Tranche Expansion Research

## Question
What is the correct path from the successful 4-law bounded pilot toward broader laws coverage without violating Phase 11 gates or overloading an M2 MacBook Pro with 8GB RAM?

## Fresh evidence
From the latest readiness dry-run:
- command:
  - `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-all-dry-run --review-preset m2-8gb-safe`
- run id:
  - `20260417T004649Z`
- result:
  - `phase_11_gate = gated`
  - `review_model = qwen2.5:7b`
  - `raw_law_folder_count = 47`
  - `raw_pdf_count = 183`
  - `bounded_manifest_law_unit_count = 4`
  - `inventory_only_law_count = 43`
  - `refined_markdown_count = 5`

## What this means
The repo is still in a very asymmetric state:
- we have a working 4-law execution lane
- we do **not** have broad refined/canonical coverage across the remaining 43 law folders
- therefore the correct next step is **not** one all-laws execute path

## Correct expansion model
Expand by **tranche**, not by whole corpus.

### Why tranche expansion is the right shape
1. keeps memory and disk growth bounded on 8GB
2. preserves manifest-scoped truth governance
3. lets us re-measure after each tranche
4. avoids giving the false impression that all 47 law folders are equally ready
5. aligns with the existing bounded pilot architecture rather than bypassing it

## Recommended tranche criteria
A tranche should be:
- small enough to run on 8GB with the `m2-8gb-safe` preset
- coherent by authority family or operational adjacency
- explicit in a manifest (never inferred from directory heuristics)
- admitted only after source-quality review and scoped planning

## Suggested tranche sequencing

### Tranche 0 — readiness only
Already implemented:
- `run-laws-all-dry-run`
- `m2-8gb-safe`

### Tranche 1 — closest-law-family widening
Use a tranche of law folders that are:
- AEC-relevant
- legally adjacent to the current 4-law pilot
- likely to have enough produced/refined data to justify source admission work

Candidate selection should be based on:
- raw folder present
- refined markdown present or easily producible
- obvious legal adjacency to the pilot corpus
- manageable PDF count

### Tranche 2+ — additional bounded widening
Each subsequent tranche should only start after:
- tranche validation exists
- disk/artifact growth is understood
- 8GB review behavior stays stable

## Requirements before tranche execution
1. tranche manifest exists
2. tranche source-admission plan exists
3. 8GB-safe review preset is used by default for readiness / bounded exploration
4. dry-run for the tranche passes first
5. no generic all-laws execution path is implied

## Non-goal
- merged all-laws execute graph in the next slice
- all-resources execute graph in the next slice
