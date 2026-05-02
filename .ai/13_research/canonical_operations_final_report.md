# Canonical Operations Final Report

Date: 2026-05-01 23:15:32 +08:00

## 1. Implementation summary

This loop operationalized canonical graph stewardship without applying production duplicate merges. It added scalable batch review, priority scoring, concrete decision packets, rollback preview/apply, hash-chained transaction manifests, stronger mutation gates, and canonical-search ambiguity metadata.

## 2. Files changed

Primary implementation files:

- pi/graph/canonicalStewardship.ts
- pi/index.ts
- pi/validateCanonicalGraphStewardship.ts
- pi/canonicalGraphStewardship.test.ts
- pi/resourceLayer/transactionManifest.ts
- pi/resourceLayer/reviewWorkflow.ts
- explorer/src/api/graphApi.ts
- explorer/src/api/graphApi.test.ts
- explorer/src/app.searchInspector.integration.test.tsx
- explorer/src/types/index.ts
- explorer/src/components/canonical-review/CanonicalReviewAdmin.tsx
- explorer/src/components/canonical-review/CanonicalReviewAdmin.test.tsx
- docs/knowledge-graph/resource-layer.md
- .ai/10_state/decisions.md

Reports/logs:

- .ai/13_research/dirty_worktree_change_scope_review.md
- .ai/13_research/canonical_operations_loop_progress.md
- .ai/13_research/canonical_operations_final_report.md
- .ai/13_research/concrete_stewardship_decision_packet.md
- .ai/13_research/canonical_batch_review_report.md
- .ai/13_research/canonical_rollback_unmerge_report.md
- .ai/13_research/admin_gate_security_review.md
- .ai/05_logs/2026-05-01_canonical_operations_loop.md

## 3. Dirty worktree/change-scope findings

The worktree remains broad and dirty from multiple prior loops. GitNexus detect-changes still reports critical risk across the whole dirty worktree. This loop-owned changes are documented in .ai/13_research/dirty_worktree_change_scope_review.md. Because the dirty tree is broad, this loop performed no destructive production canonical mutation.

## 4. Baseline canonical operations metrics

From un run api/validateCanonicalGraphStewardship.ts:

- duplicate groups: 544
- unresolved duplicate groups: 544
- groups by risk: high=69, medium=475
- groups by priority: P0=2, P1=66, P2=223, P3=253
- concrete duplicate groups: 2
- batches: 0 production records
- batch decisions: 0 production records
- stewardship decisions: 0
- applied decisions: 0
- aliases: 0
- redirects: 0
- blockers: 0

## 5. Batch review implementation

Added:

- GET /graph/canonical/batches
- POST /graph/canonical/batches
- GET /graph/canonical/batches/:batchId
- POST /graph/canonical/batches/:batchId/preview
- POST /graph/canonical/batches/:batchId/decision
- GET /graph/canonical/priorities
- POST /graph/canonical/groups/:groupId/priority

Allowed batch actions are non-destructive: reviewer assignment, priority/tags, needs-review, keep-separate, and reject-candidate triage. Batch merge is blocked server-side.

## 6. Concrete/Reinforced Concrete decision-packet summary

Detailed packet: .ai/13_research/concrete_stewardship_decision_packet.md.

- VTN-DOM-0000068 and VTN-DOM-0000267 remain P0 unresolved.
- VTN-DOM-0000271 and VTN-DOM-0012147 remain P0 unresolved.
- Kimi recommended keep-separate for both groups, with future governed relationship/disambiguation work rather than merge.
- No destructive merge, alias, redirect, or fake decision was applied.

## 7. Rollback/unmerge implementation

Added rollback routes:

- GET /graph/canonical/decisions/:decisionId/rollback-preview
- POST /graph/canonical/decisions/:decisionId/rollback

Supported:

- Full rollback for metadata-only alias/triage decisions.
- Partial rollback reporting for merge decisions with affected edges/resource links.
- Rollback requires reviewer/rationale and admin gate.

Limitations:

- Full destructive unmerge is not claimed.
- Alias/redirect tombstone history is deferred.
- Partial rollback remediation manifest is deferred.

## 8. Manifest integrity implementation

Canonical and Resource Layer manifests now include:

- transaction id
- subsystem
- operation type
- before/after hashes
- previous manifest hash
- manifest hash
- optional subsystem-scoped HMAC signature via VITRUVIUS_TRANSACTION_HMAC_KEY
- validation status
- rollback capability fields where available

Canonical validation checks manifest hashes, hash chain, and HMAC mismatch when key is configured.

## 9. Admin/mutation gate implementation

Production mutation routes require a valid VITRUVIUS_ADMIN_TOKEN unless local/dev/test conditions apply. Token comparison uses timing-safe comparison. Read-only routes remain available.

## 10. Canonical search changes

/graph/canonical/search now includes unresolved duplicate ambiguity metadata. Search for concrete reports the unresolved P0 duplicate group instead of pretending one canonical node has already been approved.

## 11. Resource Layer compatibility status

Resource Layer validation passes. Resource Layer links are preserved as canonical dry-run and rollback preservation targets. No Resource Layer records were auto-created, auto-linked, or auto-promoted.

## 12. Graph relationship visibility regression status

Graph relationship validation passes. Sendai Mediatheque / Toyo Ito regression remains covered by API tests. Dynamic semantic edge visibility was not regressed.

## 13. Tests added/updated

- Batch review creation/preview/decision tests.
- P0 concrete priority tests.
- Metadata rollback tests.
- Manifest tamper/hash-chain tests.
- Admin mutation gate tests.
- Canonical Review UI batch/priority/rollback/manifest tests.
- Canonical API client route contract tests.

## 14. Commands run and results

- un test api/canonicalGraphStewardship.test.ts - PASS, 14 tests.
- cd api && bun test - PASS, 148 tests.
- cd explorer && bun test - PASS, 111 tests.
- cd explorer && bun run build - PASS; Vite large chunk warning only.
- un run api/validateGraphRelationships.ts - PASS, ok=true.
- un run api/validateResourceLayer.ts - PASS, ok=true, with two existing standard-context warnings.
- un run api/validateCanonicalGraphStewardship.ts - PASS, ok=true.
- ash ./scripts/refresh_code_intelligence.sh - completed; code-review-graph still warns about missing 	ree-sitter-yaml and embedding batch _Task.elapsed errors.
- cmd /c npx --yes gitnexus@1.6.4-rc.32 detect-changes --repo vitruvius - completed; reports critical risk over broad dirty worktree.

## 15. Kimi review summary

### Review 1: Batch strategy

Accepted:
- Non-destructive batch-only policy.
- Rollback/hash-chain manifests as first-class substrate.
- P0 material-scope gating for concrete/reinforced concrete.

Rejected/deferred:
- Law-folder/source-custody comments that were outside this loop's graph-canonical scope.

### Review 2: Concrete decision packets

Accepted:
- Keep concrete and structural-concrete contexts separate.
- Keep reinforced-concrete structural topic and architecture-material concept separate.
- Future governed relationship/disambiguation should connect them rather than merging.

### Review 3: Rollback/unmerge

Accepted:
- Store rollback capability.
- Add schema version to before snapshot.
- Preserve per-decision alias records to reduce later-decision alias-loss risk.

Deferred:
- Alias/redirect tombstones.
- Full destructive unmerge.
- Partial rollback remediation manifests.

### Review 4: Admin gate and manifest security

Accepted:
- Timing-safe token comparison.
- Subsystem-scoped HMAC derivation.
- HMAC over stable payload.

Deferred:
- Socket-origin local gate.
- Failed-auth backoff/audit log.
- Strong advisory lock library.

### Review 5: Final implementation review

Kimi verdict: accepted with minor documentation nits; no blockers. Kimi confirmed the loop safely advances operational canonical stewardship without reckless merges.

## 16. Remaining unresolved duplicate groups

- Total unresolved groups: 544.
- P0 unresolved groups: 2.
- High-risk unresolved groups: 69.

## 17. Remaining gaps

- Human steward decisions are still needed.
- Concrete/reinforced-concrete should likely be keep-separate plus governed cross-domain/specialization relationships, but that has not been applied.
- Full unmerge support for destructive graph rewrites remains future work.
- Production auth, failed-auth audit logging, and rate limiting remain future work.
- Broad dirty worktree still needs commit grouping/review before merge.

## 18. Recommended next loop

1. Steward the two P0 concrete groups using the packet.
2. Add governed disambiguation/cross-domain relationship decisions if approved.
3. Add alias/redirect tombstones and partial-rollback remediation manifests.
4. Add batch triage for P1 groups.
5. Isolate or commit prior-loop dirty worktree groups before production mutations.

## 19. Current git status snapshot

``text
 M .ai/01_roadmap/current-phase.md
 M .ai/01_roadmap/milestone-tracker.md
 M .ai/03_plans/AEC-MEPFS-Backbone/registry-candidates/source-rights-registry.json
 M .ai/03_plans/INDEX.md
 M .ai/10_state/decisions.md
 M .env.example
 M .gitignore
 M .omx/.gitignore
 M .omx/wiki/index.md
 M .omx/wiki/log.md
 M api/explorerPerformance.test.ts
 M api/index.ts
 M api/v2Backbone.test.ts
 M explorer/src/App.tsx
 M explorer/src/api/graphApi.test.ts
 M explorer/src/api/graphApi.ts
 M explorer/src/app.searchInspector.integration.test.tsx
 M explorer/src/components/ExplorerRail.tsx
 M explorer/src/components/HomeScreen.tsx
 M explorer/src/components/componentInteraction.test.tsx
 M explorer/src/components/graph/NodeContextMenu.tsx
 M explorer/src/components/graph/QueryPanel.tsx
 M explorer/src/components/inspector/NodeInspector.tsx
 M explorer/src/stores/useSceneStore.ts
 M explorer/src/types/index.ts
 M scripts/pipeline_cli.py
 M scripts/tests/fixtures/aec_mepfs_backbone/admitted_backbone_nodes_l1_l2.json
 M scripts/tests/fixtures/aec_mepfs_backbone/valid_readiness_s2.json
 M scripts/tests/test_kg_backbone_contracts.py
 M scripts/tests/test_kg_backbone_resolver_qa.py
 M scripts/tests/test_kg_backbone_shadow_staging.py
 M scripts/vitruvius/kg/backbone_shadow_staging.py
?? .ai/02_audits/aec-mepfs-domain-cluster-interrelationships-audit.md
?? .ai/02_audits/architecture-civil-structural-kg-loop-audit.md
?? .ai/02_audits/resource-layer-implementation-audit.md
?? .ai/03_plans/AEC-MEPFS-Backbone/2026-05-01_aec_mepfs_domain_cluster_interrelationships_packet.md
?? .ai/03_plans/AEC-MEPFS-Backbone/2026-05-01_architecture_civil_structural_kg_loop_packet.md
?? .ai/03_plans/resource-layer-implementation-plan.md
?? .ai/04_tasks/aec-mepfs-domain-cluster-interrelationships-trigger.md
?? .ai/05_logs/2026-05-01_acs_external_gate_apply_paths_validation.md
?? .ai/05_logs/2026-05-01_acs_external_gated_gap_scaffold_validation.md
?? .ai/05_logs/2026-05-01_acs_gap_closure_validation.md
?? .ai/05_logs/2026-05-01_acs_remaining_gaps_followup_validation.md
?? .ai/05_logs/2026-05-01_aec_mepfs_domain_cluster_interrelationships_validation.md
?? .ai/05_logs/2026-05-01_architecture_civil_structural_kg_loop_validation.md
?? .ai/05_logs/2026-05-01_canonical_graph_stewardship_loop.md
?? .ai/05_logs/2026-05-01_canonical_operations_loop.md
?? .ai/05_logs/2026-05-01_graph_relationship_visibility_loop.md
?? .ai/05_logs/2026-05-01_resource_layer_review_workflow.md
?? .ai/05_logs/2026-05-01_resource_layer_validation.md
?? .ai/10_state/baselines/aec-mepfs-domain-cluster-interrelationships-baseline.md
?? .ai/13_research/admin_gate_security_review.md
?? .ai/13_research/aec-mepfs-domain-cluster-interrelationships-research.md
?? .ai/13_research/architecture-civil-structural-kg-loop-research.md
?? .ai/13_research/canonical_batch_review_report.md
?? .ai/13_research/canonical_graph_stewardship_decision_log.md
?? .ai/13_research/canonical_graph_stewardship_final_report.md
?? .ai/13_research/canonical_graph_stewardship_loop_progress.md
?? .ai/13_research/canonical_graph_stewardship_validation_report.md
?? .ai/13_research/canonical_operations_loop_progress.md
?? .ai/13_research/canonical_rollback_unmerge_report.md
?? .ai/13_research/concrete_stewardship_decision_packet.md
?? .ai/13_research/dirty_worktree_change_scope_review.md
?? .ai/13_research/graph_duplicate_canonicalization_report.md
?? .ai/13_research/graph_relationship_visibility_final_report.md
?? .ai/13_research/graph_relationship_visibility_loop_progress.md
?? .ai/13_research/resource_layer_final_report.md
?? .ai/13_research/resource_layer_implementation_progress.md
?? .ai/13_research/resource_layer_kimi_final_review.md
?? .ai/13_research/vitruvius_resource_layer_markdown_pack/
?? .omx/context/acs-external-apply-20260501T084523Z.md
?? .omx/context/acs-final-gates-20260501T075556Z.md
?? .omx/context/acs-gap-closure-20260501T060836Z.md
?? .omx/context/acs-hard-blocker-readiness-20260501T094600Z.md
?? .omx/context/acs-remaining-gaps-20260501T071500Z.md
?? .omx/context/aec-relationship-improvement-20260501T141445Z.md
?? .omx/context/architecture-civil-structural-kg-loop-20260501T045108Z.md
?? .omx/context/canonical-graph-stewardship-20260501T133949Z.md
?? .omx/context/canonical-operations-20260501T143709Z.md
?? .omx/context/graph-relationship-visibility-20260501T124231Z.md
?? .omx/context/resource-layer-20260501T102153Z.md
?? .omx/context/resource-layer-review-workflow-20260501T114806Z.md
?? 006_System-Manifests/aec-mepfs-backbone/architecture-civil-structural-enrichment/
?? 006_System-Manifests/aec-mepfs-backbone/architecture-civil-structural-gated-review/
?? 006_System-Manifests/aec-mepfs-backbone/architecture-civil-structural-quality/
?? 006_System-Manifests/aec-mepfs-backbone/domain-cluster-enrichment/
?? 006_System-Manifests/aec-mepfs-backbone/graph-quality/
?? 006_System-Manifests/aec-mepfs-backbone/resolver-qa/20260501T040000Z_DOMAIN_CLUSTER_RESOLVER_QA/
?? 006_System-Manifests/aec-mepfs-backbone/resolver-qa/20260501T054000Z_ACS_RESOLVER_QA/
?? 006_System-Manifests/aec-mepfs-backbone/resolver-qa/20260501T063000Z_ACS_GAP_CLOSURE_RESOLVER_QA/
?? 006_System-Manifests/aec-mepfs-backbone/resolver-qa/20260501T072100Z_ACS_REMAINING_GAPS_RESOLVER_QA/
?? 006_System-Manifests/aec-mepfs-backbone/resolver-qa/20260501T082400Z_ACS_EXTERNAL_GATED_GAP_RESOLVER_QA/
?? 006_System-Manifests/aec-mepfs-backbone/semantic-overlays/20260501T143850Z/
?? 006_System-Manifests/aec-mepfs-backbone/shadow-staging/20260501T040000Z_DOMAIN_CLUSTER_SHADOW/
?? 006_System-Manifests/aec-mepfs-backbone/shadow-staging/20260501T054000Z/
?? 006_System-Manifests/aec-mepfs-backbone/shadow-staging/20260501T062700Z/
?? 006_System-Manifests/aec-mepfs-backbone/shadow-staging/20260501T071900Z/
?? 006_System-Manifests/aec-mepfs-backbone/shadow-staging/20260501T081700Z/
?? 006_System-Manifests/aec-mepfs-backbone/shadow-staging/20260501T082100Z/
?? 006_System-Manifests/resource-layer/
?? api/canonicalGraphStewardship.test.ts
?? api/graph/
?? api/graphRelationshipVisibility.test.ts
?? api/indexLocalResources.ts
?? api/resourceLayer.test.ts
?? api/resourceLayer/
?? api/validateCanonicalGraphStewardship.ts
?? api/validateGraphRelationships.ts
?? api/validateResourceLayer.ts
?? docs/
?? explorer/src/components/canonical-review/
?? explorer/src/components/resource-review/
?? scripts/tests/test_kg_aec_relationship_improvement.py
?? scripts/tests/test_kg_architecture_civil_structural_enrichment.py
?? scripts/tests/test_kg_architecture_civil_structural_gate_review.py
?? scripts/tests/test_kg_backbone_graph_quality.py
?? scripts/tests/test_kg_domain_cluster_enrichment.py
?? scripts/vitruvius/kg/aec_relationship_improvement.py
?? scripts/vitruvius/kg/architecture_civil_structural_enrichment.py
?? scripts/vitruvius/kg/architecture_civil_structural_gate_review.py
?? scripts/vitruvius/kg/architecture_civil_structural_quality.py
?? scripts/vitruvius/kg/backbone_graph_quality.py
?? scripts/vitruvius/kg/domain_cluster_enrichment.py
``
