# AEC Engine First Sprint Template

## Companion Artifacts

- `.ai/02_audits/AEC_ENGINE_WHOLE_CODEBASE_READINESS_AUDIT_2026-04-16.md`
- `.ai/04_tasks/aec-engine-master-execution-task-list-2026-04-16.md`
- `.ai/04_tasks/aec-engine-traceability-matrix-2026-04-16.md`
- `.ai/04_tasks/aec-engine-subsystem-gates-2026-04-16.md`
- `.ai/03_plans/templates/aec-engine-first-sprint-template.md`
- `.ai/04_tasks/aec-engine-file-touch-matrix-2026-04-16.md`
- `.ai/04_tasks/aec-engine-gates.schema.json`
- `.ai/04_tasks/aec-engine-gates-spec-2026-04-16.md`
- `.ai/04_tasks/aec-engine-language-boundary-blacklists-2026-04-16.md`


## Purpose
This template is the mandatory scaffold for the first real AEC implementation sprint once the readiness gate turns green. It exists to prevent the first sprint from quietly skipping contracts, replay, parity, benchmark, or truth-governance requirements.

## Usage Instructions
Use this template only after:
- the strengthened AEC audit remains truthful
- the master execution task list is current
- the subsystem gates are current
- the readiness gate says implementation planning may proceed

## Prerequisite Checklist
- [ ] namespace and ownership map frozen
- [ ] audit/snapshot envelope frozen
- [ ] DTO / ID / versioning family frozen
- [ ] frame / unit / tolerance policy frozen
- [ ] candidate / canonical split frozen
- [ ] strict-vs-legacy boundary import behavior defined
- [ ] parity matrix row exists for every seam touched
- [ ] benchmark doctrine exists for every planned Rust candidate
- [ ] branch baseline is clean

## Forbidden Starts
Reject the sprint immediately if it includes any of the following:
- Rust-first ECS
- TypeScript orchestration growth
- Z3 over raw prose
- canonical truth writes without candidate/canonical separation
- pricing + optimization + tooling together in the first bounded slice

## Sprint Header Template

```yaml
---
task: aec-engine-<slice-name>
phase: 00
created: YYYY-MM-DD
author: PLANNER
supersedes: null
status: DRAFT
slice_class: bounded-first-implementation
blocked_by:
  - list blocker task ids still open or "none"
subsystem_scope:
  - boundary
  - ecs
  - spatial
  - verification
---
```

## Required Sections

### 1. Slice Statement
- one sentence only
- must name one bounded deliverable
- must not include downstream subsystems unless explicitly justified

### 2. In Scope
List exact files, modules, behaviors, and artifact paths.

### 3. Out of Scope
List every attractive but forbidden expansion.

### 4. Inputs
- audit sections used
- task IDs from master task list
- gate rows from subsystem gates doc
- fixture families used
- plans/subsystem gates used

### 5. Work Package Template
For each work package include:
- package ID
- purpose
- exact likely touched files
- dependencies
- required fixtures
- required tests
- required replay/parity/benchmark evidence
- stop conditions
- definition of done

### 6. Validation Evidence Template
For each work package, require fresh evidence for:
- pytest / cargo / npm lanes touched
- parity lane(s)
- replay lane(s)
- benchmark lane(s) where Rust is involved
- no-go checks still green

### 7. Rollback / Refusal Log
Every sprint must define:
- what gets rolled back if validation fails
- what gets refused rather than “deferred by implication”
- what artifacts must remain untouched if blockers are encountered

### 8. Sprint Closeout Gate
A sprint closes only when:
- all package done criteria are met
- required validation evidence exists
- required stop conditions never fired, or fired and were resolved transparently
- resulting artifacts remain within the bounded slice

## Final Rule
The first AEC implementation sprint must be narrower than management wants and stricter than engineers find convenient.
