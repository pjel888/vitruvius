# Phase 6G Source-Custody External Candidates Report

**Generated:** 2026-05-03T01:00:00+08:00

---

## Integration

External persisted candidates now appear in the source-custody queue via `buildSourceCustodyQueue()`.

### New Group: `externalCandidates`

Added to `SourceCustodyQueue.groups` and `SourceCustodyQueue.metrics`.

### Item Type: `external_candidate`

Added to `SourceCustodyItem.itemType` union.

### Mapping Logic

`enrichExternalCandidateItem(candidate)` maps:
- `itemType`: `'external_candidate'`
- `id`: `candidate.candidateId`
- `title`: `candidate.title`
- `resourceType`: `candidate.resourceType`
- `reviewStatus`: `candidate.status`
- `verificationStatus`: `candidate.verificationStatus`
- `custodyStatus`: `'blocked'` if placeholder flags, else `'candidate'`
- `displayPolicy`: `'blocked'` if placeholder flags, else `'dev_only'`
- `learnerEligible`: `false`
- `promotionBlocked`: `true`
- `nextReviewAction`: `'review_candidate_metadata'` or reject placeholder action
- `warningFlags`: `candidate.warningFlags`
- `rawUrl`: `candidate.proposedUrl`
- `rawIdentifier`: `candidate.proposedDoi || candidate.proposedIsbn`

### Metrics

`metrics.externalCandidates` counts all external candidate items in the queue.

---

## Safety

- External candidates never appear in `learner_visible` group
- External candidates never appear in `accepted` tab
- `learnerEligible` is always `false`
- `promotionBlocked` is always `true`
