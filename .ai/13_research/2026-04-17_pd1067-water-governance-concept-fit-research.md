---
task: pd1067-water-governance-concept-fit
created: 2026-04-17
status: complete
---

# Research — PD-1067 water-governance concept-fit

## Problem
Tranche-3 executes, but `PD-1067` still triggers the shallow-representation guardrail because the admitted law family has rich section structure and zero admitted law-native concepts.

## Fresh evidence
- `laws-tranche-3` dry-run reports `shallow_representation_count = 1`
- the shallow source is `001-Laws/refined_markdown/PD-1067/Water Code of PH IRR 2005.md`
- guardrail details show `structural_heading_count = 38`, `admitted_concept_count = 0`, `admitted_relationship_count = 0`
- strongest bounded concept evidence in PD-1067 law/IRR:
  - `water-permit`
  - `water-right`
  - `groundwater-drilling`

## Smallest truthful slice
Admit three new shared concepts and a bounded set of dataset-scoped `governs` relationships for the PD-1067 law family. This is the smallest slice that should clear the current guardrail threshold without widening tranche scope.
