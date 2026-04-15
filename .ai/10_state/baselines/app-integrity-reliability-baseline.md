---
task: app-integrity-reliability
phase: 02
created: 2026-04-16
author: STEWARD
supersedes: null
status: ACCEPTED
---

# Baseline — App Integrity Reliability

## 1. Repo Baseline
- Commit SHA: `027e45711db18990f40d4c9222677711ea058c63`
- Branch: `main`
- GitNexus status: up to date on the current commit
- Worktree note: repo already contains unrelated dirty `.ai/` and generated run artifacts; they are not part of this integrity trigger unless touched by validation evidence

## 2. Python Test Baseline
Command:

```bash
PYTHONPATH=scripts python3 -m pytest scripts/tests/ -q
```

Observed result:
- collection interrupted with `1 error`, `13 skipped`, exit code `2`
- failing import path:
  - `scripts/tests/test_livewiring_bench.py:17`
  - `scripts/vitruvius/bench/run_livewiring_bench.py:37`
- exception: `ModuleNotFoundError: No module named 'psutil'`
- runtime: `20.79s`

## 3. CLI Baseline
Command:

```bash
PYTHONPATH=scripts python3 scripts/pipeline_cli.py --help
```

Observed result:
- CLI imports successfully
- command surface is present and includes the expected operator-facing entrypoints such as `scan`, `status`, `lint`, `convert`, `run`, `run-with-review`, `review-relationships-ollama`, `promote`, `build-graph`, `query`, and `query-structured`

Command:

```bash
PYTHONPATH=scripts python3 scripts/pipeline_cli.py run --help
```

Observed result:
- help path works without heavy-import failure

Command:

```bash
PYTHONPATH=scripts python3 scripts/pipeline_cli.py status
```

Observed result:
- command runs successfully
- summary: `New files: 0`, `Changed files: 0`, `Missing files: 5`, `Unchanged files: 424`
- side effect: rewrites `006_System-Manifests/runs/latest_status_report.json` and `.txt`, plus timestamped report snapshots, as part of normal command behavior

## 4. Feature Flag Baseline
Config snapshot from `config/vitruvius.yaml`:
- total `features.*` flags: `115`
- flags currently `true`:
  - `hp_rocksdb_event_store`
  - `hp_rocksdb_verdict_cache`
  - `rust_mig_spatial_kernels`
  - `rust_mig_stats_kernels`
- flags currently `false`: `111`

## 5. State Truthfulness Baseline
- `current-phase.md` correctly says the repo is between implementation sprints
- `active_context.md` is not a trustworthy live baseline for `main`; it still claims branch `feat/sprint-r-per-layer-embeddings` and historical green test counts

## 6. Baseline Conclusion
The current `main` branch is not integrity-clean yet. The main reproducible blocker is a test-collection failure caused by an optional dependency being imported as a hard requirement in the livewiring bench module. The CLI entry surface is otherwise alive enough to continue with a bounded repair-and-validate pass.
