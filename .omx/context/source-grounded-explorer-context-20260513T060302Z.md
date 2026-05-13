# Source-Grounded Explorer Context Packet

## Task Statement

Implement the next roadmap packet for Vitruvius: reconcile current source-grounded KG AI direction with the recent AEC relationship/node overlay campaigns, then add a no-write source/resource coverage inventory and read-only Explorer/API answer-context surface.

## Desired Outcome

- The project state reflects the recent AEC pending overlay campaigns without treating pending candidates as admitted graph truth.
- Operators can run a no-write coverage inventory that measures graph/source/resource grounding for nodes, relationships, and pending overlays.
- API/Explorer can expose a rights-safe, read-only source-grounded context for a selected concept or query.
- The implementation preserves pending-only behavior, active graph immutability, Resource Layer safety, and production database blockers.

## Known Facts / Evidence

- `.ai/STRATEGIC_NEXT_MOVE.md` names the no-write source/resource coverage inventory plus `SourceGroundedAnswerContext` as the single best next move.
- `.ai/14_project_management/source_grounded_kg_ai_goal_tracker.md` tracks source-grounded KG AI as the north star.
- Recent run `aec_backbone_all_nodes_bounded_004` reported 30,000 new relationship model calls, 20,000 ledger skips, 1,579 accepted pending relationship candidates, 1,178 review candidates, 76 accepted pending node consolidations, and pending-only Explorer overlay visibility.
- Existing active graph mutation remains blocked; pending overlay artifacts are proposal/review surfaces only.
- `api/index.ts`, Explorer inspector/rail components, Resource Layer helpers, and AEC overlay artifacts are likely touchpoints.

## Constraints

- Do not mutate active graph files.
- Do not write to Neo4j or Postgres.
- Do not weaken `--apply` rejection or pending-only behavior.
- Do not expose API keys, bearer tokens, protected payload text, or `reasoning_content`.
- Do not auto-admit pending overlay edges or node consolidations.
- Do not use web search or external source fetching for this packet.

## Unknowns / Open Questions

- Exact existing Resource Layer helper shapes need local inspection before endpoint implementation.
- Explorer panel placement should reuse existing UI conventions and avoid graph-state mutation.
- Coverage inventory should prefer compact no-write reporting over deep refactors.

## Likely Codebase Touchpoints

- `.ai/01_roadmap/current-phase.md`
- `.ai/01_roadmap/milestone-tracker.md`
- `.ai/14_project_management/source_grounded_kg_ai_goal_tracker.md`
- `.ai/ACTIVE_WORK.md`
- `.ai/STRATEGIC_NEXT_MOVE.md`
- `.ai/03_plans/INDEX.md`
- `api/index.ts`
- `api/resourceLayer/*`
- `explorer/src/components/*`
- `explorer/src/types/index.ts`
- `scripts/pipeline_cli.py`
- possible new script under `scripts/vitruvius/kg/`
- possible tests under `scripts/tests/`, `api/*.test.ts`, `explorer/src/**/*.test.tsx`
