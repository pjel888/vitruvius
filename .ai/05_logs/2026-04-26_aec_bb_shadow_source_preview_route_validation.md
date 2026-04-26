# AEC-BB Shadow Source Preview Route Validation

**Date:** 2026-04-26
**Scope:** sixteenth AEC-MEPFS Backbone shadow slice
**Status:** validated

## Implemented Boundary

- Added additive file-backed `GET /v2/sources/:source_id`.
- Added compact source preview schema:
  `aec-bb-shadow-v2-source-preview/v1`.
- Resolved staged source-rights registry rows by source ID or source-family
  label.
- Returned sanitized source metadata: copyable labels, evidence title,
  publisher authority, source-rights class, clearance state, declared-use
  boundary, currentness check date, steward, and update cadence.
- Returned `400 SHADOW_BACKBONE_SOURCE_ID_INVALID` for malformed or
  whitespace-only decoded source IDs, and `404 SHADOW_BACKBONE_SOURCE_NOT_FOUND`
  only for syntactically valid unknown source IDs.
- Omitted official URLs, blocking notes, intended-use prose, standards text,
  source payloads, and protected content.
- Did not change Explorer defaults, v1 routes, Neo4j code, KG pipeline code,
  source ingestion, or feature flags.

## Cleanup Plan

1. Keep the route additive under `/v2/sources/:source_id`.
2. Reuse existing file-backed shadow report and staging artifact validation.
3. Fail closed when source IDs are missing/unknown, malformed, or runtime
   boundaries drift.
4. Expose only sanitized source metadata needed by preview/parity consumers.
5. Regenerate parity evidence after the route-backed source case is connected.

## Code-Impact Evidence

- `npx --yes gitnexus@1.6.2-rc.10 status`
  - Indexed commit before slice: `ebac545`
  - Current commit before slice: `ebac545`
  - Status: up to date.
- `npx --yes gitnexus@1.6.2-rc.10 impact --repo vitruvius buildShadowBackboneTaxonomyPreview --direction upstream --include-tests`
  - Risk: LOW
  - Impacted count: 5
  - Direct impacts: `api/index.ts`, `api/v2Backbone.test.ts`,
    `buildShadowBackboneNodePreview`, and `buildShadowBackboneSearchPreview`

Risk disposition: the new helper is additive and route-local. It reuses the
same staging validation path as the existing taxonomy/search previews and is
verified with focused route tests, broad API tests, parity-runner evidence, and
Explorer regression checks.

## Verification

- `cd api && bun test v2Backbone.test.ts`
  - Result: 38 passed.
- `cd api && bunx tsc --noEmit`
  - Result: passed.
- `PYTHONPATH=scripts python3 -m vitruvius.kg.backbone_parity_runner --run-id 20260426T052238Z --timeout-seconds 300`
  - Result: ok, 6/6 commands passed, 24/24 cases passed.
- `PYTHONPATH=scripts python3 -m pytest -q scripts/tests/test_kg_backbone_parity_runner.py scripts/tests/test_kg_backbone_contracts.py scripts/tests/test_kg_backbone_placement_qa.py scripts/tests/test_kg_backbone_shadow_staging.py scripts/tests/test_kg_backbone_shadow_report_reader.py`
  - Result: 96 passed.
- `cd api && bun test`
  - Result: 56 passed.
- `cd explorer && bun test`
  - Result: 42 passed.
- `cd explorer && bun run lint`
  - Result: passed.
- `cd explorer && bun run build`
  - Result: passed with the existing Vite chunk-size warning.

Generated parity report:

`006_System-Manifests/aec-mepfs-backbone/parity/20260426T052238Z/api-explorer-parity-report.json`

Report counts:

- Commands run: 6
- Commands passed: 6
- Cases declared: 24
- Cases passed: 24

## Advisory Review

- Gemini CLI was attempted with `--approval-mode plan`; it remained blocked by
  account-side HTTP 403 before producing findings.
- Kimi CLI was attempted with `--plan`; it reported no safety regressions for
  Neo4j writes, KG rebuilds, protected ingest, feature cutover, Explorer
  adoption, source leaks, parity/status/shape coverage, or 503 fail-closed
  coverage.
- Kimi identified one low-value route semantics gap: whitespace-only decoded
  source IDs previously mapped to `404`. This was fixed so blank decoded IDs
  now return `400 SHADOW_BACKBONE_SOURCE_ID_INVALID`.
- Kimi also noted request-level audit logging and declared-use-boundary
  semantics as non-blocking future production-readiness checks. Those remain
  outside this preview-only shadow slice.
- After the blank-ID parity-contract fix, Gemini was attempted again and
  remained blocked by the same account-side HTTP 403 before producing findings.
- After the blank-ID parity-contract fix, Kimi was attempted again with a
  bounded non-editing review prompt and timed out without producing additional
  findings.
- After the parity-runner required-category enforcement fix, Gemini was
  attempted again and remained blocked by the same account-side HTTP 403 before
  producing findings.
- After the parity-runner required-category enforcement fix, Kimi was attempted
  again with a bounded non-editing review prompt and timed out without
  producing additional findings.

## Architect Review

Initial native architect review returned `REJECTED` with two evidence-quality
findings:

- `API-PARITY-011` declared top-level `sourceLabels` and `evidenceTitle` even
  though the route returns those fields under `sourceRecord`.
- The route-level 503 unavailable path was not tested end to end.

Both were addressed before commit:

- `API-PARITY-011.expected_shape` now declares nested `sourceRecord` fields.
- `api/v2Backbone.test.ts` now reads `API-PARITY-011` directly and asserts the
  real route response status and nested expected shape.
- `api/v2Backbone.test.ts` now includes an end-to-end missing-report test that
  proves the route returns `503 SHADOW_BACKBONE_SOURCE_UNAVAILABLE`.
- Parity evidence was regenerated after those corrections; the final accepted
  report for this slice is `20260426T052238Z`.
- The first native architect re-review returned `APPROVED` / `CLEAR` before
  the later blank-ID hardening.
- A follow-up native architect review after blank-ID hardening returned
  `REJECTED` because the accepted contract and parity artifact did not yet
  encode the new blank decoded source-ID behavior.
- That follow-up rejection was addressed by:
  - updating the parity contract to document blank decoded source IDs as 400
    client errors,
  - updating the sixteenth-slice packet planned test coverage,
  - adding `API-PARITY-011A` as a first-class invalid source-ID parity case,
  - binding the blank-ID route test to `API-PARITY-011A`, and
  - regenerating fresh 24/24 parity evidence at `20260426T052238Z`.
- A second follow-up native architect review returned `REJECTED` because
  `API-PARITY-011A` existed but the parity runner's required category set did
  not yet enforce `source_invalid_id`.
- That governance rejection was addressed by:
  - adding `source_invalid_id` to the parity runner required category set,
  - adding a runner regression test that removes `source_invalid_id` and
    verifies the runner fails before executing parity commands, and
  - regenerating the final `20260426T052238Z` report so
    `required_case_categories` includes `source_invalid_id`.
- Final native architect re-review returned `APPROVED` with no blocking
  findings after the runner enforcement fix. The approval confirmed that
  `source_invalid_id` is first-class in runner enforcement, `API-PARITY-011A`
  is tied to the route test, the generated report proves the case and required
  category, and the route remains additive/file-backed with no write or cutover
  path.

## Cleanup Pass

AI slop cleanup was scoped to the slice-owned API route, tests, parity fixture,
generated parity report, and state/evidence docs. Behavior was locked by
focused route tests before cleanup. The cleanup pass found no dead code,
duplicated branch, needless abstraction, or boundary leak that justified
additional edits beyond the architect-required evidence fixes.

## Safety Invariants

- No Neo4j writes: no Neo4j write path changed or run.
- No KG rebuild: no reset, rebuild, load, or pipeline command run.
- No protected content ingest: route exposes staged source-rights metadata only
  and tests assert official URLs, blocking notes, intended-use prose, and hidden
  payloads stay absent.
- No source-ID ambiguity: malformed and whitespace-only IDs fail as client
  errors without reading or exposing content payloads.
- No feature flag cutover: no feature flag file changed.
- No Explorer default graph adoption: no Explorer runtime file changed.
- Preview/read-only/shadow-only behavior remains additive under `/v2`.
- Generated artifacts are auditable under
  `006_System-Manifests/aec-mepfs-backbone/parity/20260426T052238Z/`.

## Known Residual Risks

- `integration_rollback_proof_plan` remains a planned warning in the parity
  report; it is not required for this API-only shadow preview slice.
- Runtime integration remains blocked exactly as before.
- Source preview currently covers staged source-rights metadata only; resolver
  traces and document/source admission payloads remain future shadow-only
  surfaces.

## Next Recommended Safe Slice

Choose the next bounded shadow-only/read-only improvement from fresh evidence.
Prefer one of:

- route-backed resolver/trace preview contracts without runtime mutation,
- additional manifest/report hardening,
- Explorer preview-only rendering refinements that do not adopt the default
  graph.
