# Alias Redirect Tombstone Report

Date: 2026-05-01

## Production records

- Aliases: 0
- Redirects: 0
- Tombstones: 0

No alias, redirect, or tombstone was applied to concrete, reinforced concrete, P1 groups, or any other production node.

## Infrastructure changes

The canonical stewardship model now validates and reports:

- alias cycles,
- redirect cycles,
- aliases pointing to missing nodes,
- redirects pointing to missing nodes,
- tombstones without reasons,
- tombstone policy violations for live edges or Resource Layer links,
- rejected/deprecated aliases ignored by canonical status/search,
- duplicate exact alias records,
- alias records involving redirected source nodes,
- redirect target/source conflicts involving alias participants.

## Kimi review disposition

Accepted:
- Add explicit cycle and missing-target validation.
- Avoid search/status use of rejected or deprecated aliases.
- Warn on duplicate alias records.

Deferred:
- Full operation-scoped admin tokens.
- Complete tombstone migration path.
- Resource link rewrite policy for future destructive merges.
- Stronger two-person review for remediation waivers.

## Validation

`bun run api/validateCanonicalGraphStewardship.ts` reports `aliases: 0`, `redirects: 0`, `tombstones: 0`, `aliasCycles: 0`, `redirectCycles: 0`, `tombstonePolicyViolations: 0`, and no blockers.
