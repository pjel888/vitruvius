---
task: aec-g10-missing-evidence-inventory
phase: 00
created: 2026-04-16
author: PLANNER
supersedes: null
status: ACCEPTED
---

# AEC G10 Missing Evidence Inventory

## Purpose
This artifact is the live inventory of what evidence is still missing before `G10` can close.

## Baseline checked
- branch/worktree: `aec/clean-baseline-20260416`
- path: `/Users/philiplewis/vitruvius-aec-clean-baseline`

## Test-file inventory
| Path | Status |
|---|---|
| `scripts/tests/test_aec_boundary_contract_parity.py` | missing |
| `scripts/tests/test_aec_boundary_dto.py` | missing |
| `scripts/tests/test_aec_boundary_refusals.py` | missing |
| `scripts/tests/test_aec_ecs_contract.py` | missing |
| `scripts/tests/test_aec_ecs_replay.py` | missing |
| `scripts/tests/test_aec_ecs_schedule.py` | missing |
| `scripts/tests/test_aec_spatial_contracts.py` | missing |
| `scripts/tests/test_aec_spatial_parity.py` | missing |
| `scripts/tests/test_aec_spatial_routing.py` | missing |
| `scripts/tests/test_aec_z3_compiler.py` | missing |
| `scripts/tests/test_aec_z3_replay.py` | missing |
| `scripts/tests/test_aec_z3_refusals.py` | missing |
| `scripts/tests/test_aec_z3_artifacts.py` | missing |

## Fixture-family status
Expected fixture roots still to be materialized:
- `scripts/tests/fixtures/aec/first_slice/boundary/`
- `scripts/tests/fixtures/aec/first_slice/ecs/`
- `scripts/tests/fixtures/aec/first_slice/spatial/`
- `scripts/tests/fixtures/aec/first_slice/verification/`

## Why G10 stays open
G10 stays open because the clean baseline does not yet contain the named bounded-slice tests and fixtures, so the verification runbook cannot yet be executed for real.

## Final rule
Update this inventory whenever a future execution session creates or verifies new evidence for the bounded first slice.
