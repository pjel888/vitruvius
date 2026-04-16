---
task: aec-first-bounded-slice-implementation
phase: 05
created: 2026-04-16
author: PLANNER
supersedes: null
status: accepted
execution_state: baseline-ready-evidence-pending
slice_class: bounded-first-implementation
baseline_branch: aec/clean-baseline-20260416
baseline_worktree: /Users/philiplewis/vitruvius-aec-clean-baseline
subsystem_scope:
  - boundary
  - ecs
  - spatial
  - verification
ready_to_implement: false
entry_gates_verified: false
readiness_evidence:
  - .ai/04_tasks/aec-engine-gates-state-2026-04-16.json
  - .ai/10_state/baselines/aec-clean-implementation-baseline-2026-04-16.md
  - .ai/04_tasks/2026-04-16-aec-first-bounded-slice-implementation-trigger.md
---

# AEC First Bounded Slice Sprint Plan

## Slice Statement
Implement one strict boundary-to-reference-world AEC spine: one bounded DTO family, one strict boundary import lane, one Python ECS world, one bounded spatial fact lane, and one verifier whitelist/refusal/artifact lane.

## Inputs
- `.ai/04_tasks/aec-engine-g2-g8-freeze-pack-2026-04-16.md`
- `.ai/03_plans/2026-04-16-aec-first-bounded-slice-pre-implementation-plan.md`
- `.ai/03_plans/2026-04-16-aec-t013-knowledge-vault-foundation-plan.md`
- `.ai/03_plans/2026-04-16-aec-t017-coordination-foundation-plan.md`
- `.ai/03_plans/2026-04-16-aec-t018-pricing-optimization-foundation-plan.md`
- `.ai/03_plans/2026-04-16-aec-t019-tooling-foundation-plan.md`
- `.ai/04_tasks/aec-t011-fixture-corpus-spec-2026-04-16.md`
- `.omx/plans/prd-aec-first-bounded-slice.md`
- `.omx/plans/test-spec-aec-first-bounded-slice.md`
- `.ai/04_tasks/aec-first-slice-test-and-fixture-scaffold-map-2026-04-16.md`
- `.ai/04_tasks/aec-first-slice-module-order-and-fixture-shapes-2026-04-16.md`
- `.ai/04_tasks/aec-first-slice-verification-runbook-2026-04-16.md`
- `.ai/04_tasks/aec-first-slice-artifact-shapes-2026-04-16.md`
- `.ai/04_tasks/aec-first-slice-ownership-and-review-checklist-2026-04-16.md`
- `.ai/04_tasks/aec-first-slice-lane-exit-criteria-matrix-2026-04-16.md`
- `.ai/04_tasks/aec-g10-closure-criteria-2026-04-16.md`
- `.ai/04_tasks/aec-first-slice-execution-handoff-dossier-2026-04-16.md`
- `.ai/00_performance/2026-04-16_aec-first-slice-benchmark-hotspot-matrix.md`

## In Scope
- `scripts/vitruvius/aec/contracts/*`
- `scripts/vitruvius/aec/boundary/*`
- `scripts/vitruvius/aec/ecs/*`
- `scripts/vitruvius/aec/spatial/*`
- `scripts/vitruvius/aec/verification/*`
- `scripts/tests/test_aec_*`
- `scripts/tests/fixtures/aec/first_slice/*`
- `005_Operational-Intelligence-Layer/aec/candidates/first-slice/*`
- `005_Operational-Intelligence-Layer/aec/admitted/first-slice/*`
- `006_System-Manifests/aec/promotions/first-slice/*`

## Out of Scope
- pricing
- optimization
- coordination
- tooling
- Rust implementation beyond future candidate isolation
- TypeScript policy/orchestration logic


## Activation Gate
This sprint may execute only from the clean baseline branch/worktree and only after confirming that the gate artifact no longer reports any open execution-evidence blocker for the bounded first-slice lane.

## Entry Gates Verified
- clean baseline branch/worktree exists
- machine-readable gate artifact currently remains `ready_to_implement=false` until execution evidence scaffolds are created
- PRD and test spec exist under `.omx/plans/`
- the bounded fixture corpus is frozen by `aec-t011-fixture-corpus-spec-2026-04-16.md`

## Preconditions
- boundary remains import-first
- TypeScript remains boundary-only
- Rust remains benchmark-gated and out of initial ownership
- outputs must respect the candidate/admitted/promotion path split from the freeze pack

## Execution Order
1. strict boundary import lane
2. Python ECS world lane
3. bounded spatial fact lane
4. verifier whitelist/refusal/artifact lane
5. validation log + artifact review

## Required Outputs
- strict boundary DTO artifacts
- ECS world + snapshot artifacts
- bounded spatial fact bundle
- verifier sat/unsat/refusal artifacts
- validation report and replay evidence

## Stop Conditions
- generic `first-slice` artifact dumping bypasses the candidate/admitted/promotion split
- boundary import stops being import-first or begins to imply export breadth
- TypeScript gains policy ownership
- Rust enters the first slice without benchmark and parity evidence
- any downstream subsystem is pulled into scope

## Boundary Guardrail
The first bounded slice is **import-first**. Export behavior is allowed only when it remains audit/snapshot-bounded and does not widen the slice into generic boundary orchestration.

## Work Packages
### WP1 Boundary contract lane
- files: `scripts/vitruvius/aec/contracts/*`, `scripts/vitruvius/aec/boundary/*`
- tests: `test_aec_boundary_contract_parity.py`, `test_aec_boundary_dto.py`, `test_aec_boundary_refusals.py`
- stop: silent legacy fallback, implicit units/tolerances, TS policy ownership

### WP2 ECS reference world lane
- files: `scripts/vitruvius/aec/ecs/*`
- tests: `test_aec_ecs_contract.py`, `test_aec_ecs_replay.py`, `test_aec_ecs_schedule.py`
- stop: unstable IDs, second world authority, hidden mutable state

### WP3 Spatial fact lane
- files: `scripts/vitruvius/aec/spatial/*`
- tests: `test_aec_spatial_contracts.py`, `test_aec_spatial_parity.py`, `test_aec_spatial_routing.py`
- stop: frame/unit/tolerance drift, benchmark-free Rust migration, policy in geometry layer

### WP4 Verification lane
- files: `scripts/vitruvius/aec/verification/*`
- tests: `test_aec_z3_compiler.py`, `test_aec_z3_replay.py`, `test_aec_z3_refusals.py`, `test_aec_z3_artifacts.py`
- stop: raw prose in solver, unsupported families treated as covered, undefined timeout/refusal behavior

## Verification path
1. execute from baseline branch/worktree only
2. run affected pytest lanes
3. run any TS parity checks only if boundary schema changes
4. collect candidate/admitted/promotion artifacts under the freeze-pack-aligned first-slice roots
5. write validation log before completion

## Execution Evidence Gap
The bounded first-slice sprint is now baseline-ready and fully specified, but execution evidence is still pending because the named AEC test files and fixture materialization have not been created yet in the clean baseline worktree.

## Final rule
This sprint plan is the first true execution-handoff artifact for the bounded slice. It is intentionally narrow, baseline-ready, and evidence-pending; it must not absorb downstream subsystems.
