---
task: ra7899-concept-fit-admission
phase: 11
created: 2026-04-17
author: CODEX
status: DRAFT
---

# 2026-04-17 RA-7899 Concept-Fit Admission Research

## Question
What is the smallest truthful graph-richness slice inside tranche-2 after tranche-2 execute succeeded but produced zero edges?

## Fresh evidence
- tranche-2 execute stages:
  - `RA-7279`
  - `RA-4726`
  - `RA-7899`
- tranche-2 graph result:
  - `node_count = 3`
  - `edge_count = 0`
- current tranche-2 source evidence:
  - `urban-development-and-housing-act.md` → referenced concepts: none
  - `condominium-act.md` → referenced concepts: none
  - `amendments-to-the-condominium-act.md` → referenced concepts:
    - `concept-floor-area`

## Why RA-7899 is the smallest starting point
- it already resolves one existing shared concept (`floor-area`)
- it stays inside the current tranche
- it is narrower than `RA-7279`
- it is closely adjacent to `RA-4726`, so it can become the first bounded richness anchor for the condominium-law lane

## Smallest candidate slice
1. admit existing shared concept:
   - `003_Canonical-Knowledge-Layer/shared/concepts/floor-area.md`
2. admit one dataset-scoped source→concept relationship:
   - `law-amendments-to-the-condominium-act governs concept-floor-area`
3. rerun tranche-2 source-to-graph dry-run / execute

## Expected effect
- tranche-2 should move from a pure source-only graph toward at least one admitted edge
- this keeps the follow-on bounded and auditable before attempting richer `RA-4726` or `RA-7279` slices
