---
task: aec-first-bounded-slice
phase: 03
created: 2026-04-16
author: PLANNER
supersedes: null
status: ACCEPTED
---

# Research Pack — AEC First Bounded Slice (Pre-Implementation Candidate)

## 00 — Follow-on risk resolution note
- `G2` through `G8` were later closed at the planning/spec layer via `.ai/04_tasks/aec-engine-g2-g8-freeze-pack-2026-04-16.md`.
- `AEC-T013`, `AEC-T017`, `AEC-T018`, and `AEC-T019` were later moved from unresolved risk to planned-blocked through accepted foundation plans.
- `G1` / `AEC-T006` remain open because the repo baseline is still dirty.

## 01 — Discover

### Tooling note
The repo contract prefers `code-review-graph` and GitNexus before manual scanning. Those graph tools were not available in this Codex tool surface, so research fell back to authoritative planning artifacts plus read-only shell inspection.

### Artifact inventory consulted
- Trigger: `.ai/04_tasks/aec-engine-bounded-implementation-planning-trigger.md`
- Readiness audit: `.ai/02_audits/AEC_ENGINE_WHOLE_CODEBASE_READINESS_AUDIT_2026-04-16.md`
- Master task list: `.ai/04_tasks/aec-engine-master-execution-task-list-2026-04-16.md`
- Traceability matrix: `.ai/04_tasks/aec-engine-traceability-matrix-2026-04-16.md`
- Subsystem gates: `.ai/04_tasks/aec-engine-subsystem-gates-2026-04-16.md`
- File touch matrix: `.ai/04_tasks/aec-engine-file-touch-matrix-2026-04-16.md`
- Language blacklists: `.ai/04_tasks/aec-engine-language-boundary-blacklists-2026-04-16.md`
- Live gate state: `.ai/04_tasks/aec-engine-gates-state-2026-04-16.json`
- Master AEC plan: `.ai/03_plans/AEC_ENGINE_MASTER_IMPLEMENTATION_PLAN.md`
- Boundary subsystem plan: `.ai/03_plans/AEC_ENGINE_BOUNDARY_TRANSLATION_IMPLEMENTATION_PLAN.md`
- First sprint template: `.ai/03_plans/templates/aec-engine-first-sprint-template.md`

### Ground truths confirmed
1. AEC coding is still blocked by open gates `G1`–`G8` and by unresolved upstream tasks.
2. `AEC-T020` describes the likely shape of a first bounded slice, but it is not yet closable.
3. The most dangerous current risk is boundary/contract drift, not missing downstream subsystem breadth.
4. TypeScript must remain boundary-only; Rust must remain benchmarked compute-only; Python must keep truth/validation/routing authority.
5. The first planning artifact must not pretend the sprint template means implementation-readiness already exists.

## 02 — Viable options

### Option A — blocked pre-implementation bounded-slice candidate (**recommended**)
**Shape:** define the likely first-slice spine, but only as a candidate plan that stays blocked until the upstream freezes close.

**Pros**
- aligns with the accepted trigger
- gives future execution a narrow target
- binds tests, fixtures, replay, parity, and stop conditions without authorizing code

**Cons**
- must be very explicit to avoid sounding implementation-ready
- depends on many still-open upstream closures

### Option B — contract-only planning package
**Shape:** stop at freeze-stack documentation only.

**Pros**
- safest against accidental execution optimism
- easiest to keep truthful while gates remain open

**Cons**
- too weak for the accepted trigger
- does not meaningfully narrow the future first slice

### Option C — ECS-first internal slice
**Shape:** start from Python ECS planning and let boundary details follow.

**Pros**
- Python-first and deterministic

**Cons**
- misorders the actual highest-risk seam
- lets DTO/boundary drift remain unresolved too long

## 03 — Recommendation
Choose **Option A**, explicitly framed as a **blocked pre-`AEC-T020` bounded-slice candidate**.

The candidate shape is still the narrow boundary-to-reference-world spine, but the plan must make three things explicit:
- implementation remains blocked
- upstream closures remain first-class work
- verifier scope is planning-grade whitelist/refusal/schema design, not a claim that implementation is ready

## 04 — Required upstream closures before any later execution
The later implementation sprint must not start until the following are closed and evidenced:
- `AEC-T001` namespace freeze
- `AEC-T002` audit/snapshot envelope freeze
- `AEC-T003` DTO/ID/version freeze
- `AEC-T004` frame/unit/tolerance freeze
- `AEC-T005` candidate/canonical + AST admission freeze
- `AEC-T006` clean implementation baseline
- `AEC-T007` strict-vs-legacy boundary split definition
- `AEC-T008` graph-contract reuse/separation decision
- `AEC-T009` benchmark doctrine
- `AEC-T010` parity matrix
- `AEC-T010A` backend-factory parity doctrine where applicable
- `AEC-T011` replay/fixture corpus definition
- `AEC-T013` vault foundation planning still unresolved
- `AEC-T017` coordination planning still unresolved
- `AEC-T018` pricing/optimization planning still unresolved
- `AEC-T019` tooling planning still unresolved
- `AEC-T020A` stop-condition enforcement package

## 05 — Future evidence lanes this candidate must pre-bind
- `scripts/tests/test_aec_boundary_contract_parity.py`
- `scripts/tests/test_aec_ecs_contract.py`
- `scripts/tests/test_aec_ecs_replay.py`
- `scripts/tests/test_aec_ecs_schedule.py`
- `scripts/tests/test_aec_spatial_contracts.py`
- `scripts/tests/test_aec_spatial_parity.py`
- `scripts/tests/test_aec_spatial_routing.py`
- `scripts/tests/test_aec_z3_compiler.py`
- `scripts/tests/test_aec_z3_replay.py`
- `scripts/tests/test_aec_z3_refusals.py`
- `scripts/tests/test_aec_z3_artifacts.py`

Fixture doctrine to pre-bind:
- strict + invalid boundary fixtures
- ECS replay fixtures
- bounded spatial fixture lane
- verifier sat / unsat / timeout / unsupported-family fixtures
- benchmark doctrine cited only; no Rust work authorized

## 06 — Why this is the safest candidate now
- it preserves planning truth while still narrowing the future first slice
- it puts boundary and contract risk ahead of downstream subsystem appetite
- it binds evidence lanes early enough to prevent hand-wavy execution later
- it avoids self-certifying readiness while `ready_to_implement=false`
