---
task: laws-m2-admission-path
phase: 05
created: 2026-04-16
author: PLANNER
supersedes: null
status: ACCEPTED
---

# 2026-04-16 Laws M2 Admission Path Plan

## 1. Executive Summary
After the M1 scoped graph proof completed as `PARTIAL`, the next truthful step is to admit `RA-9514`, `BP-344`, and `BP-220` into the truth-bearing pipeline before asking the graph layer to cover them.

This plan therefore reframes M2 as:
1. **M2A — Per-law truth admission** (raw → conversion → refinement → canonical source admission)
2. **M2B — Dataset-safe relationship generation/review/promotion inputs**
3. **M2C — Scoped graph rerun and coverage reclassification**

## 2. Decision
Do **not** widen directly into full M3 orchestration or "implement everything" blindly.
Proceed by bounded admission slices for the three blocked laws, with explicit authoritative-variant policy and dataset-safe review/promotion routing.

## 3. Why this is required
Fresh audit findings show:
- all three laws currently have raw PDFs only
- none have converted/refined/canonical/promoted truth-bearing artifacts
- current extraction/review/promotion tooling still depends on global `latest_*` artifacts

Therefore graph-layer scoping alone cannot admit them truthfully.

## 4. Scope
### In scope
- authoritative-variant selection for RA-9514 / BP-344 / BP-220
- bounded admission of the selected files into conversion/refinement/canonical source layers
- design and implementation of dataset-safe extraction/review/promotion inputs as needed
- rerun of the scoped graph proof after new truth-bearing inputs exist

### Not in scope
- generic all-laws expansion
- per-section or merged-graph orchestration
- Rust
- silent reuse of global `latest_relationship_*` in dataset mode

## 5. Per-law admission defaults
### RA-9514
- admission candidate: `RA9514-RIRR-rev-2019.pdf`
- default stance: single authoritative admission candidate unless a competing source appears
- source-page default: `irr-implementing-rules-and-regulations-of-the-fire-code-of-the-philippines`

### BP-344
- admission candidate: `2024 Revised Implementing Rules and Regulations ... NCDA ... .pdf`
- reference-only variant: `BP-344 IRR Accessibility Law DPWH.pdf`
- adjacent context excluded from canonical admission by default: `DPWH DO037 Enforcement of BP344 along National Roads.pdf`

### BP-220
- admission candidate: `Revised_IRR_BP220_2008.pdf`
- default stance: single authoritative admission candidate unless a competing source appears
- source-page default: `irr-revised-implementing-rules-and-regulations-of-batas-pambansa-blg-220`

## 6. Milestones
### M2A — Per-law truth admission
Deliverables:
- selected raw files confirmed by manifest/policy
- conversion + refinement outputs for those selected files
- canonical source pages admitted for each selected law
- explicit variant-role notes where multiple raw variants exist

### M2B — Dataset-safe extraction / review / promotion inputs
Deliverables:
- extraction inputs no longer depend on global `latest_relationship_*` in dataset mode
- dataset-scoped review outputs if relationship generation is needed
- dataset-scoped promotion inputs / audit refs if promotion is needed

### M2C — Scoped graph rerun
Deliverables:
- updated dataset manifest reflecting newly admitted truth-bearing inputs
- rerun dataset snapshot / integrity / coverage / seeded queries
- explicit decision whether bundle coverage now reaches `SUCCESS` or remains `PARTIAL`

## 7. Execution-readiness gate
Do not implement M2 until all of the following are explicit:
- authoritative variant choices are frozen for the three laws
- admission path for conversion/refinement/canonicalization is bounded
- dataset-safe review/promotion routing is specified where needed
- no global-latest dependency remains hidden in dataset mode
- rollback/removability remain intact

## 8. Immediate next slice
The smallest truthful next implementation slice is:
1. admit **one law at a time**
2. start with the clearest candidate (`RA-9514` or `BP-220`), or start with `BP-344` only if the authoritative-variant choice is explicitly frozen first
3. keep the slice bounded to truth admission before broader orchestration

## 9. Recommended first execution target
Recommended first M2A implementation target:
- `RA-9514`

Why:
- only one known raw admission candidate
- no same-folder variant ambiguity
- simplest path to proving the admission lane before tackling BP-344 policy complexity

## 10. Verification requirements
- prove newly admitted law artifacts are bounded to the selected files
- prove dataset mode still avoids global `latest_relationship_*`
- prove default/global path still behaves unchanged when dataset mode unused
- prove updated coverage report reflects the newly admitted law honestly

## 11. Stop conditions
Stop and re-plan if:
- BP-344 authority policy becomes contested
- per-law admission unexpectedly requires broad all-laws orchestration
- dataset-safe review/promotion routing cannot be added without destabilizing the current default/global path

## 12. Plan Critique
### What this plan gets right
- it distinguishes **truth admission** from later **graph/query use**
- it keeps the first post-M1 slice bounded to one law at a time
- it preserves the explicit variant/adjacency policy burden instead of hiding it in heuristics

### Remaining tension
- the repo already has operational single-file commands, which may tempt direct source admission before the dataset-safe review/promotion lane is fully specified
- the current shared canonical layer is still globally shared, so any newly admitted source page must be reviewed carefully before claiming that the overall dataset path is already safe end-to-end

### Planning rule
Use the smallest honest M2A slice first, then stop to validate before widening to M2B.

## 13. Execution Checklist
- [x] verify current authority docs still align with this M2 plan
- [x] choose the first law-admission target explicitly (`RA-9514`)
- [x] run bounded single-file admission steps only for that target
- [x] inspect the resulting canonical plan/output before accepting it as truth-bearing
- [x] stop after first-law admission and validate whether M2B is now required
- [x] do not widen to other blocked laws until the first-law admission slice is truthful

Execution status note (2026-04-16):
- M2A source admission slices executed for `RA-9514`, `BP-344`, and `BP-220`
- Validation artifact: `/.ai/05_logs/2026-04-16_laws-m2a-source-admission-validation.md`
- all three previously blocked laws now contribute admitted source nodes in the scoped graph
- additive M2B dataset-safe stage wiring is now implemented
- Validation artifact: `/.ai/05_logs/2026-04-16_laws-m2b-dataset-safe-stage-validation.md`
- conservative relationship admission is now partially complete
- Validation artifact: `/.ai/05_logs/2026-04-16_laws-m2b-relationship-admission-validation.md`
- `RA-9514` now has 2 manually audited dataset-scoped relationship inputs admitted into the official manifest
- `BP-344` and `BP-220` remain source-admitted but relationship-thin
- fresh validation (`/.ai/05_logs/2026-04-16_non-pd-concept-gap-validation.md`) indicates the next bottleneck is concept coverage / concept fit for non-PD laws rather than stage wiring

## 14. Next action after this plan
Create the implementation-ready M2A slice for the first admitted law, then run the full SEL before code changes or truth-bearing content writes.
