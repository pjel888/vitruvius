# First Broader ACS Graph Enrichment Candidates

Last updated: 2026-05-02T07:58:28Z

This is a candidate-only Architecture/Civil/Structural graph enrichment batch. It does not admit production graph relationships and does not claim source truth. Every candidate uses existing node IDs observed in the current graph. Kimi reviewed the batch and recommended no admission until relation-vocabulary and source/context gates are satisfied.

## Kimi review summary

Accepted as high-quality candidates pending future review: 2, 3, 4, 5, 7, 8, 10, 13, 15, 18, 19, 23, 25. Held/revise before admission: 1, 6, 9, 11, 12, 14, 16, 17, 20, 21, 22, 24. All 25 require external/source or internal-authoring context before production admission.

## Candidate table

| # | Source | Proposed relation | Target | Kimi status | Notes |
|---:|---|---|---|---|---|
| 1 | `VTN-DOM-0012266` Slab | `TRANSFERS_GRAVITY_LOAD_TO` | `VTN-DOM-0012263` Beam | hold/revise | Contextual load path only; not universal for all slab systems. |
| 2 | `VTN-DOM-0012263` Beam | `TRANSFERS_LOAD_TO` | `VTN-DOM-0012269` Column | accepted candidate | Strong conceptual candidate pending relation vocabulary and source/context review. |
| 3 | `VTN-DOM-0012269` Column | `TRANSFERS_LOAD_TO` | `VTN-DOM-0012273` Foundation System | accepted candidate | Strong conceptual candidate pending relation vocabulary and source/context review. |
| 4 | `VTN-DOM-0012273` Foundation System | `CONSTRAINED_BY` | `VTN-DOM-0012293` Soil Bearing Capacity | accepted candidate | Can likely reuse/normalize to existing constrains semantics after review. |
| 5 | `VTN-DOM-0012769` Geotechnical Investigation Interface | `INFORMS` | `VTN-DOM-0012273` Foundation System | accepted candidate | Strong workflow candidate pending INFORMS vocabulary. |
| 6 | `VTN-DOM-0003013` Deep Foundations | `CONSTRAINED_BY` | `VTN-DOM-0012293` Soil Bearing Capacity | hold/revise | Too shallow-foundation-biased; deep foundations depend on end bearing, skin friction, and lateral capacity. |
| 7 | `VTN-DOM-0003010` Shallow Foundations | `CONSTRAINED_BY` | `VTN-DOM-0012293` Soil Bearing Capacity | accepted candidate | Strong conceptual candidate pending source/context review. |
| 8 | `VTN-DOM-0012771` Groundwater Design Level | `CONSTRAINS` | `VTN-DOM-0000313` Excavation Support | accepted candidate | Potentially can reuse existing constrains predicate after review. |
| 9 | `VTN-DOM-0000316` Excavation Sequencing | `COORDINATES_WITH` | `VTN-DOM-0000313` Excavation Support | hold/revise | Likely symmetric coordination; define directionality before admission. |
| 10 | `VTN-DOM-0003023` Lateral Earth Pressure | `CONSTRAINS` | `VTN-DOM-0003026` Retaining Walls | accepted candidate | Prefer this direction over duplicative retaining-wall review edge. |
| 11 | `VTN-DOM-0003026` Retaining Walls | `REQUIRES_REVIEW_OF` | `VTN-DOM-0003023` Lateral Earth Pressure | hold/revise | Overlaps candidate 10; prefer pressure constrains wall. |
| 12 | `VTN-DOM-0002906` Site Grading | `DIRECTS_SURFACE_RUNOFF_TO` | `VTN-DOM-0012758` Surface Runoff | hold/revise | Wording too strong; grading influences runoff but does not always direct to a runoff node. |
| 13 | `VTN-DOM-0012764` Roof Drainage Discharge Interface | `DISCHARGES_TO` | `VTN-DOM-0002899` Stormwater Networks | accepted candidate | Strong conceptual candidate pending DISCHARGES_TO vocabulary and source/context review. |
| 14 | `VTN-DOM-0012742` Roof Drainage Interface | `COORDINATES_WITH` | `VTN-DOM-0012764` Roof Drainage Discharge Interface | hold/revise | Likely symmetric coordination; define relation semantics first. |
| 15 | `VTN-DOM-0012777` Structural Wind Load | `CONSTRAINS` | `VTN-DOM-0012313` Facade Assembly | accepted candidate | Strong conceptual candidate pending context review. |
| 16 | `VTN-DOM-0012743` Facade Anchor Interface | `REQUIRES_COORDINATION_WITH` | `VTN-DOM-0012313` Facade Assembly | hold/revise | Likely part/coordination relation; endpoint direction may be backwards. |
| 17 | `VTN-DOM-0000012` Accessible Routes | `CONSTRAINED_BY` | `VTN-DOM-0002906` Site Grading | hold/revise | Plausible but accessibility/site-slope source context is required. |
| 18 | `VTN-DOM-0012741` Floor Opening Coordination | `REQUIRES_COORDINATION_WITH` | `VTN-DOM-0012266` Slab | accepted candidate | Strong coordination candidate pending vocabulary/source context. |
| 19 | `VTN-DOM-0012165` Structural Grid | `COORDINATES_WITH` | `VTN-DOM-0012261` Column Grid | accepted candidate | Strong coordination candidate pending symmetric vocabulary. |
| 20 | `VTN-DOM-0012289` Expansion Joint | `ACCOMMODATES` | `VTN-DOM-0012794` Structural Movement Joint | hold/revise | Endpoint mismatch risk; both may be joint concepts. |
| 21 | `VTN-DOM-0012767` Permeable Pavement | `SUPPORTED_BY` | `VTN-DOM-0012815` Pavement Subgrade Interface | hold/revise | Plausible but detail/source dependent. |
| 22 | `VTN-DOM-0012807` Pavement Subgrade Preparation | `INFORMS` | `VTN-DOM-0012815` Pavement Subgrade Interface | hold/revise | Vague; consider constrains or coordination after semantics review. |
| 23 | `VTN-DOM-0012280` Foundation Settlement | `CONSTRAINS` | `VTN-DOM-0012273` Foundation System | accepted candidate | Strong conceptual candidate pending context review. |
| 24 | `VTN-DOM-0012773` Differential Settlement Evaluation | `INFORMS` | `VTN-DOM-0012280` Foundation Settlement | hold/revise | Evaluation informs design response, not the settlement phenomenon itself. |
| 25 | `VTN-DOM-0012281` Lateral Stability | `REQUIRES` | `VTN-DOM-0012270` Shear Wall | accepted candidate | Strong but must respect existing Shear Wall high-risk packet; source/scope review needed before admission. |

## Relation vocabulary additions or normalization required

- Define or normalize `TRANSFERS_LOAD_TO`, `TRANSFERS_GRAVITY_LOAD_TO`, `INFORMS`, `COORDINATES_WITH`, `REQUIRES_COORDINATION_WITH`, `DISCHARGES_TO`, `DIRECTS_SURFACE_RUNOFF_TO`, `SUPPORTED_BY`, `ACCOMMODATES`, and `REQUIRES_REVIEW_OF`.
- Prefer existing `constrains` / `requires` where accurate and avoid generic `related_to`.
- Do not admit code, standard, AHJ, numerical, or project-specific claims without Resource Layer/source support.

## Next action

Select a small subset of accepted candidates that can reuse existing `constrains` or `requires` semantics, prepare dry-run admission packets, and seek another Kimi implementation-safety review before any graph mutation.
