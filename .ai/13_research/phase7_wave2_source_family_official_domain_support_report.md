# Phase 7 Wave 2 Source-Family Official Domain Support Report

**Date:** 2026-05-06
**Unit:** Controlled source-verification helper support for Phase 7 wave 2 source-family candidates
**Status:** validation passed, commit pending

## Scope

This unit extends the controlled source-verification official-domain mapping for the five source-family candidates added in Phase 7 candidate intake wave 2 and moved to `needs_review` in review wave 2.

Supported families added:

- `us_access_board`: `access-board.gov`
- `wbdg_nibs`: `wbdg.org`, `nibs.org`
- `istructe`: `istructe.org`
- `ice`: `ice.org.uk`, `knowledgehub.ice.org.uk`
- `riba`: `architecture.com`

## Implementation

Changed files:

- `api/resourceLayer/sourceVerification.ts`
- `api/resourceLayerSourceVerification.test.ts`

Implementation details:

- Introduced `ControlledSourceFamily` as the typed source-family vocabulary for controlled checks.
- Added official-host matching for the five wave 2 source families.
- Added candidate-family inference from `proposedSourceFamilyId`, publisher/title text, and explicit requested/proposed URL host.
- Added mocked helper coverage for all five new official-domain families.
- Added mocked preview-route coverage for a wave 2 source-family candidate with an explicit official requested URL.

## Safety

- No live source verification occurred in this unit.
- No URL was fetched outside mocked tests.
- No Resource was created.
- No nodeResourceLink was created.
- No candidate status changed.
- No candidate was promoted.
- No learner exposure occurred.
- No graph/canonical/P0/high-risk P1 mutation occurred.
- No source-truth, current/governing, compliance, jurisdiction, or AHJ claim was added.

## Code Intelligence

- `bash ./scripts/refresh_code_intelligence.sh`: PASS_WITH_WARNINGS. GitNexus was current; ChunkHound emitted known large-file/embedding warnings; code-review-graph emitted known missing `tree-sitter-yaml` warnings.
- `gitnexus impact officialSourceFamilyForCandidate --direction upstream --repo vitruvius --depth 3 --include-tests`: LOW risk, one direct caller.
- `gitnexus impact isOfficialHostForFamily --direction upstream --repo vitruvius --depth 3 --include-tests`: LOW risk, two direct callers.

## Delegated Review

Kimi returned `PASS_WAVE2_SOURCE_FAMILY_OFFICIAL_DOMAIN_SUPPORT` with no blockers.

This is delegated external AI review, not biological human review, not source truth, and not production approval by itself.

## Next Safe Action

Commit and push this scoped helper/test/report unit, then reassess whether any remaining Phase 7 work is unblocked without promotion, Resource creation, nodeResourceLink creation, learner exposure, graph/canonical mutation, or invented metadata.
