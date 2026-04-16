---
task: aec-t017-coordination-foundation
phase: 05
created: 2026-04-16
author: PLANNER
supersedes: null
status: accepted
implementation_blocked: true
planning_gate_ready: true
subsystem_ready: false
execution_role: downstream-not-selected-for-first-slice
paired_subsystem_plan: AEC_ENGINE_MULTI_DISCIPLINARY_COORDINATION_IMPLEMENTATION_PLAN.md
gate_key: coordination
---

# AEC-T017 Coordination Foundation Plan

## Planning Status
- planning gate: ready
- execution selection: downstream / not in first bounded slice
- interpretation: planning readiness is satisfied, but execution evidence is still pending and the subsystem is not selected for the current bounded sprint

## Purpose
Resolve `AEC-T017` at the planning layer by defining the accepted coordination foundation package while keeping implementation blocked.

## Required outputs
- precedence manifest defined
- replay log defined
- escalation states defined
- discipline enum and issue schema defined
- oscillation/cascade bounds defined

## Required future tests
- `scripts/tests/test_aec_coordination_precedence.py`
- `scripts/tests/test_aec_coordination_replay.py`
- `scripts/tests/test_aec_coordination_escalation.py`
- `scripts/tests/test_aec_coordination_oscillation.py`

## Stop conditions
- replay/audit log undefined
- precedence implicit
- oscillation unbounded
- coordination replaces verification or optimization
