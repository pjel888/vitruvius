---
task: pd1185-concept-fit-admission
phase: 11
created: 2026-04-17
author: CODEX
status: DRAFT
---

# 2026-04-17 PD-1185 Concept-Fit Admission Research

## Question
What is the next smallest truthful graph-richness slice after the bounded PD-957 concept-fit pass?

## Fresh evidence
- latest tranche source-to-graph execute:
  - `staged_law_folders = [PD-957, PD-1216, PD-1185]`
  - `generated_relationship_count = 2`
  - graph snapshot nodes/edges remain dominated by `PD-957`
- current admitted concept/relationship coverage:
  - `PD-957` already has a bounded concept-fit slice
  - `PD-1216` has `admitted_concept_count = 0`, but the current source page resolves no shared concepts yet
  - `PD-1185` has `admitted_concept_count = 0`, while its canonical source page already resolves:
    - `concept-means-of-egress`
    - `concept-building-permit`
    - `concept-yards`
- latest `PD-1185` extract also surfaced one direct candidate:
  - `law-fire-code-of-the-philippines governs concept-yards`

## Why PD-1185 is the next smallest slice
- it stays inside the current tranche
- it uses only existing shared concepts
- the admitted Fire Code source already names or resolves those concepts
- it avoids the noisier `PD-1216` concept-selection problem for now

## Source-local evidence
The admitted Fire Code source contains direct governing language for:
- `means-of-egress`
  - “FIRE SAFETY CONSTRUCTIONS ... means of egress ... integral to and incorporated into a building or structure...”
- `building-permit`
  - “... one half to be paid prior to the issuance of the building permit ...”
- `yards`
  - “Constructing gates, entrances and walkways to buildings components and yards which obstruct the orderly and easy passage of fire fighting vehicles and equipment”

## Smallest truthful slice
1. admit three existing shared concepts for `PD-1185`
   - `means-of-egress`
   - `building-permit`
   - `yards`
2. admit matching dataset-scoped `governs` relationship files for those same concepts
3. rerun tranche source-to-graph execute to confirm graph nodes/edges increase without widening scope

## Expected effect
- the tranche graph stops being almost entirely a `PD-957` story
- `PD-1185` gains truthful concept/edge presence using already-admitted source text
- no new law units, OCR work, or all-laws widening is introduced
