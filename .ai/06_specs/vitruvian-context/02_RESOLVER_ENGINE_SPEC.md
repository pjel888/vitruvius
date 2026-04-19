# Vitruvian Context — Resolver Engine Specification

> **Type:** Core architectural specification
> **Authority:** `00_locked_decisions.md` (D1–D10), `01_CROSS_DISCIPLINE_RELATIONSHIP_TAXONOMY.md`
> **Schema version:** `1.0.0`
> **Date:** 2026-04-19

---

## 1. Definition

> **The Vitruvian Context = the engine that resolves canonical knowledge into context-specific truth.**

It transforms a query + context into a resolved output that answers:
- **What** applies?
- **Why** it applies?
- **Where** it applies?
- **When** it applies?

The engine never mutates truth. It selects, composes, and ranks.

---

## 2. System Position

```text
Raw Data
→ Canonical Knowledge (Backbone)
→ Facets (multi-dimensional classification)
→ Overlays (jurisdiction, standards, project rules)
→ ⚡ Vitruvian Context Resolver
→ Output (API / UI / decisions)
```

| Layer | Responsibility | Owned By |
|-------|---------------|----------|
| Backbone | Single source of truth for canonical meaning | Editorial |
| Facets | Multi-dimensional classification | Data |
| Overlays | Jurisdiction-specific variations | Backend |
| **Vitruvian Context** | **Context resolution and composition** | **Backend** |
| Delivery | API + UI presentation | Frontend |

---

## 3. Core Interface

### 3.1 Function Signature

```typescript
function resolve(
  query: CanonicalQuery,
  context: ResolutionContext,
  options?: ResolveOptions
): ResolvedTruth;
```

### 3.2 CanonicalQuery

```typescript
interface CanonicalQuery {
  // What is being asked
  concept_id?: string;           // Specific concept (e.g., VTN-CON-0000042)
  path_code?: string;            // Backbone path (e.g., ACC.BFD.ROU.ARA)
  search_text?: string;          // Full-text search
  
  // What kind of answer
  return_type: "concept" | "overlay" | "evidence" | "standards" | "full";
  
  // Filtering
  facets?: FacetFilter;
  
  // Cross-discipline expansion
  expand_domains?: string[];     // Domains to include in influence search
  max_hops?: number;             // Max edge hops for influence traversal (default: 2)
}
```

### 3.3 ResolutionContext

```typescript
interface ResolutionContext {
  // Jurisdiction hierarchy (most specific first)
  jurisdiction_code: string;     // e.g., "PH-NCR-Makati"
  
  // Temporal
  date: string;                  // ISO-8601 date (e.g., "2026-04-19")
  
  // Project context
  project_type?: string;         // e.g., "high-rise residential"
  asset_scope?: string;          // e.g., "building"
  lifecycle_stage?: string;      // e.g., "construction"
  
  // Optional overrides
  user_overrides?: {
    standard_system?: string;    // e.g., "OmniClass"
    confidence_threshold?: number; // default: 0.70
  };
}
```

### 3.4 ResolvedTruth

```typescript
interface ResolvedTruth {
  // The canonical concept (always present)
  canonical_concept: CanonicalConcept;
  
  // Resolution metadata
  resolution: {
    jurisdiction_chain: JurisdictionNode[];
    applicable_overlays: Overlay[];
    effective_documents: AuthorityDocumentEdition[];
    precedence_applied: string[];
  };
  
  // Cross-discipline influences
  influences: {
    primary_domain: DomainNode;
    affected_domains: AffectedDomain[];
    regulating_domains: DomainNode[];
  };
  
  // Evidence chain
  evidence: EvidenceSpan[];
  
  // Standards mappings
  standards_mappings: StandardMapping[];
  
  // Reasoning trace (non-negotiable)
  reasoning_trace: ReasoningStep[];
  
  // Query metadata
  query: CanonicalQuery;
  context: ResolutionContext;
  resolved_at: string;           // ISO-8601 timestamp
}

interface AffectedDomain {
  domain: DomainNode;
  relationship_type: string;     // CONSTRAINS, AFFECTS, REQUIRES, etc.
  confidence: number;
  rationale: string;
}

interface ReasoningStep {
  step: number;
  operation: string;
  input: any;
  output: any;
  evidence: string;
}
```

---

## 4. Precedence Rules

### 4.1 Jurisdiction Precedence

```text
project-specific > municipal > agency > state/province > national > supranational > international
```

**Code values:**
| Level | Example Code | Precedence Rank |
|-------|-------------|-----------------|
| Project-specific | `PROJ-123` | 0 (highest) |
| Municipal | `PH-NCR-Makati` | 1 |
| Agency | `PH-DPWH` | 2 |
| State/Province | `PH-NCR` | 3 |
| National | `PH` | 4 |
| Supranational | `ASEAN` | 5 |
| International | `ISO` | 6 (lowest) |

**Rule:** When multiple overlays apply to the same concept, the overlay from the highest-precedence jurisdiction wins.

**Tie-breaker:** If same precedence, the overlay with the most specific condition wins.

### 4.2 Temporal Precedence

```text
For each jurisdiction level, select the edition effective on the query date.
Ignore superseded editions.
If no edition is effective, return the most recent past edition with a warning.
```

### 4.3 Standards Precedence

```text
project-specified > local-code > national-code > international-standard
```

**User override:** `user_overrides.standard_system` forces that system to rank 0.

### 4.4 Confidence Thresholding

Default minimum confidence: `0.70`

| Data Type | Default Threshold | Overrideable |
|-----------|------------------|--------------|
| Overlay | 0.90 | No |
| Evidence | 0.80 | Yes |
| Standards mapping | 0.70 | Yes |
| Cross-discipline edge | 0.75 | Yes |

---

## 5. Resolver Algorithm

### 5.1 Step-by-Step

```
RESOLVE(query, context):
  
  STEP 1: IDENTIFY CONCEPT
    IF query.concept_id:
      concept ← LookupByCanonicalId(query.concept_id)
    ELSE IF query.path_code:
      concept ← LookupByPathCode(query.path_code)
    ELSE IF query.search_text:
      candidates ← FullTextSearch(query.search_text, query.facets)
      concept ← candidates[0]  // highest score
    
    IF concept == null:
      RETURN Error("Concept not found")
  
  STEP 2: VALIDATE CONTEXT
    jurisdiction_chain ← ResolveJurisdictionChain(context.jurisdiction_code)
    IF jurisdiction_chain == null:
      RETURN Error("Invalid jurisdiction code")
    
    effective_date ← ParseDate(context.date)
    IF effective_date > TODAY:
      LogWarning("Future date — using current effective editions")
  
  STEP 3: GATHER OVERLAYS
    overlays ← []
    FOR jurisdiction IN jurisdiction_chain:
      jurisdiction_overlays ← FindOverlays(concept, jurisdiction, effective_date)
      overlays ← overlays + jurisdiction_overlays
    
    // Apply precedence
    selected_overlay ← SelectByPrecedence(overlays)
    
    // Apply project-specific overrides
    IF context.project_type:
      project_overlay ← FindProjectOverlay(concept, context.project_type)
      IF project_overlay:
        selected_overlay ← project_overlay  // project always wins
  
  STEP 4: GATHER EVIDENCE
    evidence ← FindEvidenceSpans(concept)
    IF selected_overlay:
      overlay_evidence ← FindEvidenceSpans(selected_overlay)
      evidence ← evidence + overlay_evidence
    
    // Filter by confidence
    evidence ← FilterByConfidence(evidence, threshold)
  
  STEP 5: GATHER STANDARDS MAPPINGS
    mappings ← FindStandardMappings(concept)
    mappings ← FilterByConfidence(mappings, threshold)
    
    IF context.user_overrides.standard_system:
      mappings ← PrioritizeSystem(mappings, context.user_overrides.standard_system)
  
  STEP 6: GATHER CROSS-DISCIPLINE INFLUENCES
    primary_domain ← GetPrimaryDomain(concept)
    
    affected_domains ← []
    FOR edge IN FindOutgoingEdges(concept, [CONSTRAINS, AFFECTS, REQUIRES, INFLUENCES, USED_IN, EXECUTED_IN]):
      affected_domains.append({
        domain: edge.target,
        relationship_type: edge.type,
        confidence: edge.confidence,
        rationale: edge.rationale
      })
    
    regulating_domains ← []
    FOR edge IN FindOutgoingEdges(concept, [REGULATED_BY]):
      regulating_domains.append(edge.target)
  
  STEP 7: BUILD REASONING TRACE
    trace ← [
      {step: 1, operation: "IDENTIFY", input: query, output: concept.id},
      {step: 2, operation: "JURISDICTION", input: context.jurisdiction_code, output: jurisdiction_chain},
      {step: 3, operation: "OVERLAY", input: overlays, output: selected_overlay.id},
      {step: 4, operation: "EVIDENCE", input: evidence.length, output: evidence.length},
      {step: 5, operation: "STANDARDS", input: mappings.length, output: mappings.length},
      {step: 6, operation: "INFLUENCES", input: primary_domain, output: affected_domains.length}
    ]
  
  STEP 8: ASSEMBLE OUTPUT
    RETURN {
      canonical_concept: concept,
      resolution: {
        jurisdiction_chain: jurisdiction_chain,
        applicable_overlays: [selected_overlay],
        effective_documents: GetEffectiveDocuments(selected_overlay),
        precedence_applied: ["jurisdiction", "temporal", "project"]
      },
      influences: {
        primary_domain: primary_domain,
        affected_domains: affected_domains,
        regulating_domains: regulating_domains
      },
      evidence: evidence,
      standards_mappings: mappings,
      reasoning_trace: trace,
      query: query,
      context: context,
      resolved_at: Now()
    }
```

### 5.2 Cypher Implementation (Neo4j)

```cypher
// Step 1: Identify concept
MATCH (c:CanonicalNode {canonical_id: $concept_id})

// Step 2: Resolve jurisdiction chain
MATCH path = (j:Jurisdiction {code: $jurisdiction_code})-[:WITHIN_JURISDICTION*0..5]->(parent:Jurisdiction)
WITH c, j, collect(parent) + j AS jurisdiction_chain

// Step 3: Gather overlays
UNWIND jurisdiction_chain AS jurisdiction
MATCH (c)-[:HAS_OVERLAY]->(o:Overlay)-[:APPLIES_IN]->(jurisdiction)
WHERE o.effective_date <= date($query_date)
  AND (o.repeal_date IS NULL OR o.repeal_date > date($query_date))
WITH c, jurisdiction_chain, collect(o) AS overlays

// Step 3b: Select by precedence
WITH c, jurisdiction_chain,
     apoc.coll.maxBy(overlays, 'precedence_rank') AS selected_overlay

// Step 4: Gather evidence
OPTIONAL MATCH (c)-[:SUPPORTED_BY]->(e:EvidenceSpan)
WITH c, jurisdiction_chain, selected_overlay, collect(e) AS evidence

// Step 5: Gather standards mappings
OPTIONAL MATCH (c)-[m:MAPS_TO_STANDARD]->(sr:StandardReference)
WHERE m.confidence >= $confidence_threshold
WITH c, jurisdiction_chain, selected_overlay, evidence, collect({mapping: m, standard: sr}) AS mappings

// Step 6: Gather influences
OPTIONAL MATCH (c)-[inf:CONSTRAINS|AFFECTS|REQUIRES|INFLUENCES|USED_IN|EXECUTED_IN|REGULATED_BY]->(target)
WITH c, jurisdiction_chain, selected_overlay, evidence, mappings, collect(inf) AS influences

// Step 7: Primary domain
MATCH (c)-[:primary_domain]->(primary:BackboneNode)

RETURN {
  canonical_concept: c,
  resolution: {
    jurisdiction_chain: jurisdiction_chain,
    applicable_overlays: [selected_overlay],
    effective_documents: []
  },
  influences: {
    primary_domain: primary,
    affected_domains: influences
  },
  evidence: evidence,
  standards_mappings: mappings,
  reasoning_trace: []
} AS result
```

---

## 6. Edge Cases

### 6.1 No Overlay Found

**Condition:** Concept exists, but no overlay applies in the requested jurisdiction.

**Behavior:**
- Return canonical concept with empty `applicable_overlays`
- Add reasoning step: `"No overlay found for jurisdiction PH-NCR-Makati. Returning canonical definition only."`
- Log warning for analytics

### 6.2 Multiple Overlays at Same Precedence

**Condition:** Two overlays from same jurisdiction level with different conditions.

**Behavior:**
- Select overlay with more specific condition (longer condition string)
- If equally specific, return both overlays with `conflict: true` flag
- Add reasoning step documenting conflict

### 6.3 Superseded Edition

**Condition:** Query date falls between repeal date of old edition and effective date of new edition.

**Behavior:**
- Return most recent past edition with `warning: "Edition superseded on {date}. Check for newer edition."`
- Include `superseded_by` reference to newer edition

### 6.4 Future Date

**Condition:** `context.date` is in the future.

**Behavior:**
- Log warning
- Use current date for edition resolution
- Add reasoning step: `"Future date requested. Using current effective date {today}."`

### 6.5 Invalid Jurisdiction Code

**Condition:** `context.jurisdiction_code` does not exist in graph.

**Behavior:**
- Return error: `INVALID_JURISDICTION`
- Suggest closest valid code using Levenshtein distance

### 6.6 Missing Facet Data

**Condition:** Concept exists but missing required facet values.

**Behavior:**
- Return concept with `incomplete: true` flag
- List missing facets in reasoning trace
- Do not fail resolution

---

## 7. Performance Requirements

| Operation | Target Latency | Max Latency |
|-----------|---------------|-------------|
| Single concept resolution | <100ms | 500ms |
| Full-text search + resolution | <200ms | 1s |
| Cross-discipline influence traversal (2 hops) | <150ms | 750ms |
| Jurisdiction chain resolution | <50ms | 250ms |

**Optimization strategies:**
- Precompute jurisdiction chains at ingestion time
- Cache `ResolvedTruth` for common context combinations (TTL: 1 hour)
- Materialize `primary_domain` and `BELONGS_TO_DOMAIN` as composite indexes
- Use Neo4j relationship indexes for cross-discipline edges

---

## 8. Test Cases

### 8.1 TC-01: Philippine Accessible Ramp

**Input:**
```json
{
  "query": {"concept_id": "VTN-CON-0000042", "return_type": "full"},
  "context": {"jurisdiction_code": "PH", "date": "2026-04-19"}
}
```

**Expected:**
- Canonical concept: "Accessible Ramps"
- Jurisdiction chain: `[PH]`
- Overlay: slope_max_1_12 (from BP 344)
- Primary domain: Accessibility
- Affected domains: Architecture (constrains clearances)
- Standards: OmniClass 23-27 11 11

### 8.2 TC-02: Makati Override

**Input:**
```json
{
  "query": {"concept_id": "VTN-CON-0000042", "return_type": "full"},
  "context": {"jurisdiction_code": "PH-NCR-Makati", "date": "2026-04-19"}
}
```

**Expected:**
- Jurisdiction chain: `[PH-NCR-Makati, PH-NCR, PH]`
- If Makati has stricter overlay: return Makati overlay
- If no Makati overlay: return PH overlay
- Reasoning trace shows precedence decision

### 8.3 TC-03: Cross-Discipline Query

**Input:**
```json
{
  "query": {
    "search_text": "concrete",
    "expand_domains": ["architecture", "construction"],
    "max_hops": 2,
    "return_type": "full"
  },
  "context": {"jurisdiction_code": "PH", "date": "2026-04-19"}
}
```

**Expected:**
- Returns "Reinforced Concrete Detailing" (primary: Structural)
- Shows `CONSTRAINS` → Architecture
- Shows `EXECUTED_IN` → Construction
- Returns related architectural concepts affected by concrete

### 8.4 TC-04: Future Date Warning

**Input:**
```json
{
  "query": {"concept_id": "VTN-CON-0000042", "return_type": "full"},
  "context": {"jurisdiction_code": "PH", "date": "2030-01-01"}
}
```

**Expected:**
- Concept resolved
- Warning in reasoning trace
- Edition resolution uses current date

### 8.5 TC-05: Invalid Jurisdiction

**Input:**
```json
{
  "query": {"concept_id": "VTN-CON-0000042", "return_type": "full"},
  "context": {"jurisdiction_code": "XX-Invalid", "date": "2026-04-19"}
}
```

**Expected:**
- Error: `INVALID_JURISDICTION`
- Suggestion: closest valid code

---

## 9. Error Codes

| Code | Meaning | HTTP Status |
|------|---------|-------------|
| `CONCEPT_NOT_FOUND` | Query did not match any concept | 404 |
| `INVALID_JURISDICTION` | Jurisdiction code not in graph | 400 |
| `INVALID_DATE` | Date format invalid or out of range | 400 |
| `NO_OVERLAY_FOUND` | Concept exists but no overlay for context | 200 (with warning) |
| `EDITION_CONFLICT` | Multiple editions claim applicability | 200 (with conflict flag) |
| `SUPERSEDED_EDITION` | Edition was superseded before query date | 200 (with warning) |
| `INCOMPLETE_FACETS` | Concept missing required facet values | 200 (with incomplete flag) |
| `RESOLUTION_TIMEOUT` | Query exceeded max latency | 504 |

---

## 10. Implementation Invariants

1. **Never mutate canonical nodes.** The resolver only reads.
2. **Never create overlays on the fly.** All overlays must exist in the graph before resolution.
3. **Precedence is deterministic.** Same input always produces same output.
4. **Reasoning trace is mandatory.** Every response must explain how the answer was derived.
5. **Confidence is explicit.** Every selected edge, overlay, or mapping shows its confidence.
6. **Jurisdiction chain is complete.** From most specific to most general, no gaps.
