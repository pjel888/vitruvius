# High-Risk P1 Edge Neighborhood Review Report

Date: 2026-05-02T10:24:13Z

## Shear Wall review update

Packet: `p1-decision-packet-9d2ac282265b` / group `dup-db832ee203d2`.

Nodes:
- `VTN-DOM-0000265` Shear Walls, `STR.SEI.WAL`, subtopic under Seismic Design. Edges: hierarchy children for load path behavior, member sizing, connection/detailing, serviceability/deflection, inspection/retrofit.
- `VTN-DOM-0012270` Shear Wall, `ARC.BLD.STR.SHW`, concept under Structural Coordination Basics. Edges: incoming `HAS_FACET` from Reinforced Concrete, incoming `REQUIRES` from Lateral Stability, outgoing `MAPS_TO_EXTERNAL_STANDARD` to CHED architecture curriculum metadata.

Result: remains high-risk blocked.

Reasoning:
- Taxonomy scopes differ: STR seismic design topic versus ARC building-element/coordination concept.
- Existing edge neighborhoods indicate related but non-identical roles.
- Directionality for any future `RELATED_SPECIALIZATION_OF` or cross-domain relationship is still not proven.
- There is standards/curriculum metadata on the ARC node; no source-specific scope review was performed.

Kimi status:
- Prior Kimi review already classified this as high-risk/human-review-needed and rejected merge/alias/equivalence/immediate admission.
- The fresh Kimi second-pass prompt timed out; no downgrade was accepted.

Next safe action: prepare a source/scope packet for Shear Wall directionality and edge-neighborhood meaning before any future non-destructive admission.


## Phase 4 Wave 1 Retaining Wall Source-Scope Review (2026-05-02T11:25:29Z)

Subagent Mencius performed read-only inspection of `p1-decision-packet-12e81a4fbcde` / `dup-b2f8807aa183`.

Verdict: do not downgrade now; Retaining Wall remains high-risk blocked.

Findings:
- `VTN-DOM-0003026` Retaining Walls is a GEO subtopic under `GEO.RSS.REW` with retaining-wall child topics.
- `VTN-DOM-0012272` Retaining Wall is an ARC concept under `ARC.BLD.STR.RTW` with a `MAPS_TO_EXTERNAL_STANDARD` edge to CHED curriculum metadata.
- Packet risk remains driven by different node roles, different taxonomy contexts, and unresolved source/scope risk.
- Resource Layer links for these packet nodes: 0; no Resource Layer rewrite risk, but also no source-backed relationship evidence.
- No target-touching `HAS_FACET` or `REQUIRES` evidence justifies stronger semantics.

Future conditional path: only after confirming the CHED metadata edge is non-governing curriculum context, a future reciprocal `CROSS_DOMAIN_ALIGNMENT` preview may be considered as navigation/alignment only, not identity, merge, alias, source truth, standard authority, AHJ claim, or code compliance.
