---
title: AEC Engine Whole-Codebase Readiness Audit
type: audit
status: REVIEW
date: 2026-04-16
author: Codex
task: aec-engine-whole-codebase-readiness
governing_inputs:
  - AGENTS.md
  - .ai/00_system/EXECUTION_LOOP.md
  - .ai/00_system/principles.md
  - .ai/01_roadmap/master-roadmap.md
  - .ai/01_roadmap/current-phase.md
  - .ai/01_roadmap/milestone-tracker.md
  - .ai/03_plans/00-governing-implementation-plan.md
  - .ai/03_plans/INDEX.md
  - .ai/03_plans/AEC_ENGINE_MASTER_IMPLEMENTATION_PLAN.md
  - .ai/03_plans/AEC_ENGINE_BOUNDARY_TRANSLATION_IMPLEMENTATION_PLAN.md
  - .ai/03_plans/AEC_ENGINE_ECS_CORE_IMPLEMENTATION_PLAN.md
  - .ai/03_plans/AEC_ENGINE_SPATIAL_KERNEL_IMPLEMENTATION_PLAN.md
  - .ai/03_plans/AEC_ENGINE_KNOWLEDGE_VAULT_IMPLEMENTATION_PLAN.md
  - .ai/03_plans/AEC_ENGINE_Z3_VERIFICATION_IMPLEMENTATION_PLAN.md
  - .ai/03_plans/AEC_ENGINE_MULTI_DISCIPLINARY_COORDINATION_IMPLEMENTATION_PLAN.md
  - .ai/03_plans/AEC_ENGINE_FINANCIAL_PRICING_ORACLE_IMPLEMENTATION_PLAN.md
  - .ai/03_plans/AEC_ENGINE_OPTIMIZATION_ENGINE_IMPLEMENTATION_PLAN.md
  - .ai/03_plans/AEC_ENGINE_LLM_TOOL_CALLING_IMPLEMENTATION_PLAN.md
  - .ai/06_specs/AEC_ENGINE/02_ECS_AND_COMPONENT_DESIGN_RULES.md
  - .ai/06_specs/AEC_ENGINE/03_SPATIAL_COMPREHENSION_PROTOCOL.md
  - .ai/06_specs/AEC_ENGINE/04_KNOWLEDGE_VAULT_AND_RULE_AST_CONTRACT.md
  - .ai/06_specs/AEC_ENGINE/05_MULTI_DISCIPLINARY_COORDINATION_RULES.md
  - .ai/06_specs/AEC_ENGINE/06_FORMAL_VERIFICATION_AND_Z3_PROTOCOL.md
  - .ai/06_specs/AEC_ENGINE/07_BOUNDARY_TRANSLATION_PROTOCOL.md
  - .ai/06_specs/AEC_ENGINE/08_DETERMINISM_TEMPORALITY_AND_AUDIT_RULES.md
  - .ai/06_specs/AEC_ENGINE/09_PARETO_OPTIMIZATION_AND_FINANCIAL_LAYER_RULES.md
  - .ai/06_specs/GOVERNANCE/01_VALIDATION_PROTOCOL.md
  - .ai/06_specs/GOVERNANCE/04_CROSS_LANGUAGE_BOUNDARY_CONTRACT.md
  - .ai/06_specs/GOVERNANCE/05_TRUTH_GOVERNANCE_AND_PROMOTION_CONTRACT.md
  - .ai/06_specs/GOVERNANCE/06_PERFORMANCE_BUDGET_AND_BENCHMARK_POLICY.md
  - .ai/06_specs/RUST/04_RUST_ARCHITECTURE_AND_BOUNDARY_RULES.md
  - .ai/06_specs/RUST/05_RUST_TESTING_BENCHMARKING_AND_VALIDATION.md
  - .ai/13_research/AEC-ECS-SC_RESEARCH.md
audited_repo_surfaces:
  - scripts/pipeline_cli.py
  - scripts/vitruvius/features.py
  - scripts/vitruvius/config.py
  - scripts/vitruvius/spatial/
  - scripts/vitruvius/graph/
  - scripts/vitruvius/review/
  - scripts/vitruvius/compound/
  - scripts/vitruvius/geometric/
  - scripts/vitruvius/ontology/
  - scripts/vitruvius/normalization/outlier_detector.py
  - scripts/vitruvius/engine_rs/
  - spatial-daemon/
  - scripts/tests/
  - 001B_Spatial-Source-Layer/
  - 005_Operational-Intelligence-Layer/
  - 006_System-Manifests/
---

# AEC Engine Whole-Codebase Readiness Audit

## 1. Title and Metadata

- **Title:** AEC Engine Whole-Codebase Readiness Audit
- **Type:** whole-codebase audit + implementation-preparation artifact
- **Date:** 2026-04-16
- **Status:** review-ready, implementation-blocking audit
- **Dispatcher truth:** AEC is still planning-only. `current-phase.md` and `00-governing-implementation-plan.md` both block implementation until namespace, validation, and determinism gates are frozen.
- **Observed runtime truth:** there is **no** `scripts/vitruvius/aec/` code root, no AEC CLI, no AEC test family, and no accepted execution trigger.
- **This revision is intentionally harsher than the previous one.** It removes optimism that was not fully backed by code and distinguishes “good substrate exists” from “safe to start implementation.”

## 2. Executive Summary

### Brutal Summary

This repo is **good at building deterministic substrate** and **not yet safe for AEC implementation**.

What is genuinely strong:
- append-only replay patterns exist (`scripts/vitruvius/graph/event_store.py`, `graph/rocksdb_event_store.py`)
- backend-parity and migration discipline exist (`review/stateful_registry.py`, `review/rocksdb_stateful_registry.py`, `kv_migrate.py`)
- Python↔TypeScript contract integrity exists for the **current** spatial boundary (`spatial/schema.py`, `spatial/contract_reader.py`, `spatial-daemon/src/types.ts`, `contract_writer.ts`)
- Python-first → feature-gated Rust fast-path discipline is already real (`spatial_edge_builder.py`, `proximity_jump.py`, `normalization/outlier_detector.py`, `engine_rs/*`, parity tests)
- dataset-scoped immutable graph builds already exist and are richer replay precedents than the root `latest_*` aliases (`scripts/vitruvius/graph/dataset_manifest.py`, `graph/cli.py`, `005_Operational-Intelligence-Layer/graph/datasets/*`)
- test density is respectable around the relevant anchors, and targeted validation passed in this audit run.

What is not strong enough and would break an AEC rollout if ignored:
- **the AEC runtime does not exist**
- **the AEC contract layer does not exist**
- **the AEC truth boundary does not exist**
- **the AEC replay layer does not exist**
- **the current spatial boundary is too narrow and too legacy-tolerant for AEC use**
- **several anchor subsystems are disabled by default behind feature flags**, so they are not the default runtime path
- **current graph `latest_*` artifacts are operator conveniences, not replay-safe AEC precedents**
- **current mutable SQLite/RocksDB registry backends are valid performance-cache patterns, not canonical-truth storage precedents**
- **some code comments and fixtures are stale or legacy-oriented**, so they cannot be treated as authority without checking current runtime behavior.

### Final Recommendation

- **GO** only for preparatory work: namespace freeze, contract freeze, artifact-location freeze, feature-flag planning, fixture design, benchmark planning, and repo-hygiene cleanup.
- **NO-GO** for any AEC subsystem implementation that assumes DTOs, frames, units, tolerances, rule ASTs, replay envelopes, or pricebook schemas already exist.
- **HARD NO-GO** for:
  - Rust-first ECS
  - TypeScript-first orchestration
  - Z3 over raw prose
  - optimization before verification replay is stable
  - pricing before quantity/provenance/currency contracts exist
  - any implementation launched from the current dirty working tree.

### Practical Readiness Verdict

- **Planning-readiness:** yes
- **Implementation-readiness:** no
- **Honest state:** **planning-ready, implementation-blocked**

## 3. Self-Critique of the Prior Audit Revision

The earlier revision of this audit was useful but too trusting in six ways:

1. **It over-scored readiness.** It treated “good substrate exists” as closer to “AEC implementation can start” than the code supports.
2. **It underplayed feature-gate reality.** Important anchors (`l_spatial_ingestion`, `l_z3_constraint_solver`, `gt_proximity_jump`, `gt_spatial_edges`, `gt_engine_rs`) are default-off, so they are not the default runtime lane.
3. **It missed file-level touchpoints.** The earlier version underused `graph/snapshot.py`, `graph/dataset_manifest.py`, `query/result.py`, `engine_rs/__init__.py`, `normalization/outlier_detector.py`, `test_spatial_bootstrap.py`, and live CLI surfaces as precedents and risks.
4. **It did not call out plan/code contradictions hard enough.** The AEC specs discuss `bevy_ecs`, voxel carving, terrain heightmaps, a RocksDB rule vault, and strict frame/tolerance contracts; the repo does not currently implement those things.
5. **It blurred legacy compatibility with safe AEC baseline.** Example: `spatial/contract_reader.py` defaults to `require_footer=False`, and the sample spatial fixture lacks a footer. That is appropriate for older files, but not safe as the AEC import contract.
6. **It was too soft on mutable stores and `latest_*` aliases.** Current caches and root aliases are useful operator/performance conveniences, but they are not valid precedents for AEC truth or replay identity.

This revision corrects those defects.

## 4. Current State of the Repo

### 4.1 What exists now

#### Python orchestration and rollout discipline
- `scripts/pipeline_cli.py` is a mature lazy-import CLI entrypoint.
- `scripts/vitruvius/features.py` gives a frozen default-false feature contract.
- `config/vitruvius.yaml` shows the existing repo pattern clearly: new capabilities ship behind explicit flags first.
- `scripts/vitruvius/cli_experience.py` and `scripts/tests/test_pipeline_cli_byte_identity.py` are additional load-bearing CLI surfaces. Any AEC-facing CLI change that perturbs help output, command inventory, or byte-identity guarantees is already inside blast radius.

#### Deterministic storage and replay substrate
- `scripts/vitruvius/graph/contract.py` defines frozen graph dataclasses and validation helpers.
- `scripts/vitruvius/graph/snapshot.py` writes deterministic JSON snapshots with `sort_keys=True` and explicit optional-field handling.
- `scripts/vitruvius/graph/event_store.py` + `graph/rocksdb_event_store.py` provide append-only replay projection.
- `scripts/vitruvius/graph/temporal_query.py` provides temporal interval filtering in memory.
- `scripts/vitruvius/review/stateful_registry.py` + RocksDB variant provide feature-gated mutable caches.
- `scripts/vitruvius/kv_migrate.py` provides idempotent backend migration.
- `scripts/vitruvius/graph/dataset_manifest.py` and dataset-scoped graph builds already prove a richer manifest/pilot/freshness style than the root `latest_*` graph aliases.

#### Spatial boundary and Python↔TypeScript integrity
- `scripts/vitruvius/spatial/schema.py` validates a frozen v1 spatial payload.
- `scripts/vitruvius/spatial/contract_reader.py` verifies a SHA-256 footer when present.
- `scripts/vitruvius/spatial/walker.py` turns file contracts into sorted candidate records.
- `scripts/vitruvius/spatial/cli.py` already exposes `ingest-spatial` and `evaluate-spatial` as user-visible control-plane commands under flag control.
- `spatial-daemon/src/types.ts` mirrors the current Python boundary.
- `spatial-daemon/src/contract_writer.ts` emits integrity-footed files.
- `spatial-daemon/README.md` correctly states the daemon is an isolated sibling process, not shared-runtime orchestration.
- `scripts/tests/test_spatial_bootstrap.py`, `scripts/tests/test_spatial_cli.py`, and `scripts/tests/test_spatial_walker.py` already lock in current flag defaults and ingest behavior.

#### Narrow Z3 and optimization precedents
- `scripts/vitruvius/spatial/constraint_solver.py` does lazy-import scalar Z3 checks.
- `scripts/vitruvius/geometric/inequality_compiler.py` compiles extracted numeric rules into Z3 expressions.
- `scripts/vitruvius/geometric/pareto_optimizer.py` is a narrow deterministic LP-style optimizer.

#### Rust compute extension discipline
- `scripts/vitruvius/engine_rs/core/` provides pure compute primitives only.
- `scripts/vitruvius/engine_rs/pyo3_shim/src/lib.rs` proves the right thin-binding pattern.
- `scripts/vitruvius/engine_rs/spatial_kernels/` and `stats_kernels/` prove benchmark-driven kernel ports.
- `scripts/vitruvius/engine_rs/__init__.py` proves graceful Python fallback and lazy exposure of fast-path symbols.
- `scripts/vitruvius/normalization/outlier_detector.py` is an important additional precedent: it shows a safe internal perf cache (`_RS_MODEL_CACHE`) that does **not** become truth-bearing state.

#### Tooling / explanation precursors
- `scripts/vitruvius/query/result.py` and `query/engine.py` define frozen evidence-bearing result contracts.
- `scripts/vitruvius/compound/dependency_tracker.py` + `differential_propagator.py` prove deterministic invalidation.
- `scripts/vitruvius/compound/adversarial.py` and `compound/dspy_compiler.py` show bounded LLM role separation and prompt-compilation patterns.

### 4.2 What does not exist

The following AEC-planned surfaces are absent:
- `scripts/vitruvius/aec/`
- `scripts/vitruvius/aec/contracts/`
- `scripts/vitruvius/aec/boundary/`
- `scripts/vitruvius/aec/vault/`
- `scripts/vitruvius/aec/ecs/`
- `scripts/vitruvius/aec/spatial/`
- `scripts/vitruvius/aec/verification/`
- `scripts/vitruvius/aec/coordination/`
- `scripts/vitruvius/aec/optimization/`
- `scripts/vitruvius/aec/pricing/`
- `scripts/vitruvius/aec/tools/`

Also absent:
- AEC DTO family and schema evolution policy
- `frame_id`, payload-level `unit_system`, operation-class tolerance policy
- AEC rule AST schema and vault write contract
- AEC candidate/canonical store separation
- AEC world revision / snapshot / replay envelope
- AEC CLI surface
- AEC feature flags
- AEC fixture families
- `scripts/tests/test_aec_*`
- `005_Operational-Intelligence-Layer/aec/`
- `006_System-Manifests/cache/` for planned AEC vault/caches

### 4.3 What exists only partially

#### Boundary translation
- `spatial/concept_mapper.py` only verifies that a concept id exists; it does not do robust boundary mediation or refusal taxonomy.
- `ontology/ifc_mapping.yaml` is a small static mapping table, not a versioned AEC translation surface.
- `spatial/walker.py` parses contract files and then discards `schema_version`, `generated_at_utc`, `source_daemon`, footer presence/digest, and integrity metadata when it collapses into `SpatialCandidate` and `SpatialEdgeCandidate`.

#### Spatial kernel
- Current compute is AABB-centric and narrow (`spatial_edge_builder.py`, `proximity_jump.py`, `spatial-daemon/src/cli.ts`).
- `spatial-daemon/src/gjk.ts` exists, but it is not the authoritative Python-integrated clash path today. Treating it as the current engine would be wrong.
- There is no voxel engine, no terrain/heightmap ingest path, no occupancy service, and no AEC routing service.

#### Formal verification
- Current Z3 paths are scalar and bounded.
- There is no vault-admitted AST → verifier pipeline.
- No witness envelope, unsat-core artifact, oversize-query refusal, or timeout taxonomy exists.

#### Optimization and pricing
- There is one narrow deterministic optimizer, not a full candidate-frontier subsystem.
- There is no pricebook schema, currency policy, quantity-to-price contract, or pricing artifact lineage.

### 4.4 What is dangerous to assume

- `bevy_ecs` is present — it is not.
- current spatial JSON already carries `frame_id` — it does not.
- current spatial JSON already carries payload-level units — it does not.
- tolerance policy exists — it does not.
- the current spatial import path is hardened — it is not; it still supports legacy no-footer mode.
- TypeScript is “just types” — it is not; it already contains geometric computation.
- AEC vault storage exists because RocksDB patterns exist — it does not.
- AEC pricing exists because optimization precedent exists — it does not.
- feature-disabled anchors are “live baseline” — they are not.
- the current `001B_Spatial-Source-Layer` proves an active real-data boundary lane — it does not; in this repo snapshot it contains only `.gitkeep` and `README.md`.

## 5. AEC Engine Readiness Scorecard

| Subsystem | Grade | File-grounded evidence | Why this grade is harsh |
|---|---:|---|---|
| Boundary Translation | C- | `spatial/schema.py`, `contract_reader.py`, `walker.py`, `concept_mapper.py`, `ifc_registry.py`, `spatial-daemon/src/types.ts`, `contract_writer.ts` | strong v1 boundary discipline, but no AEC DTOs, no frame policy, no refusal taxonomy, no import manifest id |
| Knowledge Vault | D+ | `graph/event_store.py`, `graph/rocksdb_event_store.py`, `review/stateful_registry.py`, `kv_migrate.py`, `graph/temporal_query.py`, `promotion_validator.py` | replay substrate exists, but no AEC rule-vault contract, no `rule:`/`cost:` runtime surface, no candidate/canonical vault split |
| ECS Core | D | `graph/contract.py`, `graph/snapshot.py`, dependency tracker, `engine_rs/core` | useful patterns only; no ECS world, no component registry, no schedule groups, no AEC snapshot/replay fixtures, no runtime crate choice |
| Spatial Kernel | D+ | `spatial_edge_builder.py`, `proximity_jump.py`, `engine_rs/core`, `engine_rs/spatial_kernels`, `spatial-daemon/src/*` | current substrate is narrow and partially feature-disabled; no AEC compute DTOs, no routing/occupancy service, no frame/tolerance contract |
| Z3 Verification | D+ | `spatial/constraint_solver.py`, `geometric/inequality_compiler.py`, `spatial/cli.py` | the repo proves bounded scalar Z3 discipline only, not an AEC verification service |
| Coordination | D | `compound/dependency_tracker.py`, `compound/differential_propagator.py`, `query/engine.py`, `graph/physics.py` | deterministic invalidation exists, but no discipline model, precedence manifest, issue schema, or replay log |
| Pricing | F | only weak precedents | no runtime substrate worth calling “pricing” yet |
| Optimization | D | `geometric/pareto_optimizer.py`, `graph/physics.py` | tiny deterministic precedent exists, but no verified-candidate pipeline or reproducibility envelope |
| LLM Tooling | C- | `compound/adversarial.py`, `compound/dspy_compiler.py`, `query/result.py`, `query/engine.py`, `graphrag_router.py` | bounded tooling patterns exist, but no AEC tool authority fence or refusal taxonomy |
| Cross-language boundary integrity | C+ | Python/TS contract + integrity footer + tests | good current v1 parity, but AEC-required fields are absent and TS already has compute creep risk |
| Determinism / replay / governance | C- | event stores, dataset manifests, promotion validator, snapshot writer, backend parity, migration path | strongest substrate in the repo, but not yet materialized for AEC-specific truth objects and too many live surfaces still depend on ambient clock or mutable aliases |
| Audit artifact identity / snapshot binding | D | dataset-scoped graph builds only | root `latest_*` graph artifacts, review outputs, and prompt/audit traces are not sufficient AEC-grade audit envelopes |

**Bottom line:** the repo is **not empty**, but most AEC subsystem plans are still trying to land on substrate that exists only as precedent, not as implementation.

## 6. Contradictions Between Plans and Current Code

### 6.1 ECS spec vs live code
- The AEC ECS spec (`.ai/06_specs/AEC_ENGINE/02_ECS_AND_COMPONENT_DESIGN_RULES.md`) is built around `bevy_ecs` and a Rust-side ECS architecture.
- The live Rust workspace under `scripts/vitruvius/engine_rs/` contains `core`, `pyo3_shim`, `pdf`, `spatial_kernels`, `stats_kernels` — **no ECS crate exists**.
- Any implementation plan that behaves as if Rust ECS is already scaffolded is fiction.

### 6.2 Spatial protocol vs live code
- The spatial spec (`03_SPATIAL_COMPREHENSION_PROTOCOL.md`) describes voxel CSG, resolution hierarchy, heightmaps, routing, and a 3-layer execution stack.
- The live code today provides:
  - AABB contracts
  - adjacency edges
  - proximity weighting
  - optional GJK in TypeScript
  - octree primitives in Rust
- That is a useful precursor, not the described spatial engine.

### 6.3 Knowledge vault spec vs live code
- The vault spec (`04_KNOWLEDGE_VAULT_AND_RULE_AST_CONTRACT.md`) prescribes `rule:`, `cost:`, `terrain:`, `asset:`, and `entity:` namespaces plus a four-block JSON payload.
- Live code has graph event logs and verdict caches, not a rule vault.
- The existence of RocksDB patterns must not be misreported as an existing AEC vault.

### 6.4 TypeScript boundary contract vs live TypeScript code
- Governance wants TypeScript bounded to a boundary layer.
- Live `spatial-daemon/src/cli.ts`, `aabb.ts`, and `gjk.ts` already do geometry work.
- That is still acceptable because it is boundary-local and isolated, but it proves the drift risk is already present, not theoretical.

### 6.5 Comment / runtime drift inside live code
- `scripts/vitruvius/graph/event_store.py` still says the plan originally specified RocksDB but SQLite was used because a wheel was unavailable.
- Current runtime factories and config defaults now prefer RocksDB (`hp_rocksdb_event_store: true`, `hp_rocksdb_verdict_cache: true`).
- Code comments are not authoritative by themselves; runtime wiring must be checked directly.

### 6.6 Boundary fixture and ontology drift already exist
- `scripts/tests/fixtures/spatial/sample_residential_01_spatial.json` has no integrity footer and uses `source_daemon: "spatial-daemon@0.1.0"`, while `spatial-daemon/src/cli.ts` emits `vitruvius-spatial-daemon@0.1.0`.
- `scripts/vitruvius/ontology/ifc_mapping.yaml` uses `concept-setback`, while spatial fixtures and canonical concept surfaces use `concept-setbacks`.
- Even low-stakes boundary metadata and concept IDs already drift across Python, TypeScript, fixtures, and ontology mapping. AEC cannot rely on “informational” metadata staying aligned without tests.

## 7. Repo Anchor Reuse Map

### 7.1 Strong anchors to reuse directly

| Anchor | Why it matters | Reuse rule |
|---|---|---|
| `scripts/pipeline_cli.py` | lazy imports and bounded subcommands | AEC commands must follow this pattern; no eager heavy imports |
| `scripts/vitruvius/features.py` + `config/vitruvius.yaml` | safe rollout discipline | AEC flags default false, with matching tests in `scripts/tests/test_features.py` |
| `scripts/vitruvius/graph/contract.py` | frozen contract + validation idiom | reuse style, not ID vocabulary blindly |
| `scripts/vitruvius/graph/snapshot.py` | deterministic snapshot writer | reuse for AEC artifacts, but do not inherit optional-field dropping casually |
| `scripts/vitruvius/graph/dataset_manifest.py` | manifest-scoped, pilot-gated artifact pattern | strong precedent for AEC fixture/manifest-driven pilot slices |
| `scripts/vitruvius/graph/event_store.py` + RocksDB variant | append-only replay substrate | reuse event/replay discipline, not the current thin envelope as-is |
| `scripts/vitruvius/review/stateful_registry.py` + RocksDB variant | bounded mutable-cache pattern | reuse only for non-authoritative caches |
| `scripts/vitruvius/kv_migrate.py` | idempotent migration discipline | reuse for backend transitions, not for truth semantics |
| `scripts/vitruvius/promotion_validator.py` | hard truth-admission gates | copy the governance posture |
| `scripts/vitruvius/spatial/schema.py` | inline schema validation idiom | reuse pattern; evolve only in lockstep with TS |
| `scripts/vitruvius/spatial/contract_reader.py` | boundary integrity check | AEC import path should use stricter mode than current legacy default |
| `scripts/vitruvius/query/result.py` + `query/engine.py` | frozen machine-facing evidence contracts | reuse for AEC artifact explanation surfaces |
| `scripts/vitruvius/compound/dependency_tracker.py` + `differential_propagator.py` | deterministic invalidation | strong precursor for coordination cascades |
| `scripts/vitruvius/engine_rs/__init__.py` | extension fallback and explicit exported fast paths | future AEC kernels must be exposed this way, not via implicit imports |
| `scripts/vitruvius/engine_rs/core` / `pyo3_shim` / `spatial_kernels` / `stats_kernels` | selective Rust extension points | primary acceleration targets; do not create new crates first without evidence |
| `spatial-daemon/src/types.ts` + `contract_writer.ts` | current cross-language contract parity | evolve only atomically with Python |

### 7.2 Precedents only — do not use as dumping grounds
- `scripts/vitruvius/spatial/walker.py` — deterministic candidate extraction style, but current DTO collapse loses provenance
- `scripts/vitruvius/spatial/concept_mapper.py` — only direct concept-id existence checks
- `scripts/vitruvius/ontology/ifc_registry.py` and `ontology/ifc_mapping.yaml` — useful loader pattern, but too shallow and already drifting on IDs
- `scripts/vitruvius/spatial/constraint_solver.py`
- `scripts/vitruvius/geometric/inequality_compiler.py`
- `scripts/vitruvius/geometric/pareto_optimizer.py`
- `scripts/vitruvius/query/*`
- `scripts/vitruvius/compound/*`
- `spatial-daemon/src/gjk.ts`

Reason: these files prove useful idioms, but if AEC semantics are inserted directly into them, the repo will sprawl instead of gaining a bounded subsystem.

## 8. Blast Radius Analysis

### 8.1 Direct touchpoints that the first audit underplayed

| Path | Why it is a direct touchpoint | Expected prep need |
|---|---|---|
| `scripts/vitruvius/aec/` | new AEC root | create |
| `scripts/pipeline_cli.py` | future AEC CLI | additive + lazy-import discipline |
| `scripts/vitruvius/features.py` | AEC flags depend on frozen feature contract | additive only |
| `config/vitruvius.yaml` | AEC flags, default false | contract freeze |
| `scripts/tests/test_features.py` | feature flag additions require tests | additive |
| `scripts/vitruvius/spatial/schema.py` | current boundary must change for AEC v2 | contract freeze |
| `scripts/vitruvius/spatial/contract_reader.py` | importer hardening and version-aware parse rules | contract freeze |
| `scripts/vitruvius/spatial/walker.py` | current candidate extraction will be pressured by v2 schema and currently discards provenance | bounded adaptation or replacement |
| `scripts/vitruvius/spatial/cli.py` | existing `ingest-spatial` / `evaluate-spatial` surfaces already lock in help/flag/output behavior | control-plane regression risk |
| `scripts/vitruvius/cli_experience.py` | command docs and output framing are operator-facing | help/UX drift risk |
| `scripts/tests/test_pipeline_cli_byte_identity.py` | protects byte-identity and command-set behavior | direct CLI blast radius test surface |
| `scripts/tests/test_spatial_cli.py` | locks current CLI/flag behavior | direct blast radius test surface |
| `scripts/tests/test_spatial_walker.py` | locks current ingest behavior | direct blast radius test surface |
| `spatial-daemon/src/types.ts` | schema parity | contract freeze |
| `spatial-daemon/src/contract_writer.ts` | footer/version parity | contract freeze |
| `spatial-daemon/src/cli.ts` | boundary-local compute path may need minimal adaptation only | hard boundary review |
| `scripts/vitruvius/ontology/ifc_mapping.yaml` + `ifc_registry.py` | current mapping precedent is too shallow to extend blindly | versioned replacement path |
| `scripts/vitruvius/graph/contract.py` | any AEC integration with current graph IDs/types will pressure prefix, status, and evidence vocabularies | explicit decision required |
| `scripts/vitruvius/graph/snapshot.py` | likely serializer precedent for AEC snapshots | review for provenance field retention |
| `scripts/vitruvius/graph/dataset_manifest.py` | strong manifest/pilot precedent for AEC pilot artifacts | reuse candidate |
| `scripts/vitruvius/graph/cli.py` | root graph build writes `latest_*` aliases and dataset-scoped immutable builds | direct artifact-identity policy touchpoint |
| `scripts/vitruvius/graph/builder.py` | current snapshot builder can fall back to filesystem mtime and ambient wall clock | direct determinism touchpoint |
| `scripts/vitruvius/engine_rs/__init__.py` | any new AEC fast path needs export/fallback handling | additive |
| `scripts/vitruvius/engine_rs/core/*` | future narrow compute DTOs or indices | selective extension |
| `scripts/vitruvius/engine_rs/spatial_kernels/*` | future hot spatial kernels | selective extension |
| `scripts/vitruvius/engine_rs/pyo3_shim/src/lib.rs` | bindings for future kernels | additive |
| `005_Operational-Intelligence-Layer/aec/` | projected AEC machine artifacts | create only after contract freeze |
| `006_System-Manifests/cache/` | planned mutable AEC stores/caches | create only after layout freeze |
| `001B_Spatial-Source-Layer/README.md` and path semantics | decide whether AEC boundary keeps using 001B or introduces a new bounded landing zone | contract decision |

### 8.2 Indirect touchpoints that the first audit missed or softened

| Path | Why it is indirectly affected |
|---|---|
| `scripts/vitruvius/query/result.py` | likely pattern source for AEC explanation/tool result contracts |
| `scripts/vitruvius/query/engine.py` | evidence-bearing response pattern may be generalized |
| `scripts/vitruvius/query/nl_translator.py` | current free-form heuristic NL routing is not an AEC authority precedent, but it will be pressure-tested by any AEC tool layer |
| `scripts/vitruvius/normalization/outlier_detector.py` | safe non-authoritative cache pattern for future hot-path wrappers |
| `scripts/vitruvius/spatial/_feature_gate.py` | current internal helper must **not** become a cross-subsystem dependency leak; AEC should create its own neutral feature helper if needed |
| `scripts/tests/test_spatial_bootstrap.py` | proves additive contract evolution and flag-default rules |
| `scripts/tests/test_engine_rs_octree.py` | likely extension point for future AEC Rust kernel contract tests |
| `scripts/tests/test_spatial_edge_builder_parity.py`, `test_proximity_jump_weight_parity.py`, `test_mahalanobis_parity.py` | benchmark/parity discipline precedents for future AEC kernels |
| `005_Operational-Intelligence-Layer/graph/datasets/*` | shows the repo already supports pilot-scoped graph outputs; AEC should not bypass this manifest mindset |
| `scripts/vitruvius/review/cot_audit.py`, `review/tension_analyzer.py`, `review/ontology_prompt_builder.py` | current review/audit/prompt surfaces use wall-clock timestamps and prose-rich prompt payloads; these are cautionary precedents, not AEC truth precedents |
| `scripts/vitruvius/ontology/owl_exporter.py` and ontology tests | AEC concept/IFC/OWL changes will pressure ontology export and concept-frontmatter validation, even if boundary work begins elsewhere |

### 8.3 Fragile modules and why they are fragile

1. `scripts/vitruvius/spatial/schema.py`
   - fragile because Python and TS must advance atomically.
2. `scripts/vitruvius/spatial/contract_reader.py`
   - fragile because it currently carries a legacy compatibility mode that is too weak for AEC truth-bearing import paths.
3. `spatial-daemon/src/types.ts` + `src/contract_writer.ts`
   - fragile because they are load-bearing for parity and already close to becoming a second compute plane.
4. `scripts/vitruvius/graph/contract.py`
   - fragile because AEC integration will pressure existing ID, status, and evidence vocabularies.
5. `scripts/vitruvius/engine_rs/__init__.py`
   - fragile because new Rust exports must preserve fallback behavior and not break unbuilt hosts.
6. `scripts/vitruvius/graph/event_store.py`
   - fragile because its comments are stale and its current envelope is too thin for AEC audit identity.
7. `scripts/vitruvius/graph/cli.py` + root `latest_*` outputs
   - fragile because operator aliases are easy to mistake for replay-safe artifacts.
8. current repo baseline (`git status --short`)
   - fragile because unrelated modified/untracked files make blast radius and verification less trustworthy.

## 9. Cross-Language Parity Risk Register

| Risk | Current evidence | Why it matters for AEC |
|---|---|---|
| Python schema ↔ TS type drift | `spatial/schema.py` vs `spatial-daemon/src/types.ts` | AEC v2 contract will definitely require more fields; unilateral edits will corrupt imports |
| Footer/reader drift | `contract_writer.ts` ↔ `contract_reader.py` | integrity footer is currently the strongest boundary control; drift breaks trust |
| Legacy no-footer compatibility persists too long | `parse_contract(... require_footer=False)` and `walker.py` default usage | safe for historical files, unsafe for AEC authoritative imports |
| TS emits implicit meters/3-decimal rounding | `spatial-daemon/src/cli.ts` | AEC cannot let emitter-local rounding become system-wide tolerance policy |
| TS compute creep | `aabb.ts`, `gjk.ts`, `cli.ts` | without discipline, TS becomes a second spatial kernel |
| Metadata drift in fixtures | sample fixture vs emitter `source_daemon` string | proves metadata is not yet frozen tightly enough for audit-bearing AEC artifacts |
| Missing schema validators in boundary v1 | no `frame_id`, no payload-level `unit_system`, no tolerance manifest, no uniqueness checks, no bbox min≤max validation, no edge→instance referential integrity, weak `generated_at_utc` typing | current boundary contract is not AEC-ready even before feature expansion |
| No end-to-end TS→Python parity lane | TS tests and Python tests are siloed today | AEC cannot claim parity until one test runs TS emission through Python reader + validator + walker + mapper in one path |

**Required parity gates before AEC work:**
- Python + TS schema version must advance in one commit
- footer verification must be required for new AEC imports
- shared fixture set must include valid, corrupt, truncated, wrong-version, wrong-frame, wrong-unit, and missing-tolerance cases
- one end-to-end lane must run a TS-emitted artifact through Python reader + footer verification + schema validation + walker ingest + concept mapping
- any TS compute extension must be justified as boundary-local and mirrored or superseded on the Python/Rust side if it becomes authoritative.

## 10. Python-First vs Rust Migration Analysis

### 10.1 Corrected migration table

| Area | Start in | Stay in | Rust later? | Why |
|---|---|---|---|---|
| DTOs, schemas, versioning, import/export manifests | Python | Python | No | semantics and governance, not kernels |
| Boundary importers/exporters | Python | Python | No | refusal logic, provenance, mapping diagnostics belong in orchestration |
| Rule AST compilation and vault admission | Python | Python | No | truth/governance must not migrate into Rust |
| ECS world semantics and schedule rules | Python | Python first | Maybe, selective only | the world model must stabilize before any kernel port |
| Clash / clearance / occupancy / route primitives | Python reference | Python + Rust fast paths | Yes | best legitimate Rust lane after benchmarks |
| Spatial indexing and broadphase | existing Rust-capable substrate | Rust for hot path, Python orchestration | Already yes | use `engine_rs/core` and `spatial_kernels` |
| Z3 query assembly and artifact formatting | Python | Python | No | solver orchestration is not a compute kernel |
| Coordination precedence and escalation | Python | Python | No by default | semantics-heavy subsystem; only isolated numeric subkernels may ever move, not the coordination layer |
| Quantity aggregation / pricing policy | Python | Python | No by default | pricing semantics, provenance, freshness, and currency policy stay Python-owned unless a named numeric loop is isolated and proven hot |
| Frontier/dominance computation | Python | Python | No by default | optimization policy, objective semantics, and reproducibility stay Python-owned unless a tiny pure numeric kernel is isolated and benchmarked |
| LLM tool router/refusals/explainer | Python | Python | No | authority fence and explanation stay in orchestration |
| TypeScript boundary | TypeScript | TypeScript boundary only | N/A | do not let it become orchestration or authority |

### 10.2 Legitimate later Rust candidates

Only after Python reference paths, parity tests, and AEC-specific benchmarks exist:
- future AEC clash/clearance kernels
- future occupancy aggregation kernels
- future bounded route-candidate kernels
- future broadphase update/index maintenance kernels
- only the pure numeric portion of later frontier dominance kernels if candidate-set size proves large enough
- only isolated ECS iteration/index update kernels if replay-stable Python ECS shows real hotspot evidence

Current file-grounded precedent for legitimate later Rust scope:
- Python precursors: `scripts/vitruvius/spatial/spatial_edge_builder.py`, `spatial/proximity_jump.py`, `normalization/outlier_detector.py::mahalanobis_distance`
- current Rust ports: `scripts/vitruvius/engine_rs/spatial_kernels/src/adjacency_edges.rs`, `distance_weight.rs`, `scripts/vitruvius/engine_rs/stats_kernels/src/mahalanobis.rs`

### 10.3 Not legitimate Rust candidates

These should stay out of Rust entirely:
- boundary translation DTOs and schema validation
- IFC mapping/version tables
- rule AST admission and provenance logic
- tool routing and refusal behavior
- pricing authority and currency/freshness policy
- formal query assembly around Z3
- candidate/canonical promotion rules
- semantics-heavy coordination logic
- optimization policy and reproducibility orchestration

### 10.4 Benchmark prerequisites before any Rust port

Before porting any AEC function to Rust, require **all** of the following:
1. named Python reference implementation
2. representative workload fixture
3. worst-case workload fixture
4. explicit hardware context (baseline: Apple M2 8GB per policy)
5. parity harness with documented tolerance
6. pre-port benchmark artifact committed or logged
7. memory/allocation evidence, not just wall time
8. post-port benchmark on same workload and hardware
9. documented fallback behavior when extension is unbuilt
10. no truth-bearing logic crossing the boundary
11. AEC-specific benchmark harness, not reuse of generic `bench_rust_mig_baseline.py` alone
12. flag-off baseline and flag-on comparison on the same fixture
13. explicit threshold and acceptance gate recorded before the port

## 11. Validation / Test / Benchmark Audit

### 11.1 Validation evidence gathered in this audit

Executed and passed:
- targeted pytest lane: **117 passed**
- `cargo test --workspace --quiet`: observed **26 executed Rust tests passed** in this environment
- `spatial-daemon` tests: **21/21 passed**
- `npm run typecheck`: passed

### 11.2 Important caveat on validation evidence

The roadmap claims 33 Rust unit tests in one historical snapshot. This audit run observed 26 executed Rust tests in the current local command output. That may be harmless (workspace/test-layout drift, filtered targets, or changed crate composition), but it is still a **documentation-vs-local-evidence discrepancy** and should not be glossed over.

### 11.3 Reusable existing test families

#### Contract / parity / boundary
- `scripts/tests/test_spatial_schema.py`
- `scripts/tests/test_spatial_contract_reader.py`
- `spatial-daemon/tests/contract_writer.test.ts`
- `scripts/tests/test_spatial_cli.py`
- `scripts/tests/test_spatial_bootstrap.py`
- `scripts/tests/test_pipeline_cli_byte_identity.py`

#### Replay / storage / migration / temporality
- `scripts/tests/test_graph_contract.py`
- `scripts/tests/test_graph_event_store.py`
- `scripts/tests/test_graph_event_store_delta.py`
- `scripts/tests/test_rocksdb_event_store.py`
- `scripts/tests/test_rocksdb_stateful_registry.py`
- `scripts/tests/test_kv_migrate_cli.py`
- `scripts/tests/test_temporal_query.py`

#### Rust fast-path and parity discipline
- `scripts/tests/test_spatial_edge_builder_parity.py`
- `scripts/tests/test_proximity_jump_weight_parity.py`
- `scripts/tests/test_mahalanobis_parity.py`
- `scripts/tests/test_engine_rs_octree.py`
- `scripts/tests/test_bench_rust_mig_baseline.py`
- `scripts/tests/test_bench_kv_backends.py`
- `scripts/tests/test_integrity_audit.py`

#### Formal-solving / optimization precedents
- `scripts/tests/test_spatial_constraint_solver.py`
- `scripts/tests/test_geometric_inequality_compiler.py`
- `scripts/tests/test_geometric_pareto_optimizer.py`

#### Explanation / tool precursors
- `scripts/tests/test_query_result.py`
- `scripts/tests/test_query_engine.py`
- `scripts/tests/test_graphrag_router.py`
- `scripts/tests/test_compound_dspy_compiler.py`
- `scripts/tests/test_review_cot_audit.py`

### 11.4 Missing test families (hard gap)

Missing entirely today:
- `scripts/tests/test_aec_boundary_*`
- `scripts/tests/test_aec_vault_*`
- `scripts/tests/test_aec_ecs_*`
- `scripts/tests/test_aec_spatial_*`
- `scripts/tests/test_aec_z3_*`
- `scripts/tests/test_aec_coordination_*`
- `scripts/tests/test_aec_pricing_*`
- `scripts/tests/test_aec_optimization_*`
- `scripts/tests/test_aec_tools_*`

The plans name specific missing suites that should be called out explicitly, not hand-waved:
- `scripts/tests/test_aec_boundary_contract_parity.py`
- `scripts/tests/test_aec_vault_backend_parity.py`
- `scripts/tests/test_aec_ecs_replay.py`
- `scripts/tests/test_aec_spatial_parity.py`
- `scripts/tests/test_aec_z3_replay.py`
- `scripts/tests/test_aec_coordination_replay.py`
- `scripts/tests/test_aec_pricing_refusals.py`
- `scripts/tests/test_aec_optimization_replay.py`
- `scripts/tests/test_aec_tools_refusals.py`

### 11.5 Missing parity harnesses

- Python↔TypeScript AEC boundary v2 parity
- Python ECS ↔ any future Rust ECS subset parity
- Python AEC spatial reference ↔ Rust AEC spatial kernels parity
- SQLite↔RocksDB AEC vault parity
- verification replay parity from stored artifacts
- pricebook/quantity replay parity
- optimization seeded replay parity
- end-to-end TS→Python import parity

### 11.6 Missing fixture families

Required before implementation is safe:
- valid AEC DTO import fixtures
- wrong-version / wrong-frame / wrong-unit / missing-tolerance fixtures
- candidate-rule vs canonical-rule vault fixtures
- ECS world snapshot fixtures
- sat / unsat / timeout / oversize verification fixtures
- coordination cascade / precedence / oscillation fixtures
- pricebook snapshot + quantity fixtures
- verified-candidate frontier fixtures
- corrupt/truncated/forged boundary artifacts

### 11.7 Dependency and optional-import risk

The current repo uses several optional or lazy imports:
- `jsonschema` in `spatial/schema.py`
- `z3` in `spatial/constraint_solver.py` and GEOM tests
- `cvxpy` in `geometric/pareto_optimizer.py`
- `rocksdict` in RocksDB paths/tests

AEC work must explicitly decide for each dependency whether it is:
- mandatory for the base AEC slice
- optional and feature-gated
- unsupported on constrained hosts

Do not quietly inherit the repo’s optional-import pattern without deciding whether the AEC baseline is allowed to depend on those packages.

## 12. Determinism / Replay / Truth Governance Audit

### 12.1 Strong patterns to copy
- append-only event logs
- deterministic snapshot writing
- hard promotion validation
- backend parity with idempotent migration
- explicit feature-gated rollout
- dataset-scoped immutable artifact builds in `scripts/vitruvius/graph/cli.py` + `graph/dataset_manifest.py`

### 12.2 Hidden mutable state risks

| Surface | Risk | Judgment |
|---|---|---|
| `review/stateful_registry.py` | persistent mutable cache with `INSERT OR REPLACE` plus purge/vacuum surface | acceptable only as non-authoritative review cache, not truth |
| `review/rocksdb_stateful_registry.py` | same mutable overwrite/purge semantics in RocksDB | acceptable only as performance cache precedent |
| `normalization/outlier_detector.py::_RS_MODEL_CACHE` | in-memory perf cache | acceptable because cached data is derived, non-authoritative, and auto-evicting |
| future AEC caches | risk of becoming hidden authority | unacceptable unless explicitly non-truth-bearing and replay-safe |

### 12.3 Additional replay and artifact-identity hazards

1. `scripts/vitruvius/graph/cli.py` writes root `005_Operational-Intelligence-Layer/graph/latest_graph_snapshot.json` and `latest_graph_integrity_report.json` aliases using `_utc_run_id()`. These are operator conveniences, not safe AEC replay precedents.
2. `scripts/vitruvius/graph/builder.py` can fall back to filesystem `st_mtime` and ambient wall clock for dates. That is acceptable for today’s graph tooling but not for AEC-grade audit identity.
3. `scripts/vitruvius/graph/temporal_query.py` is an interval filter only; it does not impose stable ordering beyond caller iterable order.
4. `scripts/vitruvius/review/cot_audit.py` and `review/tension_analyzer.py` write useful audit traces, but they still depend on ambient `datetime.now(...)` rather than declared run clocks or bound snapshot ids.
5. `scripts/vitruvius/query/result.py` and `query/engine.py` carry citations but no snapshot binding, audit cursor, subsystem identity, or declared temporal clock.

### 12.4 Truth-boundary leak risks

1. raw legal prose entering Z3 directly
2. free-form LLM output becoming rule-vault truth without AST admission
3. IFC external schema becoming internal ontology by convenience
4. pricebook spreadsheets or ad hoc JSON becoming runtime truth without schema/version/currency policy
5. TypeScript boundary payloads becoming implicit authority because Python lacks stricter validation
6. AEC tooling copying current prompt builders (`review/ontology_prompt_builder.py`, `query/nl_translator.py`) that still rely on prose-rich heuristics rather than explicit artifact refs/refusals

### 12.5 Candidate / canonical separation requirement

The AEC specs require a candidate/canonical distinction. The repo already knows how to do truth admission in spirit (`promotion_validator.py`), but **no AEC implementation exists yet**. Therefore:
- any first-pass AEC vault write path that does not preserve candidate/canonical separation is an immediate red flag
- any optimization, pricing, or tooling layer that reads candidate records as if they were canonical is an architectural failure, not a bug.

Concrete current-path truth split precedent:

| Path | Current role | AEC lesson |
|---|---|---|
| `006_System-Manifests/runs/latest_relationship_review_high_confidence.json` | candidate/run convenience artifact | not canonical truth |
| `006_System-Manifests/runs/latest_relationship_review_merged.json` | merged review convenience artifact | not canonical truth |
| `006_System-Manifests/runs/latest_promotion_audit.log` | admission log | log only, not truth record |
| `003_Canonical-Knowledge-Layer/shared/relationships/*.md` | promoted canonical truth | real truth-bearing precedent |
| `006_System-Manifests/registries/graph_registry.csv` | currently header-only / weak registry surface | not a meaningful replay anchor yet |

## 13. Contract Freeze Dependencies

These dependencies are non-negotiable:

1. **Audit/snapshot envelope freeze before subsystem coding** (`snapshot_id`, actor, subsystem, status taxonomy, input/output artifact refs, declared clock source)
2. **Namespace freeze before subsystem coding**
3. **DTO/version/id freeze before boundary, vault, ECS, or verifier coding**
4. **frame/unit/tolerance freeze before spatial or Z3 coding**
5. **rule AST + candidate/canonical freeze before verifier coding**
6. **world/snapshot/replay freeze before coordination coding**
7. **quantity contract + currency/pricebook freeze before pricing coding**
8. **verified-candidate artifact freeze before optimization coding**
9. **deterministic artifact availability before tool-catalog coding**

Unsafe parallelization assumptions corrected here:
- boundary import, vault projection, and coordination logging must not proceed before the audit/snapshot envelope is frozen
- boundary translation and vault work cannot safely diverge if DTO ids and provenance envelopes are still soft
- ECS and spatial cannot safely run in parallel before `frame_id`, units, and tolerance policy are frozen
- pricing and optimization cannot safely start in parallel with verification design; they depend on verified-candidate outputs, not planned ones.

## 14. Recommended Pre-Implementation Refactors

| Path | Action | Why | Required | Blocker |
|---|---|---|---:|---:|
| `scripts/vitruvius/spatial/schema.py` | define boundary v2 with `frame_id`, payload-level unit system, manifest/version fields, uniqueness checks, bbox min≤max validation, edge→instance referential integrity, and explicit invalid-state rejection | current v1 is too small for AEC | Yes | Yes |
| `scripts/vitruvius/spatial/contract_reader.py` | split legacy compatibility path from strict AEC import path; AEC path must require footer + version checks | current default is too permissive | Yes | Yes |
| `scripts/vitruvius/spatial/walker.py` | widen or replace if AEC import must retain integrity metadata, schema version, emitted daemon identity, and footer presence | current DTO collapse discards provenance | Yes | Yes |
| `spatial-daemon/src/types.ts` | advance only atomically with Python schema | prevents schema drift | Yes | Yes |
| `spatial-daemon/src/contract_writer.ts` | preserve footer parity and add only boundary metadata, not orchestration logic | keep TS bounded | Yes | Yes |
| `spatial-daemon/src/cli.ts` | explicitly forbid AEC orchestration logic here; keep emitter-local only | prevent second orchestration plane | Yes | Yes |
| `scripts/vitruvius/graph/contract.py` | decide whether AEC reuses graph IDs/types or gets separate contract family | current prefix/status/evidence vocabularies cannot be stretched ad hoc | Yes | Yes |
| `scripts/vitruvius/graph/snapshot.py` | review whether serializer omission rules are acceptable for AEC provenance-bearing artifacts | AEC artifacts may need fields that current helper would treat as optional | Yes | No |
| `scripts/vitruvius/graph/cli.py` + `graph/builder.py` | treat root `latest_*` aliases and ambient-clock fallbacks as anti-patterns for AEC; reuse only dataset-scoped immutable artifact richness | current root graph build is not AEC-grade replay identity | Yes | Yes for any artifact reuse |
| `scripts/vitruvius/graph/dataset_manifest.py` | reuse or clone its manifest/pilot-gate pattern for AEC fixture pilots | prevents ad hoc pilot artifact sprawl | Recommended | No |
| `scripts/vitruvius/spatial/_feature_gate.py` | do **not** reuse directly for AEC; create neutral or AEC-local helper if needed | avoids hidden cross-package coupling to an internal spatial helper | Recommended | No |
| `scripts/vitruvius/review/ontology_prompt_builder.py` + `query/nl_translator.py` | explicitly exclude from AEC truth, verifier, and vault flows | current heuristic/prose-rich LLM paths are not safe truth precedents | Recommended | No |
| repo baseline | begin AEC work only from a clean branch | current dirty tree is a real blast-radius defect | Yes | Yes |

## 15. Ordered Preparation Plan

### Phase 0 — Baseline honesty
1. start from a clean baseline
2. accept the relevant AEC plan set or keep work strictly planning-only
3. choose one bounded AEC slice, not the whole program

**Exit gate:** clean branch + accepted planning slice.

### Phase 1 — Audit/snapshot envelope + namespace freeze
1. freeze the audit/snapshot envelope (`snapshot_id`, actor, subsystem, status, input/output artifact refs, declared clock source)
2. freeze `scripts/vitruvius/aec/` as the only AEC Python root
3. freeze Rust extension points to existing `engine_rs` members
4. freeze TypeScript to boundary-only ownership
5. decide whether AEC integrates with existing graph contracts or keeps separate AEC contracts

**Exit gate:** no subsystem plan still depends on an unfrozen root, ownership assumption, or audit envelope.

### Phase 2 — Contract freeze
1. freeze DTOs, IDs, schema versions
2. freeze `frame_id`, units, and tolerance policy
3. freeze replay ids, clocks, and refusal taxonomy
4. freeze candidate/canonical distinction for rule-bearing artifacts

**Exit gate:** no AEC subsystem still depends on undefined DTO, frame, unit, tolerance, or id semantics.

### Phase 3 — Boundary translation v2 and parity
1. upgrade Python and TS contracts together
2. create valid/corrupt/truncated/wrong-version/wrong-frame/wrong-unit/missing-tolerance fixture families
3. make AEC import strict-footer only
4. version IFC mappings instead of inflating the current toy registry in place

**Exit gate:** Python↔TS parity is explicit and tested.

### Phase 4 — Vault foundation
1. freeze rule AST schema and vault payload structure
2. freeze candidate/canonical separation
3. freeze backend layout and projection/output roots
4. define replay and temporal query requirements

**Exit gate:** machine rule truth is structured and replayable.

### Phase 5 — Python reference ECS
1. implement Python world/snapshot model
2. freeze component families
3. add replay and deterministic schedule tests

**Do not do:** Rust ECS yet.

### Phase 6 — Python reference spatial service
1. implement clash/clearance/occupancy/routing reference path
2. add fixtures and pre-port benchmarks
3. only then identify hot kernels for Rust candidates

### Phase 7 — Bounded verification
1. implement AST whitelist
2. add witness/unsat/timeout artifact contracts
3. add explicit refusals for unsupported rule families and oversize queries

### Phase 8 — Coordination
1. freeze discipline enum and precedence manifest
2. implement deterministic issue ordering and escalation states
3. add oscillation/cascade tests

### Phase 9 — Pricing
1. freeze quantity contract
2. freeze pricebook snapshot identity, currency, and freshness policy
3. add missing/stale-price refusal behavior

### Phase 10 — Optimization
1. freeze deterministic objective vectors and dominance rules
2. implement frontier first
3. only later add seeded search with replay metadata

### Phase 11 — Tooling last
1. add tool catalog only after deterministic artifacts exist
2. bind tool outputs to replayable artifacts
3. refuse unsupported or authority-violating requests explicitly

## 16. Risk Register

| Risk | Severity | Likelihood | Affected surfaces | Containment |
|---|---|---|---|---|
| namespace sprawl into generic packages | Critical | High | `spatial/*`, `graph/*`, `compound/*`, `geometric/*`, `query/*` | enforce `scripts/vitruvius/aec/` root |
| undefined frame/unit/tolerance contract | Critical | High | boundary, spatial, verifier, pricing | freeze before coding |
| candidate/canonical mixing | Critical | High | future AEC vault, verifier, pricing, optimization | implement separation first |
| TypeScript becomes second orchestration plane | High | Medium | `spatial-daemon/*` | strict boundary-only rule |
| marker-only or orphaned control flags proliferate | Medium | Medium | `config/vitruvius.yaml`, bootstrap tests | no AEC flag may exist without a real enforcement path and tests |
| Rust-first ECS or verifier | Critical | Medium | `engine_rs/*`, future AEC runtime | Python reference first |
| Z3 over raw prose or heavy geometry | Critical | Medium | verifier | whitelist ASTs and precompute geometry outside solver |
| Python↔TS schema/footer drift | Critical | High | current spatial boundary | atomic parity changes + shared fixtures |
| benchmark-free Rust migration | Critical | Medium | future kernels | require benchmark + parity + fallback |
| fixture drift mistaken for hardened contract | High | High | sample spatial fixtures, tests | distinguish legacy compatibility from AEC baseline |
| pricebook/provenance ambiguity | High | Medium | pricing, optimization | freeze schema/freshness/currency/refusal policy |
| stale comments/docs used as authority | Medium | High | event store comments, old fixtures, historical roadmap claims | verify runtime code paths, not comments |
| dirty baseline contaminates AEC diffs | High | High | repo-wide | clean branch required |
| root `latest_*` artifacts used as truth or replay anchors | Critical | Medium | `005_Operational-Intelligence-Layer/graph/latest_*`, review run artifacts | require immutable dataset/run-scoped artifacts instead |

## 17. Stop Conditions

Stop immediately if any of the following are true:

1. AEC implementation starts before the namespace and ownership decision is frozen.
2. AEC implementation starts from the current dirty working tree.
3. DTOs or IDs are still changing while multiple subsystems begin coding.
4. `frame_id`, unit system, or tolerance policy are undefined.
5. boundary v2 is changed on one side only (Python or TypeScript).
6. `parse_contract`-style legacy compatibility is being used as the authoritative AEC import path.
7. rule AST / candidate-canonical distinction is still undefined but vault or verifier work starts.
8. raw prose or free-form LLM text is entering the verifier or runtime truth path.
9. TypeScript begins owning coordination, verification, pricing, optimization, or authoritative spatial reasoning.
10. Rust begins owning legal meaning, provenance logic, pricing policy, or tool routing.
11. optimization starts before verified-candidate artifacts and replay guarantees exist.
12. pricing starts before quantity/currency/freshness contracts exist.
13. any proposed Rust port lacks a benchmark baseline, parity harness, and fallback story.
14. any implementation plan relies on the presence of `bevy_ecs`, voxel grids, heightmap storage, or an AEC vault as if they already exist in the repo.
15. any AEC state or snapshot identity is derived from filesystem mtime or ambient wall clock.
16. any truth-bearing AEC store permits overwrite or purge semantics modeled after the mutable review caches.
17. any AEC flow uses root `latest_*` artifacts as authoritative inputs.
18. any AEC LLM flow receives raw vault payloads, raw rule text, or raw candidate state instead of bounded summaries or artifact refs.

## 18. Acceptance Criteria For “AEC Engine Ready”

The repo is safe to begin AEC implementation only when **all** of the following are true:

- [ ] clean branch baseline exists
- [ ] relevant AEC plans are accepted, not merely proposed
- [ ] `scripts/vitruvius/aec/` is created as the sole AEC code root
- [ ] AEC audit/snapshot envelope (`snapshot_id`, actor, subsystem, status taxonomy, input/output artifact refs, declared clock source) is frozen
- [ ] AEC DTO family, IDs, and versioning policy are frozen
- [ ] `frame_id`, payload-level units, and tolerance policy are frozen
- [ ] AEC boundary v2 parity tests exist for Python↔TypeScript
- [ ] one end-to-end TS-emitted contract lane passes through Python reader + footer verification + schema validation + walker ingest + mapper
- [ ] AEC import path requires integrity footer validation
- [ ] AEC rule AST schema and candidate/canonical separation are frozen
- [ ] AEC replay ids, clocks, and artifact envelopes are frozen
- [ ] AEC artifact roots under `005_Operational-Intelligence-Layer/aec/` and `006_System-Manifests/cache/` are created intentionally
- [ ] no marker-only/orphaned AEC control flags exist
- [ ] Python reference ECS replay tests pass
- [ ] Python reference spatial service fixtures and benchmarks exist
- [ ] Z3 whitelist, refusal behavior, witness artifacts, and timeout policy are implemented and tested
- [ ] coordination precedence and escalation states are frozen
- [ ] quantity contract, pricebook schema, currency policy, and freshness policy are frozen
- [ ] optimization objective vector and reproducibility metadata are frozen
- [ ] tool catalog, refusal taxonomy, and authority fence are frozen
- [ ] benchmark budgets exist for every planned hot path

Until those are true, the honest answer remains: **do not implement the AEC engine yet**.

## 19. Appendix

### 19.1 Commands run
- read governing docs, AEC plan family, AEC/GOV/RUST specs, and AEC research
- enumerated repo trees for `scripts/vitruvius/`, `engine_rs/`, `spatial-daemon/`, `005_...`, `006_...`, and `001B_Spatial-Source-Layer/`
- inspected key Python, Rust, and TypeScript files with `sed`, `rg`, and small AST summaries
- executed targeted validation:
  - `python3 -m pytest ... -q`
  - `cargo test --workspace --quiet`
  - `npm test`
  - `npm run typecheck`
- reviewed `git status --short` for baseline hygiene

### 19.2 Key files inspected directly
- `scripts/pipeline_cli.py`
- `scripts/vitruvius/features.py`
- `scripts/vitruvius/config.py`
- `scripts/vitruvius/cli_experience.py`
- `scripts/vitruvius/graph/contract.py`
- `scripts/vitruvius/graph/snapshot.py`
- `scripts/vitruvius/graph/dataset_manifest.py`
- `scripts/vitruvius/graph/cli.py`
- `scripts/vitruvius/graph/builder.py`
- `scripts/vitruvius/graph/event_store.py`
- `scripts/vitruvius/graph/rocksdb_event_store.py`
- `scripts/vitruvius/graph/temporal_query.py`
- `scripts/vitruvius/review/stateful_registry.py`
- `scripts/vitruvius/review/rocksdb_stateful_registry.py`
- `scripts/vitruvius/review/cot_audit.py`
- `scripts/vitruvius/review/tension_analyzer.py`
- `scripts/vitruvius/review/ontology_prompt_builder.py`
- `scripts/vitruvius/kv_migrate.py`
- `scripts/vitruvius/promotion_validator.py`
- `scripts/vitruvius/spatial/schema.py`
- `scripts/vitruvius/spatial/contract_reader.py`
- `scripts/vitruvius/spatial/walker.py`
- `scripts/vitruvius/spatial/concept_mapper.py`
- `scripts/vitruvius/spatial/spatial_edge_builder.py`
- `scripts/vitruvius/spatial/proximity_jump.py`
- `scripts/vitruvius/spatial/constraint_solver.py`
- `scripts/vitruvius/spatial/cli.py`
- `scripts/vitruvius/spatial/_feature_gate.py`
- `scripts/vitruvius/ontology/ifc_registry.py`
- `scripts/vitruvius/ontology/ifc_mapping.yaml`
- `scripts/vitruvius/ontology/owl_exporter.py`
- `scripts/vitruvius/geometric/inequality_compiler.py`
- `scripts/vitruvius/geometric/pareto_optimizer.py`
- `scripts/vitruvius/compound/dependency_tracker.py`
- `scripts/vitruvius/compound/differential_propagator.py`
- `scripts/vitruvius/compound/adversarial.py`
- `scripts/vitruvius/compound/dspy_compiler.py`
- `scripts/vitruvius/query/result.py`
- `scripts/vitruvius/query/engine.py`
- `scripts/vitruvius/query/graphrag_router.py`
- `scripts/vitruvius/query/nl_translator.py`
- `scripts/vitruvius/normalization/outlier_detector.py`
- `scripts/vitruvius/engine_rs/__init__.py`
- `scripts/vitruvius/engine_rs/Cargo.toml`
- `scripts/vitruvius/engine_rs/core/src/lib.rs`
- `scripts/vitruvius/engine_rs/core/src/octree.rs`
- `scripts/vitruvius/engine_rs/pyo3_shim/src/lib.rs`
- `scripts/vitruvius/engine_rs/spatial_kernels/src/*`
- `scripts/vitruvius/engine_rs/stats_kernels/src/mahalanobis.rs`
- `spatial-daemon/package.json`
- `spatial-daemon/README.md`
- `spatial-daemon/src/types.ts`
- `spatial-daemon/src/contract_writer.ts`
- `spatial-daemon/src/cli.ts`
- `spatial-daemon/src/aabb.ts`
- `spatial-daemon/src/gjk.ts`
- `scripts/tests/fixtures/spatial/sample_residential_01_spatial.json`
- `001B_Spatial-Source-Layer/README.md`
- `006_System-Manifests/registries/graph_registry.csv`
- `006_System-Manifests/runs/latest_relationship_review_high_confidence.json`
- `006_System-Manifests/runs/latest_relationship_review_merged.json`
- `006_System-Manifests/runs/latest_promotion_audit.log`

### 19.3 Executed test evidence
- targeted pytest lane: **117 passed**
- `cargo test --workspace --quiet`: **passed** (observed 26 executed tests in local output)
- `npm test`: **21/21 passed**
- `npm run typecheck`: passed

### 19.4 Unresolved uncertainties
- whether AEC artifacts should integrate with existing graph contracts or remain separate
- whether Rust ECS will ever be justified, or whether Python-first ECS will remain sufficient longer than the specs assume
- whether AEC boundary v2 extends the current spatial contract or becomes a separate AEC-specific contract family
- whether the future AEC vault should be a specialized reuse of current RocksDB patterns or a more distinct surface

### 19.5 Assumptions that still need confirmation before implementation
1. AEC work will start from a clean branch.
2. `scripts/vitruvius/aec/` remains the accepted root.
3. TypeScript remains boundary-only.
4. Rust remains compute-only.
5. frame/unit/tolerance policy will be frozen before spatial or verifier coding.
6. optimization remains downstream of verification.
7. tools remain downstream of deterministic artifacts.

### 19.6 Tooling limitation during this audit
Repo guidance prefers code-review-graph / GitNexus first. Those graph tools were not available in this session, so this audit used direct file inspection, ripgrep, AST summaries, and targeted validation runs instead.
