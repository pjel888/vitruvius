---
id: rel-source-hlurb-clup-vol-3-b6b5f2-governs-concept-floor-area
title: source-hlurb-clup-vol-3-b6b5f2 governs concept-floor-area
page_type: relationship
relationship_type: governs
from_entity: source-hlurb-clup-vol-3-b6b5f2
to_entity: concept-floor-area
trust_level: unverified
canonical_status: promoted
confidence_score: 0.95
promotion_batch_id: 20260424T111855Z_1811a3fb
promotion_audit_log_ref: 006_System-Manifests/runs/kg_pipeline_20260424T110840Z/promotion_audit.log
last_promoted_utc: 20260424T111855Z
evidence:
- source_id: source-hlurb-clup-vol-3-b6b5f2
  source_section_id: section-12.2.1
  evidence_snippet: t Such home industry shall not occupy more than thirty percent of the floor area of the dwelling unit. t There shall be no change or alteration in the outside appearance of the dwelling unit and shall not be a hazard or nuisance; and
  review_decision: keep
  reviewer_model: llama3.1:8b
  reviewer_provider: ollama
  reviewer_confidence: 0.95
  reviewer_reason: 'pre_review_filter: structural_governs_pattern: source->concept, occ>=3, characteristic language'
  local_review_decision: keep
  local_reviewer_confidence: 0.95
  extracted_at_utc: 20260424T111855Z
  reviewed_at_utc: 20260424T111855Z
---

# source-hlurb-clup-vol-3-b6b5f2 governs concept-floor-area

## Relationship Summary

Promoted relationship of type `governs` from `source-hlurb-clup-vol-3-b6b5f2` to `concept-floor-area`.

## Evidence

### Evidence 1 - `source-hlurb-clup-vol-3-b6b5f2` §section-12.2.1

> t Such home industry shall not occupy more than thirty percent of the floor area of the dwelling unit. t There shall be no change or alteration in the outside appearance of the dwelling unit and shall not be a hazard or nuisance; and

- Reviewer: `llama3.1:8b` · Decision: `keep` · Confidence: `0.95`
- Reviewed: 20260424T111855Z
- Batch: `20260424T111855Z_1811a3fb`

