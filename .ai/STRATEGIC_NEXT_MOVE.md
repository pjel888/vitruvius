# Strategic Next Move

**Updated:** 2026-05-13

## Single Best Next Move

**Use the no-write source-grounding inventory, gap workqueue, source-link proposal file, and `SourceGroundedAnswerContext` to close high-value source/resource gaps before any answer composer, cloud AI automation, database projection, or new Rust optimization.** Relationship enrichment should continue only when it improves source-grounded reasoning paths; the next highest-value work is connecting admitted graph structure to learner-safe resources, evidence selectors, and explicit claim classes.

## Why This Is Right Now

- The AEC-MEPFS authored backbone and local file-backed runtime/Explorer surfaces exist.
- The graph now has enough relationship structure and pending overlay coverage that quality, evidence attachment, and reasoning coverage matter more than raw edge count.
- `aec-source-grounding-inventory` and `POST /v2/answer/context` now exist as read-only inspection surfaces.
- `aec-source-grounding-inventory` now also writes proposal-only gap workqueue and source-link proposal JSONL artifacts from existing Resource metadata.
- `GET /v2/backbone/source-gap-workqueue`, Explorer NodeInspector, and the AEC-MEPFS rail preview now make those gap/proposal artifacts inspectable without creating source links or admitting graph changes.
- The raw/conversion/canonical layers exist specifically to preserve document custody and convert source material into admitted, traceable knowledge.
- Future database projection work should accelerate this model, not replace the custody/admission truth model.

## Concrete Tasks

1. Keep `/.ai/14_project_management/source_grounded_kg_ai_goal_tracker.md` current as the project-manager surface for purpose, achievements, gaps, gates, and next actions.
2. Use the Explorer workqueue browsing surface to select high-value source/resource attachment targets.
3. Add source/resource support for selected answer-critical nodes and relationships through the existing review workflow.
4. Design the AI-assisted relationship/source-link script as proposal-only by default, with no direct canonical mutation.
5. Add reasoning-path tests that require both graph traversal and source/resource availability for priority answer flows.
6. Keep database work as deterministic projection architecture: canonical custody first, projection speed second.
7. Treat Rust and databases as acceleration layers only after benchmark/parity gates.

## Do Not Do

- Do not treat AI output as admitted truth.
- Do not invent source metadata, URLs, editions, AHJ claims, code claims, or numerical design criteria.
- Do not copy protected source payloads into graph/database properties.
- Do not mutate production graph stores or Resource Layer records without the existing review and rollback gates.
- Do not optimize for raw relationship count at the expense of source grounding and reasoning quality.

## Next Boundary

The next implementation packet should be source/resource gap closure driven by the inventory report. Only after priority paths have real resource selectors should Vitruvius add an AI answer composer, cloud batch acceleration, database projection loaders, or Rust ports.
