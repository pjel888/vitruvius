# PRD — KG Semantic Connectedness Overlays

## Objective
Improve the file-backed AEC-MEPFS backbone graph so it better answers cross-discipline coordination, commissioning/handover, resilience/continuity, and applicability questions.

## User stories

1. As an AEC coordinator, I want equipment anchorage/support relationships across MEPFS/ICT/security topics so that seismic, wind, flood, vibration, access, penetration, firestopping, and structural coordination are discoverable.
2. As a commissioning lead, I want testing/inspection/acceptance/handover concepts connected to the systems they verify so that closeout workflows are visible in the graph.
3. As an operations/resilience planner, I want continuity, backup power, redundancy, cybersecurity, water, IAQ, and emergency communications topics connected to source families and facility systems.
4. As a code/steward reviewer, I want applicability overlays for AHJ, local adoption, occupancy, risk category, climate, seismic/flood/hazard, and lifecycle phase to constrain discipline topics without protected payload ingest.

## Scope
- File-backed graph data, deterministic enrichment script, metadata-only source registry updates, tests, reports, shadow artifacts, and state docs.
- Kimi-assisted research/synthesis/review only for model-assisted taxonomy work.

## Out of scope
- Protected source payload ingestion.
- Live graph/Neo4j mutation or promotion.
- KG rebuild/reload/reset.
- Runtime API behavior changes beyond fixture/report count expectations caused by file-backed data.

## Acceptance criteria
- At least 250 governed relationships added if schema permits.
- At least 40 cross-domain relationships.
- At least 40 commissioning/testing/handover relationships.
- At least 40 resilience/continuity relationships.
- At least 40 applicability overlay relationships.
- At least 25 existing nodes improved.
- Add only necessary real nodes.
- Add/improve source-rights rows only as metadata/reference-only.
- All required validation passes.
