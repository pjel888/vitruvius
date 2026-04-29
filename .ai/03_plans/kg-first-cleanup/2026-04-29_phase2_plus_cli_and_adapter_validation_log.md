---
task: kg-first-cleanup
phase: phase2-plus-cli-adapter-plan-surface-reconciliation
created: 2026-04-29
author: CODEX
status: VALIDATED
---

# KG-First Cleanup Phase 2/3/4 Validation Log

## Scope

Phase 2/3/4 continues the KG-first cleanup after the Phase 1 live-doc
reconciliation commit `8fce5807`. This slice is behavior-preserving:

- Phase 2: CLI/operator help wording only.
- Phase 3: source-evidence adapter docstrings/comments only.
- Phase 4: active plan/status/index reconciliation only.
- Phase 5 deletion: explicitly skipped.

## Start State

- Branch: `main`
- Start commit: `8fce5807`
- Initial working tree: clean relative to `origin/main` before this slice.
- Team/runtime note: OMX team `read-only-kg-first-cleanup-pha` was launched with Claude workers, but worker panes stalled with no start evidence. The leader marked both advisory tasks failed, shut the team down with `--confirm-issues`, and continued locally. Worker reports contained no diffs.
- Kimi/Spark: Spark was not used. Kimi CLI was attempted for advisory review; both Phase 2+ advisory prompts timed out after 45 seconds without usable findings, so local verification was strengthened.

## Files Changed

- `.ai/ACTIVE_WORK.md`
- `.ai/STRATEGIC_NEXT_MOVE.md`
- `.ai/01_roadmap/current-phase.md`
- `.ai/01_roadmap/milestone-tracker.md`
- `.ai/03_plans/INDEX.md`
- `.ai/03_plans/kg-first-cleanup/2026-04-29_execution_checklist.md`
- `.ai/03_plans/kg-first-cleanup/2026-04-29_phase2_plus_cli_and_adapter_validation_log.md`
- `scripts/tests/test_cli_operator_experience.py`
- `scripts/vitruvius/cli_experience.py`
- `scripts/vitruvius/conversion.py`
- `scripts/vitruvius/normalization/refine.py`
- `scripts/vitruvius/canonicalize.py`
- `scripts/vitruvius/source_identity.py`
- `scripts/vitruvius/dataset_pipeline.py`
- `scripts/vitruvius/kg/evidence_ingestor.py`

No API, Explorer, raw source, Neo4j, KG runtime, generated artifact, or numbered
layer directory files were changed.

## Implementation Summary

### Phase 2 — CLI/operator wording

- Added CLI help regression tests for:
  - `run-with-review`
  - `run-kg-pipeline`
  - `canonicalize-one`
- Reframed root CLI and selected command docs as source custody, extraction
  staging, source-evidence compatibility, and KG snapshot compatibility support.
- Preserved command names, aliases, arguments, output paths, and runtime behavior.
- Added a `run-kg-pipeline` command doc entry so help text warns that the command
  is not KG-first cleanup, Explorer cutover, or production graph promotion.

### Phase 3 — adapter clarification

- Added or revised module docstrings only for source/evidence adapter modules:
  - conversion staging
  - refinement staging
  - canonical source-evidence support
  - source identity
  - dataset source-to-graph compatibility
  - guarded evidence ingestion
- No function bodies, path logic, IDs, output formats, API behavior, Explorer
  behavior, KG reset/rebuild behavior, or Neo4j behavior were changed.

### Phase 4 — active plan/index cleanup

- Reconciled active work, strategic next move, current phase, milestone tracker,
  plan index, and execution checklist from stale Phase 1-only status to Phase
  2/3/4 final validation status.
- Preserved hard blocks against deletion, production mutation, raw-source writes,
  protected payload admission, and API/Explorer behavior changes.

### Phase 5 — deletion

- Skipped. The cleanup plan's deletion proof gates are not satisfied, and the
  legacy source/evidence modules remain compatibility/provenance infrastructure.

## GitNexus / Impact Evidence

- `npx --yes gitnexus@1.6.2-rc.10 status`
  - Indexed commit: `8fce580`
  - Current commit: `8fce580`
  - Result: up to date.
- `npx --yes gitnexus@1.6.2-rc.10 impact -r vitruvius --depth 2 COMMAND_DOCS`
  - Target: `scripts/vitruvius/cli_experience.py:COMMAND_DOCS`
  - Impacted count: `0`
  - Risk: `LOW`
  - Direct/process/module affected counts: `0/0/0`
- Installed GitNexus CLI help exposes `status`, `query`, `context`, and `impact`,
  but not a `detect_changes` command; final changed-file scope was checked with
  `git diff --name-only` and `git diff --check`.

## Verification Commands and Results

- `PYTHONPATH=scripts python3 -m pytest scripts/tests/test_cli_operator_experience.py -q`
  - Result: `6 passed in 0.63s`
- `PYTHONPATH=scripts python3 -m pytest scripts/tests/test_dataset_pipeline_cli.py scripts/tests/test_kg_pipeline_force_path.py scripts/tests/test_cli_operator_experience.py -q`
  - Result: `107 passed in 49.16s`
- `PYTHONPATH=scripts python3 -m py_compile scripts/vitruvius/conversion.py scripts/vitruvius/normalization/refine.py scripts/vitruvius/canonicalize.py scripts/vitruvius/source_identity.py scripts/vitruvius/dataset_pipeline.py scripts/vitruvius/kg/evidence_ingestor.py`
  - Result: passed.
- `PYTHONPATH=scripts python3 -m pytest scripts/tests/test_conversion_fallback.py scripts/tests/test_refine.py scripts/tests/test_source_identity.py scripts/tests/test_dataset_source_to_graph_pipeline.py scripts/tests/test_evidence_ingestor.py -q`
  - Result: `20 passed, 1 skipped in 0.53s`
- CLI help smoke checks:
  - `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-with-review --help`
  - `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-kg-pipeline --help`
  - `PYTHONPATH=scripts python3 scripts/pipeline_cli.py canonicalize-one --help`
  - Result: help text prints the new KG-first/source-evidence framing and keeps existing options.
- `git diff --check`
  - Result: passed after line-ending-safe conversion docstring insertion.
- Reference scan:
  - `rg -n "raw -> conversion -> canonical|raw → conversion → canonical|six-layer|six layer|layer-first|sole canonical|primary product architecture|primary future product" README.md AGENTS.md scripts/AGENTS.md .ai/README.md .ai/ACTIVE_WORK.md .ai/STRATEGIC_NEXT_MOVE.md .ai/01_roadmap .ai/03_plans/INDEX.md || true`
  - Result: no matches.

## Kimi Advisory Status

Kimi CLI path: `/Users/philiplewis/.local/bin/kimi`.

Attempts:

- Documentation auditor prompt: timed out after 45 seconds without usable output.
- Verification critic prompt: timed out after 45 seconds without usable output.

Kimi output was not used as authority. Spark/Codex-Spark was not used.

## Safety Invariants Confirmed

- No `001_Raw-Source-Layer/**` writes.
- No numbered layer directory renames.
- No generated artifact deletion.
- No validation log, manifest, provenance, source-rights, currentness, or
  admission record deletion.
- No KG rebuild/reload/reset.
- No Neo4j mutation.
- No protected payload ingest/exposure.
- No API runtime behavior change.
- No Explorer behavior change.
- No tests removed.
- No legacy pipeline module deletion.

## Residual Risks / Next Boundary

- This slice intentionally does not delete or refactor legacy pipeline modules.
- Future deletion/refactor work requires exact no-caller proof, reference cleanup,
  replacement documentation, regression tests, and clean rollback.
- Future source-overlay/content admission work requires a dedicated packet and
  protected-content/source-rights gates.

## End State

- Status: validated.
- Final commit: this committed validation slice.
- Final git status: clean/synced after commit and push verification.
