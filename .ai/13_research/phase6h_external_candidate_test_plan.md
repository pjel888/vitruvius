# Phase 6H External Candidate Test Plan

**Date:** 2026-05-03
**Status:** Planning — Tests Designed, NOT Implemented

## API Tests

### Correction Preview Tests

1. **correction-preview rejects placeholder metadata**
   - Patch title to "TBD" → returns blocker
   - Patch edition to "latest" → returns blocker

2. **correction-preview cannot set learnerVisible=true**
   - Patch `learnerVisible: true` → returns blocker, invalid

3. **correction-preview cannot set verificationStatus=verified**
   - Patch `verificationStatus: 'verified'` → returns blocker, invalid

4. **correction-preview cannot create resourceId**
   - Patch `resourceId: 'fake'` → returns blocker, invalid

5. **correction-preview shows diff for valid patch**
   - Patch title from "A" to "B" → diff.before.title === "A", diff.after.title === "B"

### Correction Apply Tests

6. **correction apply requires dev/admin gate**
   - Request without admin token → 403

7. **correction apply writes candidate registry only**
   - After apply, candidate.title updated
   - resources.json unchanged
   - node-resource-links.json unchanged

8. **correction apply writes transaction manifest**
   - Response includes `manifest.transactionId`
   - Manifest file exists in `transaction-manifests/`

9. **correction apply appends decision record**
   - `external-candidate-decisions.json` gains entry
   - Entry has `decisionType: 'correction'`

### Review Decision Tests

10. **reject decision preserves candidate record**
    - Status becomes `rejected`
    - Candidate still exists in registry
    - Decision history has rejection rationale

11. **duplicate decision links to another candidate but does not delete**
    - Status becomes `duplicate_candidate`
    - Original candidate preserved
    - `duplicateOfCandidateId` set

12. **ready_for_promotion_review requires all readiness gates**
    - Candidate with placeholder → 400, blockers
    - Candidate with all gates passing → 200, status updated

13. **standards candidate cannot be ready without context**
    - `standard_candidate` missing edition → 400, blockers
    - `standard_candidate` with edition + jurisdiction → 200

14. **rights-limited candidate cannot be learner-visible**
    - Even if all other gates pass, `learnerVisible` stays false

15. **promotion preview does not create resource (future)**
    - Response has `proposedResource` but no file mutation

16. **promotion preview does not create nodeResourceLink (future)**
    - Response has `proposedLinks` but no file mutation

### Learner Exposure Tests

17. **learner endpoint still hides external candidates**
    - `GET /node/:id/resources` with `mode='learner'` → no external candidates

18. **source-custody queue shows updated candidate status**
    - After decision apply, queue reflects new status

## UI Tests

19. **review panel renders candidate status**
    - Selected candidate shows status badge

20. **correction preview shows diff**
    - Preview button renders before/after

21. **invalid correction shows blockers**
    - Placeholder in form → blockers list visible

22. **ready checklist renders blockers**
    - Promotion readiness shows red X for failed gates

23. **no unsafe wording**
    - UI contains no "accepted", "verified", "official", etc.

24. **no promote/apply button unless future gate explicitly allows it**
    - Promotion apply button absent in 6H
    - Only "Ready for promotion review" status is shown

## Integration Tests

25. **full review workflow: persist → correct → review → history**
    - End-to-end test of 6H flow without promotion

26. **no graph/canonical/registry mutation during review workflow**
    - Run validators before and after; no diff except candidate registry

## Test Data Requirements

- Use `beforeEach` + `afterAll` cleanup (same as 6G tests).
- Clean transaction manifests after suite.
- Do not depend on real external URLs/DOIs/ISBNs.
