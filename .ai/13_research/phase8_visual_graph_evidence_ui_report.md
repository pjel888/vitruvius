# Phase 8 Visual Graph Evidence UI Report

**Date:** 2026-05-06
**Status:** VALIDATED_UI_ONLY
**Scope:** Explorer ResourceReviewAdmin Source Custody cards and NodeInspector Sources tab.

## Objective

Improve visual clarity for evidence states without mutating Resource Layer registries, graph/canonical data, candidates, Resources, or nodeResourceLinks.

## Changes

- ResourceReviewAdmin Source Custody cards now display explicit evidence-state badges:
  - item type, including external candidates,
  - review/status state such as `standards_context_in_review` and `source_custody_in_review`,
  - verification status such as `unverified`,
  - display policy such as `dev_only`,
  - learner visibility and promotion blockers.
- Source Custody overview now includes an External candidates metric when the API provides it.
- Explorer types now include `external_candidate` source-custody items and optional external candidate metrics.
- NodeInspector resource cards now mark accepted/human-reviewed resources as `Learner Visible`.
- NodeInspector Sources tab now states that learner mode only shows accepted or human-reviewed links and hides reviewer-only, unverified, or incomplete-standards records.

## Safety Boundaries

- No Resource created.
- No nodeResourceLink created.
- No candidate promoted.
- No external source verification performed.
- No learner exposure change.
- No graph/canonical mutation.
- No P0/high-risk P1 work.
- UI wording does not claim source truth, current/governing/compliance/AHJ status, or verification beyond existing registry fields.

## Impact Analysis

GitNexus impact checks:

| Symbol | Risk | Direct upstream impact |
|---|---|---|
| `CustodyBadge` | LOW | `SourceCustodyCard` |
| `SourceCustodyCard` | LOW | `ResourceReviewAdmin` |
| `ResourceCard` | LOW | `NodeInspector` |
| `NodeInspector` | LOW | none reported |

## Focused Validation

| Command | Result |
|---|---|
| `cd explorer && bun test src/components/resource-review/ResourceReviewAdmin.test.tsx` | PASS, 11 tests |
| `cd explorer && bun test src/components/componentInteraction.test.tsx` | PASS, 26 tests |
| `cd explorer && bun run build` | PASS, existing Vite chunk-size warning only |

## Full Validation

| Command | Result |
|---|---|
| `bun run api/validateResourceLayer.ts -- --no-write` | PASS, resources 7, nodeResourceLinks 9, blockers [] |
| `bun run api/validateGraphRelationships.ts -- --no-write` | PASS, admitted 264, base edges 13,670, effective edges 13,934 |
| `bun run api/validateCanonicalGraphStewardship.ts -- --no-write` | PASS, admitted relationships 264, CROSS_DOMAIN_ALIGNMENT 22, blockers [] |
| `cd api && bun test` | PASS, 426 tests |
| `cd explorer && bun test` | PASS, 121 tests |
| `cd explorer && bun run build` | PASS, existing Vite chunk-size warning only |
| `.venv\Scripts\python.exe -m pytest scripts/tests/test_kg_aec_relationship_improvement.py` | PASS, 118 tests |

## Known Non-Blocking Tool Notes

- `chunkhound search` found relevant artifacts but failed formatting one result due a Windows console Unicode encoding issue. GitNexus queries and direct file inspection were used after the required code-intelligence refresh.

## Next Action

Commit the scoped UI-only change and reports after post-edit code-intelligence refresh and staged-only change review.
