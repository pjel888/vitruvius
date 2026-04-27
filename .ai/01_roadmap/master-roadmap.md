# Vitruvius Master Roadmap

> **2026-04-27 AEC-MEPFS-first update:** Product direction moved from legacy-default preservation to a prelaunch AEC-MEPFS-first Explorer default. The file-backed cutover is governed by `.ai/03_plans/AEC-MEPFS-Backbone/2026-04-27_aec_mepfs_first_explorer_cutover_packet.md`; legacy graph behavior is secondary, while production Neo4j promotion, KG mutation, protected ingest, broad live runtime, and unsupported threshold claims remain blocked.


> **2026-04-27 superseding update:** AEC-MEPFS safe autonomous scope is closed through `8b05e559` and evidence run `20260427T044757Z`. Static resolver contract verification, guarded default-off file-backed resolver routes, resolver fixtures, parity, observational benchmark evidence, Explorer/API runtime-status parity, and final closure/state reconciliation are complete; broad live runtime remains blocked.


**Updated:** 2026-04-27
**Purpose:** strategic roadmap for the active operating layer  
**Truth rule:** repository evidence overrides historical planning claims

## 1. Purpose

This roadmap defines what Vitruvius has actually shipped, what is strategically active now, and what remains blocked or deferred.

It is intentionally compact. Historical sprint narration, tranche-by-tranche execution detail, and superseded planning logic belong in:

- `/.ai/09_archive/`
- `/.ai/05_logs/`
- `/.ai/03_plans/laws-wave/`
- `/.ai/10_state/decisions.md`

## 2. Current State Snapshot

| Area | Status | Evidence | Next action |
|---|---|---|---|
| Core document pipeline (scan → convert → refine → canonicalize → extract → review → promote) | completed | `scripts/pipeline_cli.py`, `scripts/vitruvius/promotion_validator.py`, `003_Canonical-Knowledge-Layer/shared/relationships/` | Maintain only; no roadmap expansion needed now |
| Graph build/query surface | completed | `scripts/vitruvius/graph/cli.py`, `scripts/vitruvius/graph/visualize.py`, `005_Operational-Intelligence-Layer/graph/` | Keep docs truthful and artifact references valid |
| Knowledge Graph v2 transition | completed | `scripts/vitruvius/kg/`, `scripts/tests/test_kg*.py`, `005_Operational-Intelligence-Layer/graph/kg-v2/` | Treat v2 audit/rectification docs as reference, not active work |
| Laws-wave bounded automation | completed | `.ai/10_state/laws-wave-status.json`, `config/datasets/laws-completed-lanes.yaml`, `.ai/03_plans/laws-wave/LAWS_WAVE_ARTIFACT_INDEX.md` | Keep artifact index and state ledgers consistent |
| Graph Explorer | completed | `explorer/src/components/graph/*`, `api/index.ts`, `explorer/README.md` | Maintain only if implementation changes |
| Nested AGENTS coverage | completed | `**/AGENTS.md`, `.ai/05_logs/2026-04-20_nested-agents-governance-validation.md` | Archive plan as completed reference |
| Active planning surface rebase | completed | `/.ai/01_roadmap/`, `/.ai/03_plans/INDEX.md`, `/.ai/README.md` | Keep the rewritten surface stable and trim remaining active plan families |

## 3. Active Strategic Priorities

### Priority 1 — AEC-MEPFS Backbone max-safe-scope closure
- **Status:** closed to current repo-actionable safe scope through `8b05e559` and final closure/state reconciliation
- **Why it matters:** the authored Backbone plan now has file-backed preview, resolver contract, guarded default-off resolver, parity, observational benchmark, runtime-status evidence, and closure proof without crossing blocked live graph or protected-content boundaries.
- **Evidence:** `/.ai/03_plans/AEC-MEPFS-Backbone/final-aec-mepfs-closure-packet.md`, `/.ai/03_plans/AEC-MEPFS-Backbone/2026-04-27_final_closure_and_state_reconciliation_packet.md`, `/.ai/03_plans/AEC-MEPFS-Backbone/readiness-closure-scorecard.md`, `/.ai/05_logs/2026-04-27_aec_mepfs_final_closure_state_reconciliation_validation.md`
- **Next concrete action:** no further GREEN or satisfied-YELLOW AEC-MEPFS implementation work remains; require a new dedicated gated packet or valid external authority before live runtime, graph mutation, protected ingest, Explorer default, default-on flag, or threshold-adoption work.

### Priority 2 — Verification refresh for unverified claims
- **Status:** planned
- **Why it matters:** some operational claims are log-backed but not freshly rerun.
- **Evidence:** `/.ai/IMPLEMENTATION_MATRIX.md` (`Full test suite green claim`), `.ai/05_logs/2026-04-20_full-test-suite-green-validation.md`
- **Next concrete action:** rerun high-value verification only when the implementation surface changes or before making fresh success claims.

### Priority 3 — Preserve the live planning surface
- **Status:** maintain
- **Why it matters:** completed control-surface cleanup should remain stable while the next lane decision is made.
- **Evidence:** `/.ai/README.md`, `/.ai/03_plans/INDEX.md`, `/.ai/01_roadmap/current-phase.md`
- **Next concrete action:** keep the live entry docs truthful and avoid reactivating completed reference-only plan families.

## 4. Completed / Shipped Capabilities

These are not active roadmap targets anymore.

- **Promotion governance** — completed  
  Evidence: `scripts/vitruvius/promotion_validator.py`, `003_Canonical-Knowledge-Layer/shared/relationships/`
- **Graph contract + query surfaces** — completed  
  Evidence: `scripts/vitruvius/graph/cli.py`, `scripts/pipeline_cli.py`
- **KG v2 transition** — completed  
  Evidence: `scripts/vitruvius/kg/`, `scripts/tests/test_kg*.py`, `/.ai/02_audits/2026-04-19_knowledge_graph_transition_post_implementation_audit_v2.md`
- **Laws-wave bounded execution and aggregate closure** — completed  
  Evidence: `.ai/10_state/laws-wave-status.json`, `.ai/05_logs/2026-04-20_ra-386-residual-hardening-validation.md`
- **Graph Explorer implementation** — completed  
  Evidence: `explorer/README.md`, `explorer/src/components/graph/`, `api/index.ts`
- **Nested AGENTS governance** — completed  
  Evidence: `.ai/05_logs/2026-04-20_nested-agents-governance-validation.md`, `**/AGENTS.md`

## 5. Blocked / Dependent Items

### AEC live runtime kickoff
- **Status:** blocked beyond the default-off file-backed resolver runtime packet
- **Why blocked:** current implemented runtime is limited to default-off, file-backed `/v2/resolve*` routes plus an observational in-process benchmark harness. Broader hot runtime, Neo4j mutation, KG rebuild/reload, protected ingest, Explorer defaults, default-on feature flags, and runtime threshold pass/fail adoption remain unauthorized.
- **Evidence:** `/.ai/IMPLEMENTATION_MATRIX.md`, `/.ai/03_plans/AEC-MEPFS-Backbone/runtime-governance-admission-packet.md`, `/.ai/03_plans/AEC-MEPFS-Backbone/2026-04-27_bounded_resolver_runtime_contract_packet.md`, `/.ai/03_plans/AEC-MEPFS-Backbone/runtime-root-implementation-packet.md`
- **Dependency:** a later explicit live-runtime packet with rollback, impact, source-rights, route, parity, and benchmark evidence.
- **Next concrete action:** keep broader live runtime blocked; open a new dedicated packet only when rollback, parity, route inventory, source-rights, benchmark, and safety evidence satisfy the relevant gate.

### Generic dataset expansion beyond bounded laws-wave
- **Status:** blocked
- **Why blocked:** current truthful state is bounded completion/maintenance, not open-ended expansion.
- **Evidence:** `/.ai/10_state/laws-wave-status.json`, `/.ai/03_plans/laws-wave/LAWS_WAVE_RELOAD_PROTOCOL.md`
- **Next concrete action:** only reopen with a new authoritative source or explicit user-directed strategy change.

## 6. Deferred / Not Worth Pursuing Now

- Broad new roadmap creation before active docs are stable
- Physical archive migrations that may break references before the active surface is stable
- Treating completed tranche-by-tranche plans as live execution queues
- Opening generic Phase 11 work without a new accepted strategy decision

## 7. References

### Live operating references
- `/.ai/README.md`
- `/.ai/ACTIVE_WORK.md`
- `/.ai/STRATEGIC_NEXT_MOVE.md`
- `/.ai/IMPLEMENTATION_MATRIX.md`

### State / evidence references
- `/.ai/10_state/active_context.md`
- `/.ai/10_state/laws-wave-status.json`
- `/.ai/05_logs/2026-04-20_ra-386-residual-hardening-validation.md`
- `/.ai/05_logs/2026-04-20_full-test-suite-green-validation.md`

### Archive / reference history
- `/.ai/archive/ARCHIVE_INDEX.md`
- `/.ai/09_archive/`
- `/.ai/10_state/decisions.md`
