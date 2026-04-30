# Read-Only Advisory: Source-Safe Architecture Evidence Paths

> **Scope:** Vitruvius AEC-MEPFS file-backed backbone (shadow staging run `20260430T070501Z`)  
> **Baseline:** 9,761 nodes / 12,495 governed relationships  
> **Advisory type:** Read-only; no graph mutation, no protected payload admission  
> **Generated:** 2026-04-30  
> **Authority:** `.ai/01_roadmap/current-phase.md` — AEC-MEPFS Backbone Readiness Gate

---

## 1. Executive Summary

This advisory proposes **source-safe, project-specific architecture evidence paths** for a curated set of globally significant architects, a regional vernacular tradition, and four primary construction materials. All paths respect the existing backbone model that **avoids direct person-to-material edges** (verified: 0 direct architect-to-material edges exist for all 7 target persons).

The proposed paths use the **governed predicate vocabulary** (`broader_than`, `has_facet`, `maps_to_external_standard`, `requires`, `constrains`) and the **VTN canonical ID namespace** (`VTN-DOM-XXXXXXXX`). No protected source text is quoted. All source-rights cautions are drawn from the live source-rights registry (102 entries, `shadow-backbone-staging.json`).

---

## 2. Existing Model Verification

### 2.1 Baseline Graph Metrics
| Metric | Value |
|--------|-------|
| Total nodes | 9,761 |
| Total edges | 12,495 |
| Predicates | 10 (`broader_than`, `has_facet`, `maps_to_external_standard`, `requires`, `constrains`, `governs`, `part_of`, `applicable_in_jurisdiction`, `conflicts_with`, `supersedes`) |
| Person nodes | 118 (path root `FIG.PTE` / `FIG.ARD`) |
| Work nodes | 69 (path root `FIG.WRK`) |
| Material nodes | 428 (path root `MAT` / `ARC.MAT`) |
| Direct person-to-material edges | **0** |

### 2.2 Model Invariant: No Direct Person-Material Edges
All 7 target architects were verified for direct material edges:

| Architect | VTN ID | Direct Material Edges |
|-----------|--------|----------------------|
| Santiago Calatrava | VTN-DOM-0012458 | 0 |
| Zaha Hadid | VTN-DOM-0012443 | 0 |
| Tadao Ando | VTN-DOM-0012446 | 0 |
| Frei Otto | VTN-DOM-0012434 | 0 |
| Pier Luigi Nervi | VTN-DOM-0012461 | 0 |
| Shigeru Ban | VTN-DOM-0012435 | 0 |
| Francis Kere | VTN-DOM-0012426 | 0 |

**Model contract preserved.** Person-to-material association is mediated exclusively through `Work` nodes.

---

## 3. Candidate Evidence Paths

### 3.1 Path Pattern
The safe, admissible path template is:

```
Person --[has_facet]→ Work --[has_facet]→ Material
```

This is a **2-hop path** with an intermediate `Work` node, respecting the invariant.

### 3.2 Architects: Person → Work → Material

| Architect | Work | Material Evidence Edge |
|-----------|------|------------------------|
| **Santiago Calatrava** | Alamillo Bridge | → Tensile Behavior (`MAT.PRF.MEC.TEN`) |
| | Milwaukee Art Museum Quadracci Pavilion | → Stainless Steel (`MAT.STM.STS.STS`) |
| **Zaha Hadid** | Vitra Fire Station | → Cast In Place Concrete (`MAT.CMA.CEM.CIP`) |
| | MAXXI Museum | → Cast In Place Concrete (`MAT.CMA.CEM.CIP`) |
| | Heydar Aliyev Center | → Facade Assembly (`MAT.ASM.FAC`) |
| **Tadao Ando** | Church Of The Light | → Exposed Concrete (`MAT.CMA.CEM.EXP`) |
| **Frei Otto** | Munich Olympic Stadium Roof | → Tensile Behavior (`MAT.PRF.MEC.TEN`) |
| **Pier Luigi Nervi** | Palazzetto Dello Sport | → Reinforced Concrete (`ARC.MAT.CON.RCC`) |
| **Shigeru Ban** | Paper Church Kobe | → Thatch (`MAT.EAR.THC`) |
| | | → Plywood (`MAT.TBB.ENW.PLY`) |
| **Francis Kere** | Gando Primary School | → Compressed Earth Block (`MAT.EAR.CEB`) |
| | | → Local Material Availability (`MAT.PRF.ENV.LOC`) |

### 3.3 Materials: Category → Specific Material → Work

The four primary materials exist as **category nodes** with `broader_than` taxonomic children and `has_facet` work connections:

| Material Node | VTN ID | Incoming Edges (sample) |
|--------------|--------|------------------------|
| **Reinforced Concrete** | VTN-DOM-0012147 | ← `Concrete And Masonry Systems` (`broader_than`)  
| | | ← `Palazzetto Dello Sport` (`has_facet`)  
| | | ← `Villa Savoye` (`has_facet`)  
| | | ← `Cultural Center Of The Philippines` (`has_facet`) |
| **Architectural Glass** | VTN-DOM-0012154 | ← `Steel Timber And Composite Systems` (`broader_than`)  
| | | ← `Philippines ALE Structures Materials Utilities Area` (`has_facet`) |
| **Structural Steel** | VTN-DOM-0012151 | ← `Steel Timber And Composite Systems` (`broader_than`)  
| | | ← `Lloyds Building` (`has_facet`)  
| | | ← `Centre Pompidou` (`has_facet`)  
| | | ← `HSBC Main Building Hong Kong` (`has_facet`) |
| **Wood And Timber** | VTN-DOM-0012152 | ← `Steel Timber And Composite Systems` (`broader_than`)  
| | | ← `Bahay Na Bato Hybrid Construction` (`has_facet`)  
| | | ← `Timber Frame` (`requires`) |

**Note:** Architectural Glass has fewer direct work connections in the current snapshot; the more granular `Curtain Wall Glazing` (`MAT.GLA.CWG`) has stronger work coverage.

### 3.4 Filipino Vernacular: Topic → Subtopic → Material

| Node | VTN ID | Evidence Path |
|------|--------|--------------|
| **Philippine Vernacular Architecture** | VTN-DOM-0011997 | → Cross Ventilation (`ARC.TAC.NVS.XVN`)  
| | | → Hardwood (`MAT.TBB.DIL.HDW`)  
| | | → Bamboo Culm (`MAT.TBB.BAS.BCM`)  
| | | → Nipa (`MAT.TBB.BAS.NIP`)  
| | | → Anahaw (`MAT.TBB.BAS.ANH`)  
| | | → Capiz Shell (`MAT.TBB.BAS.CAP`) |
| **Filipino And Southeast Asian Architecture** | VTN-DOM-0002448 | → `broader_than` → Bahay Kubo Spatial Logic  
| | | → `broader_than` → Bahay Na Bato Hybrid Construction  
| | | → `broader_than` → Postwar Modern Philippine Architecture |
| **Bahay Na Bato Hybrid Construction** | VTN-DOM-0005043? | → `has_facet` → Wood And Timber (`ARC.MAT.STM.TIM` path) |

The vernacular path is **taxonomy-first**: `ARC.HIS.SEA` (Southeast Asian history) → `Philippine Vernacular Architecture` → material facets. No person-to-material shortcuts exist.

---

## 4. Source-Rights Cautions

### 4.1 Registry Status
- **Total entries:** 102
- **Classes:** `reference_only` (82), `metadata_crosswalk` (20)
- **Clearance states:** `planning_reference_only`, `unverified_currentness`, `metadata_crosswalk_planned`, `clearance_required`

### 4.2 Per-Entity Cautions

| Entity Class | Caution |
|-------------|---------|
| **Pritzker Laureates** (all 7 architects) | Source `SRC-PRITZKER-LAUREATES-OFFICIAL` is `reference_only` / `planning_reference_only`. Metadata (name, nationality, year) is safe; biography text or jury citations are **blocked** until explicit license review. |
| **Philippine Law / Code References** | Sources `SRC-RA-10066-HERITAGE-ACT`, `SRC-PD-1096-NBCP`, `SRC-NSCP-METADATA` are `reference_only`. **Do not ingest clause text, tables, or figures.** Use metadata-only crosswalks (`maps_to_external_standard`). |
| **Local Raw-Source PDFs** | Sources `SRC-RAW-LEA-FILIPINO-ARCHITECTURE-PDF`, `SRC-RAW-LEA-TROPICAL-ARCHITECTURE-PDF` are `reference_only` / `clearance_required`. Filename metadata is in the registry; **content ingest is blocked** pending rights clearance. |
| **Wikidata Crosswalk** | Source `SRC-WIKIDATA-CC0-AEC-IDENTIFIERS` is `metadata_crosswalk` / `metadata_crosswalk_planned`. CC0 identifiers (Q-codes) are safe; **descriptive text may carry downstream attribution obligations** — verify per-item. |
| **Building Materials** | Most material nodes are taxonomy-derived with no external source dependency. `maps_to_external_standard` edges to `SRC-CHED-CMO-61-2017-BS-ARCH` and `SRC-NSCP-METADATA` are **metadata-only** — do not cache standard clauses locally. |

### 4.3 Prohibited Actions (Hard-Blocked)
1. **No protected payload ingest** — exam questions, reviewer text, code tables/clauses/figures.
2. **No direct person-to-material edge creation** — model invariant; violation breaks validation.
3. **No Neo4j/live graph mutation** — production promotion requires credentials + rollback proof (per `current-phase.md` §5).
4. **No raw-source content quoting** — this advisory contains **zero** protected text excerpts.

---

## 5. Validation Checklist

### 5.1 Structural Validation
- [ ] All proposed paths are **2-hop minimum** (Person → Work → Material; no direct edges).
- [ ] All predicates are in the **governed vocabulary** (`has_facet`, `broader_than`, `requires`, `maps_to_external_standard`).
- [ ] All endpoint IDs are **resolvable VTN-DOM-XXXXXXXX** canonical IDs.
- [ ] No proposed edge creates a **cycle** with existing `broader_than` taxonomy.
- [ ] Work nodes are **shared anchors** (appear in both person and material neighborhoods).

### 5.2 Source-Rights Validation
- [ ] Every proposed `maps_to_external_standard` edge targets a **metadata-only** source-rights entry.
- [ ] No proposed edge relies on `clearance_required` sources for its evidentiary basis.
- [ ] Pritzker-related person nodes are scoped to **public metadata only** (name, nationality, laureate status).
- [ ] Philippine heritage law edges (`RA-10066`) are **constrains** or `maps_to_external_standard`, never `governs` with clause text.
- [ ] Local raw-source PDFs are **not cited as evidence payloads** — only filename metadata in source-rights registry.

### 5.3 Graph Integrity Validation
- [ ] Run `kg-validate-assertions` (R1–R14) against any admitted additions.
- [ ] Run `kg-detect-contradictions` to verify no `REQUIRES` vs `EXCLUDES` conflicts on material nodes.
- [ ] Verify `broader_than` acyclicity for any new taxonomy insertions under `ARC.HIS.SEA`.
- [ ] Confirm `direct_person_to_material_edges_added` remains **0** in enrichment report quality controls.

### 5.4 Resolver/Explorer Validation
- [ ] Run resolver QA (`/v2/resolve*`) for each proposed architect + work + material triple.
- [ ] Verify Explorer label/highlight tests pass for new nodes (target: 37+ cases).
- [ ] Confirm API-Explorer parity report shows **zero regressions**.

---

## 6. Concise Path Reference Table

| Query Target | Canonical Entry Point | Safe Path | Hops |
|-------------|----------------------|-----------|------|
| Calatrava + concrete | VTN-DOM-0012458 | Person → has_facet → Work → **(no concrete edge)**; via `Tensile Behavior` or `Stainless Steel` | 2 |
| Hadid + concrete | VTN-DOM-0012443 | Person → has_facet → Vitra Fire Station / MAXXI → has_facet → Cast In Place Concrete | 2 |
| Ando + concrete | VTN-DOM-0012446 | Person → has_facet → Church Of The Light → has_facet → Exposed Concrete | 2 |
| Frei Otto + tensile | VTN-DOM-0012434 | Person → has_facet → Munich Olympic Stadium Roof → has_facet → Tensile Behavior | 2 |
| Nervi + concrete | VTN-DOM-0012461 | Person → has_facet → Palazzetto Dello Sport → has_facet → Reinforced Concrete | 2 |
| Shigeru Ban + timber | VTN-DOM-0012435 | Person → has_facet → Paper Church Kobe → has_facet → Thatch / Plywood | 2 |
| Francis Kere + earth | VTN-DOM-0012426 | Person → has_facet → Gando Primary School → has_facet → Compressed Earth Block | 2 |
| Filipino vernacular + timber | VTN-DOM-0011997 | Topic → has_facet → Hardwood / Bamboo Culm / Nipa / Anahaw | 1 |
| Concrete (category) | VTN-DOM-0012147 | Category ← broader_than ← Concrete And Masonry Systems; ← has_facet ← Palazzetto Dello Sport, Villa Savoye, CCP | 1–2 |
| Glass (category) | VTN-DOM-0012154 | Category ← broader_than ← Steel Timber And Composite Systems; granular: Curtain Wall Glazing | 1–2 |
| Steel (category) | VTN-DOM-0012151 | Category ← broader_than ← Steel Timber And Composite Systems; ← has_facet ← Centre Pompidou, HSBC HK, Lloyds | 1–2 |
| Timber (category) | VTN-DOM-0012152 | Category ← broader_than ← Steel Timber And Composite Systems; ← has_facet ← Bahay Na Bato; ← requires ← Timber Frame | 1–2 |

---

## 7. Assumptions & Limitations

1. **Assumption:** The user-requested architects are evaluated against the **existing** backbone snapshot (`20260430T070501Z`). Future enrichment may add works or material edges.
2. **Assumption:** "Do not quote protected text" is interpreted as **zero verbatim extraction** from raw-source PDFs, reviewer materials, or licensed standards text. All labels are canonical node labels or metadata-derived summaries.
3. **Limitation:** Architectural Glass (`VTN-DOM-0012154`) has sparse direct work coverage in this snapshot. The more specific `Curtain Wall Glazing` (`MAT.GLA.CWG`) is the practical query target for glass-related evidence.
4. **Limitation:** Calatrava has **no concrete-specific work edge** in the current snapshot; his material evidence is via `Tensile Behavior` and `Stainless Steel`.
5. **Limitation:** All paths are **read-only projections** from the file-backed shadow graph. Production runtime queries require the `/v2/resolve*` resolver path, which is default-on but gated by `VITRUVIUS_AEC_MEPFS_RESOLVER_RUNTIME`.

---

## 8. Artifact References

| Artifact | Path |
|----------|------|
| Shadow backbone graph (9,761 nodes) | `006_System-Manifests/aec-mepfs-backbone/shadow-staging/20260430T070501Z/shadow-backbone-graph.json` |
| Shadow backbone staging (source rights) | `006_System-Manifests/aec-mepfs-backbone/shadow-staging/20260430T070501Z/shadow-backbone-staging.json` |
| Architecture interconnectivity report | `006_System-Manifests/aec-mepfs-backbone/architecture-interconnectivity/20260430T070000Z/architecture-interconnectivity-enrichment-report.json` |
| Current phase (authority) | `.ai/01_roadmap/current-phase.md` |
| Source-rights registry schema | `config/vitruvius.yaml` §kg_transition |

---

*End of advisory. No graph mutations performed. No protected text quoted. All node labels are canonical backbone metadata.*
