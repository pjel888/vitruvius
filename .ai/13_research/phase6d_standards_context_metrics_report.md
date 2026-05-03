# Phase 6D Standards-Context Metrics Report

Date: 2026-05-03T05:15:00+08:00

## Current Metrics (from `ValidationResult`)

| Metric | Source | Actionable? |
|--------|--------|-------------|
| `standardsTotal` | Count of standard/code-like resources | ✅ Yes — baseline |
| `standardsMissingEdition` | Count missing edition/version | ✅ Yes — direct remediation target |
| `standardsMissingJurisdiction` | Count missing jurisdiction/geographicScope | ✅ Yes — direct remediation target |
| `standardsMissingScope` | Count missing citation/scope | ✅ Yes — direct remediation target |
| `standardsContextComplete` | Count with complete context | ✅ Yes — success metric |
| `standardsContextPartial` | Count with partial context | ✅ Yes — review queue sizing |
| `standardsContextNeedsReview` | Count in needs_review with missing context | ✅ Yes — review queue sizing |
| `standardsAcceptedMissingContext` | Count of accepted links with missing context | ✅ Yes — critical blocker |
| `standardsPromotionBlocked` | Count blocked from promotion | ✅ Yes — blocker tracking |
| `standardsContextReviewable` | Count with any missing context | ✅ Yes — review queue sizing |
| `standardsContextWarnings` | Array of warning strings | ✅ Yes — specific remediation guidance |
| `standardsContextIncomplete` | Count with any missing context (resource-level) | ✅ Yes — added in 6A |
| `standardsContextBlocked` | Count of accepted links blocked by missing context | ✅ Yes — added in 6A |

## Metrics Not Added (Intentionally)

The following metrics were requested in the task spec but judged too noisy or derivable from existing metrics:

- `standardsMissingVersion` — derivable from `standardsMissingEdition` (edition/version are checked together)
- `standardsMissingCitationContext` — derivable from `standardsMissingScope` (citation/scope is the same field)
- `standardsMissingReviewerContext` — too vague; use `standardsContextNeedsReview` instead
- `standardsContextAcceptedComplete` — derivable from `standardsContextComplete` minus `standardsAcceptedMissingContext`
- `standardsContextJustifiedMissing` — interesting but not yet needed (zero instances in current registry)
- `standardsContextPlaceholderRejected` — too granular; warnings array already captures specifics
- `standardsLearnerHidden` — derivable from `standardsPromotionBlocked`
- `standardsLearnerWarningGated` — interesting but not yet needed (zero instances in current registry)

## Metric Philosophy

Keep metrics minimal and actionable. A metric should answer one of:
1. How many items need work? → `standardsMissingEdition`, `standardsMissingScope`, `standardsPromotionBlocked`
2. How many items are done? → `standardsContextComplete`
3. What specifically is wrong? → `standardsContextWarnings`

No metric redundancy. No metric without a clear next action.
