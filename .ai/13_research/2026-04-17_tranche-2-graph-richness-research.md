---
task: tranche-2-graph-richness
phase: 11
created: 2026-04-17
author: CODEX
status: DRAFT
---

# 2026-04-17 Tranche-2 Graph Richness Research

## Question
What is the next truthful step after tranche-2 execute succeeded but produced a sparse graph?

## Fresh evidence
Latest tranche-2 execute:
- staged laws:
  - `RA-7279`
  - `RA-4726`
  - `RA-7899`
- graph result:
  - `node_count = 3`
  - `edge_count = 0`
- generated relationship count from execute summary:
  - `0`

Source-level evidence:
- `urban-development-and-housing-act.md`
  - referenced concepts: none
- `condominium-act.md`
  - referenced concepts: none
- `amendments-to-the-condominium-act.md`
  - referenced concepts:
    - `concept-floor-area`
- tranche-2 review artifacts:
  - all three `_review.json` files currently show zero admitted candidates

## Meaning
Tranche-2 is a successful bounded execute lane, but not yet a rich knowledge-graph slice.

The smallest truthful next move is **not** tranche-3 first.
The smallest truthful next move is a **tranche-2 concept-fit slice**.

## Best starting point
`RA-7899` looks like the smallest entry point because:
- it already resolves at least one existing shared concept (`floor-area`)
- it is narrower than `RA-7279`
- it is an amendment companion to `RA-4726`, so it can stay bounded

## Recommended order
1. start with a minimal `RA-7899` concept-fit slice
2. if successful, consider `RA-4726` as the next tranche-2 richness follow-on
3. defer `RA-7279` until concept-fit is clearer
