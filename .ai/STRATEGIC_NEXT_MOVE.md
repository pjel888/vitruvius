# Strategic Next Move

**Updated:** 2026-04-29

## Single Best Next Move

**Close the KG-first cleanup Phase 2/3/4 reconciliation slice.** Phase 1 live-doc reconciliation is complete; finish the behavior-preserving operator wording, adapter docstring, and active-plan status cleanup so future work routes to KG-first/AEC-MEPFS without deleting or destabilizing source custody/evidence infrastructure.

## Why This Is Right Now

- The AEC-MEPFS authored backbone and local file-backed runtime/default Explorer surfaces exist, while production Neo4j and protected-payload gates remain blocked.
- Phase 1 removed the main live-doc contradiction; Phase 2/3/4 now needs final verification so CLI help and source-adapter comments match the same KG-first/source-evidence story.
- Cleanup must remain language/operator-surface truth, not deletion, graph rebuilds, Explorer changes, API/runtime edits, or source-content admission.

## Concrete Tasks

1. Verify the CLI help wording slice that reframes source-derived commands as compatibility/evidence paths while preserving all commands, aliases, output paths, and behavior.
2. Verify adapter docstrings/comments only, preserving numbered layer directories and old pipeline modules as custody/staging/evidence/compatibility/provenance infrastructure.
3. Reconcile active plan/status docs from Phase 1 wording to Phase 2/3/4 completion wording.
4. Record validation evidence under `/.ai/03_plans/kg-first-cleanup/`.

## Do Not Do In This Cleanup Slice

- Do not edit raw source files or rename numbered layer directories.
- Do not delete generated artifacts, validation logs, provenance records, source-rights records, or historical audit evidence.
- Do not run KG rebuild/reload/reset or mutate Neo4j.
- Do not ingest or expose protected payloads.
- Do not change API or Explorer behavior.
- Do not delete legacy pipeline code.

## Next Boundary

After Phase 2/3/4 validates and is committed, stop cleanup implementation. Any deletion/refactor or source-overlay work requires a new dedicated packet with GitNexus no-caller proof, tests, and rollback evidence.
