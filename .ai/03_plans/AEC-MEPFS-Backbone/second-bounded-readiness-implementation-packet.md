---
task: aec-mepfs-backbone
phase: second-bounded-readiness-implementation-packet
created: 2026-04-25
author: CODEX
status: IMPLEMENTED-VALIDATED
---

# Second Bounded Readiness Implementation Packet

## Slice ID

`AEC-BB-S2`: executable readiness fixture validation.

## Goal

Extend the file-backed Backbone contract validator so readiness fixtures can
check the next control surfaces before runtime code consumes them:

- predicate registry rows
- source-rights registry rows
- authoring and migration QA cases
- resolver golden cases
- API / Explorer parity cases
- shadow rollback plan metadata

## Scope

Allowed write scope:

- `scripts/vitruvius/kg/backbone_contracts.py`
- `scripts/tests/test_kg_backbone_contracts.py`
- `scripts/tests/fixtures/aec_mepfs_backbone/valid_readiness_s2.json`
- AEC-MEPFS readiness docs and validation logs

## Explicit Non-Scope

This slice did not authorize or perform:

- KG schema migration
- Neo4j writes, backup, restore, cleanup, or reset
- graph rebuild
- API or Explorer route changes
- feature-flag changes
- canonical taxonomy source admission
- protected standards, legal clause, table, figure, or source-text ingest

## Contract Added

The validator now fails closed for malformed known list sections and validates:

- registered predicates only; vague predicates remain blocked
- predicate rows with owner, direction, domain/range, examples,
  non-examples, evidence fields, validation rule, and migration behavior
- source-rights rows with official URL, clearance state, steward owner,
  currentness check date, declared use boundary, update cadence, and blocking
  notes
- `content_ingest` claims requiring `cleared_for_declared_use`,
  `legal_reviewer`, and `reviewer_decision`
- AI-authored L1/L2 changes as blocked
- L3/L4 auto-accept only through LD-8 `PlacementAssertion` with confidence
  `>= 0.92`
- resolver golden cases using `effective_date`, valid result types, valid
  confidence classes, and coverage for `single_value`, `composed`,
  `conflict`, and `none`
- API / Explorer v1 parity cases preserving v1 behavior
- API / Explorer v2 cases using `/v2` shadow routes and `shadow_only`
- API / Explorer parity cases rejecting unsupported surfaces outside `v1` and
  `v2`
- shadow rollback plans keeping destructive operations blocked and warning when
  rollback proof is planned but not executed

## Fixture Added

`scripts/tests/fixtures/aec_mepfs_backbone/valid_readiness_s2.json` is a
contract fixture, not canonical source admission.

It contains metadata-only examples for:

- 12 first-slice predicate registry entries
- 3 source-rights registry rows
- 3 authoring/migration QA cases
- 4 resolver golden cases covering all resolver result types
- 3 API / Explorer parity cases
- a planned, not executed, shadow rollback plan

## Validation

Focused validation:

```bash
PYTHONPATH=scripts python3 -m pytest scripts/tests/test_kg_backbone_contracts.py -q
```

Result:

```text
25 passed
```

Additional checks:

```bash
python3 -m json.tool scripts/tests/fixtures/aec_mepfs_backbone/valid_readiness_s2.json
python3 -m py_compile scripts/vitruvius/kg/backbone_contracts.py
python3 -m compileall -q scripts/vitruvius/kg/backbone_contracts.py scripts/tests/test_kg_backbone_contracts.py
```

All passed.

## Remaining Blockers

`AEC-BB-S2` improves executable readiness but does not make the full
architecture ready for runtime implementation. The remaining blockers are:

- independent second review
- legal/licensing reviewer decision for any use beyond reference/crosswalk
- production source-rights registry location and release process
- exact API / Explorer response fixtures and v1/v2 parity runner
- backup/export and restore proof
- benchmark corpus, repetition policy, and percentile reporting
- accepted runtime registries and canonical source files
