---
id: rel-concept-floor-area-affects-concept-building-height
title: concept-floor-area affects concept-building-height
page_type: relationship
relationship_type: affects
from_entity: concept-floor-area
to_entity: concept-building-height
trust_level: unverified
canonical_status: promoted
confidence_score: 0.9
promotion_batch_id: 20260414T234203Z_2b941c4d
promotion_audit_log_ref: 006_System-Manifests/runs/latest_promotion_audit.log
last_promoted_utc: 20260414T234203Z
evidence:
- source_id: concept-floor-area
  source_section_id: section-irr-general
  evidence_snippet: BUILDING BULK - The overall size of a proposed building/structure as initially characterized by the expanse of its gross floor area (GFA) or total gross floor area (TGFA), by the overall dimensions of its allowable maximum building footprint (AMBF), by its height as dictated by the building height limit (BHL) and also by the extent of allowable building projections (if these are large enough to host certain types of activities). The building bulk, expressed in cubic meters, must not exceed the established AMVB above grade. All measurements pertaining to building bulk shall be made from the outermost faces of the exterior walls and roof or from the most bottom surface of the lowermost floor of the building/structure (including those below grade).  BUILDING HEIGHT LIMIT (BHL) - The maximum height to be allowed for buildings/ structures based on their proposed use or occupancy; the BHL is generally determined after the application of other development control (DC) and certain other parameters, i.e., considerations of site conditions, view, etc.. The BHL shall be generally measured from the established grade line to the topmost portion of the proposed building/structure.
  review_decision: keep
  reviewer_model: gemma4:31b
  reviewer_confidence: 0.9
  reviewer_reason: The provided example explicitly discusses 'BUILDING BULK' which is characterized by the overall size, including dimensions related to 'gross floor area' (GFA) and 'height' (BHL). The relationship 'concept-floor-area' affects 'concept-building-height' is supported by the text linking GFA/floor area to the overall size calculation which includes height.
  extracted_at_utc: 20260414T234203Z
  reviewed_at_utc: 20260414T234203Z
---

# concept-floor-area affects concept-building-height

## Relationship Summary

Promoted relationship of type `affects` from `concept-floor-area` to `concept-building-height`.

## Evidence

### Evidence 1 - `concept-floor-area` §section-irr-general

> BUILDING BULK - The overall size of a proposed building/structure as initially characterized by the expanse of its gross floor area (GFA) or total gross floor area (TGFA), by the overall dimensions of its allowable maximum building footprint (AMBF), by its height as dictated by the building height limit (BHL) and also by the extent of allowable building projections (if these are large enough to host certain types of activities). The building bulk, expressed in cubic meters, must not exceed the established AMVB above grade. All measurements pertaining to building bulk shall be made from the outermost faces of the exterior walls and roof or from the most bottom surface of the lowermost floor of the building/structure (including those below grade).  BUILDING HEIGHT LIMIT (BHL) - The maximum height to be allowed for buildings/ structures based on their proposed use or occupancy; the BHL is generally determined after the application of other development control (DC) and certain other parameters, i.e., considerations of site conditions, view, etc.. The BHL shall be generally measured from the established grade line to the topmost portion of the proposed building/structure.

- Reviewer: `gemma4:31b` · Decision: `keep` · Confidence: `0.9`
- Reviewed: 20260414T234203Z
- Batch: `20260414T234203Z_2b941c4d`

