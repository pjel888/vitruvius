# AEC Explorer Improvement Overlay Campaigns

Last updated: 2026-05-13

## Current State

The AEC-MEPFS relationship-improvement workflow now produces two pending-only Explorer overlay classes:

- Relationship improvement edges from accepted and needs-review relationship candidates.
- Node consolidation edges from alias-approved and needs-evidence duplicate/same-concept candidates.

These overlays are review surfaces. They do not mutate the active graph, do not write to Neo4j or Postgres, and do not auto-merge nodes.

## Campaign Archive

| Run ID | Status | Relationship pairs processed | Skipped from ledger | New model calls | Accepted relationships | Relationship review | Rejected relationships | Accepted node consolidations | Node consolidation review | Estimated cloud cost | Ledger saved |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `aec_backbone_all_nodes_bounded_001` | completed | 5,000 | 0 | 5,000 | 240 | 111 | 4,649 | 42 | 740 | $2.164821 | $0.000000 |
| `aec_backbone_all_nodes_bounded_002` | interrupted/error artifact run | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| `aec_backbone_all_nodes_bounded_003` | completed | 15,000 | 5,000 | 15,000 | 1,153 | 844 | 13,003 | 33 | 162 | $4.939353 | $1.646451 |
| `aec_backbone_all_nodes_bounded_004` | completed | 30,000 | 20,000 | 30,000 | 1,579 | 1,178 | 27,243 | 76 | 1,179 | $12.260028 | $8.173352 |

The best current Explorer overlay source is:

`006_System-Manifests/aec-mepfs-backbone/semantic-overlays/aec_backbone_all_nodes_bounded_004/`

Key review artifacts:

- `relationship-improvement-report.json`
- `relationship-improvement-summary.txt`
- `accepted-relationships-review.tsv`
- `rejected-relationships-review.tsv`
- `node-consolidation-review.tsv`
- `relationship-admission-ready.jsonl`
- `relationship-admission-review-required.jsonl`
- `node-consolidation-steward-actions.jsonl`
- `bulk-pending-resolution-decisions.nobom.tsv`
- `pending-resolution-decisions.jsonl`
- `pending-resolution-decision-manifest.json`

## Explorer Overlay States

Explorer renders these pending overlay edge states distinctly:

- `PENDING_RELATIONSHIP_STEWARD_APPROVED`: relationship candidate has passed deterministic audit and recorded steward review for staged admission packet work.
- `PENDING_RELATIONSHIP_NEEDS_EVIDENCE`: relationship candidate should stay visible but needs more support before admission.
- `PENDING_NODE_CONSOLIDATION_ALIAS_APPROVED`: node pair is safe for alias-only review visibility, not an automatic merge.
- `PENDING_NODE_CONSOLIDATION_NEEDS_EVIDENCE`: node pair is useful to inspect but needs more evidence or steward review before any consolidation action.

The edge inspector should show the source run, decision state, rationale, evidence, confidence/similarity, and provider/model metadata.

## Explorer Review Workflow

Use Explorer as the inspection surface for campaign outputs, not as an admission surface:

1. Open the AEC-MEPFS backbone preview rail.
2. Use the sparkle control to load pending relationship and node-consolidation overlays.
3. Use the overlay quick filters for approved-only, needs-evidence, relationship-only, node-consolidation-only, or all overlay views.
4. Use the source-gap control to load graph-wide source/resource gaps.
5. Filter source gaps by `All`, `Nodes`, or `Relationships`.
6. Expand a source-gap row to inspect matched terms, suggested existing Resources, proposal rationale, and target node/edge IDs.
7. Jump from relationship source-gap rows to either endpoint with the `From` / `To` controls.
8. In Node Inspector, use the Overview source-gap callout or the `Context` tab to inspect node-specific source-link proposals.

These controls are intentionally review-only. They do not approve relationships, merge nodes, create Resource Layer links, admit source claims, mutate active graph files, or write to Neo4j/Postgres.

## Source-Grounded Context Packet

The Explorer now also exposes a read-only source-grounded context packet for selected AEC nodes:

- API: `POST /v2/answer/context`
- Node detail: `GET /node/<AEC_NODE_ID>` includes `sourceGroundedContext`
- Explorer UI: Node Inspector -> `Context`
- CLI inventory: `python scripts/pipeline_cli.py aec-source-grounding-inventory --relationship-run-id latest`

This packet separates source-backed paths, admitted/domain-synthesis graph paths, and proposal-only overlay paths. It includes learner-safe resource metadata and evidence selectors only; it does not include protected source text and does not admit pending overlay records into the active graph.

The current smoke inventory is stored at:

`006_System-Manifests/aec-mepfs-backbone/source-grounding-inventory/SOURCE_GROUNDING_SMOKE/`

Reported coverage from that smoke run:

- 10,018 nodes
- 13,670 governed relationships
- 8 source-backed nodes
- 4,344 source-backed relationships
- 2,757 pending relationship overlay records
- 1,255 pending node-consolidation overlay records

The inventory command also writes proposal-only source/resource gap artifacts:

- `source-grounding-gap-workqueue.jsonl`: ranked nodes and relationships that need source/resource review.
- `source-link-proposals.jsonl`: deterministic candidate links from existing Resource Layer metadata.

These files are review queues only. They do not create Resources, do not create NodeResourceLinks, do not admit graph edges, and do not write to Neo4j or Postgres. Use them to decide which source-link admission packets are worth preparing next.

Explorer surfaces these artifacts in two places:

- A graph-wide Source gaps panel in the AEC-MEPFS rail.
- A node-specific Source Gap Workqueue panel in Node Inspector -> `Context`.

Both surfaces show bounded, sanitized previews only. They include Resource metadata, matched terms, target IDs, proposal rationale, and safety flags, but never protected source text.

## Use Case: RA 9266 Change Review

When reviewing a law or standards node such as `RA 9266`, the Explorer can act like a version-control impact map for the knowledge graph:

1. Select the law or standards node.
2. Inspect related role, practice, jurisdiction, document, compliance, and project nodes.
3. Turn on approved relationship overlays to see candidate paths that are likely ready for admission packet work.
4. Turn on needs-evidence overlays to see the records that should not be admitted yet but may need source review.
5. Use the edge inspector to check rationale, evidence, confidence, and provider/model provenance before any steward action.

This keeps graph edits reviewable before changing canonical records.

## Use Case: Materials And Maintenance Review

The same workflow applies to materials, assemblies, assets, and maintenance concepts:

1. Select a material, assembly, asset, or maintenance node.
2. Inspect connected standards, lifecycle phases, handoff records, risk flags, and operations/maintenance concepts.
3. Use node-consolidation overlays to find duplicate or near-duplicate material and maintenance terms.
4. Use relationship overlays to find missing governance, requirement, evidence, or taxonomy relationships.
5. Keep needs-evidence items in the review queue until a steward can add source-backed support.

This helps turn large discovery campaigns into a practical review queue without treating AI output as admitted truth.

## Safety Boundary

The campaign outputs remain pending-only. The Explorer can display them and help the operator inspect them, but active graph mutation remains blocked by the admission workflow and the `--apply` rejection boundary.
