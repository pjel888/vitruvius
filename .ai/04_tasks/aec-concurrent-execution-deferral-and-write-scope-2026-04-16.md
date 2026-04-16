---
task: aec-concurrent-execution-deferral-and-write-scope
phase: 00
created: 2026-04-16
author: PLANNER
supersedes: null
status: ACCEPTED
---

# AEC Concurrent Execution Deferral and Write-Scope Protocol

## Purpose
This artifact defines how to defer the bounded first-slice implementation when another Codex task is active, and how to resume safely once that conflict clears.

## Current rule
Do **not** start bounded first-slice runtime implementation while another active Codex task may touch overlapping repo surfaces.

## Deferral status language
Use:
- `execution_deferred_by_conflict: true`
- `architectural_readiness_unchanged: true`
- `planning_continues: true`

## Reserved write scopes for future bounded-slice execution
### Boundary/contracts lane
- `scripts/vitruvius/aec/contracts/*`
- `scripts/vitruvius/aec/boundary/*`
- `scripts/tests/test_aec_boundary_*`
- `scripts/tests/fixtures/aec/first_slice/boundary/*`

### ECS lane
- `scripts/vitruvius/aec/ecs/*`
- `scripts/tests/test_aec_ecs_*`
- `scripts/tests/fixtures/aec/first_slice/ecs/*`

### Spatial lane
- `scripts/vitruvius/aec/spatial/*`
- `scripts/tests/test_aec_spatial_*`
- `scripts/tests/fixtures/aec/first_slice/spatial/*`

### Verification lane
- `scripts/vitruvius/aec/verification/*`
- `scripts/tests/test_aec_z3_*`
- `scripts/tests/fixtures/aec/first_slice/verification/*`

## Resume checklist after conflict clears
1. confirm the other Codex task is finished or non-overlapping
2. confirm the clean baseline worktree still exists and is clean
3. confirm `G10` is still the only open blocker
4. confirm no new repo-wide state drift invalidates the sprint plan
5. resume from the execution handoff dossier and G10 work order

## Refusal rule
If overlap risk is unclear, stay in planning-only mode and do not begin coding.

## Final rule
This protocol exists to prevent avoidable merge/scope conflicts without pretending the bounded first slice lost architectural readiness.


## Resume-after-deferral checklist
- `.ai/04_tasks/aec-resume-after-deferral-checklist-2026-04-16.md`
