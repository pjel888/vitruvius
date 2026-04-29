# Milestone Tracker

> **2026-04-29 broad taxonomy real semantic enrichment update:** All 24
> AEC-MEPFS root taxonomies now have zero L4 scaffold labels. Run
> `20260429T015840Z` adds 6240 real non-Architecture semantic L4 nodes and
> preserves the Architecture real semantic branch from `15dae0d0`.

> **2026-04-29 Architecture real semantic enrichment update:** The Architecture
> branch now uses run `20260429T013500Z` with 1064 Architecture records and 878
> real Architecture L4 topics. All 146 Architecture L3 parents have at least six
> real L4 children, and Architecture L4 placeholder labels ending in `Concepts`,
> `Concept Anchor`, `Rule Context`, or `Topics` are at zero.

> **2026-04-29 all-taxonomy deep population update:** AEC-MEPFS taxonomy
> population now uses run `20260428T174344Z` with 4605 nodes and 4581 edges
> across all 24 roots. The expansion added 1908 metadata-only records across
> history, laws, civil, structural, geotechnical, urban, MEPFS, sanitary,
> security, smart systems, heritage, governance, and supporting domains.

> **2026-04-28 actual implementation update:** The prep-only/four-lane closure
> state has been superseded by project-owner actual implementation authority.
> The local AEC-MEPFS file-backed runtime is now default-on for `/v2/resolve*`
> with an explicit rollback disable flag, Explorer remains AEC-MEPFS-first, and
> API-local resolver thresholds are adopted for evidence run `20260428T004350Z`.
> Production Neo4j live promotion and protected payload admission remain
> hard-blocked by missing production credentials/rollback proof and missing
> external legal/steward/source-rights authority.

> **2026-04-27 AEC-MEPFS-first update:** The prior Explorer-default blocked state has been superseded by a project-owner prelaunch cutover directive and packet. AEC-MEPFS is now the intended default Explorer taxonomy via file-backed artifacts; the remaining blockers are production/live graph promotion, protected payload admission, destructive KG/Neo4j mutation, and unsupported broad runtime threshold claims.


> **2026-04-27 superseding update:** AEC-MEPFS safe autonomous scope is closed through `8b05e559` and evidence run `20260427T044757Z`. Static/no-op contract work, default-off file-backed resolver runtime, fixture expansion, parity, observational benchmark evidence, Explorer/API runtime-status parity, and final closure/state reconciliation are complete. Broad live runtime, Neo4j/KG mutation, protected ingest, Explorer default adoption, default-on flags, and runtime threshold pass/fail claims remain blocked.


**Updated:** 2026-04-29
**Purpose:** verified milestone tracker for active, completed, blocked, and deferred milestones

## 1. Active Milestones

| Milestone | Status | Evidence | Next concrete action | Dependency / blocker |
|---|---|---|---|---|
| AEC-MEPFS actual file-backed runtime and Explorer default | implemented locally with hard-blocked production/protected gates | `/.ai/03_plans/AEC-MEPFS-Backbone/2026-04-27_actual_aec_mepfs_implementation_cutover_packet.md`, `/.ai/03_plans/AEC-MEPFS-Backbone/final-aec-mepfs-actual-implementation-closure-packet.md`, `/.ai/05_logs/2026-04-28_aec_mepfs_actual_implementation_cutover_validation.md`, `/006_System-Manifests/aec-mepfs-backbone/api-route-inventory/20260428T004350Z/api-route-inventory-report.json`, `/006_System-Manifests/aec-mepfs-backbone/runtime-resolver-benchmark/20260428T004350Z/runtime-resolver-benchmark-report.json`, `/006_System-Manifests/aec-mepfs-backbone/runtime-thresholds/20260428T004350Z/runtime-threshold-adoption-report.json` | no further local implementation slice remains for file-backed `/v2/resolve*`, Explorer AEC-MEPFS default behavior, or API-local resolver thresholds | Production Neo4j live promotion requires production target credentials and backup/restore/rollback proof; protected payload admission requires valid external legal/steward/source-rights authority; broader external/browser/Neo4j runtime thresholds require those runtime surfaces |
| AEC-MEPFS taxonomy population expansion | implemented locally; all 24 root taxonomies deeply populated with rights-safe metadata labels | `.ai/03_plans/AEC-MEPFS-Backbone/2026-04-28_aec_mepfs_taxonomy_domain_expansion_and_spacing_packet.md`, `.ai/03_plans/AEC-MEPFS-Backbone/2026-04-28_architecture_licensure_taxonomy_expansion_packet.md`, `.ai/05_logs/2026-04-28_aec_mepfs_taxonomy_domain_expansion_and_spacing_validation.md`, `.ai/05_logs/2026-04-28_architecture_licensure_taxonomy_expansion_validation.md`, `/006_System-Manifests/aec-mepfs-backbone/shadow-staging/20260428T174344Z/shadow-staging-consumer-report.json`, `/006_System-Manifests/aec-mepfs-backbone/taxonomy-expansion/20260428T174344Z/all-taxonomy-deep-population-report.json` | continue with steward-reviewed typed relationship/source-overlay enrichment and performance monitoring for the larger graph | Protected source payloads and production Neo4j promotion remain externally gated |

Twenty-second shadow slice evidence is also current for the active AEC-MEPFS
Backbone milestone: `/.ai/03_plans/AEC-MEPFS-Backbone/twenty-second-shadow-evidence-manifest-packet.md`,
`/.ai/05_logs/2026-04-26_aec_bb_shadow_evidence_manifest_validation.md`,
`/006_System-Manifests/aec-mepfs-backbone/benchmarks/20260426T084118Z/benchmark-report.json`,
and
`/006_System-Manifests/aec-mepfs-backbone/evidence-manifest/20260426T084131Z/shadow-evidence-manifest-report.json`.

Twenty-third shadow slice evidence is current for the active AEC-MEPFS Backbone
milestone: `/.ai/03_plans/AEC-MEPFS-Backbone/twenty-third-shadow-evidence-preview-route-packet.md`,
`/.ai/05_logs/2026-04-26_aec_bb_shadow_evidence_preview_route_validation.md`,
`/006_System-Manifests/aec-mepfs-backbone/parity/20260426T090300Z/api-explorer-parity-report.json`,
`/006_System-Manifests/aec-mepfs-backbone/api-route-inventory/20260426T090320Z/api-route-inventory-report.json`,
`/006_System-Manifests/aec-mepfs-backbone/boundary-audit/20260426T090340Z/shadow-boundary-audit-report.json`,
`/006_System-Manifests/aec-mepfs-backbone/benchmarks/20260426T090400Z/benchmark-report.json`,
and
`/006_System-Manifests/aec-mepfs-backbone/evidence-manifest/20260426T090420Z/shadow-evidence-manifest-report.json`.

Twenty-fourth shadow slice evidence is current for the active AEC-MEPFS
Backbone milestone:
`/.ai/03_plans/AEC-MEPFS-Backbone/twenty-fourth-shadow-evidence-hash-consistency-packet.md`,
`/.ai/05_logs/2026-04-26_aec_bb_shadow_evidence_hash_consistency_validation.md`,
`/006_System-Manifests/aec-mepfs-backbone/api-route-inventory/20260426T093920Z/api-route-inventory-report.json`,
`/006_System-Manifests/aec-mepfs-backbone/parity/20260426T093921Z/api-explorer-parity-report.json`,
`/006_System-Manifests/aec-mepfs-backbone/boundary-audit/20260426T093922Z/shadow-boundary-audit-report.json`,
`/006_System-Manifests/aec-mepfs-backbone/benchmarks/20260426T093923Z/benchmark-report.json`,
and
`/006_System-Manifests/aec-mepfs-backbone/evidence-manifest/20260426T093924Z/shadow-evidence-manifest-report.json`.

Twenty-fifth shadow slice evidence is current for the active AEC-MEPFS Backbone
milestone:
`/.ai/03_plans/AEC-MEPFS-Backbone/twenty-fifth-shadow-evidence-explorer-preview-packet.md`,
`/.ai/05_logs/2026-04-26_aec_bb_shadow_evidence_explorer_preview_validation.md`,
`/006_System-Manifests/aec-mepfs-backbone/api-route-inventory/20260426T095439Z/api-route-inventory-report.json`,
`/006_System-Manifests/aec-mepfs-backbone/parity/20260426T095440Z/api-explorer-parity-report.json`,
`/006_System-Manifests/aec-mepfs-backbone/boundary-audit/20260426T100631Z/shadow-boundary-audit-report.json`,
`/006_System-Manifests/aec-mepfs-backbone/benchmarks/20260426T100632Z/benchmark-report.json`,
and
`/006_System-Manifests/aec-mepfs-backbone/evidence-manifest/20260426T100633Z/shadow-evidence-manifest-report.json`.

Twenty-sixth shadow slice evidence is current for the active AEC-MEPFS
Backbone milestone:
`/.ai/03_plans/AEC-MEPFS-Backbone/twenty-sixth-shadow-contract-reconciliation-packet.md`
and
`/.ai/05_logs/2026-04-26_aec_bb_shadow_contract_reconciliation_validation.md`.

Twenty-seventh shadow slice evidence is current for the active AEC-MEPFS
Backbone milestone:
`/.ai/03_plans/AEC-MEPFS-Backbone/twenty-seventh-shadow-evidence-repo-state-hardening-packet.md`
and
`/.ai/05_logs/2026-04-26_aec_bb_shadow_evidence_repo_state_hardening_validation.md`.

Twenty-eighth shadow slice evidence is current for the active AEC-MEPFS
Backbone milestone:
`/.ai/03_plans/AEC-MEPFS-Backbone/twenty-eighth-shadow-evidence-refresh-packet.md`,
`/.ai/05_logs/2026-04-26_aec_bb_shadow_evidence_refresh_validation.md`,
and
`/006_System-Manifests/aec-mepfs-backbone/evidence-manifest/20260426T105418Z/shadow-evidence-manifest-report.json`.

Twenty-ninth shadow slice evidence is current for the active AEC-MEPFS
Backbone milestone:
`/.ai/03_plans/AEC-MEPFS-Backbone/twenty-ninth-shadow-repo-state-helper-packet.md`
and
`/.ai/05_logs/2026-04-26_aec_bb_shadow_repo_state_helper_validation.md`.

Thirtieth shadow slice evidence is current for the active AEC-MEPFS Backbone
milestone:
`/.ai/03_plans/AEC-MEPFS-Backbone/thirtieth-shadow-evidence-refresh-packet.md`,
`/.ai/05_logs/2026-04-26_aec_bb_shadow_post_helper_evidence_refresh_validation.md`,
and
`/006_System-Manifests/aec-mepfs-backbone/evidence-manifest/20260426T112330Z/shadow-evidence-manifest-report.json`.

Thirty-first shadow slice evidence is current for the active AEC-MEPFS Backbone
milestone:
`/.ai/03_plans/AEC-MEPFS-Backbone/thirty-first-shadow-parity-fixture-hardening-packet.md`,
`/.ai/05_logs/2026-04-26_aec_bb_shadow_parity_fixture_hardening_validation.md`,
and
`/006_System-Manifests/aec-mepfs-backbone/parity/20260426T113000Z/api-explorer-parity-report.json`.

Thirty-second shadow slice evidence is current for the active AEC-MEPFS Backbone
milestone:
`/.ai/03_plans/AEC-MEPFS-Backbone/thirty-second-shadow-evidence-refresh-packet.md`,
`/.ai/05_logs/2026-04-26_aec_bb_shadow_post_parity_evidence_refresh_validation.md`,
and
`/006_System-Manifests/aec-mepfs-backbone/evidence-manifest/20260426T113840Z/shadow-evidence-manifest-report.json`.

Thirty-third shadow slice evidence is current for the active AEC-MEPFS Backbone
milestone:
`/.ai/03_plans/AEC-MEPFS-Backbone/thirty-third-shadow-resolver-qa-expansion-packet.md`,
`/.ai/05_logs/2026-04-26_aec_bb_shadow_resolver_qa_expansion_validation.md`,
and
`/006_System-Manifests/aec-mepfs-backbone/resolver-qa/20260426T115200Z/resolver-qa-report.json`.

Thirty-fourth shadow slice evidence is current for the active AEC-MEPFS
Backbone milestone:
`/.ai/03_plans/AEC-MEPFS-Backbone/thirty-fourth-shadow-evidence-refresh-packet.md`,
`/.ai/05_logs/2026-04-26_aec_bb_shadow_post_resolver_qa_evidence_refresh_validation.md`,
and
`/006_System-Manifests/aec-mepfs-backbone/evidence-manifest/20260426T120350Z/shadow-evidence-manifest-report.json`.

Thirty-fifth shadow slice evidence is current for the active AEC-MEPFS
Backbone milestone:
`/.ai/03_plans/AEC-MEPFS-Backbone/thirty-fifth-shadow-placement-qa-expansion-packet.md`,
`/.ai/05_logs/2026-04-26_aec_bb_shadow_placement_qa_expansion_validation.md`,
and
`/006_System-Manifests/aec-mepfs-backbone/placement-qa/20260426T122042Z/placement-qa-report.json`.

Thirty-sixth shadow slice evidence is current for the active AEC-MEPFS
Backbone milestone:
`/.ai/03_plans/AEC-MEPFS-Backbone/thirty-sixth-shadow-evidence-refresh-packet.md`,
`/.ai/05_logs/2026-04-26_aec_bb_shadow_post_placement_qa_evidence_refresh_validation.md`,
and
`/006_System-Manifests/aec-mepfs-backbone/evidence-manifest/20260426T122733Z/shadow-evidence-manifest-report.json`.

Thirty-seventh shadow slice evidence is current for the active AEC-MEPFS
Backbone milestone:
`/.ai/03_plans/AEC-MEPFS-Backbone/thirty-seventh-shadow-parity-resolver-route-hygiene-packet.md`,
`/.ai/05_logs/2026-04-26_aec_bb_shadow_parity_resolver_route_hygiene_validation.md`,
and
`/006_System-Manifests/aec-mepfs-backbone/parity/20260426T124014Z/api-explorer-parity-report.json`.

Thirty-eighth shadow slice evidence is current for the active AEC-MEPFS
Backbone milestone:
`/.ai/03_plans/AEC-MEPFS-Backbone/thirty-eighth-shadow-evidence-refresh-packet.md`,
`/.ai/05_logs/2026-04-26_aec_bb_shadow_post_parity_resolver_route_evidence_refresh_validation.md`,
and
`/006_System-Manifests/aec-mepfs-backbone/evidence-manifest/20260426T124700Z/shadow-evidence-manifest-report.json`.

Thirty-ninth shadow slice evidence is current for the active AEC-MEPFS
Backbone milestone:
`/.ai/03_plans/AEC-MEPFS-Backbone/thirty-ninth-shadow-benchmark-evidence-hardening-packet.md`
and
`/.ai/05_logs/2026-04-26_aec_bb_shadow_benchmark_evidence_hardening_validation.md`.

Fortieth shadow slice evidence is current for the active AEC-MEPFS Backbone
milestone:
`/.ai/03_plans/AEC-MEPFS-Backbone/fortieth-shadow-evidence-refresh-packet.md`,
`/.ai/05_logs/2026-04-26_aec_bb_shadow_post_benchmark_hardening_evidence_refresh_validation.md`,
and
`/006_System-Manifests/aec-mepfs-backbone/evidence-manifest/20260426T132003Z/shadow-evidence-manifest-report.json`.

Forty-first shadow slice evidence closes the current safe shadow-only/read-only
scope:
`/.ai/03_plans/AEC-MEPFS-Backbone/forty-first-shadow-safe-scope-closure-packet.md`
and
`/.ai/05_logs/2026-04-26_aec_bb_shadow_safe_scope_closure_validation.md`.

## 2. Completed Milestones

| Milestone | Status | Evidence | Notes |
|---|---|---|---|
| Source custody/evidence-prep pipeline through promotion | completed as compatibility infrastructure | `scripts/pipeline_cli.py`, `scripts/vitruvius/promotion_validator.py`, `003_Canonical-Knowledge-Layer/shared/relationships/` | Supports source-derived evidence, provenance, and compatibility beneath KG-first AEC-MEPFS; not the product architecture going forward |
| Live-docs rebase across `.ai/01_roadmap/` and `.ai/03_plans/INDEX.md` | completed | `/.ai/01_roadmap/`, `/.ai/03_plans/INDEX.md`, `/.ai/README.md` | Active operating docs now use repo-verified status language |
| KG-first cleanup Phase 1 live-doc reconciliation | active | `/.ai/03_plans/kg-first-cleanup/` | Reframes legacy layer-centered wording into KG-first/source-custody/evidence-prep language without behavior changes, raw-source writes, or artifact deletion |
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
| Historical transcript demotion | completed | `.ai/09_archive/research/chatgpt-conversations/`, `.ai/chatGPT-Conversations/README.md`, `.ai/03_plans/secondary-cleanup/2026-04-27_chatgpt_transcript_archive_demotion_packet.md` | Transcript contents are archive/reference material; old path is a forwarding pointer only |

## 3. Blocked / Deferred Milestones

| Milestone | Status | Evidence | Blocker / reason | Next concrete action |
|---|---|---|---|---|
| AEC production/live runtime beyond file-backed resolver | hard-blocked beyond implemented local surface | `/.ai/03_plans/AEC-MEPFS-Backbone/2026-04-27_actual_aec_mepfs_implementation_cutover_packet.md`, `/.ai/03_plans/AEC-MEPFS-Backbone/final-aec-mepfs-actual-implementation-closure-packet.md`, `/006_System-Manifests/aec-mepfs-backbone/runtime-thresholds/20260428T004350Z/runtime-threshold-adoption-report.json` | `/v2/resolve*` is now default-on and file-backed with rollback disable behavior, Explorer is AEC-MEPFS-first, and API-local resolver threshold pass/fail evidence exists. Neo4j live graph promotion, primary KG mutation, protected payload admission, external API/server benchmarks, Explorer browser benchmarks, and Neo4j-backed thresholds remain blocked by missing credentials, rollback proof, or external authority. | provide production target credentials plus backup/restore/rollback transcript for live graph promotion, and valid legal/steward/source-rights records before protected payload admission |
| Generic dataset expansion beyond bounded laws-wave | blocked | `.ai/10_state/laws-wave-status.json`, `.ai/03_plans/laws-wave/LAWS_WAVE_RELOAD_PROTOCOL.md` | current truthful state is maintenance/completion, not open expansion | reopen only with new authoritative source or explicit strategy change |
| Skills/agents layer consolidation | duplicate skill-doc cleanup completed; imported/reference packs deferred | `/.ai/skills/`, `/.ai/11_skills/README.md`, `/.ai/12_agents/README.md`, `/.ai/09_archive/skills/legacy-11-skills-duplicates/`, `/.ai/03_plans/secondary-cleanup/2026-04-27_skills_agents_source_of_truth_decision.md` | canonical skill source is now `/.ai/skills/`; imported/reference packs are not blocking core operating surface | optional later rewrite/archive pass for imported packs |

## 4. Milestone Evidence Notes

- Use repository artifacts and run logs as evidence before plan text.
- Treat old tranche-by-tranche and sprint-by-sprint narrative as historical reference only.
- Treat fresh verification claims as **unverified** unless they were rerun after the last implementation change.
