# Phase 8D Accepted-Link Review Packet

Run date: 2026-05-06

## Reviewer Instructions

This packet is for delegated external AI review. The reviewer must not be treated as a biological human reviewer, source truth, external verification by itself, or production approval.

Required statement:

`This is delegated external AI review, not biological human review, not source truth, and not production approval by itself.`

Reviewer verdict per link must be one of:

- `ACCEPT_LINK`
- `KEEP_NEEDS_REVIEW`
- `MARK_RIGHTS_REVIEW_NEEDED`
- `MARK_SOURCE_CUSTODY_REVIEW_NEEDED`
- `REJECT_LINK`
- `DEFER_LINK`

## Current Baseline

- Resources: 10
- nodeResourceLinks: 12
- accepted links: 5
- needs_review links: 6
- rejected links: 1
- External metadata candidates: 15
- Learner-visible external candidates: 0
- Graph admitted relationships: 264
- Base edges: 13670
- Effective edges: 13934
- CROSS_DOMAIN_EQUIVALENT: 0
- CROSS_DOMAIN_ALIGNMENT: 22
- No graph/canonical/P0/high-risk P1 mutation in this task.

## Link A: buildingSMART IFC -> BIM Schemas

```yaml
linkId: nrl_521bc0e1-130d-4332-91b9-68ab8f83efc7
resourceId: res_9c586758-66e4-46f2-b62a-8720db1c0976
resourceTitle: Industry Foundation Classes (IFC) - buildingSMART International
nodeId: VTN-DOM-0000092
nodeLabel: BIM Schemas
relationship: explains
currentStatus: needs_review
learnerEligible: false
learnerExposure: false
resourceVerificationStatus: unverified
resourceDisplayPolicy: reviewer_only
sourceFamilyIds:
  - buildingsmart
officialLocatorChecked: https://buildingsmart.org/standards/bsi-standards/industry-foundation-classes
finalUrl: https://www.buildingsmart.org/standards/bsi-standards/industry-foundation-classes/
httpStatus: 200
publicTitle: Industry Foundation Classes (IFC) - buildingSMART International
protectedContentAvoided: true
acceptDryRun: blocked
acceptBlockers:
  - accepted link points to unverified resource
  - accepted external resource missing lastCheckedAt
proposedStatus: KEEP_NEEDS_REVIEW
```

Assessment: the link rationale is node-specific and the official source-family page matches the Resource title. However, accepted-link validation currently blocks because the Resource remains unverified and lacks `lastCheckedAt`. No learner visibility should be allowed.

## Link B: WBDG Fire Protection -> Fire Protection

```yaml
linkId: nrl_68b933e6-36b9-4dbb-a628-8a5d923fc485
resourceId: res_115f8683-e9a2-4ce8-9575-d6b9b6c9ce40
resourceTitle: Fire Protection | WBDG - Whole Building Design Guide
nodeId: VTN-DOM-0000056
nodeLabel: Fire Protection
relationship: provides_design_guidance
currentStatus: needs_review
learnerEligible: false
learnerExposure: false
resourceVerificationStatus: unverified
resourceDisplayPolicy: reviewer_only
sourceFamilyIds:
  - wbdg_nibs
storedLocator: https://wbdg.org/do/secure/fire-protection
storedLocatorFinalUrl: https://www.wbdg.org/
storedLocatorPublicTitle: WBDG Home | WBDG - Whole Building Design Guide
exactOfficialLocatorChecked: https://www.wbdg.org/do/secure/fire-protection
exactLocatorHttpStatus: 200
exactLocatorPublicTitle: Fire Protection | WBDG - Whole Building Design Guide
protectedContentAvoided: true
acceptDryRun: blocked
acceptBlockers:
  - accepted link points to unverified resource
  - accepted external resource missing lastCheckedAt
proposedStatus: KEEP_NEEDS_REVIEW
```

Assessment: the node relation is direct, but the stored non-`www` URL redirects to the WBDG home page. The exact `www` locator resolves to the expected official page. Because Resource metadata correction and verification are not part of this accepted-link status change, the link should remain `needs_review` pending source locator correction and Resource verification.

## Link C: Uniclass -> Classification Systems

```yaml
linkId: nrl_d2eb1f9c-7502-40bf-a7d8-ae2c50bd2477
resourceId: res_4b0866ea-2ae0-4172-8f43-ea3d34ffd67c
resourceTitle: Uniclass, delivered by NBS
nodeId: VTN-DOM-0000093
nodeLabel: Classification Systems
relationship: provides_classification
currentStatus: needs_review
learnerEligible: false
learnerExposure: false
resourceVerificationStatus: unverified
resourceDisplayPolicy: reviewer_only
sourceFamilyIds:
  - uniclass_nbs
officialLocatorChecked: https://uniclass.thenbs.com/
finalUrl: https://uniclass.thenbs.com/
httpStatus: 200
publicTitle: Uniclass, delivered by NBS
protectedContentAvoided: true
acceptDryRun: blocked
acceptBlockers:
  - accepted link points to unverified resource
  - accepted external resource missing lastCheckedAt
proposedStatus: KEEP_NEEDS_REVIEW
```

Assessment: the link rationale is node-specific and the official source-family page matches the Resource title. However, accepted-link validation currently blocks because the Resource remains unverified and lacks `lastCheckedAt`. No learner visibility should be allowed.

## Questions For Reviewer

1. Is any link safe to mark `accepted` under current Resource Layer gates?
2. Should any link remain `needs_review` because the Resource is still unverified?
3. Should WBDG be treated as blocked by source locator correction before accepted-link review?
4. Are the relations node-specific enough for continued reviewer-only tracking?
5. Is learner visibility allowed for any link?
6. Are any claims overbroad, source-truth-claiming, compliance-claiming, current/governing, AHJ, or jurisdictional?
7. Is any graph/canonical mutation justified by this link review?

## Codex Proposed Actions

| Link | Proposed action | Reason |
|---|---|---|
| buildingSMART IFC -> BIM Schemas | keep `needs_review`; append transaction-backed review note | Source page matches, but accepted-link validation blocks on unverified Resource and missing `lastCheckedAt`. |
| WBDG Fire Protection -> Fire Protection | keep `needs_review`; append transaction-backed review note | Stored locator needs correction; accepted-link validation blocks on unverified Resource and missing `lastCheckedAt`. |
| Uniclass -> Classification Systems | keep `needs_review`; append transaction-backed review note | Source page matches, but accepted-link validation blocks on unverified Resource and missing `lastCheckedAt`. |

No Resource metadata mutation, learner exposure, graph/canonical mutation, or new link creation is proposed.
