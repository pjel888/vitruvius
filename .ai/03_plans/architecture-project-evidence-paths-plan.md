# Architecture project evidence paths implementation plan

## Objective
Deepen the architecture interconnectivity graph with project-specific, source-safe evidence paths and resolver/API/UI assertions.

## Implementation steps
1. Extend `architecture_interconnectivity_enrichment.py` with additional high-confidence work/project anchor nodes, material/system/method nodes, and relationship batches.
2. Add relationship rationale categories for project-specific paths while preserving existing governed predicates.
3. Add resolver golden cases for specific path questions and stale-label prevention.
4. Regenerate file-backed fixture, source-rights registry if needed, resolver fixture, shadow staging, and resolver QA artifacts only through approved file-backed workflow.
5. Update tests/count contracts and API/Explorer assertions.
6. Run focused, broad, API, Explorer, shadow, JSON, safety, Kimi, and GitNexus validation.

## Plan critique
- Avoid overclaiming exact material use where public sources are ambiguous; prefer work->system/movement/design concept paths unless material is widely verified.
- Do not chase counts at the expense of path quality.
- Do not change live graph or production Neo4j surfaces.
- Do not use direct person->material links because they are less explanatory and easier to overclaim.
