---
task: aec-engine-bounded-implementation-planning
phase: 00
created: 2026-04-16
author: PLANNER
supersedes: null
status: ACCEPTED
---

# Trigger — AEC Engine Bounded Implementation Planning

## Task Statement
Create the next bounded AEC implementation plan using the enterprise-grade AEC control package, without starting production implementation.

## In Scope
- creation of the next bounded implementation-planning artifact for the first safe AEC slice
- use of the readiness audit, task list, traceability matrix, subsystem gates, touch matrix, gate schema/state, and language-boundary blacklists as controlling inputs
- planning-only SEL artifacts required to shape the first bounded implementation slice safely
- refinement of task sequencing, tests, fixtures, parity lanes, benchmarks, and stop conditions for that first bounded implementation slice

## Out of Scope
- AEC production code
- creation of `scripts/vitruvius/aec/*` runtime modules
- Rust acceleration implementation
- TypeScript feature implementation beyond planning references
- widening into pricing, optimization, coordination, and tool-calling implementation unless the bounded slice explicitly and safely requires planning references to them

## Identity-Locked File Check
- `AGENTS.md`: read-only authority
- `.ai/00_system/EXECUTION_LOOP.md`: read-only authority
- `.ai/00_system/principles.md`: read-only authority
- `.ai/03_plans/00-governing-implementation-plan.md`: read-only authority unless truthful dispatcher alignment is required
- `.ai/01_roadmap/*`: read-only state authority unless direct reconciliation is required by the planning work

## Risk Class
- `L` — governance-critical multi-artifact planning work with direct effect on future AEC implementation sequencing and safety

## Roles
- PLANNER: Codex
- AUDITOR: Codex + review artifacts
- IMPLEMENTER: planning-artifact only, no runtime code
- REVIEWER: architect-style review before acceptance of the resulting bounded implementation plan
- STEWARD: Codex

## Linked Prior Artifacts
- `.ai/02_audits/AEC_ENGINE_WHOLE_CODEBASE_READINESS_AUDIT_2026-04-16.md`
- `.ai/04_tasks/aec-engine-master-execution-task-list-2026-04-16.md`
- `.ai/04_tasks/aec-engine-traceability-matrix-2026-04-16.md`
- `.ai/04_tasks/aec-engine-subsystem-gates-2026-04-16.md`
- `.ai/04_tasks/aec-engine-file-touch-matrix-2026-04-16.md`
- `.ai/04_tasks/aec-engine-gates.schema.json`
- `.ai/04_tasks/aec-engine-gates-spec-2026-04-16.md`
- `.ai/04_tasks/aec-engine-gates-state-2026-04-16.json`
- `.ai/04_tasks/aec-engine-language-boundary-blacklists-2026-04-16.md`
- `.ai/03_plans/templates/aec-engine-first-sprint-template.md`
- `.ai/04_tasks/aec-engine-control-artifacts-README-2026-04-16.md`

## MCP / Intelligence Precheck
- code-review-graph / GitNexus-first exploration remains required where available
- this trigger opens planning only; it does not authorize implementation regardless of current tool availability

## Trigger Gate
This trigger is accepted for planning work only. It does **not** close the current AEC implementation blockers.

## Mandatory Control Inputs
The next bounded implementation-planning artifact must:
- reconcile against the live gate-state JSON
- cite exact task IDs from the master task list
- obey subsystem entry/exit gates
- obey file touch classes
- obey Rust/TypeScript blacklists
- use the first sprint template as the planning scaffold

## Hard Stops Inherited Into The Planning Task
Stop the bounded implementation-planning task if:
- it attempts to authorize coding while blockers remain open
- it widens the first bounded slice into multiple downstream subsystems unnecessarily
- it assumes any unresolved freeze is already solved
- it proposes Rust or TypeScript ownership that violates the blacklists
- it omits required tests, parity lanes, replay fixtures, or benchmark doctrine where required

## Definition of Success For This Trigger
Success means the next SEL artifact chain produces a bounded, implementation-ready **plan** for the first AEC slice — not code.
