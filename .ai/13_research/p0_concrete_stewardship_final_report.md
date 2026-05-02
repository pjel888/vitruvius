# P0 Concrete Stewardship Final Report

Date: 2026-05-01

## 1. Implementation summary

This loop made the two P0 concrete duplicate groups more truthful and operationally reviewable without applying unsafe canonicalization. It added governed disambiguation decision support, proposed-only relationship proposals, search/UI ambiguity metadata, alias/redirect/tombstone validation hardening, rollback remediation manifests, and a non-destructive P1 triage batch.

No production concrete or reinforced-concrete merge was applied.

## 2. Files changed

Core implementation:
- `api/graph/canonicalStewardship.ts`
- `api/index.ts`
- `api/validateCanonicalGraphStewardship.ts`
- `api/canonicalGraphStewardship.test.ts`

Explorer:
- `explorer/src/api/graphApi.ts`
- `explorer/src/api/graphApi.test.ts`
- `explorer/src/types/index.ts`
- `explorer/src/components/canonical-review/CanonicalReviewAdmin.tsx`
- `explorer/src/components/canonical-review/CanonicalReviewAdmin.test.tsx`
- `explorer/src/components/command-bar/SearchCombobox.tsx`
- `explorer/src/app.searchInspector.integration.test.tsx`

Canonical manifests:
- `006_System-Manifests/graph-canonical/stewardship-decisions.json`
- `006_System-Manifests/graph-canonical/batches.json`
- `006_System-Manifests/graph-canonical/transaction-manifests/`

Reports:
- `.ai/13_research/p0_concrete_stewardship_loop_progress.md`
- `.ai/13_research/p0_concrete_stewardship_final_report.md`
- `.ai/13_research/concrete_stewardship_decision_packet.md`
- `.ai/13_research/concrete_governed_disambiguation_report.md`
- `.ai/13_research/concrete_relationship_enrichment_report.md`
- `.ai/13_research/alias_redirect_tombstone_report.md`
- `.ai/13_research/rollback_remediation_manifest_report.md`
- `.ai/13_research/p1_batch_triage_report.md`
- `.ai/05_logs/2026-05-01_p0_concrete_stewardship_loop.md`
- `.ai/10_state/decisions.md`

## 3. Current-state and dirty-worktree findings

The worktree remains broadly dirty from prior loops and unrelated AEC-MEPFS enrichment work. This loop avoided destructive production data mutation and touched only canonical stewardship/API/UI/test/reporting surfaces. A final GitNexus change-scope pass is recorded separately if available; broad dirty scope should remain visible before any commit grouping.

## 4. Concrete group analysis

- Nodes: `VTN-DOM-0000068`, `VTN-DOM-0000267`.
- Decision/status: `DISAMBIGUATED_KEEP_SEPARATE`, `proposed`.
- Merge: not applied.
- Alias/redirect/tombstone: none.
- Rationale: broad materials topic vs structural-material subtopic.
- Kimi critique: keep separate; use governed disambiguation and structural-to-material specialization proposal; do not merge or alias.
- Edges/resources/search impact: production edges/resources unchanged; search now shows disambiguation labels and P0 pending-review metadata.

## 5. Reinforced concrete group analysis

- Nodes: `VTN-DOM-0000271`, `VTN-DOM-0012147`.
- Decision/status: `CROSS_DOMAIN_EQUIVALENCE`, `proposed`.
- Merge: not applied.
- Alias/redirect/tombstone: none.
- Rationale: structural-system subtopic vs architecture/material concept with dense semantic neighborhood.
- Kimi critique: cross-domain aligned concepts, not true duplicates; do not merge or migrate edges.
- Edges/resources/search impact: production edges/resources unchanged; search now shows disambiguation labels and P0 pending-review metadata.

## 6. Governed disambiguation decisions applied or proposed

Two proposed-only decisions were recorded:

- `canonical-20260501155958-e011dc288980`: concrete `DISAMBIGUATED_KEEP_SEPARATE`.
- `canonical-20260501155958-f8da3711275f`: reinforced concrete `CROSS_DOMAIN_EQUIVALENCE`.

They are intentionally not applied as human-steward-approved resolutions; validation still reports P0 unresolved count 2.

## 7. New or updated relationships

No production graph relationships were added. Three stewardship relationship proposals were recorded inside decision metadata:

- `VTN-DOM-0000267 RELATED_SPECIALIZATION_OF VTN-DOM-0000068`.
- `VTN-DOM-0000271 CROSS_DOMAIN_EQUIVALENT VTN-DOM-0012147`.
- `VTN-DOM-0012147 CROSS_DOMAIN_EQUIVALENT VTN-DOM-0000271`.

These are proposals only, not learner graph edges.

## 8. Alias/redirect/tombstone changes

No production alias, redirect, or tombstone records were created. Validation support was hardened for cycles, missing targets, duplicate exact alias records, tombstone policy violations, rejected/deprecated alias handling, and redirect/alias conflicts.

## 9. Rollback remediation manifest changes

Added remediation manifest model/API/UI/validation for partial rollback cases. Current production manifest count is 0 because no partial rollback was applied.

## 10. Search behavior changes

Canonical search now surfaces proposed disambiguation metadata, P0 status, review state, resource link counts, and relationship summaries for concrete ambiguity. General Explorer `/search` was constrained so proposed decisions do not globally rerank unrelated learner searches.

## 11. Graph UI/inspector behavior changes

`/dev/canonical-review` now shows remediation manifests and existing stewardship status. Search combobox results display disambiguation text and P0/pending-review badges. The learner graph canvas remains production-edge-only; proposed relationships are not rendered as admitted graph edges.

## 12. Resource Layer preservation status

Resource Layer data was not mutated. Resource validation passed with existing standards-context warnings and no blockers. `nodeResourceLinks` remained 9.

## 13. P1 batch triage summary

Created one open non-destructive P1 triage batch with 20 groups and no decisions. It assigns tags only and blocks destructive batch actions.

## 14. Tests added/updated

- Governed disambiguation preview/record tests.
- Concrete canonical search ambiguity tests.
- Alias/redirect/tombstone validation tests.
- Partial rollback remediation manifest tests.
- Explorer canonical review remediation route/UI tests.
- Search integration mock updated for remediation exports.

## 15. Validation scripts updated

`api/validateCanonicalGraphStewardship.ts` now reports disambiguation decision counts, stewardship edge proposals, tombstones, open remediation manifests, and partial rollback remediation gaps.

## 16. Commands run

- `bun test` in `api`.
- `bun test` in `explorer`.
- `bun run build` in `explorer`.
- `bun run api/validateGraphRelationships.ts`.
- `bun run api/validateResourceLayer.ts`.
- `bun run api/validateCanonicalGraphStewardship.ts`.

## 17. Test/build/validation results

- API tests: 152 pass, 0 fail.
- Explorer tests: 111 pass, 0 fail.
- Explorer build: pass, chunk-size warning only.
- Graph relationship validation: ok true, issueCount 0.
- Resource Layer validation: ok true, blockers 0, existing standards warnings 2.
- Canonical stewardship validation: ok true, blockers 0, warnings 0, transactionManifests 3, graphStewardshipEdgeProposals 3.

## 18. Kimi review summary

1. Concrete ontology: accepted keep-separate plus proposed specialization; rejected merge/alias.
2. Reinforced concrete ontology: accepted cross-domain alignment; rejected merge/retype/edge migration.
3. Disambiguation relationships: accepted proposed-only relationship metadata; warned that cross-domain equivalence must not imply identity.
4. Alias/redirect/tombstone/remediation: accepted cycle/missing-target/status validation hardening; deferred stronger waiver and resource-rewrite policy.
5. Final review: no blocking safety concern; emphasized final language must say proposed-only advancement, not P0 resolution.

## 19. Remaining unresolved groups

- Total unresolved duplicate groups: 544.
- P0 unresolved duplicate groups: 2.
- High-risk unapplied candidates: 69.

This is expected because no fake approval or destructive production merge was applied.

## 20. Remaining gaps

- Human steward approval is still required for P0 decisions.
- `CROSS_DOMAIN_EQUIVALENT` should be vocabulary-reviewed before production edge admission.
- Proposed stewardship relationships need a policy gate before learner-graph rendering.
- P1 triage needs decision packets and domain review.
- Broad dirty worktree still needs commit/change-scope management.

## 21. Recommended next loop

Run a steward-facing P0 approval loop that reviews the proposed concrete decisions, chooses final relation vocabulary, and either applies disambiguated keep-separate decisions or leaves them in human review with explicit rationale. Do not proceed to P1 destructive actions until P0 approval/rejection semantics are settled.

## Post-implementation code-intelligence checks

- `bash ./scripts/refresh_code_intelligence.sh`: exit 0. GitNexus already up to date; ChunkHound processed changed files; code-review-graph rebuilt. Known tool warnings persisted: missing `tree-sitter-yaml` for YAML parsing and code-review-graph embedding batch `_Task.elapsed` errors.
- `cmd /c npx --yes gitnexus@1.6.4-rc.32 detect-changes --repo vitruvius`: exit 0 but reported `Risk level: critical` over 33 files / 219 symbols / 23 flows because the repository has a broad pre-existing dirty worktree. This is not treated as a signal that P0 merge is safe; it reinforces the non-destructive posture.
- `tool_search` did not expose a code-review-graph `detect_changes` callable in this session; no separate MCP detect-changes run was available.
- `chunkhound search --regex "DISAMBIGUATED_KEEP_SEPARATE|CROSS_DOMAIN_EQUIVALENT|remediation"` initially failed on Windows cp1252 output, then passed with `PYTHONIOENCODING=utf-8` / `PYTHONUTF8=1`.
