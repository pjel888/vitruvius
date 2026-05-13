# Source-Grounded Explorer Context Implementation Plan

Date: 2026-05-13

## Goal

Add a no-write source-grounding inventory and Explorer-visible `SourceGroundedAnswerContext` so campaign outputs can be inspected as graph proposals while source coverage gaps remain explicit.

## Plan

1. Add `scripts/vitruvius/kg/source_grounding_inventory.py`.
   - Read active AEC backbone fixture.
   - Read resource-layer registries.
   - Optionally read latest or selected semantic overlay run.
   - Classify nodes and relationships as `source_backed`, `domain_synthesis`, `proposal_only`, or `unsupported`.
   - Write report and summary under a dedicated source-grounding inventory folder only.

2. Wire CLI command `aec-source-grounding-inventory`.
   - Keep imports lazy.
   - Print JSON summary.
   - Do not write active graph files.

3. Add API context contract and endpoint.
   - `POST /v2/answer/context`.
   - Build context from AEC graph, optional pending overlay graph, and resource-layer metadata.
   - Return graph paths, resource references, evidence selectors, coverage summary, and safety boundaries.

4. Add Explorer display.
   - Add source-grounded context types.
   - Add a compact Context tab in `NodeInspector`.
   - Show source-backed/pending/domain-synthesis counts and resource/evidence selectors.

5. Validate.
   - Python inventory tests.
   - CLI parse smoke.
   - API tests for context endpoint.
   - Explorer component/type tests.
   - Compile Python and run targeted frontend tests.

## Critique

- Do not label pending overlay edges as admitted facts.
- Do not quote protected source text or raw model output.
- Keep the first API contract small and deterministic; answer generation belongs in a later step.
- If source support is ambiguous, report a gap instead of upgrading the claim.

## Execution Checklist

- [x] Inventory module added.
- [x] CLI wired.
- [x] API context endpoint added.
- [x] Explorer context tab added.
- [x] Tests added and passing.
- [x] `.ai` state reconciled.
- [x] No active graph mutation.
