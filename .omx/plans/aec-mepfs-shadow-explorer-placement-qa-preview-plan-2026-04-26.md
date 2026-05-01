# AEC-MEPFS Shadow Slice Plan Review — Explorer Placement QA Preview

## Scope

Add an opt-in placement QA summary section inside the existing AEC-MEPFS Backbone preview panel in Explorer. The section must consume `GET /v2/backbone/placement-qa` only after explicit user action and must preserve all current shadow-only boundaries:

- no Explorer default graph adoption
- no graph state replacement
- no Neo4j writes
- no KG rebuild
- no protected content ingest
- no feature flag cutover

## Repo-Grounded Findings

- The active phase and milestone tracker already name this exact slice as the preferred next bounded shadow action.
- `ExplorerRail.tsx` already uses a two-step opt-in pattern:
  - opening the AEC-MEPFS preview triggers `getBackboneSummary()`
  - clicking the taxonomy detail control triggers `getBackboneTaxonomyPreview()`
- `BackbonePreviewPanel.tsx` already has a dedicated summary area plus an opt-in “Readiness details” subsection, so the placement QA summary fits as a parallel additive subsection rather than a new panel.
- `explorer/src/types/index.ts` already defines `BackbonePlacementQaPreview`; this reduces risk and likely eliminates the need to edit the central types file unless the route contract drifted.
- `graphApi.ts` does not yet expose a `getBackbonePlacementQaPreview()` helper.
- Existing tests already assert the non-default and non-state-replacement behavior for the backbone preview and taxonomy detail fetch.

## Implementation Plan

1. Extend the Explorer rail data flow in `explorer/src/components/ExplorerRail.tsx`.
Acceptance criteria:
- Add local state for placement QA data, loading, error, and request identity mirroring the taxonomy preview pattern.
- Add a dedicated loader that calls a new API helper for `/v2/backbone/placement-qa`.
- Do not fetch placement QA on Explorer load or on backbone preview open.
- Do not mutate `useSceneStore` graph nodes, edges, or perspective when placement QA is loaded or refreshed.

2. Add the API helper in `explorer/src/api/graphApi.ts`.
Acceptance criteria:
- Export `getBackbonePlacementQaPreview(): Promise<BackbonePlacementQaPreview>`.
- Keep the route additive and read-only against `/v2/backbone/placement-qa`.
- Reuse the existing `api<T>()` wrapper and current error behavior.

3. Add an opt-in Placement QA summary subsection in `explorer/src/components/explorer-rail/BackbonePreviewPanel.tsx`.
Acceptance criteria:
- Add a second explicit-action control or clearly separated action inside the panel for loading placement QA.
- Render a compact summary only after explicit action:
  - pass/fail totals
  - auto-accept count
  - proposal level counts
  - review queue counts
  - required coverage booleans
  - contract-validation status/warnings
  - safety boundary status
- Keep the section clearly labeled as shadow/read-only preview data.
- Preserve the existing taxonomy subsection behavior; loading placement QA must not implicitly load taxonomy, and vice versa.
- Refreshing the backbone preview should clear cached opt-in detail sections the same way taxonomy currently resets.

4. Expand focused component tests in `explorer/src/components/componentInteraction.test.tsx`.
Acceptance criteria:
- Add fixture data for `BackbonePlacementQaPreview`.
- Assert the panel shows placement QA as “Not loaded” before explicit action.
- Assert clicking the placement QA control invokes the handler and renders the compact summary.
- Assert error and loading copy for the new subsection without regressing the existing summary/taxonomy assertions.

5. Expand integration coverage in `explorer/src/app.searchInspector.integration.test.tsx`.
Acceptance criteria:
- Add a placement-QA fetch counter and mock route response.
- Assert zero placement-QA fetches before user action.
- Assert opening the backbone preview still fetches only the summary.
- Assert clicking the placement-QA control fetches the new route exactly once.
- Assert graph state remains unchanged after placement-QA load:
  - same perspective
  - same nodes
  - same edges
- Assert backbone refresh clears placement-QA detail state just as it clears taxonomy detail state.

## Test Plan

- `bun test explorer/src/components/componentInteraction.test.tsx`
- `bun test explorer/src/app.searchInspector.integration.test.tsx`

Optional follow-up if the touched test harness expects broader coupling:

- `bun test explorer/src/components`

## Blockers / Risks

- No hard blocker found for planning.
- The only contract check to confirm during implementation is that the live `/v2/backbone/placement-qa` payload still matches the already-present `BackbonePlacementQaPreview` interface. If it has drifted, the additive type change becomes justified; otherwise avoid touching `explorer/src/types/index.ts`.
- UX microcopy/control placement is mildly open, but not a planning blocker: the safest path is to mirror the existing taxonomy opt-in affordance instead of introducing a new panel or workflow.

## Recommended Write Scope

- `explorer/src/components/ExplorerRail.tsx`
- `explorer/src/components/explorer-rail/BackbonePreviewPanel.tsx`
- `explorer/src/api/graphApi.ts`
- `explorer/src/components/componentInteraction.test.tsx`
- `explorer/src/app.searchInspector.integration.test.tsx`

Only if contract drift is confirmed:

- `explorer/src/types/index.ts`
