---
task: vitruvius-audit-pass-1
phase: 04
created: 2026-04-16
author: AUDITOR
supersedes: null
status: ACCEPTED
---

# 2026-04-16 Frontend Behavior Audit

## Purpose
Determine whether Vitruvius has a real frontend/UI surface that needs behavioural auditing.

## Scope
- Top-level repo shape
- `README.md`
- `scripts/pipeline_cli.py`
- `spatial-daemon/`

## What Was Inspected
- Top-level directories
- `README.md`
- `spatial-daemon/README.md`
- `spatial-daemon/src/cli.ts`
- `scripts/pipeline_cli.py --help`

## What Was Tested
- `python3 scripts/pipeline_cli.py --help`
- `npm test`
- `npm run typecheck`
- `npm run build`

## What Works
- The repo’s user-facing runtime surfaces are headless CLIs.
- `spatial-daemon/` behaves as an isolated sibling CLI and validates cleanly.

## What Fails
- No frontend exists to test for loading, navigation, form, or rendering behaviour.

## What Is Misleading
- README and research material mention browser/WebAssembly/React Three Fiber and a Ranger dashboard as future or gated directions.
- Those references do not correspond to an implemented UI surface in this checkout.

## Severity-Ranked Findings
- `INFO` Frontend/UI audit is largely not applicable. No `web/`, `app/`, `frontend/`, dashboard, HTTP server, or route-rendering tree exists.
- `LOW` Documentation can mislead cold readers into expecting a browser-facing surface because of future-facing language around React Three Fiber and the Ranger dashboard.

## Reproduction Steps
1. Inspect repo top level.
2. Read `spatial-daemon/README.md:8-12`.
3. Read `spatial-daemon/src/cli.ts:81-91`.
4. Run `python3 scripts/pipeline_cli.py --help`.

## Suspected Root Causes
- Future-facing AEC/browser vision is documented alongside current runtime surfaces without a clear “not implemented here” boundary.

## Recommended Fix Direction
- Keep frontend/admin/browser claims explicitly labelled as future or externally gated.
- Keep PASS 2 stabilization scoped to CLI/operator paths, not invented UI work.

## Validation Needed After Fix
- None for a non-existent frontend.
- If a frontend is later added, create a separate audit pack for it.

## Audit Verdict
Frontend/UI is `N/A` for PASS 1. The real runtime surface is CLI-only.
