---
task: aec-first-bounded-slice
phase: 02
created: 2026-04-16
author: PLANNER
supersedes: null
status: ACCEPTED
---

# Baseline — AEC First Bounded Slice (Pre-Implementation Candidate)

## Scope Baseline
This baseline anchors a **planning-only, blocked pre-implementation candidate** for the first bounded AEC slice. It does not authorize runtime implementation and it does not close `AEC-T020`.

## Governing Inputs Read
- `AGENTS.md`
- `.ai/00_system/EXECUTION_LOOP.md`
- `.ai/00_system/principles.md`
- `.ai/01_roadmap/master-roadmap.md`
- `.ai/01_roadmap/current-phase.md`
- `.ai/01_roadmap/milestone-tracker.md`
- `.ai/03_plans/00-governing-implementation-plan.md`
- `.ai/03_plans/INDEX.md`
- `.ai/04_tasks/aec-engine-bounded-implementation-planning-trigger.md`
- `.ai/02_audits/AEC_ENGINE_WHOLE_CODEBASE_READINESS_AUDIT_2026-04-16.md`
- `.ai/04_tasks/aec-engine-master-execution-task-list-2026-04-16.md`
- `.ai/04_tasks/aec-engine-traceability-matrix-2026-04-16.md`
- `.ai/04_tasks/aec-engine-subsystem-gates-2026-04-16.md`
- `.ai/04_tasks/aec-engine-file-touch-matrix-2026-04-16.md`
- `.ai/04_tasks/aec-engine-language-boundary-blacklists-2026-04-16.md`
- `.ai/04_tasks/aec-engine-gates-state-2026-04-16.json`
- `.ai/03_plans/templates/aec-engine-first-sprint-template.md`

## Current Repo Truth
- AEC remains planning-only; `ready_to_implement` is `false`.
- `G1` through `G8` remain open; only `G0` and `G9` are closed.
- `AEC-T006` clean baseline is still unresolved because the working tree contains uncommitted planning/control artifacts.
- There is still no `scripts/vitruvius/aec/` runtime code root.
- No subsystem gate is ready.

## Planning Baseline Decision
The accepted next artifact is a **blocked pre-`AEC-T020` bounded-slice candidate plan**. The candidate shape is the narrow boundary-to-reference-world spine:
- one bounded DTO family
- one strict boundary import lane
- one Python reference ECS world
- one bounded spatial fixture lane
- one verifier whitelist / refusal / artifact-schema lane

This candidate excludes pricing, optimization, coordination, and LLM tooling and must not be mistaken for a sprint plan.

## Baseline No-Go Rules
Stop if the planning artifacts:
- imply implementation readiness while `ready_to_implement=false`
- treat open upstream tasks as completed
- widen the slice into downstream subsystems
- assign policy or truth authority to Rust or TypeScript
