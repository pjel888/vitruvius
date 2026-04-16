---
task: aec-first-slice-blast-radius-map
phase: 00
created: 2026-04-16
author: PLANNER
supersedes: null
status: ACCEPTED
---

# AEC First-Slice Blast Radius Map

## Purpose
This map translates the high-level file-touch policy into an operator-friendly view of likely edit zones, adjacent-risk files, and immediate regression checks.

## 1. Expected edit zone — low surprise
These are the intended first-slice write roots:
- `scripts/vitruvius/aec/contracts/*`
- `scripts/vitruvius/aec/boundary/*`
- `scripts/vitruvius/aec/ecs/*`
- `scripts/vitruvius/aec/spatial/*`
- `scripts/vitruvius/aec/verification/*`
- `scripts/tests/test_aec_*`
- `scripts/tests/fixtures/aec/first_slice/*`

Blast-radius expectation:
- local to the bounded slice unless a test or schema contract reveals otherwise

## 2. Boundary-adjacent risk zone — medium surprise
Touch only if the slice is truly blocked:
- `scripts/vitruvius/spatial/schema.py`
- `scripts/vitruvius/spatial/contract_reader.py`
- `scripts/vitruvius/spatial/cli.py`
- `spatial-daemon/src/types.ts`
- `spatial-daemon/src/contract_writer.ts`

Immediate regression checks if touched:
- `pytest scripts/tests/test_spatial_schema.py`
- `pytest scripts/tests/test_spatial_contract_reader.py`
- `pytest scripts/tests/test_spatial_cli.py`
- `npm test && npm run typecheck` in `spatial-daemon/`

## 3. Precedent-only risk zone — high surprise
Do not touch inline unless the bounded slice is blocked and no smaller fix exists:
- `scripts/vitruvius/spatial/spatial_edge_builder.py`
- `scripts/vitruvius/spatial/proximity_jump.py`
- `scripts/vitruvius/graph/contract.py`
- `scripts/vitruvius/graph/event_store.py`
- `scripts/vitruvius/compound/differential_propagator.py`
- `scripts/vitruvius/geometric/inequality_compiler.py`

Immediate regression checks if touched:
- nearest `test_spatial_*` for spatial precedents
- nearest `test_graph_*` for graph precedents
- nearest `test_geometric_*` for geometric precedents
- nearest `test_query_*` / `test_review_*` if the change leaks into query/review behavior

## 4. Stop-and-review zone — extreme surprise
If a required fix appears to live here, stop and re-evaluate sprint scope:
- pricing
- optimization
- coordination
- tooling
- broad governance docs
- Rust compute members as first-slice owners

## 5. Minimum blast-radius note to record during execution
When any non-direct-target file is touched, record:
- why the bounded slice was blocked without the change
- which zone the file belongs to
- what regressions were run
- whether the change remained inside ownership law and artifact-root law

## Final rule
The later implementation should assume every step is local until evidence proves otherwise, and should escalate blast radius one zone at a time rather than jumping straight to broad refactors.
