# AEC Relationship Run Directory Persistence Validation

**Date:** 2026-05-02
**Scope:** pending-only `aec-improve-relationships` run directory bootstrap, fatal handling, resume guard, watcher missing-run output, and CLI wiring.

## Changes Validated

- Run directories are created before startup output, DeepSeek preflight, embeddings, and model calls.
- New runs write `run-started.json`, a `starting` checkpoint, and a `run_started` event before work begins.
- Checkpoint/report/run-started/fatal-error JSON writes use atomic temp-file replacement.
- JSONL append helpers flush and fsync records.
- Unhandled fatal run errors write `fatal-error.json`, append `errors.jsonl` and events, and mark checkpoint status `error`.
- KeyboardInterrupt handling preserves checkpoint status `interrupted`.
- Missing explicit resume directories fail without creating a replacement run folder.
- Watcher prints a missing-run message plus latest available runs instead of crashing.
- `pipeline_cli.py` catches `RunFatalError` as a non-zero run failure after artifacts are written.

## Validation Commands

```bash
PYTHONPATH=scripts python -m pytest scripts/tests/test_kg_aec_relationship_improvement.py -q
# 104 passed

PYTHONPATH=scripts python -m pytest scripts/tests/test_kg_backbone_shadow_staging.py scripts/tests/test_kg_backbone_graph_quality.py -q
# 18 passed

python -m py_compile scripts/vitruvius/kg/aec_relationship_improvement.py scripts/pipeline_cli.py
# passed
```

Manual no-model smoke:

```bash
PYTHONPATH=scripts python scripts/pipeline_cli.py aec-improve-relationships \
  --dry-run \
  --run-id debug_run_dir_20260502T023835Z \
  --council-mode deepseek_local \
  --max-nodes 0 \
  --max-pairs 0 \
  --progress-mode plain
```

Observed:

- `RUN DIR EXISTS`
- `run-started.json` present
- `relationship-improvement-checkpoint.json` present with completed status after the smoke
- `relationship-improvement-events.jsonl` present
- `relationship-improvement.log` present
- watcher attached successfully with `aec-watch-relationship-run --watch-latest --progress-mode plain --exit-when-complete`

## Code Intelligence

- Pre-edit `refresh_code_intelligence.sh` completed; code-review-graph reported missing `tree-sitter-yaml` warnings for YAML parsing.
- Post-edit `refresh_code_intelligence.sh` completed; same YAML parser warnings remained.
- `gitnexus impact` for `run_relationship_improvement`, `watch_relationship_run`, and `build_parser` reported LOW upstream risk before edits.
- Post-edit `gitnexus detect-changes` reported critical risk because the core run workflow changed; scope was expected and covered by focused workflow and graph regression tests.

## Safety Confirmation

- No active graph file mutation was introduced.
- No Neo4j/Postgres writes were introduced.
- `--apply` remains rejected.
- Fatal/error artifacts are sanitized for API keys, bearer tokens, and `reasoning_content`.
