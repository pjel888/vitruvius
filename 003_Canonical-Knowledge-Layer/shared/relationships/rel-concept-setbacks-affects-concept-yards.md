---
id: rel-concept-setbacks-affects-concept-yards
title: concept-setbacks affects concept-yards
page_type: relationship
relationship_type: affects
from_entity: concept-setbacks
to_entity: concept-yards
trust_level: unverified
canonical_status: promoted
confidence_score: 0.9
promotion_batch_id: 20260414T234203Z_2b941c4d
promotion_audit_log_ref: 006_System-Manifests/runs/latest_promotion_audit.log
last_promoted_utc: 20260414T234203Z
evidence:
- source_id: concept-setbacks
  source_section_id: section-irr-general
  evidence_snippet: '- A. DETERMINING BUILDING BULK  - 1. General. Building bulk (a volume quantity) shall be generally determined by the application of the Floor-Lot Area Ratio (FLAR), vertically projecting the Allowable Maximum Building Footprint (AMBF), establishing the Outermost Faces of Building (OFB) and quantifying the Allowable Maximum Volume of Building (AMVB). The building bulk may be ultimately governed by the width of the RROW and other applicable provisions for light and ventilation (including incremental setbacks as a result of satisfying natural light and ventilation requirements for RROW and front yards as partly shown in Table VII.G.1. hereafter).'
  review_decision: keep
  reviewer_model: gemma4:31b
  reviewer_confidence: 0.9
  reviewer_reason: The examples explicitly mention that building bulk may be governed by 'other applicable provisions for light and ventilation (including incremental setbacks as a result of satisfying natural light and ventilation requirements for RROW and front yards...)' which directly supports the relationship 'concept-setbacks' affects 'concept-yards'.
  extracted_at_utc: 20260414T234203Z
  reviewed_at_utc: 20260414T234203Z
---

# concept-setbacks affects concept-yards

## Relationship Summary

Promoted relationship of type `affects` from `concept-setbacks` to `concept-yards`.

## Evidence

### Evidence 1 - `concept-setbacks` §section-irr-general

> - A. DETERMINING BUILDING BULK  - 1. General. Building bulk (a volume quantity) shall be generally determined by the application of the Floor-Lot Area Ratio (FLAR), vertically projecting the Allowable Maximum Building Footprint (AMBF), establishing the Outermost Faces of Building (OFB) and quantifying the Allowable Maximum Volume of Building (AMVB). The building bulk may be ultimately governed by the width of the RROW and other applicable provisions for light and ventilation (including incremental setbacks as a result of satisfying natural light and ventilation requirements for RROW and front yards as partly shown in Table VII.G.1. hereafter).

- Reviewer: `gemma4:31b` · Decision: `keep` · Confidence: `0.9`
- Reviewed: 20260414T234203Z
- Batch: `20260414T234203Z_2b941c4d`

