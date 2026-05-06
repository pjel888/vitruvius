# Phase 7 Wave 3 Source-Family Official Domain Support Report

**Date:** 2026-05-06
**Status:** VALIDATION_PASSED_COMMIT_PENDING

## Objective

Extend the controlled source-verification helper to recognize official-domain allowlists for the two wave 3 source-family candidates:

- `uniclass_nbs`
- `omniclass_csi`

This unit enables future explicit reviewer-supplied URL previews for those source families. It does not perform live source verification and does not mutate Resource Layer registries.

## Implementation Scope

Changed files:

- `api/resourceLayer/sourceVerification.ts`
- `api/resourceLayerSourceVerification.test.ts`

Code changes:

- Added `uniclass_nbs` and `omniclass_csi` to `ControlledSourceFamily`.
- Allowed only these host families:
  - Uniclass/NBS: `thenbs.com`, `uniclass.thenbs.com`, and subdomains
  - OmniClass/CSI: `csiresources.org`, `csinet.org`, and subdomains
- Added candidate source-family inference using exact `proposedSourceFamilyId`, precise publisher/title cues, or official hosts.
- Added mocked helper tests for both official-domain families.
- Added mocked preview-route coverage for a wave 3 source-family candidate.

## Code-Intelligence Evidence

- `bash ./scripts/refresh_code_intelligence.sh` before edits: PASS_WITH_WARNINGS
  - GitNexus already current.
  - ChunkHound completed with known large-file timeout/embedding warnings.
  - code-review-graph completed with known missing `tree-sitter-yaml` warnings.
- GitNexus impact:
  - `officialSourceFamilyForCandidate`: LOW, impacted count 5.
  - `isOfficialHostForFamily`: LOW, impacted count 5.
  - `checkOfficialSourceCandidate`: LOW, impacted count 6.
- `bash ./scripts/refresh_code_intelligence.sh` after edits: PASS_WITH_WARNINGS with the same known warning classes.

## Safety

- No live source verification occurred.
- No URL was fetched in production.
- Mocked tests only.
- No Resource Layer registry mutation occurred.
- No Resource was created.
- No nodeResourceLink was created.
- No candidate was promoted.
- No learner exposure occurred.
- No graph/canonical/P0/high-risk P1 mutation occurred.
- No source-truth, current/governing/compliance, jurisdiction, AHJ, DOI, ISBN, publication metadata, or learner-trust claim was introduced.

## Next Safe Action

Commit and push this scoped helper/test/report unit. Future source-custody work may use explicit reviewer-supplied official URLs for Uniclass/NBS or OmniClass/CSI previews, but those previews still do not establish source truth, Resource acceptance, node links, or learner trust by themselves.
