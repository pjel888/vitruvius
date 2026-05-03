# Phase 6 Node Sidebar Resource Strategy

Date: 2026-05-03T03:45:00+08:00

## Goal

Define how the right sidebar should display resources for a selected node, balancing trustworthiness with usefulness.

## Current Sidebar Behavior

The `NodeInspector` Sources tab already renders `ResourceReference` cards with:
- Title, subtitle, authors, organization/publisher/year
- Display score (percent)
- Resource type, source authority, verification status, review status, access type badges
- Chapter/section/page references
- Local file indicator

Current filtering: `RESOURCE_ELIGIBLE_NODE_TYPES` restricts sources to concept/topic/subtopic nodes.

## Resource Categories for Sidebar Display

| Category | User Visibility | Badge | Sort Priority |
|----------|----------------|-------|---------------|
| `accepted_node_resource_link` | ✅ Always show | "Verified" / green | 1 |
| `human_reviewed_link` | ✅ Always show | "Reviewed" / green | 1 |
| `needs_review_link` | ⚠️ Dev/reviewer only | "Needs review" / amber | 2 |
| `candidate_resource` | ❌ Hidden from users | "Candidate" / blue | 3 (dev only) |
| `local_file_candidate` | ❌ Hidden until admitted | "Local file" / neutral | 3 (dev only) |
| `standards_context_incomplete` | ⚠️ Show with warning | "Context incomplete" / amber | 2 |
| `rejected_resource` | ❌ Never show | — | Hidden |
| `source_family_reference` | ✅ Show as attribution | Family label / neutral | 4 |
| `external_url_candidate` | ❌ Hidden until verified | — | 3 (dev only) |
| `book_or_pdf_candidate` | ❌ Hidden until verified | — | 3 (dev only) |
| `protected_or_rights_limited_source` | ⚠️ Show with rights notice | "Rights limited" / amber | 2 |

## Sidebar Behavior Rules

### Primary View (Learner-Facing)

- Show only `accepted` and `human_reviewed` links.
- Rank by display score (highest first).
- Target: 3–8 resources per node.
- Show source-family attribution subtly (e.g., small text below title).
- Show standards-context completeness indicator:
  - Green check: edition + jurisdiction + scope present
  - Amber dot: partial context
  - Red dot: missing context (do not show as governing)

### Reviewer/Dev View (Toggle or `/dev/resource-review`)

- Show all link statuses.
- Group by: accepted / needs_review / candidates / local files / rejected.
- Display raw scores and penalty breakdowns.
- Allow inline review actions.

### Warning Badges

- Missing evidence: "No verified sources"
- Incomplete standard: "Standard context incomplete — not a compliance claim"
- General web source: "Web source — verify before use"
- Unverified: "Unverified — pending review"
- Rights limited: "Excerpt limited — full text restricted"

### Standards Display Policy

- ASCE/ACI links without edition/version/scope MUST show "context incomplete" and MUST NOT imply governing/current status.
- No placeholder text like "latest edition" or "current code" is permitted.
- If a standard link is accepted but context is incomplete, show it with a visible caveat, not as a primary reference.

### Local File Display Policy

- Local files are NOT shown in the learner sidebar until admitted via review workflow.
- Admitted local files show "Local file" badge with hash verification status.
- Unadmitted local files appear only in the reviewer local-files tab.

## Implementation Notes

- The existing `rankNodeResources` and `displayScore` logic in `api/resourceLayer/ranking.ts` already supports most of this.
- The `NodeInspector` already renders `ResourceReference` cards; the main gap is filtering by view mode and adding warning badges.
- No schema changes needed for Phase 6A; use existing `reviewStatus`, `verificationStatus`, and `standardReviewContext` fields.
