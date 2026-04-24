---
id: rel-irr-implementing-rules-and-regulations-of-the-national-building-code-8304a2-governs-concept-floor-area
title: irr-implementing-rules-and-regulations-of-the-national-building-code-8304a2 governs concept-floor-area
page_type: relationship
relationship_type: governs
from_entity: irr-implementing-rules-and-regulations-of-the-national-building-code-8304a2
to_entity: concept-floor-area
trust_level: primary
canonical_status: promoted
confidence_score: 0.95
promotion_batch_id: 20260423T204318Z_ace8a49a
promotion_audit_log_ref: 006_System-Manifests/runs/kg_pipeline_20260423T203224Z/promotion_audit.log
last_promoted_utc: 20260423T204318Z
evidence:
- source_id: irr-implementing-rules-and-regulations-of-the-national-building-code-8304a2
  source_section_id: section-502
  evidence_snippet: A building/structure which is located partly in one (1) fire zone and partly in another shall be considered to be in the more highly restrictive fire zone, when more than one third (1/3) of its total floor area is located in such zone.
  review_decision: keep
  reviewer_model: qwen2.5:3b
  reviewer_provider: ollama
  reviewer_confidence: 0.95
  reviewer_reason: 'pre_review_filter: structural_governs_pattern: source->concept, occ>=3, characteristic language'
  local_review_decision: keep
  local_reviewer_confidence: 0.95
  extracted_at_utc: 20260423T204318Z
  reviewed_at_utc: 20260423T204318Z
---

# irr-implementing-rules-and-regulations-of-the-national-building-code-8304a2 governs concept-floor-area

## Relationship Summary

Promoted relationship of type `governs` from `irr-implementing-rules-and-regulations-of-the-national-building-code-8304a2` to `concept-floor-area`.

## Evidence

### Evidence 1 - `irr-implementing-rules-and-regulations-of-the-national-building-code-8304a2` §section-502

> A building/structure which is located partly in one (1) fire zone and partly in another shall be considered to be in the more highly restrictive fire zone, when more than one third (1/3) of its total floor area is located in such zone.

- Reviewer: `qwen2.5:3b` · Decision: `keep` · Confidence: `0.95`
- Reviewed: 20260423T204318Z
- Batch: `20260423T204318Z_ace8a49a`
