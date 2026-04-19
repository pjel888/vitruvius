# Schema Contract — Taxonomy Governance v2 + Vitruvian Context

> **Type:** Implementation contract (Tier 1)
> **Date:** 2026-04-19
> **Authority:** `00_locked_decisions.md` (LD-1, LD-2, LD-11, LD-12)

---

## Purpose

This document is the **implementation contract** between planning and engineering. It specifies:

1. **Pydantic schemas** for all new data models
2. **Neo4j schema** (labels, properties, constraints, indexes, FTS)
3. **Feature flag wiring** (config definitions, Python accessors, environment overrides)

Any PR that changes these contracts must update this document and all three artifact files.

---

## Artifact Map

| Artifact | Path | Format |
|----------|------|--------|
| Pydantic schemas | `scripts/vitruvius/kg/taxonomy_v2_schemas.py` | Python (Pydantic v2) |
| Neo4j schema | `scripts/vitruvius/kg/neo4j_schema_v2.cypher` | Cypher |
| Feature flags | `scripts/vitruvius/config_flags.py` | Python |
| Config YAML | `config/vitruvius.yaml` | YAML |

---

## 1. Pydantic Schemas

### 1.1 Facet Enums (Closed Vocabularies)

| Enum | Values | Used By |
|------|--------|---------|
| `KnowledgeType` | concept, rule, definition, procedure, exception, principle | `CanonicalNodeV2` |
| `AssetScope` | building, infrastructure, site, system, component, material | `CanonicalNodeV2` |
| `LifecycleStage` | planning, design, construction, operation, demolition, reuse | `CanonicalNodeV2` |
| `ProjectType` | residential, commercial, industrial, institutional, public_works, mixed_use | `CanonicalNodeV2` |
| `PerformanceTopic` | structural, fire_life_safety, accessibility, sustainability, energy, acoustics, daylight, ventilation, water, durability | `CanonicalNodeV2` |
| `JurisdictionLevel` | project_specific, local, agency, regional, state, national, supranational, international | `Jurisdiction` |
| `ObligationType` | mandatory, recommended, permitted, prohibited | `Overlay` |
| `MappingType` | exact, narrower, broader, related | `StandardMapping` |

**Rule:** These enums are closed. Adding a value requires:
1. Update the Literal type in `taxonomy_v2_schemas.py`
2. Update the Neo4j index (if indexed)
3. Update the validation script
4. Update this document

### 1.2 BackboneNode

```python
class BackboneNode(BaseModel):
    canonical_id: str   # VTN-DOM-#######
    path_code: str      # ACC.BFD.ROU.ARA
    level: int          # 1–4
    parent_path_code: str | None
    pref_label: str
    definition: str     # min_length=10
    aliases: list[str]
    scope_note: str
    example_concepts: list[str]
    steward: str
    release_version: str  # semver
```

**Validation:**
- `canonical_id` must match `^VTN-DOM-\d{7}$`
- `path_code` must match `^[A-Z]{3}(\.[A-Z]{3}){0,3}$`
- `parent_path_code` part count must equal `level - 1`

### 1.3 CanonicalNodeV2

Extends the existing `CanonicalNode` with facet fields and governance metadata.

```python
class CanonicalNodeV2(BaseModel):
    canonical_id: str           # VTN-CON-#######
    path_code: str              # ACC.BFD.ROU.ARA
    label: str
    summary: str
    knowledge_type: KnowledgeType
    asset_scope: AssetScope
    lifecycle_stage: LifecycleStage
    project_type: ProjectType
    performance_topic: PerformanceTopic
    primary_domain: str         # e.g., taxonomy-accessibility
    status: str                 # draft | enriched | verified | superseded
    steward: str
    release_version: str        # semver
    trust_level: str            # primary | secondary | tertiary | unverified | derived
    confidence: float           # 0.0–1.0
    created_at: datetime
    updated_at: datetime
```

**Migration note:** Existing `CanonicalNode` nodes keep their `id` (semantic slug) and gain `canonical_id` (opaque ID) additively. No breaking changes.

### 1.4 IdRedirect

```python
class IdRedirect(BaseModel):
    old_id: str
    new_id: str                 # VTN-XXX-#######
    scope: str                  # concept | source | relationship | taxonomy | backbone
    reason: str
    redirect_type: str          # permanent | temporary
    created_at: datetime
```

### 1.5 Jurisdiction

```python
class Jurisdiction(BaseModel):
    code: str                   # e.g., PH-NCR-Makati
    name: str
    level: JurisdictionLevel
    precedence_rank: int        # 0–6
    parent_code: str | None
    metadata: dict
```

**Precedence ranks (locked):**
| Rank | Level | Example |
|------|-------|---------|
| 0 | project_specific | PROJ-123 |
| 1 | local | PH-NCR-Makati |
| 2 | agency | PH-DPWH |
| 3 | regional | PH-NCR |
| 4 | national | PH |
| 5 | supranational | ASEAN |
| 6 | international | ISO |

### 1.6 Authority Document Models

**Authority:**
```python
class Authority(BaseModel):
    canonical_id: str           # VTN-AUT-#######
    name: str
    short_name: str
    jurisdiction_code: str
    url: str
    metadata: dict
```

**AuthorityDocumentFamily:**
```python
class AuthorityDocumentFamily(BaseModel):
    canonical_id: str           # VTN-ADF-#######
    title: str
    short_title: str
    jurisdiction_code: str
    authority_id: str           # VTN-AUT-#######
    metadata: dict
```

**AuthorityDocumentEdition:**
```python
class AuthorityDocumentEdition(BaseModel):
    canonical_id: str           # VTN-ADE-#######
    family_id: str              # VTN-ADF-#######
    edition_number: str
    effective_date: date
    repeal_date: date | None
    status: str                 # draft | active | superseded | repealed
    jurisdiction_code: str
    metadata: dict
```

**Validation:** `repeal_date` must be strictly after `effective_date`.

### 1.7 ApplicabilityRule + Overlay

**ApplicabilityRule:**
```python
class ApplicabilityRule(BaseModel):
    canonical_id: str           # VTN-APP-#######
    jurisdiction_code: str
    scope: str
    precedence_rank: int        # 0–6
    condition: str
    effective_date: date
    status: str                 # active | inactive
    edition_id: str             # VTN-ADE-#######
```

**Overlay:**
```python
class Overlay(BaseModel):
    canonical_id: str           # VTN-OVR-#######
    concept_id: str             # VTN-CON-#######
    jurisdiction_code: str
    obligation_type: ObligationType
    condition: str
    measurement: str
    effective_date: date
    repeal_date: date | None
    status: str                 # active | inactive
    edition_id: str             # VTN-ADE-#######
    confidence: float           # 0.0–1.0
```

### 1.8 Standards

**StandardReference:**
```python
class StandardReference(BaseModel):
    canonical_id: str           # VTN-STD-#######
    system: str                 # e.g., OmniClass, Uniclass, IFC
    code: str
    title: str
    url: str
    version: str
```

**StandardMapping:**
```python
class StandardMapping(BaseModel):
    canonical_id: str           # VTN-CON-#######
    standard_id: str            # VTN-STD-#######
    mapping_type: MappingType
    confidence: float           # 0.0–1.0
    mapped_by: str
    mapped_at: datetime
```

### 1.9 Resolution I/O (Vitruvian Context)

**ResolutionContext:**
```python
class ResolutionContext(BaseModel):
    jurisdiction_code: str
    query_date: date
    project_type: ProjectType | None
    asset_scope: AssetScope | None
    lifecycle_stage: LifecycleStage | None
    user_overrides: dict        # e.g., {"confidence_threshold": 0.85}
```

**CanonicalQuery:**
```python
class CanonicalQuery(BaseModel):
    concept_id: str | None      # VTN-CON-#######
    path_code: str | None       # ACC.BFD.ROU.ARA
    search_text: str | None
    return_type: str            # concept | overlay | evidence | standards | full
    facets: FacetFilter | None
    expand_domains: list[str] | None
    max_hops: int               # 1–5, default 2
```

**ResolvedTruth:**
```python
class ResolvedTruth(BaseModel):
    canonical_concept: CanonicalNodeV2
    resolution: dict
    influences: dict
    evidence: list[dict]
    standards_mappings: list[StandardMapping]
    reasoning_trace: list[ReasoningStep]
    query: CanonicalQuery
    context: ResolutionContext
    resolved_at: datetime
```

### 1.10 CrossDisciplineEdge

```python
class CrossDisciplineEdge(BaseModel):
    from_id: str                # VTN-CON-#######
    to_id: str
    edge_type: str              # must be in ALLOWED_CROSS_DISCIPLINE_PREDICATES
    from_domain: str
    to_domain: str
    confidence: float           # 0.0–1.0
    rationale: str
    valid_from: date | None
    valid_until: date | None
```

---

## 2. Neo4j Schema v2

### 2.1 New Constraints

| Label | Property | Constraint |
|-------|----------|------------|
| `BackboneNode` | `canonical_id` | UNIQUE |
| `Jurisdiction` | `code` | UNIQUE |
| `Authority` | `canonical_id` | UNIQUE |
| `AuthorityDocumentFamily` | `canonical_id` | UNIQUE |
| `AuthorityDocumentEdition` | `canonical_id` | UNIQUE |
| `ApplicabilityRule` | `canonical_id` | UNIQUE |
| `Overlay` | `canonical_id` | UNIQUE |
| `StandardReference` | `canonical_id` | UNIQUE |
| `CanonicalNode` | `canonical_id` | UNIQUE (new, additive) |

### 2.2 New Indexes

| Label | Property | Purpose |
|-------|----------|---------|
| `BackboneNode` | `path_code` | Lookup by path |
| `BackboneNode` | `level` | Filter by depth |
| `BackboneNode` | `parent_path_code` | Tree traversal |
| `CanonicalNode` | `primary_domain` | Facet filtering |
| `CanonicalNode` | `knowledge_type` | Facet filtering |
| `CanonicalNode` | `asset_scope` | Facet filtering |
| `CanonicalNode` | `lifecycle_stage` | Facet filtering |
| `CanonicalNode` | `project_type` | Facet filtering |
| `CanonicalNode` | `performance_topic` | Facet filtering |
| `Jurisdiction` | `precedence_rank` | Precedence sorting |
| `Jurisdiction` | `parent_code` | Hierarchy traversal |
| `AuthorityDocumentEdition` | `family_id` | Family lookup |
| `AuthorityDocumentEdition` | `effective_date` | Temporal queries |
| `AuthorityDocumentEdition` | `status` | Active filter |
| `Overlay` | `concept_id` | Concept overlay lookup |
| `Overlay` | `jurisdiction_code` | Jurisdiction overlay lookup |
| `Overlay` | `effective_date` | Temporal queries |
| `StandardReference` | `system, code` | Composite lookup |
| `StandardMapping` | `canonical_id` | Concept mapping lookup |

### 2.3 Full-Text Search

```cypher
CREATE FULLTEXT INDEX canonicalSearch IF NOT EXISTS
    FOR (n:CanonicalNode)
    ON EACH [n.label, n.aliases, n.summary, n.path_code];
```

**Query pattern:**
```cypher
CALL db.index.fulltext.queryNodes("canonicalSearch", "accessible ramps") YIELD node, score
RETURN node.canonical_id, node.label, score
```

### 2.4 Edge Conventions

Neo4j Community does not support relationship constraints. These are documented conventions:

| Edge | Source → Target |
|------|-----------------|
| `BELONGS_TO_DOMAIN` | CanonicalNode → BackboneNode |
| `HAS_PARENT` | BackboneNode → BackboneNode |
| `WITHIN_JURISDICTION` | Jurisdiction → Jurisdiction |
| `HAS_EDITION` | AuthorityDocumentFamily → AuthorityDocumentEdition |
| `SUPERSEDES` | AuthorityDocumentEdition → AuthorityDocumentEdition |
| `APPLIES_IN` | ApplicabilityRule → Jurisdiction |
| `GOVERNS` | ApplicabilityRule → AuthorityDocumentEdition |
| `HAS_OVERLAY` | CanonicalNode → Overlay |
| `BASED_ON` | Overlay → AuthorityDocumentEdition |
| `APPLIES_IN` | Overlay → Jurisdiction |
| `SUPPORTED_BY` | CanonicalNode → EvidenceSpan |
| `MAPS_TO_STANDARD` | CanonicalNode → StandardReference |
| `CONSTRAINS`, `AFFECTS`, `REQUIRES`, `INFLUENCES`, `USED_IN`, `EXECUTED_IN`, `REGULATED_BY` | CanonicalNode → CanonicalNode or CanonicalNode → BackboneNode |

---

## 3. Feature Flag Wiring

### 3.1 Config Definitions

```yaml
# config/vitruvius.yaml
features:
  # ... existing streams A–H ...
  # Stream K — Taxonomy Governance + Vitruvian Context
  k_taxonomy_v2: false
  k_jurisdictional_overrides: false
  k_standards_mapping: false
  k_vitruvian_context: false
  k_shadow_read: false
  k_backbone_validation: false
```

### 3.2 Python Accessor

```python
from vitruvius.config_flags import flags

if flags.taxonomy_v2:
    # Serve v2 taxonomy tree
    
if flags.vitruvian_context:
    # Enable POST /v2/resolve
```

### 3.3 Environment Override

For CI or local testing:
```bash
export VITRUVIUS_FLAGS="k_taxonomy_v2:true,k_vitruvian_context:true"
python scripts/pipeline_cli.py run
```

### 3.4 Flag Behavior Matrix

| Flag | What it gates | PR | Default |
|------|--------------|-----|---------|
| `k_taxonomy_v2` | All v2 API routes, Explorer v2 UI, shadow graph | PR-11, PR-12 | `false` |
| `k_jurisdictional_overrides` | Jurisdiction resolution, overlay filtering, `POST /v2/resolve` jurisdiction params | PR-02c, PR-08 | `false` |
| `k_standards_mapping` | `GET /v2/standards`, standards panel in Explorer | PR-04, PR-09 | `false` |
| `k_vitruvian_context` | `POST /v2/resolve`, reasoning trace, affected disciplines panel | PR-17, PR-18 | `false` |
| `k_shadow_read` | API v2 reads from shadow graph instead of primary graph | PR-14 | `false` |
| `k_backbone_validation` | CI gate: fail build if backbone files are invalid | PR-01 | `false` |

### 3.5 Rollout Sequence

```
1. k_backbone_validation = true   (PR-01 — immediate, validates backbone edits)
2. k_taxonomy_v2 = true           (PR-14 — after shadow parity passes)
3. k_jurisdictional_overrides = true  (PR-08 — after PH pack validated)
4. k_standards_mapping = true     (PR-09 — after seed mappings reviewed)
5. k_vitruvian_context = true     (PR-17 — after resolver test cases pass)
6. k_shadow_read = true           (PR-14 — toggles primary vs shadow graph)
```

---

## 4. Validation Checklist

Before any PR that touches these contracts:

- [ ] Pydantic schemas pass `mypy scripts/vitruvius/kg/taxonomy_v2_schemas.py`
- [ ] All schemas export valid JSON Schema via `model_json_schema()`
- [ ] Neo4j Cypher runs without error on empty database
- [ ] Feature flags are readable by `scripts/vitruvius/config_flags.py`
- [ ] Config YAML passes `yaml.safe_load()` without errors
- [ ] New enum values are added to both Pydantic and Neo4j schema
- [ ] ID format regexes match `VTN-<kind>-<7 digits>` from LD-2
- [ ] This document (`04_schema_contract.md`) is updated
