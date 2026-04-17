---
task: laws-tranche-7-expansion
created: 2026-04-17
status: complete
---

# Research — Tranche-7 expansion

## Goal
Select the next bounded tranche after tranche-6 maturity.

## Rejected scout cohort
- `RA-4566`
- `RA-386`
- `RA-9184`
- reason: already covered in tranche-6

## Rejected scout nuance
- `RA-9266` remains deferred because of duplicate risk
- `PD-9514` overlaps the already-covered Fire Code IRR lane

## Chosen tranche-7 cohort
- `RA-1378`
- `RA-9285`
- `RA-11201`

## Why
- duplicate cluster count: `0`
- direct-input prep path exists for all selected raw files, with one expected OCR-first path only for the RA-11201 law PDF
- built-environment / governance adjacency remains coherent:
  - plumbing law / professional regulation
  - ADR dispute resolution for contracts/projects
  - DHSUD governance law + IRR

## Explicit tranche discipline
- `RA-1378` should admit only the statute as authoritative in tranche-7
- supporting plumbing-code / board-resolution files stay explicit and excluded
- `RA-11201` tranche execution should use OCR-first prep for the law PDF and direct prep for the IRR PDF
