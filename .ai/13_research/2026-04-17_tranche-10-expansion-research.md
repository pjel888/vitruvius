---
task: laws-tranche-10-expansion
created: 2026-04-17
status: complete
---

# Research — Tranche-10 expansion

## Goal
Resolve the next strongest remaining blocker after tranche-9: the duplicate-heavy `RA-9266` folder.

## Evidence
- duplicate cluster count for `RA-9266`: 1
- duplicate raw files:
  - `IRR of RA 9266.pdf`
  - `RA-9266 IRR Architecture Act of 2004.pdf`
- both files share the same SHA-256 and the same first-page content
- semantic flag from readiness: `conflicting_law_irr_filename_semantics`

## Smallest truthful lane
Use a singleton tranche-10 for `RA-9266` with:
- one authoritative variant path
- one explicit excluded duplicate alias path
- conservative canonical admission to a single authoritative IRR source page
