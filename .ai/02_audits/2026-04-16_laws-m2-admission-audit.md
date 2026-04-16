# Audit — Laws M2 Admission Path for RA-9514 / BP-344 / BP-220

## Purpose
Audit what is actually missing before `RA-9514`, `BP-344`, and `BP-220` can be admitted truthfully into the laws mini dataset→graph pipeline.

## Core finding
These three laws are blocked in M1 **not** because the scoped graph lane failed, but because the repo has not yet admitted any truth-bearing pipeline outputs for them.

The missing boundary is wider than the original shorthand "M2 review/promotion inputs":
- no conversion outputs
- no refined outputs
- no canonical source pages
- no admitted concepts
- no approved relationships

So the proper M2 path must begin with **per-law admission into the truth-bearing pipeline**, then continue into dataset-safe extraction/review/promotion.

## Severity-ranked findings
1. **Critical — zero truth-bearing admission artifacts for all three laws**
   - each law has raw PDFs only
   - each law has `canonical_count=0` and `approved_relationship_input_count=0` in the dataset build report

2. **High — current extraction/review/promotion path is global-latest dependent**
   - new law relationship generation cannot be routed safely through current `latest_relationship_*` flows in dataset mode

3. **High — BP-344 has variant-selection ambiguity**
   - at least two in-folder RIRR candidates plus one adjacent out-of-folder DPWH memo
   - variant/adjacency policy must be explicit before canonical admission

4. **Medium — the current M2 label understates the prerequisite work**
   - review/promotion scoping alone will not solve admission because there is nothing yet to review/promote for these laws

## Law-by-law gap table
| Law | Raw evidence | Converted | Refined | Canonical source | Concepts | Approved relationships | Immediate blocker |
|---|---|---:|---:|---:|---:|---:|---|
| RA-9514 | 1 raw PDF | 0 | 0 | 0 | 0 | 0 | no admitted source page |
| BP-344 | 2 in-folder variants + 1 adjacent memo | 0 | 0 | 0 | 0 | 0 | authoritative variant not frozen |
| BP-220 | 1 raw PDF | 0 | 0 | 0 | 0 | 0 | no admitted source page |

## Blast-radius implication
The next truthful phase will likely touch:
- conversion/refinement/canonicalization flow for the selected law files
- source admission policy and canonical page creation
- extraction/review/promotion lane for dataset-safe relationship generation
- the scoped graph rerun + validation surface

## Recommended M2 execution order
1. freeze authoritative admission candidates per law
2. produce bounded conversion/refinement outputs for those candidates
3. create/admit canonical source pages
4. decide whether canonical concept admission is needed before extraction
5. create dataset-safe extraction/review/promotion outputs
6. rerun scoped graph and re-evaluate bundle coverage

## Stop conditions
Stop if any of the following occurs:
- BP-344 authoritative variant cannot be chosen without a new design decision
- admission would require silently reusing global `latest_relationship_*` in dataset mode
- new laws would force broad whole-corpus orchestration rather than bounded per-law admission
- the current laws plan cannot be extended truthfully without a new dedicated M2 implementation plan

## Audit verdict
A proper M2 path is feasible, but it is **admission-first**, not review-first.
