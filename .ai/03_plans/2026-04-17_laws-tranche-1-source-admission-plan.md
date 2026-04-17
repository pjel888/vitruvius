---
task: laws-tranche-1-source-admission
phase: 11
created: 2026-04-17
author: CODEX
status: DRAFT
supersedes: null
---

# 2026-04-17 Laws Tranche-1 Source Admission Plan

## Objective
Admit tranche-1 sources truthfully from the newly prepared produced-data outputs, while preserving blocked-state clarity for OCR-required members.

## Current tranche members
- `PD-957`
- `PD-1216`
- `PD-1185`

## Current readiness split
### Ready for admission review
- `PD-957`
- `PD-1185`

### Blocked
- `PD-1216`
  - OCR-first path still required

## Required deliverables
1. tranche-1 source admission inventory
2. candidate canonical source pages for the ready tranche members
3. explicit exclusion/blocked note for `PD-1216`
4. tranche-1 admission validation log

## Execution order
1. inspect prepared tranche-1 raw_markdown / refined_markdown / sidecar outputs
2. build/plan canonical source pages for `PD-957` and `PD-1185`
3. classify `PD-1216` as blocked pending OCR outputs
4. update tranche manifest/admission records accordingly
5. then rerun tranche dry-run / tranche source→graph dry-run with the updated tranche state

## Acceptance criteria
- ready tranche members are admitted explicitly
- blocked tranche members remain visible and blocked, not silently discarded
- tranche-1 can be re-evaluated with a truthful mixed-ready state
