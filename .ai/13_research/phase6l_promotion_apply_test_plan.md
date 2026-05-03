# Phase 6L Promotion Apply Test Plan

**Date:** 2026-05-03
**Status:** Planning — For Future Implementation

---

## API Tests

### Gate Tests

1. **promotion-apply route does not exist yet, or returns 501/404 in planning phase**
   - Verify no accidental implementation

2. **future apply route requires dev/admin gate**
   - Request without admin token → 403

3. **future apply route requires candidate `ready_for_promotion_review`**
   - Candidate with status `candidate` → 400 with blockers
   - Candidate with status `needs_review` → 400 with blockers

4. **future apply route requires reviewer/rationale/sourceOfContext**
   - Missing reviewer → 400
   - Missing rationale → 400
   - Missing sourceOfContext → 400
   - Rationale too short → 400

5. **future apply route rejects unverified syntax-only candidates for learner-visible acceptance**
   - `verificationStatus='unverified'` → allowed
   - `verificationStatus='source_verified'` without verifier → 400

6. **future apply route rejects fake URL/DOI/ISBN/standard context**
   - `fakePlaceholderFlags` non-empty → 400

7. **future apply route rejects incomplete standards context**
   - `standard_candidate` missing edition → 400
   - `guide_candidate` missing jurisdiction/scope → 400

8. **future apply route rejects rightsStatus unknown for learner-eligible paths**
   - `rightsStatus='unknown'` with `displayPolicy` that could become learner-visible → 400

### Mutation Tests

9. **future apply route creates Resource only in resource_only mode**
   - `resources.json` gains 1 record
   - `node-resource-links.json` unchanged

10. **future apply route creates no links in resource_only mode**
    - Link count unchanged

11. **future apply route creates links only in resource_and_links mode**
    - `node-resource-links.json` gains N records
    - Each link has `reviewStatus='needs_review'`

12. **future apply route writes transaction manifest**
    - Manifest file exists in `transaction-manifests/`
    - Manifest includes beforeHash/afterHash

13. **future apply route appends candidate decision history**
    - Candidate `decisions` array gains promotion decision

14. **future apply route does not mutate graph/canonical**
    - Graph node count unchanged
    - Canonical registries unchanged

15. **future apply route does not verify external data**
    - No HTTP requests to external URLs
    - No DOI resolution
    - No ISBN lookup

### Rollback Tests

16. **rollback-preview is read-only**
    - Multiple calls produce same result
    - No file mutation

17. **rollback apply reverses created resource/link or marks rollback safely**
    - Resource deleted if no other links
    - Links deleted or marked rolled_back
    - Candidate history gains rollback decision

18. **rollback transaction manifest written**
    - Manifest references original promotion manifest

### Integration Tests

19. **NodeInspector learner sidebar shows promoted resources only when accepted link eligibility passes**
    - Promoted resource with no links → hidden
    - Promoted resource with `needs_review` links → hidden
    - Promoted resource with `accepted` links → visible (if eligible)

20. **ASCE 7 / ACI 318 remain blocked unless real context supplied**
    - Incomplete standard candidate → 400 even if other gates pass

21. **production registries restored after tests**
    - `afterAll` resets all registries
    - `external-metadata-candidates.json` empty
    - `resources.json` unchanged from baseline
    - `node-resource-links.json` unchanged from baseline

---

## UI Tests

1. **apply preview renders**
   - Promotion Apply Preview tab visible

2. **apply button disabled when gates fail**
   - Button disabled, shows reason

3. **gate checklist renders blockers**
   - Blockers visible in red

4. **resource draft shows caveats**
   - Caveat text visible

5. **link draft shows caveats**
   - Caveat text visible

6. **unsafe wording absent**
   - No "verified", "official", "governing" labels

7. **standards warning shown**
   - For standard candidates, warning panel visible

8. **rights warning shown**
   - Rights panel visible with restrictions

9. **rollback preview shown after apply**
   - Rollback section visible in history

10. **no learner-visible toggle that bypasses eligibility**
    - No manual `learnerVisible=true` control
