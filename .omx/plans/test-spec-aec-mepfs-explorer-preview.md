---
task: aec-mepfs-explorer-preview
phase: test-spec
created: 2026-04-25
author: TESTER
status: ACCEPTED
---

# Test Spec: AEC-MEPFS Explorer Preview

## Proof Targets

1. Existing Explorer graph behavior remains the default.
2. The new preview uses `/v2/backbone` rather than graph or Neo4j endpoints.
3. The preview has deterministic UI states for loading, success, and failure.
4. The TypeScript surface remains type-safe.
5. The API `/v2/backbone` contract remains green after frontend integration.

## Focused Verification

- Run Explorer tests after implementation.
- Run Explorer typecheck/build according to available package scripts.
- Run API `/v2/backbone` route tests to prove the upstream route still passes.
- Run `git status --short` and GitNexus/code-impact checks before commit.

## Manual / Visual Check

- If the Explorer dev server can run locally, open the changed surface and verify that the preview is opt-in and does not replace the graph on first load.
- If a browser runner is unavailable, rely on component tests plus build/typecheck and record the limitation in the validation log.
