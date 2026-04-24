---
task: ai-relationship-enrichment-pilot
phase: 05
created: 2026-04-24
author: IMPLEMENTER
supersedes: null
status: ACCEPTED
---

# AI Relationship Enrichment Pilot Validation — 2026-04-24

## Scope
Validated the bounded Phase 5E AI relationship enrichment pilot.

## Implemented Outcomes
- Existing Phase 5E proposer now accepts grounded concept context.
- Proposer prompt includes allowed concept IDs and taxonomy paths when supplied.
- Proposer rejects endpoints outside `{section_id, source_id, supplied concept ids}` when concept context is supplied.
- Proposer skips generation entirely when no concept context is available, preventing invented concept IDs from entering extraction reports.
- Proposer now resolves the default model and timeout through existing `vitruvius.config` helpers instead of hard-coding a model.
- Proposer normalizes a single JSON object response from local models into a one-candidate list before applying the same safety filters.
- Relationship section extraction preloads concept context once per extraction run and filters it per section.
- Extraction report includes `phase_5e.enabled`, `regex_candidate_count`, `ai_candidate_count`, and `merged_candidate_count` only when Phase 5E is enabled, preserving flag-off report shape.

## Automated Validation

```bash
python3 -m pytest scripts/tests/test_phase_5e_llm_proposer.py scripts/tests/test_phase_5e_merger.py scripts/tests/test_phase_5e_integration.py scripts/tests/test_relationships_sections_split.py -q
```

Result: **26 passed**

```bash
python3 -m pytest scripts/tests/test_kg_pipeline_force_path.py -k phase3_report_uses_relationship_and_promotion_counts -q
```

Result: **1 passed, 10 deselected**

```bash
python3 -m pytest scripts/tests/test_features.py -q
```

Result: **24 passed**

```bash
python3 -m compileall -q scripts/vitruvius/relationships/llm_proposer.py scripts/vitruvius/relationships_sections.py
```

Result: **pass**

## Manual QA
Executed `run_extract_relationships_sections_one_inner()` with Phase 5E enabled and a stubbed proposer to avoid requiring a live local model during validation.

Observed output:
- exit code: `0`
- `phase_5e.enabled`: `true`
- `regex_candidate_count`: `1`
- `ai_candidate_count`: `1`
- `merged_candidate_count`: `2`
- relationships included one `regex` candidate and one `llm_proposer` candidate.

Also executed a real local-model smoke through the configured Ollama path:

```bash
python3 - <<'PY'
from vitruvius.config import get_ollama_default_timeout, resolve_review_model
from vitruvius.relationships.llm_proposer import ConceptContext, propose_relationships_llm

model = resolve_review_model()
timeout = min(get_ollama_default_timeout(), 30)
result = propose_relationships_llm(
    section_text='Mixed occupancy shall comply with the most restrictive occupancy classification.',
    section_id='section-701',
    source_id='law-test',
    model=model,
    timeout_seconds=timeout,
    concept_context=[
        ConceptContext(id='concept-mixed-occupancy', label='Mixed Occupancy', taxonomy_path=('taxonomy-building-code','topic-occupancy')),
        ConceptContext(id='concept-occupancy-classification', label='Occupancy Classification', taxonomy_path=('taxonomy-building-code','topic-occupancy')),
    ],
)
print({'model': model, 'timeout_seconds': timeout, 'candidate_count': len(result)})
PY
```

Observed output: `{'model': 'llama3.1:8b', 'timeout_seconds': 30, 'candidate_count': 0, ...}`. Empty candidate output is allowed by the proposer contract.

After fixing the observed single-object local-model response shape, reran the real local-model smoke with a 60-second timeout.

Observed output:
- model: `llama3.1:8b`
- candidate count: `1`
- candidate endpoints were whitelisted canonical concept IDs.

The exact predicate emitted by the local model is not a stable validation claim. Fresh local-model reruns may emit different allowed predicates (for example `requires` or `defines`) for the same bounded text. The stable claim is that the local model path returns parseable output and the proposer applies the closed-predicate and endpoint-whitelist filters before returning any candidate.

Verified local Ollama availability via `/api/tags`:
- service reachable: `true`
- configured model: `llama3.1:8b`
- model available: `true`

Executed a real-model extraction-path smoke with Phase 5E enabled and no stubbed proposer. Observed:
- exit code: `0`
- `phase_5e.enabled`: `true`
- `regex_candidate_count`: `1`
- `ai_candidate_count`: `1`
- `merged_candidate_count`: `1`

The final relationship was regex-origin because regex correctly wins on an overlapping AI candidate.

Independent Oracle rerun observed the same stable safety boundary with a different merged-count outcome (`merged_candidate_count: 2`) due to local-model output variability before final dedupe/overlap behavior. Therefore, the stable validation claim is not an exact merged count; it is:
- the local configured model path executes successfully;
- at least one AI candidate can be generated under bounded concept context;
- candidates remain constrained by predicate and endpoint filters;
- regex precedence applies when AI overlaps regex;
- candidate count variability is expected and must be reviewed before promotion.

## Review
Initial Oracle verification did not pass. The following blockers were fixed afterward:
- no-context proposer path now returns `[]` before any model call;
- default model and timeout now resolve through `vitruvius.config`;
- `phase_5e` report metadata is omitted when the feature flag is off;
- local Ollama/model availability was checked and a real configured-model smoke was run;
- state docs were reconciled so the pilot is completed/reference, not an active next-action item.
- local-model single-object responses are now accepted and covered by regression tests.

Post-fix validation:
- targeted Phase 5E/extraction tests: **26 passed**
- affected KG pipeline report test: **1 passed, 10 deselected**
- feature flag tests: **24 passed**
- modified Python compile check: **pass**

## Caveats
- This slice improves AI candidate generation, not direct promotion or historical graph backfill.
- Full-corpus enrichment still depends on the operator enabling `p5e_llm_extraction` and reviewing generated candidates before promotion.
