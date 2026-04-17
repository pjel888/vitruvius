---
task: laws-tranche-8-scout
created: 2026-04-17
status: complete
---

# Research — Tranche-8 scout

## Goal
Identify the safest next widening move after the 2026-04-17 tranche-7 branch state.

## Tranche-7 truth checkpoint
- `RA-1378` is **not** a cleanly blocked-prep law anymore.
- The authoritative statute path (`MASTER PLUMBING LAW.pdf`) was prepared and admitted to `003_Canonical-Knowledge-Layer/shared/sources/plumbing-law.md`.
- The law family still stays out of tranche-7 staged source-to-graph because the excluded `Board of Master Plumber.doc` file fails prep, leaving `source_admission_state = admitted_subset_failed` and `blocked_law_folders = [RA-1378]` in source-to-graph reports.

## Safest next move
- No clean three-law tranche-8 cohort is currently evidenced in-repo.
- The safest next bounded scout is a **singleton `RA-11285` probe**, not a full tranche-8 manifest.

## Why `RA-11285`
- latest raw registry shows a single repo-local statute PDF:
  - `001-Laws/RA-11285/RA 11285 - Energy Efficiency and Conservation Act 2019.pdf`
- current readiness reports show no duplicate-cluster warning for `RA-11285`
- unlike the deferred alternatives below, it does not currently carry an overlap, duplicate, draft-only, or filename-mismatch warning in the tranche records

## Deferred tranche-8 alternatives
- `RA-9266`
  - defer: current all-laws readiness reports an exact duplicate cluster inside the folder (`IRR of RA 9266.pdf` and `RA-9266 IRR Architecture Act of 2004.pdf`)
- `PD-9514`
  - defer: overlaps the already-covered fire-code lane and was explicitly rejected on the tranche-7 scout pass
- `RA-11361`
  - defer: raw-registry evidence is only `ra_11361_irr_draft_for_comments.pdf`, which is draft-only and weak for authoritative tranche admission
- `RA-9279`
  - defer: raw-registry evidence is only `IRR RA 7279 Sec 18.pdf`, which looks filename-mismatched to the folder identity and should be reviewed before tranche use

## Recommendation
- keep tranche-8 uncommitted for now
- if another bounded widening pass is needed, start with `RA-11285` source-prep/admission scouting first, then rebuild a cohort only after two additional non-duplicate, non-draft, non-overlap candidates are evidenced
