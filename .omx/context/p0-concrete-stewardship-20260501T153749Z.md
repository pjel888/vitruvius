# P0 Concrete Stewardship Context Snapshot

## Task statement
Implement the P0 Concrete/Reinforced Concrete stewardship loop safely: resolve or explain the two P0 duplicate groups through governed non-destructive stewardship, disambiguation/search/UI improvements, alias/redirect/tombstone validation, rollback remediation manifests, and P1 non-destructive triage.

## Desired outcome
Concrete and reinforced concrete P0 groups become more useful, searchable, and reviewable without fake approvals or destructive production merges. Graph relationship visibility, Resource Layer, canonical ops, and admin gates remain intact.

## Known facts/evidence
- P0 groups: concrete (`VTN-DOM-0000068`, `VTN-DOM-0000267`), reinforced concrete (`VTN-DOM-0000271`, `VTN-DOM-0012147`).
- Previous operations loop had 544 unresolved duplicate groups, aliases 0, redirects 0, applied decisions 0.
- Prior Kimi recommendation: do not blindly merge concrete; prefer governed disambiguation / keep separate unless steward-approved.
- Code intelligence refresh completed with YAML parser warnings and EmbSvc `_Task.elapsed` warning.
- Broad dirty worktree exists from prior loops and unrelated KG work.

## Constraints
- No fake steward approval, fake resources/provenance, placeholder nodes/edges, broad duplicate cleanup, or destructive P0/P1 merge.
- Preserve graph edges, Resource Layer links, selected-node relationship visibility, canonical routes, Resource Review UI, Canonical Review UI.
- Add tests/validation and Kimi reviews.

## Unknowns/open questions
- Exact current node semantics/resources/edges for the four P0 nodes.
- Whether existing decision model can be extended without breaking tests.
- Whether production decision records should be proposed-only or applied non-destructively.

## Likely touchpoints
- `api/graph/canonicalStewardship.ts`
- `api/index.ts`
- `api/validateCanonicalGraphStewardship.ts`
- `api/canonicalGraphStewardship.test.ts`
- `explorer/src/api/graphApi.ts`
- `explorer/src/types/index.ts`
- `explorer/src/components/canonical-review/CanonicalReviewAdmin.tsx`
- `.ai/13_research/*p0*`, concrete reports, final report
