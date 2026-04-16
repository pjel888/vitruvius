---
task: aec-clean-baseline-toolchain-preflight
phase: 00
created: 2026-04-16
author: PLANNER
supersedes: null
status: ACCEPTED
---

# AEC Clean-Baseline Toolchain Preflight

## Purpose
This checklist is the environment/tooling preflight for future bounded first-slice execution from the clean baseline worktree.

## Required checks
### Baseline identity
- correct worktree: `/Users/philiplewis/vitruvius-aec-clean-baseline`
- clean `git status --short --branch`

### Python lane
- `python3 -m pytest --version`
- Python test runner available

### TypeScript adjacent lane
- `spatial-daemon/node_modules` present or install path explicitly handled
- `vitest` available through local toolchain
- `npm run typecheck` available

### Bounded evidence presence
- bounded `test_aec_*` files exist
- bounded fixture roots exist

### Conflict check
- no overlapping active Codex task is still touching adjacent or direct-target write scopes

## Refusal rule
If any preflight item fails, do not start execution. Fix or record the environment gap first.

## Final rule
Preflight should fail fast before coding, not after partial implementation work has already begun.


## Companion remediation guide
- `.ai/04_tasks/aec-clean-baseline-toolchain-remediation-guide-2026-04-16.md`


## Companion dependency manifest
- `.ai/04_tasks/aec-execution-dependency-manifest-2026-04-16.md`
