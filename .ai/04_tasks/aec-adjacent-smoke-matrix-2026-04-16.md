---
task: aec-adjacent-smoke-matrix
phase: 00
created: 2026-04-16
author: PLANNER
supersedes: null
status: ACCEPTED
---

# AEC Adjacent Smoke Matrix

## Purpose
This matrix maps adjacent-risk files to their minimum smoke/regression checks when touched as bounded unblockers.

| Adjacent file family | Why it might be touched | Minimum smoke / regression checks |
|---|---|---|
| `scripts/vitruvius/spatial/schema.py` | boundary DTO/schema alignment | `pytest scripts/tests/test_spatial_schema.py` |
| `scripts/vitruvius/spatial/contract_reader.py` | strict boundary import / footer behavior | `pytest scripts/tests/test_spatial_contract_reader.py` |
| `scripts/vitruvius/spatial/cli.py` | bounded boundary CLI path only | `pytest scripts/tests/test_spatial_cli.py` |
| `spatial-daemon/src/types.ts` | boundary schema parity only | `npm test && npm run typecheck` in `spatial-daemon/` |
| `spatial-daemon/src/contract_writer.ts` | boundary footer/integrity parity only | `npm test && npm run typecheck` in `spatial-daemon/` |
| `scripts/vitruvius/spatial/spatial_edge_builder.py` | precedent-only spatial logic unblocker | `pytest scripts/tests/test_spatial_edge_builder.py scripts/tests/test_spatial_edge_builder_parity.py` |
| `scripts/vitruvius/spatial/proximity_jump.py` | precedent-only routing/distance unblocker | nearest bounded spatial test + targeted `test_spatial_edge_builder_parity.py` if parity is implicated |
| `scripts/vitruvius/graph/contract.py` | contract-family clarification only | `pytest scripts/tests/test_graph_contract.py` |
| `scripts/vitruvius/graph/event_store.py` | replay precedent unblocker only | `pytest scripts/tests/test_graph_event_store.py scripts/tests/test_graph_event_store_delta.py` |
| `scripts/vitruvius/compound/differential_propagator.py` | coordination precedent unblocker only | nearest bounded coordination-adjacent regression + local file review note |
| `scripts/vitruvius/geometric/inequality_compiler.py` | verifier precedent unblocker only | `pytest scripts/tests/test_geometric_inequality_compiler.py` |

## Rule
If a touched adjacent file has no named smoke lane here, execution should pause and add one before continuing.

## Final rule
Use the smallest honest regression that still answers whether the bounded unblocker broke the adjacent surface.
