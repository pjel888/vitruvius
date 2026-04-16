---
task: aec-engine-g2-g8-freeze-pack
phase: 00
created: 2026-04-16
author: PLANNER
supersedes: null
status: ACCEPTED
---

# AEC Engine G2-G8 Freeze Pack

## Purpose
This artifact freezes the planning-layer decisions needed to close global blockers `G2` through `G8`. It does not close `G1`, does not establish a clean baseline branch, and does not authorize coding.

## Gate closure map
| Gate | Task IDs | Decision summary |
|---|---|---|
| G2 | AEC-T002 | replay-safe envelope frozen |
| G3 | AEC-T003, AEC-T008 | DTO / ID / version family frozen; AEC contracts remain separate from current graph contracts |
| G4 | AEC-T004 | frame / unit / tolerance policy frozen |
| G5 | AEC-T005, AEC-T010A | candidate/canonical split and backend law frozen |
| G6 | AEC-T001 | namespace + ownership map frozen |
| G7 | AEC-T009 | benchmark doctrine frozen |
| G8 | AEC-T010, AEC-T010A | parity matrix frozen |

## 1. Namespace and ownership freeze (`AEC-T001`, `G6`)
- Python AEC runtime root: `scripts/vitruvius/aec/`
- Python authority: orchestration, validation, truth governance, replay coordination, tool routing
- Rust extension points only: `scripts/vitruvius/engine_rs/core`, `scripts/vitruvius/engine_rs/spatial_kernels`, `scripts/vitruvius/engine_rs/pyo3_shim`
- TypeScript boundary-only surface: `spatial-daemon/`
- Forbidden as default AEC homes: `scripts/vitruvius/spatial/*`, `graph/*`, `compound/*`, `query/*`, `geometric/*`

## 2. Replay-safe audit/snapshot envelope freeze (`AEC-T002`, `G2`)
Every future AEC artifact envelope must carry:
- `snapshot_id`
- `run_id`
- `actor`
- `subsystem`
- `status`
- `input_artifact_refs[]`
- `output_artifact_refs[]`
- `declared_clock_source`
- `schema_version`

Rules:
- identity must not derive from filesystem mtime or `latest_*` aliases
- `declared_clock_source` must be explicit and auditable
- repeated replay of the same bounded fixture family must reproduce the same envelope identity inputs

## 3. DTO / ID / version family freeze (`AEC-T003`, `G3`)
Canonical AEC artifact families are:
- `aec-boundary-payload`
- `aec-world`
- `aec-world-snapshot`
- `aec-spatial-fact-bundle`
- `aec-rule-ast`
- `aec-rule-snapshot`
- `aec-verification-run`
- `aec-coordination-run`
- `aec-pricebook-snapshot`
- `aec-optimization-run`
- `aec-tool-request`

Rules:
- every family carries explicit `schema_version`
- AEC artifact contracts remain separate from the current graph contract vocabulary unless an explicit future superseding decision says otherwise
- IDs must be stable, reviewable, and family-specific; no subsystem may invent ad hoc IDs after this freeze

## 4. Frame / unit / tolerance freeze (`AEC-T004`, `G4`)
- `frame_id` is mandatory on every boundary payload and derived spatial artifact
- every boundary payload must declare `unit_system`
- canonical internal length unit for the first bounded slice: **millimeters**
- canonical area unit: **square meters**
- canonical volume unit: **cubic meters**
- tolerance classes for the first bounded slice:
  - schema / identity fields: exact
  - boundary import normalization: 0.1 mm
  - spatial coincidence / clearance comparison: 1.0 mm
  - quantity rounding for downstream pricing inputs: 0.001 in declared output units

Rules:
- TypeScript may emit declared units but may not define authoritative unit or tolerance policy
- Rust may consume frozen numeric policy but may not redefine it

## 5. Candidate / canonical truth split and backend law (`AEC-T005`, `AEC-T010A`, `G5`)
- candidate machine-truth root: `005_Operational-Intelligence-Layer/aec/candidates/`
- canonical/admitted machine-truth root: `005_Operational-Intelligence-Layer/aec/admitted/`
- promotion / admission audit root: `006_System-Manifests/aec/promotions/`
- mutable cache or dual-backend stores are allowed only under `006_System-Manifests/cache/`

Rules:
- canonical/admitted truth must be immutable snapshot-style data; no overwrite/purge semantics
- mutable SQLite/RocksDB duality is allowed only for non-canonical caches/stores
- raw prose and free-form LLM text must not become canonical machine truth
- backend duality must remain behind explicit factory law and parity tests

## 6. Benchmark doctrine freeze (`AEC-T009`, `G7`)
Every future Rust candidate or accelerated seam must cite a benchmark doctrine that includes:
- fixture-defined workloads
- wall time
- peak RSS
- hardware context
- Python reference baseline vs accelerated path
- explicit acceptance threshold

Rule:
- no Rust AEC task may be accepted without benchmark doctrine reference and parity doctrine reference
- performance claims under the AEC family must clear a measured improvement gate before rollout defaults are reconsidered

## 7. Parity matrix freeze (`AEC-T010`, `AEC-T010A`, `G8`)
Required parity families:
- `scripts/tests/test_aec_boundary_contract_parity.py`
- `scripts/tests/test_aec_vault_backend_parity.py`
- `scripts/tests/test_aec_ecs_replay.py`
- `scripts/tests/test_aec_spatial_parity.py`
- `scripts/tests/test_aec_z3_replay.py`
- `scripts/tests/test_aec_coordination_replay.py`
- `scripts/tests/test_aec_pricing_refusals.py`
- `scripts/tests/test_aec_optimization_replay.py`
- `scripts/tests/test_aec_tools_refusals.py`

Rules:
- every cross-language or backend seam must name a parity lane before implementation starts
- canonical truth must never inherit mutable backend behavior by analogy

## Final rule
This freeze pack closes `G2`-`G8` at the planning/spec layer only. `G1` / `AEC-T006` remain open until the repo baseline is clean.
