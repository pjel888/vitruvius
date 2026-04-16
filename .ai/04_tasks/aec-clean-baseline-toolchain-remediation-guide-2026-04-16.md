---
task: aec-clean-baseline-toolchain-remediation-guide
phase: 00
created: 2026-04-16
author: PLANNER
supersedes: null
status: ACCEPTED
---

# AEC Clean-Baseline Toolchain Remediation Guide

## Purpose
This guide defines the bounded remediation path when the clean-baseline toolchain preflight fails.

## Python lane remediation
If `python3 -m pytest --version` fails:
1. confirm Python environment selection
2. restore/install the expected Python test tooling
3. re-run the Python preflight check before attempting bounded tests

## TypeScript adjacent-lane remediation
If `spatial-daemon` smoke checks fail because `vitest` or node dependencies are unavailable:
1. inspect whether `node_modules/` is present
2. inspect whether the expected package manager lockfile is present
3. restore/install the bounded `spatial-daemon` dependencies
4. re-run `npm test` and `npm run typecheck`
5. record the result in the execution journal / validation log

## Boundedness rule
Toolchain remediation must stay limited to making the declared smoke lane runnable. It must not become a broader frontend/toolchain cleanup effort.

## Refusal rule
If toolchain remediation would require broad workspace churn, pause execution and return to planning/review rather than forcing progress.

## Final rule
A failed preflight should trigger bounded remediation, not improvisation.


## Companion dependency manifest
- `.ai/04_tasks/aec-execution-dependency-manifest-2026-04-16.md`
