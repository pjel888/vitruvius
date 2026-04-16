---
task: aec-engine-subsystem-gates
phase: 00
created: 2026-04-16
author: PLANNER
supersedes: null
status: ACCEPTED
---

# AEC Engine Subsystem Gates

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


## Doctrine
This artifact defines minimum entry/exit gates for each AEC subsystem so future implementation planning cannot start a subsystem on soft assumptions or declare it ready on shallow evidence.

## Global Gate Dependencies
Every subsystem is downstream of the following global gates:
- envelope freeze
- DTO / ID / version freeze
- frame / unit / tolerance freeze where relevant
- candidate / canonical split where relevant
- benchmark doctrine where Rust is a later possibility
- parity matrix where a seam is crossed

## Per-Subsystem Gate Cards

### Boundary Translation
- **Entry gate:** DTO, ID, `frame_id`, units, tolerance, strict-vs-legacy import split, TS/Python parity requirements frozen
- **Required task IDs:** AEC-T001, AEC-T002, AEC-T003, AEC-T004, AEC-T007
- **Minimum evidence:** `test_aec_boundary_*`, end-to-end TS→Python lane, invalid-state fixtures
- **Exit gate:** strict import path defined, legacy compatibility quarantined, provenance retention explicit, TS/Python parity explicit
- **No-go states:** weak import acceptance, TS orchestration creep, hidden unit/tolerance policy in TS emitter
- **Gate owner:** boundary/planning lane

### Knowledge Vault
- **Entry gate:** envelope freeze, AST admission law, candidate/canonical split, backend law explicit
- **Required task IDs:** AEC-T002, AEC-T003, AEC-T005, AEC-T010A
- **Minimum evidence:** `test_aec_vault_*`, backend parity and migration suite, write/read envelope review
- **Exit gate:** candidate path, canonical path, promotion path, replay envelope, backend rules defined
- **No-go states:** overwrite or purge semantics in canonical truth, raw prose stored as runtime truth
- **Gate owner:** vault/planning lane

### ECS Core
- **Entry gate:** namespace frozen, DTO/ID contract frozen, replay envelope frozen, fixture family defined
- **Required task IDs:** AEC-T002, AEC-T003, AEC-T011
- **Minimum evidence:** `test_aec_ecs_contract.py`, `test_aec_ecs_replay.py`, `test_aec_ecs_schedule.py`
- **Exit gate:** Python reference world/snapshot/schedule package defined
- **No-go states:** Rust-first ECS, duplicate world authority outside ECS
- **Gate owner:** ECS/planning lane

### Spatial Kernel
- **Entry gate:** frame/unit/tolerance freeze, ECS snapshot contract, benchmark doctrine, parity doctrine
- **Required task IDs:** AEC-T004, AEC-T009, AEC-T010, AEC-T011, AEC-T014
- **Minimum evidence:** `test_aec_spatial_*`, benchmark harness, future Python↔Rust parity lane
- **Exit gate:** Python reference spatial path defined, legitimate Rust candidates isolated narrowly
- **No-go states:** policy logic in Rust kernels, TypeScript authoritative spatial semantics, benchmark-free Rust plans
- **Gate owner:** spatial/planning lane

### Z3 Verification
- **Entry gate:** AST whitelist law, candidate/canonical split, ECS/spatial fact contract, refusal taxonomy draft
- **Required task IDs:** AEC-T005, AEC-T011, AEC-T014, AEC-T015
- **Minimum evidence:** `test_aec_z3_*`, sat/unsat/timeout/oversize fixtures
- **Exit gate:** supported families, unsupported list, replay path, witness/unsat artifact schemas, timeout policy defined
- **No-go states:** raw prose in solver path, geometry-heavy search inside solver, unsupported families treated as partial support
- **Gate owner:** verification/planning lane

### Coordination
- **Entry gate:** ECS, spatial, and verification artifact contracts frozen enough to support replay-grade issue logging
- **Required task IDs:** AEC-T014, AEC-T015, AEC-T016
- **Minimum evidence:** `test_aec_coordination_*`, precedence/cascade/oscillation fixtures
- **Exit gate:** discipline enum, precedence manifest, issue schema, replay log, escalation states defined
- **No-go states:** coordination without replay log, coordination replacing verification or optimization
- **Gate owner:** coordination/planning lane

### Pricing
- **Entry gate:** verified-candidate output contract, quantity contract, pricebook/currency/freshness policy frozen
- **Required task IDs:** AEC-T011, AEC-T014, AEC-T015, AEC-T016
- **Minimum evidence:** `test_aec_pricing_*`, refusal fixtures, provenance requirements
- **Exit gate:** deterministic pricing artifacts defined with explicit snapshot identity and refusal behavior
- **No-go states:** pricing over unverified geometry, live-market theater, missing currency/freshness contract
- **Gate owner:** pricing/planning lane

### Optimization
- **Entry gate:** verified-candidate artifacts, objective vector freeze, reproducibility metadata policy
- **Required task IDs:** AEC-T016, AEC-T018
- **Minimum evidence:** `test_aec_optimization_*`, replay fixtures, seeded-search policy if ever allowed
- **Exit gate:** deterministic frontier-first baseline defined
- **No-go states:** optimization before verification, hidden stochasticity, heuristic search before deterministic baseline
- **Gate owner:** optimization/planning lane

### LLM Tools
- **Entry gate:** deterministic artifact availability, authority fence, refusal taxonomy, stop-condition package
- **Required task IDs:** AEC-T013 through AEC-T020A
- **Minimum evidence:** `test_aec_tools_*`, especially refusals and explainers
- **Exit gate:** tool catalog, authority fence, artifact-bound explanations, explicit refusals defined
- **No-go states:** direct truth inference, raw vault/rule/candidate state used as authority input, heuristic-only routing precedent copied from current NL translator
- **Gate owner:** tooling/planning lane

## Parallelization Constraints
- Boundary and vault planning may overlap only after DTO/provenance/envelope freezes are settled.
- ECS and spatial planning may overlap only after replay, frame, and tolerance contracts are frozen.
- Pricing and optimization may overlap only after verification and candidate-artifact contracts are stable.
- Tooling must remain last; it is not parallel-safe with early contract-freeze work.

## No-Go States Summary
- any subsystem starts with undefined DTOs or identity fields
- any subsystem begins from mutable canonical-storage assumptions
- any subsystem relies on root `latest_*` aliases as replay truth
- any subsystem claims Rust readiness without benchmark + parity evidence
- any subsystem leaks orchestration or policy into TypeScript

## Gate Ownership
- governance + dispatcher lanes own global gates
- subsystem planning lanes own subsystem entry/exit evidence
- no implementation sprint should self-certify its own gate closure without explicit evidence artifacts

## Final Rule
A subsystem is not “ready to plan” because it has a good idea. It is ready only when its entry gate is satisfied and its exit gate is explicit.
