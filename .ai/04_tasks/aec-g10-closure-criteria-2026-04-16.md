---
task: aec-g10-closure-criteria
phase: 00
created: 2026-04-16
author: PLANNER
supersedes: null
status: ACCEPTED
---

# AEC G10 Closure Criteria

## Purpose
This is the exact no-code closure contract for `G10 execution_evidence_scaffolds_present`.

## G10 may close only when all of the following are true in `/Users/philiplewis/vitruvius-aec-clean-baseline`

### A. Test-file presence
All bounded-slice test files exist:
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

### B. Fixture-file presence
The bounded first-slice fixture roots exist and contain the named families frozen by the scaffold map and sequencing artifact:
- boundary fixtures
- ecs fixtures
- spatial fixtures
- verification fixtures

### C. Runbook execution proof
The verification runbook can be executed for real and passes:
- boundary pytest group passes
- ECS pytest group passes
- spatial pytest group passes
- verification pytest group passes
- artifact-root inspection is completed
- validation report is written

## Required evidence to record when closing G10
Current gap inventory: `.ai/04_tasks/aec-g10-missing-evidence-inventory-2026-04-16.md`
Completion checklist: `.ai/04_tasks/aec-g10-evidence-completion-checklist-2026-04-16.md`

- exact baseline worktree path
- exact git commit used
- exact command outputs
- fixture roots inspected
- artifact roots inspected
- final validation log path
- packet template: `.ai/04_tasks/aec-g10-evidence-packet-template-2026-04-16.md`

## Refusal rule
If any one of the three categories above is incomplete, G10 must remain open.

## Companion work-order checklist
- `.ai/04_tasks/aec-g10-work-order-2026-04-16.md`

## Companion coverage matrix
- `.ai/04_tasks/aec-first-slice-evidence-coverage-matrix-2026-04-16.md`

## Final rule
G10 is the remaining blocker because it requires real execution evidence, not better planning prose. This artifact exists to make that closure decision unambiguous.
