# Current Phase — AEC-MEPFS Backbone Readiness Gate

**Status:** planned  
**Updated:** 2026-04-26
**Purpose:** single authoritative statement of the current operating phase

## 1. Current Phase

Vitruvius is currently in the **AEC-MEPFS Backbone readiness-gate** phase.

This phase follows the completed control-surface consolidation pass and the
initial AEC-MEPFS Backbone planning packet. The next bounded decision is no
longer "start AEC runtime work"; it is whether the AEC-MEPFS Backbone readiness
gates can be closed well enough to open a later bounded implementation lane.

## 2. Why This Phase Is Current

- shipped capabilities (promotion, graph/query, KG v2, laws-wave closure, explorer, nested AGENTS) already exist in the repo
- active planning docs previously mixed historical narrative with live status
- future work will be misrouted unless the active `.ai` surface points to the
  readiness gates before any implementation, cleanup, or graph cutover begins

Primary evidence:

- `/.ai/AUDIT_REPORT.md`
- `/.ai/IMPLEMENTATION_MATRIX.md`
- `/.ai/03_plans/00-governing-implementation-plan.md`
- `/.ai/03_plans/AEC-MEPFS-Backbone/2026-04-25_aec_mepfs_backbone_readiness_plan.md`

## 3. Current Work Now

### 3.0 Interleaved KG Maintenance Note
- **Status:** completed as bounded maintenance
- **Evidence:** `.ai/05_logs/2026-04-25_concept_centric_relationship_enrichment_validation.md`
- **Outcome:** the existing `001-Laws` KG snapshot was enriched for the Explorer MVP without reopening raw/canonical rebuild scope. This does not change the AEC execution-readiness phase.

### 3.1 Plan-family slimming
- **Status:** completed
- **Evidence:** `/.ai/03_plans/`, `/.ai/archive/ARCHIVE_INDEX.md`
- **Outcome:** the active plan surface now resolves to the dispatcher, `AEC_ENGINE_MASTER_IMPLEMENTATION_PLAN.md`, and the minimal AEC session packet; completed bursts are reference-only.

### 3.2 Reference integrity maintenance
- **Status:** completed
- **Evidence:** `.ai/10_state/laws-wave-status.json`, `.ai/03_plans/laws-wave/LAWS_WAVE_ARTIFACT_INDEX.md`
- **Outcome:** stale `/docs` references, dead artifact links, and invalid active-plan filename references were reconciled in the live docs.

### 3.3 AEC-MEPFS Backbone shadow slices
- **Status:** file-backed shadow staging, read-only consumer/reporting, first additive `/v2` shadow summary route, non-default Explorer shadow preview, bounded `/v2/backbone/taxonomy` detail preview, first admitted `BackboneNode` L1/L2 fixture slice, first sibling shadow graph/parity slice, parity-runner hardening, placement/authoring QA runner, read-only `/v2/backbone/placement-qa` summary route, explicit-action Explorer placement QA preview, parity-relevant Explorer test-hygiene cleanup, shadow report-reader hardening, and read-only `/v2/backbone/node/:id` preview route are implemented; not live-runtime-authorized for primary graph cutover or default Explorer adoption
- **Evidence:** `/.ai/03_plans/AEC-MEPFS-Backbone/`, `/.ai/03_plans/AEC-MEPFS-Backbone/readiness-closure-scorecard.md`, `/.ai/03_plans/AEC-MEPFS-Backbone/eighth-readiness-runtime-priming-packet.md`, `/.ai/03_plans/AEC-MEPFS-Backbone/first-shadow-only-implementation-packet.md`, `/.ai/03_plans/AEC-MEPFS-Backbone/second-shadow-readonly-consumer-reporting-packet.md`, `/.ai/03_plans/AEC-MEPFS-Backbone/third-shadow-v2-backbone-route-implementation-packet.md`, `/.ai/03_plans/AEC-MEPFS-Backbone/fourth-shadow-explorer-preview-implementation-packet.md`, `/.ai/03_plans/AEC-MEPFS-Backbone/fifth-shadow-taxonomy-preview-implementation-packet.md`, `/.ai/03_plans/AEC-MEPFS-Backbone/sixth-shadow-backbone-node-fixture-implementation-packet.md`, `/.ai/03_plans/AEC-MEPFS-Backbone/seventh-shadow-graph-parity-implementation-packet.md`, `/.ai/03_plans/AEC-MEPFS-Backbone/eighth-shadow-parity-runner-hardening-implementation-packet.md`, `/.ai/03_plans/AEC-MEPFS-Backbone/ninth-shadow-placement-qa-implementation-packet.md`, `/.ai/03_plans/AEC-MEPFS-Backbone/tenth-shadow-placement-qa-v2-route-implementation-packet.md`, `/.ai/03_plans/AEC-MEPFS-Backbone/eleventh-shadow-placement-qa-explorer-preview-implementation-packet.md`, `/.ai/03_plans/AEC-MEPFS-Backbone/twelfth-shadow-explorer-test-hygiene-packet.md`, `/.ai/03_plans/AEC-MEPFS-Backbone/thirteenth-shadow-report-reader-hardening-packet.md`, `/.ai/03_plans/AEC-MEPFS-Backbone/fourteenth-shadow-node-preview-route-implementation-packet.md`, `/.ai/03_plans/AEC-MEPFS-Backbone/first-slice-backbone-model-spec.md`, `/.ai/05_logs/2026-04-25_aec_bb_s8_runtime_priming_validation.md`, `/.ai/05_logs/2026-04-26_aec_bb_shadow_v2_backbone_route_validation.md`, `/.ai/05_logs/2026-04-26_aec_bb_explorer_preview_validation.md`, `/.ai/05_logs/2026-04-26_aec_bb_shadow_taxonomy_preview_validation.md`, `/.ai/05_logs/2026-04-26_aec_bb_shadow_backbone_node_fixture_validation.md`, `/.ai/05_logs/2026-04-26_aec_bb_shadow_parity_runner_hardening_validation.md`, `/.ai/05_logs/2026-04-26_aec_bb_shadow_placement_qa_validation.md`, `/.ai/05_logs/2026-04-26_aec_bb_shadow_placement_qa_v2_route_validation.md`, `/.ai/05_logs/2026-04-26_aec_bb_shadow_placement_qa_explorer_preview_validation.md`, `/.ai/05_logs/2026-04-26_aec_bb_shadow_explorer_test_hygiene_validation.md`, `/.ai/05_logs/2026-04-26_aec_bb_shadow_report_reader_hardening_validation.md`, `/.ai/05_logs/2026-04-26_aec_bb_shadow_node_preview_route_validation.md`, `/006_System-Manifests/aec-mepfs-backbone/shadow-staging/20260426T003710Z/shadow-staging-report.json`, `/006_System-Manifests/aec-mepfs-backbone/shadow-staging/20260426T003710Z/shadow-staging-consumer-report.json`, `/006_System-Manifests/aec-mepfs-backbone/shadow-staging/20260426T003710Z/shadow-backbone-graph.json`, `/006_System-Manifests/aec-mepfs-backbone/parity/20260426T041305Z/api-explorer-parity-report.json`, `/006_System-Manifests/aec-mepfs-backbone/placement-qa/20260426T015915Z/placement-qa-report.json`
- **Next concrete action:** choose the next bounded shadow slice only after fresh impact review, with priority on file-backed QA/evidence hardening or another non-default `/v2` preview surface over any runtime cutover.

## 4. Success Criteria

This phase will be done when all of the following are true:

1. The active planning surface stays compact and contradiction-free while the AEC-MEPFS Backbone readiness gate is resolved.
2. The AEC-MEPFS Backbone readiness scorecard is evidence-backed and remains aligned to the first shadow-only implementation boundary.
3. `ACTIVE_WORK.md`, `STRATEGIC_NEXT_MOVE.md`, `master-roadmap.md`, and `milestone-tracker.md` agree that the readiness gate is the next AEC step.
4. No AEC runtime work, Neo4j cleanup, feature-flag cutover, graph rebuild, or backup test run is implied to be active before readiness gates are satisfied.

## 5. Blockers / Dependencies

### AEC next shadow API slice
- **Status:** partially advanced
- **Why:** `GET /v2/backbone/taxonomy` now exposes sanitized registry metadata, the first admitted BackboneNode L1/L2 fixture, and sibling shadow graph counts/edges; `GET /v2/backbone/placement-qa` exposes a compact placement QA summary; Explorer can load placement QA only through an explicit preview action; the parity runner now requires both preview surfaces and their opt-in isolation. Runtime registry admission is still not available.
- **Dependency:** fresh GitNexus impact/status on exact files, route-shape or component tests, and strict preservation of no-ingest/no-live-graph/no-default-Explorer-cutover boundaries.

### Fresh verification for some historical claims
- **Status:** unverified
- **Why:** claims like full-suite pass counts are log-backed, not re-run in this phase.
- **Dependency:** rerun verification when the implementation surface changes.

## 6. Nested AGENTS Resolution

Nested AGENTS governance is **completed**, not pending.

Evidence:

- `**/AGENTS.md`
- `/.ai/05_logs/2026-04-20_nested-agents-governance-validation.md`

The corresponding plan is now historical/reference material and must not be treated as a live pending lane.

## 7. Next Review Trigger

Review this phase again when either of these happens:

- the AEC-MEPFS Backbone readiness scorecard changes status
- the live control surface drifts again and needs another bounded cleanup pass
