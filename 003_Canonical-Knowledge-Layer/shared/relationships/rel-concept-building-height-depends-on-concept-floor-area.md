---
id: rel-concept-building-height-depends-on-concept-floor-area
title: concept-building-height depends_on concept-floor-area
page_type: relationship
relationship_type: depends_on
from_entity: concept-building-height
to_entity: concept-floor-area
trust_level: unverified
canonical_status: promoted
confidence_score: 1.0
promotion_batch_id: 20260505T115100Z_866434f7
promotion_audit_log_ref: 006_System-Manifests\runs\kg_pipeline_20260505T095933Z\promotion_audit.log
last_promoted_utc: 20260505T115100Z
evidence:
- source_id: concept-building-height
  source_section_id: section-3
  evidence_snippet: '- – Euclidean Zoning—also called conventional zoning, it is characterized by the segregation of land uses into specified geographic zones with provisions on limitations of activities (such as use, building height, etc.) within each type of zone. Easy to administer but has been criticized as being ba'
  review_decision: keep
  reviewer_model: unknown
  reviewer_provider: ollama
  reviewer_confidence: 1.0
  reviewer_reason: skip_review pipeline path for source-hlurb-clup-guidebook-vol-1-11042015
  local_review_decision: keep
  local_reviewer_confidence: 1.0
  extracted_at_utc: 20260505T114946Z
  reviewed_at_utc: 20260505T114946Z
  raw_source_trust_level: null
  source_trust_normalized_from: null
- source_id: concept-building-height
  source_section_id: section-705
  evidence_snippet: 'j of Use/ Typeof "Note: Building Height limit (BHL) mtJitiplied by the Allowable Maxinun O<:cupan- Building/ Building Footprint (AMBF) expressed as a peroentage {%)of the TotiJ Lot cy Structure Area orTLA (with orwithout firewall). Figure subject to reduction lo cornpty with the floor area component'
  review_decision: keep
  reviewer_model: unknown
  reviewer_provider: ollama
  reviewer_confidence: 1.0
  reviewer_reason: skip_review pipeline path for law-national-building-code-of-the-philippines
  local_review_decision: keep
  local_reviewer_confidence: 1.0
  extracted_at_utc: 20260505T115100Z
  reviewed_at_utc: 20260505T115100Z
  raw_source_trust_level: null
  source_trust_normalized_from: null
---

# concept-building-height depends_on concept-floor-area

## Relationship Summary

Promoted relationship of type `depends_on` from `concept-building-height` to `concept-floor-area`.

## Evidence

### Evidence 1 - `concept-building-height` §section-3

> - – Euclidean Zoning—also called conventional zoning, it is characterized by the segregation of land uses into specified geographic zones with provisions on limitations of activities (such as use, building height, etc.) within each type of zone. Easy to administer but has been criticized as being ba

- Reviewer: `unknown` · Decision: `keep` · Confidence: `1.0`
- Reviewed: 20260505T114946Z
- Batch: `20260505T115100Z_866434f7`

### Evidence 2 - `concept-building-height` §section-705

> j of Use/ Typeof "Note: Building Height limit (BHL) mtJitiplied by the Allowable Maxinun O<:cupan- Building/ Building Footprint (AMBF) expressed as a peroentage {%)of the TotiJ Lot cy Structure Area orTLA (with orwithout firewall). Figure subject to reduction lo cornpty with the floor area component

- Reviewer: `unknown` · Decision: `keep` · Confidence: `1.0`
- Reviewed: 20260505T115100Z
- Batch: `20260505T115100Z_866434f7`

