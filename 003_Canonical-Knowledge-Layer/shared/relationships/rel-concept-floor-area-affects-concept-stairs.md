---
id: rel-concept-floor-area-affects-concept-stairs
title: concept-floor-area affects concept-stairs
page_type: relationship
relationship_type: affects
from_entity: concept-floor-area
to_entity: concept-stairs
trust_level: unverified
canonical_status: promoted
confidence_score: 0.9
promotion_batch_id: 20260414T234203Z_2b941c4d
promotion_audit_log_ref: 006_System-Manifests/runs/latest_promotion_audit.log
last_promoted_utc: 20260414T234203Z
evidence:
- source_id: concept-floor-area
  source_section_id: section-irr-general
  evidence_snippet: '- 1. General. The construction of stairs and exits shall conform to the occupant load requirements of buildings, reviewing stands, bleachers, and grandstands.  - a. Determination of Occupant Loads. The occupant load permitted in any building or portion thereof shall be determined by dividing the floor area assigned to that use by the unit area allowed per occupant as shown on Table XII.1. and as determined by the Secretary.'
  review_decision: keep
  reviewer_model: gemma4:31b
  reviewer_confidence: 0.9
  reviewer_reason: The examples show that the floor area (determined by dividing the floor area assigned to that use by the unit area allowed per occupant) is directly used to determine the occupant load, which in turn governs the requirements for stairs and exits.
  extracted_at_utc: 20260414T234203Z
  reviewed_at_utc: 20260414T234203Z
---

# concept-floor-area affects concept-stairs

## Relationship Summary

Promoted relationship of type `affects` from `concept-floor-area` to `concept-stairs`.

## Evidence

### Evidence 1 - `concept-floor-area` §section-irr-general

> - 1. General. The construction of stairs and exits shall conform to the occupant load requirements of buildings, reviewing stands, bleachers, and grandstands.  - a. Determination of Occupant Loads. The occupant load permitted in any building or portion thereof shall be determined by dividing the floor area assigned to that use by the unit area allowed per occupant as shown on Table XII.1. and as determined by the Secretary.

- Reviewer: `gemma4:31b` · Decision: `keep` · Confidence: `0.9`
- Reviewed: 20260414T234203Z
- Batch: `20260414T234203Z_2b941c4d`

