# Audit — Bounded Laws Source→Graph Automation

## Verdict
Proceed with a bounded orchestration slice.

## Why
The graph lane is now materially stronger, but the automation boundary is still incomplete. `run-dataset-graph` starts from admitted truth-bearing inputs and produces the graph correctly, while the upstream bounded dataset lane (refine → canonicalize → extract → review → promote) still requires manual/operator composition.

## Current verified truth
- `run-dataset-graph` is trustworthy for admitted inputs.
- dataset-safe extraction/review/promotion routing already exists.
- no raw-folder→graph shortcut is acceptable.

## Required next move
Introduce one bounded source→graph orchestration command that:
- starts from produced pipeline data
- keeps every stage dataset-local
- preserves review/promotion governance
- never mutates global `latest_*` graph/review artifacts in dataset mode

## In scope
- orchestration contract
- path isolation requirements
- stage ordering
- validation requirements

## Out of scope
- raw-PDF direct graphing
- generic all-laws rollout
- bypassing human/governed truth steps
