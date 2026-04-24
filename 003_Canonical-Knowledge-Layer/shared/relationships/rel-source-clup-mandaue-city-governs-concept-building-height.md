---
id: rel-source-clup-mandaue-city-governs-concept-building-height
title: source-clup-mandaue-city governs concept-building-height
page_type: relationship
relationship_type: governs
from_entity: source-clup-mandaue-city
to_entity: concept-building-height
trust_level: unverified
canonical_status: promoted
confidence_score: 0.95
promotion_batch_id: 20260424T190946Z_48d77dfe
promotion_audit_log_ref: 006_System-Manifests/runs/kg_pipeline_20260424T154833Z/promotion_audit.log
last_promoted_utc: 20260424T190946Z
evidence:
- source_id: source-clup-mandaue-city
  source_section_id: section-4
  evidence_snippet: Building Height Limit (BHL) - per the National Building Code, this is' the maximum height to be allowed for building/s structures... and shall be generally measured from the established grade line to the topmost portion of the proposed building structure . If applicable the BHL may be subject to cle
  review_decision: keep
  reviewer_model: llama3.1:8b
  reviewer_provider: ollama
  reviewer_confidence: 0.95
  reviewer_reason: 'pre_review_filter: structural_governs_pattern: source->concept, occ>=3, characteristic language'
  local_review_decision: keep
  local_reviewer_confidence: 0.95
  extracted_at_utc: 20260424T190946Z
  reviewed_at_utc: 20260424T190946Z
  raw_source_trust_level: unknown
  source_trust_normalized_from: unknown
---

# source-clup-mandaue-city governs concept-building-height

## Relationship Summary

Promoted relationship of type `governs` from `source-clup-mandaue-city` to `concept-building-height`.

## Evidence

### Evidence 1 - `source-clup-mandaue-city` §section-4

> Building Height Limit (BHL) - per the National Building Code, this is' the maximum height to be allowed for building/s structures... and shall be generally measured from the established grade line to the topmost portion of the proposed building structure . If applicable the BHL may be subject to cle

- Reviewer: `llama3.1:8b` · Decision: `keep` · Confidence: `0.95`
- Reviewed: 20260424T190946Z
- Batch: `20260424T190946Z_48d77dfe`

