---
task: aec-t011-fixture-corpus-spec
phase: 00
created: 2026-04-16
author: PLANNER
supersedes: null
status: ACCEPTED
---

# AEC-T011 Fixture / Replay Corpus Spec

## Purpose
Freeze the bounded fixture families required before first-slice implementation begins.

## Frozen fixture families
- strict-valid boundary payload
- invalid boundary payloads: missing footer, weak footer, missing frame, invalid unit
- ECS replay fixtures: stable world, stable schedule, invalid schedule-order case
- bounded spatial fixtures: valid transform, invalid transform, near-touching tolerance case
- verifier fixtures: sat, unsat, timeout, unsupported-family

## Replay rule
Every future implementation/test lane must replay from stored fixture inputs rather than ad hoc hand-built data.

## Fixture contract
Each fixture family must define:
- fixture id / slug
- source artifact or synthetic origin
- expected entry lane (boundary / ecs / spatial / verifier)
- expected verdict (`accept`, `reject`, `sat`, `unsat`, `timeout`, `unsupported`)
- required replay envelope fields
- expected output artifact roots

## Required corpus details
### Boundary fixtures
- `boundary_strict_valid_basic`
- `boundary_invalid_missing_footer`
- `boundary_invalid_weak_footer`
- `boundary_invalid_missing_frame`
- `boundary_invalid_unit_mismatch`

### ECS fixtures
- `ecs_world_single_revision_valid`
- `ecs_schedule_order_stable`
- `ecs_invalid_schedule_conflict`

### Spatial fixtures
- `spatial_valid_transform`
- `spatial_invalid_transform`
- `spatial_near_touching_tolerance`

### Verifier fixtures
- `verifier_sat_basic`
- `verifier_unsat_basic`
- `verifier_timeout_bounded`
- `verifier_unsupported_family`

## Output-path contract
- candidate machine-truth artifacts: `005_Operational-Intelligence-Layer/aec/candidates/first-slice/`
- admitted machine-truth artifacts: `005_Operational-Intelligence-Layer/aec/admitted/first-slice/`
- promotion / audit artifacts: `006_System-Manifests/aec/promotions/first-slice/`
- non-truth replay diagnostics may also write under bounded replay subdirectories rooted in the same first-slice namespace


## Companion scaffold map
- `.ai/04_tasks/aec-first-slice-test-and-fixture-scaffold-map-2026-04-16.md`
