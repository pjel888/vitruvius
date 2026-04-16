---
task: aec-first-slice-blast-radius
phase: 03
created: 2026-04-16
author: PLANNER
supersedes: null
status: ACCEPTED
---

# Research — AEC First-Slice Blast Radius

## Purpose
Make the likely edit surfaces and adjacent-risk surfaces explicit so the bounded first-slice execution can tell when a change is local versus when it risks leaking across the repo.

## Grounded anchors reviewed
- direct-target AEC roots under `scripts/vitruvius/aec/*`
- boundary-adjacent roots in `scripts/vitruvius/spatial/*` and `spatial-daemon/*`
- precedent-only anchors in `graph/*`, `geometric/*`, and `compound/*`
- nearby test families in `scripts/tests/test_spatial_*`, `test_graph_*`, `test_geometric_*`, `test_query_*`, `test_review_*`

## Conclusion
The bounded first slice needs a practical blast-radius map that tells future execution:
- what files are expected to change
- what files are risky-but-adjacent
- what test families should be treated as smoke/regression guards for each risk class
