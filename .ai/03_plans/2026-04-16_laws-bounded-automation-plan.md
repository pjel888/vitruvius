---
task: laws-bounded-automation
phase: 05
created: 2026-04-16
author: CODER
status: ACCEPTED
---

# 2026-04-16 Laws Bounded Source→Graph Automation Plan

## Goal
Automate the bounded dataset pipeline from produced intermediate data through the official dataset graph without weakening truth governance.

## Desired command
```bash
python3 scripts/pipeline_cli.py run-dataset-source-to-graph \
  --dataset-manifest config/datasets/laws-core-bundle-m1.yaml
```

## Pipeline boundary
The command must orchestrate only bounded, produced-data stages:
1. verify/select refined markdown inputs
2. canonicalize selected refined sources
3. extract section-aware relationship candidates dataset-locally
4. review dataset-locally
5. promote dataset-locally
6. build/query/export graph from resulting admitted dataset inputs

## Non-negotiable rules
- no raw-folder→graph shortcut
- no skipped review/promotion
- no global `latest_*` reads/writes in dataset mode
- no behavior change to default/global path when unused

## Smallest safe implementation slice
1. extend manifest/spec with the minimum upstream stage paths needed
2. add a dry-run orchestration mode first
3. add execute mode only after path-isolation tests exist
4. reuse existing stage entrypoints instead of duplicating logic

## Verification requirements
- every stage writes dataset-local outputs
- default/global outputs remain unchanged
- malformed stage input fails cleanly with machine-readable error
- bounded end-to-end run produces the same graph truth as the manually composed lane
