---
task: kg-first-cleanup
phase: execution-checklist
created: 2026-04-29
author: CODEX
status: PHASE_2_PLUS_FINAL_VALIDATION
---

# KG-First Cleanup Execution Checklist

## Global Gates Before Any Cleanup Slice

- [x] Confirm branch and working tree: `git status --short --branch`.
- [x] Confirm current phase and milestone docs remain consistent.
- [x] Confirm GitNexus index freshness (`./scripts/gitnexus_analyze.sh` if stale) before relying on impact results.
- [x] Confirm the slice is docs-only, tests-first, or has exact GitNexus symbol
      impact evidence.
- [x] Confirm no `001_Raw-Source-Layer/**` writes.
- [x] Confirm no numbered layer directory rename.
- [x] Confirm no KG rebuild/reload/reset.
- [x] Confirm no Neo4j mutation.
- [x] Confirm no protected payload ingest/exposure.
- [x] Confirm no API/Explorer behavior change unless explicitly in scope.

## Phase 1 Docs-Only Slice Checklist

- [ ] Update only live docs and operator wording.
- [ ] Preserve raw-source immutability language.
- [ ] Reframe old pipeline as source custody/extraction/evidence prep.
- [ ] Keep AEC-MEPFS current status truthful.
- [x] Run `git diff --check`.
- [ ] Run reference scan for old-primary-language contradictions.
- [ ] Write/update validation log.
- [ ] Commit with Lore trailers.

## Phase 2 CLI Wording Slice Checklist

- [x] Run GitNexus impact for exact edited function(s).
- [x] Add/adjust CLI help tests first.
- [x] Preserve old commands/aliases.
- [x] Run targeted CLI tests.
- [x] Run `git diff --check`.
- [x] Update validation evidence.

## Phase 3 Adapter Cleanup Checklist

- [x] Identify adapter clarification as docstring/comment-only across source-evidence boundaries.
- [x] Reuse existing characterization tests; no behavior change added.
- [x] Keep path outputs byte-compatible.
- [x] Run source identity, conversion/refine, dataset source-to-graph, and
      evidence ingestor tests.
- [x] Run GitNexus impact after changes; GitNexus CLI has no detect-changes command in the installed surface, so diff scope was verified with `git diff --name-only`.

## Phase 4 Archive/Index Checklist

- [x] Move no historical docs; update live status/index text only.
- [x] Update indexes/status docs in place.
- [x] Do not move validation logs required by current state.
- [x] Run reference scans.

## Phase 5 Delete-Later Checklist

- [ ] Deletion candidate has no callers in GitNexus.
- [ ] Deletion candidate has no current references in docs/tests/config.
- [ ] Replacement path is documented.
- [ ] Tests prove no behavior loss.
- [ ] Rollback is `git revert`.
