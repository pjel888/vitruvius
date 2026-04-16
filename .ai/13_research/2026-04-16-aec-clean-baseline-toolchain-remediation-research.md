---
task: aec-clean-baseline-toolchain-remediation
phase: 03
created: 2026-04-16
author: PLANNER
supersedes: null
status: ACCEPTED
---

# Research — AEC Clean-Baseline Toolchain Remediation

## Purpose
Turn the observed toolchain gaps in the clean baseline environment into an explicit remediation guide for future execution.

## Key observed gap
The adjacent TypeScript smoke lane was not immediately runnable because `vitest` was not found in the clean baseline environment.

## Conclusion
Execution should carry a bounded remediation guide for:
- Python test-runner availability
- `spatial-daemon` dependency/toolchain availability
- how to confirm remediation succeeded before trusting smoke checks
