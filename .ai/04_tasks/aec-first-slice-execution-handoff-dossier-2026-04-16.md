---
task: aec-first-slice-execution-handoff-dossier
phase: 00
created: 2026-04-16
author: PLANNER
supersedes: null
status: ACCEPTED
---

# AEC First-Slice Execution Handoff Dossier

## Purpose
This is the operator-facing master handoff for the bounded first AEC slice. It consolidates the clean baseline, sprint plan, trigger, fixture corpus, scaffold maps, module order, artifact shapes, ownership rules, verification runbook, and G10 closure contract into one navigation surface.

## Current truthful state
- The bounded first slice is **baseline-ready / evidence-pending**.
- The clean execution baseline exists at:
  - branch: `aec/clean-baseline-20260416`
  - worktree: `/Users/philiplewis/vitruvius-aec-clean-baseline`
- The remaining blocker is:
  - `G10 execution_evidence_scaffolds_present`
- `G10` remains open until the named tests/fixtures exist and the verification runbook passes on the clean baseline worktree.

## Canonical read order for future execution
1. Clean baseline artifact  
   `.ai/10_state/baselines/aec-clean-implementation-baseline-2026-04-16.md`
2. Clean-baseline toolchain preflight  
   `.ai/04_tasks/aec-clean-baseline-toolchain-preflight-2026-04-16.md`
3. Clean-baseline toolchain remediation guide  
   `.ai/04_tasks/aec-clean-baseline-toolchain-remediation-guide-2026-04-16.md`
4. Execution dependency manifest  
   `.ai/04_tasks/aec-execution-dependency-manifest-2026-04-16.md`
5. Machine-readable gate artifact  
   `.ai/04_tasks/aec-engine-gates-state-2026-04-16.json`
3. Bounded-slice sprint plan  
   `.ai/03_plans/2026-04-16-aec-first-bounded-slice-sprint-plan.md`
4. Implementation trigger  
   `.ai/04_tasks/2026-04-16-aec-first-bounded-slice-implementation-trigger.md`
5. PRD + test spec  
   `.omx/plans/prd-aec-first-bounded-slice.md`  
   `.omx/plans/test-spec-aec-first-bounded-slice.md`
6. Fixture corpus spec  
   `.ai/04_tasks/aec-t011-fixture-corpus-spec-2026-04-16.md`
7. Test/fixture scaffold map  
   `.ai/04_tasks/aec-first-slice-test-and-fixture-scaffold-map-2026-04-16.md`
8. Module order and fixture shapes  
   `.ai/04_tasks/aec-first-slice-module-order-and-fixture-shapes-2026-04-16.md`
9. Artifact shapes  
   `.ai/04_tasks/aec-first-slice-artifact-shapes-2026-04-16.md`
10. Ownership and review checklist  
    `.ai/04_tasks/aec-first-slice-ownership-and-review-checklist-2026-04-16.md`
11. Verification runbook  
    `.ai/04_tasks/aec-first-slice-verification-runbook-2026-04-16.md`
12. G10 closure criteria  
    `.ai/04_tasks/aec-g10-closure-criteria-2026-04-16.md`

## First-slice scope
In scope:
- contracts
- boundary
- ECS
- spatial
- verification
- bounded fixtures, tests, replay artifacts, and validation logs needed for that slice

Out of scope:
- pricing
- optimization
- coordination
- tooling
- Rust-first execution
- TypeScript orchestration or policy logic

## Future implementation order
1. Create contracts files
2. Create boundary files
3. Materialize boundary fixtures + tests
4. Create ECS files
5. Materialize ECS fixtures + tests
6. Create spatial files
7. Materialize spatial fixtures + tests
8. Create verification files
9. Materialize verification fixtures + tests
10. Run verification runbook
11. Inspect artifact roots
12. Write validation log
13. Re-check G10 closure criteria

## Future proof sequence
The bounded slice is only proven when all of the following are true on the clean baseline worktree:
- all named bounded-slice test files exist
- all named bounded-slice fixture families exist
- all four pytest command groups pass
- artifact-root inspection is complete
- validation report is written
- no out-of-scope subsystem was touched

## Artifact-root contract
The bounded first slice must later write only to:
- `005_Operational-Intelligence-Layer/aec/candidates/first-slice/`
- `005_Operational-Intelligence-Layer/aec/admitted/first-slice/`
- `006_System-Manifests/aec/promotions/first-slice/`
- bounded replay diagnostics rooted in the same namespace

## Review guardrails
Before bounded-slice completion is claimed, reviewers must confirm:
- no lane wrote outside its declared file family
- TypeScript stayed boundary-only
- Rust stayed out of first-slice ownership
- no downstream subsystem was pulled into scope
- artifact paths respected the candidate/admitted/promotion split
- validation evidence is fresh and complete

## G10 closure reminder
`G10` does **not** close on planning quality alone.
It closes only when the evidence exists and passes.

## Final rule
Use this dossier as the single operator handoff entrypoint for future bounded first-slice execution. If a future execution step cannot be justified by this dossier and its linked artifacts, it is not ready to run.
