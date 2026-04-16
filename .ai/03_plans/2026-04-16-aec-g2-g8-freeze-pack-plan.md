---
task: aec-g2-g8-freeze-pack
phase: 05
created: 2026-04-16
author: PLANNER
supersedes: null
status: accepted
implementation_blocked: true
ready_to_implement: false
historical_applied_checkpoint: true
not_a_sprint_plan: true
cannot_close_tasks:
  - AEC-T006
  - AEC-T020
---

# AEC G2-G8 Freeze Pack Plan

## Purpose
Close global blockers `G2` through `G8` at the planning/spec layer by producing one accepted freeze pack and reconciling the control surfaces that depend on it. This plan has now been applied and is retained as a historical/applied checkpoint while the live gate artifact carries current readiness truth.

## Work items
1. Create the freeze pack artifact covering `AEC-T001`-`AEC-T005`, `AEC-T008`, `AEC-T009`, `AEC-T010`, and `AEC-T010A`.
2. Update the machine-readable gate state so `G2`-`G8` are closed while `G1` remains open.
3. Update traceability from `OPEN` to `CONTROLLED` for the findings governed by the freeze pack.
4. Keep `ready_to_implement=false` and preserve `AEC-T006` as the remaining clean-baseline blocker.
