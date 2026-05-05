# Phase 7A Candidate Source Discovery

**Date:** 2026-05-06
**Discovery rule:** repo-local metadata only; no web/API/source verification.

## Sources Inspected

- `006_System-Manifests/resource-layer/resource-candidates.json`
- `006_System-Manifests/resource-layer/resources.json`
- `006_System-Manifests/resource-layer/node-resource-links.json`
- `006_System-Manifests/resource-layer/external-metadata-candidates.json`
- `006_System-Manifests/resource-layer/review-decisions.json`
- `006_System-Manifests/resource-layer/source-families.json`
- `006_System-Manifests/resource-layer/local-file-index.json`
- `.ai/13_research/phase7_first_candidate_batch_reviewer_plan.md`
- `.ai/13_research/phase7_first_candidate_batch_queue.md`
- `.ai/13_research/phase7_production_evidence_curation_plan.md`
- `.ai/13_research/phase7_entry_gate.md`

## Existing Registry Baseline

- Resources: 7.
- nodeResourceLinks: 9.
- Resource candidates: 4.
- External metadata candidates: 0.
- Review decisions: 0.
- Indexed local files: 25.

## Candidate Discovery Table

| Proposed item | Candidate type | Repo metadata source | Recommendation | Warning flags | Missing fields / caveats |
|---|---|---|---|---|---|
| ASCE 7: Minimum Design Loads and Associated Criteria for Buildings and Other Structures | `standard_candidate` | `resource-candidates.json` entries `cand-asce-7-wind-load`, `cand-asce-7-seismic-load`; `resources.json` record `res-asce-7-official-landing`; `source-families.json` family `asce` | `persist_reviewer_only_candidate` if delegated reviewer approves | URL syntax only; standard candidate not learner trusted; missing edition/version; missing jurisdiction/scope | No edition, version, section, adoption, AHJ, or source truth. Existing Resource record remains incomplete and not learner-trusted. |
| Earth Retaining Structures | `external_url_candidate` | `resource-candidates.json` entry `cand-fhwa-retaining-wall`; `resources.json` record `res-fhwa-earth-retaining-structures`; `source-families.json` family `fhwa` | `persist_reviewer_only_candidate` if delegated reviewer approves | URL syntax only; reachability not verified | Scope remains U.S. federal transportation/geotechnical context. No learner trust or accepted link. |
| American Institute of Steel Construction source family reference | `source_family_reference` | `source-families.json` family `aisc` | `defer_missing_metadata` | minimal metadata; no stable identifier | No specific resource URL, DOI, ISBN, title, edition, or rights record. Safe as planning note, but not recommended for first persistence batch. |

## Preview Validation Results

The no-write preview helper accepted all three proposal shapes without fake placeholder flags:

- ASCE 7 preview: `ok=true`; `learnerVisible=false`; `displayPolicy=reviewer_only`; `verificationStatus=unverified`; warning flags include missing edition/version and jurisdiction/scope.
- FHWA preview: `ok=true`; `learnerVisible=false`; `displayPolicy=reviewer_only`; `verificationStatus=unverified`; warning flags include URL syntax accepted but reachability not verified.
- AISC source-family preview: `ok=true`; `learnerVisible=false`; `displayPolicy=reviewer_only`; `verificationStatus=unverified`; warning flags include `minimal_metadata` and `no_stable_identifier`.

## Excluded Items

- `cand-aci-318-structural-column` was excluded because it touches ACI 318 / concrete context and the prompt forbids P0 Concrete/Reinforced Concrete work.
- No local file candidates were persisted because local file custody/admission is a separate reviewer workflow and the current local index is hash metadata only.

## Candidate Defaults Required If Persisted

- `status`: `candidate`.
- `verificationStatus`: `unverified`.
- `displayPolicy`: `reviewer_only`.
- `learnerVisible`: `false`.
- `reviewRequired`: `true`.
- `noAutoVerification`: `true`.
- `noAutoPromotion`: `true`.
- `noAutoLinking`: `true`.
- `noLearnerExposure`: `true`.
