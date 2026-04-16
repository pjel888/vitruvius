---
task: aec-engine-file-touch-matrix
phase: 00
created: 2026-04-16
author: PLANNER
supersedes: null
status: ACCEPTED
---

# AEC Engine File Touch Matrix

## Companion Artifacts

- `.ai/02_audits/AEC_ENGINE_WHOLE_CODEBASE_READINESS_AUDIT_2026-04-16.md`
- `.ai/04_tasks/aec-engine-master-execution-task-list-2026-04-16.md`
- `.ai/04_tasks/aec-engine-traceability-matrix-2026-04-16.md`
- `.ai/04_tasks/aec-engine-subsystem-gates-2026-04-16.md`
- `.ai/03_plans/templates/aec-engine-first-sprint-template.md`
- `.ai/04_tasks/aec-engine-file-touch-matrix-2026-04-16.md`
- `.ai/04_tasks/aec-engine-gates.schema.json`
- `.ai/04_tasks/aec-engine-gates-spec-2026-04-16.md`
- `.ai/04_tasks/aec-engine-language-boundary-blacklists-2026-04-16.md`


## Purpose
This matrix classifies file paths and modules by touch policy so future AEC planning cannot accidentally use the wrong file as a dumping ground or violate language/boundary ownership.

## Classification Legend
- **FORBIDDEN** — do not touch for AEC implementation work except via explicit governance override
- **PRECEDENT-ONLY** — read and learn from it; do not expand it into the AEC subsystem
- **ALLOWED-AFTER-FREEZE** — can be touched only after relevant freezes are complete
- **DIRECT-TARGET** — intended AEC implementation root once readiness gates are satisfied

## Matrix

| Path | Subsystem relevance | Touch class | Rationale | Owner plane | Prerequisite gate | Required tests |
|---|---|---|---|---|---|---|
| `AGENTS.md` | governance | FORBIDDEN | root contract, not feature surface | governance | override only | n/a |
| `.ai/00_system/EXECUTION_LOOP.md` | governance | FORBIDDEN | process law | governance | override only | n/a |
| `.ai/01_roadmap/*` | state truth | PRECEDENT-ONLY | read for truth; update only with explicit state reconciliation | governance/state | readiness gate | artifact validation |
| `.ai/02_audits/AEC_ENGINE_*` | planning | PRECEDENT-ONLY | source of truth for planning, not runtime | audit | none | n/a |
| `.ai/03_plans/AEC_ENGINE_*` | planning | ALLOWED-AFTER-FREEZE | truthful plan updates may be required | planning | namespace + contract freezes | plan validation |
| `scripts/pipeline_cli.py` | control plane | ALLOWED-AFTER-FREEZE | future AEC commands may land here lazily | Python | namespace freeze | CLI and help tests |
| `scripts/vitruvius/features.py` | rollout | ALLOWED-AFTER-FREEZE | AEC flags may be added only under default-false law | Python | namespace freeze | `test_features.py` |
| `config/vitruvius.yaml` | rollout | ALLOWED-AFTER-FREEZE | AEC flags/config only after contract freeze | config | contract freeze | config + feature tests |
| `scripts/vitruvius/spatial/schema.py` | boundary | ALLOWED-AFTER-FREEZE | boundary v2 may extend or supersede current v1 | Python | DTO/frame/unit freeze | boundary parity tests |
| `scripts/vitruvius/spatial/contract_reader.py` | boundary | ALLOWED-AFTER-FREEZE | strict-vs-legacy import split needed | Python | boundary freeze | reader + strict import tests |
| `scripts/vitruvius/spatial/walker.py` | boundary | PRECEDENT-ONLY | current ingest style useful, but provenance-dropping | Python | boundary freeze | strict import + provenance tests |
| `scripts/vitruvius/spatial/cli.py` | boundary control | ALLOWED-AFTER-FREEZE | current CLI is live and must remain bounded | Python | boundary freeze | `test_spatial_cli.py` |
| `scripts/vitruvius/spatial/spatial_edge_builder.py` | spatial precedent | PRECEDENT-ONLY | legitimate migration precedent, not AEC home | Python | spatial foundation | spatial parity tests |
| `scripts/vitruvius/spatial/proximity_jump.py` | spatial precedent | PRECEDENT-ONLY | legitimate migration precedent, not AEC home | Python | spatial foundation | spatial parity tests |
| `scripts/vitruvius/spatial/constraint_solver.py` | verifier precedent | PRECEDENT-ONLY | scalar solver precedent only | Python | verification foundation | verifier tests |
| `scripts/vitruvius/ontology/ifc_registry.py` | boundary / ontology | PRECEDENT-ONLY | loader pattern only; too shallow and drifting on IDs | Python | boundary freeze | ontology + boundary tests |
| `scripts/vitruvius/ontology/ifc_mapping.yaml` | boundary / ontology | PRECEDENT-ONLY | declarative mapping precedent only | declarative | boundary freeze | ontology parity tests |
| `scripts/vitruvius/graph/contract.py` | graph / contracts | ALLOWED-AFTER-FREEZE | only after explicit reuse-vs-separate-contract decision | Python | contract-family decision | graph contract tests |
| `scripts/vitruvius/graph/snapshot.py` | artifact precedent | PRECEDENT-ONLY | serializer precedent only | Python | envelope freeze | artifact schema tests |
| `scripts/vitruvius/graph/cli.py` | artifact precedent | PRECEDENT-ONLY | dataset artifact precedent good; root `latest_*` aliases unsafe | Python | envelope freeze | artifact + CLI tests |
| `scripts/vitruvius/graph/builder.py` | artifact precedent | PRECEDENT-ONLY | ambient clock / mtime contamination makes it unsafe as-is | Python | envelope freeze | replay/artifact tests |
| `scripts/vitruvius/graph/event_store.py` | replay precedent | PRECEDENT-ONLY | append-only precedent only; envelope too thin for AEC | Python | envelope freeze | event-store tests |
| `scripts/vitruvius/graph/rocksdb_event_store.py` | replay precedent | PRECEDENT-ONLY | backend parity precedent only | Python | backend law | RocksDB parity tests |
| `scripts/vitruvius/review/stateful_registry.py` | mutable cache | PRECEDENT-ONLY | cache precedent only, never canonical truth | Python | candidate/canonical freeze | cache tests |
| `scripts/vitruvius/review/rocksdb_stateful_registry.py` | mutable cache | PRECEDENT-ONLY | same as above | Python | backend law | cache parity tests |
| `scripts/vitruvius/kv_migrate.py` | migration precedent | PRECEDENT-ONLY | migration discipline precedent only | Python | backend law | migration tests |
| `scripts/vitruvius/promotion_validator.py` | truth governance | PRECEDENT-ONLY | admission mindset precedent | Python | truth split freeze | promotion-style tests |
| `scripts/vitruvius/query/result.py` | explanation precedent | PRECEDENT-ONLY | response-shape precedent only | Python | tooling foundation | tooling tests |
| `scripts/vitruvius/query/engine.py` | explanation precedent | PRECEDENT-ONLY | evidence-bearing result precedent only | Python | tooling foundation | tooling tests |
| `scripts/vitruvius/query/nl_translator.py` | tooling risk | FORBIDDEN | heuristic NL routing is not safe AEC authority precedent | Python | explicit override only | n/a |
| `scripts/vitruvius/compound/dependency_tracker.py` | coordination precedent | PRECEDENT-ONLY | algorithmic invalidation precedent only | Python | coordination foundation | coordination tests |
| `scripts/vitruvius/compound/differential_propagator.py` | coordination precedent | PRECEDENT-ONLY | algorithmic invalidation precedent only | Python | coordination foundation | coordination tests |
| `scripts/vitruvius/review/ontology_prompt_builder.py` | LLM prompt risk | FORBIDDEN | prose-rich prompt path not safe for AEC truth or verifier flows | Python | explicit override only | n/a |
| `scripts/vitruvius/engine_rs/__init__.py` | Rust FFI | ALLOWED-AFTER-FREEZE | may expose future isolated AEC kernels | Python↔Rust | benchmark + parity doctrine | kernel parity tests |
| `scripts/vitruvius/engine_rs/core/*` | Rust compute | ALLOWED-AFTER-FREEZE | extension point for narrow kernels only | Rust | benchmark + parity doctrine | kernel parity + bench |
| `scripts/vitruvius/engine_rs/spatial_kernels/*` | Rust compute | ALLOWED-AFTER-FREEZE | extension point for narrow kernels only | Rust | benchmark + parity doctrine | kernel parity + bench |
| `scripts/vitruvius/engine_rs/stats_kernels/*` | Rust compute | ALLOWED-AFTER-FREEZE | extension point for narrow kernels only | Rust | benchmark + parity doctrine | kernel parity + bench |
| `scripts/vitruvius/engine_rs/pyo3_shim/*` | Rust FFI | ALLOWED-AFTER-FREEZE | binding surface for narrow kernels only | Rust↔Python | benchmark + parity doctrine | kernel parity + build tests |
| `spatial-daemon/src/types.ts` | TS boundary | ALLOWED-AFTER-FREEZE | schema/footer parity only | TypeScript | boundary freeze | TS/Python parity tests |
| `spatial-daemon/src/contract_writer.ts` | TS boundary | ALLOWED-AFTER-FREEZE | integrity/footer parity only | TypeScript | boundary freeze | TS/Python parity tests |
| `spatial-daemon/src/cli.ts` | TS boundary | ALLOWED-AFTER-FREEZE | boundary-emitter only; must not absorb policy/orchestration | TypeScript | boundary freeze | boundary CLI + parity tests |
| `spatial-daemon/src/aabb.ts` | TS local compute | PRECEDENT-ONLY | helper only | TypeScript | boundary freeze | local TS tests |
| `spatial-daemon/src/gjk.ts` | TS local compute | PRECEDENT-ONLY | helper only | TypeScript | boundary freeze | local TS tests |
| `scripts/vitruvius/aec/*` | AEC runtime | DIRECT-TARGET | intended AEC home after readiness gate | Python | readiness gate | `test_aec_*` |
| `005_Operational-Intelligence-Layer/aec/*` | AEC artifacts | DIRECT-TARGET | intended AEC artifact root after freezes | artifact layer | envelope + truth freezes | artifact/replay tests |
| `006_System-Manifests/cache/*` | mutable storage | ALLOWED-AFTER-FREEZE | only for explicitly non-canonical AEC cache/store layouts | storage | backend law | backend parity/migration tests |
| `scripts/tests/test_aec_*` | validation | DIRECT-TARGET | intended AEC validation root | test layer | readiness gate | named suite itself |

## Forbidden Surfaces Summary
- root governance law files
- heuristic NL routing paths
- prose-rich prompt-builder paths
- current mutable cache patterns as canonical-truth models

## Final Rule
If a future plan touches a PRECEDENT-ONLY file as if it were the AEC home, that is architecture drift and should be rejected.
