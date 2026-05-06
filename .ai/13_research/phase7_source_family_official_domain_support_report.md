# Phase 7 Source-Family Official Domain Support Report

**Date:** 2026-05-06
**Unit:** Phase 7 source-family official-domain support
**Status:** VALIDATION_PASSED_COMMIT_PENDING

## Objective

Extend the controlled source-verification helper allowlist beyond ASCE and FHWA so reviewer-only source-family candidates can be checked against their own official domains in a future gated review step.

## Scope

- Added official source-family identifiers for:
  - buildingSMART
  - AISC
  - AIA
- Added official HTTPS host checks for:
  - `buildingsmart.org` and subdomains
  - `aisc.org` and subdomains
  - `aia.org` and subdomains
- Added candidate-family classification from repo-local source-family id, publisher, title, or already-supplied candidate URL host.
- Added mocked API/helper tests for source-family official-domain checks.

## Safety Boundaries

- No live source check was performed in this unit.
- No Resource was created.
- No nodeResourceLink was created.
- No candidate was promoted.
- No candidate status or registry data was changed.
- No learner exposure occurred.
- No graph/canonical registry was changed.
- No protected content was downloaded or stored.
- No DOI, ISBN, book, PDF, standards, or external API lookup occurred.
- HTTP success remains only bounded URL metadata and is not source truth.

## Code Changes

- `api/resourceLayer/sourceVerification.ts`
  - Extended `ControlledSourceCheckResult.sourceFamily` to include `buildingsmart`, `aisc`, and `aia`.
  - Added exact official host checks for the three source families.
  - Added source-family candidate classification for future preview routes.

- `api/resourceLayerSourceVerification.test.ts`
  - Added a source-family candidate fixture.
  - Added coverage for accepted buildingSMART official subdomains.
  - Added coverage blocking cross-family official-looking domains.
  - Added preview-route coverage for an AIA source-family candidate with explicit requested official URL.

## Delegated Review

Kimi reviewed the diff as a project-owner-delegated external AI reviewer and returned `PASS_SOURCE_FAMILY_OFFICIAL_DOMAIN_SUPPORT`.

Reviewer caveat:

> This is delegated external AI review, not biological human review, not source truth, and not production approval by itself.

The Kimi minor consistency note to use exact `buildingsmart` source-family matching was applied before final validation.

## Validation Summary

- `bun test api/resourceLayerSourceVerification.test.ts`: PASS, 24 pass
- `bun run api/validateResourceLayer.ts -- --no-write`: PASS, resources 7, nodeResourceLinks 9, external candidates 5
- `bun run api/validateGraphRelationships.ts -- --no-write`: PASS, admitted relationships 264, base edges 13,670, effective edges 13,934
- `bun run api/validateCanonicalGraphStewardship.ts -- --no-write`: PASS, blockers []
- `cd api && bun test`: PASS, 422 pass
- `cd explorer && bun test`: PASS, 121 pass
- `cd explorer && bun run build`: PASS with existing Vite chunk-size warning
- `.venv\Scripts\python.exe -m pytest scripts/tests/test_kg_aec_relationship_improvement.py`: PASS, 118 pass

## Current Counts

- Admitted relationships: 264
- Base graph edges: 13,670
- Effective graph edges: 13,934
- Resources: 7
- nodeResourceLinks: 9
- External metadata candidates: 5
- Learner-visible external candidates: 0

## Next Safe Action

Future source-family metadata correction or source-custody review can use the official-domain preview route for buildingSMART, AISC, and AIA only when a reviewer supplies an explicit official URL. Promotion, Resource creation, nodeResourceLink creation, learner exposure, graph/canonical mutation, and source-truth claims remain blocked.
