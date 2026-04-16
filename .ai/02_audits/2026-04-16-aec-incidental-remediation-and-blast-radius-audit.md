---
task: aec-incidental-remediation-and-blast-radius
phase: 04
created: 2026-04-16
author: AUDITOR
supersedes: null
status: ACCEPTED
---

# Audit — AEC Incidental Remediation and Blast Radius

## Verdict
Planning GO.

## Audit conclusion
The first bounded slice is now tight enough that incidental fixes are a bigger risk than missing planning. A dedicated protocol is justified so teams do not silently widen scope while chasing breakages.

## Guardrails
- direct-target AEC files may be fixed in the sprint when truly required to unblock the slice
- boundary-adjacent files require explicit blast-radius check + targeted regressions
- precedent-only and unrelated files should default to separate follow-on artifacts unless the sprint is genuinely blocked
- no incidental remediation may bypass the candidate/admitted/promotion path contract or the boundary-only / Rust-only ownership laws
