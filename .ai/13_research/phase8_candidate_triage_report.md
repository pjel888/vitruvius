# Phase 8 Candidate Triage Report

**Date:** 2026-05-06
**Status:** TRIAGED_NO_PROMOTION_READY_CANDIDATES
**Input registry:** `006_System-Manifests/resource-layer/external-metadata-candidates.json`
**Candidate count:** 12
**Review posture:** reviewer-only, unverified, no learner exposure

## Baseline Counts

| Registry | Count |
|---|---:|
| Resources | 7 |
| nodeResourceLinks | 9 |
| External metadata candidates | 12 |
| Learner-visible external candidates | 0 |
| Resource candidates | 4 |

## Triage Summary

No external metadata candidate is currently safe for resource-only promotion or resource-and-links promotion.

Reasons:

- No candidate is `ready_for_promotion_review`.
- ASCE 7 still lacks complete real edition/version/year/scope/applicability/source context.
- Earth Retaining Structures still lacks explicit rights/access/source-custody completion.
- Ten source-family reference candidates have `minimal_metadata` and `no_stable_identifier` warnings and no exact source locator in the candidate record.
- Creating a Resource, nodeResourceLink, graph edge, or learner-visible evidence item from the current candidate state would require either inventing metadata or bypassing review gates.

## Candidate Triage Table

| Candidate | Current status | Classification | Promotion readiness | Link readiness | Recommended action |
|---|---|---|---|---|---|
| `ext-cand-asce-7-minimum-design-loads-and-associat-mosyi54p-miqu` | `standards_context_in_review` | `standards_context_needed` | Blocked: no complete edition/version/year/scope/applicability/source context | Blocked: proposed wind/seismic nodes exist, but standards context and accepted-link gates are incomplete | Keep reviewer-only; request project-owner supplied real standards context or future official metadata packet. |
| `ext-cand-earth-retaining-structures-mosyi54y-jp9m` | `source_custody_in_review` | `rights_review_needed`, `source_custody_needed` | Blocked: rights/access/source custody incomplete despite prior bounded FHWA metadata check | Blocked: node relevance exists for retaining/earth structures, but accepted-link gates need rights/access and custody completion | Keep reviewer-only; plan rights/access review before promotion. |
| `ext-cand-buildingsmart-international-source-famil-motn39h2-hl6o` | `needs_review` | `metadata_correction_needed`, `source_custody_needed` | Blocked: no exact URL/stable identifier | Blocked: no proposed node-specific rationale | Defer until exact official source locator and rights/access context are provided. |
| `ext-cand-american-institute-of-steel-construction-motn39hs-lz60` | `needs_review` | `metadata_correction_needed`, `source_custody_needed`, `rights_review_needed` | Blocked: no exact URL/stable identifier; steel standards may require edition/context caution | Blocked: no proposed node-specific rationale | Defer until exact official source locator and rights/access context are provided. |
| `ext-cand-american-institute-of-architects-source--motn39ic-iz2k` | `needs_review` | `metadata_correction_needed`, `source_custody_needed`, `rights_review_needed` | Blocked: no exact URL/stable identifier | Blocked: no proposed node-specific rationale | Defer until exact official source locator and rights/access context are provided. |
| `ext-cand-u-s-access-board-source-family-reference-motolt33-ec7n` | `needs_review` | `metadata_correction_needed`, `source_custody_needed` | Blocked: no exact URL/stable identifier, despite trusted source family metadata | Blocked: no proposed node-specific rationale | Defer until exact official source locator and rights/access context are provided. |
| `ext-cand-whole-building-design-guide-nibs-source--motolt3q-wfyt` | `needs_review` | `metadata_correction_needed`, `source_custody_needed` | Blocked: no exact URL/stable identifier | Blocked: no proposed node-specific rationale | Defer until exact official source locator and rights/access context are provided. |
| `ext-cand-institution-of-structural-engineers-sour-motolt47-okhh` | `needs_review` | `metadata_correction_needed`, `source_custody_needed`, `rights_review_needed` | Blocked: no exact URL/stable identifier | Blocked: no proposed node-specific rationale | Defer until exact official source locator and rights/access context are provided. |
| `ext-cand-institution-of-civil-engineers-source-fa-motolt4p-a01t` | `needs_review` | `metadata_correction_needed`, `source_custody_needed`, `rights_review_needed` | Blocked: no exact URL/stable identifier | Blocked: no proposed node-specific rationale | Defer until exact official source locator and rights/access context are provided. |
| `ext-cand-royal-institute-of-british-architects-so-motolt57-il7t` | `needs_review` | `metadata_correction_needed`, `source_custody_needed`, `rights_review_needed` | Blocked: no exact URL/stable identifier | Blocked: no proposed node-specific rationale | Defer until exact official source locator and rights/access context are provided. |
| `ext-cand-uniclass-nbs-source-family-reference-motq601s-0s68` | `needs_review` | `metadata_correction_needed`, `source_custody_needed`, `rights_review_needed` | Blocked: no exact URL/stable identifier; source family not allowed as primary rule source | Blocked: no proposed node-specific rationale | Defer until exact official source locator and rights/access context are provided. |
| `ext-cand-omniclass-csi-source-family-reference-motq602f-ktvr` | `needs_review` | `metadata_correction_needed`, `source_custody_needed`, `rights_review_needed` | Blocked: no exact URL/stable identifier; source family not allowed as primary rule source | Blocked: no proposed node-specific rationale | Defer until exact official source locator and rights/access context are provided. |

## Source-Context Notes

- ASCE 7 has prior bounded official ASCE public landing-page metadata review. That did not complete edition/version/year/scope/applicability context and did not authorize current/governing/compliance/AHJ claims.
- Earth Retaining Structures has prior bounded official FHWA page metadata review. HTTP success and title match did not complete rights/access/source custody and did not create source truth.
- The ten source-family candidates came from repo-local source-family metadata and Kimi delegated review only. They are useful intake seeds, not promotable resources.

## Resource-Only Promotion Gate

Result: **blocked for all candidates**.

Required gates that are not currently satisfied:

- `ready_for_promotion_review` status.
- Complete metadata or justified missing metadata.
- Rights/access and source custody context.
- Standards context for standard-like candidates.
- Reviewer/rationale/sourceOfContext for promotion, not just intake/review.
- Transaction-backed apply and rollback for any Resource write.

## Resource-And-Links Gate

Result: **blocked for all candidates**.

Required gates that are not currently satisfied:

- A Resource candidate promoted through `resource_only` or equivalent safe gating.
- Explicit node-specific rationale for each proposed node.
- Link status and learner eligibility computed from accepted gates, not manually asserted.
- Transaction-backed apply and rollback for Resource plus nodeResourceLinks.

## Graph/Node/Edge Gate

Result: **blocked for mutation**.

Current candidates do not provide enough accepted Resource/Link evidence to mutate graph nodes, admit graph edges, or add graph metadata. Any graph work would require a separate evidence-backed packet with provenance, relation-vocabulary review, transaction manifest, rollback, delegated review, and visual verification.

## Safe Next Actions

1. Ask project owner for real ASCE 7 edition/version/year/scope/applicability/source context if ASCE promotion is desired.
2. Complete Earth Retaining Structures rights/access/source-custody review before promotion.
3. Supply exact official URLs and rights/access context for source-family candidates.
4. If no candidate source context is available, focus Phase 8 on Explorer/NodeInspector visual clarity and final closure without Resource/graph mutation.

## Safety Outcome

- No candidate was promoted.
- No Resource was created.
- No nodeResourceLink was created.
- No graph/canonical registry mutation occurred.
- No P0/high-risk P1 work occurred.
- No learner exposure occurred.
- No external source check was performed during this triage.
