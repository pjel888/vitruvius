---
task: aec-engine-gates-spec
phase: 00
created: 2026-04-16
author: PLANNER
supersedes: null
status: ACCEPTED
---

# AEC Engine Gates Spec

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
This is the human-readable companion to `.ai/04_tasks/aec-engine-gates.schema.json`. It explains how the machine-readable readiness gate artifact should be authored, reviewed, and consumed.

## Artifact Pair
- schema → `.ai/04_tasks/aec-engine-gates.schema.json`
- instance documents → future gate-state JSON files produced as AEC planning matures

## Core Objects

### `global_blockers`
Use one object per blocker-class gate.
Required fields:
- `id`
- `name`
- `status`
Optional fields:
- `blocks`
- `required_fields`

### `subsystem_gates`
Use one object per AEC subsystem.
Required fields:
- `entry_requires`
- `exit_requires`
- `ready`

### `required_test_families`
List every named AEC test family required before implementation readiness can be claimed.

### `hard_stop_conditions`
List execution blockers in machine-readable slug form.

## Authoring Rules
- `ready_to_implement` must remain `false` until the readiness gate actually closes.
- `waived` blocker status should be exceptional and must be backed by explicit governance artifacts, not convenience.
- subsystem `ready: true` does not authorize implementation by itself; it only indicates the subsystem’s planning gate is satisfied.

## Review Rules
- Review the gate file against the strengthened audit and the master execution task list.
- Reject any gate file that marks a blocker `closed` without corresponding evidence artifacts.
- Reject any gate file that lacks named test families for a subsystem with a crossed seam.

## Example Uses
- planning review dashboard
- implementation-sprint go/no-go checklist generation
- future CI or policy checks against planning state

## Final Rule
The machine-readable gate artifact is a control surface, not a marketing surface. If it says `ready_to_implement: true`, that statement must be auditable.
