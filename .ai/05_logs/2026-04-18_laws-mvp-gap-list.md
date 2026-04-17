# 2026-04-18 Laws MVP gap list

This log records what is still missing after the current one-command laws MVP graph became operational.

## Working now
- one-command aggregate graph for the completed authoritative laws wave
- machine-readable completed/disposition/provenance/index/status artifacts
- operator wrapper: `./run-laws-mvp-graph`

## Current gaps
### 1. Still laws-specific
The aggregate builder is still specialized to the laws wave and its ledgers.

### 2. Deferred residuals are outside the MVP graph
The current MVP intentionally excludes:
- `BERDE`
- `HB-3391`
- `HB-5207`
- `RA-11361`
- `RA-7920`
- `SB-2982`

This is correct for integrity, but means the graph is not yet a graph of literally every raw folder.

### 3. Review-heavy sources still need manual/guarded trust treatment
The aggregate run still reports:
- `manual_review_required_count = 7`
- `spot_review_required_count = 24`
- `summary_auto_withheld_count = 24`
- `shallow_representation_count = 3`

So the MVP works, but parts of the graph still rely on guarded/no-summary handling.

### 4. No incremental resume/caching layer yet
The aggregate command works, but repeated runs still redo significant work.

### 5. No dataset-agnostic aggregate-manifest builder yet
The pattern is proven, but it is not yet generalized beyond laws.

## Next engineering targets
1. incremental resume/caching for aggregate runs
2. dataset-agnostic completed-lane manifest synthesizer
3. stronger trust-tier graphing that can optionally visualize deferred / weak-authority items separately instead of excluding them entirely
4. clearer operator docs for interpreting guarded/manual-review nodes in the aggregate graph
