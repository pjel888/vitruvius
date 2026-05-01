# Ralph Context Snapshot: AEC-MEPFS Shadow Graph Parity

## Task Statement

Continue autonomous work after the admitted BackboneNode fixture slice. Make
substantial progress without waiting for repeated "what next/proceed" prompts.

## Desired Outcome

Implement the next bounded AEC-MEPFS shadow slice: a file-backed shadow graph
and parity/preview shape over admitted BackboneNode fixtures, with fresh QA,
architect verification, deslop review, and commit/push if complete.

## Known Facts / Evidence

- Latest clean pushed baseline before this snapshot: `e6769784`.
- GitNexus index is current at `e676978`.
- Prior slice added strict admitted `BackboneNode` validation and generated
  shadow run `20260426T000726Z` with 7 BackboneNodes, 12 predicates, 29 source
  rights rows, and no live-write boundaries.
- Current state docs say the next bounded move is shadow graph
  construction/parity before runtime cutover.
- Existing PRD/test-spec artifacts exist under `.omx/plans/`.

## Constraints

- No Neo4j writes, dump/load, reset, cleanup, or graph rebuild.
- No protected source text/table/figure/dataset ingest.
- No feature flag cutover and no Explorer default graph adoption.
- No edits to high-impact runtime roots without separate packet.
- Keep work file-backed, shadow-only, and reversible.
- Follow AGENTS.md: state-first, plan before implementation, GitNexus impact
  before editing symbols, validation report before completion.

## Unknowns / Open Questions

- Exact existing parity-runner and report-reader surfaces need inspection
  before choosing the smallest implementation path.
- Need determine whether the shadow graph belongs in the existing staging
  artifact, a derived consumer report, or a new artifact file.
- Need confirm API/Explorer shape that can preview graph adjacency without
  routing it into operational graph state.

## Likely Codebase Touchpoints

- `scripts/vitruvius/kg/backbone_shadow_staging.py`
- `scripts/vitruvius/kg/backbone_shadow_report_reader.py`
- `scripts/vitruvius/kg/backbone_contracts.py`
- `scripts/tests/test_kg_backbone_shadow_staging.py`
- `scripts/tests/test_kg_backbone_shadow_report_reader.py`
- `api/index.ts`
- `api/v2Backbone.test.ts`
- `explorer/src/components/explorer-rail/BackbonePreviewPanel.tsx`
- `explorer/src/types/index.ts`
- `.ai/03_plans/AEC-MEPFS-Backbone/`
- `.ai/05_logs/`
