---
task: dataset-wide-automation-mvp
created: 2026-04-18
status: in_progress
---

# Plan — Dataset-wide automation MVP

1. identify which parts of the laws aggregate builder can be generalized into dataset-agnostic helpers
2. define a minimal generic ledger/manifest contract for other dataset families
3. implement the first generic automation helper without regressing the laws MVP
4. validate that the laws MVP still works after the generalization step
5. expose the first generic aggregate execute command surface without regressing the laws MVP

## Progress to date
- steps 1 through 4 are now complete via:
  - helper extraction in `scripts/vitruvius/aggregate_manifest.py`
  - generic aggregate-manifest build command:
    - `build-completed-aggregate-manifest`
- current active step:
  - step 5 — generic aggregate execute command:
    - `run-completed-aggregate`
