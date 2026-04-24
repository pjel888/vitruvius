---
id: rel-concept-floor-area-affects-concept-floor-area-ratio
title: concept-floor-area affects concept-floor-area-ratio
page_type: relationship
relationship_type: affects
from_entity: concept-floor-area
to_entity: concept-floor-area-ratio
trust_level: unverified
canonical_status: promoted
confidence_score: 0.9
promotion_batch_id: 20260424T111317Z_c04bfe12
promotion_audit_log_ref: 006_System-Manifests/runs/kg_pipeline_20260424T110840Z/promotion_audit.log
last_promoted_utc: 20260424T111317Z
evidence:
- source_id: concept-floor-area
  source_section_id: section-4
  evidence_snippet: Determined by dividing the Gross Floor Area of the building and the area of the lob .The Gross Floor Area of any building should not exceed the prescribed floor area ratio (FAR) multiplied by the lot area.
  review_decision: keep
  reviewer_model: llama3.1:8b
  reviewer_provider: ollama
  reviewer_confidence: 0.9
  reviewer_reason: Explicit causal relationship between floor area and floor area ratio.
  local_review_decision: keep
  local_reviewer_confidence: 0.9
  extracted_at_utc: 20260424T111317Z
  reviewed_at_utc: 20260424T111317Z
---

# concept-floor-area affects concept-floor-area-ratio

## Relationship Summary

Promoted relationship of type `affects` from `concept-floor-area` to `concept-floor-area-ratio`.

## Evidence

### Evidence 1 - `concept-floor-area` §section-4

> Determined by dividing the Gross Floor Area of the building and the area of the lob .The Gross Floor Area of any building should not exceed the prescribed floor area ratio (FAR) multiplied by the lot area.

- Reviewer: `llama3.1:8b` · Decision: `keep` · Confidence: `0.9`
- Reviewed: 20260424T111317Z
- Batch: `20260424T111317Z_c04bfe12`

