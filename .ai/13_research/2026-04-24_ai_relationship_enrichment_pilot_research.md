---
task: ai-relationship-enrichment-pilot
phase: 05
created: 2026-04-24
author: IMPLEMENTER
supersedes: null
status: ACCEPTED
---

# Research Pack — AI Relationship Enrichment Pilot

## 01 — User Intent
The user wants the knowledge graph to become structurally richer and semantically deeper, and explicitly prefers using available local/OpenCode-compatible AI paths rather than adding new external API endpoints.

## 02 — Existing Enrichment Surface
The repository already contains a dormant Phase 5E seam:
- `scripts/vitruvius/relationships/llm_proposer.py`
- `scripts/vitruvius/relationships/phase_5e_merger.py`
- `scripts/vitruvius/relationships_sections.py`
- feature flag: `p5e_llm_extraction`

This is the narrowest safe insertion point because it feeds existing extraction reports into the already-shipped review and promotion path.

## 03 — Local Model Pattern
The existing local-first AI pattern is Ollama-backed and configured through `scripts/vitruvius/config.py` plus `config/vitruvius.yaml`. The implementation should therefore resolve default model and timeout via config helpers rather than hard-code a model.

## 04 — Safety Findings
- AI output must remain candidate generation, not truth admission.
- Candidate endpoints must be whitelisted to known IDs.
- If no concept context is available, generation should skip rather than allow invented concept IDs.
- Local models may return a single JSON object despite an array contract; parsing can normalize this shape only before applying all existing filters.

## 05 — Validation Implications
Validation must prove stable invariants rather than exact local-model wording:
- feature flag off keeps the previous report shape;
- no-context sections produce no AI candidates;
- whitelisted context admits only known endpoint IDs;
- regex still wins on overlap;
- local Ollama can execute the path and produce at least one candidate under a bounded prompt.
