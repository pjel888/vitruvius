---
id: rel-concept-stairs-requires-concept-means-of-egress
title: concept-stairs requires concept-means-of-egress
page_type: relationship
relationship_type: requires
from_entity: concept-stairs
to_entity: concept-means-of-egress
trust_level: unverified
canonical_status: promoted
confidence_score: 0.9
promotion_batch_id: 20260417T183839Z_068e0cf4
promotion_audit_log_ref: 006_System-Manifests/runs/datasets/laws-completed-aggregate/source_to_graph/20260417T183342Z/promotion_audit.log
last_promoted_utc: 20260417T183839Z
evidence:
- source_id: concept-stairs
  source_section_id: section-10.2.5.4
  evidence_snippet: 'Where specifically permitted for individual occupancies by Divisions 8 to 17 of this Chapter, spiral stairs as a component of means of egress shall comply with the following:'
  review_decision: keep
  reviewer_model: gemma4:31b
  reviewer_confidence: 0.9
  reviewer_reason: 'pre_review_filter: concept_requires_pattern: concept->concept, occ>=2, ''shall comply'' language'
  extracted_at_utc: 20260417T183839Z
  reviewed_at_utc: 20260417T183839Z
---

# concept-stairs requires concept-means-of-egress

## Relationship Summary

Promoted relationship of type `requires` from `concept-stairs` to `concept-means-of-egress`.

## Evidence

### Evidence 1 - `concept-stairs` §section-10.2.5.4

> Where specifically permitted for individual occupancies by Divisions 8 to 17 of this Chapter, spiral stairs as a component of means of egress shall comply with the following:

- Reviewer: `gemma4:31b` · Decision: `keep` · Confidence: `0.9`
- Reviewed: 20260417T183839Z
- Batch: `20260417T183839Z_068e0cf4`

