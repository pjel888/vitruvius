---
task: vitruvius-audit-pass-1
phase: 04
created: 2026-04-16
author: AUDITOR
supersedes: null
status: ACCEPTED
---

# 2026-04-16 Routes, CRUD, and Admin Audit

## Purpose
Audit route-like behaviour in the actual Vitruvius runtime surface without inventing a web app where none exists.

## Scope
- CLI command routing in `scripts/pipeline_cli.py`
- Graph/query CLI subcommands
- Helper scripts under `scripts/`
- Admin/dashboard applicability

## What Was Inspected
- `scripts/pipeline_cli.py`
- `scripts/vitruvius/graph/cli.py`
- `scripts/vitruvius/query/cli.py`
- `scripts/test_odl_one.py`
- `scripts/test_pdf_text_detection.py`

## What Was Tested
- `python3 scripts/pipeline_cli.py run`
- `python3 scripts/pipeline_cli.py build-graph`
- `python3 scripts/pipeline_cli.py query-graph --from law-national-building-code-of-the-philippines --to concept-building-permit`
- `python3 scripts/pipeline_cli.py query-structured --function neighbors --subject concept-occupancy-classification`
- `python3 scripts/pipeline_cli.py query "What governs occupancy classification?"`
- `python3 scripts/test_pdf_text_detection.py --help`

## What Works
- Argparse command routing is live and stable.
- `run`, `build-graph`, `query-graph`, `query-structured`, and `export-graph-owl` execute.
- `query-graph` returns a valid path payload for a known edge.

## What Fails
- There is no admin surface and no CRUD UI to audit.
- `scripts/test_odl_one.py` is not safe as a probe script; `--help` does not exist and the file executes a real conversion.

## What Is Misleading
- “Routes” in this repo means CLI dispatch, not HTTP routing.
- Query commands look user-facing, but their evidence fidelity is materially weaker than their output format implies.

## Severity-Ranked Findings
- `HIGH` The graph/query route can return topology without trustworthy provenance. `query-structured` and `query` render supporting evidence blocks even when the underlying citations are empty placeholders.
- `MEDIUM` Command behaviour is not always self-describing. `pipeline_cli.py status` and `run` write manifests; `scripts/test_odl_one.py` has no argparse safety at all.
- `INFO` Admin/dashboard audit is not applicable in this repo state.

## Reproduction Steps
1. Run `python3 scripts/pipeline_cli.py query-structured --function neighbors --subject concept-occupancy-classification`.
2. Observe `"(no snippet)"` and `"(no section)"` in the rendered evidence block.
3. Run `python3 scripts/test_odl_one.py --help`.
4. Observe that it executes conversion logic rather than showing usage help.

## Suspected Root Causes
- CLI/operator tooling and one-off helper scripts were written for developers, not hardened as read-only user tools.
- Query presentation layer assumes graph edges are sufficient to count as evidence.

## Recommended Fix Direction
- Treat CLI mutation surfaces as first-class operator UX and document them clearly.
- Either harden helper scripts with argparse or stop treating them as probe utilities.
- Make query outputs provenance-faithful before expanding the query layer.

## Validation Needed After Fix
- Re-run the same CLI commands and confirm:
  - helper scripts respect `--help`
  - query outputs include real section/snippet provenance
  - no accidental state mutations occur during read-only probe flows

## Audit Verdict
Route/admin work is only partially applicable. CLI command routing is real; admin and web CRUD surfaces are not.
