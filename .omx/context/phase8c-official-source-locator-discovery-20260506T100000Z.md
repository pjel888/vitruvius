# Phase 8C Official Source Locator Discovery Context

## Task
Phase 8C Autopilot: discover official public source locators, persist reviewer-only evidence candidates where safe, promote safe candidates to reviewer-only Resources, create nodeResourceLinks only with node-specific rationale, and keep graph/canonical and learner exposure safe.

## Desired Outcome
- At least one safe reviewer-only Resource or nodeResourceLink, or a complete blocker proof.
- No fake metadata, no protected content payload, no learner exposure, no graph/canonical mutation.
- Delegated external AI review recorded honestly.

## Known Facts
- Baseline commit: `18bb2739deec4effba833e6e88ab81e3dc5038ae`.
- Baseline counts: 7 Resources, 9 nodeResourceLinks, 12 external candidates.
- Candidate statuses: 2 duplicate candidates, 10 needs_review source-family references.
- Graph metrics: 264 admitted relationships, 13,670 base edges, 13,934 effective edges, 0 CROSS_DOMAIN_EQUIVALENT, 22 CROSS_DOMAIN_ALIGNMENT.

## Constraints
- Official-source checks only.
- No protected standards content download or storage.
- No source-truth, current/governing/compliance/AHJ claims.
- Every Resource Layer write must be transaction-manifest-backed.
- Delegated AI review is not human review.

## Likely Touchpoints
- `006_System-Manifests/resource-layer/external-metadata-candidates.json`
- `006_System-Manifests/resource-layer/resources.json`
- `006_System-Manifests/resource-layer/node-resource-links.json`
- `api/resourceLayer/externalCandidatePromotionApply.ts`
- `api/resourceLayerExternalCandidatePromotionApply.test.ts`
- `.ai/13_research/phase8c_*`
