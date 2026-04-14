---
id: rel-concept-occupancy-separation-affects-concept-occupancy-classification
title: concept-occupancy-separation affects concept-occupancy-classification
page_type: relationship
relationship_type: affects
from_entity: concept-occupancy-separation
to_entity: concept-occupancy-classification
trust_level: unverified
canonical_status: promoted
confidence_score: 0.9
promotion_batch_id: 20260414T042840Z_befa550c
promotion_audit_log_ref: 006_System-Manifests/runs/latest_promotion_audit.log
last_promoted_utc: 20260414T042840Z
evidence:
- source_id: concept-occupancy-separation
  source_section_id: section-703
  evidence_snippet: 'building shall be subject to the most restrictive requirement pertaining to any of the type of occupancy found therein except in the following: - (1) When a one-storey building houses more than one occupancy, each portion of the building shall conform to the requirement of the particular occupancy h'
  review_decision: keep
  reviewer_model: gemma4:31b
  reviewer_confidence: 0.9
  reviewer_reason: The example shows that the occupancy type (concept-occupancy-classification) dictates the requirements for the building, which is directly affected by the separation of occupancy types (concept-occupancy-separation).
  extracted_at_utc: 20260414T042840Z
  reviewed_at_utc: 20260414T042840Z
---

# concept-occupancy-separation affects concept-occupancy-classification

## Relationship Summary

Promoted relationship of type `affects` from `concept-occupancy-separation` to `concept-occupancy-classification`.

## Evidence

### Evidence 1 - `concept-occupancy-separation` §section-703

> building shall be subject to the most restrictive requirement pertaining to any of the type of occupancy found therein except in the following: - (1) When a one-storey building houses more than one occupancy, each portion of the building shall conform to the requirement of the particular occupancy h

- Reviewer: `gemma4:31b` · Decision: `keep` · Confidence: `0.9`
- Reviewed: 20260414T042840Z
- Batch: `20260414T042840Z_befa550c`

