# Milestone Tracker

**Updated:** 2026-04-25
**Purpose:** verified milestone tracker for active, completed, blocked, and deferred milestones

## 1. Active Milestones

| Milestone | Status | Evidence | Next concrete action | Dependency / blocker |
|---|---|---|---|---|
| AEC-MEPFS Backbone first shadow slice | implemented as file-backed shadow staging; not live-runtime-authorized for primary graph cutover | `/.ai/03_plans/AEC-MEPFS-Backbone/eighth-readiness-runtime-priming-packet.md`, `/.ai/03_plans/AEC-MEPFS-Backbone/readiness-closure-scorecard.md`, `/.ai/03_plans/AEC-MEPFS-Backbone/first-shadow-only-implementation-packet.md`, `/.ai/14_human_inbox/ANSWER_HERE.md`, `/.ai/05_logs/2026-04-25_aec_bb_s8_runtime_priming_validation.md`, `/006_System-Manifests/aec-mepfs-backbone/shadow-staging/20260425T154000Z/shadow-staging-report.json` | plan next bounded read-only consumer/reporting slice after fresh impact review | First shadow staging is file-backed and validated; protected content ingest, live graph mutation, API/Explorer cutover, and primary runtime promotion remain blocked |

## 2. Completed Milestones

| Milestone | Status | Evidence | Notes |
|---|---|---|---|
| Core pipeline through promotion | completed | `scripts/pipeline_cli.py`, `scripts/vitruvius/promotion_validator.py`, `003_Canonical-Knowledge-Layer/shared/relationships/` | Not a live roadmap target anymore |
| Live-docs rebase across `.ai/01_roadmap/` and `.ai/03_plans/INDEX.md` | completed | `/.ai/01_roadmap/`, `/.ai/03_plans/INDEX.md`, `/.ai/README.md` | Active operating docs now use repo-verified status language |
| Plan-family slimming | completed | `/.ai/03_plans/INDEX.md`, `/.ai/03_plans/00-governing-implementation-plan.md`, `/.ai/archive/ARCHIVE_INDEX.md` | The active plan surface now reduces AEC to the master plan + blocked session packet and marks the remaining burst reference-only |
| Reference/path integrity cleanup | completed | `/.ai/README.md`, `/.ai/01_roadmap/`, `/.ai/05_logs/2026-04-21_control-surface-consolidation-validation.md` | Live docs no longer carry stale path/viewer/reference drift in the active surface |
| Graph build/query surface | completed | `scripts/vitruvius/graph/cli.py`, `scripts/vitruvius/graph/visualize.py`, `005_Operational-Intelligence-Layer/graph/` | Historical “not started” checklist removed from active tracking |
| Knowledge Graph v2 transition | completed | `scripts/vitruvius/kg/`, `scripts/tests/test_kg*.py`, `005_Operational-Intelligence-Layer/graph/kg-v2/` | v2 audit and rectification docs are authoritative |
| Laws-wave bounded automation and ready-family aggregate closure | completed | `.ai/10_state/laws-wave-status.json`, `.ai/05_logs/2026-04-20_ra-386-residual-hardening-validation.md` | RA-386 residual-hardening is closed; do not keep as active milestone |
| Graph Explorer implementation | completed | `explorer/src/components/graph/*`, `api/index.ts`, `explorer/README.md` | Maintained as shipped capability |
| AI relationship enrichment pilot | completed | `.ai/02_audits/2026-04-24_ai_relationship_enrichment_pilot_audit.md`, `.ai/03_plans/2026-04-24_ai_relationship_enrichment_pilot_plan.md`, `.ai/05_logs/2026-04-24_ai_relationship_enrichment_pilot_validation.md` | Phase 5E candidate-generation seam is implemented; full-corpus enrichment remains a separate operator-enabled run/review activity |
| 001-Laws KG rebuild and Explorer graph refresh | completed | `.ai/02_audits/2026-04-24_post_laws_kg_rebuild_relationship_graph_audit.md`, `.ai/05_logs/2026-04-24_post_laws_kg_rebuild_relationship_graph_validation.md`, `005_Operational-Intelligence-Layer/graph/kg-v2/20260424T195515Z_kg_v2_unified.json` | Neo4j was cleared and reloaded from the `001-Laws` snapshot only; rule display-title quality is clean |
| Concept-centric relationship enrichment MVP | completed | `.ai/05_logs/2026-04-25_concept_centric_relationship_enrichment_validation.md`, `scripts/vitruvius/kg/relationship_enricher.py`, `api/index.ts`, `explorer/src/components/ExplorerRail.tsx` | Existing `001-Laws` snapshot enriched without raw/canonical rebuild; Neo4j now loaded from `20260425T003423Z_kg_v2_unified_enriched.json` |
| KG relationship quality and graph UX maintenance | completed as non-blocking MVP maintenance | `.ai/02_audits/2026-04-25_taxonomy_first_relationship_quality_audit.md`, `.ai/03_plans/2026-04-25_taxonomy_first_relationship_quality_plan.md`, `.ai/05_logs/2026-04-25_concept_centric_relationship_enrichment_validation.md` | No longer competes with the AEC-MEPFS readiness gate; future semantic relationship work belongs under governed backbone admission |
| Nested AGENTS governance | completed | `**/AGENTS.md`, `.ai/05_logs/2026-04-20_nested-agents-governance-validation.md` | No longer a pending active milestone |

## 3. Blocked / Deferred Milestones

| Milestone | Status | Evidence | Blocker / reason | Next concrete action |
|---|---|---|---|---|
| AEC first bounded slice runtime kickoff | blocked | `/.ai/IMPLEMENTATION_MATRIX.md`, `/.ai/03_plans/AEC_ENGINE_MASTER_IMPLEMENTATION_PLAN.md`, `/.ai/03_plans/AEC-MEPFS-Backbone/2026-04-25_aec_mepfs_backbone_readiness_plan.md`, `/.ai/03_plans/AEC-MEPFS-Backbone/runtime-root-implementation-packet.md` | readiness gates are not closed; runtime-root packet is prepared but not accepted; legal/steward/currentness/rollback decisions remain gated | reopen only after the AEC-MEPFS Backbone readiness scorecard reaches `ready for bounded implementation` |
| Generic dataset expansion beyond bounded laws-wave | blocked | `.ai/10_state/laws-wave-status.json`, `.ai/03_plans/laws-wave/LAWS_WAVE_RELOAD_PROTOCOL.md` | current truthful state is maintenance/completion, not open expansion | reopen only with new authoritative source or explicit strategy change |
| Skills/agents layer consolidation | deferred | `/.ai/11_skills/`, `/.ai/skills/`, `/.ai/12_agents/` | not blocking core operating surface | handle after active plan-family slimming |

## 4. Milestone Evidence Notes

- Use repository artifacts and run logs as evidence before plan text.
- Treat old tranche-by-tranche and sprint-by-sprint narrative as historical reference only.
- Treat fresh verification claims as **unverified** unless they were rerun after the last implementation change.
