---
task: aec-engine-master-execution-task-list
phase: 00
created: 2026-04-16
author: PLANNER
supersedes: null
status: ACCEPTED
---

# AEC Engine Master Execution Task List

## 1. Title and Metadata

- **Title:** AEC Engine Master Execution Task List
- **Artifact type:** execution-driving task system / staged implementation-preparation package
- **Date:** 2026-04-16
- **Status:** review-ready, pre-implementation, implementation-driving
- **Scope:** translate the strengthened AEC audit and AEC plan family into a safe staged task system
- **Non-goal:** this artifact by itself is not the execution trigger; coding authority comes from the accepted bounded-slice sprint plan plus the fresh implementation trigger
- **Canonical task layer location:** `.ai/04_tasks/`

## 2. Source Inputs Used

### Governing inputs
- `AGENTS.md`
- `.ai/00_system/EXECUTION_LOOP.md`
- `.ai/00_system/principles.md`
- `.ai/01_roadmap/master-roadmap.md`
- `.ai/01_roadmap/current-phase.md`
- `.ai/01_roadmap/milestone-tracker.md`
- `.ai/03_plans/00-governing-implementation-plan.md`

### AEC planning inputs
- `.ai/03_plans/AEC_ENGINE_MASTER_IMPLEMENTATION_PLAN.md`
- `.ai/03_plans/AEC_ENGINE_BOUNDARY_TRANSLATION_IMPLEMENTATION_PLAN.md`
- `.ai/03_plans/AEC_ENGINE_ECS_CORE_IMPLEMENTATION_PLAN.md`
- `.ai/03_plans/AEC_ENGINE_SPATIAL_KERNEL_IMPLEMENTATION_PLAN.md`
- `.ai/03_plans/AEC_ENGINE_KNOWLEDGE_VAULT_IMPLEMENTATION_PLAN.md`
- `.ai/03_plans/AEC_ENGINE_Z3_VERIFICATION_IMPLEMENTATION_PLAN.md`
- `.ai/03_plans/AEC_ENGINE_MULTI_DISCIPLINARY_COORDINATION_IMPLEMENTATION_PLAN.md`
- `.ai/03_plans/AEC_ENGINE_FINANCIAL_PRICING_ORACLE_IMPLEMENTATION_PLAN.md`
- `.ai/03_plans/AEC_ENGINE_OPTIMIZATION_ENGINE_IMPLEMENTATION_PLAN.md`
- `.ai/03_plans/AEC_ENGINE_LLM_TOOL_CALLING_IMPLEMENTATION_PLAN.md`

### Audit inputs
- `.ai/02_audits/AEC_ENGINE_WHOLE_CODEBASE_READINESS_AUDIT_2026-04-16.md`
- `.ai/02_audits/AEC_ENGINE_PLAN_CRITIQUE_2026-04-15.md`
- `.ai/02_audits/AEC_ENGINE_RESEARCH_TO_PLAN_AUDIT_2026-04-15.md`
- `.ai/02_audits/APP_INTEGRITY_RELIABILITY_AUDIT_2026-04-16.md`

## 2A. Supporting Control Artifacts

- `.ai/04_tasks/aec-engine-control-artifacts-README-2026-04-16.md` — package index / navigation guide for the AEC control set
- `.ai/04_tasks/aec-engine-traceability-matrix-2026-04-16.md` — finding→task→test→stop-condition trace map
- `.ai/04_tasks/aec-engine-subsystem-gates-2026-04-16.md` — subsystem entry/exit gates and no-go states
- `.ai/03_plans/templates/aec-engine-first-sprint-template.md` — reusable first bounded implementation sprint scaffold
- `.ai/04_tasks/aec-engine-file-touch-matrix-2026-04-16.md` — file/path touch policy by surface
- `.ai/04_tasks/aec-engine-gates.schema.json` + `.ai/04_tasks/aec-engine-gates-spec-2026-04-16.md` + `.ai/04_tasks/aec-engine-gates-state-2026-04-16.json` — machine-readable gate schema, companion spec, and live gate-state instance
- `.ai/04_tasks/aec-engine-language-boundary-blacklists-2026-04-16.md` — explicit Rust/TypeScript ownership blacklists and exception rules
- `.ai/04_tasks/aec-engine-bounded-implementation-planning-trigger.md` — next SEL trigger for bounded implementation planning using this package

## 3. Execution Doctrine Summary

This task system is governed by five non-negotiable doctrines:

1. **Contracts before code.** No subsystem implementation begins before namespace, DTO, ID, frame, unit, tolerance, replay-envelope, and candidate/canonical contracts are frozen.
2. **Python reference before Rust acceleration.** Rust is allowed only for isolated numeric kernels after a Python reference path, parity harness, and benchmark evidence exist.
3. **TypeScript stays boundary-only.** `spatial-daemon/` may evolve for schema/footer parity but must not become an AEC orchestration, pricing, verification, or coordination plane.
4. **Replay and truth before optimization.** Optimization, tool-calling, and user-facing orchestration remain downstream of verified deterministic artifacts.
5. **Mutable caches are not truth.** Existing SQLite/RocksDB registry patterns are useful cache precedents only. Canonical AEC truth must not inherit overwrite/purge semantics.

## 4. Global Blockers and Prerequisite Freezes

These are global blockers. No AEC production implementation task may begin until all blocker-class tasks below are done.

### B0 — Current global blockers
- no `scripts/vitruvius/aec/` code root exists
- no AEC DTO family exists
- no AEC rule AST/vault contract exists
- no AEC world/snapshot/replay envelope exists
- no `frame_id` / payload-level units / tolerance policy exists
- no AEC feature-flag surface exists
- no `scripts/tests/test_aec_*` suites exist
- current repo working tree is dirty and cannot be trusted as a clean implementation baseline

### B1 — Required freeze set
The following must be explicitly frozen before implementation starts:
- AEC namespace and ownership map
- audit/snapshot envelope (`snapshot_id`, actor, subsystem, status taxonomy, input/output artifact refs, declared clock source)
- DTO family and versioning policy
- ID family and artifact identity policy
- `frame_id`, unit system, and tolerance policy
- candidate/canonical truth separation
- rule AST and vault payload contracts
- quantity/pricebook/currency/freshness contracts
- objective vector and reproducibility metadata
- tool authority fence and refusal taxonomy

## 5. Phase-by-Phase Task Map

| Phase | Goal | Output class |
|---|---|---|
| Phase A | Contract and boundary freeze | blocker / contract-freeze |
| Phase B | Repo preparation and refactor blockers | refactor / implementation-prep |
| Phase C | Validation and benchmark harness groundwork | benchmark / parity / validation |
| Phase D | Subsystem foundations | implementation-prep / foundation |
| Phase E | First bounded implementation slice prep | implementation-ready prep |
| Phase F | Cross-language parity hardening | parity / hardening |
| Phase G | Readiness gate for actual implementation sprinting | gate / go-no-go |

## 6. Task Table / Task Cards

> **Legend for task type:**
> - `BLOCKER`
> - `CONTRACT-FREEZE`
> - `REFACTOR`
> - `BENCHMARK`
> - `PARITY`
> - `IMPLEMENTATION-PREP`
> - `IMPLEMENTATION-READY`

---

### Phase A — Contract and Boundary Freeze

#### Task AEC-T001
- **Type:** BLOCKER
- **Title:** Freeze AEC namespace and ownership map
- **Purpose:** make it impossible for AEC work to sprawl across generic packages by convenience
- **Why it exists:** the audit shows the repo already has strong precedents in `spatial/*`, `graph/*`, `compound/*`, `geometric/*`, and `query/*`; without a hard namespace freeze, AEC work will leak into them
- **Dependencies:** none
- **Inputs:** strengthened audit §§4, 7, 8, 13, 14; AEC master plan §3
- **Expected outputs:** accepted namespace decision centered on `scripts/vitruvius/aec/`; explicit ownership map for Python / Rust / TypeScript surfaces
- **Files likely touched:**
  - `.ai/03_plans/AEC_ENGINE_MASTER_IMPLEMENTATION_PLAN.md`
  - `.ai/03_plans/00-governing-implementation-plan.md` (only if execution order wording needs truth alignment)
  - future trigger or plan artifacts in `.ai/04_tasks/` and `.ai/03_plans/`
- **Tests required:** none yet; governance artifact validation only
- **Validation gates:** no live plan or audit may still imply generic-package AEC sprawl after this task
- **Stop conditions:** if any proposal keeps AEC orchestration in `spatial/*`, `graph/*`, `compound/*`, or `query/*` by default, stop
- **Definition of done:** AEC root and ownership map are explicit, reviewable, and reused by all downstream tasks

#### Task AEC-T002
- **Type:** BLOCKER
- **Title:** Freeze audit/snapshot envelope contract
- **Purpose:** define the minimum replay-safe identity and audit fields that every future AEC artifact must carry
- **Why it exists:** the audit found current `latest_*` aliases, wall-clock run ids, and thin event/result envelopes are not sufficient precedents
- **Dependencies:** AEC-T001
- **Inputs:** strengthened audit §§12, 13, 17, 18; graph/cli and dataset-manifest precedents
- **Expected outputs:** frozen envelope fields, at minimum:
  - `snapshot_id`
  - `run_id`
  - `actor`
  - `subsystem`
  - `status`
  - `input_artifact_refs[]`
  - `output_artifact_refs[]`
  - declared clock source
- **Files likely touched:**
  - `.ai/03_plans/AEC_ENGINE_MASTER_IMPLEMENTATION_PLAN.md`
  - future AEC contract docs/plans
- **Tests required:** contract checklist only at this stage
- **Validation gates:** no subsystem plan may still describe replay or audit artifacts without these fields
- **Stop conditions:** if any AEC artifact identity is allowed to derive from filesystem mtime or ambient wall clock, stop
- **Definition of done:** envelope is frozen and referenced by every downstream subsystem task

#### Task AEC-T003
- **Type:** CONTRACT-FREEZE
- **Title:** Freeze AEC DTO / ID / versioning contract family
- **Purpose:** define the canonical AEC DTO family and stable IDs before any subsystem coding starts
- **Why it exists:** the audit shows there is currently no AEC DTO family, no ID policy, and no artifact versioning policy
- **Dependencies:** AEC-T001, AEC-T002
- **Inputs:** strengthened audit §§4, 8, 13, 14, 18; AEC boundary, ECS, spatial, vault, and tools plans
- **Expected outputs:**
  - stable AEC DTO family
  - versioning policy
  - ID family for world revisions, snapshots, rule ASTs, pricebooks, runs, artifacts
- **Files likely touched:**
  - `.ai/03_plans/AEC_ENGINE_MASTER_IMPLEMENTATION_PLAN.md`
  - relevant AEC subsystem plans
- **Tests required:** none yet, but future tasks must reference exact DTO ids and versions from this freeze
- **Validation gates:** no downstream task may still contain “TBD” for DTO ids/versions
- **Stop conditions:** if graph contract prefix/status vocab is silently reused without explicit acceptance or separation decision, stop
- **Definition of done:** DTO and ID language is stable enough that task cards can name expected artifacts concretely

#### Task AEC-T004
- **Type:** CONTRACT-FREEZE
- **Title:** Freeze frame / unit / tolerance policy
- **Purpose:** eliminate the single most dangerous ambiguity before spatial or verification work starts
- **Why it exists:** current spatial boundary v1 has no `frame_id`, no payload-level units, and no tolerance manifest
- **Dependencies:** AEC-T003
- **Inputs:** strengthened audit §§4, 9, 13, 14, 17, 18; AEC spatial and boundary plans
- **Expected outputs:** explicit policy for:
  - `frame_id`
  - payload-level `unit_system`
  - operation-class tolerance policy
  - rounding/precision rules
- **Files likely touched:**
  - `.ai/03_plans/AEC_ENGINE_SPATIAL_KERNEL_IMPLEMENTATION_PLAN.md`
  - `.ai/03_plans/AEC_ENGINE_BOUNDARY_TRANSLATION_IMPLEMENTATION_PLAN.md`
- **Tests required:** future boundary-v2 parity and invalid-state fixtures must derive from this freeze
- **Validation gates:** no spatial or verifier task may proceed without referencing this policy
- **Stop conditions:** if units or tolerances are left implicit in TypeScript, Python, or Rust, stop
- **Definition of done:** every downstream spatial/verifier/pricing task can name frame, unit, and tolerance expectations concretely

#### Task AEC-T005
- **Type:** CONTRACT-FREEZE
- **Title:** Freeze candidate/canonical truth separation and rule AST admission model
- **Purpose:** prevent the AEC vault from becoming a mutable or prose-bearing truth sink
- **Why it exists:** the audit found strong promotion mindset but no AEC rule-vault implementation, and current cache precedents are mutable by design
- **Dependencies:** AEC-T002, AEC-T003
- **Inputs:** strengthened audit §§4, 12, 13, 17, 18; AEC vault and Z3 plans
- **Expected outputs:**
  - candidate vs canonical artifact split
  - AST admission/write contract
  - promotion gate expectations
  - explicit non-governance of mutable caches
- **Files likely touched:**
  - `.ai/03_plans/AEC_ENGINE_KNOWLEDGE_VAULT_IMPLEMENTATION_PLAN.md`
  - `.ai/03_plans/AEC_ENGINE_Z3_VERIFICATION_IMPLEMENTATION_PLAN.md`
- **Tests required:** future candidate/canonical vault fixtures and backend-parity tests
- **Validation gates:** no downstream verifier, pricing, optimization, or tools task may read candidate data as canonical truth
- **Stop conditions:** if any proposal allows overwrite or purge semantics for canonical AEC truth, stop
- **Definition of done:** truth-bearing vs non-truth-bearing stores are structurally distinct in the task system

---

### Phase B — Repo Preparation and Refactor Blockers

#### Task AEC-T006
- **Type:** BLOCKER
- **Title:** Establish clean implementation baseline branch and scope boundary
- **Purpose:** ensure future AEC work does not mix with unrelated modified/untracked files
- **Why it exists:** the audit explicitly identifies the current dirty working tree as a real blast-radius defect
- **Dependencies:** none
- **Inputs:** strengthened audit §§8, 17, 18
- **Expected outputs:** clean baseline branch + explicit statement of what pre-existing work is excluded from AEC scope
- **Files likely touched:** none required for the artifact itself beyond future trigger/state docs
- **Tests required:** `git status --short` must be clean for the AEC scope branch
- **Validation gates:** no AEC execution trigger may be accepted while baseline is dirty
- **Stop conditions:** if clean baseline cannot be established, stop the implementation-prep lane
- **Definition of done:** clean branch exists and is named as the only allowed baseline for AEC work

#### Task AEC-T007
- **Type:** REFACTOR
- **Title:** Separate strict AEC boundary import path from legacy spatial compatibility path
- **Purpose:** preserve legacy fixtures while preventing no-footer / weak-schema behavior from leaking into AEC imports
- **Why it exists:** current `parse_contract(... require_footer=False)` and `walker.py` behavior are acceptable for legacy compatibility but unsafe for AEC truth-bearing imports
- **Dependencies:** AEC-T003, AEC-T004
- **Inputs:** strengthened audit §§4, 8, 9, 14
- **Expected outputs:** explicit design decision for:
  - strict AEC import lane
  - legacy compatibility lane
  - when/whether 001B is reused vs new landing zone introduced
- **Files likely touched:**
  - `scripts/vitruvius/spatial/contract_reader.py`
  - `scripts/vitruvius/spatial/walker.py`
  - `scripts/vitruvius/spatial/cli.py`
  - `001B_Spatial-Source-Layer/README.md`
- **Tests required:** future end-to-end TS→Python strict import lane; invalid legacy/quarantine behavior tests
- **Validation gates:** no AEC import task may still rely on default legacy-no-footer mode
- **Stop conditions:** if AEC import path still silently accepts weak or provenance-losing inputs, stop
- **Definition of done:** strict AEC import behavior is defined and legacy compatibility is explicitly quarantined

#### Task AEC-T008
- **Type:** REFACTOR
- **Title:** Decide graph-contract reuse vs separate AEC contract family
- **Purpose:** prevent silent overloading of current graph ids, node types, evidence ids, and status vocabulary
- **Why it exists:** current graph contract only supports `source|concept|attribute|spatial_instance`, closed edge statuses, and `rel-` evidence ids
- **Dependencies:** AEC-T003
- **Inputs:** strengthened audit §§6, 8, 12, 14
- **Expected outputs:** either:
  - explicit extension plan for current graph contracts, or
  - explicit declaration that AEC contracts remain separate
- **Files likely touched:**
  - `scripts/vitruvius/graph/contract.py`
  - `.ai/03_plans/AEC_ENGINE_MASTER_IMPLEMENTATION_PLAN.md`
- **Tests required:** future contract tests for whichever direction is chosen
- **Validation gates:** no downstream AEC task may assume current graph contract is reusable as-is
- **Stop conditions:** if current graph status vocabulary is reused without widening or separation, stop
- **Definition of done:** contract-family relationship is explicit and referenced by downstream tasks

---

### Phase C — Validation and Benchmark Harness Groundwork

#### Task AEC-T009
- **Type:** BENCHMARK
- **Title:** Create AEC benchmark doctrine and harness specification
- **Purpose:** prevent benchmark-free Rust migration and benchmark theater
- **Why it exists:** current repo benchmark harnesses are useful precedents but are not AEC evidence
- **Dependencies:** AEC-T002, AEC-T003, AEC-T004
- **Inputs:** strengthened audit §§10, 11; performance and Rust validation specs
- **Expected outputs:** one agreed benchmark harness spec covering:
  - fixture-defined workloads
  - wall time + peak RSS
  - hardware context
  - flag-off baseline vs flag-on path
  - acceptance thresholds
- **Files likely touched:**
  - future benchmark plan/task artifacts
  - `.ai/00_performance/2026-04-16_aec-first-slice-benchmark-hotspot-matrix.md`
  - possibly additional `.ai/00_performance/` benchmark notes
- **Tests required:** none yet; this task defines benchmark expectations
- **Validation gates:** no Rust candidate task may exist without referencing this harness spec
- **Stop conditions:** if any Rust task attempts to port code before benchmark harness spec is frozen, stop
- **Definition of done:** every future Rust-related task can cite benchmark protocol and thresholds concretely

#### Task AEC-T010
- **Type:** PARITY
- **Title:** Define required AEC parity harness matrix
- **Purpose:** ensure every future cross-language or accelerated seam has a planned parity lane before coding starts
- **Why it exists:** the audit found parity proof is currently narrow and siloed
- **Dependencies:** AEC-T003, AEC-T004, AEC-T005, AEC-T009
- **Inputs:** strengthened audit §§9, 10, 11
- **Expected outputs:** required parity suite list including:
  - `test_aec_boundary_contract_parity.py`
  - `test_aec_vault_backend_parity.py`
  - `test_aec_ecs_replay.py`
  - `test_aec_spatial_parity.py`
  - `test_aec_z3_replay.py`
  - `test_aec_coordination_replay.py`
  - `test_aec_pricing_refusals.py`
  - `test_aec_optimization_replay.py`
  - `test_aec_tools_refusals.py`
- **Files likely touched:** planning/task artifacts only at this stage
- **Tests required:** none yet; task defines them
- **Validation gates:** no subsystem-foundation task may omit its parity lane if it crosses a seam
- **Stop conditions:** if a planned seam lacks a named parity test family, stop
- **Definition of done:** parity matrix exists and is referenced by all downstream subsystem tasks

#### Task AEC-T010A
- **Type:** PARITY
- **Title:** Define backend-factory parity task for SQLite/RocksDB duality
- **Purpose:** make backend duality an explicit tested seam wherever AEC mutable caches or non-canonical stores may support both SQLite and RocksDB
- **Why it exists:** the audit found current repo parity is real for caches and event stores, but dangerous if future AEC truth stores inherit mutable semantics by analogy
- **Dependencies:** AEC-T005, AEC-T009, AEC-T010
- **Inputs:** strengthened audit §§11, 12; existing `graph/event_store.py`, `graph/rocksdb_event_store.py`, `review/stateful_registry.py`, `review/rocksdb_stateful_registry.py`, `kv_migrate.py`
- **Expected outputs:** explicit backend-factory parity task package covering:
  - where dual-backend support is allowed
  - where dual-backend support is forbidden
  - required parity tests and migration tests
  - explicit statement that canonical truth must not inherit overwrite/purge cache semantics
- **Files likely touched:**
  - future AEC vault/store plans
  - future `scripts/tests/test_aec_vault_backend_parity.py`
  - future backend factory surfaces under `scripts/vitruvius/aec/vault/*`
- **Tests required:** backend parity suite + migration/idempotency suite + read/write behavior comparison on bounded fixtures
- **Validation gates:** no AEC backend duality claim may exist without parity and migration coverage
- **Stop conditions:** if canonical AEC truth is proposed on a mutable cache-style backend abstraction without separate law/contract, stop
- **Definition of done:** backend duality rules are explicit and test-driven before any AEC backend implementation starts

#### Task AEC-T011
- **Type:** IMPLEMENTATION-PREP
- **Title:** Define AEC fixture families and replay corpus
- **Purpose:** create the fixture vocabulary future tasks must use
- **Why it exists:** the audit identified missing valid/invalid boundary fixtures, ECS snapshots, AST fixtures, sat/unsat fixtures, coordination cascades, pricing snapshots, and frontier fixtures
- **Dependencies:** AEC-T002, AEC-T003, AEC-T004, AEC-T005, AEC-T010
- **Inputs:** strengthened audit §§11, 12, 18
- **Expected outputs:** fixture-family matrix with ownership, purpose, and downstream consumers
- **Files likely touched:** planning/task artifacts; future fixture directories under `scripts/tests/fixtures/` or equivalent
- **Tests required:** none yet; task defines future fixture work
- **Validation gates:** no subsystem foundation may start without its fixture family defined
- **Stop conditions:** if replay tests are planned without fixture families, stop
- **Definition of done:** fixture families are named, bounded, and mapped to subsystem tasks

---

### Phase D — Subsystem Foundations

#### Task AEC-T012
- **Type:** IMPLEMENTATION-PREP
- **Title:** Boundary v2 foundation task
- **Purpose:** prepare the AEC boundary layer without implementing business logic yet
- **Why it exists:** every other subsystem depends on stable import/export DTOs, ids, frames, units, and strict parity
- **Dependencies:** AEC-T001 to AEC-T011
- **Inputs:** boundary plan + strengthened audit boundary sections
- **Expected outputs:**
  - executable task-ready boundary freeze package
  - strict-vs-legacy import lane decision
  - parity and fixture mapping
- **Files likely touched:**
  - `scripts/vitruvius/spatial/schema.py`
  - `scripts/vitruvius/spatial/contract_reader.py`
  - `scripts/vitruvius/spatial/walker.py`
  - `spatial-daemon/src/types.ts`
  - `spatial-daemon/src/contract_writer.ts`
  - `spatial-daemon/src/cli.ts`
- **Tests required:** future `test_aec_boundary_*` + end-to-end TS→Python lane
- **Validation gates:** no AEC import path drops provenance or accepts weak inputs silently
- **Stop conditions:** if TypeScript is asked to own AEC orchestration, pricing, verifier, or coordination semantics, stop
- **Definition of done:** boundary subsystem has a safe implementation-prep package with exact files, fixtures, and gates

#### Task AEC-T013
- **Type:** IMPLEMENTATION-PREP
- **Title:** Knowledge vault foundation task
- **Purpose:** prepare the AEC vault as structured admitted machine truth rather than “graph store but more”
- **Why it exists:** verifier, pricing, optimization, and tools all depend on rule-bearing truth with candidate/canonical separation
- **Dependencies:** AEC-T002, AEC-T003, AEC-T005, AEC-T010, AEC-T011
- **Inputs:** vault plan + strengthened audit truth/replay sections
- **Expected outputs:**
  - task-ready vault schema package
  - store/backend strategy
  - candidate/canonical promotion flow
  - replay and artifact-envelope requirements
- **Files likely touched:**
  - planned future `scripts/vitruvius/aec/vault/*`
  - `006_System-Manifests/cache/`
  - `005_Operational-Intelligence-Layer/aec/`
- **Tests required:** future `test_aec_vault_*` including backend parity
- **Validation gates:** no mutable cache semantics leak into canonical truth
- **Stop conditions:** if overwrite/purge semantics are proposed for canonical storage, stop
- **Definition of done:** vault foundation package is safe enough to drive a later implementation plan

#### Task AEC-T014
- **Type:** IMPLEMENTATION-PREP
- **Title:** Python reference ECS foundation task
- **Purpose:** define the Python-first world/snapshot/schedule substrate before any Rust ECS acceleration is discussed
- **Why it exists:** the specs are Rust-heavy, but the repo has no live ECS crate or replay fixtures yet
- **Dependencies:** AEC-T002, AEC-T003, AEC-T004, AEC-T011
- **Inputs:** ECS plan + strengthened audit ECS/Rust sections
- **Expected outputs:**
  - Python reference ECS task package
  - component-family freeze
  - replay/schedule fixture plan
- **Files likely touched:**
  - planned future `scripts/vitruvius/aec/ecs/*`
- **Tests required:** future `test_aec_ecs_contract.py`, `test_aec_ecs_replay.py`, `test_aec_ecs_schedule.py`
- **Validation gates:** no Rust ECS work may start first
- **Stop conditions:** if `bevy_ecs` or a Rust ECS implementation is treated as assumed substrate, stop
- **Definition of done:** ECS foundation is explicitly Python-first and replay-driven

#### Task AEC-T015
- **Type:** IMPLEMENTATION-PREP
- **Title:** Spatial service foundation task
- **Purpose:** prepare the AEC spatial service as a Python reference path over frozen DTOs and policy contracts
- **Why it exists:** the repo has useful kernels and precedents, but not the AEC spatial service described in the plans/specs
- **Dependencies:** AEC-T004, AEC-T009, AEC-T010, AEC-T011, AEC-T014
- **Inputs:** spatial plan + strengthened audit spatial sections
- **Expected outputs:**
  - AEC spatial service task package
  - Python-reference-first kernel plan
  - identified legitimate later Rust candidates only
- **Files likely touched:**
  - planned future `scripts/vitruvius/aec/spatial/*`
  - existing `engine_rs/*` only as future extension points
- **Tests required:** future `test_aec_spatial_contracts.py`, `test_aec_spatial_parity.py`, `test_aec_spatial_routing.py`
- **Validation gates:** no Rust kernel task may exist without a Python reference counterpart and benchmark spec
- **Stop conditions:** if frames/units/tolerances are still not frozen, stop
- **Definition of done:** spatial subsystem is ready for later bounded implementation planning

#### Task AEC-T016
- **Type:** IMPLEMENTATION-PREP
- **Title:** Verification foundation task
- **Purpose:** prepare the bounded AEC verifier around AST whitelist, witness artifacts, timeout policy, and replay
- **Why it exists:** current Z3 precedent is scalar and narrow; AEC verifier needs explicit whitelist/refusal behavior
- **Dependencies:** AEC-T005, AEC-T011, AEC-T014, AEC-T015
- **Inputs:** Z3 plan + strengthened audit verifier/truth sections
- **Expected outputs:** verifier task package with whitelist, refusal taxonomy, artifact schemas, and replay plan
- **Files likely touched:**
  - planned future `scripts/vitruvius/aec/verification/*`
- **Tests required:** future `test_aec_z3_compiler.py`, `test_aec_z3_replay.py`, `test_aec_z3_refusals.py`, `test_aec_z3_artifacts.py`
- **Validation gates:** geometry-heavy search and raw prose are excluded by contract
- **Stop conditions:** if unsupported families are allowed as “mostly covered,” stop
- **Definition of done:** verifier foundation is bounded, explicit, and replayable on paper

#### Task AEC-T017
- **Type:** IMPLEMENTATION-PREP
- **Title:** Coordination foundation task
- **Purpose:** prepare deterministic precedence/escalation/replay rules for multi-disciplinary coordination
- **Why it exists:** current dependency-tracker and propagator are only algorithmic invalidation precedents, not replay-grade coordination substrate
- **Dependencies:** AEC-T014, AEC-T015, AEC-T016
- **Inputs:** coordination plan + strengthened audit coordination sections
- **Expected outputs:** task-ready coordination package with:
  - discipline enum
  - precedence manifest
  - issue model
  - replay log requirements
- **Files likely touched:**
  - planned future `scripts/vitruvius/aec/coordination/*`
- **Tests required:** future `test_aec_coordination_precedence.py`, `test_aec_coordination_replay.py`, `test_aec_coordination_escalation.py`, `test_aec_coordination_oscillation.py`
- **Validation gates:** no coordination task may proceed without persisted replay/audit log design
- **Stop conditions:** if coordination is allowed to replace verification or optimization, stop
- **Definition of done:** coordination is explicit, bounded, and sequencing-safe

#### Task AEC-T018
- **Type:** IMPLEMENTATION-PREP
- **Title:** Pricing and optimization foundation tasks
- **Purpose:** prepare downstream subsystems only after verified-candidate and quantity/provenance contracts exist
- **Why it exists:** pricing and optimization are the easiest places to over-accelerate for demos and the fastest way to corrupt architecture
- **Dependencies:** AEC-T011, AEC-T014, AEC-T015, AEC-T016, AEC-T017
- **Inputs:** pricing plan, optimization plan, strengthened audit downstream-policy sections
- **Expected outputs:**
  - pricing package with quantity contract, pricebook schema, currency/freshness policy, refusal behavior
  - optimization package with deterministic objective vector, reproducibility metadata, and frontier-first discipline
- **Files likely touched:**
  - planned future `scripts/vitruvius/aec/pricing/*`
  - planned future `scripts/vitruvius/aec/optimization/*`
- **Tests required:** future `test_aec_pricing_*` and `test_aec_optimization_*`
- **Validation gates:** pricing and optimization remain downstream of verification
- **Stop conditions:** if either subsystem is asked to bless unverified candidates, stop
- **Definition of done:** both downstream subsystem foundations are explicitly blocked on upstream truth and replay contracts

#### Task AEC-T019
- **Type:** IMPLEMENTATION-PREP
- **Title:** Tooling foundation task
- **Purpose:** prepare the AEC tool layer only after deterministic artifacts exist
- **Why it exists:** current LLM tooling precedents are useful, but also show how fast prose-rich heuristics can become authority leaks
- **Dependencies:** AEC-T013 through AEC-T018
- **Inputs:** tool-calling plan + strengthened audit tooling sections
- **Expected outputs:**
  - tool catalog design
  - authority fence
  - refusal taxonomy
  - explanation payload contract bound to artifacts/snapshots
- **Files likely touched:**
  - planned future `scripts/vitruvius/aec/tools/*`
- **Tests required:** future `test_aec_tools_catalog.py`, `test_aec_tools_router.py`, `test_aec_tools_refusals.py`, `test_aec_tools_explainer.py`
- **Validation gates:** tools may route/explain only; they may not infer truth or compliance
- **Stop conditions:** if raw rule text, raw vault payloads, or raw candidate state are fed directly into LLM tooling as authority inputs, stop
- **Definition of done:** tool layer is explicitly downstream of deterministic artifact availability

---

### Phase E — First Bounded Implementation Slice Prep

#### Task AEC-T020
- **Type:** IMPLEMENTATION-READY
- **Title:** Define first bounded AEC implementation slice
- **Purpose:** translate all upstream freezes into one bounded slice small enough to execute safely later
- **Why it exists:** the AEC master plan demands a narrow first shippable slice; this task decides that slice only after prerequisites are satisfied
- **Dependencies:** AEC-T001 through AEC-T019
- **Inputs:** strengthened audit + all subsystem foundation packages
- **Expected outputs:** a later implementation-plan candidate for a first slice roughly equivalent to:
  - one DTO family
  - one strict boundary lane
  - one Python reference ECS world
  - one bounded spatial fixture lane
  - one verifier whitelist lane
- **Files likely touched:** future plan artifacts only at this stage
- **Tests required:** must name exact test families before implementation planning begins
- **Validation gates:** slice is narrow, deterministic, replayable, and does not pull in pricing/optimization/tooling prematurely
- **Stop conditions:** if the “first slice” tries to include pricing, optimization, multi-discipline coordination, and tool-calling all at once, stop
- **Definition of done:** future implementation planning has a safe first bounded slice to target

---

### Phase F — Cross-Language Parity Hardening

#### Task AEC-T020A
- **Type:** IMPLEMENTATION-PREP
- **Title:** Create stop-condition enforcement and gate-check package
- **Purpose:** turn the audit’s hard-stop rules into execution-time checklist law for every later AEC plan and sprint
- **Why it exists:** stop conditions that only live in audits get ignored during execution; this task makes them first-class gate checks
- **Dependencies:** AEC-T001 through AEC-T019
- **Inputs:** strengthened audit §§17–18; this master task list
- **Expected outputs:** explicit stop-condition package covering:
  - plan-time no-go checks
  - checklist-time hard stops
  - required refusal language for blocked work
  - mapping from stop condition → owning subsystem/task
- **Files likely touched:**
  - future plan/checklist artifacts under `.ai/03_plans/`
  - future validation/gate logs under `.ai/05_logs/`
- **Tests required:** none initially; later plans/checklists must reference this package directly
- **Validation gates:** no subsystem implementation plan may omit its relevant stop conditions
- **Stop conditions:** if any blocker-class stop is downgraded to a soft warning without explicit approval artifact, stop
- **Definition of done:** every future implementation plan can inherit a hard-stop package instead of restating or weakening the audit ad hoc

#### Task AEC-T021
- **Type:** PARITY
- **Title:** Build cross-language parity hardening package
- **Purpose:** ensure Python, TypeScript, and later Rust seams are all explicitly governed before implementation sprinting starts
- **Why it exists:** current parity is narrow and mostly pairwise; AEC needs seam-wide hardening
- **Dependencies:** AEC-T010, AEC-T011, AEC-T012, AEC-T015, AEC-T016
- **Inputs:** strengthened audit parity sections + subsystem foundation outputs
- **Expected outputs:** parity hardening package covering:
  - boundary v2 parity
  - strict import lane
  - Python↔Rust kernel parity prerequisites
  - backend-factory parity where SQLite/RocksDB duality matters
- **Files likely touched:** future parity plans and tests only at this stage
- **Tests required:** all named parity suites must be scheduled and referenced
- **Validation gates:** no cross-language seam remains “to be figured out during implementation”
- **Stop conditions:** if any seam still relies on informal metadata agreement or prose-only spec alignment, stop
- **Definition of done:** parity-hardening work is ready to drive a later implementation sprint safely

---

### Phase G — Readiness Gate for Actual Implementation Sprinting

#### Task AEC-T022
- **Type:** IMPLEMENTATION-READY
- **Title:** Run AEC go/no-go readiness gate
- **Purpose:** make the final decision on whether implementation planning may advance into a real implementation sprint trigger
- **Why it exists:** without a final gate, task systems drift into coding before blockers are actually resolved
- **Dependencies:** AEC-T001 through AEC-T021
- **Inputs:** every prior task output; strengthened audit acceptance criteria
- **Expected outputs:** one explicit verdict:
  - `GO_TO_IMPLEMENTATION_PLANNING`
  - `NO_GO_BLOCKED`
- **Files likely touched:**
  - future trigger artifact in `.ai/04_tasks/`
  - future plan updates in `.ai/03_plans/`
- **Tests required:** documentary validation only; must cite all green gates and all remaining blockers honestly
- **Validation gates:** every blocker-class task must be closed or explicitly carried as blocker with no-go verdict
- **Stop conditions:** if any blocker is silently waived, stop and reject the gate
- **Definition of done:** repo either has a truthful go/no-go verdict or remains explicitly implementation-blocked

## 7. Critical Path

The critical path is:
1. AEC-T001 namespace freeze
2. AEC-T002 audit/snapshot envelope freeze
3. AEC-T003 DTO/ID/version freeze
4. AEC-T004 frame/unit/tolerance freeze
5. AEC-T005 candidate/canonical + AST admission freeze
6. AEC-T006 clean baseline branch
7. AEC-T007 strict-vs-legacy boundary split
8. AEC-T008 graph-contract reuse/separation decision
9. AEC-T009 benchmark doctrine
10. AEC-T010 parity matrix
11. AEC-T011 fixture/replay corpus definition
12. AEC-T012 boundary foundation
13. AEC-T013 vault foundation
14. AEC-T014 ECS foundation
15. AEC-T015 spatial foundation
16. AEC-T016 verifier foundation
17. AEC-T017 coordination foundation
18. AEC-T018 pricing + optimization foundations
19. AEC-T019 tooling foundation
20. AEC-T020 first bounded slice definition
21. AEC-T021 parity hardening package
22. AEC-T022 go/no-go readiness gate

## 8. Tasks Safe to Parallelize

These are parallel-safe **only after** their dependencies are satisfied:
- AEC-T006 can run in parallel with late Phase A contract work if it does not touch the same planning artifacts
- AEC-T009 and AEC-T010 can run in parallel after AEC-T003–T005 are frozen
- AEC-T012 and AEC-T013 can partially run in parallel after contracts are frozen, because boundary and vault are distinct but still share DTO/provenance inputs
- AEC-T014 can run in parallel with the tail of AEC-T012/AEC-T013 once DTO/envelope/truth contracts are frozen
- AEC-T018 pricing prep and optimization prep can run in parallel with each other only after ECS/spatial/verifier foundations are settled

## 9. Tasks That Must Remain Sequential

These must remain sequential:
- AEC-T001 → AEC-T005 (freeze stack)
- AEC-T002 before any replay/artifact-bearing subsystem task
- AEC-T004 before spatial or verifier tasks
- AEC-T005 before vault or verifier tasks
- AEC-T011 before any subsystem-foundation task that depends on fixtures/replay corpus
- AEC-T016 before AEC-T018 and AEC-T019
- AEC-T020 before AEC-T020A and AEC-T022
- AEC-T020A before AEC-T022

## 10. Global Stop Conditions

Stop the execution-preparation lane if any of these happen:
- namespace is unfrozen but subsystem work begins anyway
- audit/snapshot envelope is undefined but replay/artifact work begins
- DTO/version/id policy is still changing while multiple subsystem tasks start
- `frame_id`, units, or tolerances remain ambiguous
- strict boundary import path is not separated from legacy compatibility
- candidate/canonical separation is undefined but vault or verifier tasks proceed
- TypeScript is assigned orchestration, verification, pricing, coordination, or optimization authority
- Rust is assigned legal meaning, provenance logic, tool routing, or pricing policy
- benchmark-free Rust migration is proposed
- current dirty worktree is accepted as AEC baseline
- root `latest_*` artifacts are treated as authoritative replay inputs
- mutable cache/store semantics are proposed for canonical AEC truth

## 11. “AEC Engine Ready To Implement” Gate Checklist

AEC implementation planning may advance toward a true implementation sprint only when all are true:

- [ ] namespace and ownership map frozen
- [ ] audit/snapshot envelope frozen
- [ ] DTO/ID/versioning policy frozen
- [ ] frame/unit/tolerance policy frozen
- [ ] candidate/canonical truth separation frozen
- [ ] strict-vs-legacy boundary import behavior defined
- [ ] graph-contract reuse/separation decision made
- [ ] clean baseline branch exists
- [ ] benchmark doctrine exists
- [ ] parity matrix exists
- [ ] fixture/replay corpus is defined
- [ ] boundary foundation package complete
- [ ] vault foundation package complete
- [ ] ECS foundation package complete
- [ ] spatial foundation package complete
- [ ] verifier foundation package complete
- [ ] coordination foundation package complete
- [ ] pricing foundation package complete
- [ ] optimization foundation package complete
- [ ] tooling foundation package complete
- [ ] first bounded implementation slice defined
- [ ] backend-factory parity package exists where SQLite/RocksDB duality matters
- [ ] stop-condition enforcement package exists
- [ ] parity hardening package complete
- [ ] explicit go/no-go verdict recorded

## 12. Final Rule

This artifact is allowed to drive future implementation **planning**.
It is **not** permission to start coding the AEC engine before the blocker-class tasks and readiness gate are satisfied.
