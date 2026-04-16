---
task: aec-first-slice-session-packet
phase: 00
created: 2026-04-16
author: PLANNER
supersedes: null
status: ACCEPTED
---

# AEC First-Slice Session Packet

## Purpose
This is the compact operator-facing session checklist for the future bounded first-slice implementation run.

## Open first
1. `.ai/04_tasks/aec-first-slice-execution-handoff-dossier-2026-04-16.md`
2. `.ai/03_plans/2026-04-16-aec-first-bounded-slice-sprint-plan.md`
3. `.ai/04_tasks/2026-04-16-aec-first-bounded-slice-implementation-trigger.md`
4. `.ai/04_tasks/aec-g10-closure-criteria-2026-04-16.md`

## Verify before coding
Primary preflight: `.ai/04_tasks/aec-clean-baseline-toolchain-preflight-2026-04-16.md`
Resume gate after conflict: `.ai/04_tasks/aec-resume-after-deferral-checklist-2026-04-16.md`
- baseline worktree is `/Users/philiplewis/vitruvius-aec-clean-baseline`
- gate artifact still says `ready_to_implement=false` only because G10 evidence is absent
- all expected test and fixture scaffolds now exist before claiming G10 closure
- no conflicting Codex task is still active on overlapping repo surfaces (`.ai/04_tasks/aec-concurrent-execution-deferral-and-write-scope-2026-04-16.md`)
- adjacent-surface toolchain readiness is checked (`.ai/00_performance/2026-04-16_aec-first-slice-adjacent-surface-baseline-observations.md`)

## Execute in order
1. contracts + boundary
2. boundary fixtures + boundary tests
3. ECS
4. ECS fixtures + ECS tests
5. spatial
6. spatial fixtures + spatial tests
7. verification
8. verification fixtures + verification tests
9. artifact-root inspection
10. validation log
11. G10 closure check

## Watch for immediate stop conditions
Also consult `.ai/04_tasks/aec-first-slice-assumptions-and-invalidation-ledger-2026-04-16.md` when new evidence threatens bounded-slice assumptions.
Also consult `.ai/04_tasks/aec-first-slice-blast-radius-map-2026-04-16.md` when a change touches any adjacent or precedent file.
- TypeScript policy creep
- Rust-first drift
- downstream subsystem spillover
- output-path drift outside candidate/admitted/promotion roots
- missing validation evidence
- incidental remediation outside the bounded blast-radius protocol (`.ai/04_tasks/aec-incidental-remediation-and-blast-radius-matrix-2026-04-16.md`)

## Evidence to collect before leaving the session
- final go/no-go review decision from `.ai/04_tasks/aec-first-slice-gonogo-review-checklist-2026-04-16.md`
- exact git commit
- exact pytest outputs for all four command groups
- exact artifact roots inspected
- exact validation log path
- execution journal entry path (`.ai/05_logs/aec-first-slice-execution-journal-template-2026-04-16.md`)
- explicit G10 closure verdict

## Final rule
This packet is the smallest operator checklist that should be open during the future first-slice execution run. It does not close G10 by itself.
