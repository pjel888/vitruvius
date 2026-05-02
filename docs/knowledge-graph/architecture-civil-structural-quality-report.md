# Architecture Civil Structural Quality Report

Date: 2026-05-01

## Before and after metrics

| Metric | Before ACS loop | After initial ACS loop | After gap closure | Delta from initial ACS |
|---|---:|---:|---:|---:|
| Backbone nodes | 9,939 | 10,004 | 10,006 | +2 |
| Governed relationships | 13,459 | 13,610 | 13,610 | +0 net |
| Source-rights rows | 114 | 123 | 123 | +0 |
| Resolver golden cases | 124 | 132 | 135 | +3 |
| ACS introduced nodes | 0 | 65 | 67 | +2 |
| ACS typed non-hierarchy edges | 0 | 86 | 95 | +9 |
| ACS hierarchy edges | 0 | 65 | 67 | +2 |
| Historical self-loop relationships | not measured | 11 | 0 | -11 |
| Introduced orphan nodes | not applicable | 0 | 0 | 0 critical |
| Introduced generic related_to edges | 0 | 0 | 0 | 0 |
| Introduced ACS edge source coverage | not applicable | 86 of 86 | 95 of 95 | 100 percent |
| Duplicate relationship triples | 0 | 0 | 0 | 0 |

Net governed relationship count stayed at 13,610 because this pass added 11 ACS relationships and removed 11 historical self-loop relationships. The implementation enrichment report `20260501T062000Z_ACS_GAP_CLOSURE` records the pre-cleanup relationship count before self-loops were removed; the post-cleanup idempotence report `20260501T064500Z_ACS_GAP_CLOSURE_POST_CLEANUP` records the final 13,610-relationship state. Duplicate normalized labels remain globally at 514 historical groups; same-parent duplicate normalized labels are 0, and the graph-quality report now includes concrete duplicate samples for a future steward-reviewed cleanup.

## Quality score

Run: `20260501T062900Z_ACS_GAP_CLOSURE_QUALITY_FINAL`

| Dimension | Score | Max |
|---|---:|---:|
| Node completeness | 20 | 20 |
| Edge specificity | 20 | 20 |
| Cross-taxonomy reasoning paths | 20 | 20 |
| Provenance/source coverage | 15 | 15 |
| Validation/test coverage | 15 | 15 |
| Duplicate/orphan hygiene | 10 | 10 |
| Total | 100 | 100 |

## Passing traversal gates
- Accessible route to pedestrian site gradient control.
- Roof drainage interface to civil detention/stormwater path.
- Geotechnical investigation to footing/foundation selection.
- Suspended slab to soil bearing capacity through gravity load path.
- Wind load to structural core through facade, connection, diaphragm, and collector.
- Floor opening to diaphragm opening coordination.
- Retaining wall to perimeter drainage and pressure relief.
- Structural movement joint to architectural waterproofing continuity.
- Subsurface utility conflict review to foundation layout, shoring, and service-entry routing.
- Flood hazard applicability to design flood elevation, finished-floor elevation, and foundation interface.
- Slope stability to topography, grading, and retaining-wall stability basis.

## Validation result
Graph-quality run `20260501T062500Z_ACS_GAP_CLOSURE_GRAPH_QUALITY` has no errors. Key metrics: self-loop count 0, orphan node count 0, generic relationship count 0, introduced non-hierarchy orphan count 0, introduced relationship source-family coverage 95 of 95. Warning retained: historical duplicate normalized labels exist across the full graph and are documented as a non-critical hygiene gap.

## Remaining-gap follow-up quality score

Run: `20260501T072400Z_ACS_REMAINING_GAPS_QUALITY`

| Metric | After gap closure | After remaining-gap follow-up | Delta |
|---|---:|---:|---:|
| Backbone nodes | 10,006 | 10,014 | +8 |
| Governed relationships | 13,610 | 13,645 | +35 |
| Source-rights rows | 123 | 123 | 0 |
| Resolver golden cases | 135 | 139 | +4 |
| ACS introduced nodes | 67 | 75 | +8 |
| ACS typed non-hierarchy edges | 95 | 122 | +27 |
| ACS hierarchy edges | 67 | 75 | +8 |
| Historical self-loop relationships | 0 | 0 | 0 |
| Introduced orphan nodes | 0 | 0 | 0 |
| Introduced generic related_to edges | 0 | 0 | 0 |
| Introduced ACS edge source coverage | 95 of 95 | 122 of 122 | 100 percent |

Quality score remains 100/100 across all dimensions. New traversal gates pass for:
- test-hole utility verification to footing/foundation clearance;
- pavement subgrade preparation to emergency access route;
- curb-ramp geometry interface to accessible site-to-building route;
- stormwater maintenance access to civil asset handover record;
- AHJ coordination to wind-load adopted-basis gate.

Duplicate-label hygiene is now report-backed: `duplicate-label-context-index.json` classifies all 514 duplicate normalized label groups as contextual cross-parent or cross-root duplicates with 0 same-parent blockers. Canonical labels were intentionally not renamed.

## Post-review validation hardening

Architect review identified two remaining quality-gate gaps after the follow-up implementation: the new AHJ/project-basis metadata was missing from the `BackboneShadowGraphPreview` edge type, and shadow staging did not explicitly compare used governed predicates against the staged predicate registry. Both are now fixed. The follow-up validation suite includes a frontend type-contract test for the new metadata fields and a shadow-staging negative test for unregistered predicates.

## External-gated follow-up quality score

Run: `20260501T082300Z_ACS_EXTERNAL_GATED_GAP_QUALITY`

| Metric | After remaining-gap follow-up | After external-gated follow-up | Delta |
|---|---:|---:|---:|
| Backbone nodes | 10,014 | 10,018 | +4 |
| Governed relationships | 13,645 | 13,670 | +25 |
| Source-rights rows | 123 | 123 | 0 |
| Resolver golden cases | 139 | 142 | +3 |
| ACS introduced nodes | 75 | 79 | +4 |
| ACS typed non-hierarchy edges | 122 | 143 | +21 |
| ACS hierarchy edges | 75 | 79 | +4 |
| Historical self-loop relationships | 0 | 0 | 0 |
| Introduced orphan nodes | 0 | 0 | 0 |
| Introduced generic related_to edges | 0 | 0 | 0 |
| Introduced ACS edge source coverage | 122 of 122 | 143 of 143 | 100 percent |

Quality score remains 100/100 across all dimensions. New traversal gates pass for:
- accessible public-way crossing tie-in to runoff and pedestrian gradient control;
- culvert drainage interface to hydrologic basis, overland overflow, and flood/scour hazard review;
- structural criteria basis gate to AHJ, risk, seismic applicability, live load, wind load, and seismic-load concepts without numeric criteria;
- catch basin to preventive maintenance planning.

Gated-review run `20260501T083500Z_ACS_GATED_REVIEW_HARDENED` passes with 0 errors while keeping numeric criteria admission, protected payload ingest, canonical label mutation, production promotion, and live Neo4j writes false. It exports 514 duplicate-label candidate groups for steward review with 0 same-parent blockers and `auto_merge_allowed: false`.


## External-gate apply-path quality update

Gated-review run `20260501T090200Z_ACS_EXTERNAL_GATE_APPLY_PATHS_DRY_RUN` passes with 0 errors and now includes the full external-gate surface:

- `steward_duplicate_decision_gate`: blocked when no steward packet is supplied; validates safe steward packets as `validated_not_applied` and writes a dry-run apply plan only.
- `criteria_admission_gate`: remains validation-only and writes no numeric criteria.
- `external_authority_ledger_gate`: validates authority ledgers structurally without authorizing admission.
- `protected_payload_manifest_gate`: validates hash-only metadata without ingesting or exposing protected payloads.
- `live_promotion_gate`: requires production credentials plus promotion-plan/rollback evidence but remains dry-run only.
- `payload_leak_audit`: scans JSON payloads regardless file suffix and rejects protected/source/numeric/secret-like keys.

Targeted gated-review tests now cover 20 scenarios, including CLI packet flags, path-escape rejection, persisted report schema, safe steward dry-run apply plans, unsafe global merge decisions, hash-only protected payload manifests, unsafe payload text, and live-promotion dry-run gating.

## Hard-blocker readiness quality update

Gated-review run `20260501T094300Z_ACS_EXTERNAL_GATE_READINESS_BUNDLE` passes with 0 errors and adds draft readiness artifacts for every remaining external gate:

- steward preserve packet skeleton;
- project/AHJ criteria packet skeleton;
- external authority ledger skeleton;
- protected payload manifest skeleton;
- live-promotion plan skeleton;
- external-gate readiness bundle.

These artifacts improve operator readiness without changing the graph quality score or crossing truth/admission boundaries. The runner still reports the hard gates as blocked when real steward, AHJ, source-rights, credential, backup, restore, and rollback evidence is absent. Targeted gated-review tests now cover 23 scenarios, including skeleton generation, no-fabricated credential values, readiness bundle gate statuses, and same-parent duplicate behavior.
