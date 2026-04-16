---
task: aec-first-slice-ownership-and-review-checklist
phase: 00
created: 2026-04-16
author: PLANNER
supersedes: null
status: ACCEPTED
---

# AEC First-Slice Ownership and Review Checklist

## Purpose
This is the final no-code handoff for ownership boundaries and review questions during the future bounded-slice coding phase.

## 1. Lane ownership map

### Boundary/contracts lane
Owns only:
- `scripts/vitruvius/aec/contracts/*`
- `scripts/vitruvius/aec/boundary/*`
- `scripts/tests/test_aec_boundary_*`
- `scripts/tests/fixtures/aec/first_slice/boundary/*`
- parity-only boundary schema touchpoints in `spatial-daemon/*` if strictly required

Must not own:
- ECS runtime files
- spatial runtime files
- verification runtime files
- downstream subsystem files

### ECS lane
Owns only:
- `scripts/vitruvius/aec/ecs/*`
- `scripts/tests/test_aec_ecs_*`
- `scripts/tests/fixtures/aec/first_slice/ecs/*`

### Spatial lane
Owns only:
- `scripts/vitruvius/aec/spatial/*`
- `scripts/tests/test_aec_spatial_*`
- `scripts/tests/fixtures/aec/first_slice/spatial/*`

### Verification lane
Owns only:
- `scripts/vitruvius/aec/verification/*`
- `scripts/tests/test_aec_z3_*`
- `scripts/tests/fixtures/aec/first_slice/verification/*`

### Validation/review lane
Owns only:
- validation log under `.ai/05_logs/`
- artifact inspection notes
- final review pass and scope check

## 2. Change-budget ceilings
- boundary/contracts lane: no downstream subsystem edits
- ECS lane: no boundary schema policy changes
- spatial lane: no Rust hot-loop additions in the first slice
- verification lane: no new supported rule families beyond the bounded whitelist
- any lane: no pricing, optimization, coordination, or tooling changes

## 3. Final review checklist
Before calling the bounded slice complete, reviewers should ask:
1. Did any lane write outside its declared file family?
2. Did any runtime file appear outside `scripts/vitruvius/aec/*` or the declared first-slice test/fixture roots?
3. Did TypeScript stay boundary-only?
4. Did Rust stay out of first-slice ownership?
5. Did outputs respect the candidate/admitted/promotion split?
6. Did any downstream subsystem get pulled in by convenience?
7. Did the validation log prove all bounded lanes and artifact inspections?

## 4. Incidental remediation review
If out-of-scope code is touched as a bounded unblocker, require the blast-radius matrix and targeted regressions before accepting the change.

## 5. Refusal rule
If any answer above is unsafe or unclear, the slice should be refused as out-of-scope rather than “almost done.”

## Final rule
This checklist exists to keep the first bounded slice small, reviewable, and reversible. G10 remains open until the actual runtime/test evidence exists.
