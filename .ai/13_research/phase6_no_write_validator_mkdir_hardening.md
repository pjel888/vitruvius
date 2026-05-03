# Phase 6 No-Write Validator Mkdir Hardening

Date: 2026-05-03T03:45:00+08:00

## Issue

`api/validateCanonicalGraphStewardship.ts` called `mkdirSync(dirname(validationReportPath), { recursive: true })` unconditionally before the `noWrite` guard.

This did not dirty the current repo because `.ai/13_research/` already exists, but in a fresh checkout it would create the directory even in no-write mode.

## Fix Applied

Moved `mkdirSync` inside the `if (!noWrite)` block:

```ts
// Before (line 65)
mkdirSync(dirname(validationReportPath), { recursive: true });
const report = [
  // ...
];
if (!noWrite) {
  writeFileSync(validationReportPath, report, 'utf-8');
}

// After
const report = [
  // ...
];
if (!noWrite) {
  mkdirSync(dirname(validationReportPath), { recursive: true });
  writeFileSync(validationReportPath, report, 'utf-8');
}
```

## Verification

- `bun run api/validateCanonicalGraphStewardship.ts --no-write` runs successfully.
- `git status --short` before and after no-write run: no changes.
- Normal mode (without `--no-write`) still writes reports correctly.

## Other Validators

| Validator | Mkdir in No-Write? | Status |
|-----------|-------------------|--------|
| `validateGraphRelationships.ts` | No mkdir used | ✅ Clean |
| `validateCanonicalGraphStewardship.ts` | Fixed | ✅ Clean |
| `validateResourceLayer.ts` | No file writes at all | ✅ Clean |

## Future Hardening

If additional validators are added, they should follow the same pattern:
- All filesystem mutations guarded by `!noWrite`.
- No-write mode must be pure computation + stdout.
