---
task: aec-first-slice-assumptions-and-invalidation-ledger
phase: 00
created: 2026-04-16
author: PLANNER
supersedes: null
status: ACCEPTED
---

# AEC First-Slice Assumptions and Invalidation Ledger

## Purpose
This ledger records the bounded assumptions the first-slice plan depends on and what evidence would invalidate them.

| Assumption ID | Assumption | Why it matters | Invalidate if | Required response |
|---|---|---|---|---|
| A-001 | The first slice remains strictly limited to boundary + ECS + spatial + verification | preserves bounded scope | pricing/optimization/coordination/tooling becomes required to finish the slice | stop and return to planning review |
| A-002 | Clean baseline worktree remains the execution source of truth | prevents dirty-branch ambiguity | clean baseline disappears, diverges unexpectedly, or is no longer conflict-safe | re-establish baseline before coding |
| A-003 | Candidate/admitted/promotion root split remains sufficient for the first slice | preserves artifact governance | outputs require a different root contract or mixed storage semantics | stop and update artifact-shape / freeze docs first |
| A-004 | Boundary stays import-first | preserves boundedness and avoids boundary sprawl | export breadth or orchestration behavior becomes required | stop and return to planning review |
| A-005 | TypeScript stays boundary-only and Rust stays out of first-slice ownership | preserves ownership law | policy or truth logic must move into TS/Rust to make the slice work | stop and escalate to planning/architecture review |
| A-006 | Named `test_aec_*` and fixture families are sufficient to prove the bounded slice | preserves the proof contract | new unavoidable evidence classes appear | extend G10 scaffold docs before claiming closure |
| A-007 | The bounded first slice can be verified without downstream subsystem execution | preserves sequencing | verification depends on pricing/coordination/tooling outputs | stop and revisit sprint scope |
| A-008 | Existing adjacent precedent files are enough for reference and limited incidental fixes | limits blast radius | a precedent-only file becomes a required runtime home | stop and revise the file-touch matrix / sprint plan |

## Use during execution
- check this ledger when new evidence appears
- if an assumption is weakened or broken, record it in the validation log
- do not “absorb” invalidated assumptions silently into the sprint

## Final rule
This ledger exists so future execution can fail honestly instead of pretending the bounded assumptions were still true.
