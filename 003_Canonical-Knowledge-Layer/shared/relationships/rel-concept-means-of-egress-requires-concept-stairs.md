---
id: rel-concept-means-of-egress-requires-concept-stairs
title: concept-means-of-egress requires concept-stairs
page_type: relationship
relationship_type: requires
from_entity: concept-means-of-egress
to_entity: concept-stairs
trust_level: unverified
canonical_status: promoted
confidence_score: 0.9
promotion_batch_id: 20260423T215703Z_b2563c62
promotion_audit_log_ref: 006_System-Manifests/runs/kg_pipeline_20260423T184105Z/promotion_audit.log
last_promoted_utc: 20260423T215703Z
evidence:
- source_id: concept-means-of-egress
  source_section_id: section-3.409
  evidence_snippet: Where a single means· of egress consists of a combination of inside stairs and fire escape stairs, each shall comply with the applicable provisions of this Rule, and the two shall be so arranged and connected as to provide a con· tinuous safe path of travel.
  review_decision: keep
  reviewer_model: qwen2.5:3b
  reviewer_provider: ollama
  reviewer_confidence: 0.9
  reviewer_reason: 'pre_review_filter: concept_requires_pattern: concept->concept, occ>=2, ''shall comply'' language'
  local_review_decision: keep
  local_reviewer_confidence: 0.9
  extracted_at_utc: 20260423T213643Z
  reviewed_at_utc: 20260423T213643Z
- source_id: concept-means-of-egress
  source_section_id: section-10.2.5.10
  evidence_snippet: Where a single means of egress consists of a combination of inside stairs and fire escape stairs, each shall comply with the applicable provision of this Chapter, and the two shall be so arranged and connected as to provide a continuous safe path of travel.
  review_decision: keep
  reviewer_model: qwen2.5:3b
  reviewer_provider: ollama
  reviewer_confidence: 0.9
  reviewer_reason: 'pre_review_filter: concept_requires_pattern: concept->concept, occ>=2, ''shall comply'' language'
  local_review_decision: keep
  local_reviewer_confidence: 0.9
  extracted_at_utc: 20260423T215703Z
  reviewed_at_utc: 20260423T215703Z
---

# concept-means-of-egress requires concept-stairs

## Relationship Summary

Promoted relationship of type `requires` from `concept-means-of-egress` to `concept-stairs`.

## Evidence

### Evidence 1 - `concept-means-of-egress` §section-3.409

> Where a single means· of egress consists of a combination of inside stairs and fire escape stairs, each shall comply with the applicable provisions of this Rule, and the two shall be so arranged and connected as to provide a con· tinuous safe path of travel.

- Reviewer: `qwen2.5:3b` · Decision: `keep` · Confidence: `0.9`
- Reviewed: 20260423T213643Z
- Batch: `20260423T215703Z_b2563c62`

### Evidence 2 - `concept-means-of-egress` §section-10.2.5.10

> Where a single means of egress consists of a combination of inside stairs and fire escape stairs, each shall comply with the applicable provision of this Chapter, and the two shall be so arranged and connected as to provide a continuous safe path of travel.

- Reviewer: `qwen2.5:3b` · Decision: `keep` · Confidence: `0.9`
- Reviewed: 20260423T215703Z
- Batch: `20260423T215703Z_b2563c62`
