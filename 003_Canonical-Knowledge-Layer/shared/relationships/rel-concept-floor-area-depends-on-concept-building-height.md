---
id: rel-concept-floor-area-depends-on-concept-building-height
title: concept-floor-area depends_on concept-building-height
page_type: relationship
relationship_type: depends_on
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
  evidence_snippet: '###### Table VII.1. Allowable Maximum Total Gross Floor Area (TGFA)Based on the Allowed Percentage of Site Occupancy (PSO)of the Total Lot Area (TLA)  |Character of Use/ Occupancy|Type of Building/ Structure|Allowable Maximum Total Gross Floor Area (TGFA)* by Type/ Location of Lot<br><br>*Note: Building Height Limit (BHL) multiplied by the Allowable Maximum Building Footprint (AMBF) expressed as a percentage (%) of the Total Lot Area or TLA (with or without firewall). Figure subject to reduction to comply with the floor area component of the Allowable Maximum Volume of Building (AMVB). Refer to Table VII.1. to arrive at the percentage (%) of TLA.| | | | | |'
  review_decision: keep
  reviewer_model: gemma4:31b
  reviewer_confidence: 0.9
  reviewer_reason: The examples show a calculation for 'Allowable Maximum Total Gross Floor Area (TGFA)' which explicitly uses 'Building Height Limit (BHL)' multiplied by 'Allowable Maximum Building Footprint (AMBF)'. Since 'concept-floor-area' relates to floor area and 'concept-building-height' relates to height, this calculation demonstrates a direct dependency relationship.
  extracted_at_utc: 20260414T234203Z
  reviewed_at_utc: 20260414T234203Z
---

# concept-floor-area depends_on concept-building-height

## Relationship Summary

Promoted relationship of type `depends_on` from `concept-floor-area` to `concept-building-height`.

## Evidence

### Evidence 1 - `concept-floor-area` §section-irr-general

> ###### Table VII.1. Allowable Maximum Total Gross Floor Area (TGFA)Based on the Allowed Percentage of Site Occupancy (PSO)of the Total Lot Area (TLA)  |Character of Use/ Occupancy|Type of Building/ Structure|Allowable Maximum Total Gross Floor Area (TGFA)* by Type/ Location of Lot<br><br>*Note: Building Height Limit (BHL) multiplied by the Allowable Maximum Building Footprint (AMBF) expressed as a percentage (%) of the Total Lot Area or TLA (with or without firewall). Figure subject to reduction to comply with the floor area component of the Allowable Maximum Volume of Building (AMVB). Refer to Table VII.1. to arrive at the percentage (%) of TLA.| | | | | |

- Reviewer: `gemma4:31b` · Decision: `keep` · Confidence: `0.9`
- Reviewed: 20260414T234203Z
- Batch: `20260414T234203Z_2b941c4d`

