# Source Grounding Gap Workqueue Research

Date: 2026-05-13

## Research Sources

- `AGENTS.md`
- `.ai/01_roadmap/current-phase.md`
- `.ai/01_roadmap/milestone-tracker.md`
- `.ai/01_roadmap/master-roadmap.md`
- `.ai/ACTIVE_WORK.md`
- `.ai/STRATEGIC_NEXT_MOVE.md`
- `.ai/14_project_management/source_grounded_kg_ai_goal_tracker.md`
- `scripts/vitruvius/kg/source_grounding_inventory.py`
- `scripts/pipeline_cli.py`
- `scripts/tests/test_kg_source_grounding_inventory.py`
- `006_System-Manifests/resource-layer/resources.json`
- `006_System-Manifests/resource-layer/node-resource-links.json`
- `006_System-Manifests/aec-mepfs-backbone/source-grounding-inventory/SOURCE_GROUNDING_SMOKE/source-grounding-inventory-report.json`

## Current Behavior

`aec-source-grounding-inventory` reads the AEC backbone, Resource Layer registries, and an optional relationship-improvement overlay. It writes a no-write report and text summary. The report classifies nodes and relationships as `source_backed`, `domain_synthesis`, or `unsupported`, and includes bounded examples of nodes and relationships that lack accepted source support.

## Observed Gap

The inventory proves that most nodes do not yet have accepted Resource Layer links. It does not yet turn those gaps into an actionable workqueue. Operators currently have to inspect examples manually and infer which existing resources may be good candidates.

## Available Deterministic Inputs

- Node labels, preferred labels, aliases, path codes, review status, and definitions where present.
- Relationship from/predicate/to records plus source family IDs where present.
- Existing Resource metadata: title, organization, publisher, resource type, authority, authority tier, discipline tags, taxonomy tags, keywords, abstract/summary, verification status, source family IDs, and access type.
- Existing accepted node-resource links and supported edge IDs.
- Pending overlay run counts for context.

## Constraints

This work must remain proposal-only. It cannot create Resources, NodeResourceLinks, evidence claims, graph edges, graph nodes, aliases, redirects, tombstones, Neo4j writes, or Postgres writes.

## Design Implication

The next safe improvement is deterministic scaffolding:

1. Build token overlap candidates between graph nodes/relationship endpoints and existing Resource metadata.
2. Rank source gaps by answer impact and relationship predicate risk.
3. Write review workqueue JSONL and source-link proposal JSONL under the inventory output directory.
4. Include explicit no-write/no-admission flags on every artifact.

## Tooling Notes

The pre-edit code-intelligence refresh completed, but code-review-graph still reported missing `tree-sitter-yaml` warnings and embedding failures on oversized campaign logs. GitNexus impact lookup for `run_source_grounding_inventory` returned `UNKNOWN` because the module is not yet tracked as an indexed symbol. Blast radius is bounded by the CLI command and the focused test module.
