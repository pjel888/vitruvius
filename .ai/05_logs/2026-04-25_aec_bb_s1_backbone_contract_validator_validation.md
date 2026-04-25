# AEC-BB-S1 Backbone Contract Validator Validation

**Date:** 2026-04-25
**Status:** validated

## Scope

Implemented the first bounded AEC-MEPFS Backbone code slice:

- static, file-backed validator only
- no KG schema migration
- no `TaxonomyLoader`, `UnifiedSnapshotBuilder`, `CanonicalNode`, `Neo4jLoader`,
  relationship enricher, API, Explorer, or feature-flag edits
- no Neo4j writes
- no graph rebuild
- no canonical content admission
- no protected source ingest

## Files

- `scripts/vitruvius/kg/backbone_contracts.py`
- `scripts/tests/test_kg_backbone_contracts.py`
- `scripts/tests/fixtures/aec_mepfs_backbone/valid_minimal.json`

## Behavior Validated

- valid minimal candidate fixture passes
- invalid VTN ID fails
- vague governed predicate fails
- unknown governed predicate fails
- content-ingest source without clearance fails
- missing owner fails
- jurisdiction-mutated canonical record fails
- report ordering is deterministic

## Commands

```bash
PYTHONPATH=scripts python3 -m pytest scripts/tests/test_kg_backbone_contracts.py -q
python3 -m py_compile scripts/vitruvius/kg/backbone_contracts.py
git diff --check -- scripts/vitruvius/kg/backbone_contracts.py scripts/tests/test_kg_backbone_contracts.py scripts/tests/fixtures/aec_mepfs_backbone/valid_minimal.json
```

## Result

- focused pytest: 8 passed
- syntax compile: passed
- diff whitespace check: passed

## Remaining Risks

- This validator is not wired into pipeline, API, Explorer, Neo4j, or feature
  flags by design.
- Runtime Backbone work remains blocked until the readiness packet reaches
  `ready for bounded implementation`.
- Source-rights and governance gaps remain as recorded in the readiness packet:
  legal/licensing reviewer, independent second reviewer, discipline reviewers,
  fixture corpus, rollback proof, and parity evidence are still open.
