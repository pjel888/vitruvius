# 12 — Kimi Review Prompts

## General Kimi instruction

Use Kimi as a critic and co-reviewer, not as an authority.

Kimi should help identify weak relevance, overclaimed authority, jurisdiction-sensitive claims, duplicate resources, better source categories, bad relationship types, missing caveats, candidates that should be rejected, and candidates that need human review.

Codex should make the final implementation decision and log accepted/rejected Kimi suggestions.

## Prompt 1 — Candidate source review

```text
Kimi, review this Vitruvius node-resource candidate batch.

Context:
Vitruvius is an AEC knowledge graph. We are adding a Resource Intelligence Layer so clicked nodes show a ranked, verified set of sources in the right sidebar.

Do not suggest placeholder resources. Do not accept weak sources just because they mention the node term. Prefer authoritative, relevant, source-specific references. Flag jurisdiction-sensitive or code-like claims.

Node:
<node JSON>

Candidate resources:
<candidate resource JSON array>

For each candidate, return:
- decision: accept | reject | needs_review
- corrected relationship type if needed
- relevance concerns
- authority concerns
- jurisdiction/context concerns
- duplicate concerns
- copyright/access concerns
- improved rationale, one sentence
- whether human review is recommended

Also list missing source categories that would improve coverage.
```

## Prompt 2 — Rule node source review

```text
Kimi, review these proposed sources for a Vitruvius Rule node.

A Rule node may be interpreted by users as a requirement or constraint. Be strict.

Node:
<rule node JSON>

Candidate sources:
<candidates>

Check:
1. Does at least one candidate function as a primary or high-authority source?
2. Is the rule jurisdiction-sensitive?
3. Is the source binding, professional guidance, or merely explanatory?
4. Does the proposed rationale overclaim?
5. Should this rule be downgraded to Concept/Procedure/Exception instead?
6. Is human review required before marking trusted?

Return concrete accept/reject/needs_review decisions.
```

## Prompt 3 — Local PDF match review

```text
Kimi, review these local document matches for a Vitruvius node.

Node:
<node JSON>

Local document candidates:
Each candidate includes title, extracted headings, page refs, short preview, and proposed relationship.

Review for:
- real relevance to the node,
- whether page refs are specific enough,
- whether the relationship type is correct,
- whether the source appears too broad,
- whether the text only mentions the term in passing,
- whether the source should be a Document node.

Return accept/reject/needs_review and improved rationale.
```

## Prompt 4 — Sidebar top references review

```text
Kimi, review the proposed top sidebar references for this node.

Node:
<node JSON>

Accepted resources currently ranked for sidebar:
<accepted resources>

Check:
- Are the top 5 actually the best mix?
- Are lower-authority sources ranked above better professional sources?
- Are there duplicates or near-duplicates?
- Is source diversity acceptable?
- Are local sources included where useful?
- Does any resource need a jurisdiction warning?
- Does any resource need to be hidden pending human review?

Return recommended ranking changes and reasons.
```

## Prompt 5 — Document node creation review

```text
Kimi, review whether this Resource should also become a Document node in the Vitruvius graph.

Resource:
<resource JSON>

Current linked nodes:
<linked nodes summary>

Criteria:
- Is this document important enough to reason about as a graph node?
- Is it reused across many concepts/rules/procedures/evidence nodes?
- Does it represent a standard, guide, manual, textbook, report, or internal document central to the graph?
- Is metadata complete enough?
- Are copyright/access notes sufficient?

Return:
- create_document_node: yes/no/needs_review
- suggested document node type/taxonomy
- proposed relationships to existing nodes
- cautions
```

## Prompt 6 — Final quality review

```text
Kimi, perform a final review of the Vitruvius Resource Intelligence Layer implementation summary.

Review:
- data model,
- source discovery workflow,
- verification/ranking,
- sidebar UI,
- validation/tests,
- source coverage metrics,
- accepted/rejected decisions,
- remaining gaps.

Flag:
- missing quality gates,
- unsafe source assumptions,
- UI trust problems,
- weak validation,
- overclaiming,
- missing Kimi/human review for risky nodes,
- architectural simplifications that will cause future problems.

Return a prioritized fix list.
```

## Expected Kimi output format

```json
{
  "summary": "...",
  "candidateDecisions": [
    {
      "candidateId": "...",
      "decision": "accept",
      "relationship": "explains",
      "relevanceNotes": "...",
      "authorityNotes": "...",
      "jurisdictionNotes": "...",
      "recommendedRationale": "...",
      "requiresHumanReview": false
    }
  ],
  "missingSourceCategories": ["recognized textbook", "local project manual"],
  "warnings": ["Candidate 3 is jurisdiction-specific and should not be treated as universal."]
}
```

## Logging Kimi reviews

Record each Kimi review in `docs/resource-layer/kimi-review-log.md` with date, node/batch, prompt summary, accepted suggestions, rejected suggestions, implementation decision, and unresolved items.
