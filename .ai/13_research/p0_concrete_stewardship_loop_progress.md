# P0 Concrete Stewardship Loop Progress

Date: 2026-05-01

## Safety and dirty worktree review

The worktree remains broadly dirty from prior loops and unrelated AEC-MEPFS / Resource Layer / canonical operations work. This loop touched only the P0 stewardship implementation/reporting surfaces listed below and did not overwrite unrelated human or previous-loop changes.

This loop expected to touch:
- `api/graph/canonicalStewardship.ts`
- `api/index.ts`
- `api/validateCanonicalGraphStewardship.ts`
- `api/canonicalGraphStewardship.test.ts`
- `explorer/src/api/graphApi.ts`
- `explorer/src/api/graphApi.test.ts`
- `explorer/src/types/index.ts`
- `explorer/src/components/canonical-review/CanonicalReviewAdmin.tsx`
- `explorer/src/components/canonical-review/CanonicalReviewAdmin.test.tsx`
- `explorer/src/components/command-bar/SearchCombobox.tsx`
- `explorer/src/app.searchInspector.integration.test.tsx`
- `006_System-Manifests/graph-canonical/*`
- P0 stewardship reports under `.ai/13_research/`

No destructive production graph mutation was considered safe because P0 groups remain high-risk and no explicit human steward approval exists.

## P0 baseline

- Total duplicate groups: 544
- Unresolved duplicate groups: 544
- P0 groups: 2
- High-risk groups: 69
- Applied decisions before/after this loop: 0
- Aliases before/after this loop: 0
- Redirects before/after this loop: 0
- Tombstones before/after this loop: 0

## Concrete group

- Group: `dup-0aa1351d9475`
- Nodes: `VTN-DOM-0000068`, `VTN-DOM-0000267`
- Status: proposed `DISAMBIGUATED_KEEP_SEPARATE`; not applied as steward-approved resolution.
- Proposed relationship: `VTN-DOM-0000267 RELATED_SPECIALIZATION_OF VTN-DOM-0000068`, proposed only.
- Production merge/alias/redirect/tombstone: none.

## Reinforced concrete group

- Group: `dup-3751564358d7`
- Nodes: `VTN-DOM-0000271`, `VTN-DOM-0012147`
- Status: proposed `CROSS_DOMAIN_EQUIVALENCE`; not applied as steward-approved resolution.
- Proposed relationships: bidirectional `CROSS_DOMAIN_EQUIVALENT`, proposed only and documented as cross-domain alignment, not identity.
- Production merge/alias/redirect/tombstone: none.

## Implementation progress

Completed:
- Extended stewardship decision types for governed disambiguation and cross-domain alignment.
- Added proposed relationship proposals to canonical preview/decision records without admitting production graph edges.
- Added alias/redirect/tombstone validation hardening.
- Added partial rollback remediation manifest model, API, UI, validation, and tests.
- Improved canonical search and SearchCombobox ambiguity metadata for proposed P0 decisions.
- Improved `/dev/canonical-review` with remediation and existing stewardship status surfaces.
- Started non-destructive P1 triage batch with 20 groups and no batch decisions.
- Fixed general Explorer `/search` so proposed canonical metadata does not rerank unrelated learner-facing search.

Deferred:
- Human approval of concrete/reinforced-concrete decisions.
- Production admission of proposed disambiguation relationships.
- Renaming `CROSS_DOMAIN_EQUIVALENT` to a less identity-sounding term before approval.
- Full P1 decision packet generation and steward review.
