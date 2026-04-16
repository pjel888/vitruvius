---
task: non-pd-concept-admission
phase: 05
created: 2026-04-16
author: PLANNER
status: ACCEPTED
---

# 2026-04-16 Non-PD Concept Admission Plan

## Goal
Improve `BP-344` and `BP-220` from source-admitted partials toward relationship-backed coverage by admitting a minimal number of law-specific concepts and rerunning dataset-safe extraction with explicit concept filtering.

## Scope
### In scope
- admit one placeholder concept for `BP-344`
- admit one placeholder concept for `BP-220`
- add additive extraction support for concept whitelisting
- rerun dataset-safe extraction/review for those laws

### Out of scope
- broad concept family expansion
- BP-344 / BP-220 final full coverage guarantees
- any widening into generic Phase 11 expansion

## First concepts
- `accessible ramps` for `BP-344`
- `socialized housing projects` for `BP-220`

## Execution order
1. add concept whitelist support to section extraction
2. create the two placeholder concept files
3. rerun dataset-safe extraction for each law with only its new concept enabled
4. review whether any resulting source→concept candidate is strong enough for conservative admission
5. stop and validate before widening

## Success condition
A source-admitted non-PD law yields at least one truthful, relationship-backed edge without global latest leakage.

## Stop condition
If the first whitelisted concept still does not yield truthful candidates, stop and re-plan before adding more concepts.
