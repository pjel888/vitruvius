---
task: laws-tranche-expansion
phase: 11
created: 2026-04-17
author: CODEX
status: DRAFT
supersedes: null
---

# 2026-04-17 Laws Tranche Expansion Plan

## Objective
Move from the successful 4-law bounded pilot toward broader laws coverage by introducing **manifest-backed tranche execution**, rather than attempting a generic all-laws run.

## Scope
In scope:
1. tranche planning artifacts
2. tranche manifest strategy
3. tranche-1 execution gate definition

Out of scope:
1. generic all-laws execute
2. all-resources execute
3. merged all-laws graph execute in this slice

## Proposed tranche architecture
- `laws-core-bundle-m1` remains the current proven baseline
- future tranche manifests should be additive siblings, e.g.:
  - `laws-tranche-01.yaml`
  - `laws-tranche-02.yaml`
- each tranche manifest must define:
  - explicit law units
  - explicit raw anchors
  - explicit admitted source/concept/relationship inputs
  - low-spec expectations

## Execution order

### Step 1 — tranche design docs
- define tranche acceptance criteria
- define tranche naming and report roots
- define tranche readiness checklist
- keep orchestration/reporting logic in Python unless profiling later proves a compute-bound hotspot worth moving into Rust

### Step 2 — tranche-1 manifest
- create first tranche manifest after explicit selection
- do not widen by directory sweep

### Step 3 — tranche-1 dry-run
- run tranche readiness / source-to-graph dry-run first
- collect quality and machine-safety evidence

### Step 4 — tranche-1 execute
- only after dry-run evidence is acceptable

## Acceptance criteria
- tranche expansion is documented as the next legal move
- no generic all-laws execute path is introduced
- tranche-1 can be planned without ambiguity
- 8GB-safe preset remains the recommended broad-readiness baseline

## Rust candidacy note
Rust remains available for future narrow compute kernels if profiling justifies it, but the current tranche-expansion slice is still dominated by:
- manifest design
- readiness reporting
- source admission governance
- staged orchestration

Those remain Python-owned unless measured evidence later shows a specific compute-bound kernel is worth isolating.
