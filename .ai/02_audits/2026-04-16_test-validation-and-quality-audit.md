---
task: vitruvius-audit-pass-1
phase: 04
created: 2026-04-16
author: AUDITOR
supersedes: null
status: ACCEPTED
---

# 2026-04-16 Test, Validation, and Quality Audit

## Purpose
Measure what can actually be validated today and identify quality-gate gaps.

## Scope
- Python tests
- TypeScript tests/build/typecheck
- Rust tests and strict static gates
- Probe-script safety

## What Was Inspected
- `scripts/tests/**`
- `spatial-daemon/package.json`
- `scripts/vitruvius/engine_rs/**`
- `scripts/vitruvius/datalog_rs/**`
- `scripts/test_odl_one.py`
- `scripts/test_pdf_text_detection.py`

## What Was Tested
- `pytest scripts/tests -q`
- `npm test`
- `npm run typecheck`
- `npm run build`
- `cargo test --quiet` in both Rust roots
- `cargo fmt --all --check` in both Rust roots
- `cargo clippy --workspace --all-targets -- -D warnings` in both Rust roots

## What Works
- Python: `1566 passed, 1 skipped`
- TypeScript: `21/21` tests passed; typecheck and build passed
- Rust runtime tests passed in both Rust roots
- Feature-flag coverage tests are present and green

## What Fails
- Rust strict formatting gate fails in both Rust roots
- Rust `clippy -D warnings` fails in both Rust roots
- No authoritative repo-level Python lint/type gate was found
- `scripts/test_odl_one.py` is not a safe validation helper

## What Is Misleading
- Older audit/state claims of Python instability are stale on the current checkout.
- Green runtime tests can hide red static hygiene in Rust.

## Severity-Ranked Findings
- `MEDIUM` Rust static hygiene is red. `clippy` fails on `needless_range_loop`, `too_many_arguments`, `approx_constant`, `len_zero`, and `useless_conversion`; `fmt --check` also fails in both Rust roots.
- `MEDIUM` There is no clear repo-level Python lint/type gate to run in PASS 1. The current quality story is dominated by tests, not by static analysis.
- `LOW` Validation helper ergonomics are inconsistent. `scripts/test_pdf_text_detection.py` is safe and argparse-backed; `scripts/test_odl_one.py` is a hard-coded execution script.

## Reproduction Steps
1. Run `pytest scripts/tests -q`.
2. Run `npm test && npm run typecheck && npm run build` under `spatial-daemon/`.
3. Run `cargo fmt --all --check` and `cargo clippy --workspace --all-targets -- -D warnings` under both Rust roots.
4. Inspect `scripts/test_odl_one.py`.

## Suspected Root Causes
- Rust runtime correctness was prioritized over style/static cleanup.
- Python quality gates grew organically around tests rather than a formal lint/type pipeline.
- Legacy helper scripts predate stricter operator hygiene expectations.

## Recommended Fix Direction
- Make Rust static gates green before adding more Rust surface area.
- Decide on a real Python static gate or explicitly document that tests are the only authoritative Python quality gate.
- Harden or quarantine helper scripts that perform real writes.

## Validation Needed After Fix
- Re-run all current commands.
- Add PASS 2 proof that Rust runtime tests still pass after hygiene fixes.
- If a Python lint/type gate is introduced, include it in the standard validation ladder.

## Audit Verdict
Runtime validation is stronger than the stale docs claim, but the quality-gate story is incomplete and uneven across languages.
