---
task: aec-first-slice-failure-triage
phase: 03
created: 2026-04-16
author: PLANNER
supersedes: null
status: ACCEPTED
---

# Research — AEC First-Slice Failure Triage

## Purpose
Freeze a bounded failure-triage model for the first slice so the later implementation phase knows how to respond to the most likely failures without widening scope.

## Conclusion
The bounded first slice needs an explicit triage matrix for failures in:
- boundary inputs
- ECS replay/schedule
- spatial contract/parity
- verification whitelist/refusal
- artifact-root and validation-log completeness

This improves later execution discipline but does not close G10.
