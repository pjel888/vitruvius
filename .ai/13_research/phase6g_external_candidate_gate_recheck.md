# Phase 6G External Candidate Gate Recheck

**Date:** 2026-05-03
**Status:** Verified

## Route Gating

| Route | Gate | Status |
|---|---|---|
| GET /resources/review/source-custody | `requireLocalDevAdmin` | ✅ Gated |
| GET /resources/review/external-candidates/schema | Open (schema only) | ✅ Safe |
| POST /resources/review/external-candidates/preview | `requireLocalDevAdmin` | ✅ Gated |
| POST /resources/review/external-candidates | `requireLocalDevAdmin` | ✅ Gated |
| GET /resources/review/external-candidates | `requireLocalDevAdmin` | ✅ Gated |
| GET /resources/review/external-candidates/:candidateId | `requireLocalDevAdmin` | ✅ Gated |
| GET /node/:id/resources | Learner-safe, no candidate inclusion | ✅ Safe |

## Learner Exposure Check

- `getNodeResources()` reads `resources.json` + `node-resource-links.json` only.
- External candidate registry is NOT read by learner endpoints.
- `rankNodeResources()` filters by `reviewStatus === 'accepted' || 'human_reviewed'` in learner mode.
- External candidates have `learnerVisible=false`, `displayPolicy='reviewer_only'`.
- `verificationStatus` is forced to `'unverified'`.

## NodeInspector Sources
- NodeInspector uses `GET /node/:id/resources` with `mode='learner'`.
- External candidates are invisible.

## Conclusion
All gates correct. No learner exposure. No external verification occurs.
