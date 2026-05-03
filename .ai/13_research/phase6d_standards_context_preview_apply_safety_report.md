# Phase 6D Standards-Context Preview/Apply Safety Report

Date: 2026-05-03T05:15:00+08:00

## Routes Reviewed

- `GET /resources/review/standards/:id`
- `POST /resources/review/standards/:id/context-preview`
- `POST /resources/review/standards/:id/context-decision`

## Safety Checks

| Requirement | Status | Implementation |
|-------------|--------|----------------|
| Preview catches placeholder values | ✅ Yes | `validateStandardsContextDecisionBody` calls `isPlaceholderStandardContextValue` on all context fields |
| Preview distinguishes warning vs blocker | ✅ Yes | `buildStandardsContextResponse` returns `validationImpact` with `ok`, `warnings`, `blockers` |
| Apply requires admin/dev gate | ✅ Yes | `previewOrApplyStandardsContext` uses `apply` flag; API route gates mutations behind `isLocalDevAdminGateOpen` |
| Apply requires reviewer/rationale/sourceOfContext for complete/not-required/justified-missing | ✅ Yes | `validateStandardsContextDecisionBody` enforces `sourceOfContext` for `update_context_complete`, `mark_context_not_required`, `promote_if_context_complete` |
| Apply does not allow learner-trusted promotion with missing context | ✅ Yes | `previewOrApplyStandardsContext` throws if `promote_if_context_complete` requested but context still missing |
| Apply writes transaction manifest if production data changes | ✅ Yes | `withResourceLayerTransaction` writes manifest with before/after hashes |
| Apply does not auto-promote resource/link status unless explicitly requested and valid | ✅ Yes | Only `promote_if_context_complete` changes `link.reviewStatus` to `accepted`; all other decisions keep or demote status |
| Apply does not infer edition/version/scope | ✅ Yes | No inference logic; only uses values explicitly supplied in the decision body |

## Gap Fixed in 6D

`hasStructuredContextJustification` in `reviewWorkflow.ts` previously did not reject placeholder values in `reviewedBy`, `rationale`, or `sourceOfContext`. This created a discrepancy where the preview/apply workflow could permit a promotion that full validation would block.

**Fix applied:** `hasStructuredContextJustification` now explicitly checks `isPlaceholderStandardContextValue` on all three justification fields, matching the stricter `hasStructuredMissingContextJustification` in `validation.ts`.

## Tests Added

- `justified missing context with placeholder rationale is blocked` — proves preview/apply would reject fake justification
- `complete standards context requires reviewer, rationale, sourceOfContext` — proves valid context passes
- `justified missing context requires reviewer, rationale, sourceOfContext, and is not placeholder` — proves legitimate justification passes

## Conclusion

Preview/apply workflow is safe. Placeholder values are rejected. Promotion requires complete context or legitimate justification. Transaction manifests are written. No auto-inference occurs.
