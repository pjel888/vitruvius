# Source Grounding Gap Workqueue Plan

Date: 2026-05-13

## Goal

Extend the no-write source-grounding inventory so it also writes an actionable, ranked source/resource gap workqueue and source-link proposal file.

## Implementation Steps

1. Extend `SourceGroundingInventoryConfig`.
   - Add `write_gap_workqueue`, `max_workqueue_items`, `max_resource_proposals_per_item`, and `min_resource_proposal_score`.

2. Add deterministic Resource matching helpers.
   - Normalize/tokenize node and Resource metadata.
   - Score overlap plus authority/verification/access signals.
   - Keep only existing non-rejected Resources.

3. Build workqueue and proposal artifacts.
   - Write `source-grounding-gap-workqueue.jsonl`.
   - Write `source-link-proposals.jsonl`.
   - Add `source_gap_workqueue` report summary.
   - Add paths/counts to the CLI summary.

4. Wire CLI flags.
   - `--write-gap-workqueue` / `--no-write-gap-workqueue`
   - `--max-workqueue-items`
   - `--max-resource-proposals-per-item`
   - `--min-resource-proposal-score`

5. Add tests.
   - Artifact creation.
   - Stable high-impact prioritization.
   - CLI parse.
   - No input/Resource Layer mutation.
   - No secrets or `reasoning_content`.

6. Update documentation/state.
   - Goal tracker.
   - Active work / strategic next move.
   - Explorer overlay campaign docs.
   - Validation log after verification.

## Plan Critique

- The workqueue is only as good as available Resource metadata. This is acceptable because every output is candidate-only.
- Do not attempt external source lookup or AI matching in this slice.
- Do not admit NodeResourceLinks or relationships.
- Keep test fixtures small and deterministic.

## Acceptance Criteria

- `aec-source-grounding-inventory` still runs without model/API calls.
- Workqueue/proposal files are written by default.
- CLI can disable workqueue output.
- Tests prove the active graph fixture and Resource Layer inputs are not modified.
- Verification passes with focused Python tests and compile checks.
