---
id: rel-source-no-17-098b-governs-concept-floor-area
title: source-no-17-098b governs concept-floor-area
page_type: relationship
relationship_type: governs
from_entity: source-no-17-098b
to_entity: concept-floor-area
trust_level: unverified
canonical_status: promoted
confidence_score: 0.95
promotion_batch_id: 20260505T115102Z_b8230b42
promotion_audit_log_ref: 006_System-Manifests\runs\kg_pipeline_20260505T095933Z\promotion_audit.log
last_promoted_utc: 20260505T115102Z
evidence:
- source_id: source-no-17-098b
  source_section_id: section-2
  evidence_snippet: between the gross floor area of a building and the area of the iot on which it stands, determined by dividing the gross floor area of the building and the
  review_decision: keep
  reviewer_model: llama3.1:8b
  reviewer_provider: ollama
  reviewer_confidence: 0.95
  reviewer_reason: 'pre_review_filter: structural_governs_pattern: source->concept, occ>=3, characteristic language'
  local_review_decision: keep
  local_reviewer_confidence: 0.95
  extracted_at_utc: 20260424T183830Z
  reviewed_at_utc: 20260424T183830Z
  raw_source_trust_level: unknown
  source_trust_normalized_from: unknown
- source_id: source-no-17-098b
  source_section_id: section-3
  evidence_snippet: between the gross floor area of a building and the area of the iot on which it Stands, determined by dividing the gross floor area of the building and the area of the lot.
  review_decision: keep
  reviewer_model: unknown
  reviewer_provider: ollama
  reviewer_confidence: 1.0
  reviewer_reason: skip_review pipeline path for source-no-17-098b
  local_review_decision: keep
  local_reviewer_confidence: 1.0
  extracted_at_utc: 20260505T115102Z
  reviewed_at_utc: 20260505T115102Z
  raw_source_trust_level: unknown
  source_trust_normalized_from: unknown
---

# source-no-17-098b governs concept-floor-area

## Relationship Summary

Promoted relationship of type `governs` from `source-no-17-098b` to `concept-floor-area`.

## Evidence

### Evidence 1 - `source-no-17-098b` §section-2

> between the gross floor area of a building and the area of the iot on which it stands, determined by dividing the gross floor area of the building and the

- Reviewer: `llama3.1:8b` · Decision: `keep` · Confidence: `0.95`
- Reviewed: 20260424T183830Z
- Batch: `20260505T115102Z_b8230b42`

### Evidence 2 - `source-no-17-098b` §section-3

> between the gross floor area of a building and the area of the iot on which it Stands, determined by dividing the gross floor area of the building and the area of the lot.

- Reviewer: `unknown` · Decision: `keep` · Confidence: `1.0`
- Reviewed: 20260505T115102Z
- Batch: `20260505T115102Z_b8230b42`

