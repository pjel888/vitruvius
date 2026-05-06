---
id: rel-law-pasay-city-zoning-ordinance-of-2003-governs-concept-floor-area
title: law-pasay-city-zoning-ordinance-of-2003 governs concept-floor-area
page_type: relationship
relationship_type: governs
from_entity: law-pasay-city-zoning-ordinance-of-2003
to_entity: concept-floor-area
trust_level: primary
canonical_status: promoted
confidence_score: 0.95
promotion_batch_id: 20260505T115108Z_848576c1
promotion_audit_log_ref: 006_System-Manifests\runs\kg_pipeline_20260505T095933Z\promotion_audit.log
last_promoted_utc: 20260505T115108Z
evidence:
- source_id: law-pasay-city-zoning-ordinance-of-2003
  source_section_id: section-42
  evidence_snippet: '- 1) Such home industry shall not occupy more than sixty percent (60.0%) of the total enclosed gross floor area of the dwelling unit There shall be limited change or alternation in the outside appearance of the dwelling unit and the changes must not constitutea hazard ornuisance;'
  review_decision: keep
  reviewer_model: llama3.1:8b
  reviewer_provider: ollama
  reviewer_confidence: 0.95
  reviewer_reason: 'pre_review_filter: structural_governs_pattern: source->concept, occ>=3, characteristic language'
  local_review_decision: keep
  local_reviewer_confidence: 0.95
  extracted_at_utc: 20260424T184741Z
  reviewed_at_utc: 20260424T184741Z
- source_id: law-pasay-city-zoning-ordinance-of-2003
  source_section_id: section-43
  evidence_snippet: '- 1) Such home industry shall not occupy more than thirty percent (30.0%) of the total enclosed gross floor area of the dwelling unit. There shall be no change or alternation in the outside appearance of the dwelling unit and the structure must not constitute a'
  review_decision: keep
  reviewer_model: unknown
  reviewer_provider: ollama
  reviewer_confidence: 1.0
  reviewer_reason: skip_review pipeline path for law-pasay-city-zoning-ordinance-of-2003
  local_review_decision: keep
  local_reviewer_confidence: 1.0
  extracted_at_utc: 20260505T115108Z
  reviewed_at_utc: 20260505T115108Z
---

# law-pasay-city-zoning-ordinance-of-2003 governs concept-floor-area

## Relationship Summary

Promoted relationship of type `governs` from `law-pasay-city-zoning-ordinance-of-2003` to `concept-floor-area`.

## Evidence

### Evidence 1 - `law-pasay-city-zoning-ordinance-of-2003` §section-42

> - 1) Such home industry shall not occupy more than sixty percent (60.0%) of the total enclosed gross floor area of the dwelling unit There shall be limited change or alternation in the outside appearance of the dwelling unit and the changes must not constitutea hazard ornuisance;

- Reviewer: `llama3.1:8b` · Decision: `keep` · Confidence: `0.95`
- Reviewed: 20260424T184741Z
- Batch: `20260505T115108Z_848576c1`

### Evidence 2 - `law-pasay-city-zoning-ordinance-of-2003` §section-43

> - 1) Such home industry shall not occupy more than thirty percent (30.0%) of the total enclosed gross floor area of the dwelling unit. There shall be no change or alternation in the outside appearance of the dwelling unit and the structure must not constitute a

- Reviewer: `unknown` · Decision: `keep` · Confidence: `1.0`
- Reviewed: 20260505T115108Z
- Batch: `20260505T115108Z_848576c1`

