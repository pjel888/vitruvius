---
id: rel-source-no-17-098b-governs-concept-comprehensive-land-use-plan
title: source-no-17-098b governs concept-comprehensive-land-use-plan
page_type: relationship
relationship_type: governs
from_entity: source-no-17-098b
to_entity: concept-comprehensive-land-use-plan
trust_level: unverified
canonical_status: promoted
confidence_score: 0.95
promotion_batch_id: 20260505T115102Z_b8230b42
promotion_audit_log_ref: 006_System-Manifests\runs\kg_pipeline_20260505T095933Z\promotion_audit.log
last_promoted_utc: 20260505T115102Z
evidence:
- source_id: source-no-17-098b
  source_section_id: section-54
  evidence_snippet: Cities, the formulation, adoption, or modification of said plan shall be in coordination with the approved Provincial Comprehensive Land Use Plan;
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
  source_section_id: section-14.1
  evidence_snippet: \ FLD-OZ regulations are applied in areas that have been determined in the CLUP as flood-prone area certified by the City Planning and Development
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

# source-no-17-098b governs concept-comprehensive-land-use-plan

## Relationship Summary

Promoted relationship of type `governs` from `source-no-17-098b` to `concept-comprehensive-land-use-plan`.

## Evidence

### Evidence 1 - `source-no-17-098b` §section-54

> Cities, the formulation, adoption, or modification of said plan shall be in coordination with the approved Provincial Comprehensive Land Use Plan;

- Reviewer: `llama3.1:8b` · Decision: `keep` · Confidence: `0.95`
- Reviewed: 20260424T183830Z
- Batch: `20260505T115102Z_b8230b42`

### Evidence 2 - `source-no-17-098b` §section-14.1

> \ FLD-OZ regulations are applied in areas that have been determined in the CLUP as flood-prone area certified by the City Planning and Development

- Reviewer: `unknown` · Decision: `keep` · Confidence: `1.0`
- Reviewed: 20260505T115102Z
- Batch: `20260505T115102Z_b8230b42`

