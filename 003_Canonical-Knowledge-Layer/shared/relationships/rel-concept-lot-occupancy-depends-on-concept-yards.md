---
id: rel-concept-lot-occupancy-depends-on-concept-yards
title: concept-lot-occupancy depends_on concept-yards
page_type: relationship
relationship_type: depends_on
from_entity: concept-lot-occupancy
to_entity: concept-yards
trust_level: unverified
canonical_status: promoted
confidence_score: 1.0
promotion_batch_id: 20260505T115023Z_15687c61
promotion_audit_log_ref: 006_System-Manifests\runs\kg_pipeline_20260505T095933Z\promotion_audit.log
last_promoted_utc: 20260505T115023Z
evidence:
- source_id: concept-lot-occupancy
  source_section_id: section-803
  evidence_snippet: '- 1. The measurement of the percentage (%) of site occupancy (or lot occupancy) shall be taken at the ground level and shall be exclusive of courts, yards and light wells. Courts, yards, and light wells shall be measured clear of all projections from the walls enclosing such wells or yards with the '
  review_decision: keep
  reviewer_model: unknown
  reviewer_provider: ollama
  reviewer_confidence: 1.0
  reviewer_reason: skip_review pipeline path for law-section-rule-viii-light-ventilation
  local_review_decision: keep
  local_reviewer_confidence: 1.0
  extracted_at_utc: 20260505T115018Z
  reviewed_at_utc: 20260505T115018Z
  raw_source_trust_level: null
  source_trust_normalized_from: null
- source_id: concept-lot-occupancy
  source_section_id: section-2
  evidence_snippet: '- 2.1 The measurement of site occupancy or lot occupancy shall be taken at the ground level and shall be exclusive of courts, yards and light wells. - 2.2 Courts, yards, and light wells shall be measured clear of all projections from the walls enclosing such wells or yards with the exception of roof'
  review_decision: keep
  reviewer_model: unknown
  reviewer_provider: ollama
  reviewer_confidence: 1.0
  reviewer_reason: skip_review pipeline path for source-george-salvan-architectural-practice-and-construction-management
  local_review_decision: keep
  local_reviewer_confidence: 1.0
  extracted_at_utc: 20260505T115023Z
  reviewed_at_utc: 20260505T115023Z
  raw_source_trust_level: null
  source_trust_normalized_from: null
---

# concept-lot-occupancy depends_on concept-yards

## Relationship Summary

Promoted relationship of type `depends_on` from `concept-lot-occupancy` to `concept-yards`.

## Evidence

### Evidence 1 - `concept-lot-occupancy` §section-803

> - 1. The measurement of the percentage (%) of site occupancy (or lot occupancy) shall be taken at the ground level and shall be exclusive of courts, yards and light wells. Courts, yards, and light wells shall be measured clear of all projections from the walls enclosing such wells or yards with the 

- Reviewer: `unknown` · Decision: `keep` · Confidence: `1.0`
- Reviewed: 20260505T115018Z
- Batch: `20260505T115023Z_15687c61`

### Evidence 2 - `concept-lot-occupancy` §section-2

> - 2.1 The measurement of site occupancy or lot occupancy shall be taken at the ground level and shall be exclusive of courts, yards and light wells. - 2.2 Courts, yards, and light wells shall be measured clear of all projections from the walls enclosing such wells or yards with the exception of roof

- Reviewer: `unknown` · Decision: `keep` · Confidence: `1.0`
- Reviewed: 20260505T115023Z
- Batch: `20260505T115023Z_15687c61`

