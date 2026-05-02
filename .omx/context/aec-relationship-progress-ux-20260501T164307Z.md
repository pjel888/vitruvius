# AEC Relationship Progress UX Context

## Task Statement
Improve operator UX and terminal interactivity for the pending-only AEC relationship-improvement workflow.

## Desired Outcome
Add in-run progress reporting plus a watcher command that can attach to existing run folders and show progress from checkpoint, report, JSONL artifacts, and events without restarting the active job.

## Known Facts / Evidence
- Current workflow module: `scripts/vitruvius/kg/aec_relationship_improvement.py`.
- Current CLI command: `scripts/pipeline_cli.py aec-improve-relationships`.
- Current tests: `scripts/tests/test_kg_aec_relationship_improvement.py`.
- The workflow is pending-only and writes review artifacts under `006_System-Manifests/aec-mepfs-backbone/semantic-overlays/<run_id>/`.
- Current state docs keep production Neo4j promotion, protected payloads, KG rebuild/reset, and destructive graph mutation hard-blocked.
- `docs/shared/agent-tiers.md` is missing.
- Deferred MCP code search returned HTTP 429, so exploration falls back to repo-local tools.

## Constraints
- Do not mutate active graph files.
- Do not write to Neo4j or Postgres.
- Do not weaken `--apply` rejection.
- Do not expose API keys.
- Do not log or store `reasoning_content`.
- Preserve existing `local_only` and `adaptive_cloud` behavior.
- Watcher must be read-only and tolerate missing/partial artifacts.

## Unknowns / Open Questions
- Whether `rich` is already installed or declared in dependencies.
- Whether adding `rich>=13` to dependency files is appropriate in this repo.
- Exact current checkpoint fields and JSONL artifact shape after the council implementation.

## Likely Codebase Touchpoints
- `scripts/vitruvius/kg/aec_relationship_improvement.py`
- `scripts/pipeline_cli.py`
- `scripts/tests/test_kg_aec_relationship_improvement.py`
- Dependency manifests, if present.
