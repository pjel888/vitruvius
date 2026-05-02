# P1 Packet Ontology Review Run Report

Date: 2026-05-02T09:55:00Z

## Summary

- P1 packets total: 20
- P1 packets reviewed: 20
- P1 packets unreviewed: 0
- Kimi-reviewed: 15
- Human-review-needed / high-risk blocked: 5
- New reviews this run: 4
- Graph mutation from review metadata alone: none

## New reviews this run

- `p1-decision-packet-74811455ff28` / `dup-1a5ed6894130` - ventilated roof cavity - nodes `VTN-DOM-0005328, VTN-DOM-0005334, VTN-DOM-0005340, VTN-DOM-0005346` - status `kimi_reviewed` - action `governed_disambiguation_candidate` - risk `medium` - packet state `not_admitted`
  - Kimi summary: Ventilated Roof Cavity appears in multiple ARC.TAC parent contexts (moisture/material response, natural ventilation, solar/shading, thermal mass). The repeated label may be a reusable roof-cavity concept, but the parent paths encode distinct design concerns and the packet has empty edge-neighborhood evidence. Preserve as governed-disambiguation / keep-separate metadata for now rather than merge, alias, or visible edge mutation.
- `p1-decision-packet-f3330c711714` / `dup-b4adf3c34e1a` - room identification logic - nodes `VTN-DOM-0005467, VTN-DOM-0005473, VTN-DOM-0005479` - status `kimi_reviewed` - action `governed_disambiguation_candidate` - risk `medium` - packet state `not_admitted`
  - Kimi summary: Room Identification Logic repeats under accessible, directional, and identification wayfinding contexts. Kimi considered it a likely shared wayfinding logic, but local governance treats the taxonomy-parent difference and empty edge-neighborhood evidence as insufficient for aliasing. Preserve as a governed-disambiguation / keep-separate advisory item pending explicit equivalence evidence.
- `p1-decision-packet-14c7a87c4441` / `dup-7d1cf0e582ce` - space syntax cue - nodes `VTN-DOM-0005289, VTN-DOM-0005295, VTN-DOM-0005301` - status `kimi_reviewed` - action `needs_edge_neighborhood_review` - risk `medium` - packet state `not_admitted`
  - Kimi summary: Space Syntax Cue repeats across adjacency, circulation, and progression contexts. Kimi flagged that cue may be underspecified and could behave like a relationship/property rather than a standalone taxonomy node. Empty edge neighborhoods and no resources make canonical identity unsafe. Keep separate and request taxonomy/edge-neighborhood review.
- `p1-decision-packet-74dbf34edf8b` / `dup-d0194612095a` - threshold and transition space - nodes `VTN-DOM-0005288, VTN-DOM-0005294, VTN-DOM-0005300` - status `kimi_reviewed` - action `governed_disambiguation_candidate` - risk `medium` - packet state `not_admitted`
  - Kimi summary: Threshold And Transition Space repeats across adjacency, circulation, and progression contexts. Kimi viewed threshold/transition as a plausible distinct spatial type, but the repeated taxonomy placements still need governed disambiguation before canonical placement changes. Preserve separate nodes pending semantic equivalence and placement review.

## Kimi accepted / rejected / deferred

- Accepted: classify the four remaining packets as advisory review-only candidates rather than merge candidates.
- Rejected: no alias, merge, redirect, tombstone, or graph edge was applied from these reviews.
- Deferred: Space Syntax Cue needs edge-neighborhood/modeling review; Room Identification Logic alias pressure is deferred to a future alias-specific dry-run.

## Custody

- After second ACS admission, all 20 P1 packet snapshots were rebased and all 20 reviews were carried forward via `canonical-tx-20260502094802-f4fdf2cf8f1f`.
- Packet content hash mismatches: 0
- Stale packet snapshots: 0
- Stale review records: 0
