# AEC-MEPFS Taxonomy L3 Expansion Packet

```yaml
status: BOUNDARY_APPROVED
created: 2026-04-28
authority: project-owner-directive-taxonomy-population
scope: rights-safe-file-backed-aec-mepfs-taxonomy-population
baseline_commit: 5d299e51
run_id: 20260428T033525Z
node_target: 779
edge_target: 760
root_count: 19
l2_count: 190
l3_count: 570
max_depth: 3
gemini_used: false
neo4j_mutation_authorized: false
kg_rebuild_reload_reset_authorized: false
protected_content_ingest_authorized: false
```

## 1. Project-owner decision

The project owner accepted the AEC-MEPFS-first Explorer setup but rejected the
remaining sparse skeleton as insufficient. The requested direction is to populate
the AEC-MEPFS backbone with a substantially more comprehensive general topic and
subtopic taxonomy, informed by repo research, public professional education
structures, accreditation/licensure structures, and course-outline style domain
coverage.

This packet authorizes a **file-backed, rights-safe taxonomy expansion**. It does
not authorize copying protected standard text, standards tables, protected course
materials, licensed classification tables, Neo4j/live graph mutation, KG
rebuild/reload/reset, production graph promotion, or protected payload exposure.

## 2. Inputs and research basis

Repo-local research inputs inspected:

- `.ai/13_research/governed taxonomy/deep-research-report.md`
- `.ai/13_research/AECMEPFS++/deep-research-report.md`
- `.ai/13_research/AEC-ECS-SC-References/Hardcoding the AEC Ontology.md`
- `.ai/13_research/AEC-ECS-SC-References/Spatial Comprehension.md`

Public reference families used only for high-level topic calibration:

- NAAB architecture accreditation conditions and criteria:
  https://www.naab.org/accreditation-criteria
- NCARB ARE division structure and guidelines:
  https://www.ncarb.org/publications/are-5-guidelines
- ABET engineering accreditation criteria:
  https://www.abet.org/accreditation/accreditation-criteria/criteria-for-accrediting-engineering-programs-2026-2027/
- APA/AICP planning content outline:
  https://www.planning.org/certification/examprep/subjectmatter/
- ASHRAE handbook volume structure:
  https://www.ashrae.org/technical-resources/ashrae-handbook
- SFPE fire protection education/core-competency references:
  https://www.sfpe.org/advocacy-qualifications/higher-education/modelcurr
- CSI MasterFormat overview as a work-results/specification organizing
  reference, not as copied division/table content:
  https://www.csiresources.org/csiredesign/standards/masterformat

## 3. Allowed scope

- Expand the admitted AEC-MEPFS backbone fixture with original high-level topic
  labels, definitions, aliases, and path codes.
- Keep the existing 19 L1 roots and all existing IDs stable.
- Increase each L1 root to 10 L2 topics and 30 L3 subtopics.
- Preserve deterministic `broader_than` parent-child relationships.
- Regenerate file-backed shadow staging, consumer report, and route inventory
  evidence for the expanded graph.
- Update API and Explorer tests that assert graph counts, depth, node-detail
  relationship counts, and search totals.
- Add API-facing Explorer performance smoke evidence for the expanded graph.
- Update validation/state docs so Explorer expectations match the denser graph.

## 4. Blocked scope preserved

- No protected source text/table/figure/dataset/clause ingestion or exposure.
- No copying of standards tables, licensed classification tables, or protected
  course materials into fixtures, logs, reports, API responses, or Explorer.
- No Neo4j write/reset/reload/promotion/cleanup.
- No KG rebuild/reload/reset against primary graph surfaces.
- No production graph promotion.
- No broad/global `LIVE_RUNTIME_AUTHORIZED` change.
- No secret/environment printing.

## 5. Implementation plan

1. Expand `scripts/tests/fixtures/aec_mepfs_backbone/admitted_backbone_nodes_l1_l2.json`
   from the sparse 114-node L1/L2 skeleton into a 779-node L1/L2/L3 backbone.
2. Preserve fixture schema constraints: stable `VTN-DOM-*` IDs, semver
   `release_version`, admitted review status, one primary parent, path-code
   regex compatibility, and level/path-code consistency.
3. Regenerate shadow staging and consumer reports for `20260428T033525Z`.
4. Regenerate route inventory for `20260428T033525Z`.
5. Update focused Python, API, and Explorer tests for the expanded graph.
6. Produce Explorer-facing API smoke performance evidence.
7. Run focused and broader affected verification.
8. Record validation evidence and commit.

## 6. Completion criteria

- Fixture contains 779 records, 760 relationships, 19 roots, 190 L2 topics, 570
  L3 topics, and max depth 3.
- Architecture and every other root have 10 L2 topics and 30 L3 subtopics.
- Shadow staging and consumer reports are `ok: true` for run `20260428T033525Z`.
- Route inventory is generated for the expanded run.
- Explorer-facing API smoke report confirms the expanded graph endpoint returns
  779 nodes and 760 edges within the documented smoke threshold.
- Focused Python, API, and Explorer tests pass.
- Broad affected API/Explorer checks pass.
- Safety greps show no unauthorized protected ingest, Neo4j mutation, KG reset,
  broad live authorization, or destructive commands in changed implementation.
- Validation log exists under `.ai/05_logs/`.
