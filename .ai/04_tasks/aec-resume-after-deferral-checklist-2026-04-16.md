---
task: aec-resume-after-deferral-checklist
phase: 00
created: 2026-04-16
author: PLANNER
supersedes: null
status: ACCEPTED
---

# AEC Resume After Deferral Checklist

## Purpose
This is the exact restart checklist once the conflicting Codex task clears.

## Resume only if all are true
1. the other Codex task is finished or clearly non-overlapping
2. `/Users/philiplewis/vitruvius-aec-clean-baseline` still exists and is clean
3. the clean-baseline toolchain preflight passes
4. the gate artifact still reports only `G10` as open
5. no new state drift invalidates the bounded first-slice sprint plan
6. the team resumes from:
   - execution handoff dossier
   - session packet
   - G10 work order
   - G10 closure criteria

## Pause again if any are false
- conflict status is unclear
- baseline is no longer clean
- toolchain preflight fails
- a new blocker appears
- the sprint scope has drifted

## Final rule
Restart should be deliberate and checklist-driven, not opportunistic.
