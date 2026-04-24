---
id: rel-law-section-rule-viii-light-ventilation-governs-concept-yards
title: law-section-rule-viii-light-ventilation governs concept-yards
page_type: relationship
relationship_type: governs
from_entity: law-section-rule-viii-light-ventilation
to_entity: concept-yards
trust_level: primary
canonical_status: promoted
confidence_score: 0.95
promotion_batch_id: 20260423T220140Z_61f50125
promotion_audit_log_ref: 006_System-Manifests/runs/kg_pipeline_20260423T184105Z/promotion_audit.log
last_promoted_utc: 20260423T220140Z
evidence:
- source_id: law-section-rule-viii-light-ventilation
  source_section_id: section-802
  evidence_snippet: Courts, yards, and light wells shall be measured clear of all projections from the walls enclosing such wells or yards with the exception of roof leaders, wall copings, sills, or steel fire escapes not exceeding 1.20 meters in width.
  review_decision: keep
  reviewer_model: qwen2.5:3b
  reviewer_provider: ollama
  reviewer_confidence: 0.95
  reviewer_reason: 'pre_review_filter: structural_governs_pattern: source->concept, occ>=3, characteristic language'
  local_review_decision: keep
  local_reviewer_confidence: 0.95
  extracted_at_utc: 20260423T220140Z
  reviewed_at_utc: 20260423T220140Z
---

# law-section-rule-viii-light-ventilation governs concept-yards

## Relationship Summary

Promoted relationship of type `governs` from `law-section-rule-viii-light-ventilation` to `concept-yards`.

## Evidence

### Evidence 1 - `law-section-rule-viii-light-ventilation` §section-802

> Courts, yards, and light wells shall be measured clear of all projections from the walls enclosing such wells or yards with the exception of roof leaders, wall copings, sills, or steel fire escapes not exceeding 1.20 meters in width.

- Reviewer: `qwen2.5:3b` · Decision: `keep` · Confidence: `0.95`
- Reviewed: 20260423T220140Z
- Batch: `20260423T220140Z_61f50125`
