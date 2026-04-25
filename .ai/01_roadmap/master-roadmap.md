# Vitruvius Master Roadmap

**Updated:** 2026-04-25
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

### Priority 1 — AEC-MEPFS Backbone readiness gate
- **Status:** planned
- **Why it matters:** the next AEC move is to admit an authored, standards-aligned AEC-MEPFS Backbone as the classification target before documents and rules are mapped into it.
- **Evidence:** `/.ai/03_plans/AEC-MEPFS-Backbone/2026-04-25_aec_mepfs_backbone_readiness_plan.md`, `/.ai/03_plans/AEC_ENGINE_MASTER_IMPLEMENTATION_PLAN.md`, `/.ai/IMPLEMENTATION_MATRIX.md`, `/.ai/05_logs/2026-04-23_aec-runtime-roots-audit-and-lane-decision.md`
- **Next concrete action:** close the AEC-MEPFS Backbone readiness gates; do not open runtime implementation, Neo4j cleanup, feature-flag cutover, graph rebuild, or backup test runs until the scorecard reaches `ready for bounded implementation`.

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

### AEC first bounded slice runtime kickoff
- **Status:** blocked
- **Why blocked:** AEC-MEPFS Backbone readiness gates are not closed and runtime implementation roots were not verified in the codebase.
- **Evidence:** `/.ai/IMPLEMENTATION_MATRIX.md`, `/.ai/03_plans/AEC_ENGINE_MASTER_IMPLEMENTATION_PLAN.md`, `/.ai/03_plans/AEC-MEPFS-Backbone/2026-04-25_aec_mepfs_backbone_readiness_plan.md`, `/.ai/05_logs/2026-04-23_aec-runtime-roots-audit-and-lane-decision.md`
- **Dependency:** accepted readiness scorecard + explicit execution packet + runtime namespace decision + implementation roots.
- **Next concrete action:** keep runtime blocked until the AEC-MEPFS Backbone readiness scorecard reaches `ready for bounded implementation`.

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
