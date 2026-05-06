# Full Autopilot Candidate Intake Batches

Date: 2026-05-07 local

No new reviewer-only external metadata candidates were persisted in the source-family locator units.

Reason:

- The highest-value unblocked lane was correcting official source-family locators for existing candidates rather than adding new candidates.
- Nine existing source-family candidates had enough official public locator evidence to move to `source_custody_in_review`.
- RIBA initially remained blocked because the checked `architecture.com` locator redirects to `riba.org`, which was not in the controlled RIBA source-family domain list.
- A separate RIBA domain review later added `riba.org` support and moved the existing RIBA candidate to `source_custody_in_review`.

Counts after this unit:

| Item | Count |
|---|---:|
| Resources | 10 |
| nodeResourceLinks | 12 |
| accepted nodeResourceLinks | 9 |
| external metadata candidates | 15 |
| `source_custody_in_review` external candidates | 10 |
| `needs_review` source-family candidates | 0 |
| learner-visible external candidates | 0 |

Next safe intake action: evaluate whether the ten source-family candidates should remain candidate-only evidence, be deferred/rejected as non-promotable source-family references, or receive future Resource-specific intake packets. Do not promote the source-family references as Resources without a separate non-duplicate Resource packet and reviewer support.
