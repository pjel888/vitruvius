# AEC-MEPFS Explorer Default Adoption Packet

```yaml
status: BOUNDARY_APPROVED_PREP_ONLY
created: 2026-04-27
authority: project-owner-directive-four-gated-lanes
lane: explorer-default-adoption
classification: GREEN_PREP_AND_REGRESSION_PROOF_ONLY
baseline_commit: fd307465
explorer_default_adoption_enabled: false
```

## 1. Purpose

Complete the repo-actionable Explorer default-adoption prerequisites without
silently switching the current Explorer default graph. This packet defines UX
criteria, rollback requirements, regression proof, and an auditable preflight
report that confirms the current MVP default remains legacy `default` while the
AEC-MEPFS Backbone preview remains explicit opt-in.

## 2. Authority and baseline

- Umbrella packet: `2026-04-27_four_gated_lanes_reopen_packet.md`.
- Current Explorer behavior: `/explore` defaults to `perspective=default`, which
  is omitted from the URL and backed by `/perspective/default/nodes`.
- Current AEC-MEPFS behavior: preview panel fetches `/v2/backbone*` only after
  explicit user toggle/clicks.

## 3. UX acceptance criteria for future adoption

Default adoption may be implemented only if all are true:

1. The adopted default behavior is explicitly named and testable.
2. A user-visible escape or selector preserves access to the current `default`
   graph.
3. `/explore` URL behavior and saved scenes remain reversible.
4. AEC-MEPFS preview/API payloads are adapted to Explorer `GraphNode[]` and
   `GraphEdge[]` before they replace graph state.
5. No protected payloads appear in Explorer graph state, preview panels, tests,
   or generated reports.
6. API parity and route inventory evidence is fresh for the adoption diff.
7. Tests prove old behavior can be restored or disabled.

## 4. Allowed scope in this packet

- Add a default-adoption preflight reporter.
- Add tests that lock current MVP default behavior and opt-in preview behavior.
- Generate an evidence report under
  `006_System-Manifests/aec-mepfs-backbone/explorer-default-adoption/<RUN_ID>/`.
- Document rollback/escape requirements.

## 5. Explicitly blocked scope

- Silent default graph switch.
- Automatic AEC preview fetch on `/explore` load.
- Replacing graph state with preview payloads before an adapter exists.
- Protected payload exposure.
- Neo4j/KG mutation.
- Default-on feature flags.
- Broad/global `LIVE_RUNTIME_AUTHORIZED`.

## 6. Implementation plan

1. Add `scripts/vitruvius/kg/backbone_explorer_default_adoption.py`.
2. Add `scripts/tests/test_kg_backbone_explorer_default_adoption.py`.
3. Strengthen Explorer integration tests for `/explore` and HomeScreen default
   entry behavior.
4. Generate a preflight report proving default adoption is currently gated off.

## 7. Verification commands

```bash
python3 -m compileall -q scripts/vitruvius/kg/backbone_explorer_default_adoption.py
PYTHONPATH=scripts python3 -m pytest scripts/tests/test_kg_backbone_explorer_default_adoption.py -q
(cd explorer && bun test app.searchInspector.integration.test.tsx)
(cd explorer && bun test app.searchInspector.integration.test.tsx components/componentInteraction.test.tsx api/graphApi.test.ts)
```

## 8. Evidence artifacts

- Preflight report:
  `006_System-Manifests/aec-mepfs-backbone/explorer-default-adoption/<RUN_ID>/explorer-default-adoption-report.json`
- Validation log:
  `.ai/05_logs/2026-04-27_aec_mepfs_explorer_default_adoption_validation.md`

## 9. Completion criteria for this packet

- Preflight reporter and tests pass.
- Explorer regression tests prove current default behavior remains unchanged.
- Generated evidence says `defaultAdoptionReady=false` and
  `explorerDefaultAdoptionEnabled=false` until a later adoption implementation
  packet provides the graph adapter, UX selector/escape path, and fresh parity.
- No Explorer default behavior changes are introduced in this prep packet.

## 10. Next boundary

Actual Explorer default adoption remains `UNSATISFIED_YELLOW` until the future
implementation packet defines and tests the graph adapter and migration/escape
UX. This packet completes the no-behavior-change repo-actionable preparation and
regression evidence.
