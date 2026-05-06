# Phase 7 Candidate Intake Wave 3 Review Packet

**Date:** 2026-05-06
**Reviewer requested:** Kimi delegated external AI reviewer

This is delegated external AI review, not biological human review, not source truth, and not production approval by itself.

## Request

Review whether the following repo-local source-family references are safe to persist as unverified, reviewer-only external metadata candidates.

Do not approve source truth, verification, promotion, Resource creation, nodeResourceLink creation, learner exposure, graph/canonical mutation, current/governing/compliance/AHJ claims, DOI/ISBN claims, or external source checks.

## Baseline

- Resources: 7
- nodeResourceLinks: 9
- External metadata candidates: 10
- Learner-visible external metadata candidates: 0
- Existing source-family candidates are reviewer-only and unverified or `needs_review`.

## Candidates

| Proposed title | Source family ID | Repo-local source metadata | Proposed candidate defaults |
|---|---|---|---|
| Uniclass / NBS Source Family Reference | `uniclass_nbs` | label `Uniclass / NBS`; domains `thenbs.com`, `uniclass.thenbs.com`; organization `NBS`; authority `industry_body`; typical type `classification_system`; classification/construction source context | `candidate`, `unverified`, `reviewer_only`, `learnerVisible=false`, no auto verification/promotion/linking/exposure |
| OmniClass / CSI Source Family Reference | `omniclass_csi` | label `OmniClass / CSI`; domains `csiresources.org`, `csinet.org`; organization `Construction Specifications Institute`; authority `industry_body`; typical type `classification_system`; construction/specification taxonomy context | `candidate`, `unverified`, `reviewer_only`, `learnerVisible=false`, no auto verification/promotion/linking/exposure |

## Proposed Recommendation

`PASS_PERSIST_REVIEWER_ONLY_SOURCE_FAMILY_REFERENCES` for both candidates.

Rationale:

- Metadata comes only from repo-local `source-families.json`.
- No exact URL/source page is asserted.
- No source verification is claimed.
- No learner exposure is allowed.
- Both candidates are source-family references for future source-custody work, not accepted Resources.

## Required Verdict

Return one verdict:

- `PASS_PERSIST_REVIEWER_ONLY_SOURCE_FAMILY_REFERENCES`
- `PASS_ZERO_CANDIDATES_INTAKE_READY`
- `DEFER_MISSING_METADATA`
- `BLOCK_FAKE_OR_UNSAFE_METADATA`
- `NEEDS_PROJECT_OWNER_METADATA`

Also state whether either candidate implies source verification, source truth, current/governing/compliance status, AHJ/jurisdiction applicability, learner trust, Resource creation, link creation, or graph/canonical mutation.
