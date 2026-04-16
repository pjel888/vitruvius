---
task: aec-first-bounded-slice
phase: 05
created: 2026-04-16
author: PLANNER
supersedes: null
status: accepted
plan_type: pre-implementation-candidate
implementation_blocked: true
ready_to_implement: false
not_a_sprint_plan: true
cannot_close_tasks:
  - AEC-T020
historical_checkpoint: true
superseded_by: .ai/03_plans/2026-04-16-aec-first-bounded-slice-sprint-plan.md
candidate_shape_dependencies:
  - AEC-T001
  - AEC-T002
  - AEC-T003
  - AEC-T004
  - AEC-T005
  - AEC-T006
  - AEC-T007
  - AEC-T008
  - AEC-T009
  - AEC-T010
  - AEC-T010A
  - AEC-T011
  - AEC-T012
  - AEC-T014
  - AEC-T015
  - AEC-T016
  - AEC-T020A
subsystem_scope:
  - boundary
  - ecs
  - spatial
  - verification
---

# AEC First Bounded Slice Pre-Implementation Plan

## Purpose
Define the next bounded AEC implementation-planning artifact as a **blocked pre-`AEC-T020` candidate**. This document narrows the future first slice and pre-binds its evidence lanes, but it does not authorize implementation and it does not claim sprint-readiness.

## Historical Status Note
This artifact is retained as the authoritative pre-implementation checkpoint, but it is now historically superseded for execution purposes by `/.ai/03_plans/2026-04-16-aec-first-bounded-slice-sprint-plan.md` and the fresh implementation trigger. Any `ready_to_implement=false` language below should be read as checkpoint-time truth, not current execution truth.

## RALPLAN-DR Summary

### Principles
1. Planning truth over implementation optimism.
2. Contracts before subsystem shape.
3. Python remains the first authority plane.
4. One seam per subsystem; no downstream sprawl.
5. Replay/parity evidence before acceleration.

### Decision Drivers
1. Live gate truth: `ready_to_implement=false`; planning/spec blockers `G2`–`G8` are closed, but `G1` remains open.
2. `AEC-T020` defines the likely first-slice shape, but cannot yet be closed.
3. Boundary and contract drift are the highest current risks.

### Viable Options
| Option | Summary | Pros | Cons |
|---|---|---|---|
| A | blocked pre-implementation bounded-slice candidate (**chosen**) | aligns with trigger; binds future evidence; stays narrow | must loudly avoid implying readiness |
| B | contract-only planning package | safest | too weak for the trigger |
| C | ECS-first internal slice | Python-heavy | misorders boundary risk |

## ADR
- **Decision:** create a blocked pre-implementation candidate for the first bounded AEC slice.
- **Drivers:** preserve gate truth, narrow the future first slice, bind proof obligations before execution pressure arrives.
- **Alternatives considered:**
  - contract-only package — rejected as too weak for the accepted trigger
  - ECS-first slice framing — rejected because boundary risk still comes first
- **Why chosen:** it gives the repo a concrete future target without pretending the upstream freeze stack is done.
- **Consequences:** this plan can guide later execution only after blockers close; until then it remains a planning artifact.
- **Follow-ups:** close the blocker stack, then produce or approve a true sprint plan based on this candidate.

## 1. Candidate Slice Statement
The likely first AEC slice, once upstream freezes are truly closed, should turn one strict boundary payload into one Python reference ECS world, one bounded spatial fixture lane, and one verifier whitelist/refusal/artifact-schema lane under a single bounded DTO family.

## 2. Scope Classification
### In scope for this planning artifact
- define the candidate shape implied by `AEC-T020`
- record exact missing prerequisites before `AEC-T020` can be truthfully satisfied
- pre-bind tests, fixtures, replay lanes, parity lanes, benchmark doctrine references, and stop conditions
- constrain likely future touch surfaces using the file-touch matrix and language blacklists

### Out of scope
- production implementation
- any claim that `AEC-T020` is now complete
- coordination (`AEC-T017`)
- pricing + optimization (`AEC-T018`)
- tooling (`AEC-T019`)
- Rust implementation work
- TypeScript growth beyond boundary/schema parity references
- broad vault runtime implementation

## 3. Blocking Truth
Implementation remains blocked by:
- `ready_to_implement=false`
- no `scripts/vitruvius/aec/*` runtime surface
- no implemented `scripts/tests/test_aec_*` suites
- planning-layer freezes and downstream foundation plans now exist, but a true sprint plan and fresh implementation trigger are still required before coding

## 4. Inputs
- Trigger: `.ai/04_tasks/aec-engine-bounded-implementation-planning-trigger.md`
- Baseline: `.ai/10_state/baselines/aec-first-bounded-slice-baseline.md`
- Research: `.ai/13_research/2026-04-16-aec-first-bounded-slice-research.md`
- Audit: `.ai/02_audits/2026-04-16-aec-first-bounded-slice-pre-implementation-audit.md`
- Readiness audit: `.ai/02_audits/AEC_ENGINE_WHOLE_CODEBASE_READINESS_AUDIT_2026-04-16.md`
- Master task list: `.ai/04_tasks/aec-engine-master-execution-task-list-2026-04-16.md`
- Traceability matrix: `.ai/04_tasks/aec-engine-traceability-matrix-2026-04-16.md`
- Subsystem gates: `.ai/04_tasks/aec-engine-subsystem-gates-2026-04-16.md`
- File touch matrix: `.ai/04_tasks/aec-engine-file-touch-matrix-2026-04-16.md`
- Language blacklists: `.ai/04_tasks/aec-engine-language-boundary-blacklists-2026-04-16.md`
- Live gate state: `.ai/04_tasks/aec-engine-gates-state-2026-04-16.json`
- First sprint template: `.ai/03_plans/templates/aec-engine-first-sprint-template.md` (future scaffold only; not directly executable yet)

## 5. In-scope task IDs for this candidate
- Contract freezes: `AEC-T001`, `AEC-T002`, `AEC-T003`, `AEC-T004`, `AEC-T005`
- Baseline/blocker truth: `AEC-T006`
- Boundary risk control: `AEC-T007`, `AEC-T012`
- Benchmark/parity/fixtures: `AEC-T009`, `AEC-T010`, `AEC-T010A`, `AEC-T011`
- Foundations referenced by the candidate shape: `AEC-T014`, `AEC-T015`, `AEC-T016`
- Slice-definition target: `AEC-T020` as **candidate-shape only**, not closure
- Stop-condition package: `AEC-T020A`
- Graph/backend law reminders: `AEC-T008`, `AEC-T010A`

## 6. Candidate work packages (planning packages, not execution packages)

### WP-1 — Contract freeze bundle
- **Task IDs:** `AEC-T001`–`AEC-T005`
- **Purpose:** define the mandatory freeze stack the future slice depends on
- **Outputs to demand later:** namespace/ownership map, envelope law, DTO/ID/version family, frame/unit/tolerance policy, candidate/canonical split + AST admission law
- **Stop conditions:** any freeze left as `TBD`; any attempt to delegate authority to Rust or TypeScript

### WP-2 — Strict boundary lane definition
- **Task IDs:** `AEC-T007`, `AEC-T012`
- **Purpose:** define the future strict boundary import lane without treating it as implemented yet
- **Required future evidence:** `scripts/tests/test_aec_boundary_contract_parity.py`, strict + invalid boundary fixtures, TS/Python parity lane
- **Guardrails:** boundary is import-first; export is allowed only if audit/snapshot-bounded; TypeScript remains boundary-only

### WP-3 — Python reference ECS world planning package
- **Task IDs:** `AEC-T011`, `AEC-T014`
- **Purpose:** define the future single-world, single-snapshot, single-schedule Python reference path
- **Required future evidence:** `scripts/tests/test_aec_ecs_contract.py`, `scripts/tests/test_aec_ecs_replay.py`, `scripts/tests/test_aec_ecs_schedule.py`
- **Guardrails:** Rust-first ECS forbidden; replay envelope required; no second world authority outside ECS

### WP-4 — Bounded spatial fixture lane planning package
- **Task IDs:** `AEC-T009`, `AEC-T010`, `AEC-T015`
- **Purpose:** define the future bounded spatial lane the candidate slice will use
- **Required future evidence:** `scripts/tests/test_aec_spatial_contracts.py`, `scripts/tests/test_aec_spatial_parity.py`, `scripts/tests/test_aec_spatial_routing.py`
- **Guardrails:** frame/unit/tolerance freeze must already exist; benchmark doctrine is cited only; no Rust ownership is implied

### WP-5 — Verifier whitelist lane planning package
- **Task IDs:** `AEC-T011`, `AEC-T016`
- **Purpose:** define the future bounded verifier whitelist / refusal / artifact-schema lane
- **Required future evidence:** `scripts/tests/test_aec_z3_compiler.py`, `scripts/tests/test_aec_z3_replay.py`, `scripts/tests/test_aec_z3_refusals.py`, `scripts/tests/test_aec_z3_artifacts.py`
- **Guardrails:** this is planning-grade only; vault truth law must already be frozen before execution; raw prose and geometry-heavy search stay out

### WP-6 — Slice consolidation / anti-sprawl gate
- **Task IDs:** `AEC-T020`, `AEC-T020A`
- **Purpose:** preserve the candidate slice shape and prevent scope creep
- **Outputs to demand later:** true sprint-plan conversion only after blockers close, explicit no-go mapping, refusal language
- **Guardrails:** cannot close `AEC-T020`; cannot silently absorb `AEC-T017`, `AEC-T018`, or `AEC-T019`

## 7. Future evidence doctrine to pre-bind
### Test families
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

### Fixture doctrine
- strict + invalid boundary fixtures
- ECS replay fixtures
- bounded spatial fixtures
- verifier sat / unsat / timeout / unsupported-family fixtures
- benchmark doctrine cited only; no Rust execution authorization

### File-touch doctrine
- `scripts/vitruvius/aec/*` = future direct-target references only
- `scripts/vitruvius/spatial/*` and `spatial-daemon/*` = precedent-only or boundary-limited per matrix
- Rust excluded from authority logic
- TypeScript remains boundary-only

## 8. Why this is the safest bounded candidate
- it matches the likely `AEC-T020` shape without claiming `AEC-T020` is done
- it keeps the slice narrow and deterministic
- it addresses boundary/replay/parity/verifier risk before downstream expansion
- it keeps open blockers visible instead of turning them into background assumptions

## Plan Critique
- **Architect steelman antithesis:** keep the first artifact as a gate-closure proof package only, because any slice language risks implying readiness.
- **Tradeoff tension:** if the artifact stops at gate proof only, the future first slice stays vague; if it gets too concrete, it risks sounding executable before the repo is ready.
- **Synthesis:** keep the boundary-to-reference-world spine, but label it as a blocked candidate; foreground blocker truth; demote verifier scope to planning-grade whitelist/refusal/schema design.
- **Critic verdict:** APPROVE.
- [C001] Do not convert open freeze tasks into implied completed work.
- [C002] Do not let TypeScript own policy, units, tolerance, or routing semantics.
- [C003] Do not let verifier scope imply finished vault truth law or execution readiness.
- [C004] Do not let `AEC-T020` appear closed by the existence of this plan.
- [C005] Do not lose `AEC-T008` or `AEC-T010A` when moving from freeze-stack planning to slice-shape planning.

## Execution Checklist
- [G001] Treat this file as planning-only until blockers are verifiably closed.
- [G002] Verify `G1`–`G8` are closed before creating runtime files.
- [G003] Verify `AEC-T001`–`AEC-T011` and `AEC-T020A` are closed before proposing a true sprint plan.
- [G004] Keep pricing, optimization, coordination, and tooling out of the first slice.
- [G005] Preserve Python authority; keep Rust benchmarked-only and TypeScript boundary-only.
- [G006] Require explicit artifact citations for any future claim that blocker status changed.

## Available Agent Types Roster
- `planner` — maintain plan truth and execution sequencing
- `architect` — guard boundaries and subsystem coupling
- `executor` — future bounded implementation work once blockers close
- `verifier` — validate blocker closure and later completion evidence
- `test-engineer` — future targeted pytest / npm verification lanes
- `build-fixer` — future failure repair inside bounded scope
- `code-reviewer` — future cross-scope review before merge
- `writer` — keep validation and handoff artifacts truthful

## Follow-up staffing guidance
### If later executing via `ralph`
- use one owner only after blockers close
- sequence: gate-proof validation -> true sprint-plan conversion -> boundary -> ECS -> spatial -> verifier -> validation
- reasoning: high for planning, implementation, and verification

### If later executing via `team`
Suggested lanes only after blockers close and a true sprint plan exists:
1. boundary/contracts lane
2. ECS/fixtures lane
3. spatial/verifier lane
4. verification lane

## Launch hints
These are **future** hints, not current instructions:
- `ralph`: `$ralph "Execute the future sprint converted from .ai/03_plans/2026-04-16-aec-first-bounded-slice-pre-implementation-plan.md only after blocker closure is verified"`
- `team`: `$team "Execute the future sprint converted from .ai/03_plans/2026-04-16-aec-first-bounded-slice-pre-implementation-plan.md only after blocker closure is verified"`

## Team verification path (future)
1. verifier confirms blocker closure with artifact citations
2. planner/executor converts this candidate into a true sprint plan
3. boundary evidence lane proves strict contract behavior
4. ECS evidence lane proves deterministic world/snapshot/schedule behavior
5. spatial evidence lane proves bounded facts and parity doctrine
6. verifier evidence lane proves whitelist/refusal/artifact behavior
7. final verifier confirms scope discipline and writes the validation log

## Final rule
This plan is approved as a **pre-implementation candidate only**. It narrows the future first slice; it does not authorize code and it does not close `AEC-T020`.
