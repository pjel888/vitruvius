# First Graph Admission Queue

Date: 2026-05-02T09:55:00Z

This queue is advisory unless a specific scoped approval/admission record exists. P1 reviews remain advisory metadata; Kimi review is not approval. No merge, alias, redirect, tombstone, fake source, or Resource Layer mutation is authorized by this queue.

## 1. Already admitted / consumed by admission

- `p1-decision-packet-fee6fbd9a0fc` / `dup-ca1078594013` - building - nodes `VTN-DOM-0000716, VTN-DOM-0000757` - status `kimi_reviewed` - action `governed_disambiguation_candidate` - risk `medium` - packet state `metadata_disambiguation_admitted`
- `p1-decision-packet-d5a20759fdfd` / `dup-6400e3e0c204` - shallow foundation - nodes `VTN-DOM-0000261, VTN-DOM-0003010` - status `kimi_reviewed` - action `cross_domain_alignment_candidate` - risk `medium` - packet state `consumed_by_non_destructive_admission`
- `p1-decision-packet-8a66e785d02a` / `dup-5c6457d515c1` - deep foundation - nodes `VTN-DOM-0000262, VTN-DOM-0003013` - status `kimi_reviewed` - action `cross_domain_alignment_candidate` - risk `medium` - packet state `consumed_by_non_destructive_admission`

## 2. Ready for non-destructive admission review

- No new P1 packet from the four completed reviews passed admission gates in this run. Existing newly reviewed packets remain advisory keep-separate/governed-disambiguation or edge-neighborhood review candidates.

## 3. Relationship-enrichment candidates

- `p1-decision-packet-14c7a87c4441` / `dup-7d1cf0e582ce` - space syntax cue - nodes `VTN-DOM-0005289, VTN-DOM-0005295, VTN-DOM-0005301` - status `kimi_reviewed` - action `needs_edge_neighborhood_review` - risk `medium` - packet state `not_admitted`

## 4. Keep-separate / governed-disambiguation candidates

- `p1-decision-packet-eaebb01d3604` / `dup-7a43f7bf68ed` - door hardware usability - nodes `VTN-DOM-0004631, VTN-DOM-0004637, VTN-DOM-0004643, VTN-DOM-0004649` - status `kimi_reviewed` - action `record_advisory_keep_separate_metadata_only` - risk `medium` - packet state `not_admitted`
- `p1-decision-packet-cf24f7d51a8e` / `dup-ffcce92d5e84` - humidity resistant material - nodes `VTN-DOM-0005331, VTN-DOM-0005337, VTN-DOM-0005343, VTN-DOM-0005349` - status `kimi_reviewed` - action `record_advisory_keep_separate_metadata_only` - risk `medium` - packet state `not_admitted`
- `p1-decision-packet-26f00d4bf4c6` / `dup-b7032a0f24c3` - material reuse strategy - nodes `VTN-DOM-0005305, VTN-DOM-0005311, VTN-DOM-0005317, VTN-DOM-0005323` - status `kimi_reviewed` - action `record_advisory_keep_separate_metadata_only` - risk `medium` - packet state `not_admitted`
- `p1-decision-packet-55f26dda8b24` / `dup-47284b85f39a` - material transition joint - nodes `VTN-DOM-0004860, VTN-DOM-0004866, VTN-DOM-0004872, VTN-DOM-0004878` - status `kimi_reviewed` - action `record_advisory_keep_separate_metadata_only` - risk `medium` - packet state `not_admitted`
- `p1-decision-packet-2929eb94bf83` / `dup-ea9ec467eac1` - room data sheet - nodes `VTN-DOM-0005166, VTN-DOM-0005172, VTN-DOM-0005178, VTN-DOM-0005184` - status `kimi_reviewed` - action `record_advisory_keep_separate_metadata_only` - risk `medium` - packet state `not_admitted`
- `p1-decision-packet-a2815b94c60e` / `dup-2db283685d10` - street wall continuity - nodes `VTN-DOM-0005417, VTN-DOM-0005423, VTN-DOM-0005429, VTN-DOM-0005435` - status `kimi_reviewed` - action `record_advisory_keep_separate_metadata_only` - risk `medium` - packet state `not_admitted`
- `p1-decision-packet-172d3ad16eb1` / `dup-1c35a40aa1b7` - toilet room clearance - nodes `VTN-DOM-0004632, VTN-DOM-0004638, VTN-DOM-0004644, VTN-DOM-0004650` - status `kimi_reviewed` - action `record_advisory_keep_separate_metadata_only` - risk `medium` - packet state `not_admitted`
- `p1-decision-packet-74811455ff28` / `dup-1a5ed6894130` - ventilated roof cavity - nodes `VTN-DOM-0005328, VTN-DOM-0005334, VTN-DOM-0005340, VTN-DOM-0005346` - status `kimi_reviewed` - action `governed_disambiguation_candidate` - risk `medium` - packet state `not_admitted`
- `p1-decision-packet-be194427b107` / `dup-a8be2c4e5b91` - facade maintenance access - nodes `VTN-DOM-0004977, VTN-DOM-0004983, VTN-DOM-0004989` - status `kimi_reviewed` - action `record_advisory_keep_separate_metadata_only` - risk `medium` - packet state `not_admitted`
- `p1-decision-packet-f3330c711714` / `dup-b4adf3c34e1a` - room identification logic - nodes `VTN-DOM-0005467, VTN-DOM-0005473, VTN-DOM-0005479` - status `kimi_reviewed` - action `governed_disambiguation_candidate` - risk `medium` - packet state `not_admitted`
- `p1-decision-packet-74dbf34edf8b` / `dup-d0194612095a` - threshold and transition space - nodes `VTN-DOM-0005288, VTN-DOM-0005294, VTN-DOM-0005300` - status `kimi_reviewed` - action `governed_disambiguation_candidate` - risk `medium` - packet state `not_admitted`

## 5. Alias-only candidates

- None currently queued. Kimi mentioned possible alias pressure for Room Identification Logic, but this run rejected alias action because no alias-specific dry-run/source/UX gate was performed.

## 6. Needs edge-neighborhood review

- `p1-decision-packet-0cfa6a7f88a1` / `dup-79f6cd2af6bf` - wall finishe - nodes `VTN-DOM-0000513, VTN-DOM-0003441, VTN-DOM-0012156` - status `human_review_needed` - action `needs_edge_neighborhood_review` - risk `high` - packet state `not_admitted`
- `p1-decision-packet-fa4918982178` / `dup-a403cae6e1ea` - mat foundation - nodes `VTN-DOM-0000263, VTN-DOM-0003016, VTN-DOM-0012278` - status `human_review_needed` - action `needs_edge_neighborhood_review` - risk `high` - packet state `not_admitted`
- `p1-decision-packet-9d2ac282265b` / `dup-db832ee203d2` - shear wall - nodes `VTN-DOM-0000265, VTN-DOM-0012270` - status `human_review_needed` - action `needs_edge_neighborhood_review` - risk `high` - packet state `not_admitted`

## 7. Needs source/resource review

- `p1-decision-packet-3946860e327a` / `dup-621135f7b4b9` - load path - nodes `VTN-DOM-0002932, VTN-DOM-0012160` - status `human_review_needed` - action `needs_human_review` - risk `high` - packet state `not_admitted`
- `p1-decision-packet-12e81a4fbcde` / `dup-b2f8807aa183` - retaining wall - nodes `VTN-DOM-0003026, VTN-DOM-0012272` - status `human_review_needed` - action `needs_source_review` - risk `high` - packet state `not_admitted`

## 8. High-risk blocked

- `p1-decision-packet-3946860e327a` / `dup-621135f7b4b9` - load path - nodes `VTN-DOM-0002932, VTN-DOM-0012160` - status `human_review_needed` - action `needs_human_review` - risk `high` - packet state `not_admitted`
- `p1-decision-packet-0cfa6a7f88a1` / `dup-79f6cd2af6bf` - wall finishe - nodes `VTN-DOM-0000513, VTN-DOM-0003441, VTN-DOM-0012156` - status `human_review_needed` - action `needs_edge_neighborhood_review` - risk `high` - packet state `not_admitted`
- `p1-decision-packet-fa4918982178` / `dup-a403cae6e1ea` - mat foundation - nodes `VTN-DOM-0000263, VTN-DOM-0003016, VTN-DOM-0012278` - status `human_review_needed` - action `needs_edge_neighborhood_review` - risk `high` - packet state `not_admitted`
- `p1-decision-packet-9d2ac282265b` / `dup-db832ee203d2` - shear wall - nodes `VTN-DOM-0000265, VTN-DOM-0012270` - status `human_review_needed` - action `needs_edge_neighborhood_review` - risk `high` - packet state `not_admitted`
- `p1-decision-packet-12e81a4fbcde` / `dup-b2f8807aa183` - retaining wall - nodes `VTN-DOM-0003026, VTN-DOM-0012272` - status `human_review_needed` - action `needs_source_review` - risk `high` - packet state `not_admitted`

## 9. Rejected / false positive

- None.

## 10. Deferred

- Space Syntax Cue is deferred for relation/property modeling review before any graph admission.

## Exact next action

Run a focused relation-vocabulary/source-context review for the next ACS candidate batch, then inspect Shear Wall and Retaining Wall with source-context evidence before any admission attempt.


---

## Phase 3 MVP Graph Enrichment Update - 2026-05-02T10:24:13Z

- P1 review backlog remains complete: 20/20 reviewed.
- Admitted 12 additional ACS overlays under scoped approval `canonical-approval-20260502102405-baf8f5958e7d`.
- Total active admitted relationships: 26.
- Effective graph edges: 13,696; base graph edges remain 13,670.
- P1 packet custody rebased via `canonical-tx-20260502102405-c20aaacb8002`.
- No merge, alias, redirect, tombstone, Resource Layer mutation, fake source, AHJ/code/numerical claim, or protected payload.
- High-risk Shear Wall remains blocked; deferred Kimi-source candidates moved to next queue.
