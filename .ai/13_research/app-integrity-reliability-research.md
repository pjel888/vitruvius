---
task: app-integrity-reliability
phase: 03
created: 2026-04-16
author: RESEARCHER
supersedes: null
status: ACCEPTED
---

# Research — App Integrity Reliability

## 1. Research Objective
Ground an integrity-first reliability pass on the current `main` branch so fixes and validation target actual runtime breakpoints rather than stale branch-era claims.

## 2. Execution Reality
- `current-phase.md` says the repo is between implementation sprints and active work is governance/planning maintenance, so this integrity pass is a fresh maintenance trigger rather than continuation of an active runtime sprint.
- `INDEX.md` shows no active plan already governing an app-integrity sweep.
- `known_issues.md` still carries RI-004 (`Python Environment / PYTHONPATH`) as a tolerated environment sharp edge, which makes command validation part of integrity work rather than an unrelated concern.

## 3. Intelligence Surface
- GitNexus local CLI is available and up to date on commit `027e457`.
- `code-review-graph` MCP tools are not exposed in this session, so graph-first discovery is limited to GitNexus CLI plus direct file inspection.
- `docs/shared/agent-tiers.md` is not present under the repo or local Codex home, so Ralph delegation must use explicit role choices without a local tier map.

## 4. Key Code and State Paths

### 4.1 Failing Test Surface
- `scripts/tests/test_livewiring_bench.py:1-21`
  - imports `run_livewiring_bench` at module load
  - explicitly expects the bench harness to be importable without side effects
- `scripts/tests/test_livewiring_bench.py:53-120`
  - asserts the returned summary shape and that `flag_on_config()` never mutates `config/vitruvius.yaml`

### 4.2 Bench Harness
- `scripts/vitruvius/bench/run_livewiring_bench.py:1-37`
  - module docstring claims informational behavior
  - hard-imports `psutil` at line 37
- `scripts/vitruvius/bench/run_livewiring_bench.py:142-185`
  - `_RssSampler` directly constructs `psutil.Process()` and catches `psutil.Error`
- `scripts/vitruvius/bench/run_livewiring_bench.py:227-288`
  - `run_livewiring_bench()` depends on `_RssSampler` but otherwise patches config and review behavior cleanly for tests

### 4.3 CLI Integrity Surface
- `scripts/pipeline_cli.py:1-8`
  - explicitly documents lazy-import guarantees for CLI usability in minimal environments
- `scripts/pipeline_cli.py:17-57`
  - defines `run_pipeline()` and `run_pipeline_with_review()`; the latter deliberately keeps LLM review opt-in
- `scripts/pipeline_cli.py:60-261`
  - exposes the current command surface through `build_parser()`

### 4.4 State Surfaces with Potential Drift
- `.ai/10_state/active_context.md:3-7`
  - claims a different branch and historical green test counts
- `.ai/10_state/active_context.md:31-34`
  - documents operator work requiring `psutil` + Pillow for the optional vision path
- `.ai/10_state/known_issues.md:32-36`
  - records the repo’s non-`src/` Python environment sharp edge
- `.ai/10_state/known_issues.md:99`
  - asserts new capability surfaces shipped behind false-by-default feature flags

## 5. Fresh Evidence Gathered
- `PYTHONPATH=scripts python3 -m pytest scripts/tests/ -q` fails with `ModuleNotFoundError: psutil` during collection of `test_livewiring_bench.py`
- `PYTHONPATH=scripts python3 scripts/pipeline_cli.py --help` works and enumerates the full CLI surface
- `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run --help` works, supporting the lazy-import contract for that help path
- `PYTHONPATH=scripts python3 scripts/pipeline_cli.py status` works and writes the expected latest status reports
- `config/vitruvius.yaml` currently has 115 feature flags, with only 4 set `true`

## 6. Research Implications
- The first runtime repair should be narrow: make the livewiring bench importable without forcing `psutil` into the global test dependency set.
- Validation cannot stop at the single test fix, because `active_context.md` currently overstates branch-local health for `main`.
- Command validation must distinguish:
  - safe help/preflight surfaces that should always work
  - heavier commands whose success depends on real corpus state or local services
- Any claim that “the app works” must be tied to fresh evidence on `main`, not historical branch summaries.

## 7. Research Conclusion
Vitruvius on `main` is close enough to healthy that a bounded integrity pass is appropriate, but it is not currently proven healthy. The repo has one concrete import-time regression, a live CLI surface that still responds, and at least one operator-facing state file whose health claims are stale for the active branch.
