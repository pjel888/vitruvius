---
task: ai-relationship-enrichment-pilot
phase: 05
created: 2026-04-24
author: IMPLEMENTER
supersedes: null
status: IMPLEMENTED
---

# AI Relationship Enrichment Pilot Plan

## Metadata
- **Status:** implemented and validated
- **Created:** 2026-04-24
- **Audit:** `.ai/02_audits/2026-04-24_ai_relationship_enrichment_pilot_audit.md`

## Goal
Upgrade the existing Phase 5E LLM proposer into a taxonomy-aware, concept-constrained candidate generator that enriches relationship extraction without bypassing review/promotion safeguards.

## Scope

### In Scope
- Improve `llm_proposer.py` prompt/context contract.
- Thread concept/taxonomy context into the proposer from `relationships_sections.py`.
- Preserve feature-flag gating under `p5e_llm_extraction`.
- Add extraction-report visibility for AI-origin candidates.
- Add tests for the new proposer context and merged-report behavior.

### Out of Scope
- Turning AI candidates directly into promoted relationships.
- Rebuilding the entire historical graph corpus.
- External API-based orchestration.
- New predicate vocabulary.

## Implementation Steps

### Step 1 — Strengthen proposer contract
- [ ] Extend `ProposedCandidate` if needed for audit metadata only.
- [ ] Expand prompt input to include:
  - section/source identifiers,
  - known concept IDs for the section,
  - taxonomy hints for those concepts,
  - explicit instruction to avoid unknown IDs.
- [ ] Keep output contract backward-compatible enough for merger/review.

### Step 2 — Pass grounded context from extraction
- [ ] In `relationships_sections.py`, build section-local concept context from matches / concept map.
- [ ] Provide taxonomy hints to the proposer.
- [ ] Merge regex + AI candidates while preserving `source` and AI confidence metadata.

### Step 3 — Make the report auditable
- [ ] Add report counters/fields for:
  - regex candidate count,
  - AI candidate count,
  - merged candidate count,
  - whether Phase 5E was enabled.

### Step 4 — Test the pilot thoroughly
- [ ] Add proposer unit tests for prompt/context building and parsing.
- [ ] Add integration tests for flag-on extraction path with AI candidates.
- [ ] Keep flag-off byte identity.

## Acceptance Criteria
- With `p5e_llm_extraction` off, behavior is unchanged.
- With `p5e_llm_extraction` on, the proposer sees grounded concept/taxonomy context.
- AI candidates never use IDs outside the supplied canonical whitelist.
- Extraction reports make AI contribution visible.
- Existing regex candidates still win on overlap.

## Validation
- Run targeted Phase 5E tests first.
- Run affected KG pipeline tests next.
- Do not claim semantic quality improvements beyond candidate-generation quality in this slice.

## Stop Conditions
- Any flag-off regression.
- Any proposer output contract breakage.
- Any increase in unknown/disallowed IDs or predicates.

## Plan Critique
- The safest seam is the existing Phase 5E proposer hook inside `relationships_sections.py`; adding a parallel KG-native relationship extractor would duplicate review/promotion surfaces and broaden scope.
- The main risk is hallucinated endpoints. The implementation must therefore skip generation without grounded concept context and whitelist all endpoints when context exists.
- The second risk is feature-flag regression. The report shape must remain unchanged when `p5e_llm_extraction` is disabled.
- The third risk is local-model contract variability. The parser must tolerate the observed safe local shape (`dict` singleton) while still rejecting unknown predicates/IDs and malformed output.

## Execution Checklist
- [x] Add proposer concept/taxonomy context contract.
- [x] Add no-context skip to prevent invented concept IDs.
- [x] Resolve default model and timeout through existing config helpers.
- [x] Normalize single-object local-model JSON responses.
- [x] Pass cached concept context from section extraction into proposer.
- [x] Emit Phase 5E counters only when Phase 5E is enabled.
- [x] Add regression tests for prompt context, endpoint filtering, flag-off shape, config defaults, and single-object local responses.
- [x] Run targeted tests, affected pipeline test, feature tests, compile check, stubbed extraction smoke, and real local-model smoke.

## Implementation Result
- Implemented via existing Phase 5E extraction seam.
- Added taxonomy-aware concept context to the proposer prompt.
- Added endpoint whitelist filtering when concept context is supplied.
- Added `phase_5e` extraction-report counters.
- Validation log: `.ai/05_logs/2026-04-24_ai_relationship_enrichment_pilot_validation.md`.
