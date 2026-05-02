# 00 — Manifesto and Scope

## The actual product goal

Vitruvius should become a knowledge graph that is not only rich in nodes and edges, but also **source-literate**. A user clicking a lower-level node should see the best evidence, references, books, PDFs, guidance, standards, and local documents that explain or support that node.

The sidebar must not be a search-results dump. It should be a curated, ranked, verified source panel.

## Target behavior

When a user clicks a node such as:

- `Retaining Wall`
- `Accessible Route`
- `Fire-rated Wall`
- `Load Path`
- `Mat Foundation`
- `Site Grading`
- `Door Clearance`
- `Lateral Earth Pressure`
- `Embodied Carbon`
- `Concrete Curing Procedure`

The right sidebar should show a small set of high-quality references:

- official guidance / standards pages where available,
- professional body references,
- recognized textbooks and handbooks,
- local PDFs/books/documents,
- academic papers for evidence-heavy subjects,
- internal source documents,
- page/section references when extractable,
- a short explanation of why each source is relevant.

## Scope of node types

Primary eligible nodes:

- `Concept`
- `Rule`
- `Definition`
- `Procedure`
- `Exception`
- `Evidence`
- `Document`

Defer aggregate behavior for:

- `Taxonomy`
- `Topic`
- `Subtopic`

Higher nodes may later show inherited resources from child nodes or curated overview references, but they should not be the first implementation target.

## Why a separate Resource Registry is better than putting URLs directly on nodes

Putting URL arrays directly on every node creates problems:

- duplicates everywhere,
- no verification state,
- no DOI/ISBN/canonical URL dedupe,
- no local file hash support,
- no page-level references,
- no shared document reuse,
- no separation between “candidate” and “accepted”,
- no authority scoring,
- no review workflow,
- no stable audit trail.

Instead, add a dedicated layer:

```text
Graph node -> NodeResourceLink -> Resource
```

A Resource may be reused across hundreds of nodes. A NodeResourceLink explains exactly why the resource is relevant to that node.

## Relationship to existing graph nodes

Graph nodes answer:

- What is this thing/concept/rule/procedure/evidence/document?
- How does it relate to other graph nodes?
- What taxonomy does it belong to?
- What systems, assemblies, processes, and constraints does it participate in?

Resource links answer:

- Where can the user learn more?
- What source supports this node?
- Is the source authoritative?
- What page/section is relevant?
- Is this rule/code/guidance jurisdiction-sensitive?
- Is the source local, online, paywalled, public, or internal?

## Design principle: top few, not many

For each eligible node, target:

- **3–5 accepted resources** for normal Concept nodes,
- **5–10 accepted resources** for high-centrality or safety-critical nodes,
- **1+ primary source** for Rule nodes,
- **1+ procedural source** for Procedure nodes,
- **1+ evidence source** for Evidence nodes,
- complete metadata for Document nodes.

Do not aim for 100+ URLs per node. That makes the UI worse and destroys trust.

## Source-quality hierarchy

Prefer sources in this order, all else equal:

1. Official standards, official documentation, government/professional body sources.
2. Recognized textbooks, handbooks, professional guidance, and industry manuals.
3. Peer-reviewed academic papers and technical reports.
4. University/open course materials.
5. Manufacturer manuals when product-specific.
6. Reputable trade articles.
7. General web content only as low-priority background.

## What must never happen

Do not:

- attach random URLs,
- mark unverified candidates as accepted,
- create placeholder resources,
- create `Rule` nodes without source support,
- imply a code applies universally when it is jurisdictional,
- paste long copyrighted standards/book text,
- link pirated PDFs,
- show broken links as accepted,
- treat metadata discovery as truth verification,
- treat a book search result as proof that the book is the best authority,
- flood a sidebar with hundreds of low-quality links.

## Long-term vision

Once this source layer exists, Vitruvius can support:

- source-backed definitions,
- source-backed rules,
- procedure cards,
- evidence cards,
- document graph nodes,
- “why is this edge true?” support,
- academic/professional literature discovery,
- local library integration,
- human review workflows,
- safer code/regulatory caveats,
- source coverage metrics,
- graph quality scoring.
