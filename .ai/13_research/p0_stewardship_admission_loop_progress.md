# P0 Stewardship Admission Loop Progress

Date: 2026-05-02

## Scope

This loop operationalized a guarded admission path for the proposed P0 Concrete and Reinforced Concrete stewardship records. The loop did **not** merge production nodes, did **not** create aliases, redirects, tombstones, fake approvals, fake resources, or fake provenance.

## Dirty-worktree safety review

The worktree remains broadly dirty from prior loops and unrelated AEC-MEPFS/resource/canonical work. GitNexus `detect-changes` still reports critical risk across a broad dirty worktree. Current-loop production data mutation was therefore limited to non-destructive file-backed review artifacts and P1 packet generation.

Current-loop expected touch set:
- `api/graph/canonicalStewardship.ts`
- `api/index.ts`
- `api/canonicalGraphStewardship.test.ts`
- `explorer/src/api/graphApi.ts`
- `explorer/src/api/graphApi.test.ts`
- `explorer/src/app.searchInspector.integration.test.tsx`
- `explorer/src/components/canonical-review/CanonicalReviewAdmin.tsx`
- `explorer/src/components/canonical-review/CanonicalReviewAdmin.test.tsx`
- `explorer/src/components/inspector/NodeInspector.tsx`
- `explorer/src/types/index.ts`
- `006_System-Manifests/graph-canonical/p1-decision-packets.json`
- `006_System-Manifests/graph-canonical/transaction-manifests/*`
- this loop's `.ai/13_research/*` reports and `.ai/05_logs/*` validation log

Files not to overwrite: pre-existing broad dirty files outside this loop, especially AEC-MEPFS enrichment/shadow-staging artifacts and prior Resource Layer/canonical reports.

## Loaded P0 proposed decisions

### Concrete

- Group: `dup-0aa1351d9475`
- Nodes: `VTN-DOM-0000068`, `VTN-DOM-0000267`
- Decision: `canonical-20260501155958-e011dc288980`
- Type: `DISAMBIGUATED_KEEP_SEPARATE`
- Status: `proposed`
- Approval: none
- Admission: none
- Relationship proposal: `VTN-DOM-0000267 RELATED_SPECIALIZATION_OF VTN-DOM-0000068`
- Production edge: not admitted

### Reinforced Concrete

- Group: `dup-3751564358d7`
- Nodes: `VTN-DOM-0000271`, `VTN-DOM-0012147`
- Decision: `canonical-20260501155958-f8da3711275f`
- Type: `CROSS_DOMAIN_EQUIVALENCE`
- Status: `proposed`
- Approval: none
- Admission: none
- Relationship proposals currently remain metadata using `CROSS_DOMAIN_EQUIVALENT`; admission path normalizes them to `CROSS_DOMAIN_ALIGNMENT`.
- Production edge: not admitted

## Implementation progress

Completed:
- Added steward approval/admission data model and API helpers.
- Added approval validation requiring reviewer, rationale, risk acknowledgment for high risk, rollback plan, validation snapshot, decision hash, transaction manifest for mutation, and admin gate.
- Added API routes for approvals and P1 decision packets.
- Added admitted relationship overlay support without rewriting production graph files.
- Included `admitted-relationships.json` in the AEC Explorer graph cache key to prevent stale graph visibility after future admissions/rollbacks.
- Blocked direct `apply: true` for disambiguation/admission decision types; those must be proposed first and admitted through approval gate.
- Renamed/refined admitted cross-domain relation semantics to `CROSS_DOMAIN_ALIGNMENT`; old `CROSS_DOMAIN_EQUIVALENT` remains only proposed metadata and is normalized before admission.
- Added rollback/replay fixture coverage for non-destructive admissions.
- Generated 20 non-destructive P1 decision packets.
- Updated canonical review UI with approval panel, P1 packet panel, manifest/approval/admitted relationship summaries, and gate-disabled mutation controls.
- Updated inspector/search typing to surface canonical/stewardship status.

Not performed:
- No P0 steward approval was recorded because no real human approval input was provided.
- No P0 production graph edges were admitted.
- No alias, redirect, tombstone, or merge was applied.
- No P1 destructive action was applied.

## Validation snapshot

- `cd api && bun test`: 156 pass, 0 fail.
- `cd explorer && bun test`: 111 pass, 0 fail.
- `cd explorer && bun run build`: pass; Vite chunk-size warning only.
- `bun run api/validateGraphRelationships.ts`: ok true, 13,670 edges, 0 issues, concrete duplicate candidates 2.
- `bun run api/validateResourceLayer.ts`: ok true, blockers [], existing standards-context warnings 2.
- `bun run api/validateCanonicalGraphStewardship.ts`: ok true, duplicate groups 544, unresolved 544, P0 unresolved 2, approvals 0, admittedRelationships 0, P1 packets 20.
- `bash ./scripts/refresh_code_intelligence.sh`: completed; code-review-graph warned about missing `tree-sitter-yaml` and `_Task.elapsed` embedding service issue.
- `cmd /c npx --yes gitnexus@1.6.4-rc.32 detect-changes --repo vitruvius`: critical risk due broad dirty worktree.
