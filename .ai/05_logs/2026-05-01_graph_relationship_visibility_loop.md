# Graph Relationship Visibility Loop Validation Log

Date: 2026-05-01

## Scope

This loop prioritized making actual knowledge-graph relationships visible or explicitly discoverable in the Explorer graph UI. Resource Layer reviewer workflow behavior was preserved and regression-tested.

## Root cause verified

- Active graph data contains the Sendai Mediatheque -> Toyo Ito class relationship:
  - Sendai Mediatheque: `VTN-DOM-0012495`
  - Toyo Ito: `VTN-DOM-0012436`
  - Relationship: `VTN-DOM-0012436--has_facet--VTN-DOM-0012495`
  - API edge type: `HAS_FACET`
  - Category: semantic/person-work
- The backend detail route could expose the relationship, but the graph canvas was governed by static frontend edge filters that omitted real AEC edge types. Because `HAS_CHILD` intersected the existing filter set, the frontend did not reset or union semantic edge types, so real edges were silently hidden.
- Query/expand paths also risked store/canvas divergence because canvas controller merges did not always update the canonical Explorer store.

## Implemented validation artifacts

- `api/graphRelationshipVisibility.test.ts`
- `api/validateGraphRelationships.ts`
- `.ai/13_research/graph_duplicate_canonicalization_report.md`
- Updated API and Explorer tests for selected-node neighborhood hydration, inspector/canvas consistency signals, and resource-layer regression.

## Commands run

### API tests

Command:

```bash
cd api
bun test
```

Result:

- 134 pass
- 0 fail

### Explorer tests

Command:

```bash
cd explorer
bun test
```

Result:

- 108 pass
- 0 fail

### Explorer build

Command:

```bash
cd explorer
bun run build
```

Result:

- TypeScript build passed
- Vite build passed
- Existing warning: two chunks exceed 500 kB after minification

### Graph relationship validation

Command:

```bash
bun run api/validateGraphRelationships.ts
```

Result:

```json
{
  "ok": true,
  "nodeCount": 10018,
  "edgeCount": 13670,
  "hierarchyEdgeCount": 9994,
  "semanticEdgeCount": 3676,
  "issueCount": 0,
  "duplicateCanonicalLabelCount": 544,
  "safeDuplicateReviewCandidates": 251,
  "unsafeDuplicateReviewCandidates": 293,
  "concreteDuplicateCandidates": 2
}
```

### Resource Layer regression validation

Command:

```bash
bun run api/validateResourceLayer.ts
```

Result:

- `ok: true`
- resources: 7
- nodeResourceLinks: 9
- sourceFamilies: 25
- resourceCandidates: 4
- accepted_count: 5
- needs_review_count: 3
- rejected_count: 1
- local_files_indexed: 25
- local_files_admitted: 0
- standards_missing_context: 2
- duplicateCount: 0
- brokenLinkCount: 0
- blockers: []
- expected warnings retained for ASCE/ACI edition/version context

## Kimi review

- Long diagnosis prompt timed out after 184 seconds.
- Short no-tools diagnosis review succeeded and flagged N+1 selection fetch risk, endpoint hydration scope, type-registry drift, and inspector/canvas source split.
- Short no-tools implementation review succeeded and flagged high-degree payload limits, dynamic type allowlisting, store dedupe, and partial-normalization risks.
- Accepted actions already implemented: bounded neighborhood limit/truncation, hydrated endpoints, dynamic filter reconciliation, ID-based store merge, validation for broken references and duplicate labels.
- Deferred actions: formal ontology edge-type allowlist for user-facing filter groups and reviewer-driven duplicate apply workflow.

- Short no-tools final review succeeded and warned that UI visibility/hydration does not solve canonical fragmentation: 544 duplicate label groups remain. This was accepted as a next-loop blocker for canonical stewardship, not as a blocker for this visibility loop.

## Resource Layer status

No Resource Layer backfill, candidate promotion, local file linking, fake URL creation, or status mutation was performed. Existing Resource Layer API tests and validation passed.

## Remaining warnings/blockers

- No graph relationship blockers detected.
- Duplicate canonical labels are reported for steward review; no unsafe merge was performed.
- Resource Layer retains the expected standards context warnings for ASCE/ACI.

