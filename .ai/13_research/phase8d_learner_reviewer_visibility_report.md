# Phase 8D Learner And Reviewer Visibility Report

Run date: 2026-05-06

## Visibility Issue Found

During Phase 8D visibility verification, `GET /node/:id/resources?includeCandidates=true` returned reviewer-only `needs_review` Resources even when no reviewer mode was requested.

Root cause: the route forwarded `includeCandidates=true` into `getNodeResources` regardless of `mode`. `rankNodeResources` treats `includeCandidates` as reviewer-style inclusion, so a learner-mode request could include reviewer-only resources.

## Fix

`api/index.ts` now honors `includeCandidates` only when `mode === "reviewer"`:

```ts
const mode = c.req.query('mode') || 'learner';
const includeCandidates = mode === 'reviewer' && isTruthyQuery(c.req.query('includeCandidates'));
```

Reviewer mode still requires the local dev/admin gate.

## Regression Coverage

`api/resourceLayer.test.ts` now proves:

- learner default mode hides reviewer-only resources;
- learner mode with `includeCandidates=true` still hides reviewer-only resources;
- reviewer mode with `mode=reviewer&includeCandidates=true` can return `needs_review` resources through the reviewer/admin path.

## Verified Target Nodes

| Node | Learner default | Learner with `includeCandidates=true` | Reviewer with `mode=reviewer&includeCandidates=true` |
|---|---:|---:|---:|
| `VTN-DOM-0000092` BIM Schemas | 0 resources | 0 resources | 1 `needs_review` Resource |
| `VTN-DOM-0000056` Fire Protection | 0 resources | 0 resources | 1 `needs_review` Resource |
| `VTN-DOM-0000093` Classification Systems | 0 resources | 0 resources | 1 `needs_review` Resource |

## Source Custody Queue

The source custody queue still shows the three links in the reviewer/admin path as `needsReview` with:

- `displayPolicy: dev_only` in queue output
- `learnerEligible: false`
- hidden reason: pending review before trusted use

## Safety Result

- No external candidate appears in learner view.
- No reviewer-only Resource appears as learner-trusted.
- Reviewer/admin visibility remains available for review workflows.
- No Explorer UI files were changed in this unit; the API visibility contract was corrected and tested.
