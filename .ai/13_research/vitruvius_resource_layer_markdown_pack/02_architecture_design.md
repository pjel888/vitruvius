# 02 — System Architecture Design

## High-level architecture

```text
Knowledge Graph Node
  └─ node_id
     └─ NodeResourceLink
        ├─ relationship
        ├─ relevance / authority / confidence
        ├─ rationale
        ├─ page/chapter/section refs
        └─ resource_id
           └─ Resource
              ├─ online URL / DOI / ISBN / canonical URL
              ├─ local file path / hash
              ├─ title / authors / organization / publisher / year
              ├─ source authority / access type / jurisdiction
              └─ verification status
```

## Main modules

### 1. Resource Registry

Stores stable metadata for resources. Reused across graph nodes.

### 2. NodeResourceLink Registry

Stores why a resource is relevant to a specific graph node.

### 3. Source Discovery Adapters

Adapters discover candidate resources:

- local filesystem scanner,
- Google Books/Open Library,
- Crossref/DataCite,
- Semantic Scholar/OpenAlex,
- CORE/Unpaywall,
- Internet Archive,
- curated source domains.

### 4. Candidate Queue

New search results should first become candidates, not accepted resources. Candidate records may include:

- raw API response excerpt,
- query used,
- candidate score,
- adapter that found it,
- dedupe key,
- review status.

### 5. Verifier

Checks:

- URL health,
- canonical URL,
- DOI/ISBN normalization,
- local file exists,
- local file hash,
- metadata consistency,
- source authority,
- relevance score,
- duplicate detection.

### 6. Kimi Reviewer

Reviews candidate batches for:

- relevance,
- authority,
- overclaiming,
- jurisdiction issues,
- duplicate concepts,
- weak source-node mapping,
- better source categories.

### 7. Sidebar API / Selector

Given a node ID, returns top accepted resources ranked by:

- relationship fit,
- authority,
- verification status,
- local availability,
- recency where relevant,
- diversity of source types.

### 8. Sidebar UI

Displays resource cards and filters.

## Data flow: online source candidate

```text
Node selected for backfill
  → query builder creates search queries from node name, aliases, taxonomy, description
  → adapters search APIs/domains
  → candidates stored
  → dedupe and normalize
  → verifier checks link/identifier/metadata
  → ranker scores relevance and authority
  → Kimi reviews candidate batch
  → accepted candidates become Resources and NodeResourceLinks
  → sidebar displays accepted links
```

## Data flow: local PDF candidate

```text
Local library scan
  → metadata extraction
  → file hash
  → page/chunk text extraction
  → embeddings / keyword index
  → match chunks to nodes by aliases/taxonomy/semantic similarity
  → candidate NodeResourceLinks generated with page refs
  → verifier checks file path/hash
  → Kimi reviews high-impact matches
  → accepted links shown in sidebar
```

## Where to store data

Use existing repo conventions. If none exist, possible layouts:

```text
data/resources/resources.json
data/resources/node-resource-links.json
data/resources/source-families.json
data/resources/resource-checks.json
data/resources/resource-candidates.json
data/resources/local-file-index.json
```

or relational tables:

```sql
resources
node_resource_links
source_families
resource_checks
resource_candidates
resource_chunks
review_events
backfill_batches
```

## Separation of candidate vs accepted

Candidate means discovered but not fully verified and not shown by default.

Accepted means basic verification completed, the source is relevant enough, rationale exists, deduping is done, and it is safe to show in the sidebar.

Rejected means low relevance, low quality, duplicate, broken link, inaccessible, legally problematic, too jurisdiction-specific without context, or overclaimed.

## Sidebar query behavior

For a node ID:

1. Fetch accepted NodeResourceLinks for that node.
2. Join Resource metadata.
3. Exclude broken/rejected resources by default.
4. Sort by computed display score.
5. Return top 5 by default.
6. Allow expand to top 10.
7. Allow filters.

Recommended display score:

```text
display_score =
  0.35 * relevance_score
+ 0.25 * authority_score
+ 0.20 * verification_score
+ 0.10 * local_or_stable_identifier_bonus
+ 0.10 * source_type_diversity_bonus
```

## Caching

Do not call external APIs during normal sidebar render.

Normal UI should read from local application data or database only.

External API calls happen in backfill scripts, batch jobs, admin actions, agent loops, or explicit refresh workflows.

## Relationship to Document nodes

Resources are registry records. `Document` nodes are graph nodes.

A resource may become a Document node when it is important enough to reason about inside the graph, such as a major standard, local design guide, textbook used across many concepts, internal O&M manual, basis-of-design document, or critical paper supporting evidence nodes.

Do not create a Document node for every URL.
