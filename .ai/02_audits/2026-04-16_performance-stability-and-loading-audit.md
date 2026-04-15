---
task: vitruvius-audit-pass-1
phase: 04
created: 2026-04-16
author: AUDITOR
supersedes: null
status: ACCEPTED
---

# 2026-04-16 Performance, Stability, and Loading Audit

## Purpose
Audit the stability profile of the live repo and identify load/path risks that matter before PASS 2.

## Scope
- GitNexus indexing path
- CLI/operator command side effects
- manifest drift
- graph snapshot health
- headless operator UX truthfulness

## What Was Inspected
- `npx gitnexus status`
- `npx gitnexus analyze`
- `pipeline_cli.py run` outputs
- `latest_status_report.txt`
- `latest_lint_report.txt`
- `latest_graph_snapshot.json`
- `latest_graph_integrity_report.json`

## What Was Tested
- GitNexus index refresh
- `pipeline_cli.py run`
- `pipeline_cli.py build-graph`
- `pipeline_cli.py export-graph-owl`

## What Works
- GitNexus can refresh the repo index successfully.
- `run` completes and writes all expected reports.
- Graph build and OWL export are fast and finish without runtime failure.
- TypeScript daemon commands finish quickly and cleanly.

## What Fails
- GitNexus analyze emits repeated `MaxListenersExceededWarning` warnings while indexing.
- Runtime stability depends on stateful manifest drift being understood; current raw layer comparison reports heavy new/missing-file churn.
- Graph snapshot integrity passes despite weak semantic quality and orphan nodes.

## What Is Misleading
- “Passed” integrity status is weaker than it looks because warnings do not fail the build and duplicate nodes are not checked.
- Headless operator commands such as `run` and `status` are mutating state/report surfaces by design; they are not read-only health probes.

## Severity-Ranked Findings
- `MEDIUM` Manifest stability is currently noisy. `run` reported `82` new files, `8` changed files, and `156` missing files; that is too much drift to treat manifests as quietly healthy without operator intent.
- `MEDIUM` GitNexus analyzer emitted repeated event-listener warnings during index refresh. It still succeeded, but the tooling path is not clean under current load.
- `MEDIUM` Graph integrity “pass” hides orphan-node and identity-quality issues.
- `LOW` Raw-layer lint still includes `.DS_Store`, non-PDF files, and duplicate-like names, which degrade audit cleanliness and operator trust.

## Reproduction Steps
1. Run `npx gitnexus analyze`.
2. Run `python3 scripts/pipeline_cli.py run`.
3. Inspect `006_System-Manifests/runs/latest_status_report.txt`.
4. Run `python3 scripts/pipeline_cli.py build-graph`.

## Suspected Root Causes
- Corpus changed substantially without corresponding manifest reconciliation.
- Tooling warnings were tolerated because indexing still completed.
- Integrity/status checks emphasize structural completion over operational cleanliness.

## Recommended Fix Direction
- Reconcile raw-layer manifest state explicitly before treating status outputs as healthy baselines.
- Investigate GitNexus analyzer warning spam; either fix or document it as expected noise.
- Tighten integrity checks so “passed” more closely matches operator expectations.

## Validation Needed After Fix
- Re-run `gitnexus analyze` and confirm warning-free or documented-safe behaviour.
- Re-run `pipeline_cli.py run` and confirm manifest drift reflects intended corpus state.
- Rebuild graph and verify integrity warnings align with actual issues only.

## Audit Verdict
Core commands are stable enough to execute, but the repo’s stability story is noisier than the current docs admit.
