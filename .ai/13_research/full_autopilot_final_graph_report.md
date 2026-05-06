# Full Autopilot Final Graph Report

Date: 2026-05-07 local

## Graph Metrics

| Metric | Before full loop | After full loop |
|---|---:|---:|
| Admitted graph relationships | 266 | 266 |
| Base graph edges | 13,670 | 13,670 |
| Effective graph edges | 13,936 | 13,936 |
| `CROSS_DOMAIN_EQUIVALENT` | 0 | 0 |
| `CROSS_DOMAIN_ALIGNMENT` | 22 | 22 |
| Graph edges admitted in this full loop | 0 | 0 |
| Graph nodes improved in this full loop | 0 | 0 |

## Existing Resource-Backed Graph Edges Preserved

- `BIM Schemas INFORMS IFC Exchange`
- `Structural Wind Load INFORMS Load Path`

Both remained visible through validator/API/Explorer regression coverage.

## New Graph Candidate Disposition

| Candidate area | Disposition | Reason |
|---|---|---|
| FHWA Retaining Wall | Resource Layer only | Potential `RESISTS` edge duplicates existing retaining-wall/lateral-earth-pressure semantics; drainage and groundwater candidates overclaim metadata-only public page context |
| WBDG Fire Protection | Resource Layer only | Public metadata supports Resource evidence, not a precise non-duplicative graph relation |
| Uniclass | Resource Layer only | Classification context does not prove adoption, mapping, equivalence, or jurisdictional authority |
| ASCE/ACI standards | Blocked | Standards context incomplete and protected standard text was not ingested |
| Source-family candidates | Blocked | Source-family metadata is too broad for graph edges and not node-specific |

## Safety Gates

- No `CROSS_DOMAIN_EQUIVALENT` admitted.
- No generic `related_to` admitted.
- No placeholder node created.
- No P0 Concrete/Reinforced Concrete mutation.
- No high-risk P1 packet touched.
- No source-truth/current/governing/compliance/AHJ/numerical claim introduced.
- No graph/canonical registry write occurred in this full loop.
