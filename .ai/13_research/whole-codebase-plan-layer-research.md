---
task: whole-codebase-plan-upgrade
phase: 03
created: 2026-04-16
author: RESEARCHER
supersedes: null
status: ACCEPTED
---

# Research — Whole Codebase Plan Layer

## 1. Research Objective
Ground the active planning layer in the actual Vitruvius repository rather than in stale sprint history or architecture-only abstractions.

## 2. Repo Reality

### 2.1 Execution State
- The repo is between sprints.
- The historical sprint burst described in state files is largely closed.
- No active implementation sprint is open by default.
- The AEC engine remains planning/governance work, not runtime code.

### 2.2 Runtime Architecture
- Python remains the orchestration and product surface.
- `scripts/pipeline_cli.py` is the spine and uses lazy imports by command.
- Rust is a hardened compute zone under `scripts/vitruvius/engine_rs/` and `scripts/vitruvius/datalog_rs/`.
- TypeScript is isolated to `spatial-daemon/` and communicates by file contract, not by live RPC.

### 2.3 Existing Capability Clusters
- Parsing / ingestion: `scripts/vitruvius/parsers/*`, `conversion.py`, `scanner.py`, `ocr.py`
- Review / promotion: `ollama_review.py`, `review/*`, `pre_review_filter.py`, `promotion_validator.py`, `promotion/*`
- Graph / query: `graph/*`, `query/*`
- Spatial: `spatial/*`, `spatial-daemon/*`
- Compound AI: `compound/*`
- Geometric reasoning: `geometric/*`
- Benchmarking / audits: `bench/*`

## 3. Existing AEC-Adjacent Code

### 3.1 Spatial / Verification Precursors
- `scripts/vitruvius/spatial/constraint_solver.py` already provides a narrow Z3 evaluator.
- `scripts/vitruvius/geometric/inequality_compiler.py` compiles parametric rules into Z3 inequalities.
- `scripts/vitruvius/spatial/cli.py` already enforces flag-gated spatial commands.
- `scripts/vitruvius/spatial/contract_reader.py` verifies the SHA-256 footer written by `spatial-daemon/src/contract_writer.ts`.

### 3.2 Storage / Replay Precursors
- `scripts/vitruvius/graph/event_store.py` and `graph/rocksdb_event_store.py` already define append-only event log patterns.
- `scripts/vitruvius/review/stateful_registry.py` and `review/rocksdb_stateful_registry.py` already define feature-gated backend factories.
- `scripts/vitruvius/kv_migrate.py` already provides a migration pattern between SQLite and RocksDB-backed stores.

### 3.3 Coordination / Propagation Precursors
- `scripts/vitruvius/compound/dependency_tracker.py` and `compound/differential_propagator.py` already model deterministic downstream invalidation.
- `scripts/vitruvius/query/engine.py` already models structured evidence-citing query surfaces.
- `scripts/vitruvius/compound/adversarial.py` already models bounded multi-role orchestration and deterministic adjudication.

### 3.4 Optimization Precursors
- `scripts/vitruvius/geometric/pareto_optimizer.py` already ships a narrow deterministic optimization site.
- `scripts/tests/test_geometric_pareto_optimizer.py` is the closest existing precedent for optimization validation.

## 4. Feature Flags Relevant to Planning
- Spatial/AEC precursor flags:
  - `l_spatial_ingestion`
  - `l_z3_constraint_solver`
  - `m_ifc_ontology_mapping`
  - `m_owl_turtle_export`
  - `n_spatial_daemon_enabled`
- Related shipped capability flags:
  - `geom_*`
  - `gt_*`
  - `hp_*`
  - `z_*`
  - `y_*`
- Parser-chain flags with similar activation discipline:
  - `p1b_*`

## 5. Test and Validation Surfaces
- Spatial / contracts:
  - `scripts/tests/test_spatial_cli.py`
  - `scripts/tests/test_spatial_constraint_solver.py`
  - `scripts/tests/test_spatial_contract_reader.py`
  - `scripts/tests/test_spatial_schema.py`
  - `scripts/tests/test_spatial_edge_builder.py`
  - `scripts/tests/test_spatial_edge_builder_parity.py`
  - `spatial-daemon/tests/*.test.ts`
- Graph / storage / replay:
  - `scripts/tests/test_graph_contract.py`
  - `scripts/tests/test_graph_event_store.py`
  - `scripts/tests/test_graph_event_store_delta.py`
  - `scripts/tests/test_temporal_query.py`
- Query / tool routing precursors:
  - `scripts/tests/test_query_engine.py`
  - `scripts/tests/test_query_cli.py`
  - `scripts/tests/test_graphrag_router.py`
- Compound / orchestration precursors:
  - `scripts/tests/test_compound_wasm_kernel.py`
  - `scripts/tests/test_datalog_rs_bridge.py`
  - `scripts/tests/test_review_moe_routing_policy.py`
  - `scripts/tests/test_review_routing.py`
- Optimization precursors:
  - `scripts/tests/test_geometric_pareto_optimizer.py`

## 6. Plan-Layer Drift

### 6.1 Governing Plan Drift
- The governing plan still describes a plan inventory that no longer exists.
- It embeds obsolete historical execution tasks inline, which reads like live work even though the queue is closed.

### 6.2 Index Drift
- `INDEX.md` still claims only the governing plan is active.
- It contains duplicated changelog content and an obsolete dependency view.

### 6.3 AEC Plan Drift
- The AEC plan family is coherent at the architecture level.
- It is not yet grounded in:
  - actual code roots
  - actual modules to extend
  - current feature flags
  - current tests
  - current Rust/TypeScript boundary surfaces
  - repo-specific stop conditions

### 6.4 State Drift Affecting Plan Consumption
- `current-phase.md` still references old version numbers and a historically closed side-track.
- Root `AGENTS.md` still points to stale state file paths.

## 7. Planning Implications
- The governing plan must become a truthful dispatcher for the current plan set, not a closed sprint ledger.
- The index must reflect all active plans currently in `.ai/03_plans/`.
- The nested-AGENTS plan must reflect the repo’s real current coverage gap rather than a hypothetical clean slate.
- Every AEC plan must name:
  - proposed code location
  - specific existing modules to reuse or not overload
  - exact validation surfaces
  - relevant feature flags
  - relevant Rust or TypeScript boundaries
  - concrete stop conditions tied to the existing repo

## 8. Open Questions That the Plans Must Handle Explicitly
- Planned Python namespace for AEC implementation: use `scripts/vitruvius/aec/` unless superseded by a later approved namespace decision
- Planned AEC storage layout: keep human canonical law in layer 3, machine-admitted vault data in layers 5/6
- Planned CLI exposure: follow the existing lazy-import pattern in `pipeline_cli.py`, do not create direct heavyweight imports at module load
- Planned Rust scope: only accelerate frozen compute contracts, never lead with Rust when the Python contract is still fluid

## 9. Research Conclusion
Vitruvius already contains many of the lower-level building blocks an AEC engine would rely on, but the live plans do not currently say so. The required rewrite is not cosmetic. It is a control-layer correction so future implementation work starts from the actual repo rather than from stale plan memory.
