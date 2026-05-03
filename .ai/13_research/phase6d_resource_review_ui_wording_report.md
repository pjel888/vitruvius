# Phase 6D Resource Review UI / API Wording Report

Date: 2026-05-03T05:15:00+08:00

## UI Reviewed

- `explorer/src/components/resource-review/ResourceReviewAdmin.tsx`
- `explorer/src/components/resource-review/ResourceReviewAdmin.test.tsx`

## Risky Wording Check

| Risky Term | Found? | Location | Mitigation |
|------------|--------|----------|------------|
| "current edition" | ❌ No | — | — |
| "governing standard" | ❌ No | — | — |
| "project applicability" | ❌ No | — | — |
| "jurisdiction adoption" | ❌ No | — | — |
| "AHJ approval" | ❌ No | — | — |
| "code compliance" | ❌ No | — | — |
| "source verification" (implied) | ❌ No | — | — |
| "resource acceptance" (implied) | ❌ No | — | — |
| "learner-facing trust" (implied) | ❌ No | — | — |

## Current UI Wording

### Standards Context Card

- **Context display:** "Current context" panel shows "Edition: {value || 'not supplied'}" — neutral, not authority-claiming.
- **Promotion blockers:** "Promotion blockers" panel lists explicit blocker reasons — transparent.
- **Warning banner:** "Missing context is honest while the item remains needs_review. Do not guess edition/version, 'latest,' or jurisdiction/adoption. Promotion requires complete source-backed or reviewer-supported standards context."
- **Badges:** "missing edition/section", "promotion blocked", "needs_human_review" — factual status labels.
- **Form placeholder:** "Do not guess" on edition input — explicit anti-invention cue.

### Link Card

- **Accept button rationale:** "Accepted after reviewer confirmed edition/scope/provenance context." — confirms review requirement.
- **Hold button rationale:** "Hold for more source, section, jurisdiction, or rights context." — honest about missing context.

### Metrics Dashboard

- "Standards missing context", "Std. missing edition", "Std. promotion blocked" — factual counts, no authority claims.

## Conclusion

UI wording is already safe and does not imply compliance, governing status, or learner trust for incomplete standards. No wording changes required for 6D.
