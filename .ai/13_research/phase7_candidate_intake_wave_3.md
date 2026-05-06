# Phase 7 Candidate Intake Wave 3

**Date:** 2026-05-06
**Status:** validation passed, commit pending
**Scope:** reviewer-only source-family candidate intake

## Baseline

- Resources: 7
- nodeResourceLinks: 9
- External metadata candidates before wave: 10
- Learner-visible external metadata candidates: 0
- Graph/canonical/P0/high-risk P1 mutation: none

## Candidate Source Discovery

Codex inspected repo-local `006_System-Manifests/resource-layer/source-families.json` and the current `external-metadata-candidates.json`.

Two high-value source-family references remain safe for a small reviewer-only intake wave:

| Source family ID | Label | Domains in repo metadata | Reason selected |
|---|---|---|---|
| `uniclass_nbs` | Uniclass / NBS | `thenbs.com`, `uniclass.thenbs.com` | Classification source family for construction/architecture taxonomy references; not a design-code or Concrete/P0 candidate. |
| `omniclass_csi` | OmniClass / CSI | `csiresources.org`, `csinet.org` | Classification/source taxonomy family for construction/specification references; not a design-code or Concrete/P0 candidate. |

## Deferred Source Families

- `aci`: deferred because it is Concrete/Reinforced Concrete adjacent and standards-context sensitive.
- `iso`: deferred because broad standards-context handling needs exact standard/edition/scope metadata.
- `nibs`: deferred because WBDG/NIBS already exists as a candidate and this entry overlaps.
- Academic and discovery-provider families such as Crossref/OpenAlex/DataCite/CORE/Unpaywall/Open Library/Google Books/Internet Archive: deferred because they are metadata/discovery providers rather than direct high-value AEC evidence sources for this wave.
- `general_web`: deferred because it is too broad.

## Proposed Reviewer-Only Candidates

| Title | Resource type | Source type | Proposed source family | Warning flags | Missing fields |
|---|---|---|---|---|---|
| Uniclass / NBS Source Family Reference | `source_family_reference` | `industry_body_source_family` | `uniclass_nbs` | `minimal_metadata`, `no_stable_identifier` | URL, DOI, ISBN, authors, publication date, edition/version, jurisdiction/scope |
| OmniClass / CSI Source Family Reference | `source_family_reference` | `industry_body_source_family` | `omniclass_csi` | `minimal_metadata`, `no_stable_identifier` | URL, DOI, ISBN, authors, publication date, edition/version, jurisdiction/scope |

## Safety Defaults

If persisted, each candidate must remain:

- `status: candidate`
- `verificationStatus: unverified`
- `displayPolicy: reviewer_only`
- `learnerVisible: false`
- `reviewRequired: true`
- `noAutoVerification: true`
- `noAutoPromotion: true`
- `noAutoLinking: true`
- `noLearnerExposure: true`

No source verification, URL/DOI/ISBN lookup, Resource creation, nodeResourceLink creation, promotion, learner exposure, graph/canonical mutation, P0 work, or high-risk P1 work is authorized by this wave.

## Outcome

Kimi reviewed the packet as a project-owner-delegated external AI reviewer and returned `PASS_PERSIST_REVIEWER_ONLY_SOURCE_FAMILY_REFERENCES`.

Persisted candidates:

- `ext-cand-uniclass-nbs-source-family-reference-motq601s-0s68`
- `ext-cand-omniclass-csi-source-family-reference-motq602f-ktvr`

Both remain `candidate`, `unverified`, `reviewer_only`, and `learnerVisible=false`.
