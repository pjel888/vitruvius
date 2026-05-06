---
id: rel-concept-stairs-requires-concept-fire-resistive-construction
title: concept-stairs requires concept-fire-resistive-construction
page_type: relationship
relationship_type: requires
from_entity: concept-stairs
to_entity: concept-fire-resistive-construction
trust_level: unverified
canonical_status: promoted
confidence_score: 0.9
promotion_batch_id: 20260505T115116Z_10f901e8
promotion_audit_log_ref: 006_System-Manifests\runs\kg_pipeline_20260505T095933Z\promotion_audit.log
last_promoted_utc: 20260505T115116Z
evidence:
- source_id: concept-stairs
  source_section_id: section-1207
  evidence_snippet: '- i. Stairway Construction - Interior. Interior stairways shall be constructed as specified in this Code. Where there is enclosed usable space under the stairs the walls and soffits of the enclosed space shall be protected on the enclosed side as required for one-hour fire resistive construction. - '
  review_decision: keep
  reviewer_model: llama3.1:8b
  reviewer_provider: ollama
  reviewer_confidence: 0.9
  reviewer_reason: Stairway construction requires fire resistive construction as specified in section-1207.
  local_review_decision: keep
  local_reviewer_confidence: 0.9
  extracted_at_utc: 20260424T174922Z
  reviewed_at_utc: 20260424T174922Z
  raw_source_trust_level: null
  source_trust_normalized_from: null
- source_id: concept-stairs
  source_section_id: section-1207
  evidence_snippet: '- (10b) Stairway Construction-Exterior. Exterior stairways shall be of incombustible material: Except, that on Type Ill buildings which do not exceed tw''o storeys in height, which are located in less fire-restrictive Fire Zones, as well as on Type I buildings which may be of wood not less than 50 mi'
  review_decision: keep
  reviewer_model: llama3.1:8b
  reviewer_provider: ollama
  reviewer_confidence: 0.9
  reviewer_reason: Examples explicitly state that stairway construction requires fire resistive construction.
  local_review_decision: keep
  local_reviewer_confidence: 0.9
  extracted_at_utc: 20260424T183501Z
  reviewed_at_utc: 20260424T183501Z
  raw_source_trust_level: null
  source_trust_normalized_from: null
- source_id: concept-stairs
  source_section_id: section-1207
  evidence_snippet: 'material: Except, that on Type III buildings which do not exceed two storeys in height, which are located in less fire-restrictive Fire Zones, as well as on Type I buildings which may be of wood not less than 50 millimeters in nominal thickness. Exterior stairs shall be protected as required for ext'
  review_decision: keep
  reviewer_model: unknown
  reviewer_provider: ollama
  reviewer_confidence: 1.0
  reviewer_reason: skip_review pipeline path for law-national-building-code-of-the-philippines-2e00e2
  local_review_decision: keep
  local_reviewer_confidence: 1.0
  extracted_at_utc: 20260505T115047Z
  reviewed_at_utc: 20260505T115047Z
  raw_source_trust_level: null
  source_trust_normalized_from: null
- source_id: concept-stairs
  source_section_id: section-1207
  evidence_snippet: '- millimeters in nominal thickness. Exterior stairs shall be protected as required for exterior walls due to location on property as specified in this Code. Exterior stairways shall not project into an area where openings are required to be protected. Where there is enclosed usable space under stair'
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

# concept-stairs requires concept-fire-resistive-construction

## Relationship Summary

Promoted relationship of type `requires` from `concept-stairs` to `concept-fire-resistive-construction`.

## Evidence

### Evidence 1 - `concept-stairs` §section-1207

> - i. Stairway Construction - Interior. Interior stairways shall be constructed as specified in this Code. Where there is enclosed usable space under the stairs the walls and soffits of the enclosed space shall be protected on the enclosed side as required for one-hour fire resistive construction. - 

- Reviewer: `llama3.1:8b` · Decision: `keep` · Confidence: `0.9`
- Reviewed: 20260424T174922Z
- Batch: `20260505T115116Z_10f901e8`

### Evidence 2 - `concept-stairs` §section-1207

> - (10b) Stairway Construction-Exterior. Exterior stairways shall be of incombustible material: Except, that on Type Ill buildings which do not exceed tw'o storeys in height, which are located in less fire-restrictive Fire Zones, as well as on Type I buildings which may be of wood not less than 50 mi

- Reviewer: `llama3.1:8b` · Decision: `keep` · Confidence: `0.9`
- Reviewed: 20260424T183501Z
- Batch: `20260505T115116Z_10f901e8`

### Evidence 3 - `concept-stairs` §section-1207

> material: Except, that on Type III buildings which do not exceed two storeys in height, which are located in less fire-restrictive Fire Zones, as well as on Type I buildings which may be of wood not less than 50 millimeters in nominal thickness. Exterior stairs shall be protected as required for ext

- Reviewer: `unknown` · Decision: `keep` · Confidence: `1.0`
- Reviewed: 20260505T115047Z
- Batch: `20260505T115116Z_10f901e8`

### Evidence 4 - `concept-stairs` §section-1207

> - millimeters in nominal thickness. Exterior stairs shall be protected as required for exterior walls due to location on property as specified in this Code. Exterior stairways shall not project into an area where openings are required to be protected. Where there is enclosed usable space under stair

- Reviewer: `unknown` · Decision: `keep` · Confidence: `1.0`
- Reviewed: 20260505T115116Z
- Batch: `20260505T115116Z_10f901e8`

