# 07 — Golden Example: Accessible Ramps

> **Scope:** End-to-end concrete walkthrough of the governed taxonomy architecture using "Accessible Ramps" as the reference concept.
> **Date:** 2026-04-19
> **Authority:** `00_locked_decisions.md`, `03_implementation_plan.md`

---

## 1. Legacy State (Before Migration)

### 1.1 Legacy Markdown File

**File path:** `003_Canonical-Knowledge-Layer/shared/concepts/concept-accessible-ramps.md`

```yaml
---
id: concept-accessible-ramps
title: Accessible Ramps
page_type: concept
canonical_status: enriched
trust_level: primary
regulatory_basis:
- source_id: irr-revised-implementing-rules-and-regulations-of-batas-pambansa-blg-344
  section_id: section-1
  evidence_snippet: "Ramps shall be provided as an alternative to stairs..."
- source_id: law-national-building-code-of-the-philippines
  section_id: section-408.2
  evidence_snippet: "Ramps shall have a maximum slope of 1:12..."
taxonomy_path:
- taxonomy-accessibility
- topic-barrier-free-design
- subtopic-routes
---

## Accessible Ramps

Ramps provide accessible routes for persons with disabilities...
```

### 1.2 Legacy Neo4j Node

```cypher
CREATE (c:CanonicalNode:Concept {
  id: "concept-accessible-ramps",
  label: "Accessible Ramps",
  type: "concept",
  kind: "concept",
  summary: "Ramps provide accessible routes...",
  slug: "accessible-ramps",
  status: "enriched",
  confidence: 1.0,
  taxonomy_path: ["taxonomy-accessibility", "topic-barrier-free-design", "subtopic-routes"],
  created_at: datetime(),
  updated_at: datetime()
})
```

### 1.3 Legacy API Response (v1)

```json
{
  "id": "concept-accessible-ramps",
  "label": "Accessible Ramps",
  "type": "concept",
  "kind": "concept",
  "summary": "Ramps provide accessible routes...",
  "taxonomy_path": ["taxonomy-accessibility", "topic-barrier-free-design", "subtopic-routes"],
  "status": "enriched",
  "regulatory_basis": [
    {
      "source_id": "irr-revised-implementing-rules-and-regulations-of-batas-pambansa-blg-344",
      "section_id": "section-1",
      "evidence_snippet": "Ramps shall be provided..."
    },
    {
      "source_id": "law-national-building-code-of-the-philippines",
      "section_id": "section-408.2",
      "evidence_snippet": "Ramps shall have a maximum slope..."
    }
  ]
}
```

**Problems in legacy state:**
1. `regulatory_basis` is embedded inside the concept node — collapses canonical meaning with local obligation.
2. Semantic slug ID is mutable and breaks on rename.
3. `taxonomy_path` array of semantic IDs breaks when any ID changes.
4. No facet model — cannot answer "show me all design-phase accessibility concepts for commercial buildings."
5. No jurisdiction model — cannot answer "what are the ramp requirements in Makati vs Manila?"
6. No standards mapping — cannot answer "what is the OmniClass code for accessible ramps?"

---

## 2. Migration: Old → New

### 2.1 ID Migration

**Old ID:** `concept-accessible-ramps`
**New opaque ID:** `VTN-CON-0000042`

**ID Redirect Record:**
```yaml
# 006_System-Manifests/audits/taxonomy-governance/id_redirect.csv
old_id: concept-accessible-ramps
new_id: VTN-CON-0000042
scope: concept
reason: migration-to-opaque-ids
redirect_type: permanent
```

**Neo4j:**
```cypher
MATCH (c:CanonicalNode {id: "concept-accessible-ramps"})
SET c.canonical_id = "VTN-CON-0000042"
```

### 2.2 Backbone Placement

**Home-domain assignment rulebook (from `03_implementation_plan.md` §6):**
> Accessibility has its own L1 domain. "Accessible Ramps" lives in `taxonomy-accessibility`.

**Backbone path:**
```
L1: taxonomy-accessibility (Accessibility)
  L2: barrier-free-design
    L3: routes
      L4: accessible-ramps
```

**Backbone node:**
```yaml
# 003_Canonical-Knowledge-Layer/backbone/backbone-l4.yaml
- canonical_id: VTN-DOM-0000042
  path_code: ACC.BFD.ROU.ARA
  level: 4
  parent_path_code: ACC.BFD.ROU
  pref_label: Accessible Ramps
  definition: "Ramps designed to provide accessible routes for persons with disabilities."
  aliases: ["wheelchair ramps", "access ramps"]
  scope_note: "Includes interior and exterior ramps. Excludes stair lifts."
  steward: accessibility-steward@example.com
  release_version: 1.0.0
```

### 2.3 Facet Assignment

```yaml
# Frontmatter after migration
---
canonical_id: VTN-CON-0000042
path_code: ACC.BFD.ROU.ARA
title: Accessible Ramps
page_type: concept
canonical_status: enriched
trust_level: primary
knowledge_type: concept
asset_scope: building
lifecycle_stage: design
project_type: mixed_use
performance_topic: accessibility
primary_domain: taxonomy-accessibility
steward: accessibility-steward@example.com
release_version: 1.0.0
---
```

### 2.4 DocumentVersion vs DocumentEdition Separation

**Legacy:** `regulatory_basis` embedded in concept frontmatter.

**New model:**

**DocumentVersion (extraction artifact — preserved, not changed):**
```cypher
CREATE (dv:DocumentVersion {
  id: "docver-irr-bp344-20250301",
  sha256: "abc123...",
  source_path: "001_Raw-Source-Layer/001-Laws/BP344.pdf",
  extraction_method: "opendataloader-pdf",
  extracted_at: datetime()
})
```

**AuthorityDocumentFamily (normative):**
```cypher
CREATE (adf:AuthorityDocumentFamily {
  id: "VTN-ADF-0000001",
  canonical_id: "VTN-ADF-0000001",
  title: "Batas Pambansa Blg. 344 — Accessibility Law",
  short_title: "BP 344",
  jurisdiction_code: "PH",
  authority_code: "PH-CONGRESS"
})
```

**AuthorityDocumentEdition (normative):**
```cypher
CREATE (ade:AuthorityDocumentEdition {
  id: "VTN-ADE-0000001",
  canonical_id: "VTN-ADE-0000001",
  edition_number: "Revised IRR 2007",
  effective_date: date("2007-01-01"),
  repeal_date: null,
  status: "active"
})
CREATE (ade)-[:HAS_EDITION]->(adf)
```

### 2.5 Jurisdiction Chain + Applicability Rule

**Jurisdiction hierarchy:**
```cypher
CREATE (ph:Jurisdiction {code: "PH", name: "Philippines", level: "national"})
CREATE (ncr:Jurisdiction {code: "PH-NCR", name: "National Capital Region", level: "regional"})
CREATE (makati:Jurisdiction {code: "PH-NCR-Makati", name: "Makati City", level: "local"})
CREATE (ncr)-[:WITHIN_JURISDICTION]->(ph)
CREATE (makati)-[:WITHIN_JURISDICTION]->(ncr)
```

**Applicability Rule:**
```cypher
CREATE (ar:ApplicabilityRule {
  id: "VTN-APP-0000001",
  canonical_id: "VTN-APP-0000001",
  jurisdiction_code: "PH",
  scope: "national",
  precedence: 1,
  condition: "all_buildings",
  effective_date: date("2007-01-01"),
  status: "active"
})
CREATE (ade)-[:APPLIES_IN]->(ph)
CREATE (ar)-[:GOVERNS]->(ade)
```

### 2.6 Overlay (Jurisdiction-Specific Obligation)

```cypher
CREATE (o:Overlay {
  id: "VTN-OVR-0000001",
  canonical_id: "VTN-OVR-0000001",
  obligation_type: "mandatory",
  condition: "slope_max_1_12",
  measurement: "1:12",
  jurisdiction_code: "PH",
  effective_date: date("2007-01-01"),
  status: "active"
})
CREATE (c)-[:HAS_OVERLAY]->(o)
CREATE (o)-[:BASED_ON]->(ade)
CREATE (o)-[:APPLIES_IN]->(ph)
```

**Key principle:** The overlay stores jurisdiction-specific obligation. The canonical node stores globally meaningful definition. They are separate.

### 2.7 Evidence Linkage

```cypher
CREATE (es1:EvidenceSpan {
  id: "VTN-EVS-0000001",
  canonical_id: "VTN-EVS-0000001",
  source_edition_id: "VTN-ADE-0000001",
  section_id: "section-1",
  evidence_snippet: "Ramps shall be provided as an alternative to stairs..."
})
CREATE (c)-[:SUPPORTED_BY {relationship_type: "defined_in"}]->(es1)
CREATE (es1)-[:EXTRACTED_FROM]->(dv)
```

### 2.8 Standards Mapping

```cypher
CREATE (sr1:StandardReference {
  id: "VTN-STD-0000001",
  system: "OmniClass",
  code: "23-27 11 11",
  title: "Ramps",
  url: "https://www.omniclass.org/..."
})
CREATE (c)-[:MAPS_TO_STANDARD {
  mapping_type: "exact",
  confidence: 0.92,
  mapped_by: "steward-accessibility",
  mapped_at: datetime()
}]->(sr1)
```

---

## 3. New Canonical Markdown File

**File path:** `003_Canonical-Knowledge-Layer/backbone/concepts/VTN-CON-0000042.md`

```yaml
---
canonical_id: VTN-CON-0000042
path_code: ACC.BFD.ROU.ARA
title: Accessible Ramps
page_type: concept
canonical_status: enriched
trust_level: primary
knowledge_type: concept
asset_scope: building
lifecycle_stage: design
project_type: mixed_use
performance_topic: accessibility
primary_domain: taxonomy-accessibility
steward: accessibility-steward@example.com
release_version: 1.0.0
id_redirect:
  from: concept-accessible-ramps
  type: permanent
---

## Accessible Ramps

Ramps provide accessible routes for persons with disabilities...
```

**Note:** `regulatory_basis` is removed from frontmatter. Evidence is linked via graph edges. Jurisdiction obligations are stored in overlays.

---

## 4. New Neo4j Graph State

```cypher
// Canonical node (globally meaningful)
CREATE (c:CanonicalNode:Concept {
  id: "VTN-CON-0000042",
  canonical_id: "VTN-CON-0000042",
  path_code: "ACC.BFD.ROU.ARA",
  label: "Accessible Ramps",
  knowledge_type: "concept",
  asset_scope: "building",
  lifecycle_stage: "design",
  project_type: "mixed_use",
  performance_topic: "accessibility",
  primary_domain: "taxonomy-accessibility",
  summary: "Ramps provide accessible routes...",
  status: "enriched",
  steward: "accessibility-steward@example.com",
  release_version: "1.0.0"
})

// Backbone placement
CREATE (b4:BackboneNode {path_code: "ACC.BFD.ROU.ARA", level: 4, pref_label: "Accessible Ramps"})
CREATE (b3:BackboneNode {path_code: "ACC.BFD.ROU", level: 3, pref_label: "Routes"})
CREATE (b2:BackboneNode {path_code: "ACC.BFD", level: 2, pref_label: "Barrier-Free Design"})
CREATE (b1:BackboneNode {path_code: "ACC", level: 1, pref_label: "Accessibility"})
CREATE (c)-[:BELONGS_TO_DOMAIN]->(b4)
CREATE (b4)-[:HAS_PARENT]->(b3)
CREATE (b3)-[:HAS_PARENT]->(b2)
CREATE (b2)-[:HAS_PARENT]->(b1)

// Jurisdiction + overlay (local obligation)
CREATE (o:Overlay {id: "VTN-OVR-0000001", obligation_type: "mandatory", condition: "slope_max_1_12"})
CREATE (c)-[:HAS_OVERLAY]->(o)
CREATE (o)-[:APPLIES_IN]->(ph)
CREATE (o)-[:BASED_ON]->(ade)

// Evidence (supports canonical meaning)
CREATE (es1:EvidenceSpan {id: "VTN-EVS-0000001", section_id: "section-1"})
CREATE (c)-[:SUPPORTED_BY]->(es1)
CREATE (es1)-[:EXTRACTED_FROM]->(dv)

// Standards mapping (crosswalk)
CREATE (c)-[:MAPS_TO_STANDARD {confidence: 0.92}]->(sr1)

// Legacy redirect
CREATE (old:CanonicalNode {id: "concept-accessible-ramps"})
CREATE (old)-[:SUPERSEDED_BY {reason: "migration-to-opaque-ids"}]->(c)
```

---

## 5. API v2 Responses

### 5.1 GET /v2/node/VTN-CON-0000042

```json
{
  "canonical_id": "VTN-CON-0000042",
  "path_code": "ACC.BFD.ROU.ARA",
  "label": "Accessible Ramps",
  "knowledge_type": "concept",
  "asset_scope": "building",
  "lifecycle_stage": "design",
  "project_type": "mixed_use",
  "performance_topic": "accessibility",
  "primary_domain": "taxonomy-accessibility",
  "summary": "Ramps provide accessible routes for persons with disabilities...",
  "status": "enriched",
  "steward": "accessibility-steward@example.com",
  "release_version": "1.0.0",
  "facets": {
    "knowledge_type": "concept",
    "asset_scope": "building",
    "lifecycle_stage": "design",
    "project_type": "mixed_use",
    "performance_topic": "accessibility",
    "primary_domain": "taxonomy-accessibility"
  },
  "backbone": {
    "path_code": "ACC.BFD.ROU.ARA",
    "level": 4,
    "parent_path_code": "ACC.BFD.ROU",
    "pref_label": "Accessible Ramps",
    "domain": "Accessibility"
  },
  "jurisdiction_overlays": [
    {
      "jurisdiction_code": "PH",
      "jurisdiction_name": "Philippines",
      "obligation_type": "mandatory",
      "condition": "slope_max_1_12",
      "measurement": "1:12",
      "based_on": {
        "family": "Batas Pambansa Blg. 344 — Accessibility Law",
        "edition": "Revised IRR 2007",
        "effective_date": "2007-01-01"
      }
    }
  ],
  "evidence": [
    {
      "evidence_id": "VTN-EVS-0000001",
      "source_edition": "Revised IRR 2007",
      "section_id": "section-1",
      "snippet": "Ramps shall be provided as an alternative to stairs..."
    }
  ],
  "standards_mappings": [
    {
      "system": "OmniClass",
      "code": "23-27 11 11",
      "title": "Ramps",
      "confidence": 0.92
    }
  ],
  "legacy_redirect": {
    "old_id": "concept-accessible-ramps",
    "redirect_type": "permanent",
    "status": 308
  }
}
```

### 5.2 POST /v2/resolve (Jurisdiction-Aware)

**Request:**
```json
{
  "canonical_id": "VTN-CON-0000042",
  "jurisdiction_code": "PH-NCR-Makati",
  "date": "2025-06-15"
}
```

**Response:**
```json
{
  "canonical_node": {
    "canonical_id": "VTN-CON-0000042",
    "label": "Accessible Ramps",
    "facets": { /* ... */ }
  },
  "resolved_context": {
    "jurisdiction": {
      "requested": "PH-NCR-Makati",
      "resolved": "PH-NCR-Makati",
      "precedence_chain": ["PH-NCR-Makati", "PH-NCR", "PH"]
    },
    "applicable_overlays": [
      {
        "jurisdiction_code": "PH",
        "obligation_type": "mandatory",
        "condition": "slope_max_1_12",
        "measurement": "1:12",
        "source": "BP 344 Revised IRR 2007"
      }
    ],
    "effective_documents": [
      {
        "family": "Batas Pambansa Blg. 344",
        "edition": "Revised IRR 2007",
        "effective_date": "2007-01-01",
        "status": "active"
      }
    ]
  }
}
```

### 5.3 GET /v2/standards?system=OmniClass&code=23-27%2011%2011

**Response:**
```json
{
  "system": "OmniClass",
  "code": "23-27 11 11",
  "title": "Ramps",
  "mappings": [
    {
      "canonical_id": "VTN-CON-0000042",
      "label": "Accessible Ramps",
      "confidence": 0.92,
      "mapped_by": "steward-accessibility"
    }
  ]
}
```

### 5.4 GET /v2/search?q=ramps&facets=knowledge_type:concept&jurisdiction=PH

**Response:**
```json
{
  "query": "ramps",
  "facets": { "knowledge_type": "concept" },
  "jurisdiction": "PH",
  "results": [
    {
      "canonical_id": "VTN-CON-0000042",
      "label": "Accessible Ramps",
      "path_code": "ACC.BFD.ROU.ARA",
      "primary_domain": "taxonomy-accessibility",
      "score": 0.95,
      "highlights": {
        "label": ["Accessible <em>Ramps</em>"],
        "summary": ["...accessible routes..."]
      }
    }
  ],
  "total": 1,
  "page": 1,
  "per_page": 20
}
```

---

## 6. Explorer UI

### 6.1 Taxonomy Tree

```
📁 Accessibility (ACC)
  📁 Barrier-Free Design (ACC.BFD)
    📁 Routes (ACC.BFD.ROU)
      📄 Accessible Ramps (ACC.BFD.ROU.ARA) ← selected
```

### 6.2 Node Detail Page

**Header:** Accessible Ramps `VTN-CON-0000042`

**Layer Badge:** 🔵 Canonical

**Facet Panel:**
| Facet | Value |
|-------|-------|
| Knowledge Type | Concept |
| Asset Scope | Building |
| Lifecycle Stage | Design |
| Project Type | Mixed Use |
| Performance Topic | Accessibility |
| Primary Domain | Accessibility |

**Jurisdiction Panel:**
| Jurisdiction | Obligation | Source |
|-------------|-----------|--------|
| Philippines (PH) | Mandatory: slope ≤ 1:12 | BP 344 Revised IRR 2007 |

**Standards Panel:**
| System | Code | Title | Confidence |
|--------|------|-------|------------|
| OmniClass | 23-27 11 11 | Ramps | 92% |

**Evidence Panel:**
| Source | Section | Snippet |
|--------|---------|---------|
| BP 344 Revised IRR 2007 | Section 1 | "Ramps shall be provided..." |

### 6.3 Search Results

**Search:** `ramps` + Facet: `knowledge_type:concept` + Jurisdiction: `Philippines`

**Result card:**
```
┌─────────────────────────────────────────┐
│ Accessible Ramps                        │
│ VTN-CON-0000042                         │
│ 🔵 Canonical | Accessibility | Design   │
│                                         │
│ Ramps provide accessible routes...      │
│                                         │
│ [PH] Mandatory: slope ≤ 1:12            │
│ OmniClass 23-27 11 11 (92%)             │
└─────────────────────────────────────────┘
```

---

## 7. Redirect Behavior

### 7.1 Old URL → New URL

**Old API request:**
```
GET /api/v1/node/concept-accessible-ramps
```

**Response (v1, additive):**
```json
{
  "id": "concept-accessible-ramps",
  "canonical_id": "VTN-CON-0000042",
  "label": "Accessible Ramps",
  /* ... rest of v1 fields unchanged ... */
}
```

**Old Explorer URL:**
```
/explorer/node/concept-accessible-ramps
```

**Behavior:** HTTP 308 Permanent Redirect to `/explorer/node/VTN-CON-0000042`

### 7.2 v2 API Request

```
GET /api/v2/node/VTN-CON-0000042
```

**Response:** Full v2 response (see §5.1).

### 7.3 v2 API Request with Old ID

```
GET /api/v2/node/concept-accessible-ramps
```

**Response:** HTTP 308 Permanent Redirect to `/api/v2/node/VTN-CON-0000042`

---

## 8. Migration Implications

### 8.1 What Happens During Migration

1. **Generate:** `migrate_to_v2.py` reads `concept-accessible-ramps.md`
2. **Transform:**
   - Generate `VTN-CON-0000042`
   - Remove `regulatory_basis` from frontmatter
   - Add facet fields
   - Add `path_code: ACC.BFD.ROU.ARA`
   - Add `id_redirect` field
   - Move file to `backbone/concepts/VTN-CON-0000042.md`
3. **Diff:** Git diff shows:
   - Old file deleted
   - New file created with new frontmatter
   - `id_redirect.csv` updated
4. **Review:** Steward reviews diff, confirms:
   - Definition unchanged
   - Facet assignments correct
   - Path code correct
   - Evidence links will be created post-migration
5. **Apply:** Move staging to canonical. Commit.
6. **Graph build:** Neo4j MERGE creates new nodes and edges.
7. **Parity check:** v1 query for `concept-accessible-ramps` returns same label, summary, taxonomy path.

### 8.2 Rollback Implications

If rollback is needed after "Accessible Ramps" migration:

1. **Run `rollback.py`:**
   - Restore `concept-accessible-ramps.md` from Git backup
   - Remove `VTN-CON-0000042.md`
   - Remove `canonical_id` property from Neo4j
   - Remove redirect record
2. **Rebuild graph:** Graph builder re-creates old node from restored Markdown
3. **Verify:** Parity check confirms v1 behavior restored

**Time to rollback:** 15 minutes (script + graph rebuild).

### 8.3 Shadow Graph Implications

During shadow graph build:

1. Shadow graph contains `VTN-CON-0000042` with all new labels/edges
2. Primary graph still contains `concept-accessible-ramps` with old labels/edges
3. Parity check: v1 query against primary graph == v1 query against shadow graph (via redirect)
4. Shadow read: v2 API reads from shadow graph; v1 API reads from primary graph
5. After 1-week observation: cutover — v1 API also reads from shadow graph (with backward-compatible response)

---

## 9. Validation Checklist

| Check | Method | Expected Result |
|-------|--------|-----------------|
| Old slug resolves to new ID | `GET /api/v2/node/concept-accessible-ramps` | HTTP 308 → `/api/v2/node/VTN-CON-0000042` |
| v1 endpoint still works | `GET /api/v1/node/concept-accessible-ramps` | Returns node with `canonical_id` additive field |
| Facet search works | `GET /v2/search?q=ramps&facets=knowledge_type:concept` | Includes `VTN-CON-0000042` |
| Jurisdiction resolution works | `POST /v2/resolve` with `PH-NCR-Makati` | Returns PH-level overlay (no local override) |
| Standards mapping works | `GET /v2/standards?system=OmniClass&code=23-27%2011%2011` | Returns `VTN-CON-0000042` |
| Evidence linkage works | Query Neo4j for `SUPPORTED_BY` edges from `VTN-CON-0000042` | Returns `VTN-EVS-0000001` |
| Overlay separation works | Query Neo4j for `HAS_OVERLAY` edges from `VTN-CON-0000042` | Returns `VTN-OVR-0000001` with PH jurisdiction |
| Backbone placement works | Query Neo4j for `BELONGS_TO_DOMAIN` from `VTN-CON-0000042` | Returns `ACC.BFD.ROU.ARA` |
| Parity check passes | `parity_check.py` | 100% match for all v1 query patterns |
| Rollback works | `rollback.py` + rebuild | v1 behavior fully restored |
