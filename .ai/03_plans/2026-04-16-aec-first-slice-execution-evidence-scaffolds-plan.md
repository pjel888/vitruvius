---
task: aec-first-slice-execution-evidence-scaffolds
phase: 05
created: 2026-04-16
author: PLANNER
supersedes: null
status: accepted
implementation_blocked: true
planning_gate_ready: true
subsystem_ready: false
execution_role: first-slice-evidence-handoff
---

# AEC First-Slice Execution Evidence Scaffolds Plan

## Purpose
Define the exact file-by-file execution-evidence scaffolds required to clear G10 for the bounded first slice.

## Outputs
- one scaffold map naming every missing test file
- one fixture-to-test responsibility contract
- one command matrix for future verification
- one artifact-output map for replay/admitted/promotion surfaces

## Non-goal
This plan does not create tests, fixtures, or runtime code.

## Gate effect
Completing this plan improves execution handoff quality, but G10 remains open until the named scaffolds exist on the clean baseline branch/worktree.


## Companion task artifact
- `.ai/04_tasks/aec-first-slice-module-order-and-fixture-shapes-2026-04-16.md`


## Companion verification runbook
- `.ai/04_tasks/aec-first-slice-verification-runbook-2026-04-16.md`
