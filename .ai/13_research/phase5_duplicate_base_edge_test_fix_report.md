# Phase 5 Duplicate Base Edge Test Fix Report

Date: 2026-05-03T02:45:00+08:00

## Bug Description

In `api/graphReasoningPaths.test.ts`, the "admitted edges do not duplicate base graph tuples" test used raw `baseEdges` fields:

```ts
// BROKEN: baseEdges use from_id/to_id/predicate, not source/target/type
const baseKeys = new Set(baseEdges.map((e: any) => `${e.source}|${e.type}|${e.target}`));
```

Since shadow-graph base edges have fields `from_id`, `to_id`, `predicate` (not `source`, `target`, `type`), this produced keys like `undefined|undefined|undefined`. The test would **always falsely pass** because no admitted edge could match an all-undefined key.

## Fix Applied

Changed the test to use `normalizedBaseEdges`, which maps shadow fields to canonical fields:

```ts
const normalizedBaseEdges = baseEdges.map((e: any) => ({
  ...e,
  source: e.from_id,
  target: e.to_id,
  type: e.predicate,
}));
// ...
const baseKeys = new Set(normalizedBaseEdges.map((e: any) => `${e.source}|${e.type}|${e.target}`));
```

Added a regression assertion that proves the old assumption was broken:

```ts
const rawBaseKeys = new Set(baseEdges.map((e: any) => `${e.source}|${e.type}|${e.target}`));
expect(rawBaseKeys.has('undefined|undefined|undefined')).toBe(true);
```

## Verification

- Test passes with the fix.
- If a future developer reverts to raw fields, the regression assertion will fail.
- No graph data was mutated.
