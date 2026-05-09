# AEC Relationship Campaign Resilience Plan

## Goal

Prepare the pending-only AEC relationship and node-improvement workflow for longer campaign runs by preventing transient cloud response defects from killing the whole run and by replacing fragile pasted mega-commands with short checked scripts.

## Criteria

- A DeepSeek response with an empty `choices` array is retried when retry budget is available.
- If the empty response still cannot be used, the current pair is recorded as a validation rejection and the run continues.
- Node-consolidation cloud response rejections are pair-scoped, not run-fatal.
- Existing empty-content, truncated-JSON, schema-validation, and pending-only safety behavior remains intact.
- No active graph file, Neo4j database, or Postgres database is mutated.
- Campaign scripts reuse the isolated campaign ledgers and keep threshold fingerprints aligned.
- The next campaign is launched through a short script command, not a copied multi-line flag block.

## Implementation Scope

- `scripts/vitruvius/kg/aec_relationship_improvement.py`
  - Retry actual empty-choices DeepSeek responses.
  - Catch node-consolidation `CloudResponseRejectedError` and write validation/rejected artifacts instead of allowing a fatal run.
- `scripts/tests/test_kg_aec_relationship_improvement.py`
  - Add regression coverage for empty DeepSeek choices retry.
  - Add regression coverage for node-consolidation response rejection as pair-scoped failure.
- `scripts/run_aec_backbone_all_nodes_bounded_003.sh`
  - Preserve the known-good short runner used for campaign 003.
- `scripts/run_aec_backbone_all_nodes_bounded_004.sh`
  - Add the next larger campaign runner: 50,000 relationship pairs and 20,000 node-consolidation pairs with campaign ledger reuse.
- `scripts/watch_aec_relationship_campaign.sh`
  - Add a short watcher command for latest or `RUN_ID`-selected campaign progress.

## Validation

- Run focused regression tests for empty choices, node-consolidation pair rejection, and existing empty-content handling.
- Run the full AEC relationship-improvement test file.
- Compile the changed Python module and CLI.
- Syntax-check the Bash scripts.
- Confirm generated run artifacts remain untracked.
