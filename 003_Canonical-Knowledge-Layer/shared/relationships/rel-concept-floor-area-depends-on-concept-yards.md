---
id: rel-concept-floor-area-depends-on-concept-yards
title: concept-floor-area depends_on concept-yards
page_type: relationship
relationship_type: depends_on
from_entity: concept-floor-area
to_entity: concept-yards
trust_level: unverified
canonical_status: promoted
confidence_score: 1.0
promotion_batch_id: 20260505T115100Z_866434f7
promotion_audit_log_ref: 006_System-Manifests\runs\kg_pipeline_20260505T095933Z\promotion_audit.log
last_promoted_utc: 20260505T115100Z
evidence:
- source_id: concept-floor-area
  source_section_id: section-706
  evidence_snippet: The floor areas hereinabove provided may be increased in certain specific instances and under appropriate conditions, based on the existence of public space, streets or yards extending along and adjoining two or more sides of the building or structure subject to the approval of the Building Official
  review_decision: keep
  reviewer_model: unknown
  reviewer_provider: ollama
  reviewer_confidence: 1.0
  reviewer_reason: skip_review pipeline path for irr-implementing-rules-and-regulations-of-the-national-building-code
  local_review_decision: keep
  local_reviewer_confidence: 1.0
  extracted_at_utc: 20260505T115039Z
  reviewed_at_utc: 20260505T115039Z
  raw_source_trust_level: null
  source_trust_normalized_from: null
- source_id: concept-floor-area
  source_section_id: section-706
  evidence_snippet: The floor areas hereinabove provided may be increased in certain specific instances ano under appropriate conditions, based on the existence of public space. streets or yards extending along and adjoining two or more sides of the building or structure subject to the approval of the Building Official
  review_decision: keep
  reviewer_model: unknown
  reviewer_provider: ollama
  reviewer_confidence: 1.0
  reviewer_reason: skip_review pipeline path for law-national-building-code-of-the-philippines
  local_review_decision: keep
  local_reviewer_confidence: 1.0
  extracted_at_utc: 20260505T115100Z
  reviewed_at_utc: 20260505T115100Z
  raw_source_trust_level: null
  source_trust_normalized_from: null
---

# concept-floor-area depends_on concept-yards

## Relationship Summary

Promoted relationship of type `depends_on` from `concept-floor-area` to `concept-yards`.

## Evidence

### Evidence 1 - `concept-floor-area` §section-706

> The floor areas hereinabove provided may be increased in certain specific instances and under appropriate conditions, based on the existence of public space, streets or yards extending along and adjoining two or more sides of the building or structure subject to the approval of the Building Official

- Reviewer: `unknown` · Decision: `keep` · Confidence: `1.0`
- Reviewed: 20260505T115039Z
- Batch: `20260505T115100Z_866434f7`

### Evidence 2 - `concept-floor-area` §section-706

> The floor areas hereinabove provided may be increased in certain specific instances ano under appropriate conditions, based on the existence of public space. streets or yards extending along and adjoining two or more sides of the building or structure subject to the approval of the Building Official

- Reviewer: `unknown` · Decision: `keep` · Confidence: `1.0`
- Reviewed: 20260505T115100Z
- Batch: `20260505T115100Z_866434f7`

