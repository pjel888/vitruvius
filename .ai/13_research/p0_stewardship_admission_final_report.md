# P0 Stewardship Admission Final Report

Date: 2026-05-02

## 1. Implementation summary

This loop added a governed admission layer between proposed canonical stewardship decisions and any applied/admitted production graph effect. P0 Concrete and Reinforced Concrete remain unmerged and unresolved because no real steward approval record was provided. The system now prevents proposed disambiguation decisions from being directly applied, requires approval metadata before admission, normalizes the over-strong `CROSS_DOMAIN_EQUIVALENT` proposal to `CROSS_DOMAIN_ALIGNMENT` for future admission, supports admitted relationship overlays, keeps graph cache sensitive to admitted relationship changes, and generates non-destructive P1 decision packets.

No fake human approval was created. No production P0 learner graph edge was admitted. No aliases, redirects, tombstones, node merges, Resource Layer rewrites, or fake resources were created.

## 2. Files changed

Primary implementation:
- `api/graph/canonicalStewardship.ts`
- `api/index.ts`
- `explorer/src/api/graphApi.ts`
- `explorer/src/types/index.ts`
- `explorer/src/components/canonical-review/CanonicalReviewAdmin.tsx`
- `explorer/src/components/inspector/NodeInspector.tsx`

Tests:
- `api/canonicalGraphStewardship.test.ts`
- `explorer/src/api/graphApi.test.ts`
- `explorer/src/components/canonical-review/CanonicalReviewAdmin.test.tsx`
- `explorer/src/app.searchInspector.integration.test.tsx`

Data/review artifacts:
- `006_System-Manifests/graph-canonical/p1-decision-packets.json`
- `006_System-Manifests/graph-canonical/transaction-manifests/*`

Reports/logs:
- `.ai/13_research/p0_stewardship_admission_loop_progress.md`
- `.ai/13_research/p0_stewardship_admission_final_report.md`
- `.ai/13_research/cross_domain_relationship_naming_report.md`
- `.ai/13_research/p0_admitted_relationships_report.md`
- `.ai/13_research/steward_approval_gate_report.md`
- `.ai/13_research/stewardship_rollback_replay_drill_report.md`
- `.ai/13_research/p1_decision_packet_generation_report.md`
- `.ai/05_logs/2026-05-02_p0_stewardship_admission_loop.md`
- `.ai/10_state/decisions.md`

## 3. Dirty-worktree/current-state findings

The repository remains broadly dirty from prior loops and unrelated work. GitNexus still reports critical risk across 34 changed files and 224 symbols. This loop therefore avoided destructive production graph mutation and limited persistent data writes to non-destructive P1 packet artifacts plus reports.

Code intelligence refresh completed after implementation. The refresh had known tooling warnings: missing `tree-sitter-yaml` for YAML parsing and a code-review-graph embedding-service `_Task.elapsed` warning. GitNexus `detect-changes` completed through `cmd /c npx ...` after PowerShell blocked `npx.ps1` execution; risk remained critical due the broad dirty worktree.

## 4. P0 proposed-decision loading results

### Concrete

- Nodes: `VTN-DOM-0000068`, `VTN-DOM-0000267`
- Group: `dup-0aa1351d9475`
- Decision ID: `canonical-20260501155958-e011dc288980`
- Decision type: `DISAMBIGUATED_KEEP_SEPARATE`
- Status: `proposed`
- Proposed relationship: `VTN-DOM-0000267 RELATED_SPECIALIZATION_OF VTN-DOM-0000068`
- Approval status: none
- Admission status: none

### Reinforced Concrete

- Nodes: `VTN-DOM-0000271`, `VTN-DOM-0012147`
- Group: `dup-3751564358d7`
- Decision ID: `canonical-20260501155958-f8da3711275f`
- Decision type: `CROSS_DOMAIN_EQUIVALENCE`
- Status: `proposed`
- Existing proposed relationship metadata: reciprocal `CROSS_DOMAIN_EQUIVALENT`
- Future admission relation: `CROSS_DOMAIN_ALIGNMENT`
- Approval status: none
- Admission status: none

## 5. Steward approval gate

Implemented approval/admission records and routes:
- `GET /graph/canonical/approvals`
- `GET /graph/canonical/approvals/:approvalId`
- `POST /graph/canonical/decisions/:decisionId/approval-preview`
- `POST /graph/canonical/decisions/:decisionId/approve`
- `POST /graph/canonical/decisions/:decisionId/reject-approval`

Approval metadata includes reviewer identity fields, role, source, rationale, mutation scope, risk acknowledgment, rollback plan, decision hash, validation snapshot, Kimi summary, transaction manifest id, and post-admission validation snapshot where applicable.

Rules now enforced:
- proposed decisions cannot become admitted without approval;
- high-risk approval requires risk acknowledgment;
- `test_fixture` approvals cannot be used for production `VTN-DOM-*` nodes and are test-mode only;
- destructive merge is blocked from this admission path;
- disambiguation/admission decision types cannot be directly applied and must pass the approval/admission gate;
- Kimi review is advisory and cannot stand in for steward approval.

The `/dev/canonical-review` UI now exposes an approval panel, approval preview, required fields, mutation scope, risk acknowledgment, rollback plan, approval/admitted summaries, P1 packet generation, and gate-disabled controls when local/dev/admin gate is not open.

## 6. CROSS_DOMAIN_EQUIVALENT review

Final admitted relation name: `CROSS_DOMAIN_ALIGNMENT`.

Rationale: `CROSS_DOMAIN_EQUIVALENT` was too strong because it implies identity. `CROSS_DOMAIN_ALIGNMENT` communicates cross-domain relationship/navigation without implying merge, redirect, alias, or canonical equivalence. Existing proposed metadata was not destructively rewritten; the admission path normalizes proposed `CROSS_DOMAIN_EQUIVALENT` to `CROSS_DOMAIN_ALIGNMENT`, and validation blocks active admitted `CROSS_DOMAIN_EQUIVALENT` edges.

## 7. Concrete decision status

Concrete remains proposed and unresolved.

- No merge.
- No alias.
- No redirect.
- No tombstone.
- No admitted production graph edge.
- Search/canonical review can show proposed disambiguation metadata without claiming an approved canonical result.

The proposed `RELATED_SPECIALIZATION_OF` direction remains available for steward review, but it is not learner-graph reality until a real approval is recorded.

## 8. Reinforced Concrete decision status

Reinforced Concrete remains proposed and unresolved.

- No merge.
- No alias.
- No redirect.
- No tombstone.
- No admitted production graph edge.
- Proposed `CROSS_DOMAIN_EQUIVALENT` metadata is treated as proposal-only; future admission uses `CROSS_DOMAIN_ALIGNMENT`.

## 9. Admitted relationships

None admitted in production.

Current counts:
- approvals: 0
- admitted relationships: 0
- graph edge count: unchanged at 13,670

If future admitted relationships are written, the AEC Explorer graph builder now overlays active admitted relationships and includes `admitted-relationships.json` in its cache key so selected-node neighborhood/search/graph visibility can refresh after admission/rollback.

## 10. Rollback/replay drill

Completed in test fixtures only.

Covered:
- approval preview blocker with missing fields;
- fixture approval with `test_fixture` source in test mode;
- non-destructive relationship admission;
- validation after admission;
- rollback preview;
- rollback apply;
- preservation of rolled-back relationship history;
- replay/re-approval after rollback.

No production rollback was executed because no production P0 approval/admission occurred.

## 11. P1 decision packets

Generated 20 non-destructive P1 decision packets.

Top groups include:
1. `dup-ca1078594013` building — `VTN-DOM-0000716`, `VTN-DOM-0000757` — `NEEDS_HUMAN_REVIEW`.
2. `dup-621135f7b4b9` load path — `VTN-DOM-0002932`, `VTN-DOM-0012160` — `NEEDS_HUMAN_REVIEW`.
3. `dup-6400e3e0c204` shallow foundation — `VTN-DOM-0000261`, `VTN-DOM-0003010` — `DISAMBIGUATED_KEEP_SEPARATE`.
4. `dup-79f6cd2af6bf` wall finishe — high risk — `NEEDS_HUMAN_REVIEW`.
5. `dup-a403cae6e1ea` mat foundation — high risk — `NEEDS_HUMAN_REVIEW`.

No P1 merge, alias, redirect, tombstone, resource rewrite, or production graph write occurred.

## 12. Resource Layer preservation status

Resource Layer data was not mutated by this loop.

Validation:
- resources: 7
- nodeResourceLinks: 9
- duplicateCount: 0
- brokenLinkCount: 0
- blockers: []
- warnings: existing standards-context warnings for ASCE 7 and ACI 318 only

## 13. Graph relationship visibility regression status

Graph relationship validation passed with:
- nodeCount: 10,018
- edgeCount: 13,670
- issueCount: 0
- semanticEdgeCount: 3,676
- concreteDuplicateCandidates: 2

Sendai Mediatheque/Toyo Ito remains covered by API regression tests. No P0 production stewardship edge was added, so graph edge count is unchanged.

## 14. Tests added/updated

API:
- Approval gate blocks missing metadata.
- Disambiguation decisions cannot bypass approval gate via direct apply.
- Fixture approval/admission rollback/replay.
- `CROSS_DOMAIN_EQUIVALENT` proposals normalize to `CROSS_DOMAIN_ALIGNMENT` before admission.
- P1 packets are generated without destructive actions.
- Canonical validation covers approvals, admitted relationships, and P1 packets.

Explorer:
- API client contract covers approvals and P1 packet routes.
- Canonical review admin renders approval and P1 packet controls.
- Search/inspector test mocks updated for the expanded graph API client.

## 15. Commands run

- `bun test api/canonicalGraphStewardship.test.ts`
- `cd api && bun test`
- `cd explorer && bun test`
- `cd explorer && bun run build`
- `bun run api/validateGraphRelationships.ts`
- `bun run api/validateResourceLayer.ts`
- `bun run api/validateCanonicalGraphStewardship.ts`
- `bash ./scripts/refresh_code_intelligence.sh`
- `cmd /c npx --yes gitnexus@1.6.4-rc.32 detect-changes --repo vitruvius`
- `chunkhound search --regex --page-size 20 --path-filter "api/" "CROSS_DOMAIN_ALIGNMENT|CanonicalApproval|admitted-relationships" .`

## 16. Test/build/validation results

- API tests: 156 pass, 0 fail.
- Explorer tests: 111 pass, 0 fail.
- Explorer build: pass; Vite chunk-size warning only.
- Graph relationship validation: ok true, 0 issues.
- Resource Layer validation: ok true, blockers [].
- Canonical stewardship validation: ok true, duplicate groups 544, unresolved 544, P0 unresolved 2, approvals 0, admittedRelationships 0, P1 packets 20.
- GitNexus detect-changes: critical risk due broad dirty worktree, not because a P0 merge/admission was performed.

## 17. Kimi review summary

### Review 1: P0 approval/admission model

Accepted:
- Separate proposed, steward-approved, and admitted states.
- Require approval metadata before admission.
- Block production use of test-fixture approvals.
- Bind approval to a decision hash.
- Treat Kimi as advisory, not approval.

Deferred:
- Server-derived authenticated identity.
- Two-person approval and stale approval re-checks.

### Review 2: CROSS_DOMAIN naming and semantics

Accepted:
- Use `CROSS_DOMAIN_ALIGNMENT` instead of `CROSS_DOMAIN_EQUIVALENT` for admitted relationships.
- Make semantics non-identity and non-canonicalizing.

Rejected:
- Keeping `CROSS_DOMAIN_EQUIVALENT` as admitted edge type.

Deferred:
- Full external mapping/SKOS policy.

### Review 3: P0 edge admission

Accepted:
- Keep P0 proposed until explicit human approval.
- Treat Concrete specialization proposal as plausible but not admitted.
- Normalize Reinforced Concrete cross-domain proposals to alignment before admission.

Rejected:
- Any P0 merge, alias, redirect, tombstone, or production edge admission without approval.

### Review 4: Rollback/replay drill

Accepted:
- Fix admitted relationship initialization ordering.
- Preserve rolled-back relationship history on replay.
- Include transaction manifest metadata before manifest write.

Deferred:
- Full production replay drill until real steward approval exists.

### Review 5: P1 packet strategy

Accepted:
- Expand packets with schema/run metadata, scoring reasons, decision alternatives, non-mutation flags, and review requirements.
- Block destructive packet-generated actions.

Deferred:
- Source graph/resource snapshot hashes per packet.
- Kimi review for every P1 packet.

### Review 6: Final implementation review

Accepted:
- Approval/admission model is safe for final report with caveats.
- `CROSS_DOMAIN_ALIGNMENT` admission semantics are safer.
- P1 packets and validation are non-destructive.

Hardened during final review:
- Added `admitted-relationships.json` to the AEC Explorer graph cache key.
- Blocked direct apply for disambiguation/admission decision types.
- Fixed admitted relationship confidence so only `test_fixture` approvals are labeled `test_fixture`; API/dev/human approvals are labeled `steward_approved`.

Deferred:
- Full production-ready identity/auth, relation domain/range registry, file-lock concurrency hardening beyond existing manifests, full alias/redirect/tombstone admission workflows.

## 18. Remaining unresolved groups

- Duplicate groups: 544
- Unresolved groups: 544
- P0 unresolved groups: 2
- P1 groups: 66, with 20 decision packets generated
- High-risk groups: 69
- Production approvals: 0
- Production admitted relationships: 0

## 19. Remaining gaps

- A real human/steward approval record is still needed before P0 admission.
- Server-derived reviewer identity and production auth are not implemented.
- Proposed P0 `CROSS_DOMAIN_EQUIVALENT` metadata is not migrated/superseded in place; admission normalizes it instead.
- No P0 production relationship edge is visible yet because no approval exists.
- P1 packets are generated but not human-reviewed.
- Source graph/resource snapshot hashes per P1 packet are deferred.

## 20. Recommended next loop

Run a human-steward approval session for P0 Concrete/Reinforced Concrete:
1. Review the P0 decision packet and Kimi critiques.
2. If approved, create real approval records through `/dev/canonical-review` or imported human record path.
3. Admit only non-destructive relationships using `RELATED_SPECIALIZATION_OF` and `CROSS_DOMAIN_ALIGNMENT` if approved.
4. Validate graph visibility and rollback on the approved production edge admission.
5. Expand P1 packet review with human/Kimi review for the top 20 generated packets.

---

## Latest manifest afterHash custody validation update

Date: 2026-05-02T02:20:15Z

Canonical stewardship validation now reports latest transaction-manifest afterHash custody metrics. Current state: 10 transaction manifests, 10 with afterHash entries, 3 files under manifest custody, 3 matches, 0 mismatches. Strict latest-afterHash mode passes for the current manifest-governed files.

No Concrete/Reinforced Concrete approval, merge, alias, redirect, tombstone, or admitted production edge was created.
