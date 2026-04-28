# AEC-MEPFS Taxonomy Domain Expansion And Explorer Spacing Packet

```yaml
status: BOUNDARY_APPROVED_IMPLEMENTED
created: 2026-04-28
authority: project-owner-directive-taxonomy-population-and-explorer-usability
scope: rights-safe-file-backed-taxonomy-and-explorer-layout-controls
baseline_commit: df8232d9
run_id: 20260428T053531Z
node_target: 984
edge_target: 960
root_count: 24
l2_count: 240
l3_count: 720
max_depth: 3
gemini_used: false
neo4j_mutation_authorized: false
kg_rebuild_reload_reset_authorized: false
protected_content_ingest_authorized: false
```

## Project-owner decision

The project owner accepted the current AEC-MEPFS taxonomy direction but requested
more domain coverage and better Explorer spacing because the graph still felt
cramped. The requested additions are: Sanitary Engineering, Security systems
(CCTV, electric fences, access control), Smart Systems / IoT / home automation,
Heritage Conservation, and a Laws taxonomy.

This packet authorizes a local, file-backed, rights-safe taxonomy expansion and
Explorer layout-control improvement. It does not authorize protected source
payload ingestion, Neo4j mutation, KG rebuild/reload/reset, production graph
promotion, secret exposure, or copying standards/course/proprietary text into
fixtures or reports.

## Research basis

High-level topic calibration used only non-protected labels and topic families.
No quoted standards, exam content tables, protected course materials, or source
payloads were copied.

- Repo-local research under `.ai/13_research/`, especially AEC taxonomy and laws
  readiness notes.
- NAAB architecture accreditation criteria for architecture history/theory,
  technical, and professional coordination coverage:
  https://www.naab.org/accreditation-criteria
- NCEES civil/engineering licensure specifications for civil, structural,
  environmental, water, electrical/computer, and related engineering families:
  https://ncees.org/exams/pe-exam/civil/
- APA/AICP planning content outline for planning, land use, infrastructure,
  historic/cultural resources, technology, and policy topic families:
  https://www.planning.org/certification/examprep/subjectmatter/
- CEDIA smart-home professional domain framing for smart home technology and
  automation: https://cedia.org/smart-home-professionals/
- ICOMOS heritage conservation framing around cultural significance,
  authenticity, integrity, protection, conservation, and management:
  https://www.icomos.org/world-heritage/

## Allowed scope

- Add rights-safe high-level BackboneNode records for new L1 roots:
  - `SAN` Sanitary Engineering
  - `SEC` Security Systems
  - `SMS` Smart Systems And Automation
  - `HRC` Heritage Conservation
  - `LAW` Laws, Codes, And Governance
- Add 10 L2 topics and 30 L3 subtopics under each new root.
- Preserve all existing path codes and IDs; append new deterministic IDs only.
- Regenerate file-backed shadow staging and consumer reports for run
  `20260428T053531Z`.
- Regenerate route inventory evidence for the same run.
- Add Explorer minimap filter correctness and layout spread control tests.
- Add a user-facing graph spread slider that expands/compresses clustered,
  circular, random, and large-graph force-layout seed positions.

## Blocked scope

- No protected source text, clauses, tables, figures, datasets, or local protected
  caches.
- No Neo4j write/reset/reload/promotion/cleanup.
- No KG rebuild/reload/reset.
- No production graph promotion.
- No broad/global `LIVE_RUNTIME_AUTHORIZED` change.
- No Gemini use.
- No secret, token, credential, database URL, or private connection string output.

## Implementation plan

1. Append the five requested top-level domains to the admitted backbone fixture.
2. Keep every new record admitted, owner-covered, parented, and path-code valid.
3. Regenerate shadow staging, consumer report, route inventory, and Explorer
   performance/interaction evidence for run `20260428T053531Z`.
4. Update API/Explorer/Python tests for 984 nodes, 960 edges, 24 roots, 240 L2,
   and 720 L3 records.
5. Fix minimap snapshots so filtered/hidden nodes are excluded from the minimap.
6. Add graph layout spread control and helper tests.
7. Run focused and broader affected verification.
8. Record validation evidence and commit.

## Completion criteria

- Fixture validates with 984 BackboneNode records and 960 `broader_than`
  relationships.
- New roots `SAN`, `SEC`, `SMS`, `HRC`, and `LAW` are present with 10 L2 and 30
  L3 children each.
- Shadow staging, consumer, and route inventory reports are `ok: true` for run
  `20260428T053531Z`.
- Explorer minimap changes when node-type filters change because the snapshot
  excludes filtered/hidden nodes.
- Explorer exposes a graph spread slider and helper tests prove clamp/radius
  behavior.
- Focused Python/API/Explorer tests pass, followed by broader affected Explorer
  checks.
- Safety checks show no protected ingest, Neo4j mutation, KG reset/reload, or
  unauthorized production/live work.

## Kimi advisory resolution

Kimi review was attempted and returned actionable findings. The accepted fixes are
part of this packet:

- stale Explorer evidence-preview root counts were reconciled from 19 to 24;
- the Explorer spread control now includes an explicit reset-to-default control;
- synthesized taxonomy rows now carry `generation_method` so downstream consumers
  can distinguish steward-governed batch synthesis from individually written
  source payload admissions;
- rollback remains git-revert based for the fixture and UI changes, with the
  previous `20260428T033525Z` evidence run preserved as a historical reference.
