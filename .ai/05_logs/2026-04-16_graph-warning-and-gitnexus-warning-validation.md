---
task: graph-warning-and-gitnexus-warning
phase: "09"
created: 2026-04-16
author: REVIEWER
supersedes: null
status: DRAFT
---

# Graph Warning and GitNexus Warning Validation — 2026-04-16

## Validation scope
Validate two sequential fixes:
1. eliminate the current `build-graph` orphan warnings using truthful graph semantics
2. remove the local GitNexus `MaxListenersExceededWarning` from the recommended analyze path

## Part 1 — `build-graph` warnings
### Fresh evidence
```bash
PYTHONPATH=scripts python3 -m pytest -q \
  scripts/tests/test_graph_builder.py \
  scripts/tests/test_graph_integrity.py \
  scripts/tests/test_query_engine.py \
  scripts/tests/test_query_cli.py \
  scripts/tests/test_query_aggregate_confidence.py \
  scripts/tests/test_query_seed_accuracy.py
PYTHONPATH=scripts python3 scripts/pipeline_cli.py build-graph
```

### Results
- graph/query pytest slice: `61 passed`
- `build-graph`: `passed: true`, `warning_count: 0`, `error_count: 0`

### Interpretation
The operational graph now models existing provenance more faithfully:
- source frontmatter relationships become edges
- enriched concept `regulatory_basis` becomes source-to-concept provenance edges
- truly ungrounded/unreferenced placeholder concepts are excluded from the operational graph snapshot

## Part 2 — GitNexus warning
### Repo-side mitigation introduced
- added `scripts/gitnexus_analyze.sh`
- wrapper pins `gitnexus@1.6.2-rc.10`
- wrapper auto-preserves embeddings when `.gitnexus/meta.json` reports `stats.embeddings > 0`
- updated the scoped authority and GitNexus skill docs to call the wrapper instead of raw `npx gitnexus analyze`

### Validation intent
A forced re-analyze through the wrapper must complete without emitting `MaxListenersExceededWarning`.

### Part 2 — forced wrapper verification
```bash
./scripts/gitnexus_analyze.sh --force 2>&1 | tee /tmp/gitnexus_rc10_force.log
rg -n 'MaxListenersExceededWarning' /tmp/gitnexus_rc10_force.log
```

#### Results
- forced pinned re-analyze completed successfully
- output: `Repository indexed successfully (7.6s)`
- `rg` check result: `warning-absent`

#### Interpretation
The warning-free path is now reproducible from within the repo by using the pinned wrapper instead of the older unpinned `npx gitnexus analyze` path.

## Overall verdict
**PASS**

- Part 1: repo-side graph warnings eliminated truthfully
- Part 2: repo-local GitNexus mitigation added and verified warning-free on a forced analyze


## Architect rejection follow-up — 2026-04-16
### Must-fix issue 1 — source filtering narrowed
- changed `build_snapshot()` so unreferenced sources are preserved by default
- only sources with unresolved frontmatter-only relationships and no live graph references are excluded
- added regression test: `test_build_snapshot_keeps_unreferenced_sources_without_broken_frontmatter_links`

### Must-fix issue 2 — wrapper docs made consistent
- updated stale GitNexus sections in `AGENTS.md` and `CLAUDE.md`
- all scoped authority and GitNexus skill guidance now points to `./scripts/gitnexus_analyze.sh`

### Fresh follow-up evidence
```bash
PYTHONPATH=scripts python3 -m pytest -q   scripts/tests/test_graph_builder.py   scripts/tests/test_graph_integrity.py   scripts/tests/test_query_engine.py   scripts/tests/test_query_cli.py   scripts/tests/test_query_aggregate_confidence.py   scripts/tests/test_query_seed_accuracy.py
PYTHONPATH=scripts python3 scripts/pipeline_cli.py build-graph --dry-run
./scripts/gitnexus_analyze.sh --force 2>&1 | tee /tmp/gitnexus_rc10_force.log
rg -n 'npx gitnexus analyze|MaxListenersExceededWarning' AGENTS.md CLAUDE.md .ai/00_system/EXECUTION_LOOP.md .ai/skills/gitnexus/gitnexus-cli/SKILL.md .ai/skills/gitnexus/gitnexus-guide/SKILL.md .ai/skills/gitnexus/gitnexus-exploring/SKILL.md .ai/skills/gitnexus/gitnexus-debugging/SKILL.md .ai/skills/gitnexus/gitnexus-impact-analysis/SKILL.md .ai/skills/gitnexus/gitnexus-refactoring/SKILL.md /tmp/gitnexus_rc10_force.log
```

#### Follow-up results
- targeted graph/query pytest slice: `62 passed`
- `build-graph --dry-run`: `passed: true`, `warning_count: 0`, `error_count: 0`
- pinned wrapper re-analyze: `Repository indexed successfully (7.7s)`
- stale-doc / warning grep result: no remaining raw `npx gitnexus analyze` references in the scoped authority/skill docs and no `MaxListenersExceededWarning` in the forced wrapper log
- `git diff --check` on the scoped files: PASS
- affected Python files: no diagnostics reported by the available local diagnostic tool

## Architect rejection follow-up
The first architect pass rejected the change because several repeated/generated GitNexus guidance blocks still referenced the old raw `npx gitnexus analyze` path.

### Follow-up fix
- replaced the remaining stale `npx gitnexus analyze` and `npx gitnexus analyze --embeddings` references in:
  - `AGENTS.md`
  - `CLAUDE.md`
  - `.ai/00_system/EXECUTION_LOOP.md`
  - `.ai/skills/gitnexus/*/SKILL.md`
- re-ran grep to confirm the stale command no longer appears in the reviewed authority/skill surfaces.

### Follow-up evidence
- stale-ref grep across reviewed docs: `stale-ref-absent`
- `build-graph --dry-run`: still `warning_count: 0`, `error_count: 0`
- `./scripts/gitnexus_analyze.sh --force`: still `warning-absent`

## Final stale-guidance correction
A literal grep across the reviewed authority/skill files now returns no raw `npx gitnexus analyze` references.

### Final evidence
- `rg -n 'npx gitnexus analyze|npx gitnexus analyze --embeddings' AGENTS.md CLAUDE.md .ai/skills/gitnexus/*/SKILL.md .ai/00_system/EXECUTION_LOOP.md` → no matches
- `build-graph --dry-run` remains clean
- `./scripts/gitnexus_analyze.sh --force` remains warning-free


## Durable wrapper note
The wrapper now calls GitNexus with `--skip-agents-md` so future re-index runs do not overwrite the repo's local AGENTS/CLAUDE guidance back to the noisy unpinned command.

## Durable wrapper verification
The wrapper now uses `--skip-agents-md`, and a forced re-analyze no longer reintroduces stale raw `npx gitnexus analyze` guidance into `AGENTS.md` or `CLAUDE.md`.

### Evidence
- forced wrapper re-analyze: warning-absent
- post-run stale-guidance grep across reviewed files: stale-ref-absent

## Final skill-surface correction
The `.ai/skills/gitnexus/*` skill files were the last stale pocket still mentioning the raw `npx gitnexus analyze` path. They now point to `./scripts/gitnexus_analyze.sh` as well.

### Final evidence refresh
- stale-guidance grep across AGENTS/CLAUDE/EXECUTION_LOOP/`.ai/skills/gitnexus/*`: stale-ref-absent
- cached forced-wrapper warning grep: warning-absent

## Ralph deslop follow-up — scoped durability fix
The deslop pass found one non-style issue that still threatened truthfulness: a forced wrapper re-analyze kept restoring stale raw `npx gitnexus analyze` guidance into `.ai/skills/gitnexus/*`.

### Deslop fix
- updated `scripts/gitnexus_analyze.sh` to back up and restore the repo-managed `.ai/skills/gitnexus/*.md` files around `gitnexus analyze`
- re-applied the scoped skill guidance so those skill files consistently point to `./scripts/gitnexus_analyze.sh`
- left the graph builder, tests, AGENTS, CLAUDE, and execution-loop behavior unchanged during the deslop pass because no safe simplifications were warranted there

### Deslop evidence
- forced wrapper re-analyze after the wrapper update: completed successfully
- post-run grep across AGENTS/CLAUDE/EXECUTION_LOOP/`.ai/skills/gitnexus/*`: no raw `npx gitnexus analyze` references
- post-run wrapper log grep: no `MaxListenersExceededWarning`
- targeted graph/query pytest slice: `62 passed`
- `build-graph --dry-run`: `warning_count: 0`, `error_count: 0`

## Deslop pass and post-deslop re-verification
### Deslop result
- attempted a bounded code-simplifier/deslop lane on the session-owned authored files
- no further simplifications were warranted beyond the implemented changes
- final cleanup decision: **no-op**

### Post-deslop verification
```bash
git diff --check -- [scoped files]
PYTHONPATH=scripts python3 -m pytest -q \
  scripts/tests/test_graph_builder.py \
  scripts/tests/test_graph_integrity.py \
  scripts/tests/test_query_engine.py \
  scripts/tests/test_query_cli.py \
  scripts/tests/test_query_aggregate_confidence.py \
  scripts/tests/test_query_seed_accuracy.py
PYTHONPATH=scripts python3 scripts/pipeline_cli.py build-graph --dry-run
./scripts/gitnexus_analyze.sh --force
PYTHONPATH=scripts python3 -m py_compile scripts/vitruvius/graph/builder.py scripts/tests/test_graph_builder.py
bash -n scripts/gitnexus_analyze.sh
```

### Post-deslop results
- `diff-check: PASS`
- targeted graph/query pytest slice: PASS
- `build-graph --dry-run`: PASS (`warning_count: 0`, `error_count: 0`)
- wrapper re-analyze: PASS (`warning-absent`)
- `py_compile: PASS`
- `bash -n: PASS`


## Durable wrapper verification (final)
After repatching the `.ai/skills/gitnexus/*` files to the wrapper path, a forced wrapper run preserved those skill files and did not reintroduce the raw unpinned command.

### Final durable evidence
- stale-guidance grep after forced wrapper run: stale-ref-absent
- wrapper log grep for `MaxListenersExceededWarning`: warning-absent

## Durable wrapper verification (final)
After fixing the wrapper's recursive skill backup/restore, a forced wrapper run now preserves the `.ai/skills/gitnexus/*` files as well.

### Final durable evidence
- stale-guidance grep after forced wrapper run: `stale-ref-absent`
- wrapper log grep for `MaxListenersExceededWarning`: `warning-absent`
- `bash -n scripts/gitnexus_analyze.sh`: PASS
- targeted graph/query pytest slice: PASS (`62 passed`)
