---
task: app-integrity-reliability
phase: 04
created: 2026-04-16
author: AUDITOR
supersedes: null
status: ACCEPTED
---

# Audit — App Integrity Reliability

## 1. Summary
The current `main` branch is not yet safe to describe as fully healthy. The strongest evidence is a reproducible pytest collection failure caused by a hard `psutil` import in the livewiring bench module. The main CLI entrypoint still loads and exposes commands correctly, so the right response is a bounded integrity repair plus a broader validation pass, not a broad architectural rewrite.

## 2. Findings

### 2.1 Import-Time Optional Dependency Trap
Judgment: real defect.

Evidence:
- `scripts/tests/test_livewiring_bench.py:17` imports the bench harness at module load specifically to prove import safety
- `scripts/vitruvius/bench/run_livewiring_bench.py:37` hard-imports `psutil`
- `_RssSampler` at `scripts/vitruvius/bench/run_livewiring_bench.py:142-185` assumes `psutil` exists unconditionally
- full pytest baseline aborts with `ModuleNotFoundError: psutil`

Impact:
- breaks the test suite on environments that do not install bench-only extras
- weakens the CLI’s documented “minimal environment” contract by making a non-core optional dependency mandatory for module import

Required fix:
- make RSS sampling degrade gracefully when `psutil` is absent, without violating the summary contract tested in `test_livewiring_bench.py`

### 2.2 Operator-Facing Health Claims Are Stale for `main`
Judgment: truthfulness defect.

Evidence:
- `.ai/10_state/active_context.md:4-7` still claims branch `feat/sprint-r-per-layer-embeddings` and historical green counts
- fresh baseline is on `main` and currently fails pytest

Impact:
- a future operator could wrongly conclude the active branch is already validated

Required fix:
- do not trust `active_context.md` as the live runtime health source until post-fix validation is complete
- reconcile or annotate stale claims after fresh validation evidence exists

### 2.3 Core CLI Surface Is Alive but Not Yet Fully Proven
Judgment: partial positive signal, not completion evidence.

Evidence:
- `pipeline_cli.py --help` succeeds
- `pipeline_cli.py run --help` succeeds
- `pipeline_cli.py status` succeeds and writes expected run artifacts

Impact:
- the CLI spine is intact enough to continue
- “all commands work” is not yet proven because only a first validation ladder has been run

Required fix:
- expand command validation after the first test blocker is removed

## 3. Audit Decision
Proceed with a bounded integrity initiative:
1. fix the import-time optional dependency regression
2. rerun targeted then full pytest
3. expand CLI validation on the most operator-critical command surfaces
4. reconcile stale health claims only after fresh evidence exists

## 4. Final Judgment
This is an execution-worthy maintenance task with low-to-moderate implementation risk and high truthfulness value. Proceed.
