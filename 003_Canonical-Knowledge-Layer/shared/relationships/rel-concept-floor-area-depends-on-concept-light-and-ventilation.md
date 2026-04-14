---
id: rel-concept-floor-area-depends-on-concept-light-and-ventilation
title: concept-floor-area depends_on concept-light-and-ventilation
page_type: relationship
relationship_type: depends_on
from_entity: concept-floor-area
to_entity: concept-light-and-ventilation
trust_level: unverified
canonical_status: promoted
confidence_score: 0.9
promotion_batch_id: 20260414T234203Z_2b941c4d
promotion_audit_log_ref: 006_System-Manifests/runs/latest_promotion_audit.log
last_promoted_utc: 20260414T234203Z
evidence:
- source_id: concept-floor-area
  source_section_id: section-irr-general
  evidence_snippet: '- 2. In case of proposed additional construction on a lot on which another building/structure already stands, the Percentage of Site Occupancy (PSO) arising out of such existing buildings/structures must be included in the computation of the PSO for the Total Lot Area (TLA). In case of discrepancy between the specified Maximum Allowable PSO and the other light and ventilation provisions under this Rule, the resulting lesser building/structure footprint or gross floor area at the ground floor (or at grade level) must prevail. - 3. Maximum site occupancy shall be governed by use, type of construction, and height of the building and the use, area, nature and location of the site; and subject to the provisions of the local zoning requirements and in accordance with the following types of open spaces:'
  review_decision: keep
  reviewer_model: gemma4:31b
  reviewer_confidence: 0.9
  reviewer_reason: The examples show that the calculation of Site Occupancy (PSO) and the resulting building footprint/gross floor area must consider multiple provisions, including 'light and ventilation provisions' and 'local zoning requirements,' indicating a dependency relationship.
  extracted_at_utc: 20260414T234203Z
  reviewed_at_utc: 20260414T234203Z
---

# concept-floor-area depends_on concept-light-and-ventilation

## Relationship Summary

Promoted relationship of type `depends_on` from `concept-floor-area` to `concept-light-and-ventilation`.

## Evidence

### Evidence 1 - `concept-floor-area` §section-irr-general

> - 2. In case of proposed additional construction on a lot on which another building/structure already stands, the Percentage of Site Occupancy (PSO) arising out of such existing buildings/structures must be included in the computation of the PSO for the Total Lot Area (TLA). In case of discrepancy between the specified Maximum Allowable PSO and the other light and ventilation provisions under this Rule, the resulting lesser building/structure footprint or gross floor area at the ground floor (or at grade level) must prevail. - 3. Maximum site occupancy shall be governed by use, type of construction, and height of the building and the use, area, nature and location of the site; and subject to the provisions of the local zoning requirements and in accordance with the following types of open spaces:

- Reviewer: `gemma4:31b` · Decision: `keep` · Confidence: `0.9`
- Reviewed: 20260414T234203Z
- Batch: `20260414T234203Z_2b941c4d`

