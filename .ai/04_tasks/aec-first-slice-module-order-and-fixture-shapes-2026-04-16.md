---
task: aec-first-slice-module-order-and-fixture-shapes
phase: 00
created: 2026-04-16
author: PLANNER
supersedes: null
status: ACCEPTED
---

# AEC First-Slice Module Order and Fixture Shapes

## Purpose
This is the exact no-code handoff for runtime file creation order plus fixture-file naming and minimal shape contracts.

## 1. Runtime module creation order

### Step 1 — contracts
Create first:
- `scripts/vitruvius/aec/contracts/__init__.py`
- `scripts/vitruvius/aec/contracts/dto.py`
- `scripts/vitruvius/aec/contracts/ids.py`
- `scripts/vitruvius/aec/contracts/envelope.py`

Why first:
- every later lane imports IDs, DTOs, and artifact envelopes from here

### Step 2 — boundary
Create next:
- `scripts/vitruvius/aec/boundary/__init__.py`
- `scripts/vitruvius/aec/boundary/importers.py`
- `scripts/vitruvius/aec/boundary/refusals.py`
- `scripts/vitruvius/aec/boundary/validators.py`

Why second:
- boundary lane materializes the first DTO-bearing inputs

### Step 3 — boundary fixtures
Create next:
- `scripts/tests/fixtures/aec/first_slice/boundary/boundary_strict_valid_basic.json`
- `scripts/tests/fixtures/aec/first_slice/boundary/boundary_invalid_missing_footer.json`
- `scripts/tests/fixtures/aec/first_slice/boundary/boundary_invalid_weak_footer.json`
- `scripts/tests/fixtures/aec/first_slice/boundary/boundary_invalid_missing_frame.json`
- `scripts/tests/fixtures/aec/first_slice/boundary/boundary_invalid_unit_mismatch.json`

### Step 4 — ECS
Create next:
- `scripts/vitruvius/aec/ecs/__init__.py`
- `scripts/vitruvius/aec/ecs/world.py`
- `scripts/vitruvius/aec/ecs/snapshot.py`
- `scripts/vitruvius/aec/ecs/schedule.py`
- `scripts/vitruvius/aec/ecs/serializers.py`

### Step 5 — ECS fixtures
Create next:
- `scripts/tests/fixtures/aec/first_slice/ecs/ecs_world_single_revision_valid.json`
- `scripts/tests/fixtures/aec/first_slice/ecs/ecs_replay_roundtrip_stable.json`
- `scripts/tests/fixtures/aec/first_slice/ecs/ecs_schedule_order_stable.json`
- `scripts/tests/fixtures/aec/first_slice/ecs/ecs_invalid_schedule_conflict.json`

### Step 6 — spatial
Create next:
- `scripts/vitruvius/aec/spatial/__init__.py`
- `scripts/vitruvius/aec/spatial/reference.py`
- `scripts/vitruvius/aec/spatial/facts.py`
- `scripts/vitruvius/aec/spatial/routing.py`

### Step 7 — spatial fixtures
Create next:
- `scripts/tests/fixtures/aec/first_slice/spatial/spatial_valid_transform.json`
- `scripts/tests/fixtures/aec/first_slice/spatial/spatial_invalid_transform.json`
- `scripts/tests/fixtures/aec/first_slice/spatial/spatial_near_touching_tolerance.json`
- `scripts/tests/fixtures/aec/first_slice/spatial/spatial_route_candidate_basic.json`

### Step 8 — verification
Create last in the runtime chain:
- `scripts/vitruvius/aec/verification/__init__.py`
- `scripts/vitruvius/aec/verification/ast.py`
- `scripts/vitruvius/aec/verification/compiler.py`
- `scripts/vitruvius/aec/verification/refusals.py`
- `scripts/vitruvius/aec/verification/artifacts.py`

### Step 9 — verification fixtures
Create next:
- `scripts/tests/fixtures/aec/first_slice/verification/verifier_sat_basic.json`
- `scripts/tests/fixtures/aec/first_slice/verification/verifier_unsat_basic.json`
- `scripts/tests/fixtures/aec/first_slice/verification/verifier_timeout_bounded.json`
- `scripts/tests/fixtures/aec/first_slice/verification/verifier_unsupported_family.json`

## 2. Minimal fixture shape contracts

### Boundary fixture shape
```json
{
  "fixture_id": "boundary_strict_valid_basic",
  "schema_version": "v1",
  "frame_id": "building-local-mm",
  "unit_system": "mm",
  "payload": {},
  "expected_verdict": "accept"
}
```

### ECS fixture shape
```json
{
  "fixture_id": "ecs_world_single_revision_valid",
  "schema_version": "v1",
  "input_boundary_fixture": "boundary_strict_valid_basic",
  "expected_world_revision_id": "world-rev-0001",
  "expected_verdict": "accept"
}
```

### Spatial fixture shape
```json
{
  "fixture_id": "spatial_valid_transform",
  "schema_version": "v1",
  "input_ecs_fixture": "ecs_world_single_revision_valid",
  "expected_fact_bundle_id": "fact-bundle-0001",
  "expected_verdict": "accept"
}
```

### Verification fixture shape
```json
{
  "fixture_id": "verifier_sat_basic",
  "schema_version": "v1",
  "input_fact_fixture": "spatial_valid_transform",
  "rule_family": "scalar-min-max",
  "expected_verdict": "sat"
}
```

## 3. Test-file creation order
After the fixture families above exist, create tests in this order:
1. `test_aec_boundary_contract_parity.py`
2. `test_aec_boundary_dto.py`
3. `test_aec_boundary_refusals.py`
4. `test_aec_ecs_contract.py`
5. `test_aec_ecs_replay.py`
6. `test_aec_ecs_schedule.py`
7. `test_aec_spatial_contracts.py`
8. `test_aec_spatial_parity.py`
9. `test_aec_spatial_routing.py`
10. `test_aec_z3_compiler.py`
11. `test_aec_z3_replay.py`
12. `test_aec_z3_refusals.py`
13. `test_aec_z3_artifacts.py`

## 4. Artifact output expectations
Later runtime/test execution should populate:
- `005_Operational-Intelligence-Layer/aec/candidates/first-slice/`
- `005_Operational-Intelligence-Layer/aec/admitted/first-slice/`
- `006_System-Manifests/aec/promotions/first-slice/`
- bounded replay diagnostics rooted in the same first-slice namespace

## Final rule
The implementation phase should follow this order unless a later accepted planning artifact explicitly supersedes it. G10 still remains open until these files actually exist in the clean baseline worktree.
