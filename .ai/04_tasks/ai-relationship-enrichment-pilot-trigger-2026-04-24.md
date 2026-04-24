---
task: ai-relationship-enrichment-pilot
phase: 05
created: 2026-04-24
author: IMPLEMENTER
supersedes: null
status: ACCEPTED
---

# Trigger — AI Relationship Enrichment Pilot

## Task Statement
Implement a bounded AI-assisted relationship candidate-generation pilot that integrates with Vitruvius without adding external API endpoints or bypassing existing review/promotion safeguards.

## In Scope
- Reuse the existing Phase 5E relationship proposer path.
- Constrain AI output with section-local canonical concept IDs and taxonomy context.
- Keep `p5e_llm_extraction` feature-flag behavior safe.
- Preserve regex precedence on overlap.
- Add tests and validation evidence for candidate-generation behavior only.

## Out of Scope
- Direct promotion of AI candidates.
- Full-corpus backfill.
- New predicate vocabulary.
- Explorer UI changes.

## Risk Class
- **M** — central relationship extraction code is touched, but the behavior remains feature-flagged and candidate-only.

## Linked Artifacts
- Research: `.ai/13_research/2026-04-24_ai_relationship_enrichment_pilot_research.md`
- Audit: `.ai/02_audits/2026-04-24_ai_relationship_enrichment_pilot_audit.md`
- Plan: `.ai/03_plans/2026-04-24_ai_relationship_enrichment_pilot_plan.md`
- Validation: `.ai/05_logs/2026-04-24_ai_relationship_enrichment_pilot_validation.md`

## Acceptance Boundary
The task is complete when Phase 5E can propose safe, whitelisted relationship candidates through the existing local-model path and all generated candidates remain review/promotion candidates rather than admitted truth.
