# Phase 6F — UI Evidence-Path Tests Report

Date: 2026-05-03

## Updated Test File

`explorer/src/components/resource-review/ResourceReviewAdmin.test.tsx`

Added `sampleSourceCustody()` helper and 4 new Source Custody tab tests.

## New Tests

1. `Source Custody tab renders grouped queue with safe badges`
   - Verifies learner-visible item shows "Learner visible" badge and "learner eligible"
   - Verifies standards-incomplete item shows "Context incomplete" and "not learner visible"
   - Verifies blocked item shows "Blocked" badge

2. `Source Custody tab shows local files as indexed-only and not admitted`
   - Verifies local file shows "Indexed only" badge
   - Verifies "not learner visible" badge

3. `Source Custody tab shows needs_review items with safe wording`
   - Verifies needs_review item shows "Needs review" badge
   - Verifies "not learner visible" badge

4. `Source Custody metrics render in overview section`
   - Verifies "Source Custody Overview" section renders
   - Verifies metric labels and values appear

## Existing Tests (preserved)

1. `renders queue metrics, needs_review links, candidates, local files, and rejected records`
2. `decision action uses structured form, calls API, and refreshes queue when applied`
3. `standards tab renders context workflow, preview diff, and disabled unsafe apply when gate is closed`
4. `renders empty and error states`

## Results

All 8 ResourceReviewAdmin tests pass. Full Explorer suite: 100 pass, 9 pre-existing failures in `ExploreView search-to-inspector integration`.

## NodeInspector Coverage

NodeInspector Sources tab is covered by:
- `api/resourceEvidencePath.test.ts` endpoint tests (verifies API returns safe data)
- `app.searchInspector.integration.test.tsx` (pre-existing, 9 failures unrelated to this work)
- Manual review confirms `ResourceCard` renders warning badges for rights/standards issues

No new dedicated NodeInspector test file was created; the component is tested through integration tests and the API contract tests above.
