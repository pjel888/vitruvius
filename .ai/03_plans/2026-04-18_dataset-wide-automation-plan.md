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
6. expose a profile-driven generic operator path so future dataset families can onboard with one reusable wrapper

## Progress to date
- steps 1 through 4 are now complete via:
  - helper extraction in `scripts/vitruvius/aggregate_manifest.py`
  - generic aggregate-manifest build command:
    - `build-completed-aggregate-manifest`
- current active step:
  - steps 5 and 6 are now complete via:
    - `run-completed-aggregate`
    - `build-completed-aggregate-from-profile`
    - `run-completed-aggregate-from-profile`
    - `./run-dataset-mvp-graph`

## Next live step
- reusable demo-family validation is now complete:
  - `laws-demo`
- dataset-family aliasing is now complete:
  - catalog + family run path
- dataset-family registration is now complete:
  - one command can write the profile and catalog entry

## Current next step
- family scaffolding is now in place:
  - starter completed-ledger
  - starter manifest index
  - profile
  - catalog entry
- family lane admission is now in place:
  - completed manifest -> ledger/index registration
- the next real proof is still:
  - onboard the first true non-laws trusted dataset family once its completed lanes are admitted
