---
task: pd957-concept-fit-admission
phase: 11
created: 2026-04-17
author: CODEX
status: DRAFT
---

# 2026-04-17 PD-957 Concept-Fit Admission Research

## Question
What is the smallest truthful admission slice that reduces PD-957 shallow-representation risk without widening tranche execute?

## Fresh evidence
- latest tranche source-to-graph dry-run:
  - `staged_law_folders = [PD-957, PD-1185]`
  - `blocked_law_folders = [PD-1216]`
  - `shallow_representation_count = 1`
- the shallow source is:
  - `001-Laws/refined_markdown/PD-957/PD 957 IRR - Subdivision and Condominium IRR.md`
- current representation guardrail for `PD-957`:
  - `structural_heading_count = 73`
  - `admitted_concept_count = 0`
  - `admitted_relationship_count = 0`
  - severity = `high`

## Source-local evidence
The admitted PD-957 source already explicitly references shared concepts in the canonical source page:
- `concept-floor-area`
- `concept-setbacks`
- `concept-yards`
- plus other shared concepts such as `building-permit`

The refined source contains direct governing language for at least:
- `floor-area`
  - “Minimum floor area for open market housing shall be 42 square meters…”
- `setbacks`
  - “The minimum setback of dwelling units… shall conform to the National Building Code…”
- `yards`
  - “These shall include courts, yards, setbacks…”

## Smallest truthful slice
The smallest safe concept-fit slice is:
1. admit a minimal set of existing shared concepts for `PD-957`
   - `floor-area`
   - `setbacks`
   - `yards`
2. admit matching dataset-scoped source→concept `governs` relationship files for those same concepts
3. rerun tranche source-to-graph dry-run

## Why this is smaller than broader widening
- no new OCR work
- no new law-family expansion
- no generic all-laws widening
- no section-hierarchy implementation yet
- no tranche execute

## Expected effect
Because the guardrail goes `high` at `>= 50 headings && <= 1 admitted concept` and `medium` at `>= 25 headings && <= 2 admitted concepts`, admitting **3** concepts should drop `PD-957` out of shallow-representation status for this checkpoint.
