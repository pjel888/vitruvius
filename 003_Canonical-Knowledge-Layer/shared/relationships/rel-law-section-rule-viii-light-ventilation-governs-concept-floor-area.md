---
id: rel-law-section-rule-viii-light-ventilation-governs-concept-floor-area
title: law-section-rule-viii-light-ventilation governs concept-floor-area
page_type: relationship
relationship_type: governs
from_entity: law-section-rule-viii-light-ventilation
to_entity: concept-floor-area
trust_level: primary
canonical_status: promoted
confidence_score: 0.95
promotion_batch_id: 20260423T220140Z_61f50125
promotion_audit_log_ref: 006_System-Manifests/runs/kg_pipeline_20260423T184105Z/promotion_audit.log
last_promoted_utc: 20260423T220140Z
evidence:
- source_id: law-section-rule-viii-light-ventilation
  source_section_id: section-804
  evidence_snippet: '- e) **** Mixed-Use Buildings/Structures in R-5 lots shall be considered a commercial use or occupancy if a substantial percentage, i.e., 55% of the Gross Floor Area (GFA) is commercial.'
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

# law-section-rule-viii-light-ventilation governs concept-floor-area

## Relationship Summary

Promoted relationship of type `governs` from `law-section-rule-viii-light-ventilation` to `concept-floor-area`.

## Evidence

### Evidence 1 - `law-section-rule-viii-light-ventilation` §section-804

> - e) **** Mixed-Use Buildings/Structures in R-5 lots shall be considered a commercial use or occupancy if a substantial percentage, i.e., 55% of the Gross Floor Area (GFA) is commercial.

- Reviewer: `qwen2.5:3b` · Decision: `keep` · Confidence: `0.95`
- Reviewed: 20260423T220140Z
- Batch: `20260423T220140Z_61f50125`
