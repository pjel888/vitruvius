# Audit â€” Explorer Source-Gap Detail Expansion

## Current State

The Explorer rail Source gaps card shows summary counts, a short list of workqueue items, the first resource hint, and node navigation controls. It does not yet expose the proposal rationale or matched-term detail that would help an operator decide what to inspect next.

## Gap

The source-gap preview is useful but still compressed. Operators need an in-place way to inspect:

- why a suggested Resource was proposed
- what terms matched
- which proposal IDs are attached to the workqueue item
- whether the item is node-targeted or relationship-targeted

## Blast Radius

Low:

- Component-only UI state and markup.
- Existing preview endpoint and types are sufficient.
- Existing tests can be extended with fixture proposal data.

## Safety

The proposed detail panel is display-only. It must keep the same read-only copy and must not add any apply/admit/approve controls.
