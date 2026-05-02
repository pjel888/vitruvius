# Ralph Context Snapshot - P0 Stewardship Admission

## Task statement
Create and execute a guarded steward-admission workflow for P0 Concrete and Reinforced Concrete after proposed-only P0 stewardship.

## Desired outcome
Implement approval/admission infrastructure, review/rename risky cross-domain relation semantics, keep P0 production decisions truthful unless explicit steward approval exists, enable non-destructive admission in controlled/test-fixture paths, run rollback/replay drill, generate P1 decision packets, and validate all API/Explorer/graph/resource regressions.

## Known facts/evidence
- P0 decisions are proposed-only: concrete DISAMBIGUATED_KEEP_SEPARATE; reinforced concrete CROSS_DOMAIN_EQUIVALENCE.
- No aliases, redirects, tombstones, or applied production steward decisions exist.
- Proposed relationship proposals are review metadata, not learner graph edges.
- Prior validations passed; GitNexus reports critical due broad pre-existing dirty worktree.
- CROSS_DOMAIN_EQUIVALENT naming is risky before production edge admission.

## Constraints
- No fake steward approval.
- No destructive Concrete/Reinforced Concrete merge.
- No fake graph facts/resources/provenance.
- Preserve graph relationship visibility and Resource Layer routes.
- Do not bulk-merge P1.
- Use Kimi at least five times and record accepted/rejected/deferred suggestions.

## Unknowns/open questions
- Existing exact schema hooks for approval records and transaction manifests.
- Whether admission can be production-applied or must remain test-fixture only due lack of human approval.
- Existing UI component structure for adding approval panels and P1 packet display.

## Likely touchpoints
- api/graph/canonicalStewardship.ts
- api/index.ts
- api/validateCanonicalGraphStewardship.ts
- api/canonicalGraphStewardship.test.ts
- explorer/src/api/graphApi.ts
- explorer/src/types/index.ts
- explorer/src/components/canonical-review/CanonicalReviewAdmin.tsx
- explorer/src/components/command-bar/SearchCombobox.tsx
- 006_System-Manifests/graph-canonical/
- .ai/13_research/*admission* reports
