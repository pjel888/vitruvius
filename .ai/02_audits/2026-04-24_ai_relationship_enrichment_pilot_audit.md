---
task: ai-relationship-enrichment-pilot
phase: 05
created: 2026-04-24
author: IMPLEMENTER
supersedes: null
status: ACCEPTED
---

# AI Relationship Enrichment Pilot Audit — 2026-04-24

## Purpose
Define the safest insertion point for AI-assisted relationship enrichment in Vitruvius without adding a new external API service.

## Current State
- The repository already contains a dormant Phase 5E path:
  - `scripts/vitruvius/relationships/llm_proposer.py`
  - `scripts/vitruvius/relationships/phase_5e_merger.py`
  - feature flag: `p5e_llm_extraction`
- This path is already wired into `scripts/vitruvius/relationships_sections.py::run_extract_relationships_sections_one_inner()`.
- Today the proposer is too shallow:
  - prompt only sees `section_text`, `section_id`, `source_id`
  - no taxonomy context
  - no explicit candidate concept whitelist
  - no provenance metadata beyond evidence/confidence
  - no report visibility for regex vs AI counts

## Best Insertion Point
The correct bounded insertion point is **before review, inside section extraction**, where regex candidates are already being produced and deduped.

Why this is the best seam:
- Reuses existing review and promotion layers.
- Keeps AI output as **candidate generation**, not direct truth admission.
- Preserves the fallback path: regex-only remains available when the feature flag is off or the local model path fails.

## Constraints
- No new external API layer should be introduced.
- AI enrichment must remain optional and flag-gated.
- Candidate output must stay inside the closed predicate vocabulary.
- Candidate endpoints must be restricted to known canonical IDs.
- Taxonomy should constrain and inform proposals.

## Existing Assets We Can Reuse
- Prompt template: `.ai/08_prompts/gemma-phase-5e-proposer.txt`
- Model config helpers: `scripts/vitruvius/config.py`
- Review/promotion infrastructure: `scripts/vitruvius/ollama_review.py`, `scripts/vitruvius/promotion/__init__.py`
- Existing tests:
  - `scripts/tests/test_phase_5e_llm_proposer.py`
  - `scripts/tests/test_phase_5e_merger.py`
  - `scripts/tests/test_phase_5e_integration.py`

## Risks
- If the proposer is not constrained, it will generate semantically shallow or invalid edges.
- If AI candidates are merged without provenance/audit visibility, operators cannot distinguish signal from noise.
- If taxonomy context is absent, the proposer will keep generating weak generic relationships.

## Recommended Pilot Scope
Implement a taxonomy-aware proposer that:
- receives a whitelist of known concepts for the section,
- receives taxonomy path hints for those concepts,
- emits candidates only between known canonical IDs,
- records AI-origin metadata in the extraction report,
- keeps regex as the preferred overlap winner.

## Out of Scope
- Bulk re-review of historical graphs.
- Full semantic-enrichment ontology redesign.
- Explorer visualization redesign.
