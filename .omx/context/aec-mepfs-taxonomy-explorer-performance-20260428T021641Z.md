# AEC-MEPFS Taxonomy And Explorer Performance Context

## Task Statement
Proceed with the AEC-MEPFS implementation after the user reported that Explorer only shows seven nodes and that the graph feels janky/errors-prone. Determine the JSON source, expand the runtime graph to the governed AEC-MEPFS taxonomy skeleton, and check/fix Explorer performance risks.

## Desired Outcome
- Explorer defaults to an AEC-MEPFS graph that reflects the accepted L1/L2 taxonomy skeleton, not the seven-node staging stub.
- `HIS` and `FIG` remain top-level auxiliary domains, not Architecture children.
- Explorer remains stable with the larger graph.
- Fresh API, Python, Explorer, and safety verification evidence exists.

## Known Facts And Evidence
- Current branch is `main` at `21b95698`, synced with `origin/main` before edits.
- Explorer's AEC-MEPFS default currently consumes `shadow-backbone-graph.json`.
- The graph is generated from `scripts/tests/fixtures/aec_mepfs_backbone/admitted_backbone_nodes_l1_l2.json`.
- That fixture currently has 7 BackboneNode records and 4 `broader_than` relationships.
- The governed taxonomy seed is in `.ai/03_plans/AEC-MEPFS-Backbone/master-taxonomy-l1-l2-decision-record.md`.
- GitNexus index was up to date at `21b9569`; `loadPerspective`, `setLayout`, and `GraphScene` impact checks returned LOW risk.

## Constraints
- Do not use Gemini.
- Do not print secrets or environment variables.
- Do not ingest protected source content.
- Do not mutate Neo4j or run KG rebuild/reload/reset paths.
- Keep taxonomy material as high-level non-protected labels/definitions only.
- Preserve AEC-MEPFS-first Explorer behavior and the legacy escape path.

## Unknowns / Open Questions
- Whether the larger graph exposes vis-network initialization or physics jank in browser-level use.
- Whether route/evidence manifests need only a new staging run or additional parity artifacts.

## Likely Touchpoints
- `scripts/tests/fixtures/aec_mepfs_backbone/admitted_backbone_nodes_l1_l2.json`
- `006_System-Manifests/aec-mepfs-backbone/shadow-staging/`
- `api/v2Backbone.test.ts`
- `explorer/src/components/graph/VisNetworkHost.tsx`
- Explorer tests covering AEC default graph counts and legacy escape behavior
- `.ai/05_logs/`
