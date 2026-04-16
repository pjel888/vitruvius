---
task: aec-first-slice-test-and-fixture-scaffold-map
phase: 00
created: 2026-04-16
author: PLANNER
supersedes: null
status: ACCEPTED
---

# AEC First-Slice Test and Fixture Scaffold Map

## Purpose
This is the exact implementation handoff map for the missing bounded-slice evidence. It freezes which test file owns which behavior, which fixtures each test consumes, and which command lanes later prove completion.

## 1. Boundary lane

### `scripts/tests/test_aec_boundary_contract_parity.py`
Owns:
- Python/TypeScript contract parity for the bounded first-slice boundary payload
- footer and schema parity checks only
Consumes fixtures:
- `boundary_strict_valid_basic`
- `boundary_invalid_missing_footer`
- `boundary_invalid_weak_footer`
Pass proof:
- `pytest scripts/tests/test_aec_boundary_contract_parity.py`

### `scripts/tests/test_aec_boundary_dto.py`
Owns:
- DTO shape validation
- required IDs, `frame_id`, `unit_system`, and schema-version expectations
Consumes fixtures:
- `boundary_strict_valid_basic`
- `boundary_invalid_missing_frame`
- `boundary_invalid_unit_mismatch`
Pass proof:
- `pytest scripts/tests/test_aec_boundary_dto.py`

### `scripts/tests/test_aec_boundary_refusals.py`
Owns:
- explicit refusal taxonomy for unsupported or weak boundary inputs
Consumes fixtures:
- all invalid boundary fixtures
Pass proof:
- `pytest scripts/tests/test_aec_boundary_refusals.py`

## 2. ECS lane

### `scripts/tests/test_aec_ecs_contract.py`
Owns:
- world IDs, snapshot envelope fields, component-family presence
Consumes fixtures:
- `ecs_world_single_revision_valid`
Pass proof:
- `pytest scripts/tests/test_aec_ecs_contract.py`

### `scripts/tests/test_aec_ecs_replay.py`
Owns:
- stable snapshot -> world -> snapshot replay behavior
Consumes fixtures:
- `ecs_world_single_revision_valid`
- `ecs_replay_roundtrip_stable`
Pass proof:
- `pytest scripts/tests/test_aec_ecs_replay.py`

### `scripts/tests/test_aec_ecs_schedule.py`
Owns:
- deterministic schedule order and invalid schedule refusal case
Consumes fixtures:
- `ecs_schedule_order_stable`
- `ecs_invalid_schedule_conflict`
Pass proof:
- `pytest scripts/tests/test_aec_ecs_schedule.py`

## 3. Spatial lane

### `scripts/tests/test_aec_spatial_contracts.py`
Owns:
- spatial input/output contract checks for the bounded first slice
Consumes fixtures:
- `spatial_valid_transform`
- `spatial_invalid_transform`
Pass proof:
- `pytest scripts/tests/test_aec_spatial_contracts.py`

### `scripts/tests/test_aec_spatial_parity.py`
Owns:
- Python-first spatial parity expectations for bounded facts
Consumes fixtures:
- `spatial_valid_transform`
- `spatial_near_touching_tolerance`
Pass proof:
- `pytest scripts/tests/test_aec_spatial_parity.py`

### `scripts/tests/test_aec_spatial_routing.py`
Owns:
- bounded routing primitive behavior for the first slice only
Consumes fixtures:
- `spatial_route_candidate_basic`
Pass proof:
- `pytest scripts/tests/test_aec_spatial_routing.py`

## 4. Verification lane

### `scripts/tests/test_aec_z3_compiler.py`
Owns:
- AST compiler whitelist behavior
Consumes fixtures:
- `verifier_sat_basic`
- `verifier_unsat_basic`
Pass proof:
- `pytest scripts/tests/test_aec_z3_compiler.py`

### `scripts/tests/test_aec_z3_replay.py`
Owns:
- replay from stored verification inputs/artifacts
Consumes fixtures:
- `verifier_sat_basic`
- `verifier_unsat_basic`
Pass proof:
- `pytest scripts/tests/test_aec_z3_replay.py`

### `scripts/tests/test_aec_z3_refusals.py`
Owns:
- unsupported-family and oversize/timeout refusal behavior
Consumes fixtures:
- `verifier_timeout_bounded`
- `verifier_unsupported_family`
Pass proof:
- `pytest scripts/tests/test_aec_z3_refusals.py`

### `scripts/tests/test_aec_z3_artifacts.py`
Owns:
- witness / unsat / refusal artifact schema checks
Consumes fixtures:
- `verifier_sat_basic`
- `verifier_unsat_basic`
- `verifier_timeout_bounded`
Pass proof:
- `pytest scripts/tests/test_aec_z3_artifacts.py`

## 5. Fixture root expectations
Fixtures should later materialize under:
- `scripts/tests/fixtures/aec/first_slice/boundary/`
- `scripts/tests/fixtures/aec/first_slice/ecs/`
- `scripts/tests/fixtures/aec/first_slice/spatial/`
- `scripts/tests/fixtures/aec/first_slice/verification/`

Each fixture file/family must define:
- fixture id
- source or synthetic origin
- expected verdict
- input lane
- expected artifact root

## 6. Runtime artifact roots to verify later
- candidate machine-truth artifacts: `005_Operational-Intelligence-Layer/aec/candidates/first-slice/`
- admitted machine-truth artifacts: `005_Operational-Intelligence-Layer/aec/admitted/first-slice/`
- promotion / audit artifacts: `006_System-Manifests/aec/promotions/first-slice/`
- replay diagnostics: bounded first-slice replay subdirectories rooted in the same namespace

## 7. Future command matrix
Later execution should prove the slice with exactly these commands or their equivalent bounded variants:
- `pytest scripts/tests/test_aec_boundary_contract_parity.py scripts/tests/test_aec_boundary_dto.py scripts/tests/test_aec_boundary_refusals.py`
- `pytest scripts/tests/test_aec_ecs_contract.py scripts/tests/test_aec_ecs_replay.py scripts/tests/test_aec_ecs_schedule.py`
- `pytest scripts/tests/test_aec_spatial_contracts.py scripts/tests/test_aec_spatial_parity.py scripts/tests/test_aec_spatial_routing.py`
- `pytest scripts/tests/test_aec_z3_compiler.py scripts/tests/test_aec_z3_replay.py scripts/tests/test_aec_z3_refusals.py scripts/tests/test_aec_z3_artifacts.py`

## Final rule
G10 closes only when these files and fixture families exist in the clean baseline worktree and the command matrix passes there.


## Companion sequencing artifact
- `.ai/04_tasks/aec-first-slice-module-order-and-fixture-shapes-2026-04-16.md`
