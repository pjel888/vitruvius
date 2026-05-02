# Architecture Civil Structural KG Progress

Date: 2026-05-01

## Loop status
Completed the Ralph/UltraWork/UltraQA Architecture, Civil Engineering, and Structural Engineering gap-closure loop for the safe file-backed Backbone surface. Production Neo4j mutation, KG rebuild/reset, and protected source payload admission remain blocked.

## Implemented batches
1. Repository and state discovery: graph fixture, source-rights registry, resolver fixture, validation scripts, API shadow consumers, Explorer graph contracts, and generated manifests were rechecked.
2. Parallel review: repository/cartography, graph-hygiene, API metadata, and ACS gap candidates were reviewed through subagents. Kimi CLI was attempted for external critique, but it did not return a usable final response before its step limit.
3. ACS enrichment: added 2 additional source-backed ACS nodes for Subsurface Utility Conflict Review and Design Flood Elevation Interface, plus 11 typed mechanism relationships and 3 resolver cases for utility conflicts, flood-elevation coordination, and slope-stability traversal.
4. Graph hygiene: removed 11 historical self-loop relationships and upgraded graph-quality reporting with duplicate-label samples, same-parent duplicate checks, global self-loop blocking, introduced non-hierarchy orphan detection, and generic `predicate` or `edge_type` counting.
5. API metadata: implemented an allowlisted edge-metadata path for taxonomy/node/explorer detail surfaces while preserving compact render payloads and excluding raw source paths, URLs, and quoted payload fields.
6. Validation: refreshed shadow staging, graph quality, ACS quality score, resolver QA, API tests, and Python tests after the gap closure.

## Current metrics after gap closure
- Backbone nodes: 10,006.
- Governed relationships: 13,610.
- Source-rights rows: 123.
- Resolver golden cases: 135.
- ACS introduced nodes: 67.
- ACS typed non-hierarchy relationships: 95.
- ACS hierarchy relationships: 67.
- Global self-loops: 0 after cleanup.
- Generic relationships: 0.
- Introduced non-hierarchy orphans: 0.

## Key run artifacts
- Gap closure enrichment before self-loop cleanup: `006_System-Manifests/aec-mepfs-backbone/architecture-civil-structural-enrichment/20260501T062000Z_ACS_GAP_CLOSURE/architecture-civil-structural-enrichment-report.json`
- Post-cleanup idempotence report: `006_System-Manifests/aec-mepfs-backbone/architecture-civil-structural-enrichment/20260501T064500Z_ACS_GAP_CLOSURE_POST_CLEANUP/architecture-civil-structural-enrichment-report.json`
- Graph quality: `006_System-Manifests/aec-mepfs-backbone/graph-quality/20260501T062500Z_ACS_GAP_CLOSURE_GRAPH_QUALITY/graph-quality-report.json`
- Shadow staging: `006_System-Manifests/aec-mepfs-backbone/shadow-staging/20260501T062700Z/shadow-staging-consumer-report.json`
- ACS score: `006_System-Manifests/aec-mepfs-backbone/architecture-civil-structural-quality/20260501T062900Z_ACS_GAP_CLOSURE_QUALITY_FINAL/architecture-civil-structural-quality-report.json`
- Resolver QA: `006_System-Manifests/aec-mepfs-backbone/resolver-qa/20260501T063000Z_ACS_GAP_CLOSURE_RESOLVER_QA/resolver-qa-report.json`

## Review decisions
Accepted: close the deferred API edge-metadata gap through an allowlist, close historical self-loop hygiene now that graph-quality blocks them globally, add utility-conflict/flood-elevation/slope-stability ACS paths, and keep duplicate normalized label cleanup as a steward-reviewed future merge/alias pass.

Rejected or deferred: explicit inverse-edge inflation, numerical load or flood criteria, jurisdiction-specific code adoption claims, live Neo4j promotion, protected source admission, and broad utility/network expansion outside the Architecture-Civil-Structural scope.

## Remaining-gap follow-up pass
Date: 2026-05-01

Implemented the requested non-critical remaining gaps as a second safe file-backed pass:

1. Added 8 source-backed ACS nodes for subsurface utility data quality, test-hole utility verification, pavement subgrade/structure interfaces, curb-ramp geometry, emergency-access geometry, stormwater maintenance access, and civil asset handover.
2. Added 27 new mechanism-based ACS relationships covering SUE uncertainty, pavement/subgrade/drainage/access, curb-ramp runoff/accessibility, stormwater maintenance, civil as-built/asset-register handoff, AHJ adoption gates, and non-numeric structural load-basis gates.
3. Added explicit edge metadata fields `applicability_basis`, `jurisdiction_context`, and `design_basis_status` to admitted ACS relationships and preserved them through shadow staging/API allowlists.
4. Implemented a non-destructive duplicate-label context index instead of renaming canonical labels. Same-parent duplicates remain validation errors; all 514 global duplicate groups are now classified as contextual duplicates with path/parent display hints.
5. Added resolver cases `RES-ACS-012` through `RES-ACS-015` and expanded traversal gates for SUE-to-footing, pavement-to-emergency-access, curb-ramp-to-accessible-route, stormwater-maintenance-to-handover, and AHJ-to-load-basis paths.
6. Closed architect-review blockers by adding the new applicability metadata fields to the `BackboneShadowGraphPreview` Explorer contract and by validating staged governed predicates against the staged predicate registry during shadow graph generation.

## Current metrics after remaining-gap follow-up
- Backbone nodes: 10,014.
- Governed relationships: 13,645.
- Source-rights rows: 123.
- Resolver golden cases: 139.
- ACS introduced nodes: 75.
- ACS typed non-hierarchy relationships: 122.
- ACS hierarchy relationships: 75.
- Global self-loops: 0.
- Generic relationships: 0.
- Introduced non-hierarchy orphans: 0.
- Duplicate normalized labels: 514 groups / 1,377 nodes / 863 excess labels; all are cross-parent or cross-root contextual duplicates, same-parent duplicates remain 0.

## Remaining-gap follow-up artifacts
- Enrichment: `006_System-Manifests/aec-mepfs-backbone/architecture-civil-structural-enrichment/20260501T071500Z_ACS_REMAINING_GAPS/architecture-civil-structural-enrichment-report.json`
- Predicate/key cleanup idempotence: `006_System-Manifests/aec-mepfs-backbone/architecture-civil-structural-enrichment/20260501T072200Z_ACS_REMAINING_GAPS_KEY_FIX/architecture-civil-structural-enrichment-report.json`
- Graph quality and duplicate context index: `006_System-Manifests/aec-mepfs-backbone/graph-quality/20260501T072300Z_ACS_REMAINING_GAPS_GRAPH_QUALITY/graph-quality-report.json`
- ACS quality score: `006_System-Manifests/aec-mepfs-backbone/architecture-civil-structural-quality/20260501T072400Z_ACS_REMAINING_GAPS_QUALITY/architecture-civil-structural-quality-report.json`
- Shadow staging: `006_System-Manifests/aec-mepfs-backbone/shadow-staging/20260501T071900Z/shadow-staging-consumer-report.json`
- Resolver QA: `006_System-Manifests/aec-mepfs-backbone/resolver-qa/20260501T072100Z_ACS_REMAINING_GAPS_RESOLVER_QA/resolver-qa-report.json`

## Post-review hardening
- Added a frontend contract test that type-consumes `applicabilityBasis`, `jurisdictionContext`, and `designBasisStatus` on shadow graph preview edges.
- Added a shadow-staging negative test that rejects a governed relationship predicate absent from the staged predicate registry.
- Revalidated Python KG tests, API tests, and Explorer tests after the blocker fixes.

## External-gated follow-up pass
Date: 2026-05-01

Implemented the requested non-critical and externally gated remaining-gap work that can be closed safely in the repository without crossing authority gates:

1. Added 4 source-backed ACS nodes: Accessible Public-Way Crossing Tie-In, Culvert Drainage Interface, Pavement Subgrade Interface, and Structural Criteria Basis Gate.
2. Added 21 additional mechanism-based non-hierarchy ACS relationships plus 4 hierarchy relationships for public-way accessibility tie-ins, culvert hydrology/overflow/flood-scour reasoning, pavement/subgrade/utility-restoration interfaces, AHJ rainfall/load-basis gates, structural criteria basis gating, and civil/structural O&M inspection paths.
3. Added resolver cases `RES-ACS-016` through `RES-ACS-018` for public-way crossing, culvert/flood-scour, and structural criteria-basis traversal.
4. Added `architecture_civil_structural_gate_review.py` as a non-destructive gate-review runner for duplicate-label steward review, numeric criteria packet preflight, external authority ledger preflight, protected/numeric payload-key leak audit, and live-promotion dry-run blocking.
5. Added gated-review tests proving no canonical label mutation, no numeric criteria admission, no protected payload leakage, no live promotion, and no raw-source output writes.
6. Attempted Kimi review again. The CLI either returned no review, hit a step limit, or lost the queued prompt; peer subagent review was used instead and Kimi remains externally/tooling gated.

## Current metrics after external-gated follow-up
- Backbone nodes: 10,018.
- Governed relationships: 13,670.
- Source-rights rows: 123.
- Resolver golden cases: 142.
- ACS introduced nodes: 79.
- ACS typed non-hierarchy relationships: 143.
- ACS hierarchy relationships: 79.
- Global self-loops: 0.
- Generic relationships: 0.
- Introduced non-hierarchy orphans: 0.
- Duplicate normalized labels: 514 groups / 1,377 nodes / 863 excess labels; same-parent duplicates remain 0 and all merge/alias changes remain steward-gated.

## External-gated follow-up artifacts
- Enrichment idempotence: `006_System-Manifests/aec-mepfs-backbone/architecture-civil-structural-enrichment/20260501T082000Z_ACS_EXTERNAL_GATED_GAP_SCAFFOLD_FIX/architecture-civil-structural-enrichment-report.json`
- Shadow staging: `006_System-Manifests/aec-mepfs-backbone/shadow-staging/20260501T082100Z/shadow-staging-report.json`
- Graph quality and duplicate context index: `006_System-Manifests/aec-mepfs-backbone/graph-quality/20260501T082200Z_ACS_EXTERNAL_GATED_GAP_GRAPH_QUALITY/graph-quality-report.json`
- ACS quality score: `006_System-Manifests/aec-mepfs-backbone/architecture-civil-structural-quality/20260501T082300Z_ACS_EXTERNAL_GATED_GAP_QUALITY/architecture-civil-structural-quality-report.json`
- Resolver QA: `006_System-Manifests/aec-mepfs-backbone/resolver-qa/20260501T082400Z_ACS_EXTERNAL_GATED_GAP_RESOLVER_QA/resolver-qa-report.json`
- Gated review: `006_System-Manifests/aec-mepfs-backbone/architecture-civil-structural-gated-review/20260501T083500Z_ACS_GATED_REVIEW_HARDENED/architecture-civil-structural-gated-review-report.json`
- Duplicate steward candidates: `006_System-Manifests/aec-mepfs-backbone/architecture-civil-structural-gated-review/20260501T083500Z_ACS_GATED_REVIEW_HARDENED/duplicate-merge-review-candidates.json`


## External-gate apply-path follow-up
Date: 2026-05-01

Implemented the remaining repo-actionable external-gate work as dry-run/preflight capability rather than fabricated admission:

1. Added steward duplicate decision packet validation and a generated `steward-duplicate-apply-plan-dry-run.json` artifact. The apply plan lists intended actions but keeps canonical label mutation, alias application, migration writes, and auto-merge false.
2. Added protected payload manifest preflight for hash-only/source-rights metadata. Protected payload text, quotes, standard text, table text, raw-source paths, formulas, secrets, token/password fields, and numeric/design-payload keys remain rejected.
3. Expanded live-promotion preflight to require a production promotion plan with backup, restore-test, and rollback evidence paths in addition to credential names. The runner reports missing credential names only and performs no Neo4j connection or write.
4. Added CLI flags for all external packet inputs: `--steward-decision-packet`, `--criteria-packet`, `--authority-ledger`, `--protected-payload-manifest`, `--live-promotion-plan`, and `--rollback-proof`.
5. Added packet path-escape tests and report schema persistence tests so packet inputs cannot escape the repo root and generated reports retain all gate sections.
6. Added packet template documentation at `docs/knowledge-graph/architecture-civil-structural-external-gate-packet-templates.md`.

## External-gate apply-path artifacts
- Gated review and duplicate candidates: `006_System-Manifests/aec-mepfs-backbone/architecture-civil-structural-gated-review/20260501T090200Z_ACS_EXTERNAL_GATE_APPLY_PATHS_DRY_RUN/architecture-civil-structural-gated-review-report.json`
- Steward duplicate dry-run apply plan: `006_System-Manifests/aec-mepfs-backbone/architecture-civil-structural-gated-review/20260501T090200Z_ACS_EXTERNAL_GATE_APPLY_PATHS_DRY_RUN/steward-duplicate-apply-plan-dry-run.json`
- Packet templates: `docs/knowledge-graph/architecture-civil-structural-external-gate-packet-templates.md`

## Hard-blocker readiness automation follow-up
Date: 2026-05-01

Implemented the maximum safe autonomous hard-blocker assistance without fabricating external facts:

1. Added always-generated draft skeletons for steward duplicate preservation, project/AHJ criteria packets, authority ledgers, protected payload manifests, and live-promotion plans.
2. Added `external-gate-readiness-bundle.json` to aggregate current gate statuses, skeleton paths, missing inputs, and operations explicitly not performed.
3. Added root `.env.local` and `.env.*.local` ignore rules and blank production Neo4j credential names to `.env.example`.
4. Preserved all hard safety boundaries: no canonical label mutation, no alias application, no migration write, no numeric criteria admission, no protected payload ingest/exposure, no live Neo4j write, and no production promotion.

## Hard-blocker readiness artifacts
- Gated review: `006_System-Manifests/aec-mepfs-backbone/architecture-civil-structural-gated-review/20260501T094300Z_ACS_EXTERNAL_GATE_READINESS_BUNDLE/architecture-civil-structural-gated-review-report.json`
- Readiness bundle: `006_System-Manifests/aec-mepfs-backbone/architecture-civil-structural-gated-review/20260501T094300Z_ACS_EXTERNAL_GATE_READINESS_BUNDLE/external-gate-readiness-bundle.json`
- Steward skeleton: `006_System-Manifests/aec-mepfs-backbone/architecture-civil-structural-gated-review/20260501T094300Z_ACS_EXTERNAL_GATE_READINESS_BUNDLE/steward-preserve-packet-skeleton.json`
- Criteria skeleton: `006_System-Manifests/aec-mepfs-backbone/architecture-civil-structural-gated-review/20260501T094300Z_ACS_EXTERNAL_GATE_READINESS_BUNDLE/criteria-packet-skeleton.json`
- Authority skeleton: `006_System-Manifests/aec-mepfs-backbone/architecture-civil-structural-gated-review/20260501T094300Z_ACS_EXTERNAL_GATE_READINESS_BUNDLE/authority-ledger-skeleton.json`
- Protected payload skeleton: `006_System-Manifests/aec-mepfs-backbone/architecture-civil-structural-gated-review/20260501T094300Z_ACS_EXTERNAL_GATE_READINESS_BUNDLE/protected-payload-manifest-skeleton.json`
- Live-promotion skeleton: `006_System-Manifests/aec-mepfs-backbone/architecture-civil-structural-gated-review/20260501T094300Z_ACS_EXTERNAL_GATE_READINESS_BUNDLE/live-promotion-plan-skeleton.json`
