---
task: laws-tranche-5-expansion
created: 2026-04-17
status: complete
---

# Research — Tranche-5 expansion

## Goal
Select the next bounded tranche after tranche-4 reached a non-shallow execute state.

## Candidate evidence
Chosen cohort:
- `PD-856`
- `RA-7160`
- `RA-9257` (file evidence is RA 9275 Clean Water Act under the `RA-9257` folder)

## Why this cohort
- exact duplicate clusters: `0`
- all selected files classify as `TEXT_PDF`
- all selected files use `OPENDATALOADER_DIRECT`
- bounded adjacency:
  - PD-856 sanitation / food-establishment operations
  - RA-7160 local-government permitting / land-use governance context
  - RA-9275 water-quality / environmental compliance

## Known wrinkle
The clean-water folder is named `RA-9257`, but the contained file and law text are RA 9275. The tranche should preserve the folder path while canonicalizing truthfully to the Clean Water Act.
