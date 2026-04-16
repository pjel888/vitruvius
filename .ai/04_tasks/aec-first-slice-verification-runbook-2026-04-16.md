---
task: aec-first-slice-verification-runbook
phase: 00
created: 2026-04-16
author: PLANNER
supersedes: null
status: ACCEPTED
---

# AEC First-Slice Verification Runbook

## Purpose
This is the exact future proof sequence for the bounded first slice once the missing tests, fixtures, and runtime files exist in the clean baseline worktree.

## 1. Required execution environment
- branch/worktree: `aec/clean-baseline-20260416` at `/Users/philiplewis/vitruvius-aec-clean-baseline`
- gate-state JSON must still show no open blocker other than the one being closed by the newly created evidence
- all bounded-slice test files and fixtures from the scaffold map must exist

## 2. Command sequence

### Boundary lane
```bash
pytest   scripts/tests/test_aec_boundary_contract_parity.py   scripts/tests/test_aec_boundary_dto.py   scripts/tests/test_aec_boundary_refusals.py
```

### ECS lane
```bash
pytest   scripts/tests/test_aec_ecs_contract.py   scripts/tests/test_aec_ecs_replay.py   scripts/tests/test_aec_ecs_schedule.py
```

### Spatial lane
```bash
pytest   scripts/tests/test_aec_spatial_contracts.py   scripts/tests/test_aec_spatial_parity.py   scripts/tests/test_aec_spatial_routing.py
```

### Verification lane
```bash
pytest   scripts/tests/test_aec_z3_compiler.py   scripts/tests/test_aec_z3_replay.py   scripts/tests/test_aec_z3_refusals.py   scripts/tests/test_aec_z3_artifacts.py
```

## 3. Artifact inspection order
After command success, inspect these roots in order:
1. `005_Operational-Intelligence-Layer/aec/candidates/first-slice/`
2. `005_Operational-Intelligence-Layer/aec/admitted/first-slice/`
3. `006_System-Manifests/aec/promotions/first-slice/`
4. bounded replay diagnostics under the same first-slice namespace

## 4. Validation report checklist
Template to use: `.ai/05_logs/aec-first-slice-validation-template-2026-04-16.md`

The future validation report must explicitly record:
- exact baseline branch/worktree used
- exact pytest commands run
- pass/fail outputs for each lane
- artifact roots inspected
- whether any out-of-scope subsystem files changed
- whether any stop condition fired
- final verdict: bounded slice still inside scope or not

## 5. Completion rule
The bounded first slice is only proven when:
- all four command groups pass
- artifact-root inspection is complete
- validation report is written
- no out-of-scope subsystem was pulled into the change

## Final rule
This runbook is a no-code execution handoff artifact. G10 stays open until the named evidence actually exists and this runbook can be executed for real.


## Companion lane exit-criteria matrix
- `.ai/04_tasks/aec-first-slice-lane-exit-criteria-matrix-2026-04-16.md`
