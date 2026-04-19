# 01 — Codebase Audit: Taxonomy Governance Readiness

> **Scope:** Full-repository evidence-based audit against the governed global AEC taxonomy architecture.
> **Date:** 2026-04-19
> **Auditor:** Kimi Code CLI
> **Authority:** `00_locked_decisions.md`, `.ai/13_research/governed taxonomy/`

---

## Executive Summary

**Observed:** Vitruvius is a mature pipeline with strong canonicalization governance, a working Neo4j KG v2, and a six-layer data architecture. The current taxonomy is a shallow three-level hierarchy (12 taxonomies → 24 topics → 55 subtopics → ~105 concepts) living in Markdown frontmatter at `003_Canonical-Knowledge-Layer/shared/`. IDs are semantic slugs (`concept-building-permit`). No jurisdiction entity, no standards mappings, no facet model, no localization.

**Inferred:** The pipeline and graph infrastructure can support the target model with moderate schema extensions. The taxonomy content, API contracts, and UI assumptions require bounded refactoring.

**Recommended:** Schema-first, backbone-second, shadow-graph-third, migration-last. Do not cut over without parity checks.

**Verdict:** Infrastructure is ready to extend. Content and contracts are not yet aligned.

---

## 1. Repository Map

```
/Users/philiplewis/vitruvius/
├── 001_Raw-Source-Layer/          # PDF/DOCX/PPTX raw sources (Philippine focus)
├── 001B_Spatial-Source-Layer/     # Empty except .gitkeep
├── 002_Raw-Conversion-Layer/      # Machine-extracted Markdown + JSON sidecars
├── 003_Canonical-Knowledge-Layer/ # Trusted knowledge pages
│   ├── 001-Laws/ … 009-Practice/  # Per-category stubs (index.md, log.md)
│   └── shared/                    # Taxonomy backbone + concepts + sources
│       ├── taxonomy/              # 12 top-level taxonomies
│       ├── topics/                # 24 second-level topics
│       ├── subtopics/             # 55 third-level subtopics
│       ├── concepts/              # ~105 leaf concept pages
│       ├── relationships/         # ~25 typed semantic edges
│       ├── sources/               # ~340 canonical source pages
│       └── glossary/              # 1 file (occupancy.md)
├── 004_Derived-Content-Layer/     # HTML graph viewers only
├── 005_Operational-Intelligence-Layer/
│   └── graph/kg-v2/               # 20+ timestamped JSON snapshots
├── 006_System-Manifests/          # Registries, migrations, run artifacts
├── api/                           # Hono + Neo4j BFF (api/index.ts, 545 lines)
├── explorer/                      # Vite + React + vis-network graph UI
├── scripts/                       # Python package (~230 .py files)
│   └── vitruvius/
│       ├── kg/                    # Neo4j loader, schemas, enums
│       ├── graph/                 # JSON snapshot builder, analytics
│       ├── review/                # LLM routing, MoE, CoT audit
│       ├── parsers/               # PDF/office ingestion
│       ├── rules/                 # canonical_rules.yaml, relationship_registry.yaml
│       └── …
├── spatial-daemon/                # TypeScript spatial contract engine
├── config/                        # vitruvius.yaml, moe_routing.yaml, datasets/
└── .ai/                           # Operating system for governance, plans, state
```

**Key evidence paths:**
- `api/index.ts:1-545` — entire API surface
- `explorer/src/components/ExplorerRail.tsx:1-120` — taxonomy tree + hardcoded filters
- `explorer/src/types/index.ts` — TypeScript graph interfaces
- `scripts/vitruvius/kg/neo4j_schema.cypher` — Neo4j constraints and indexes
- `scripts/vitruvius/kg/enums.py` — NodeType, EdgeType, ValidationState
- `scripts/vitruvius/kg/schemas.py` — Pydantic KG schemas
- `scripts/vitruvius/graph/builder.py` — JSON graph snapshot builder
- `scripts/vitruvius/canonicalize.py` — canonical ID validation
- `config/vitruvius.yaml` — hardcoded categories and feature flags
- `.ai/06_specs/canonicalization/CANONICAL_ID_STANDARD.md` — ID format spec
- `.ai/06_specs/canonicalization/CANONICALIZATION_RULES.md` — page types and trust hierarchy

---

## 2. Machine-Readable Audit Artifacts

The following artifacts must be generated and committed to `006_System-Manifests/audits/taxonomy-governance/` before any migration PR is approved.

| Artifact | Purpose | Generator | Output Format |
|----------|---------|-----------|---------------|
| `node_inventory.csv` | Every node in canonical layer with ID, type, taxonomy_path, status | `scripts/vitruvius/graph/builder.py` | CSV |
| `edge_inventory.csv` | Every edge in KG v2 snapshots with source, target, type | `scripts/vitruvius/kg/canonical_graph_builder.py` | CSV |
| `hardcoded_constants_inventory.json` | All hardcoded strings in API, UI, and configs | Static analysis script | JSON |
| `legacy_id_usage_report.csv` | Every file reference to old semantic slug IDs | Grep across repo | CSV |
| `frontmatter_field_inventory.csv` | All unique frontmatter keys across canonical Markdown | YAML parser script | CSV |
| `api_surface_inventory.json` | All routes, params, response shapes in `api/index.ts` | AST extraction or manual | JSON |

**Observed:** None of these artifacts exist yet. They must be produced in Phase 0.

---

## 3. Current Architecture Narrative

### 3.1 Data Flow

**Observed:** Raw sources (PDFs) → conversion (Markdown/JSON) → canonicalization (Markdown with YAML frontmatter) → promotion (`003_Canonical-Knowledge-Layer/shared/`) → graph build (JSON snapshot or Neo4j MERGE) → Explorer UI.

**Inferred:** This flow is deterministic and well-governed, but the canonicalization step conflates subject taxonomy, knowledge type, and regulatory evidence in one frontmatter block.

**Recommended:** Separate the canonicalization step into:
1. Canonical node creation (global meaning + facets)
2. Evidence linkage (`SUPPORTED_BY` edges)
3. Jurisdiction overlay creation (applicability rules)

### 3.2 Canonicalization Governance

**Observed:** Trust levels (primary/secondary/tertiary/unverified/derived), review queues, promotion validators, and audit trails exist.

**Inferred:** Governance is tuned for Philippine regulatory content and does not generalize to multi-jurisdiction.

**Recommended:** Extract Philippine rules into `jurisdiction/PH/` packs. Generalize rule schema to support `authority` + `jurisdiction` + `edition`.

### 3.3 Storage Architecture

| Store | Role | Technology | Assessment |
|-------|------|------------|------------|
| Canonical source of truth | Editorial content + taxonomy | Git-tracked Markdown/YAML | **Reuse** — aligned with target |
| Operational registry | Pipeline runs, file hashes, review queues | PostgreSQL 16 | **Reuse** — add new tables |
| Knowledge graph | Runtime nodes, edges, evidence | Neo4j 5.26 Community | **Reuse** — extend schema |
| Code intelligence | Symbol graph for agent navigation | SQLite 3 | **Reuse** — orthogonal |
| Search index | None dedicated; Cypher `CONTAINS` | Neo4j label indexes | **Extend** — add FTS |

**Observed:** No dedicated search index. Search is substring matching.

**Recommended:** Add Neo4j full-text index `canonicalSearch` on `label`, `aliases`, `summary`, `path_code`.

---

## 4. Current Taxonomy Implementation Map

### 4.1 Where the Taxonomy Lives

**Observed:** Markdown frontmatter in:
- `003_Canonical-Knowledge-Layer/shared/taxonomy/` (12 files)
- `003_Canonical-Knowledge-Layer/shared/topics/` (24 files)
- `003_Canonical-Knowledge-Layer/shared/subtopics/` (55 files)
- `003_Canonical-Knowledge-Layer/shared/concepts/` (~105 files)

**Inferred:** Editorial content, not compiled schema. Graph builder reads frontmatter and projects into Neo4j.

**Recommended:** Keep Markdown/YAML as editorial format. Move backbone to `003_Canonical-Knowledge-Layer/backbone/`. Migrate concepts to new facet schema.

### 4.2 Frontmatter Patterns

**Observed (taxonomy root):**
```yaml
id: taxonomy-architecture
title: Architecture
page_type: taxonomy
canonical_status: validated
trust_level: primary
```

**Observed (concept leaf):**
```yaml
id: concept-accessible-ramps
title: Accessible Ramps
page_type: concept
canonical_status: enriched
regulatory_basis:
- source_id: irr-revised-implementing-rules-and-regulations-of-batas-pambansa-blg-344
  section_id: section-1
  evidence_snippet: "..."
taxonomy_path:
- taxonomy-accessibility
- topic-barrier-free-design
- subtopic-routes
```

**Inferred:** `regulatory_basis` is embedded inside the concept node. This collapses canonical meaning with local obligation.

**Recommended:** Remove `regulatory_basis` from concept frontmatter. Replace with `SUPPORTED_BY` edges to `EvidenceSpan` nodes + jurisdiction overlay records.

### 4.3 Structural Issue: Mixed Axes

**Observed:** The current taxonomy mixes three axes at the same level:
- **Subject domain:** `taxonomy-accessibility`, `taxonomy-architecture`, `taxonomy-fire-life-safety`
- **Knowledge type:** `concept`, `rule`, `definition`, `procedure`, `exception`
- **Regulatory form:** `law`, `irr`, `handout`, `reviewer`

**Inferred:** This is exactly the anti-pattern the target architecture prohibits.

**Recommended:**
- Subject domain → `primary_domain` backbone (15 L1 domains, L2–L4 depth)
- Knowledge type → `knowledge_type` facet
- Regulatory form → `AuthorityDocumentFamily` / `AuthorityDocumentEdition` entities

### 4.4 Graph Node Labels and Properties

**Observed:**
- Labels: `CanonicalNode`, `Taxonomy`, `Topic`, `Subtopic`, `DocumentVersion`, `Section`, `Chunk`, `EvidenceSpan`
- Properties: `id`, `label`, `type`, `kind`, `summary`, `slug`, `status`, `confidence`, `aliases`, `taxonomy_path`, `created_at`, `updated_at`

**Inferred:** `DocumentVersion` is source-oriented (`sha256`, `source_path`, `extraction_method`), not normative-edition-oriented.

**Recommended:**
- Keep `DocumentVersion` for extraction artifacts
- Create `AuthorityDocumentEdition` for normative code/standard editions
- Add facet properties to `CanonicalNode`
- Add `canonical_id`, `path_code`, `release_version`, `steward`

### 4.5 Edge Types

**Observed:** `HAS_CHILD`, `BELONGS_TO`, `RELATED_TO`, `DEFINED_BY`, `DEPENDS_ON`, `REQUIRES`, `APPLIES_TO`, `OVERRIDES`, `CONTRADICTS`, `SAME_AS`, `PART_OF`, `SUPPORTED_BY`, `EXCLUDES`

**Recommended additions:**
- `MAPS_TO_STANDARD` — standards crosswalk
- `APPLIES_IN` — jurisdiction applicability
- `HAS_OVERLAY` — jurisdictional overlay
- `SUPERSEDES` / `SUPERSEDED_BY` — edition lifecycle
- `WITHIN_JURISDICTION` — jurisdiction hierarchy
- `BELONGS_TO_DOMAIN` — backbone classification

---

## 5. Region / Standards / Regulatory Handling

### 5.1 Jurisdiction

**Observed:** No explicit jurisdiction model. Jurisdiction is implicit in:
1. Folder paths (`001_Raw-Source-Layer/001-Laws/LGU/davao/`)
2. Canonical source IDs (`law-national-building-code-of-the-philippines`)
3. `regulatory_basis.source_id` inside concept frontmatter

**Evidence:**
- `explorer/src/components/HomeScreen.tsx:24` — "Explore concepts, rules, and evidence across Philippine building codes."
- `scripts/vitruvius/rules/canonical_rules.yaml` — 1,186 lines of Philippine law rules
- `config/vitruvius.yaml` — `k_jurisdictional_overrides: false`, `k_rosetta_stone: false`

**Inferred:** The system is single-jurisdiction (Philippines) by design, not by limitation.

**Recommended:** Build explicit `Jurisdiction` model. Convert implicit folder paths to explicit jurisdiction packs (`config/jurisdictions/PH.yaml`, `PH-MetroManila.yaml`).

### 5.2 Standards and Code Editions

**Observed:** No structured standards mapping. External classification systems (OmniClass, Uniclass, IFC, MasterFormat, ICC, NFPA, Eurocode) are not referenced.

**Evidence:**
- Grep `OmniClass`, `Uniclass`, `IFC`, `MasterFormat`, `Eurocode` in `003_Canonical-Knowledge-Layer/` = 0 matches
- `.ai/06_specs/canonicalization/CANONICAL_ID_STANDARD.md` — 9 prefixes: `law`, `irr`, `concept`, `glossary`, `relationship`, `handout`, `reviewer`, `law-section`, `source`

**Recommended:** Create `StandardReference` and `StandardMapping` schemas. Seed with sample crosswalks.

### 5.3 DocumentVersion vs DocumentEdition

**Observed:** `DocumentVersion` exists with properties: `sha256`, `source_path`, `extraction_method`.

**Inferred:** This models the extraction artifact (PDF → Markdown), not the normative edition.

**Recommended:** Create separate `AuthorityDocumentEdition` entity for code/standard editions. Preserve `DocumentVersion` for extraction artifacts. See `07_golden_example.md` §2.3 for concrete separation.

### 5.4 Localization

**Observed:** No locale support. All content is English.

**Evidence:** Grep `locale`, `i18n`, `lang`, `translation` in `explorer/` and `api/` = no relevant matches.

**Recommended:** Add `Localization` schema. Defer to v1.1.

---

## 6. Application Behavior Assessment

### 6.1 Explorer UI

**Observed:**
- `ExplorerRail.tsx` fetches `/taxonomy`, renders recursive `TreeItem`
- Hardcoded `NODE_TYPES` array of 8 types (`explorer/src/components/ExplorerRail.tsx:49-58`)
- Hardcoded `EDGE_TYPES` array of 7 types (`explorer/src/components/ExplorerRail.tsx:60-68`)
- `HomeScreen.tsx:24` hardcodes "Philippine building codes"

**Inferred:** UI assumes a single taxonomy tree with a fixed set of node/edge types.

**Recommended:**
- Make `NODE_TYPES` dynamic from `knowledge_type` + `primary_domain`
- Add `FacetPanel`, `JurisdictionSelector`, `LayerBadge` components
- Preserve legacy tree rendering during transition

### 6.2 API

**Observed:**
- `/taxonomy` returns `TaxonomyNode[]` with `kind: 'taxonomy' | 'topic' | 'subtopic'`
- `/search` does `CONTAINS` on `c.label` and `c.id` (`api/index.ts:92-127`)
- Perspectives hardcode type predicates (`api/index.ts:438-446`)

**Inferred:** No endpoints for jurisdiction, standards, facet search, date-aware retrieval.

**Recommended:** Add `/v2/` routes. Keep v1 routes additive-only.

### 6.3 Search / Retrieval

**Observed:** Substring `CONTAINS` search capped at 100 results.

**Recommended:** Add Neo4j FTS + facet filtering + jurisdiction precedence ranking.

---

## 7. Migration Feasibility

### 7.1 Reuse As-Is

| Component | Assessment |
|-----------|------------|
| Six-layer data architecture | **Reuse** — aligned with target |
| Neo4j graph store + driver | **Reuse** — extensible |
| PostgreSQL registry | **Reuse** — add tables |
| Pipeline CLI + feature flags | **Reuse** — gate new work |
| Evidence graph (`SUPPORTED_BY`, `EvidenceSpan`) | **Reuse** — already correct |
| Assertion layer | **Reuse** — extend for standards mappings |

### 7.2 Adapt with Moderate Effort

| Component | Adaptation |
|-----------|------------|
| `CanonicalNode` schema | Add facet fields, `path_code`, `canonical_id`, `release_version`, `steward` |
| Neo4j schema | Add labels/edges for jurisdiction, standards, overlays |
| Graph builder | Read new frontmatter fields, emit new node/edge types |
| API | Add `/v2/` routes, extend existing routes with optional facet params |
| Explorer types | Add new interface fields |
| Explorer UI | Add facet filters, jurisdiction selector; keep backward-compatible tree |

### 7.3 Structurally Wrong — Do Not Preserve

| Component | Why It Must Change |
|-----------|-------------------|
| Semantic slug IDs | Mutable, non-opaque, break on rename |
| Three-level taxonomy as only hierarchy | Too shallow; mixes axes |
| Hardcoded node-type lists in API/UI | Assumes closed world of 8 types |
| `taxonomy_path` array of semantic IDs | Breaks when IDs change |
| Philippine-only perspective in UI | `HomeScreen.tsx:24` hardcodes jurisdiction |
| `regulatory_basis` inside concept frontmatter | Collapses canonical meaning with local obligation |

### 7.4 What Breaks If Backbone Is Frozen

1. **Explorer taxonomy tree** — needs to consume new backbone. Preserve old labels as legacy aliases.
2. **Graph snapshots** — historical artifacts; can be left as-is or rebuilt.
3. **Neo4j graph** — old nodes deprecated with `SUPERSEDED` status and `SUPERSEDES` edges.
4. **API consumers** — v1 endpoints receive additive fields only; old clients ignore them.
5. **Canonical source documents** — ~340 source pages + ~105 concept pages need frontmatter migration.

---

## 8. Risk Register (Preliminary)

| ID | Risk | Severity | Evidence |
|----|------|----------|----------|
| R1 | Changing canonical IDs breaks graph references | 🔴 Critical | `api/index.ts` uses `id` as PK; `taxonomy_path` arrays contain old IDs |
| R2 | Explorer UI breaks if node types change | 🔴 Critical | `ExplorerRail.tsx` hardcodes 8 node types |
| R3 | Philippine rules do not generalize | 🟠 High | `canonical_rules.yaml` is 1,186 lines of Philippine law |
| R4 | Search regression without index | 🟠 High | Current search is Cypher `CONTAINS` |
| R5 | Governance gap: no backbone change process | 🟠 High | No steward assignment, no PRD |
| R6 | Data loss if old nodes deleted | 🟠 High | No redirect field yet |
| R7 | AI corrupts backbone | 🟠 High | Post-migration AI policy must be explicit |
| R8 | Performance: jurisdiction resolution | 🟡 Medium | No precedence engine |
| R9 | Operational complexity of jurisdiction packs | 🟡 Medium | Must separate release artifacts |
| R10 | Standards mapping ambiguity | 🟡 Medium | No confidence thresholding yet |

---

## 9. Unknowns / Ambiguities

| ID | Unknown | Why It Matters | Resolution Path |
|----|---------|---------------|-----------------|
| U1 | Is current `Taxonomy` label becoming `primary_domain` backbone? | Determines migration strategy | **Resolved by LD-1:** New backbone in `003_Canonical-Knowledge-Layer/backbone/`; old `Taxonomy`/`Topic`/`Subtopic` become legacy aliases |
| U2 | Do 12 existing taxonomies map to target L1 domains? | Some align, others are regulatory forms | **Resolved by LD-10:** Home-domain assignment rulebook defines mapping |
| U3 | Cardinality of `taxonomy_path`? Currently exactly 3. | Affects graph builder and UI | **Resolved:** New model uses `path_code` (dot-delimited string) and graph edges (`BELONGS_TO_DOMAIN`) |
| U4 | Does `DocumentVersion` model code editions? | It is source-oriented, not normative | **Resolved by I6:** Separate `DocumentVersion` (artifact) from `AuthorityDocumentEdition` (normative) |
| U5 | Is embedding pipeline active? | `embedding_ref` is null on all nodes | **Deferred:** Semantic search is v1.1 |
| U6 | Production deployment model? | Affects migration downtime | **Unknown:** Must be documented in Phase 0 |
| U7 | External API consumers beyond Explorer? | Affects backward-compatibility requirements | **Unknown:** Must be documented in Phase 0 |

---

## 10. File-Path Evidence Index

| Claim | Evidence Files | Observation Type |
|-------|---------------|-----------------|
| Taxonomy lives in Markdown frontmatter | `003_Canonical-Knowledge-Layer/shared/taxonomy/*.md`, `topics/*.md`, `subtopics/*.md`, `concepts/*.md` | Observed |
| IDs are semantic slugs | `.ai/06_specs/canonicalization/CANONICAL_ID_STANDARD.md`; `scripts/vitruvius/canonicalize.py` | Observed |
| No jurisdiction entity | Grep `jurisdiction` in `003_Canonical-Knowledge-Layer/` returns no structured entity | Observed |
| No standards mappings | Grep `OmniClass`, `Uniclass`, `IFC`, `MasterFormat`, `Eurocode` in repo returns no data-layer matches | Observed |
| Hardcoded node types in API | `api/index.ts:438-446` (perspectives), `:92-127` (search filters) | Observed |
| Hardcoded node types in UI | `explorer/src/components/ExplorerRail.tsx:49-58` (NODE_TYPES) | Observed |
| Philippine-only focus | `explorer/src/components/HomeScreen.tsx:24`; `scripts/vitruvius/rules/canonical_rules.yaml` | Observed |
| Feature flags for future features | `config/vitruvius.yaml` (`k_jurisdictional_overrides: false`, `k_rosetta_stone: false`, `taxonomy_seeding: false`) | Observed |
| Graph schema definitions | `scripts/vitruvius/kg/neo4j_schema.cypher`, `scripts/vitruvius/kg/enums.py`, `scripts/vitruvius/kg/schemas.py` | Observed |
| Pipeline CLI | `scripts/pipeline_cli.py` | Observed |
| Graph builder | `scripts/vitruvius/graph/builder.py`, `scripts/vitruvius/kg/canonical_graph_builder.py` | Observed |
| Canonical rules | `scripts/vitruvius/rules/canonical_rules.yaml` | Observed |
| API types | `explorer/src/types/index.ts` | Observed |
| Six-layer config | `config/vitruvius.yaml` | Observed |
| `DocumentVersion` is source-oriented | `scripts/vitruvius/kg/schemas.py` — `sha256`, `source_path`, `extraction_method` | Observed |
| `regulatory_basis` collapses canonical and local meaning | `003_Canonical-Knowledge-Layer/shared/concepts/concept-accessible-ramps.md` | Observed |
| Current taxonomy mixes axes | `003_Canonical-Knowledge-Layer/shared/taxonomy/*.md` contains both subject domains and regulatory forms | Inferred |
| Pipeline can support target model | Feature flags, assertion layer, evidence graph are extensible | Inferred |
| UI assumes single jurisdiction | `HomeScreen.tsx:24` hardcodes "Philippine building codes" | Inferred |
