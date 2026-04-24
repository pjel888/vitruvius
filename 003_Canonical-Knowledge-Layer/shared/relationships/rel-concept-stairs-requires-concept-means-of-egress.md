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
promotion_batch_id: 20260423T215703Z_b2563c62
promotion_audit_log_ref: 006_System-Manifests/runs/kg_pipeline_20260423T184105Z/promotion_audit.log
last_promoted_utc: 20260423T215703Z
evidence:
- source_id: concept-stairs
  source_section_id: section-3.301
  evidence_snippet: '- 3) Stairs and other exits shall be so arranged as to make clear the direction of egress to the street. Exit stairs that continue beyond the·floor of discharge shall be interrupted at the floor of discharge by partitions, door·s, or other effective means. - 4) Stairs, ramps, bridges, balconies, esc'
  review_decision: keep
  reviewer_model: qwen2.5:3b
  reviewer_provider: ollama
  reviewer_confidence: 0.9
  reviewer_reason: 'pre_review_filter: concept_requires_pattern: concept->concept, occ>=2, ''shall comply'' language'
  local_review_decision: keep
  local_reviewer_confidence: 0.9
  extracted_at_utc: 20260423T213643Z
  reviewed_at_utc: 20260423T213643Z
- source_id: concept-stairs
  source_section_id: section-10.2.5.4
  evidence_snippet: 'Where specifically permitted for individual occupancies by Divisions 8 to 17 of this Chapter, spiral stairs as a component of means of egress shall comply with the following:'
  review_decision: keep
  reviewer_model: qwen2.5:3b
  reviewer_provider: ollama
  reviewer_confidence: 0.9
  reviewer_reason: 'pre_review_filter: concept_requires_pattern: concept->concept, occ>=2, ''shall comply'' language'
  local_review_decision: keep
  local_reviewer_confidence: 0.9
  extracted_at_utc: 20260423T213855Z
  reviewed_at_utc: 20260423T213855Z
- source_id: concept-stairs
  source_section_id: section-10.2.5.2
  evidence_snippet: '- 4. Stairs, ramps, bridges, balconies, escalators, moving walks and other components of an exit discharge shall comply with the detailed requirements of this Division for such components. - 5. Subject to the approval of the C/MFM having jurisdiction, exits may be accepted to discharge to roofs or o'
  review_decision: keep
  reviewer_model: qwen2.5:3b
  reviewer_provider: ollama
  reviewer_confidence: 0.9
  reviewer_reason: 'pre_review_filter: concept_requires_pattern: concept->concept, occ>=2, ''shall comply'' language'
  local_review_decision: keep
  local_reviewer_confidence: 0.9
  extracted_at_utc: 20260423T215703Z
  reviewed_at_utc: 20260423T215703Z
---

# concept-stairs requires concept-means-of-egress

## Relationship Summary

Promoted relationship of type `requires` from `concept-stairs` to `concept-means-of-egress`.

## Evidence

### Evidence 1 - `concept-stairs` §section-3.301

> - 3) Stairs and other exits shall be so arranged as to make clear the direction of egress to the street. Exit stairs that continue beyond the·floor of discharge shall be interrupted at the floor of discharge by partitions, door·s, or other effective means. - 4) Stairs, ramps, bridges, balconies, esc

- Reviewer: `qwen2.5:3b` · Decision: `keep` · Confidence: `0.9`
- Reviewed: 20260423T213643Z
- Batch: `20260423T215703Z_b2563c62`

### Evidence 2 - `concept-stairs` §section-10.2.5.4

> Where specifically permitted for individual occupancies by Divisions 8 to 17 of this Chapter, spiral stairs as a component of means of egress shall comply with the following:

- Reviewer: `qwen2.5:3b` · Decision: `keep` · Confidence: `0.9`
- Reviewed: 20260423T213855Z
- Batch: `20260423T215703Z_b2563c62`

### Evidence 3 - `concept-stairs` §section-10.2.5.2

> - 4. Stairs, ramps, bridges, balconies, escalators, moving walks and other components of an exit discharge shall comply with the detailed requirements of this Division for such components. - 5. Subject to the approval of the C/MFM having jurisdiction, exits may be accepted to discharge to roofs or o

- Reviewer: `qwen2.5:3b` · Decision: `keep` · Confidence: `0.9`
- Reviewed: 20260423T215703Z
- Batch: `20260423T215703Z_b2563c62`
