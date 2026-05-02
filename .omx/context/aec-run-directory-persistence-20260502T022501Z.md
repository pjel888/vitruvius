# AEC Run Directory Persistence Fix Context

## Task Statement
Fix the pending-only AEC relationship-improvement workflow so the announced run directory is durably created before any preflight, embeddings, model calls, or long-running work.

## Desired Outcome
Once the CLI prints a run id and output path, that directory already exists and contains startup artifacts: `run-started.json`, `relationship-improvement-checkpoint.json`, `relationship-improvement-events.jsonl`, and a log/fatal artifact path.

## Known Facts
- Target module: `scripts/vitruvius/kg/aec_relationship_improvement.py`.
- CLI: `scripts/pipeline_cli.py`.
- Tests: `scripts/tests/test_kg_aec_relationship_improvement.py`.
- Prior startup printed the output directory before the operator could later find the run folder.
- Workflow is Stage 1 Discovery only and must remain pending-only.
- Production Neo4j/Postgres writes and active graph mutation are prohibited.

## Constraints
- Do not modify the active AEC fixture.
- Do not weaken `--apply` rejection.
- Do not leak API keys, bearer tokens, or `reasoning_content`.
- Do not use web lookup or model tools.
- Do not delete the final run directory on failures or interrupts.

## Unknowns / Open Questions
- Whether the missing directory was caused by early startup failure, downstream cleanup, or an external deletion path is not yet known.
- Need inspect for cleanup paths such as `rmtree` and for resume behavior on missing directories.

## Likely Touchpoints
- Run bootstrap and `_touch_output_files`.
- Checkpoint/report JSON write helpers.
- `run_relationship_improvement` exception handling.
- Watcher run directory resolution.
- CLI parser flag wiring tests.
