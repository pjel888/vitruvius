# Phase 8D Next Actions

Run date: 2026-05-06

## Immediate Safe Next Action

Prepare a Resource metadata/source-custody correction packet for the three reviewer-only Resources before rerunning accepted-link review.

Priority:

1. Correct the WBDG Fire Protection stored locator from `https://wbdg.org/do/secure/fire-protection` to the exact official URL `https://www.wbdg.org/do/secure/fire-protection`, only through a reviewed Resource metadata correction workflow.
2. Add or verify `lastCheckedAt` and source-custody fields only through controlled source-custody workflow; do not treat HTTP success as source truth.
3. Keep buildingSMART IFC and Uniclass reviewer-only until Resource verification/custody fields are complete.
4. Rerun accepted-link review after Resource verification/custody gates pass.

## Blocked Actions

- Accepting the three links is blocked by unverified Resources and missing `lastCheckedAt`.
- Learner exposure is blocked.
- Graph improvement is blocked until accepted evidence or a separately gated graph packet exists.

## Safety Reminders

- Do not manually set `learnerEligible=true`.
- Do not infer current/governing/compliance/AHJ status.
- Do not mutate graph/canonical/P0/high-risk P1 surfaces without a separate gated packet.
