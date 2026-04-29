---
task: kg-first-cleanup
phase: execution-checklist
created: 2026-04-29
author: CODEX
status: READY_FOR_FIRST_DOCS_ONLY_SLICE
---

# KG-First Cleanup Execution Checklist

## Global Gates Before Any Cleanup Slice

- [ ] Confirm branch and working tree: `git status --short --branch`.
- [ ] Confirm current phase and milestone docs remain consistent.
- [ ] Confirm the slice is docs-only, tests-first, or has exact GitNexus symbol
      impact evidence.
- [ ] Confirm no `001_Raw-Source-Layer/**` writes.
- [ ] Confirm no numbered layer directory rename.
- [ ] Confirm no KG rebuild/reload/reset.
- [ ] Confirm no Neo4j mutation.
- [ ] Confirm no protected payload ingest/exposure.
- [ ] Confirm no API/Explorer behavior change unless explicitly in scope.

## Phase 1 Docs-Only Slice Checklist

- [ ] Update only live docs and operator wording.
- [ ] Preserve raw-source immutability language.
- [ ] Reframe old pipeline as source custody/extraction/evidence prep.
- [ ] Keep AEC-MEPFS current status truthful.
- [ ] Run `git diff --check`.
- [ ] Run reference scan for old-primary-language contradictions.
- [ ] Write/update validation log.
- [ ] Commit with Lore trailers.

## Phase 2 CLI Wording Slice Checklist

- [ ] Run GitNexus impact for exact edited function(s).
- [ ] Add/adjust CLI help tests first.
- [ ] Preserve old commands/aliases.
- [ ] Run targeted CLI tests.
- [ ] Run `git diff --check`.
- [ ] Update validation evidence.

## Phase 3 Adapter Cleanup Checklist

- [ ] Identify one adapter boundary only.
- [ ] Add characterization tests.
- [ ] Keep path outputs byte-compatible.
- [ ] Run source identity, conversion/refine, dataset source-to-graph, and
      evidence ingestor tests.
- [ ] Run GitNexus detect/impact after changes.

## Phase 4 Archive/Index Checklist

- [ ] Move only historical docs that are not live authority.
- [ ] Leave forwarding pointers or update indexes.
- [ ] Do not move validation logs required by current state.
- [ ] Run reference scans.

## Phase 5 Delete-Later Checklist

- [ ] Deletion candidate has no callers in GitNexus.
- [ ] Deletion candidate has no current references in docs/tests/config.
- [ ] Replacement path is documented.
- [ ] Tests prove no behavior loss.
- [ ] Rollback is `git revert`.
