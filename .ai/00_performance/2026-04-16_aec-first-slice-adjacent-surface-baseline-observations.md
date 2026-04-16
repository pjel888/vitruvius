---
task: aec-first-slice-adjacent-surface-baseline-observations
date: 2026-04-16
author: PLANNER
status: ACCEPTED
---

# AEC First-Slice Adjacent-Surface Baseline Observations

## Scope
Bounded baseline experimentation on adjacent surfaces that the first slice may rely on or touch as unblockers.

## Hardware / environment note
These observations were gathered from the clean baseline worktree, but they should be treated as environment observations rather than benchmark-grade performance claims.

## Observations
### 1. Clean baseline worktree exists
- branch/worktree: `aec/clean-baseline-20260416`
- path: `/Users/philiplewis/vitruvius-aec-clean-baseline`
- status: clean

### 2. Bounded-slice evidence is still absent
Spot-check confirms the clean baseline still lacks core bounded-slice tests and fixture roots.
This is the main reason `G10` remains open.

### 3. `spatial-daemon` test lane is not immediately runnable in the current environment
Observed command:
- `npm test -- --runInBand`

Observed result:
- return code: `127`
- `vitest: command not found`

Interpretation:
- the clean baseline does not automatically imply all execution dependencies are present in the current environment
- future execution should treat dependency/tool availability as part of preflight before trusting TS-adjacent smoke lanes

## Planning consequence
Before first-slice execution resumes, preflight should verify:
- Python test runner availability
- `spatial-daemon` test toolchain availability (`vitest`, node_modules or equivalent install state)
- no conflict with the active parallel Codex task

## Caveat
These are readiness observations, not optimization benchmarks. They help reduce wasted execution attempts more than they help compare runtime performance.
