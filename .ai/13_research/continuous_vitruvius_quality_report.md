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

---

## Latest manifest afterHash enforcement quality update

Last updated: 2026-05-02T02:20:03Z

### Quality gates checked

- API tests: passed (cd api && bun test, 159 tests).
- Explorer tests: passed (cd explorer && bun test, 111 tests).
- Explorer build: passed with known Vite chunk-size warning.
- Graph relationship validation: passed; nodes 10,018, edges 13,670, issues 0.
- Resource Layer validation: passed with known standards-context warnings for ASCE 7 and ACI 318.
- Canonical stewardship validation: passed in non-strict mode.
- Canonical strict latest-afterHash smoke test: passed because all latest manifest-governed files matched current file bytes.
- AEC relationship-improvement tests: passed via .\.venv\Scripts\python.exe -m pytest ...; direct pytest command is unavailable in this shell.

### Safety status

- No fake approval created.
- No production duplicate merge applied.
- No aliases, redirects, tombstones, or admitted production graph edges added.
- No Resource Layer resources or nodeResourceLinks changed.
- P1 packets remain advisory and unsigned in this environment.
- Latest afterHash validation checks byte-level custody drift only; it does not prove approval, ontology truth, source truth, or merge safety.

### Known caveats

- Resource Layer transaction manifests are supported by the validator but none are present in this repo state.
- Unmanifested legacy custody-critical files are not strict-blocked yet; enforcement currently focuses on files with manifest coverage to avoid bootstrap false positives.
- Standards-context warnings remain for ASCE 7 and ACI 318.
