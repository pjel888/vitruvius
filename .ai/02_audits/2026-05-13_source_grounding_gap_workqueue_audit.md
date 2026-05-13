# Source Grounding Gap Workqueue Audit

Date: 2026-05-13

## Audit Finding

The current source-grounding inventory is safe and useful, but it is still mostly diagnostic. It reports coverage and example gaps, yet does not provide a ranked operator queue that connects each gap to existing Resource metadata.

## Blast Radius

Expected touched files:

- `scripts/vitruvius/kg/source_grounding_inventory.py`
- `scripts/pipeline_cli.py`
- `scripts/tests/test_kg_source_grounding_inventory.py`
- source-grounded roadmap/docs/state files

No active graph fixture, Resource Layer registry, Neo4j, Postgres, or protected payload file should be modified.

## Risks

- Candidate Resource proposals could be mistaken for admitted source truth.
- Token matching can over-rank broad resources if not clearly labeled as proposal-only.
- Relationship source gaps need care: hierarchy and high-impact predicates should be prioritized differently.
- Existing Resource metadata is sparse, so the workqueue must state that proposal quality is bounded by available resources.

## Controls

- Write only to the selected inventory output directory.
- Every workqueue item and proposal record includes `auto_admit: false`, `active_graph_mutation: false`, and `resource_layer_mutation: false`.
- Report and summary text explicitly call the artifacts review queues.
- Tests assert no input graph or Resource Layer registry mutation.
- Tests assert no API key markers or `reasoning_content` appear.

## Audit Conclusion

Proceed with a deterministic proposal-only workqueue attached to `aec-source-grounding-inventory`. Do not create an admission or mutation command in this slice.
