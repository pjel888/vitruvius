---
task: aec-first-bounded-slice-implementation
phase: 00
created: 2026-04-16
author: PLANNER
supersedes: null
status: ACCEPTED
ready_to_implement: false
entry_gates_verified: false
readiness_evidence:
  - .ai/04_tasks/aec-engine-gates-state-2026-04-16.json
  - .ai/10_state/baselines/aec-clean-implementation-baseline-2026-04-16.md
  - .omx/plans/prd-aec-first-bounded-slice.md
  - .omx/plans/test-spec-aec-first-bounded-slice.md
---

# Trigger — AEC First Bounded Slice Implementation

## Task Statement
Implement the accepted first bounded AEC slice from the clean baseline branch/worktree using the approved sprint plan.

## In Scope
- strict boundary import lane
- bounded DTO family
- Python reference ECS world
- bounded spatial fact lane
- verifier whitelist/refusal/artifact lane
- bounded fixtures, tests, and replay artifacts required by the sprint plan

## Out of Scope
- pricing
- optimization
- coordination
- tooling
- Rust-first execution
- TypeScript orchestration or policy logic

## Baseline Requirement
- execution branch/worktree must start from `aec/clean-baseline-20260416` at `/Users/philiplewis/vitruvius-aec-clean-baseline`

## Governing Plan
- `.ai/03_plans/2026-04-16-aec-first-bounded-slice-sprint-plan.md`
- `.ai/04_tasks/aec-first-slice-test-and-fixture-scaffold-map-2026-04-16.md`
- `.ai/04_tasks/aec-first-slice-module-order-and-fixture-shapes-2026-04-16.md`
- `.ai/04_tasks/aec-first-slice-verification-runbook-2026-04-16.md`
- `.ai/04_tasks/aec-first-slice-artifact-shapes-2026-04-16.md`
- `.ai/04_tasks/aec-first-slice-ownership-and-review-checklist-2026-04-16.md`
- `.ai/04_tasks/aec-g10-closure-criteria-2026-04-16.md`
- `.ai/04_tasks/aec-first-slice-failure-triage-matrix-2026-04-16.md`
- `.ai/04_tasks/aec-first-slice-session-packet-2026-04-16.md`
- `.ai/04_tasks/aec-first-slice-execution-handoff-dossier-2026-04-16.md`

## Activation Gate
The trigger is valid only from the clean baseline branch/worktree and only after the named execution-evidence scaffolds (tests, fixtures, validation surfaces) actually exist.

## Entry Gates Verified
- machine-readable gate artifact still records `ready_to_implement=false` until execution evidence scaffolds exist
- clean baseline branch/worktree exists
- PRD and test spec exist
- sprint plan exists and is accepted

## Execution Order
1. boundary
2. ecs
3. spatial
4. verification
5. validation

## Required Outputs
- bounded first-slice runtime files only in declared AEC roots
- bounded test suite additions
- bounded fixture family additions
- replay/promotion/audit artifacts in the aligned first-slice roots

## Stop Conditions
- any downstream subsystem is pulled in
- outputs bypass the candidate/admitted/promotion split
- execution starts from a dirty branch instead of the clean baseline

## Definition of success
The bounded slice is implemented, verified on the baseline worktree, and remains inside declared scope.
