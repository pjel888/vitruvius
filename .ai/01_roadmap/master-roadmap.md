# Vitruvius Master Roadmap

> **2026-04-28 taxonomy population update:** AEC-MEPFS Explorer/API file-backed
> taxonomy population expanded from the sparse skeleton to run
> `20260428T033525Z`: 779 nodes, 760 edges, 19 roots, 190 L2 topics, 570 L3
> subtopics, and max depth 3. The update used repo research plus public
> accreditation/licensure/course-outline structures only as high-level topic
> calibration; no protected source payloads, Neo4j mutation, or KG
> rebuild/reload/reset were introduced.

> **2026-04-28 actual implementation update:** AEC-MEPFS moved from prep-only
> closure into actual local implementation. `/v2/resolve*` is now default-on,
> deterministic, file-backed, and rollback-disableable through
> `VITRUVIUS_AEC_MEPFS_RESOLVER_RUNTIME=0|false|no|off|disabled`; Explorer
> remains AEC-MEPFS-first; API-local resolver thresholds are adopted for run
> `20260428T004350Z`. Production Neo4j promotion and protected payload admission
> remain hard-blocked without production credentials/rollback proof and external
> legal/steward/source-rights authority.

> **2026-04-27 AEC-MEPFS-first update:** Product direction moved from legacy-default preservation to a prelaunch AEC-MEPFS-first Explorer default. The file-backed cutover is governed by `.ai/03_plans/AEC-MEPFS-Backbone/2026-04-27_aec_mepfs_first_explorer_cutover_packet.md`; legacy graph behavior is secondary, while production Neo4j promotion, KG mutation, protected ingest, broad live runtime, and unsupported threshold claims remain blocked.


> **2026-04-27 superseding update:** AEC-MEPFS safe autonomous scope is closed through `8b05e559` and evidence run `20260427T044757Z`. Static resolver contract verification, guarded default-off file-backed resolver routes, resolver fixtures, parity, observational benchmark evidence, Explorer/API runtime-status parity, and final closure/state reconciliation are complete; broad live runtime remains blocked.


**Updated:** 2026-04-28
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

### Priority 1 — AEC-MEPFS local actual implementation
- **Status:** implemented for file-backed runtime/default surfaces; production and protected-content gates remain hard-blocked
- **Why it matters:** the authored Backbone plan now has file-backed preview, resolver contract, default-on deterministic `/v2/resolve*` runtime with rollback disable behavior, Explorer AEC-MEPFS-first default behavior, API-local runtime threshold evidence, and closure proof without crossing production Neo4j or protected-payload boundaries.
- **Evidence:** `/.ai/03_plans/AEC-MEPFS-Backbone/2026-04-27_actual_aec_mepfs_implementation_cutover_packet.md`, `/.ai/03_plans/AEC-MEPFS-Backbone/final-aec-mepfs-actual-implementation-closure-packet.md`, `/.ai/05_logs/2026-04-28_aec_mepfs_actual_implementation_cutover_validation.md`, `/006_System-Manifests/aec-mepfs-backbone/api-route-inventory/20260428T004350Z/api-route-inventory-report.json`, `/006_System-Manifests/aec-mepfs-backbone/runtime-resolver-benchmark/20260428T004350Z/runtime-resolver-benchmark-report.json`, `/006_System-Manifests/aec-mepfs-backbone/runtime-thresholds/20260428T004350Z/runtime-threshold-adoption-report.json`
- **Next concrete action:** no further local implementation slice remains for file-backed `/v2/resolve*`, Explorer AEC-MEPFS default behavior, or API-local resolver thresholds. Production live graph promotion requires production target credentials plus backup/restore/rollback transcript; protected payload admission requires valid external legal/steward/source-rights records.

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

### AEC production/live graph and protected payload admission
- **Status:** hard-blocked beyond implemented local file-backed runtime
- **Why blocked:** the local resolver route, Explorer default, and API-local
  thresholds are implemented. Production Neo4j graph promotion lacks production
  target credentials and a fresh backup/restore/rollback transcript. Protected
  payload admission lacks source-specific legal/steward/source-rights authority.
- **Evidence:** `/.ai/03_plans/AEC-MEPFS-Backbone/2026-04-27_actual_aec_mepfs_implementation_cutover_packet.md`, `/.ai/03_plans/AEC-MEPFS-Backbone/2026-04-27_neo4j_live_promotion_readiness_packet.md`, `/.ai/03_plans/AEC-MEPFS-Backbone/legal-and-steward-admission-record.md`
- **Dependency:** production credentials plus rollback proof for live graph promotion; valid external authority for protected payload admission.
- **Next concrete action:** do not mutate production Neo4j or ingest protected payloads until those external gates are satisfied.

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
