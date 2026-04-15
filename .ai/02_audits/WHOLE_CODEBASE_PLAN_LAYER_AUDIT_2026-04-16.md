---
task: whole-codebase-plan-upgrade
phase: 04
created: 2026-04-16
author: AUDITOR
supersedes: null
status: ACCEPTED
---

# Audit — Whole Codebase Plan Layer

## 1. Summary
The active plan layer is not safe enough in its current form. The main problem is not missing files. The problem is that the live plans no longer describe the live repo. The governing dispatcher is stale, the index is stale, the AEC plans are under-grounded, and state files still point future agents toward obsolete plan versions and side-tracks.

## 2. Whole-Codebase Architecture Findings

### 2.1 Repo Shape
- Python is the actual product surface and orchestration layer.
- Rust is a hardened compute extension surface, not a product-control surface.
- TypeScript is isolated to `spatial-daemon/` and owns a file-based spatial contract writer plus CLI.

### 2.2 Existing Building Blocks the Plans Must Respect
- Storage/replay patterns already exist in `graph/event_store.py`, `graph/rocksdb_event_store.py`, `review/stateful_registry.py`, and `kv_migrate.py`.
- Z3 precedents already exist in `spatial/constraint_solver.py` and `geometric/inequality_compiler.py`.
- Spatial contract parity already exists between `spatial-daemon/src/contract_writer.ts` and `spatial/contract_reader.py`.
- Deterministic propagation and bounded orchestration patterns already exist in `compound/dependency_tracker.py`, `compound/differential_propagator.py`, `compound/adversarial.py`, and `query/engine.py`.
- Narrow optimization precedent already exists in `geometric/pareto_optimizer.py`.

### 2.3 Validation Surfaces Already Present
- Spatial, graph, query, review, promotion, parser, and Rust migration tests are already extensive.
- The AEC plans currently fail to exploit that. They talk about validation in the abstract instead of naming the actual existing test surfaces they should extend.

## 3. Active Plan Findings

### 3.1 `00-governing-implementation-plan.md`
Judgment: stale and misleading.

Problems:
- claims a two-plan world even though `.ai/03_plans/` now contains a wider active set
- still reads like a closed sprint reconciliation ledger rather than a live governing dispatcher
- keeps obsolete historical task checklists inline where a cold reader can mistake them for current work

Required fix:
- rewrite as a truthful meta-plan for the current active plan layer
- move historical context into concise reference-only notes
- make active plan consumption order explicit

### 3.2 `INDEX.md`
Judgment: stale and structurally weak.

Problems:
- active inventory is false
- duplicated changelog block remains
- current execution-order section is obsolete

Required fix:
- rebuild around current live plans
- distinguish active vs archived clearly
- make reader entry order explicit

### 3.3 `2026-04-15-nested-agents-governance-plan.md`
Judgment: useful but too thin.

Problems:
- assumes a cleaner baseline than the repo actually has
- does not clearly state which targeted `AGENTS.md` files are still missing
- does not anchor the plan tightly enough to the current authority and state drift

Required fix:
- upgrade into a repo-aware governance maintenance plan
- keep scope bounded to AGENTS hierarchy work

### 3.4 AEC Master + Subsystem Plans
Judgment: coherent but under-grounded.

Problems:
- strong on architecture, weak on repo specifics
- rarely name the real modules, tests, flags, storage patterns, or Rust/TS contracts already present
- do not yet clearly define where new AEC code would live in this repo
- stop conditions are good in principle but still too generic

Required fix:
- keep the architecture
- add concrete repo anchors, proposed code locations, validation commands, and integration constraints

## 4. Cross-Plan Issues

### 4.1 Missing Namespace Decision
No active plan currently makes a clean repository-level call on where AEC code should land. Without that, future implementation can drift across `scripts/vitruvius/`, `spatial/`, `geometric/`, `compound/`, and `engine_rs/`.

Required fix:
- the AEC master plan must freeze a planned namespace and make deviations a stop condition

### 4.2 Validation Under-Specification
The current AEC plans talk about tests and benchmarks, but they do not name:
- which current tests are precedent surfaces
- which new tests must be added
- which cross-language commands must run

Required fix:
- each subsystem plan must have concrete validation and benchmark expectations

### 4.3 Boundary Leakage Risk
Several AEC plans imply cross-language behavior, but none of them yet pin the exact ownership split between:
- Python orchestration
- Rust compute
- TypeScript spatial contract writing

Required fix:
- every relevant AEC plan must state ownership and forbidden ownership explicitly

## 5. Non-Plan Contradictions Affecting Safe Plan Consumption

### 5.1 Root `AGENTS.md`
- still points at stale state paths under `.ai/10_state/`
- this is a higher-authority defect and directly affects how plans are consumed

### 5.2 `current-phase.md`
- still points to obsolete roadmap/plan versions
- still frames a previously closed side-track as the natural next action

### 5.3 `active_context.md`
- still carries stale branch framing and historical sprint narration that no longer matches the live branch baseline

### 5.4 `milestone-tracker.md`
- contains at least one truth mismatch around already-shipped registry rotation, which remains shown as incomplete in one section

## 6. Risks If Left Unfixed
- future agents will choose the wrong plan first
- AEC implementation will start from abstract plans instead of the real codebase
- Rust and TypeScript boundaries will blur because the plans do not yet name the actual repo split strongly enough
- validation will be skipped or improvised because the plans do not yet name the actual test and benchmark surfaces
- stale state references will keep misrouting execution

## 7. Audit Decision
Proceed with a bounded but substantial rewrite:
- create the missing SEL artifacts for this task
- rewrite the governing plan and index
- upgrade the nested-AGENTS plan
- upgrade every AEC plan with repo-grounded detail
- perform minimal state/authority fixes where stale references would misroute future execution

## 8. Final Audit Judgment
The codebase is strong enough to support a detailed plan layer.

The current plan layer is not.

Rewrite is required, not optional.
