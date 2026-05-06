---
id: rel-concept-stairs-requires-concept-means-of-egress
title: concept-stairs requires concept-means-of-egress
page_type: relationship
relationship_type: requires
from_entity: concept-stairs
to_entity: concept-means-of-egress
trust_level: unverified
canonical_status: promoted
confidence_score: 0.9
promotion_batch_id: 20260505T115023Z_15687c61
promotion_audit_log_ref: 006_System-Manifests\runs\kg_pipeline_20260505T095933Z\promotion_audit.log
last_promoted_utc: 20260505T115023Z
evidence:
- source_id: concept-stairs
  source_section_id: section-10.2.5.2
  evidence_snippet: '- 4. Stairs, ramps, bridges, balconies, escalators, moving walks and other components of an exit discharge shall comply with the detailed requirements of this Division for such components. - 5. Subject to the approval of the C/MFM having jurisdiction, exits may be accepted to discharge to roofs or o'
  review_decision: keep
  reviewer_model: llama3.1:8b
  reviewer_provider: ollama
  reviewer_confidence: 0.9
  reviewer_reason: 'pre_review_filter: concept_requires_pattern: concept->concept, occ>=2, ''shall comply'' language'
  local_review_decision: keep
  local_reviewer_confidence: 0.9
  extracted_at_utc: 20260424T174130Z
  reviewed_at_utc: 20260424T174130Z
  raw_source_trust_level: null
  source_trust_normalized_from: null
- source_id: concept-stairs
  source_section_id: section-10.2.5.4
  evidence_snippet: 'Where specifically permitted for individual occupancies by Divisions 8 to 17 of this Chapter, spiral stairs as a component of means of egress shall comply with the following:'
  review_decision: keep
  reviewer_model: llama3.1:8b
  reviewer_provider: ollama
  reviewer_confidence: 0.9
  reviewer_reason: 'pre_review_filter: concept_requires_pattern: concept->concept, occ>=2, ''shall comply'' language'
  local_review_decision: keep
  local_reviewer_confidence: 0.9
  extracted_at_utc: 20260424T175258Z
  reviewed_at_utc: 20260424T175258Z
  raw_source_trust_level: null
  source_trust_normalized_from: null
- source_id: concept-stairs
  source_section_id: section-3.301
  evidence_snippet: '- 3) Stairs and other exits shall be so arranged as to make clear the direction of egress to the street. Exit stairs that continue beyond the·floor of discharge shall be interrupted at the floor of discharge by partitions, door·s, or other effective means. - 4) Stairs, ramps, bridges, balconies, esc'
  review_decision: keep
  reviewer_model: unknown
  reviewer_provider: ollama
  reviewer_confidence: 1.0
  reviewer_reason: skip_review pipeline path for source-george-salvan-architectural-practice-and-construction-management
  local_review_decision: keep
  local_reviewer_confidence: 1.0
  extracted_at_utc: 20260505T115023Z
  reviewed_at_utc: 20260505T115023Z
  raw_source_trust_level: null
  source_trust_normalized_from: null
---

# concept-stairs requires concept-means-of-egress

## Relationship Summary

Promoted relationship of type `requires` from `concept-stairs` to `concept-means-of-egress`.

## Evidence

### Evidence 1 - `concept-stairs` §section-10.2.5.2

> - 4. Stairs, ramps, bridges, balconies, escalators, moving walks and other components of an exit discharge shall comply with the detailed requirements of this Division for such components. - 5. Subject to the approval of the C/MFM having jurisdiction, exits may be accepted to discharge to roofs or o

- Reviewer: `llama3.1:8b` · Decision: `keep` · Confidence: `0.9`
- Reviewed: 20260424T174130Z
- Batch: `20260505T115023Z_15687c61`

### Evidence 2 - `concept-stairs` §section-10.2.5.4

> Where specifically permitted for individual occupancies by Divisions 8 to 17 of this Chapter, spiral stairs as a component of means of egress shall comply with the following:

- Reviewer: `llama3.1:8b` · Decision: `keep` · Confidence: `0.9`
- Reviewed: 20260424T175258Z
- Batch: `20260505T115023Z_15687c61`

### Evidence 3 - `concept-stairs` §section-3.301

> - 3) Stairs and other exits shall be so arranged as to make clear the direction of egress to the street. Exit stairs that continue beyond the·floor of discharge shall be interrupted at the floor of discharge by partitions, door·s, or other effective means. - 4) Stairs, ramps, bridges, balconies, esc

- Reviewer: `unknown` · Decision: `keep` · Confidence: `1.0`
- Reviewed: 20260505T115023Z
- Batch: `20260505T115023Z_15687c61`

