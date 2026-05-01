# Ralph Context Snapshot: AEC-MEPFS Shadow Completion

## Task Statement

Continue the Vitruvius AEC-MEPFS shadow-backbone work autonomously until the
safe shadow-only/read-only scope is exhausted or a true external blocker is
reached.

## Desired Outcome

Advance the next bounded shadow slice from fresh repository evidence, verify it
with focused and affected suites, document the evidence, commit, push, then
continue to the next safe slice.

## Current Baseline

- Branch: `main`
- Latest pushed commit at start: `8a68b148 Stage shadow graph parity before runtime graph adoption`
- Working tree at start: clean and synced with `origin/main`
- Latest generated shadow staging evidence:
  `006_System-Manifests/aec-mepfs-backbone/shadow-staging/20260426T003710Z/`
- Latest shadow graph counts: 7 nodes, 4 edges, 3 roots, max depth 2
- Existing seventh-slice validation log:
  `.ai/05_logs/2026-04-26_aec_bb_shadow_graph_parity_validation.md`

## Hard Constraints

- No Neo4j writes, resets, dump/load rehearsals, or KG rebuilds.
- No protected source content ingest or canonical source admission.
- No feature flag cutover.
- No Explorer default graph adoption.
- No live runtime promotion.
- Keep all new behavior file-backed, shadow-only, read-only, auditable, and
  fail-closed.

## Tooling Notes

- OMX state MCP transport closed during state reads/writes, so file-backed
  planning artifacts are the durable state surface for this run.
- Team workflow was requested, but this leader session is not inside `tmux`.
  Use native Codex subagents for bounded planning/review lanes instead.
- Gemini CLI is available at `/opt/homebrew/bin/gemini`.
- Kimi CLI is available at `/Users/philiplewis/.local/bin/kimi`.
- `docs/shared/agent-tiers.md` is absent; use AGENTS.md and skill docs as the
  local orchestration contract.

## Selected Next Slice

Harden the AEC-MEPFS API/Explorer parity runner so the already implemented
shadow graph and `/v2/backbone/taxonomy` preview are mandatory parity evidence.

This is the safest high-value next slice because it:

- strengthens existing evidence rather than promoting runtime behavior,
- keeps verification file-backed and command-registry bounded,
- adds no Neo4j, KG rebuild, source-ingest, feature flag, or default Explorer
  adoption path,
- directly covers the most recent shadow graph implementation with a generated
  parity report.

## Likely Touchpoints

- `scripts/vitruvius/kg/backbone_parity_runner.py`
- `scripts/tests/test_kg_backbone_parity_runner.py`
- `scripts/tests/fixtures/aec_mepfs_backbone/api-explorer-parity-cases.json`
- `scripts/tests/fixtures/aec_mepfs_backbone/valid_integration_readiness_s3.json`
- `.ai/03_plans/AEC-MEPFS-Backbone/`
- `.ai/05_logs/`
- generated parity report under
  `006_System-Manifests/aec-mepfs-backbone/parity/RUN_ID/`

## Next Exact Step

Run GitNexus impact for `run_parity_fixture` / `_validate_parity_case_coverage`,
create the eighth-slice implementation packet, then implement the parity runner
hardening with focused tests.
