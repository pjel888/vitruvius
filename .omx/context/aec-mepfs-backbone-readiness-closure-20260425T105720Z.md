# Ralph Context Snapshot — AEC-MEPFS Backbone Readiness Closure

## Task Statement
Proceed autonomously through all non-destructive work needed to make the
AEC-MEPFS Backbone packet ready for bounded integration. The user does not want
repeated readiness check-ins.

## Desired Outcome
- Close every readiness gate that can be closed locally with docs, fixtures,
  validators, tests, impact evidence, and explicit execution packets.
- Keep runtime integration blocked until evidence proves the gates are actually
  closed.
- Clearly distinguish locally closable gates from gates requiring external legal
  review, human steward approval, or database backup/restore authority.

## Known Facts / Evidence
- Current phase: AEC-MEPFS Backbone readiness gate.
- Latest commits:
  - `d35d0ead` S2 readiness validator fixtures.
  - `2e598671` post-commit impact evidence.
- GitNexus is current at `2e59867`.
- Focused S2 validator tests pass: `25 passed`.
- Dirty worktree before this session: unrelated `explorer/package.json`.
- Existing readiness docs still say runtime implementation is not ready.

## Constraints
- Do not wire the Backbone into KG runtime, Neo4j, API, Explorer, feature flags,
  graph rebuilds, or destructive cleanup during readiness closure.
- Do not edit high-risk runtime roots such as `CanonicalNode`, `TaxonomyLoader`,
  `Neo4jLoader`, API handlers, Explorer graph clients, or config flags unless a
  later approved runtime packet explicitly authorizes it.
- Do not treat fixture rows as canonical taxonomy or legal/source clearance.
- No new dependencies.
- Preserve unrelated dirty files.

## Unknowns / Open Questions
- Whether a fully executed Neo4j backup/restore proof can be run safely in the
  current local environment without stopping or mutating the active database.
- Who will perform independent legal/licensing review for content beyond
  reference/crosswalk use.
- Which canonical release location should later hold admitted runtime registries
  after steward approval.

## Likely Codebase Touchpoints
- `.ai/03_plans/AEC-MEPFS-Backbone/`
- `.ai/05_logs/`
- `.ai/ACTIVE_WORK.md`
- `.ai/STRATEGIC_NEXT_MOVE.md`
- `.omx/plans/`
- `scripts/vitruvius/kg/backbone_contracts.py`
- `scripts/tests/test_kg_backbone_contracts.py`
- `scripts/tests/fixtures/aec_mepfs_backbone/`
