---
task: laws-tranche-4-expansion
created: 2026-04-17
status: complete
---

# Research — Tranche-4 expansion

## Goal
Select the next bounded tranche after tranche-3 reaches a non-shallow execute state.

## Candidate evidence
### Rejected scout set
- `PD-1517`, `RA-11201`, `RA-11285`
- duplicate risk: zero exact duplicate clusters
- rejection reason: `RA-11201` law PDF and `RA-11285` both require OCR-first handling, so the set is not the cleanest next bounded cohort.

### Preferred scout set
- `PD-1517`
- `RA-6969`
- `RA-10066`
- duplicate risk: zero exact duplicate clusters
- readiness: all three are direct text-PDF / `OPENDATALOADER_DIRECT`
- structure: each law folder is compact and single-law scoped

## Recommendation
Use `PD-1517`, `RA-6969`, and `RA-10066` as the tranche-4 manifest because they preserve the bounded direct-text path without introducing immediate OCR debt.
