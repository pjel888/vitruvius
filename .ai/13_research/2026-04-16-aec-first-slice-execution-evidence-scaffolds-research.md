---
task: aec-first-slice-execution-evidence-scaffolds
phase: 03
created: 2026-04-16
author: PLANNER
supersedes: null
status: ACCEPTED
---

# Research — AEC First-Slice Execution Evidence Scaffolds

## Purpose
Turn the remaining evidence blocker into an explicit implementation handoff package by specifying every missing bounded-slice test and fixture scaffold before runtime coding begins.

## Fresh evidence
A clean execution baseline exists at `/Users/philiplewis/vitruvius-aec-clean-baseline`, but the named bounded-slice tests do not yet exist there.

Missing bounded-slice evidence files confirmed absent:
- `scripts/tests/test_aec_boundary_contract_parity.py`
- `scripts/tests/test_aec_boundary_dto.py`
- `scripts/tests/test_aec_boundary_refusals.py`
- `scripts/tests/test_aec_ecs_contract.py`
- `scripts/tests/test_aec_ecs_replay.py`
- `scripts/tests/test_aec_ecs_schedule.py`
- `scripts/tests/test_aec_spatial_contracts.py`
- `scripts/tests/test_aec_spatial_parity.py`
- `scripts/tests/test_aec_spatial_routing.py`
- `scripts/tests/test_aec_z3_compiler.py`
- `scripts/tests/test_aec_z3_replay.py`
- `scripts/tests/test_aec_z3_refusals.py`
- `scripts/tests/test_aec_z3_artifacts.py`

## Conclusion
The remaining blocker is not planning ambiguity anymore. It is missing execution-evidence scaffolding. The correct next no-code move is to freeze:
- exact file-by-file test responsibilities
- exact fixture families and expected verdicts
- exact command lanes that will later prove the slice
- exact artifact roots each lane must populate
