# Continuous Vitruvius Quality Report

Last updated: 2026-05-02T01:54:10Z

## Quality gates checked

- API tests: passed (`cd api && bun test`, 157 tests).
- Explorer tests: passed (`cd explorer && bun test`, 111 tests).
- Explorer build: passed with known Vite chunk-size warning.
- Graph relationship validation: passed; nodes 10,018, edges 13,670, issues 0.
- Resource Layer validation: passed with known standards-context warnings for ASCE 7 and ACI 318.
- Canonical stewardship validation: passed in non-strict mode with unsigned P1 packet warnings.
- Canonical strict-signature smoke test without key: failed as expected with 20 signature blockers.

## Safety status

- No fake approval created.
- No production duplicate merge applied.
- No aliases, redirects, tombstones, or admitted production graph edges added.
- No Resource Layer resources or nodeResourceLinks changed.
- P1 packets remain advisory and explicitly not steward approval, source truth, canonical admission, or merge safety.

## Known caveats

- No packet HMAC key is configured, so regenerated packets are unsigned. This is warning-only outside strict mode.
- Strict packet-signature mode requires a configured key before canonical validation can pass.
- GitNexus/code-review scope remains broad because the worktree includes unrelated/pre-existing AEC relationship-improvement changes.
