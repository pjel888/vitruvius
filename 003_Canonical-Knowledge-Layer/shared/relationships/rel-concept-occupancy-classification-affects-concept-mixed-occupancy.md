---
id: rel-concept-occupancy-classification-affects-concept-mixed-occupancy
title: concept-occupancy-classification affects concept-mixed-occupancy
page_type: relationship
relationship_type: affects
from_entity: concept-occupancy-classification
to_entity: concept-mixed-occupancy
trust_level: unverified
canonical_status: promoted
confidence_score: 0.9
promotion_batch_id: 20260414T035210Z_0959acf9
promotion_audit_log_ref: 006_System-Manifests/runs/latest_promotion_audit.log
last_promoted_utc: 20260414T035210Z
evidence:
- source_id: concept-occupancy-classification
  source_section_id: section-703
  evidence_snippet: 'building shall be subject to the most restrictive requirement pertaining to any of the type of occupancy found therein except in the following: - (1) When a one-storey building houses more than one occupancy, each portion of the building shall conform to the requirement of the particular occupancy h'
  review_decision: keep
  reviewer_model: gemma4:31b
  reviewer_confidence: 0.9
  reviewer_reason: The example text explicitly states that the requirements for a building with more than one occupancy (mixed occupancy) are determined by the occupancy classification, indicating that occupancy classification affects the requirements for mixed occupancy buildings.
  extracted_at_utc: 20260414T035210Z
  reviewed_at_utc: 20260414T035210Z
---

# concept-occupancy-classification affects concept-mixed-occupancy

## Relationship Summary

Promoted relationship of type `affects` from `concept-occupancy-classification` to `concept-mixed-occupancy`.

## Evidence

### Evidence 1 - `concept-occupancy-classification` §section-703

> building shall be subject to the most restrictive requirement pertaining to any of the type of occupancy found therein except in the following: - (1) When a one-storey building houses more than one occupancy, each portion of the building shall conform to the requirement of the particular occupancy h

- Reviewer: `gemma4:31b` · Decision: `keep` · Confidence: `0.9`
- Reviewed: 20260414T035210Z
- Batch: `20260414T035210Z_0959acf9`

