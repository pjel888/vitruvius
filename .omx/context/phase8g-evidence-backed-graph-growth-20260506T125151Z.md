# Phase 8G Evidence-Backed Graph Growth Context

## Task Statement

Continue evidence-backed graph improvement using accepted Resource Layer links and official-source-reviewed Resources.

## Desired Outcome

Admit at least one safe evidence-backed graph/node improvement, apply a safe node metadata/evidence annotation, or prove that all accepted Resource-backed candidates are graph-unsafe with exact blockers.

## Known Facts / Evidence

- Baseline commit is `a594bb9cc96a9eb596f2d1c1c69c9a0107e3bcc4`.
- Resources: 10.
- nodeResourceLinks: 12.
- Accepted links: 8.
- Admitted relationships: 265.
- Base edges: 13,670.
- Effective edges: 13,935.
- `CROSS_DOMAIN_EQUIVALENT`: 0.
- `CROSS_DOMAIN_ALIGNMENT`: 22.
- Phase 8F admitted `BIM Schemas INFORMS IFC Exchange`.
- WBDG Fire Protection and Uniclass remained Resource Layer evidence only.
- Baseline validators and full suites pass: API 432, Explorer 121, Explorer build with existing chunk-size warning, Python KG 118.

## Constraints

- Do not invent source metadata or source truth.
- Do not create placeholder nodes.
- Do not create graph edges merely because a Resource exists.
- Do not admit broad/generic relationships, `CROSS_DOMAIN_EQUIVALENT`, or `related_to`.
- Do not claim current/governing/compliance/AHJ/jurisdiction/source-truth status.
- Do not download or store protected content.
- Do not mutate P0 Concrete/Reinforced Concrete or high-risk P1 packets.
- Every graph/canonical write must be transaction-manifest-backed with rollback.
- Every graph improvement needs source/context gate, relation vocabulary gate, delegated review, dry-run, visual verification, and tests.

## Unknowns / Open Questions

- Whether any of the eight accepted Resource Layer links support a precise non-duplicative graph overlay beyond the Phase 8F BIM Schemas relation.
- Whether node metadata/evidence annotation is supported by current graph-canonical workflows without inventing new schema semantics.

## Likely Codebase Touchpoints

- `006_System-Manifests/resource-layer/resources.json`
- `006_System-Manifests/resource-layer/node-resource-links.json`
- `006_System-Manifests/graph-canonical/admitted-relationships.json`
- `006_System-Manifests/graph-canonical/stewardship-decisions.json`
- `006_System-Manifests/graph-canonical/approvals.json`
- `api/graph/canonicalStewardship.ts`
- `api/canonicalGraphStewardship.test.ts`
- `.ai/13_research/phase8g_*.md`
