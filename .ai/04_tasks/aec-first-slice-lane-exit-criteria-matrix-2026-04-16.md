---
task: aec-first-slice-lane-exit-criteria-matrix
phase: 00
created: 2026-04-16
author: PLANNER
supersedes: null
status: ACCEPTED
---

# AEC First-Slice Lane Exit Criteria Matrix

## Purpose
This matrix defines when each bounded first-slice lane may hand off to the next.

| Lane | Must be true before handoff | Proof source |
|---|---|---|
| Boundary | DTO/contract files exist; boundary fixtures exist; `test_aec_boundary_*` pass; no silent legacy fallback; no TS policy creep | boundary tests + execution journal + validation log |
| ECS | ECS files exist; ECS fixtures exist; `test_aec_ecs_*` pass; snapshot/replay IDs stable | ECS tests + execution journal + validation log |
| Spatial | spatial files exist; spatial fixtures exist; `test_aec_spatial_*` pass; frame/unit/tolerance policy still respected | spatial tests + execution journal + validation log |
| Verification | verification files exist; verification fixtures exist; `test_aec_z3_*` pass; refusal/whitelist behavior explicit | verification tests + execution journal + validation log |
| Final validation | artifact roots inspected; validation template completed; evidence packet completed; go/no-go review recorded | validation report + evidence packet + go/no-go checklist |

## Rule
A downstream lane should not start just because upstream code exists. It starts when the upstream lane has met its bounded exit criteria.

## Final rule
If a lane cannot prove its exit criteria, the sprint should pause at that lane rather than leaking uncertainty downstream.
