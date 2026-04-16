---
task: aec-readiness-vocabulary-and-state-model
phase: 00
created: 2026-04-16
author: PLANNER
supersedes: null
status: ACCEPTED
---

# AEC Readiness Vocabulary and State Model

## Purpose
This artifact defines the canonical vocabulary and allowed transitions for AEC planning/control status claims.

## Canonical terms

### `historical checkpoint`
Meaning:
- retained for lineage
- not current live execution truth

Use for:
- pre-implementation candidate artifacts after sprint conversion
- intermediate freeze/checkpoint artifacts after later normalization

### `planning_gate_ready`
Meaning:
- planning/specification requirements for a surface are satisfied
- runtime evidence may still be absent

### `baseline-ready`
Meaning:
- a clean execution branch/worktree exists
- dirty working-tree ambiguity has been removed for execution startup

### `evidence-pending`
Meaning:
- required tests, fixtures, commands, or validation outputs do not yet exist or have not yet been run successfully

### `execution-ready`
Meaning:
All of the following are true:
- planning gates satisfied
- baseline-ready
- required execution evidence exists
- required verification commands pass
- validation report exists

## Allowed transitions
- planning-only -> planning_gate_ready
- planning_gate_ready -> baseline-ready
- baseline-ready -> evidence-pending
- evidence-pending -> execution-ready

## Forbidden transitions
- planning-only -> execution-ready
- baseline-ready -> execution-ready without evidence
- historical checkpoint -> live readiness source

## Application rules
- machine-readable gate state is the primary live readiness surface
- `ready_to_implement=true` should be used only for `execution-ready`
- sprint plans may be `baseline-ready / evidence-pending`
- downstream foundation plans may be `planning_gate_ready: true` while `subsystem_ready: false`
- historical checkpoint files must say so explicitly when their checkpoint-time truth no longer matches live gate truth

## Final rule
If a doc can be interpreted two ways under this vocabulary, it is not specific enough yet.
