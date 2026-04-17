---
task: ra10066-cultural-heritage-concept-fit
created: 2026-04-17
status: complete
---

# Research — RA-10066 cultural-heritage concept-fit

## Problem
Tranche-4 executes, but `RA-10066` remains the sole shallow-representation law and is also flagged for spot-review-sensitive summaries.

## Fresh evidence
- tranche-4 dry-run reports `shallow_representation_count = 1`
- the shallow source is `001-Laws/refined_markdown/RA-10066/ra 10066.md`
- representation guardrail shows `structural_heading_count = 28`, `admitted_concept_count = 0`, `admitted_relationship_count = 0`
- strongest directly defined law-native concepts in the text:
  - `adaptive reuse`
  - `built heritage`
  - `heritage zone`
  - also available but broader: `cultural heritage`, `important cultural property`, `national cultural treasure`

## Smallest truthful slice
Admit three directly defined concepts and bounded dataset-scoped `governs` relationships for `RA-10066`:
- `adaptive-reuse`
- `built-heritage`
- `heritage-zone`

These are explicitly defined in Section 3 and provide the minimum concept count needed to clear the current guardrail threshold.
