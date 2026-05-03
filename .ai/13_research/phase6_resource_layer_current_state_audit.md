# Phase 6 Resource Layer Current State Audit

Date: 2026-05-03T03:45:00+08:00

## Verified State (Recomputed, Not Trusted)

### Graph Baseline

| Metric | Value |
|--------|-------|
| Nodes | 10,018 |
| Effective edges | 13,934 |
| Base edges | 13,670 |
| Admitted relationships | 264 |
| Relation families | 15 |

### Canonical Custody Baseline

| Metric | Value |
|--------|-------|
| latestAfterHashMismatches | 0 |
| manifestChainValid | true |
| Aliases / redirects / tombstones | 0 / 0 / 0 |
| P1 packets / reviews | 20 / 20 |
| p1PacketsContentHashMismatch | 0 |
| p1PacketReviewHashMismatch | 0 |
| p1PacketReviewStale | 0 |

### Resource Layer Registry

| Metric | Value |
|--------|-------|
| Resources | 7 |
| Node-resource links | 9 |
| Accepted links | 5 |
| Needs-review links | 3 |
| Rejected links | 1 |
| Candidates | 4 |
| Local files indexed | 25 |
| Local files admitted | 0 |
| Standards total | 2 |
| Standards missing context | 2 |
| Duplicate warnings | 0 |
| Broken links | 0 |
| Blockers | [] |

### Resource Inventory

| ID | Title | Type | Status |
|----|-------|------|--------|
| res-us-access-board-accessible-routes-ch4 | ADA Accessibility Standards Ch 4 | government_guidance | Active |
| res-wbdg-wind-safety-building-envelope | Wind Safety of the Building Envelope | professional_guidance | Active |
| res-wbdg-seismic-design-principles | Seismic Design Principles | professional_guidance | Active |
| res-ice-structural-load-paths | Structural Load Paths | professional_guidance | Active |
| res-asce-7-official-landing | ASCE 7 Minimum Design Loads | standard | **Missing context** |
| res-fhwa-earth-retaining-structures | Earth Retaining Structures | government_guidance | Active |
| res-aci-318-building-code-portal | ACI 318 Building Code Portal | standard | **Missing context** |

### Node-Resource Link Inventory

| Link ID | Node | Resource | Status |
|---------|------|----------|--------|
| nrl-accessible-route-usab-ch4 | Accessible Route Continuity | ADA Ch 4 | accepted |
| nrl-load-path-wbdg-wind | Load Path | WBDG Wind | accepted |
| nrl-wind-load-wbdg-wind | Structural Wind Load | WBDG Wind | accepted |
| nrl-seismic-load-wbdg-seismic | Structural Seismic Load | WBDG Seismic | accepted |
| nrl-load-path-ice | Load Path | ICE Load Paths | accepted |
| nrl-wind-load-asce-7-needs-review | Structural Wind Load | ASCE 7 | needs_review |
| nrl-seismic-load-asce-7-needs-review | Structural Seismic Load | ASCE 7 | needs_review |
| nrl-retaining-wall-fhwa-needs-review | Retaining Wall | FHWA | needs_review |
| nrl-structural-column-aci-rejected | Structural Column | ACI 318 | rejected |

### Standards Context Warnings

1. `res-asce-7-official-landing`: code/standard resource missing edition/version context
2. `res-aci-318-building-code-portal`: code/standard resource missing edition/version context
3. `nrl-wind-load-asce-7-needs-review`: standard/code-like link missing edition/version, citation/scope context
4. `nrl-seismic-load-asce-7-needs-review`: standard/code-like link missing edition/version, citation/scope context
5. `nrl-structural-column-aci-rejected`: standard/code-like link missing edition/version, citation/scope context

### No-Write Validator Check

- `bun run api/validateResourceLayer.ts --no-write`: ✅ No file changes
- `bun run api/validateGraphRelationships.ts --no-write`: ✅ No file changes
- `bun run api/validateCanonicalGraphStewardship.ts --no-write`: ✅ No file changes

### Local File Index

25 files indexed with hashes but:
- All `path` fields are null
- `indexedAt` fields are null
- Zero local files admitted to Resource Layer
- No node-resource links for local files

### Source Families

25 source families registered, including:
- US Access Board, WBDG/NIBS, buildingSMART, ASCE, ACI, AISC, IStructE, ICE, RIBA, AIA, FHWA, NIBS, ISO, Uniclass/NBS, OmniClass/CSI
- Academic discovery: Crossref, OpenAlex, Semantic Scholar, DataCite, CORE, Unpaywall, Open Library, Google Books, Internet Archive
- General web

### Review Decisions

`review-decisions.json` is empty (no human reviewer actions yet).
