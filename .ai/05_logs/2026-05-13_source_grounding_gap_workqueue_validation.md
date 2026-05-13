# Source Grounding Gap Workqueue Validation

Date: 2026-05-13

## Changes Validated

- Extended `aec-source-grounding-inventory` with proposal-only source/resource gap workqueue output.
- Added `source-grounding-gap-workqueue.jsonl`.
- Added `source-link-proposals.jsonl`.
- Added CLI controls for workqueue size, proposal count, threshold, and disabling workqueue output.
- Updated source-grounded roadmap/state docs.

## Validation Commands

```bash
bash ./scripts/refresh_code_intelligence.sh
python -m py_compile scripts/vitruvius/kg/source_grounding_inventory.py scripts/pipeline_cli.py
$env:PYTHONPATH='scripts'; python -m pytest scripts/tests/test_kg_source_grounding_inventory.py -q
$env:PYTHONPATH='scripts'; python scripts/pipeline_cli.py aec-source-grounding-inventory --run-id SOURCE_GAP_WORKQUEUE_SMOKE_FINAL --relationship-run-id latest --max-gap-examples 5 --max-workqueue-items 25 --max-resource-proposals-per-item 3 --min-resource-proposal-score 0.08
$env:PYTHONPATH='scripts'; python -m pytest scripts/tests/test_kg_source_grounding_inventory.py scripts/tests/test_kg_aec_relationship_improvement.py scripts/tests/test_kg_backbone_shadow_staging.py scripts/tests/test_kg_backbone_graph_quality.py -q
git diff --check -- scripts/vitruvius/kg/source_grounding_inventory.py scripts/pipeline_cli.py scripts/tests/test_kg_source_grounding_inventory.py .ai/13_research/2026-05-13_source_grounding_gap_workqueue_research.md .ai/02_audits/2026-05-13_source_grounding_gap_workqueue_audit.md .ai/03_plans/2026-05-13_source_grounding_gap_workqueue_plan.md .ai/14_project_management/source_grounded_kg_ai_goal_tracker.md .ai/ACTIVE_WORK.md .ai/STRATEGIC_NEXT_MOVE.md docs/knowledge-graph/aec-explorer-overlay-campaigns.md
```

## Results

- `py_compile`: passed.
- Focused source-grounding tests: `7 passed`.
- Adjacent KG safety/regression tests: `163 passed`.
- CLI smoke `SOURCE_GAP_WORKQUEUE_SMOKE_FINAL`: wrote 25 workqueue items and 39 source-link proposals.
- `git diff --check`: passed; Git printed line-ending warnings for existing working-copy settings.

## Code Intelligence Notes

- GitNexus was already up to date before implementation.
- Post-change `bash ./scripts/refresh_code_intelligence.sh` completed with exit code 0 after rerun with a longer timeout.
- ChunkHound completed with existing timeout skips on large source files.
- code-review-graph rebuilt, but reported existing missing `tree-sitter-yaml` warnings and embedding failures on oversized campaign log chunks.
- GitNexus impact lookup for `run_source_grounding_inventory` returned `UNKNOWN` because this module is newly untracked in the current working tree; blast radius was bounded with CLI/tests instead.
- GitNexus `detect-changes` reports `critical` risk for the broad dirty working tree, including prior Explorer/API/relationship-workflow changes outside this slice. The source-grounding workqueue slice itself is bounded to the inventory CLI/module/tests/docs.

## Safety

- No active graph file was modified by the workflow.
- No Resource Layer registry was modified by the workflow.
- No Neo4j or Postgres write path was added.
- Workqueue and proposal artifacts are explicitly `pending_only`, `auto_admit: false`, `active_graph_mutation: false`, and `resource_layer_mutation: false`.
- No protected source payloads, API keys, or `reasoning_content` are written.
