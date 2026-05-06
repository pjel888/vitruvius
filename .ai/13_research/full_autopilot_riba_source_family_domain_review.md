# Full Autopilot RIBA Source-Family Domain Review

Date: 2026-05-07 local

Scope: RIBA source-family candidate `ext-cand-royal-institute-of-british-architects-so-motolt57-il7t` and controlled RIBA source-family host support.

Required review caveat:

> This is delegated external AI review, not biological human review, not source truth, and not production approval by itself.

## Baseline

- Resources: 10.
- nodeResourceLinks: 12.
- Accepted nodeResourceLinks: 9.
- External metadata candidates: 15.
- RIBA candidate prior status: `needs_review`.
- RIBA candidate display/learner state: `displayPolicy=reviewer_only`, `learnerVisible=false`.
- RIBA source-family registry prior domains: `architecture.com`.
- RIBA verifier prior host support: `architecture.com` and subdomains only.

## Controlled Public Metadata Checks

Checks were bounded to official/public metadata:

- HEAD first where possible.
- GET only for public title/metadata inspection.
- Timeout cap: 10 seconds.
- Body inspection cap: 1 MB.
- No full page content stored.
- No protected payload, standard text, DOI lookup, ISBN lookup, rights clearance, source-truth, current/governing/compliance/AHJ, or learner-trust claim.

| Requested URL | Final URL | Result | Public metadata | Caveat |
|---|---|---|---|---|
| `https://www.architecture.com/knowledge-and-resources` | `https://www.riba.org/news/` | 301 to `riba.org`, then HTTP 200 text/html | `RIBA News`; page title metadata includes `Royal Institute of British Architects` | Redirect target required source-family host review before status advancement. |
| `https://www.riba.org/` | `https://www.riba.org/` | HTTP 200 text/html | `RIBA`; page title/metadata identifies `Royal Institute of British Architects` | Metadata-only identity check, not source truth or rights clearance. |

## Kimi Review

Reviewer: `kimi_reviewer` using `kimi, version 1.41.0`.

Verdict: `PASS_APPLY_SAFE_STATUS_DECISIONS`.

Reviewer-supported actions:

1. Add `riba.org` and subdomains to controlled RIBA source-family host matching.
2. Add `riba.org` to the RIBA `source-families.json` domain list.
3. Add focused tests for direct `riba.org` acceptance and `architecture.com` to `riba.org` redirect handling.
4. Move the RIBA candidate from `needs_review` to `source_custody_in_review` through the existing source-verification workflow.

Reviewer-required boundaries:

- Keep the candidate `verificationStatus=unverified`.
- Do not assert `source_custody_verified`.
- Do not create a Resource.
- Do not create a nodeResourceLink.
- Do not mutate graph/canonical data.
- Do not expose anything to learners.
- Do not claim rights clearance, source truth, current/governing/compliance/AHJ status, DOI/ISBN, or standard context.

## Applied Changes

Files changed:

- `api/resourceLayer/sourceVerification.ts`
- `api/resourceLayerSourceVerification.test.ts`
- `006_System-Manifests/resource-layer/source-families.json`
- `006_System-Manifests/resource-layer/external-metadata-candidates.json`
- `006_System-Manifests/resource-layer/transaction-manifests/resource-layer-tx-20260506175937-8e8a8996ae50.json`

Resource Layer transaction:

- `resource-layer-tx-20260506175937-8e8a8996ae50`

Candidate decision outcome:

| Candidate | Prior status | New status | Requested URL | Final URL | Source check title | Learner visible |
|---|---|---|---|---|---|---|
| `ext-cand-royal-institute-of-british-architects-so-motolt57-il7t` | `needs_review` | `source_custody_in_review` | `https://www.riba.org/` | `https://www.riba.org/` | `RIBA` | false |

Safety result:

- No Resource created.
- No nodeResourceLink created.
- No promotion performed.
- No graph/canonical/P0/high-risk P1 mutation.
- No learner exposure.
- No protected payload stored.
- No source-truth/current/governing/compliance/AHJ claim.

## Verification

Focused test:

- `bun test api/resourceLayerSourceVerification.test.ts`: PASS, 29 pass.

Full validation is recorded in `continuous_vitruvius_validation_log.md` for the commit unit.
