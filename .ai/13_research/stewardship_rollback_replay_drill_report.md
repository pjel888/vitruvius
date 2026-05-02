# Stewardship Rollback Replay Drill Report

Date: 2026-05-02

## Drill type

Fixture-only non-destructive edge admission drill. No production P0 decision was admitted or rolled back.

## What was tested

The API test `approval gate blocks admission without required steward metadata and admits non-destructive fixture edges with rollback/replay` exercises:
1. Proposed `DISAMBIGUATED_KEEP_SEPARATE` decision creation for fixture Concrete nodes.
2. Approval preview blocker when required steward metadata is missing.
3. Fixture approval with `test_fixture` source in test mode only.
4. Non-destructive relationship admission.
5. Canonical validation after admission.
6. Rollback preview and rollback apply.
7. Preservation of rolled-back admitted relationship history.
8. Replay/re-approval after rollback without deleting history.

## Result

- Rollback capability: full for the fixture non-destructive edge admission.
- Resource Layer links: unchanged.
- Graph node/edge production files: not mutated.
- Transaction manifests: written through the canonical transaction manifest path.
- Remediation manifests: not required for the fixture because rollback was full.

## Limitations

- Production P0 rollback was not run because no real steward approval/admission occurred.
- Destructive merge rollback remains partial/guarded and requires remediation manifests when information cannot be restored automatically.
