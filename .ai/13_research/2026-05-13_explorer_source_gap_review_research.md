# Research: Explorer Source Gap Review Surface

## Scope
Read-only Explorer visibility for `source-grounding-gap-workqueue.jsonl` and `source-link-proposals.jsonl` artifacts.

## Findings
- Repository state says the current active source-grounding objective is a no-write coverage inventory and workqueue. The milestone explicitly does not authorize active graph mutation, Resource Layer mutation, protected payload admission, or production database writes.
- Existing API route style for file-backed previews is in `api/index.ts`:
  - `GET /v2/backbone/improvement-overlay`
  - `POST /v2/answer/context`
  - legacy `GET /node/:id` includes `sourceGroundedContext`
- Existing Explorer display point is `explorer/src/components/inspector/NodeInspector.tsx`, especially the Context tab and `SourceContextPanel`.
- Existing source-gap artifacts contain:
  - workqueue rows keyed by `workqueue_id`, `item_type`, `node_id` or `edge_key`, `from_id`, `predicate`, `to_id`, `priority_score`, `priority_rank`, `suggested_resources`, and safety booleans.
  - proposal rows keyed by `proposal_id`, target node/edge fields, `resource_id`, `title`, `score`, `matched_terms`, and safety booleans.

## Tooling Notes
- `bash ./scripts/refresh_code_intelligence.sh` completed before code edits. It still reports known YAML parser warnings for missing `tree-sitter-yaml` and embedding failures for oversized campaign logs.
- Morph code search returned 429, so local GitNexus CLI, ChunkHound, and targeted file inspection were used.

## Evidence Boundary
This work consumes generated proposal artifacts only. It does not claim source truth and does not create source links.
