# Laws Tranche Implementation Context

## Task
Implement the next safe step after all-laws readiness:
1. create tranche-1 manifest(s)
2. run tranche-1 dry-run
3. add stronger automated guardrail checks so BP220-style shallowness is surfaced automatically

## Desired outcome
- a concrete tranche-1 manifest strategy/materialization
- a tranche dry-run command or flow that works
- additive automated guardrails that flag laws with rich section structure but weak concept admission / shallow graph representation
- no accidental generic all-laws execute path

## Known facts
- bounded 4-law pilot is successful and working
- all-laws readiness dry-run now exists and works
- `m2-8gb-safe` preset exists and works
- latest readiness evidence: 47 law folders, 183 PDFs, 43 inventory-only beyond the current pilot
- BP220 currently has one admitted BP220-native concept path but ~60 extracted structural headers and 12 BP220-backed edges to shared concepts
- current graph contract remains concept-centric, not section-hierarchy-centric

## Constraints
- preserve Phase 11 gating
- tranche-based expansion only
- machine safety on M2 8GB first
- additive / reversible changes only
- keep code and truth integrity first

## Likely touchpoints
- config/datasets/
- scripts/vitruvius/laws_readiness.py
- scripts/vitruvius/dataset_pipeline.py
- scripts/pipeline_cli.py
- scripts/vitruvius/cli_experience.py
- scripts/tests/test_dataset_pipeline_cli.py
- scripts/tests/test_dataset_source_to_graph_pipeline.py
- .ai planning/audit/log artifacts
