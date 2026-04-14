---
id: rel-concept-floor-area-depends-on-concept-yards
title: concept-floor-area depends_on concept-yards
page_type: relationship
relationship_type: depends_on
from_entity: concept-floor-area
to_entity: concept-yards
trust_level: unverified
canonical_status: promoted
confidence_score: 0.9
promotion_batch_id: 20260414T234203Z_2b941c4d
promotion_audit_log_ref: 006_System-Manifests/runs/latest_promotion_audit.log
last_promoted_utc: 20260414T234203Z
evidence:
- source_id: concept-floor-area
  source_section_id: section-irr-general
  evidence_snippet: '###### SECTION 706. Allowable Floor Area Increases  The floor areas hereinabove provided may be increased in certain specific instances and under appropriate conditions, based on the existence of public space, streets or yards extending along and adjoining two or more sides of the building or structure subject to the approval of the Building Official.'
  review_decision: keep
  reviewer_model: gemma4:31b
  reviewer_confidence: 0.9
  reviewer_reason: The examples explicitly link 'floor areas' (concept-floor-area) to the existence of 'yards' (concept-yards) as a condition for increasing floor area.
  extracted_at_utc: 20260414T234203Z
  reviewed_at_utc: 20260414T234203Z
---

# concept-floor-area depends_on concept-yards

## Relationship Summary

Promoted relationship of type `depends_on` from `concept-floor-area` to `concept-yards`.

## Evidence

### Evidence 1 - `concept-floor-area` §section-irr-general

> ###### SECTION 706. Allowable Floor Area Increases  The floor areas hereinabove provided may be increased in certain specific instances and under appropriate conditions, based on the existence of public space, streets or yards extending along and adjoining two or more sides of the building or structure subject to the approval of the Building Official.

- Reviewer: `gemma4:31b` · Decision: `keep` · Confidence: `0.9`
- Reviewed: 20260414T234203Z
- Batch: `20260414T234203Z_2b941c4d`

