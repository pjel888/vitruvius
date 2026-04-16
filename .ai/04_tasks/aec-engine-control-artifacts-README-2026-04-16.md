# AEC Engine Control Artifacts Package

## Purpose
This README is the operator-grade index for the AEC planning-control package. It explains what each artifact is for, the order in which to read them, and how they should be used to drive future implementation planning safely.

## Current Package State
- The package has progressed from planning-only to **bounded first-slice baseline-ready** at the planning/control layer.
- The approved execution baseline is `aec/clean-baseline-20260416` at `/Users/philiplewis/vitruvius-aec-clean-baseline`.
- Runtime code has still not been written in this planning branch; the package is defining the clean handoff into execution.

## Canonical Read Order
1. Readiness audit  
   `.ai/02_audits/AEC_ENGINE_WHOLE_CODEBASE_READINESS_AUDIT_2026-04-16.md`
2. Master execution task list  
   `.ai/04_tasks/aec-engine-master-execution-task-list-2026-04-16.md`
3. Traceability matrix  
   `.ai/04_tasks/aec-engine-traceability-matrix-2026-04-16.md`
4. Subsystem gates  
   `.ai/04_tasks/aec-engine-subsystem-gates-2026-04-16.md`
5. File touch matrix  
   `.ai/04_tasks/aec-engine-file-touch-matrix-2026-04-16.md`
6. Language boundary blacklists  
   `.ai/04_tasks/aec-engine-language-boundary-blacklists-2026-04-16.md`
7. Machine-readable gate artifacts  
   `.ai/04_tasks/aec-engine-gates.schema.json`  
   `.ai/04_tasks/aec-engine-gates-spec-2026-04-16.md`  
   `.ai/04_tasks/aec-engine-gates-state-2026-04-16.json`
8. Clean baseline artifact  
   `.ai/10_state/baselines/aec-clean-implementation-baseline-2026-04-16.md`
9. Clean-baseline toolchain preflight  
   `.ai/04_tasks/aec-clean-baseline-toolchain-preflight-2026-04-16.md`
10. Clean-baseline toolchain remediation guide  
   `.ai/04_tasks/aec-clean-baseline-toolchain-remediation-guide-2026-04-16.md`
11. Execution dependency manifest  
   `.ai/04_tasks/aec-execution-dependency-manifest-2026-04-16.md`
12. First bounded-slice sprint plan  
   `.ai/03_plans/2026-04-16-aec-first-bounded-slice-sprint-plan.md`
10. First bounded-slice implementation trigger  
   `.ai/04_tasks/2026-04-16-aec-first-bounded-slice-implementation-trigger.md`
11. Ralph PRD + test spec  
   `.omx/plans/prd-aec-first-bounded-slice.md`  
   `.omx/plans/test-spec-aec-first-bounded-slice.md`
12. Historical intermediate planning checkpoints  
   `.ai/03_plans/2026-04-16-aec-first-bounded-slice-pre-implementation-plan.md`  
   `.ai/04_tasks/aec-engine-g2-g8-freeze-pack-2026-04-16.md`
13. Downstream foundation plans  
   `.ai/03_plans/2026-04-16-aec-t013-knowledge-vault-foundation-plan.md`  
   `.ai/03_plans/2026-04-16-aec-t017-coordination-foundation-plan.md`  
   `.ai/03_plans/2026-04-16-aec-t018-pricing-optimization-foundation-plan.md`  
   `.ai/03_plans/2026-04-16-aec-t019-tooling-foundation-plan.md`

## Package Inventory

### 1. Readiness audit
- **File:** `.ai/02_audits/AEC_ENGINE_WHOLE_CODEBASE_READINESS_AUDIT_2026-04-16.md`
- **Purpose:** strongest current truth about what exists, what is missing, what is dangerous, and what must be frozen first

### 2. Master execution task list
- **File:** `.ai/04_tasks/aec-engine-master-execution-task-list-2026-04-16.md`
- **Purpose:** staged execution-driving task map from blocker-class work through readiness gate

### 3. Traceability matrix
- **File:** `.ai/04_tasks/aec-engine-traceability-matrix-2026-04-16.md`
- **Purpose:** maps audit findings to task IDs, files, tests, and stop/gate linkages

### 4. Subsystem gates
- **File:** `.ai/04_tasks/aec-engine-subsystem-gates-2026-04-16.md`
- **Purpose:** defines entry/exit gates and no-go states for each AEC subsystem

### 5. File touch matrix
- **File:** `.ai/04_tasks/aec-engine-file-touch-matrix-2026-04-16.md`
- **Purpose:** classifies file/path surfaces as forbidden, precedent-only, allowed-after-freeze, or direct-target

### 6. Language boundary blacklists
- **File:** `.ai/04_tasks/aec-engine-language-boundary-blacklists-2026-04-16.md`
- **Purpose:** explicit Rust/TypeScript forbidden ownership rules and exception procedure

### 7. Gate schema + spec + live state
- **Schema:** `.ai/04_tasks/aec-engine-gates.schema.json`
- **Spec:** `.ai/04_tasks/aec-engine-gates-spec-2026-04-16.md`
- **Live instance:** `.ai/04_tasks/aec-engine-gates-state-2026-04-16.json`
- **Purpose:** machine-readable representation of current blocker/gate state for AEC readiness

### 8. First sprint template
- **File:** `.ai/03_plans/templates/aec-engine-first-sprint-template.md`
- **Purpose:** reusable bounded-slice template for the first actual AEC implementation sprint after readiness goes green

### 9. Historical planning trigger
- **File:** `.ai/04_tasks/aec-engine-bounded-implementation-planning-trigger.md`
- **Purpose:** opened the valid SEL planning task that produced the bounded-slice planning chain

### 10. Historical bounded-slice pre-implementation candidate
- **File:** `.ai/03_plans/2026-04-16-aec-first-bounded-slice-pre-implementation-plan.md`
- **Purpose:** records the approved pre-`AEC-T020` candidate that preceded the sprint-ready handoff

## Operating Rules
- This package is control-oriented and now includes a bounded first-slice execution handoff.
- It must still be used to keep execution inside the declared baseline, sprint plan, trigger, and stop-condition guardrails.
- The live gate-state JSON is a status snapshot, not a self-fulfilling approval artifact.
- Any future implementation plan must cross-reference this package explicitly.

## Maintenance Rules
- If the readiness audit changes materially, update:
  - traceability matrix
  - subsystem gates
  - file touch matrix
  - language boundary blacklists
  - gate-state JSON
- If any new AEC planning artifact is created, add it to this README if it changes how operators should navigate the package.

## Final Rule
If a future plan, trigger, or sprint cannot be navigated and validated through this package, it is not enterprise-safe enough to proceed.
