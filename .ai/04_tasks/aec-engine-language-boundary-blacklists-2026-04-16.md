---
task: aec-engine-language-boundary-blacklists
phase: 00
created: 2026-04-16
author: PLANNER
supersedes: null
status: ACCEPTED
---

# AEC Engine Language Boundary Blacklists

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


## Boundary Doctrine
- Python owns orchestration, validation, truth governance, replay coordination, and tool routing.
- Rust owns only isolated deterministic compute kernels.
- TypeScript owns only boundary schema/footer emission and boundary-local helper logic.

## Rust Forbidden Ownership
Rust must not own:
- legal interpretation
- provenance logic
- candidate/canonical truth admission
- promotion decisions
- pricebook authority or currency/freshness policy
- tool routing
- refusal taxonomy
- user-facing explanation logic
- repo workflow or planning logic

## TypeScript Forbidden Ownership
TypeScript must not own:
- AEC orchestration
- AEC verification logic
- pricing logic
- optimization logic
- coordination logic
- candidate/canonical truth decisions
- authoritative unit policy
- authoritative tolerance policy
- authoritative predicate semantics beyond bounded boundary emission

## Python-Retained Authority
Python retains final authority for:
- DTO and schema validation
- import/export mediation
- truth admission and provenance preservation
- AST compilation and verifier query assembly
- pricing policy and freshness rules
- optimization policy and reproducibility metadata
- tool routing and refusal behavior

## Exception Procedure
Any exception to this blacklist requires:
1. explicit architectural justification
2. explicit affected-file list
3. explicit benchmark and/or governance evidence
4. explicit new stop conditions
5. explicit approval artifact in the planning layer

## Violation Examples
- moving rule-meaning logic into Rust “because it’s cleaner”
- adding pricing or coordination logic to `spatial-daemon/`
- using TypeScript-emitted rounding as the system tolerance law
- reusing current mutable review caches as canonical AEC truth stores

## Review Checklist
- [ ] Does this plan assign truth semantics to Rust?
- [ ] Does this plan assign orchestration semantics to TypeScript?
- [ ] Is every Rust candidate narrow, numeric, benchmarked, and parity-tested?
- [ ] Is every TypeScript change provably boundary-only and parity-bound to Python?
- [ ] Is Python explicitly retaining authority for validation, truth, and routing?

## Final Rule
If a future implementation plan needs exceptions to this blacklist, it is not a routine planning decision. It is an architectural exception and must be treated as one.
