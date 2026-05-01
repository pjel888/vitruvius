# Ralph Context Snapshot — AEC-MEPFS Backbone Readiness S2

## Task Statement
Proceed with the next bounded AEC-MEPFS Backbone readiness tasks after
`AEC-BB-S1` landed: authoring/migration QA fixtures, source-rights registry
rows, executable predicate controls, resolver/API parity fixtures, and shadow
graph rollback evidence planning.

## Desired Outcome
- Improve readiness artifacts without wiring the Backbone into KG runtime,
  Neo4j, API, Explorer, graph rebuilds, or feature flags.
- Keep changes bounded to file-backed contract validation, fixtures, and
  planning/status artifacts.
- Produce fresh verification evidence and architect review before completion.

## Known Facts / Evidence
- Latest committed implementation: `80540048 Validate backbone registry
  candidates before runtime wiring`.
- GitNexus status is current at indexed commit `8054004`.
- Focused validator tests for `AEC-BB-S1` passed: 8 tests.
- The planning packet remains `ACCEPTED-READINESS-CONTROL`, not
  `ACCEPTED-FOR-IMPLEMENTATION`.
- Current dirty worktree before this session: unrelated `explorer/package.json`.

## Constraints
- Do not rebuild KG, reset Neo4j, alter graph loaders, or change Explorer/API
  runtime behavior.
- Do not touch high-risk KG roots such as `CanonicalNode`, `TaxonomyLoader`, or
  `Neo4jLoader` in this slice.
- Preserve unrelated dirty files.
- Prefer deterministic, file-backed validation with focused tests.
- No new dependencies.

## Unknowns / Open Questions
- Exact canonical source-rights rows are not yet admitted as runtime registry
  truth; fixtures can model the contract only.
- API/Explorer parity fixtures can define contract shapes, but runtime endpoints
  remain future work.
- Backup/restore rollback proof should remain a protocol/checklist until a
  shadow database environment is explicitly authorized.

## Likely Codebase Touchpoints
- `scripts/vitruvius/kg/backbone_contracts.py`
- `scripts/tests/test_kg_backbone_contracts.py`
- `scripts/tests/fixtures/aec_mepfs_backbone/`
- `.ai/03_plans/AEC-MEPFS-Backbone/`
- `.ai/05_logs/`
