---
id: rel-concept-lot-occupancy-depends-on-concept-light-and-ventilation
title: concept-lot-occupancy depends_on concept-light-and-ventilation
page_type: relationship
relationship_type: depends_on
from_entity: concept-lot-occupancy
to_entity: concept-light-and-ventilation
trust_level: unverified
canonical_status: promoted
confidence_score: 1.0
promotion_batch_id: 20260505T115116Z_10f901e8
promotion_audit_log_ref: 006_System-Manifests\runs\kg_pipeline_20260505T095933Z\promotion_audit.log
last_promoted_utc: 20260505T115116Z
evidence:
- source_id: concept-lot-occupancy
  source_section_id: section-708
  evidence_snippet: '- (a) Dwelling Location and Lot Occupancy. The dwelling shall occupy not more than ninety percent of a corner lot and eighty percent of an inside lot, and subject to the provisions on Easement on Light and View of the Civil Code of the Philippines, shall be at least 2 meters from the property line. '
  review_decision: keep
  reviewer_model: unknown
  reviewer_provider: ollama
  reviewer_confidence: 1.0
  reviewer_reason: skip_review pipeline path for law-national-building-code-of-the-philippines-961fec
  local_review_decision: keep
  local_reviewer_confidence: 1.0
  extracted_at_utc: 20260505T115116Z
  reviewed_at_utc: 20260505T115116Z
  raw_source_trust_level: null
  source_trust_normalized_from: null
---

# concept-lot-occupancy depends_on concept-light-and-ventilation

## Relationship Summary

Promoted relationship of type `depends_on` from `concept-lot-occupancy` to `concept-light-and-ventilation`.

## Evidence

### Evidence 1 - `concept-lot-occupancy` §section-708

> - (a) Dwelling Location and Lot Occupancy. The dwelling shall occupy not more than ninety percent of a corner lot and eighty percent of an inside lot, and subject to the provisions on Easement on Light and View of the Civil Code of the Philippines, shall be at least 2 meters from the property line. 

- Reviewer: `unknown` · Decision: `keep` · Confidence: `1.0`
- Reviewed: 20260505T115116Z
- Batch: `20260505T115116Z_10f901e8`

