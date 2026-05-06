---
id: rel-source-2020-2030-clup-volume-2-final-las-pinas-governs-concept-waste-disposal
title: source-2020-2030-clup-volume-2-final-las-pinas governs concept-waste-disposal
page_type: relationship
relationship_type: governs
from_entity: source-2020-2030-clup-volume-2-final-las-pinas
to_entity: concept-waste-disposal
trust_level: unverified
canonical_status: promoted
confidence_score: 0.95
promotion_batch_id: 20260505T114917Z_eb76c3b6
promotion_audit_log_ref: 006_System-Manifests\runs\kg_pipeline_20260505T095933Z\promotion_audit.log
last_promoted_utc: 20260505T114917Z
evidence:
- source_id: source-2020-2030-clup-volume-2-final-las-pinas
  source_section_id: section-12.2.1
  evidence_snippet: '>» Waste Disposal/Trash Removal - The collection and disposal of industri waste shall be the responsibility of the operators and shall be in accordance with P.D.'
  review_decision: keep
  reviewer_model: llama3.1:8b
  reviewer_provider: ollama
  reviewer_confidence: 0.95
  reviewer_reason: 'pre_review_filter: structural_governs_pattern: source->concept, occ>=3, characteristic language'
  local_review_decision: keep
  local_reviewer_confidence: 0.95
  extracted_at_utc: 20260424T170550Z
  reviewed_at_utc: 20260424T170550Z
  raw_source_trust_level: unknown
  source_trust_normalized_from: unknown
- source_id: source-2020-2030-clup-volume-2-final-las-pinas
  source_section_id: section-12.2.2
  evidence_snippet: 1185 (Fire Code of the Philippines) » Waste Disposal/Trash Removal - The collection and disposal of industri waste shall be the responsibility of the operators and shall be in
  review_decision: keep
  reviewer_model: unknown
  reviewer_provider: ollama
  reviewer_confidence: 1.0
  reviewer_reason: skip_review pipeline path for source-2020-2030-clup-volume-2-final-las-pinas
  local_review_decision: keep
  local_reviewer_confidence: 1.0
  extracted_at_utc: 20260505T114917Z
  reviewed_at_utc: 20260505T114917Z
  raw_source_trust_level: unknown
  source_trust_normalized_from: unknown
---

# source-2020-2030-clup-volume-2-final-las-pinas governs concept-waste-disposal

## Relationship Summary

Promoted relationship of type `governs` from `source-2020-2030-clup-volume-2-final-las-pinas` to `concept-waste-disposal`.

## Evidence

### Evidence 1 - `source-2020-2030-clup-volume-2-final-las-pinas` §section-12.2.1

> >» Waste Disposal/Trash Removal - The collection and disposal of industri waste shall be the responsibility of the operators and shall be in accordance with P.D.

- Reviewer: `llama3.1:8b` · Decision: `keep` · Confidence: `0.95`
- Reviewed: 20260424T170550Z
- Batch: `20260505T114917Z_eb76c3b6`

### Evidence 2 - `source-2020-2030-clup-volume-2-final-las-pinas` §section-12.2.2

> 1185 (Fire Code of the Philippines) » Waste Disposal/Trash Removal - The collection and disposal of industri waste shall be the responsibility of the operators and shall be in

- Reviewer: `unknown` · Decision: `keep` · Confidence: `1.0`
- Reviewed: 20260505T114917Z
- Batch: `20260505T114917Z_eb76c3b6`

