# Phase 6G External Candidate Test Cleanup Report

**Date:** 2026-05-03
**Status:** Complete

## Changes Applied

### `api/resourceLayerExternalCandidates.test.ts`
1. Added `afterAll(() => resetExternalCandidateRegistry())`.
2. Added `cleanTransactionManifests()` helper using `readdirSync` + `unlinkSync`.
3. Called `cleanTransactionManifests()` in `beforeEach` and `afterAll`.
4. Added test: "registry is empty after test cleanup".

## Verification
- 46/46 tests pass.
- `external-metadata-candidates.json` has 0 candidates after suite.
- `transaction-manifests/` is empty after suite.
- Canonical validator: no drift warning.
- Resource Layer validator: no errors.

## Safety
- No production resources created.
- No nodeResourceLinks created.
- No graph/canonical mutation.
- No learner exposure.
