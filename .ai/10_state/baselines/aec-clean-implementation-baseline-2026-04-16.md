---
task: aec-clean-implementation-baseline
phase: 02
created: 2026-04-16
author: PLANNER
supersedes: null
status: ACCEPTED
---

# Baseline — AEC Clean Implementation Baseline

## Purpose
Record the clean baseline branch/worktree that future AEC execution must use so implementation does not mix with unrelated branch-local changes.

## Clean baseline identity
- baseline branch: `aec/clean-baseline-20260416`
- baseline worktree: `/Users/philiplewis/vitruvius-aec-clean-baseline`
- baseline commit: `c4f1f07`
- baseline status proof: `git -C /Users/philiplewis/vitruvius-aec-clean-baseline status --short --branch` returned only `## aec/clean-baseline-20260416`

## Excluded dirty-scope items from the source branch
The source branch `ralph/laws-dataset-phases` currently contains unrelated or not-yet-isolated changes and must not be treated as the execution baseline for AEC implementation:
- tracked modifications in `README.md`, `scripts/pipeline_cli.py`, and active planning index/state files
- untracked AEC planning/control artifacts awaiting normal repo commit flow
- unrelated generated/runtime outputs under dataset graph/report paths

## Rule
Any future AEC execution trigger must reference this clean baseline branch/worktree (or a later equally clean superseding baseline) rather than the dirty source branch.
