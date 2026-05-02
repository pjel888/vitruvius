# AEC Relationship Workflow Windows Atomic Checkpoint Validation

Date: 2026-05-02

## Scope

Fixed the Windows checkpoint persistence failure in the pending-only AEC relationship-improvement workflow.

The change is limited to:

- robust JSON atomic writes
- checkpoint fallback persistence
- fallback checkpoint resume loading
- JSONL fsync tolerance
- CLI wiring for atomic write and JSONL fsync controls
- regression tests for the above

The workflow remains pending-only. No active graph file, Neo4j, or Postgres mutation was added.

## Root Cause

The checkpoint writer used a fixed sibling temp name:

`relationship-improvement-checkpoint.json.tmp`

and then performed a single `os.replace` into `relationship-improvement-checkpoint.json`. On Windows, that fixed temp path or the target checkpoint can be briefly locked by Python, antivirus/indexing, Explorer, Git Bash, or a watcher process. A transient sharing violation therefore aborted an otherwise healthy long run.

## Implementation Evidence

- `write_json_atomic` now uses unique temp files containing process id, thread id, and `time.monotonic_ns()`.
- `write_json_atomic` retries `os.replace` on `PermissionError` with bounded exponential backoff.
- `save_checkpoint` writes a fallback checkpoint under `checkpoint-fallbacks/` if the main checkpoint replace still fails after retries.
- Resume loading prefers the main checkpoint, but can load the newest valid fallback checkpoint when the main checkpoint is missing, invalid, or stale.
- JSONL append fsync remains enabled by default but logs and continues if `fsync` itself fails.
- CLI flags were added:
  - `--atomic-write-retries`
  - `--atomic-write-backoff-seconds`
  - `--atomic-write-max-backoff-seconds`
  - `--jsonl-fsync` / `--no-jsonl-fsync`

## Validation Commands

```bash
PYTHONPATH=scripts python -m pytest scripts/tests/test_kg_aec_relationship_improvement.py -q
```

Result: `118 passed in 4.40s`

```bash
PYTHONPATH=scripts python -m pytest scripts/tests/test_kg_backbone_shadow_staging.py scripts/tests/test_kg_backbone_graph_quality.py -q
```

Result: `18 passed in 0.27s`

```bash
python -m py_compile scripts/vitruvius/kg/aec_relationship_improvement.py scripts/pipeline_cli.py
```

Result: passed.

```bash
PYTHONPATH=scripts python scripts/pipeline_cli.py aec-improve-relationships --dry-run --run-id checkpoint_windows_smoke_20260502T081450Z --council-mode deepseek_local --max-nodes 0 --max-pairs 0 --progress-mode plain
```

Result: exit 0. The run directory exists and contains `run-started.json`, `relationship-improvement-checkpoint.json`, `relationship-improvement-events.jsonl`, `relationship-improvement-report.json`, `relationship-improvement-summary.txt`, review TSVs, JSONL artifacts, and the log.

```bash
bash ./scripts/refresh_code_intelligence.sh
```

Result: exit 0. The refresh still reports known YAML parser warnings for missing `tree-sitter-yaml` and existing embedding/indexing warnings from code-review-graph.

```bash
bash -lc "npx --yes gitnexus@1.6.4-rc.32 detect-changes --repo vitruvius"
```

Result: exit 0, reported critical risk across the broad dirty worktree. The affected relationship workflow/write paths were expected and covered by the focused regression tests.

```bash
uvx --with tree-sitter-yaml code-review-graph detect-changes --repo . --brief
```

Result: analyzed 30 changed files, 0 changed functions/classes, 0 affected flows, 0 test gaps, risk score 0.00.

```bash
git diff --check -- scripts/vitruvius/kg/aec_relationship_improvement.py scripts/pipeline_cli.py scripts/tests/test_kg_aec_relationship_improvement.py
```

Result: no whitespace errors; Git reported existing LF/CRLF normalization warnings.

## Safety Confirmation

- `--apply` remains rejected by the existing safety guard.
- Outputs remain review artifacts only.
- No active graph file mutation was added.
- No Neo4j or Postgres write path was added.
- Kimi and DeepSeek routing were not changed by this fix.
- Campaign ledger behavior remains unchanged except that JSONL fsync failures are now warning-only after flush.
