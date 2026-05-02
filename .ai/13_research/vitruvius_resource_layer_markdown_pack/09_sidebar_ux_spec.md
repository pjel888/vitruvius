# 09 — Right Sidebar UX Specification

## UX goal

When a user clicks an eligible node, the sidebar should answer:

- What are the best references for this node?
- Why are these references relevant?
- Are they local or online?
- Are they official/professional/academic/general?
- Are they verified?
- Do they apply to a jurisdiction?
- Where should I look inside the source?

## Eligible nodes

Show source sidebar for Concept, Rule, Definition, Procedure, Exception, Evidence, and Document nodes.

## Default view

Show top 5 accepted resources. Allow expand to top 10. Do not show candidates by default unless user/admin toggles “Show candidates.”

## Resource card layout

```text
[Type badge] [Authority badge] [Verification badge] [Local/Online badge]
Title
Organization / Author / Publisher · Year
Relationship: explains / defines / governs / provides evidence / etc.
Relevance: 92% · Authority: High
Scope: International / US / UK / Project-specific / Unknown
Refs: pp. 42–48 / Ch. 3 / Section 5.1
Why relevant: <one sentence rationale>
[Open URL] [Open local file] [Show linked claims] [Report issue]
```

## Badge examples

Type: Book, Textbook, Standard, Code, Professional guidance, Academic paper, Technical report, Local PDF, Internal document, Classification, Webpage.

Authority: Official, Professional body, Government, Academic, Recognized publisher, Manufacturer, Internal, General web, Unknown.

Verification: Human reviewed, Content verified, Local file verified, Identifier verified, Link verified, Metadata verified, Candidate, Needs review, Rejected.

Access: Local, Open access, Public web, Preview only, Paywalled, Restricted, Unknown.

## Empty state

```text
No accepted references yet for this node.

This node may have candidate sources in the review queue, or it may not have been backfilled yet.
```

Admin/developer mode can show “Generate source candidates,” “Run local corpus match,” and “Ask Kimi to review candidates.”

## Filters

Recommended filters:

- Local only
- Online only
- Official/professional only
- Books
- PDFs
- Standards/codes
- Academic papers
- Guidance/manuals
- Open access
- Needs review
- Show candidates

## Sort options

Default: Best match.

Other sort options: Authority, Relevance, Recently verified, Local first, Newest, Oldest/classic references.

## Rule node sidebar

For Rule nodes, emphasize primary source, jurisdiction/scope, confidence, review status, and caveats.

Example warning:

```text
This rule appears jurisdiction-sensitive. Confirm applicable local code/adoption before using it for design or compliance.
```

## Evidence node sidebar

For Evidence nodes, show claim summary, source paper/report, DOI/stable ID, evidence strength if modeled, date/year, and limitations/caveats.

## Document node sidebar

For a Document node, show title, authors/organization, publisher, year/edition, resource type, identifiers, access type, verification status, and linked concepts/rules/procedures/evidence.

## Performance

Sidebar render should not call external APIs. It should read from existing resources/links. Candidate generation is a separate background/admin/agent job.
