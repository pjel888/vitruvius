# Full Autopilot Candidate Intake Batches

Date: 2026-05-07 local

No new reviewer-only external metadata candidates were persisted in this unit.

Reason:

- The highest-value unblocked lane was correcting official source-family locators for existing candidates rather than adding new candidates.
- Nine existing source-family candidates had enough official public locator evidence to move to `source_custody_in_review`.
- RIBA remains blocked pending controlled source-family domain review because the checked `architecture.com` locator redirects to `riba.org`, which is not currently in the allowed RIBA source-family domain list.

Counts after this unit:

| Item | Count |
|---|---:|
| Resources | 10 |
| nodeResourceLinks | 12 |
| accepted nodeResourceLinks | 9 |
| external metadata candidates | 15 |
| `source_custody_in_review` external candidates | 9 |
| `needs_review` source-family candidates | 1 |
| learner-visible external candidates | 0 |

Next safe intake action: evaluate whether the RIBA source-family domain allow-list should be reviewed through a separate source-family-domain packet; do not silently treat `riba.org` as official under the current verifier.
