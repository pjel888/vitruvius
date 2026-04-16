---
task: aec-incidental-remediation-and-blast-radius
phase: 03
created: 2026-04-16
author: PLANNER
supersedes: null
status: ACCEPTED
---

# Research — AEC Incidental Remediation and Blast Radius

## Purpose
Define how the bounded first-slice execution should handle incidental out-of-scope code fixes and blast-radius checks without widening the sprint by accident.

## Grounded repo anchors reviewed
- `scripts/vitruvius/spatial/schema.py`
- `scripts/vitruvius/spatial/contract_reader.py`
- `scripts/vitruvius/spatial/cli.py`
- `scripts/vitruvius/graph/contract.py`
- `scripts/vitruvius/graph/event_store.py`
- `scripts/vitruvius/compound/differential_propagator.py`
- `scripts/vitruvius/geometric/inequality_compiler.py`
- `scripts/vitruvius/spatial/spatial_edge_builder.py`
- `scripts/vitruvius/spatial/proximity_jump.py`
- `spatial-daemon/src/types.ts`
- `spatial-daemon/src/contract_writer.ts`

## Existing test surfaces available as fallback blast-radius evidence
- spatial tests: `test_spatial_*`
- graph tests: `test_graph_*`
- geometric tests: `test_geometric_*`
- query/review tests where shared behavior leaks outward
- `spatial-daemon/tests/contract_writer.test.ts`, `cli.test.ts`, `smoke.test.ts`

## Conclusion
The bounded first slice needs a dedicated incidental-remediation protocol:
- log every out-of-scope issue encountered during execution
- classify whether it is direct-target, boundary-adjacent, precedent-only, or unrelated
- run a blast-radius check before touching any non-AEC file
- keep direct-target fixes in-scope only when they unblock the slice
- split precedent-only or unrelated fixes into explicit follow-on artifacts unless the sprint cannot continue safely without them
