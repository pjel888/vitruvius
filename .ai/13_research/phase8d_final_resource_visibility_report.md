# Phase 8D Final Resource Visibility Report

Run date: 2026-05-06

## API Visibility Contract

`GET /node/:id/resources` now treats `includeCandidates=true` as reviewer-only behavior:

- learner mode ignores `includeCandidates=true`;
- reviewer mode may include candidates only after the local dev/admin gate;
- learner mode returns only learner-eligible accepted resources.

## Target Node Verification

| Node | Learner response | Reviewer/admin response |
|---|---|---|
| BIM Schemas | no Phase 8C reviewer-only Resource returned | buildingSMART IFC returned as `needs_review` |
| Fire Protection | no Phase 8C reviewer-only Resource returned | WBDG Fire Protection returned as `needs_review` |
| Classification Systems | no Phase 8C reviewer-only Resource returned | Uniclass returned as `needs_review` |

## Exposure Result

- Learner-visible additions: 0.
- Reviewer-only Resources exposed to learner mode: 0.
- External candidates exposed to learner mode: 0.
- Reviewer/admin source-custody visibility preserved: yes.
