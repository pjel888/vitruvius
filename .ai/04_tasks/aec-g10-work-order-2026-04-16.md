---
task: aec-g10-work-order
phase: 00
created: 2026-04-16
author: PLANNER
supersedes: null
status: ACCEPTED
---

# AEC G10 Work Order

## Purpose
This is the exact future execution-order checklist for clearing `G10 execution_evidence_scaffolds_present`.

## Ordered work packages

### WO-1 Test skeleton presence
Create all bounded-slice `test_aec_*` files first so the execution surface is explicit before runtime logic spreads.

### WO-2 Fixture materialization
Materialize all bounded first-slice fixtures in the frozen roots and filenames from the scaffold/spec artifacts.

### WO-3 Runtime file implementation
Implement only the bounded first-slice runtime files required to satisfy the existing tests and fixture contracts.

### WO-4 Command proof
Run the four frozen pytest command groups from the verification runbook.

### WO-5 Artifact inspection
Inspect candidate/admitted/promotion roots and replay diagnostics.

### WO-6 Validation and closure packet
Populate:
- validation report template
- G10 evidence packet template
- G10 closure criteria decision

## Completion rule
`G10` may close only after **all** work orders above are complete in the clean baseline worktree.

## Refusal rule
If work-order completion would require widening scope beyond the bounded first slice, stop and return to planning review rather than forcing closure.

## Final rule
This checklist exists to keep the final blocker closure small, ordered, and auditable.
