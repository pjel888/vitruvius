---
task: aec-first-slice-evidence-coverage-matrix
phase: 00
created: 2026-04-16
author: PLANNER
supersedes: null
status: ACCEPTED
---

# AEC First-Slice Evidence Coverage Matrix

## Purpose
This matrix shows what each bounded-slice evidence file is supposed to prove and what it depends on.

| Test file | Primary fixture families | Runtime module family | Artifact roots implicated | Review checkpoint |
|---|---|---|---|---|
| `test_aec_boundary_contract_parity.py` | boundary strict/invalid footer fixtures | `aec/contracts`, `aec/boundary` | candidates/boundary | boundary GO only if schema + footer parity hold |
| `test_aec_boundary_dto.py` | boundary valid/missing-frame/unit fixtures | `aec/contracts`, `aec/boundary` | candidates/boundary | DTO shape + ID/unit/frame rules hold |
| `test_aec_boundary_refusals.py` | invalid boundary fixtures | `aec/boundary` | candidates/boundary | refusal taxonomy explicit |
| `test_aec_ecs_contract.py` | ecs world fixture | `aec/ecs` | candidates/ecs | world/snapshot contract explicit |
| `test_aec_ecs_replay.py` | ecs replay fixtures | `aec/ecs` | candidates/ecs | replay stability proven |
| `test_aec_ecs_schedule.py` | ecs schedule fixtures | `aec/ecs` | candidates/ecs | deterministic schedule order proven |
| `test_aec_spatial_contracts.py` | spatial valid/invalid transform fixtures | `aec/spatial` | candidates/spatial | spatial contract explicit |
| `test_aec_spatial_parity.py` | spatial parity/tolerance fixtures | `aec/spatial` | candidates/spatial | bounded spatial parity holds |
| `test_aec_spatial_routing.py` | spatial route candidate fixture | `aec/spatial` | candidates/spatial | bounded routing behavior holds |
| `test_aec_z3_compiler.py` | verifier sat/unsat fixtures | `aec/verification` | candidates/verification | whitelist compiler explicit |
| `test_aec_z3_replay.py` | verifier replay fixtures | `aec/verification` | candidates/verification | replayable verification inputs/outputs hold |
| `test_aec_z3_refusals.py` | verifier timeout/unsupported fixtures | `aec/verification` | candidates/verification | refusal behavior explicit |
| `test_aec_z3_artifacts.py` | verifier sat/unsat/timeout fixtures | `aec/verification` | candidates/verification + admitted/promotion views as applicable | artifact schemas are reviewable |

## Coverage gaps to watch during execution
- a test exists but its fixture family is still missing
- a fixture exists but no test claims it
- runtime modules write outputs outside the expected roots
- review checkpoint cannot be answered from the resulting artifacts

## Final rule
G10 closes only when this matrix has no missing links in the clean baseline worktree.
