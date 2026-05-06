# Phase 7 Candidate Intake Wave 1 Validation

Date: 2026-05-06

## Registry State

| Registry | Count |
|---|---:|
| Resources | 7 |
| nodeResourceLinks | 9 |
| External metadata candidates | 5 |
| Learner-visible external metadata candidates | 0 |

External candidate statuses:

- `ext-cand-asce-7-minimum-design-loads-and-associat-mosyi54p-miqu`: `standards_context_in_review`, `unverified`, `reviewer_only`, learner-hidden
- `ext-cand-earth-retaining-structures-mosyi54y-jp9m`: `source_custody_in_review`, `unverified`, `reviewer_only`, learner-hidden
- `ext-cand-buildingsmart-international-source-famil-motn39h2-hl6o`: `candidate`, `unverified`, `reviewer_only`, learner-hidden
- `ext-cand-american-institute-of-steel-construction-motn39hs-lz60`: `candidate`, `unverified`, `reviewer_only`, learner-hidden
- `ext-cand-american-institute-of-architects-source--motn39ic-iz2k`: `candidate`, `unverified`, `reviewer_only`, learner-hidden

## Validator Results

| Command | Result |
|---|---|
| `bun run api/validateResourceLayer.ts -- --no-write` | PASS: resources 7, nodeResourceLinks 9, external metadata candidates 5, blockers [] |
| `bun run api/validateGraphRelationships.ts -- --no-write` | PASS: admitted 264, base edges 13,670, effective edges 13,934, issues 0 |
| `bun run api/validateCanonicalGraphStewardship.ts -- --no-write` | PASS: CROSS_DOMAIN_ALIGNMENT 22, latest Resource Layer manifest hash matched, blockers [] |

## Focused Tests

| Command | Result |
|---|---|
| `bun test api/resourceLayerExternalCandidates.test.ts api/resourceLayerExternalCandidateReview.test.ts api/resourceEvidencePath.test.ts` | PASS: 93 pass, 0 fail |

## Full Suites

| Command | Result |
|---|---|
| `cd api && bun test` | PASS: 419 pass, 0 fail |
| `cd explorer && bun test` | PASS: 121 pass, 0 fail |
| `cd explorer && bun run build` | PASS_WITH_WARNING: build completed; existing Vite chunk-size warning |
| `.venv\Scripts\python.exe -m pytest scripts/tests/test_kg_aec_relationship_improvement.py` | PASS: 118 pass |

## Safety Verification

- No Resource was created.
- No nodeResourceLink was created.
- No candidate was promoted.
- No learner exposure occurred.
- No graph/canonical/P0/high-risk P1 mutation occurred.
- No external source verification, URL fetch, DOI lookup, ISBN lookup, protected content access, or source-truth claim occurred in this wave.
- The only Resource Layer registry intentionally changed was `external-metadata-candidates.json`, backed by three transaction manifests.
