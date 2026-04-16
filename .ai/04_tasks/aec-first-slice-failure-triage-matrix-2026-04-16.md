---
task: aec-first-slice-failure-triage-matrix
phase: 00
created: 2026-04-16
author: PLANNER
supersedes: null
status: ACCEPTED
---

# AEC First-Slice Failure Triage Matrix

## Purpose
This is the bounded failure-triage and recovery matrix for the future first-slice implementation phase.

## Triage classes
- **B1 Boundary rejection** — invalid footer, missing frame, unit mismatch, schema mismatch
- **E1 ECS replay instability** — unstable IDs, unstable snapshot roundtrip, unstable schedule order
- **S1 Spatial contract/parity failure** — frame/tolerance mismatch, parity drift, invalid transform behavior
- **V1 Verification refusal/whitelist failure** — unsupported family, timeout, missing witness/unsat artifact
- **A1 Artifact-root failure** — writes outside candidate/admitted/promotion split or missing expected outputs
- **R1 Review/scope failure** — downstream subsystem touched, TypeScript policy creep, Rust-first drift, missing validation evidence

## Required response by class

### B1 Boundary rejection
- Stop boundary lane work immediately
- Fix only boundary/contracts/fixtures/tests
- Do not patch ECS/spatial/verification to compensate for weak boundary inputs
- Re-run only the boundary command group first

### E1 ECS replay instability
- Stop ECS lane work immediately
- Fix only ECS runtime + ECS fixtures/tests
- Do not patch spatial or verification to work around unstable ECS IDs or snapshots
- Re-run ECS tests, then full downstream sequence only after ECS is green

### S1 Spatial contract/parity failure
- Stop spatial lane work immediately
- Fix only spatial runtime + spatial fixtures/tests
- Do not redefine units/tolerances locally; return to frozen policy if ambiguity appears
- If parity failure suggests Rust or TypeScript ownership drift, escalate to review rather than widening implementation

### V1 Verification refusal/whitelist failure
- Stop verification lane work immediately
- Fix only verifier runtime + verification fixtures/tests
- Do not widen supported families to make tests pass
- Prefer explicit refusal over implicit support expansion

### A1 Artifact-root failure
- Stop the full bounded slice
- Fix path routing and artifact manifests before claiming partial progress
- Verify candidate/admitted/promotion roots again before resuming feature work

### R1 Review/scope failure
- Stop the full bounded slice
- Remove out-of-scope drift or revert it
- Re-run the validation and review checklist before claiming completion

## Escalation rule
Escalate to planning review instead of improvising if a failure would require:
- widening the first slice
- changing the frozen artifact-root split
- moving policy into TypeScript or Rust
- widening verifier rule-family support

## Final rule
This triage matrix exists to keep failures local and reversible. G10 stays open until the evidence exists and this matrix can be applied against real implementation results.


## Incidental remediation companion
- `.ai/04_tasks/aec-incidental-remediation-and-blast-radius-matrix-2026-04-16.md`
