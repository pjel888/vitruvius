# Test Spec — AEC First Bounded Slice

## Required test families
- scripts/tests/test_aec_boundary_contract_parity.py
- scripts/tests/test_aec_boundary_dto.py
- scripts/tests/test_aec_boundary_refusals.py
- scripts/tests/test_aec_ecs_contract.py
- scripts/tests/test_aec_ecs_replay.py
- scripts/tests/test_aec_ecs_schedule.py
- scripts/tests/test_aec_spatial_contracts.py
- scripts/tests/test_aec_spatial_parity.py
- scripts/tests/test_aec_spatial_routing.py
- scripts/tests/test_aec_z3_compiler.py
- scripts/tests/test_aec_z3_replay.py
- scripts/tests/test_aec_z3_refusals.py
- scripts/tests/test_aec_z3_artifacts.py

## Fixture families
- strict + invalid boundary fixtures
- ECS replay fixtures
- bounded spatial fixtures
- verifier sat/unsat/timeout/unsupported fixtures

## Gate rule
No implementation claim is complete unless the full bounded-slice suite passes on the AEC baseline branch/worktree.
