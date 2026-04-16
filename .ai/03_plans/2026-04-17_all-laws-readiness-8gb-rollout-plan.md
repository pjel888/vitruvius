---
task: all-laws-readiness-8gb-rollout
phase: 11
created: 2026-04-17
author: CODEX
status: DRAFT
supersedes: null
---

# 2026-04-17 All-Laws Readiness & 8GB Rollout Plan

## Goal
Create the correct next step after the successful bounded 4-law pilot by:
1. adding a whole-dataset readiness surface
2. adding an 8GB-safe review model preset
3. adding an all-laws dry-run command path first

## Constraints
- preserve truth and scope governance
- do not open generic Phase 11 execution by accident
- do not default an 8GB machine into a whole-dataset `gemma4:31b` run
- keep changes additive and reversible

## Deliverables

### D1. All-laws readiness surface
- a manifest or manifest-builder path for all-laws readiness scanning
- dry-run only in the first slice
- dataset-local reporting under `006_System-Manifests/runs/...`
- explicit counts / planned stage summary / law-unit summary

### D2. 8GB-safe review preset
- a named preset or flag that chooses a smaller review model path
- lower-risk context sizing for 8GB-class machines
- no silent mutation of current larger-machine defaults unless explicitly intended and documented

### D3. All-laws dry-run command path
- a command surface for broad readiness planning without broad execution
- should be able to run from repo root
- should emit operator-readable progress and a machine-readable summary

## Proposed implementation order

### Step 1 — planning/doc/state artifacts
- this research
- this audit
- this rollout plan
- validation log for planning acceptance

### Step 2 — config/preset work
- inspect `scripts/vitruvius/config.py`
- implement additive 8GB-safe preset selection path
- preserve old path for larger-memory/manual override use

### Step 3 — all-laws dry-run command surface
- add CLI entrypoint
- add manifest/readiness selection path
- add dry-run output/reporting only
- no broad execute path yet

### Step 4 — tests
- config/preset tests
- CLI dry-run tests
- no-regression checks for bounded pilot command paths

### Step 5 — docs/state updates
- README/operator docs if needed
- roadmap/state updates only after implementation is verified

## Acceptance criteria
- research/audit/plan artifacts exist
- an 8GB-safe review preset exists and is test-covered
- an all-laws dry-run command path exists and is test-covered
- bounded pilot commands still pass
- no generic all-laws execute path is introduced in this slice

## Explicit non-goals
- full all-laws execute
- broad HTML/browser automation for all-laws in this slice
- generic expansion approval without new evidence
