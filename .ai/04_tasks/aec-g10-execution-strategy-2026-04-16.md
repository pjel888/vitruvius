---
task: aec-g10-execution-strategy
phase: 00
created: 2026-04-16
author: PLANNER
supersedes: null
status: ACCEPTED
---

# AEC G10 Execution Strategy

## Purpose
This artifact answers one operational question: how the bounded first slice should actually clear `G10` once execution is allowed.

## Current truth
- `G10` is the only remaining open blocker.
- `G10` is an execution-evidence blocker, not a planning blocker.
- A clean baseline exists, but the required bounded-slice tests and fixtures do not yet exist there.
- Execution is currently deferred while another Codex task may conflict on overlapping repo surfaces.

## Strategy
1. Wait until the conflicting Codex task is finished or clearly non-overlapping.
2. Resume from the clean baseline worktree only.
3. Follow the bounded G10 work order:
   - create `test_aec_*` skeletons
   - materialize bounded first-slice fixtures
   - implement only the runtime files required by those tests
   - run the four bounded pytest groups
   - inspect candidate/admitted/promotion artifact roots
   - populate the validation template and G10 evidence packet
4. Close `G10` only if the closure criteria artifact is fully satisfied.

## Non-strategy
Do not try to clear `G10` by:
- adding more planning prose
- widening scope into downstream subsystems
- starting from the dirty planning branch
- skipping the evidence packet or validation template

## Final rule
`G10` clears through bounded execution proof, not through additional planning alone.
