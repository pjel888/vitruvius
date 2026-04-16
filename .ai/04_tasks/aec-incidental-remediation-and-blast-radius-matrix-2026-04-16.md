---
task: aec-incidental-remediation-and-blast-radius-matrix
phase: 00
created: 2026-04-16
author: PLANNER
supersedes: null
status: ACCEPTED
---

# AEC Incidental Remediation and Blast Radius Matrix

## Purpose
This is the contingency protocol for incidental remediations encountered while implementing the bounded first slice.

## 1. Scope classes

### Class A — Direct target
Files intended for the bounded first slice itself:
- `scripts/vitruvius/aec/contracts/*`
- `scripts/vitruvius/aec/boundary/*`
- `scripts/vitruvius/aec/ecs/*`
- `scripts/vitruvius/aec/spatial/*`
- `scripts/vitruvius/aec/verification/*`
- `scripts/tests/test_aec_*`
- `scripts/tests/fixtures/aec/first_slice/*`

Policy:
- fix in the same sprint if needed
- re-run the bounded-lane tests affected by the change

### Class B — Boundary-adjacent
Files allowed-after-freeze and close to the bounded slice contract:
- `scripts/vitruvius/spatial/schema.py`
- `scripts/vitruvius/spatial/contract_reader.py`
- `scripts/vitruvius/spatial/cli.py`
- `spatial-daemon/src/types.ts`
- `spatial-daemon/src/contract_writer.ts`

Policy:
- fix only if the bounded slice cannot continue without it
- require a blast-radius note + targeted regressions
- preferred regressions:
  - `pytest scripts/tests/test_spatial_schema.py`
  - `pytest scripts/tests/test_spatial_contract_reader.py`
  - `pytest scripts/tests/test_spatial_cli.py`
  - `npm test && npm run typecheck` in `spatial-daemon/` if TS files change

### Class C — Precedent-only
Files that are reference patterns, not intended AEC homes:
- `scripts/vitruvius/spatial/spatial_edge_builder.py`
- `scripts/vitruvius/spatial/proximity_jump.py`
- `scripts/vitruvius/graph/contract.py`
- `scripts/vitruvius/graph/event_store.py`
- `scripts/vitruvius/compound/differential_propagator.py`
- `scripts/vitruvius/geometric/inequality_compiler.py`

Policy:
- default to separate follow-on artifact/trigger
- only patch in the sprint if the slice is truly blocked and the change is narrower than management wants
- if patched, add explicit blast-radius note and run the nearest precedent tests before continuing

### Class D — Unrelated
Anything outside the bounded slice and outside boundary-adjacent support surfaces.

Policy:
- do not fix inline
- log and queue as a separate follow-on artifact

## 2. Incidental remediation log entry
For each incidental issue encountered, record:
- issue id
- file/path
- class (A/B/C/D)
- why it surfaced during first-slice execution
- whether the slice is blocked without the fix
- expected blast radius
- targeted regressions to run
- disposition: inline fix / defer to follow-on

## 3. Blast-radius checklist
Before touching any Class B or Class C file:
1. state why the bounded slice is blocked without the change
2. note preferred structural-impact check (GitNexus / code-review-graph when available)
3. if unavailable, record the fallback evidence used (nearest tests + local file relationship reasoning)
4. list the exact regression commands to run after the change
5. confirm whether the change still respects the file-touch matrix and language-boundary blacklists

## 4. Default regression mapping
- boundary-adjacent Python: relevant `test_spatial_*`
- boundary-adjacent TypeScript: `spatial-daemon` tests + typecheck
- graph precedent files: relevant `test_graph_*`
- geometric precedent files: relevant `test_geometric_*`
- query/review spillovers: relevant `test_query_*` / `test_review_*`

## 5. Refusal rule
Refuse inline remediation when:
- the file is Class D
- the change would widen the slice into pricing, optimization, coordination, or tooling
- the blast radius cannot be reasonably bounded
- the change would shift policy ownership into TypeScript or truth ownership into Rust

## Final rule
Incidental remediation is allowed only as a bounded unblocker, not as permission to “clean up the neighborhood.”


## First-slice blast-radius companion
- `.ai/04_tasks/aec-first-slice-blast-radius-map-2026-04-16.md`


## Companion smoke matrix
- `.ai/04_tasks/aec-adjacent-smoke-matrix-2026-04-16.md`


## Deferred-remediation backlog template
- `.ai/05_logs/aec-incidental-remediation-backlog-template-2026-04-16.md`
