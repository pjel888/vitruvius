# Full Autopilot Visual Graph Improvements

Date: 2026-05-07 local

## Unit 1 - Exact Verification Badge Tone

### Scope

This is an Explorer/NodeInspector visual truthfulness fix only.

Files changed:

- `explorer/src/utils/resourceVerification.ts`
- `explorer/src/components/inspector/NodeInspector.tsx`
- `explorer/src/components/resource-review/ResourceReviewAdmin.tsx`
- `explorer/src/components/resource-review/ResourceReviewAdmin.test.tsx`

No Resource Layer registry, candidate registry, graph/canonical registry, node metadata, graph edge, learner eligibility, source custody state, protected payload, P0 Concrete/Reinforced Concrete, or high-risk P1 state is mutated.

### Problem

`verificationStatus.includes('verified')` visually treated `unverified` as a positive verified state because `unverified` contains the substring `verified`.

Affected UI surfaces:

- NodeInspector Resource cards.
- ResourceReviewAdmin Source Custody cards.

### Implementation

Added `isPositiveResourceVerificationStatus` with exact positive status matching:

- `metadata_verified`
- `link_verified`
- `identifier_verified`
- `local_file_verified`
- `content_verified`
- `human_reviewed`
- `reviewer_verified_metadata`

Statuses not in that set, including `unverified`, `rejected`, and unknown future statuses, render as warning/neutral instead of success.

### Impact Analysis

GitNexus impact checks:

- `NodeInspector`: LOW risk; impacted count 0, affected processes 0.
- `ResourceReviewAdmin`: LOW risk; impacted count 0, affected processes 0.

This is a presentational status classification change only.

### Focused Verification

- `cd explorer; bun test src/components/resource-review/ResourceReviewAdmin.test.tsx`: PASS, 11 pass.
- `cd explorer; bun test src/components/componentInteraction.test.tsx`: PASS, 26 pass.
- `cd explorer; bun run build`: PASS with existing Vite chunk-size warning.
- `rg includes explorer/src/components/inspector/NodeInspector.tsx explorer/src/components/resource-review/ResourceReviewAdmin.tsx explorer/src/utils/resourceVerification.ts`: PASS; no `verificationStatus.includes('verified')` remains in touched surfaces.

### Delegated Review Request

Reviewer: `kimi_reviewer` using `kimi, version 1.41.0`.

This is delegated external AI review, not biological human review, not source truth, and not production approval by itself.

Requested verdict:

- `PASS_VISUAL_BADGE_FIX`
- `PASS_WITH_TEST_ADDITION_NEEDED`
- `BLOCK_UNSAFE_UI_CLAIM`
- `BLOCK_SCOPE_TOO_BROAD`
- `NEEDS_PROJECT_OWNER_INPUT`

Questions:

1. Does the exact-status helper fix the `unverified` badge false-positive without weakening verified statuses?
2. Is the change visual-only and scoped?
3. Does it avoid source-truth/current/governing/compliance/AHJ or learner eligibility claims?
4. Are the focused tests and build sufficient before full validation?

### Delegated Review Result

Reviewer: `kimi_reviewer` using `kimi, version 1.41.0`.

This is delegated external AI review, not biological human review, not source truth, and not production approval by itself.

Verdict: `PASS_VISUAL_BADGE_FIX`.

Reviewer findings:

- Exact positive-status matching prevents `unverified` from rendering as success/verified.
- No `verificationStatus.includes('verified')` predicate remains in the touched Explorer surfaces.
- The change is visual-only and does not mutate Resource Layer, graph/canonical state, learner eligibility, or API behavior.
- No source-truth, current, governing, compliance, AHJ, or learner-trust claims were introduced.
- Focused tests and Explorer build are adequate before full validation.

### Full Validation

Full suite after delegated review:

- `bun run api/validateResourceLayer.ts -- --no-write`: PASS; Resources 10, nodeResourceLinks 12, accepted links 9, blockers none.
- `bun run api/validateGraphRelationships.ts -- --no-write`: PASS; admitted relationships 266, base edges 13,670, effective edges 13,936, issueCount 0.
- `bun run api/validateCanonicalGraphStewardship.ts -- --no-write`: PASS; latest Resource Layer manifest hashes match, blockers none.
- `cd api && bun test`: PASS; 433 pass.
- `cd explorer && bun test`: PASS; 121 pass.
- `cd explorer && bun run build`: PASS with existing Vite chunk-size warning.
- `.venv\Scripts\python.exe -m pytest scripts/tests/test_kg_aec_relationship_improvement.py`: PASS; 118 pass.

### Safety Result

- Resources remain 10.
- nodeResourceLinks remain 12.
- Accepted links remain 9.
- Admitted relationships remain 266.
- Base edges remain 13,670.
- Effective edges remain 13,936.
- `CROSS_DOMAIN_EQUIVALENT` remains 0.
- No learner eligibility or learner exposure logic changed.
- No Resource Layer, graph/canonical, P0 Concrete/Reinforced Concrete, high-risk P1, or protected payload mutation occurred.

## FHWA Graph Potential Follow-Up

The newly accepted FHWA Earth Retaining Structures link was evaluated read-only after the FHWA accepted-link unit.

Recommendation: keep FHWA as Resource Layer-only evidence for now.

Exact blockers for graph mutation:

- `Structural Retaining Wall RESISTS Lateral Earth Pressure` duplicates existing `resists_lateral_earth_pressure` semantics.
- Drainage, groundwater, and perimeter-drain edges are already represented in the Retaining Wall neighborhood or would overclaim from metadata-only FHWA public-page evidence.
- `CROSS_DOMAIN_ALIGNMENT` to duplicate retaining wall variants is blocked by existing duplicate-review scope; the FHWA link does not resolve ARC/GEO/CHED duplicate semantics.
- `MAPS_TO_EXTERNAL_STANDARD` is not appropriate because FHWA Earth Retaining Structures is public government guidance, not an admitted external standard.

Safe boundary: Resource Layer evidence and NodeInspector caveat visibility only.

## NodeInspector Resource Caveat Visibility - 2026-05-07

### Change

Explorer Resource cards in `NodeInspector` now surface the Resource Layer fields already returned for learner-eligible accepted Resources:

- `sourceTruthCaveat` as an `Evidence:` row.
- `rightsCaveat` as a `Rights:` row.
- `lastCheckedAt` as a formatted `Checked:` date.

This is visual-only. It does not alter Resource Layer registries, nodeResourceLinks, learner eligibility, graph/canonical data, or API behavior.

### Safety Boundary

- No source-truth, current, governing, compliance, AHJ, jurisdictional, rights-clearance, or publication-status claim was added.
- No learner eligibility override was added.
- Reviewer-only, unverified, and incomplete standards-context Resources remain hidden from learner Resource cards by the existing filter.
- No Resource, candidate, nodeResourceLink, graph, canonical, P0, or high-risk P1 mutation occurred.

### Focused Verification

- `cd explorer && bun test src/components/componentInteraction.test.tsx`: PASS, 26 pass.
- Regression coverage asserts the metadata-only source caveat, rights caveat, and formatted checked date are visible for an accepted Resource while reviewer-only candidate Resources remain hidden.

### Delegated Review Result

Reviewer: `kimi_reviewer` using `kimi, version 1.41.0`.

This is delegated external AI review, not biological human review, not source truth, and not production approval by itself.

Verdict: `PASS_VISUAL_CAVEAT_DISPLAY`.

Reviewer findings:

- The change is visual-only and scoped to `NodeInspector` rendering and component tests.
- Existing `ResourceReference` fields are displayed without changing eligibility, Resource Layer data, graph state, or API behavior.
- The wording remains caveated and avoids source-truth/current/governing/compliance/AHJ/rights-clearance claims.
- The full validation matrix is adequate for this visual-only unit.

### Full Validation

- `bun run api/validateResourceLayer.ts -- --no-write`: PASS; Resources 10, nodeResourceLinks 12, accepted links 9, blockers none.
- `bun run api/validateGraphRelationships.ts -- --no-write`: PASS; admitted relationships 266, base edges 13,670, effective edges 13,936, issueCount 0.
- `bun run api/validateCanonicalGraphStewardship.ts -- --no-write`: PASS; latest Resource Layer manifest hashes match, blockers none.
- `cd api && bun test`: PASS; 434 pass.
- `cd explorer && bun test`: PASS; 121 pass.
- `cd explorer && bun run build`: PASS with existing Vite chunk-size warning.
- `.venv\Scripts\python.exe -m pytest scripts/tests/test_kg_aec_relationship_improvement.py`: PASS; 118 pass.

### Safety Result

- Resources remain 10.
- nodeResourceLinks remain 12.
- Accepted links remain 9.
- Admitted relationships remain 266.
- Base edges remain 13,670.
- Effective edges remain 13,936.
- `CROSS_DOMAIN_EQUIVALENT` remains 0.
- Learner-visible Resource filtering remains unchanged.
