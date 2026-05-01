# PRD: AEC-MEPFS Shadow Completion Loop

## Goal

Continue safe AEC-MEPFS Backbone work by shipping bounded shadow-only/read-only
slices that improve evidence, parity, preview safety, and QA without promoting
the backbone to the live graph.

## Non-Goals

- Do not write Neo4j.
- Do not rebuild or load the operational KG.
- Do not ingest protected source content.
- Do not make feature flags default-on.
- Do not adopt the AEC-MEPFS preview as the Explorer default graph.
- Do not touch high-impact runtime roots without a separate accepted packet.

## Current Slice

Eighth shadow slice: parity runner hardening for the existing shadow graph and
`/v2/backbone/taxonomy` preview.

## Requirements

- Add mandatory parity categories for:
  - shadow backbone summary route,
  - shadow taxonomy/graph preview route,
  - shadow graph fail-closed behavior,
  - Explorer opt-in preview isolation.
- Register only explicit allowed commands; do not use arbitrary shell
  execution.
- Keep the parity runner file-backed and read-only.
- Generate a fresh parity report under
  `006_System-Manifests/aec-mepfs-backbone/parity/`.
- Update planning/state/evidence docs with the changed readiness status.
- Attempt Gemini and Kimi advisory review for the diff or slice plan; log
  findings or availability issues.

## Acceptance Criteria

- Focused Python parity runner tests pass.
- The parity runner successfully writes a fresh report with all required cases
  passed.
- Affected API and Explorer test commands pass.
- Evidence log confirms all safety invariants.
- GitNexus impact/detect evidence is collected or the unavailable state is
  documented.
- Changes are committed and pushed before selecting the next slice.
