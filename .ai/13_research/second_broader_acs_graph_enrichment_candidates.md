# Second Broader ACS Graph Enrichment Candidates

Date: 2026-05-02T09:55:00Z

This is a candidate-only queue. No edge in this file is admitted or approved by this report. All candidates require relation-vocabulary gate, source/context gate, Kimi review, dry-run, scoped approval, transaction manifest, rollback preview, and graph visibility validation before admission.

## Candidate queue

1. `VTN-DOM-0012267` One Way Slab -> `VTN-DOM-0012263` Beam ? proposed `TRANSFERS_LOAD_TO` ? source/context: general non-numerical load path synthesis.
2. `VTN-DOM-0012268` Two Way Slab -> `VTN-DOM-0012263` Beam ? proposed `TRANSFERS_LOAD_TO` ? source/context: general non-numerical load path synthesis.
3. `VTN-DOM-0012268` Two Way Slab -> `VTN-DOM-0012269` Column ? proposed `TRANSFERS_LOAD_TO` ? verify direction/edge-neighborhood first.
4. `VTN-DOM-0012785` Grade Beam -> `VTN-DOM-0012273` Foundation System ? proposed `TRANSFERS_LOAD_TO` ? verify if grade beam endpoint should align to shallow foundation instead.
5. `VTN-DOM-0012279` Pile Foundation -> `VTN-DOM-0003013` Deep Foundations ? proposed `CROSS_DOMAIN_ALIGNMENT` ? candidate only; check existing duplicate/alignment edges first.
6. `VTN-DOM-0012786` Slab-On-Grade -> `VTN-DOM-0000261` Shallow Foundations ? proposed `RELATED_SPECIALIZATION_OF` ? vocabulary/source review required.
7. `VTN-DOM-0012293` Soil Bearing Capacity -> `VTN-DOM-0012786` Slab-On-Grade ? proposed `CONSTRAINS` ? non-numerical, no bearing value claim.
8. `VTN-DOM-0012771` Groundwater Design Level -> `VTN-DOM-0012278` Mat Foundation ? proposed `CONSTRAINS` ? blocked until Mat Foundation high-risk packet reviewed.
9. `VTN-DOM-0000317` Groundwater -> `VTN-DOM-0000313` Excavation Support ? proposed `AFFECTS` or `CONSTRAINS` ? relation-vocabulary review required.
10. `VTN-DOM-0012758` Surface Runoff -> `VTN-DOM-0002906` Site Grading ? proposed `AFFECTS` ? avoid numerical drainage claims.
11. `VTN-DOM-0002906` Site Grading -> `VTN-DOM-0005262` Stormwater Flow Path ? proposed `COORDINATES_WITH` or `CONSTRAINS` ? directionality review required.
12. `VTN-DOM-0012767` Permeable Pavement -> `VTN-DOM-0012758` Surface Runoff ? proposed `AFFECTS` ? source/context review required.
13. `VTN-DOM-0012815` Pavement Subgrade Interface -> `VTN-DOM-0000251` Pavements ? proposed `SUPPORTS` ? relation-vocabulary review required.
14. `VTN-DOM-0012807` Pavement Subgrade Preparation -> `VTN-DOM-0012815` Pavement Subgrade Interface ? proposed `SUPPORTS` ? candidate only.
15. `VTN-DOM-0012743` Facade Anchor Interface -> `VTN-DOM-0012313` Facade Assembly ? proposed `SUPPORTS` or `COORDINATES_WITH` ? vocabulary review required.
16. `VTN-DOM-0012313` Facade Assembly -> `VTN-DOM-0012163` Wind Load ? proposed `RESISTS`/`AFFECTS` ? defer until relation wording avoids overclaim.
17. `VTN-DOM-0012790` Structural Core -> `VTN-DOM-0012270` Shear Wall ? proposed `COORDINATES_WITH` ? blocked until Shear Wall high-risk review.
18. `VTN-DOM-0012210` Shaft Planning -> `VTN-DOM-0012790` Structural Core ? proposed `COORDINATES_WITH` ? verify endpoints and UI value.
19. `VTN-DOM-0004703` Vertical Shaft Planning -> `VTN-DOM-0012210` Shaft Planning ? proposed `COORDINATES_WITH` ? candidate only.
20. `VTN-DOM-0012742` Roof Drainage Interface -> `VTN-DOM-0012764` Roof Drainage Discharge Interface ? proposed `COORDINATES_WITH` ? likely safe but check duplicate edge first.

## Next gate

Prioritize candidates that reuse existing admitted/validated relation types (`TRANSFERS_LOAD_TO`, `DISCHARGES_TO`, `COORDINATES_WITH`, `CONSTRAINS`) and avoid high-risk duplicate packets.
