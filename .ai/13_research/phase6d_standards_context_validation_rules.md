# Phase 6D Standards-Context Validation Rules

Date: 2026-05-03T05:00:00+08:00

## A. Accepted/Promoted Standards-Context Blockers

An accepted or promoted standard/code/governing-document link is a **blocker** if:

1. The resource `resourceType` is `standard` or `code`.
2. The link `reviewStatus` is `accepted` or `human_reviewed`.
3. Any of the following are missing:
   - edition or version
   - jurisdiction or geographicScope
   - citation/scope (sectionRefs, chapterRefs, pageRefs, or fragmentRefs on the link)
4. AND there is no structured missing-context justification.

A structured missing-context justification requires ALL of:
- `reviewContext.contextStatus` is `justified_missing` or `not_required`
- `reviewContext.reviewedBy` is present, non-empty, and not a placeholder
- `reviewContext.rationale` is present, non-empty, and not a placeholder
- `reviewContext.sourceOfContext` is present, non-empty, and not a placeholder

**Implementation:** `validateLink` in `api/resourceLayer/validation.ts` lines 292–300.

## B. Needs-Review Standards-Context Warnings

A standard/code link in `needs_review` or `candidate` status with missing context generates **warnings**, not blockers, because it is not learner-visible and not promoted.

**Implementation:** `validateLink` lines 292–297 warn for non-accepted standard links.

## C. Placeholder Rejection

The following values are rejected as standards-context fields:

- `latest`
- `current`
- `tbd`
- `todo`
- `unknown`
- `generic`
- `placeholder`
- `sample`
- `varies`
- `n/a`
- `none`
- Empty string
- Whitespace-only string

**Fields checked:** edition, version, publicationYear, jurisdiction, geographicScope, applicabilityNote, sourceOfContext, rationale, reviewedBy, adoptionStatus, codeCycle.

**Implementation:** `isPlaceholderStandardContextValue` + `hasUsableValue` in `validation.ts`; `collectPlaceholderContextWarnings` covers resource and link standardContext fields.

## D. Incomplete Context Display Messages

Validation generates these warning/blocker messages:

- `"{id}: code/standard resource missing edition/version context"`
- `"{id}: code/standard resource missing jurisdiction or geographicScope"`
- `"{linkId}: accepted standard/code-like link requires edition/version, citation/scope, and jurisdiction/geographicScope context or structured reviewer/source justification; missing {fields}"`
- `"{linkId}: ASCE link cannot be promoted without edition/section/adoption context"`
- `"{linkId}: ACI link cannot be promoted without edition/section-specific context"`
- `"{linkId}: FHWA link cannot be promoted without explicit U.S. transportation/geotechnical scope review"`

## E. Learner Sidebar Exclusion

`isLearnerSidebarEligible(link, resource)` returns `false` if:

1. `link.reviewStatus` is not `accepted` or `human_reviewed`.
2. `resource.verificationStatus` is `rejected` or `unverified`.
3. `resource` is rights-protected content.
4. The resource is standard-like AND missing context AND lacks structured justification.

## F. No Fake Completion

- `validateStandardsContextDecisionBody` in `reviewWorkflow.ts` rejects placeholder values in decision body fields.
- `previewOrApplyStandardsContext` throws if `update_context_complete` or `promote_if_context_complete` is requested but context is still missing.
- `decideNodeResourceLink` throws if `accept` is requested for a standard-like link with missing context and no justification.

## G. Hardening Applied in 6D

- `hasStructuredContextJustification` in `reviewWorkflow.ts` now rejects placeholder values in `reviewedBy`, `rationale`, and `sourceOfContext`, matching the stricter `hasStructuredMissingContextJustification` in `validation.ts`.
- This eliminates a discrepancy where the preview/apply workflow could permit a promotion that full validation would block.
