# Phase 6 Resource Ranking Policy

Date: 2026-05-03T03:45:00+08:00

## Goal

Define the top-resource selection policy per node to avoid dumping hundreds of links on users.

## Sidebar Targets

| View | Max Resources | Grouping |
|------|--------------|----------|
| Learner-facing sidebar | 3–8 primary | By authority + confidence |
| Reviewer/dev view | up to 15 | By status + type |

## Current Ranking Formula

The existing formula in `api/resourceLayer/ranking.ts`:

```
displayScore = relevance * 0.45
             + authority * 0.25
             + confidence * 0.15
             + verification * 0.10
             + access * 0.05
             - penalties
```

Penalties:
- unverified: -0.20
- generalWeb: -0.12
- missingTitle: -0.25
- needsReview: -0.20
- candidate: -0.25
- rejected: -1.00

## Proposed Phase 6 Ranking Enhancements

### 1. Accepted-First Hard Gate

Learner sidebar ONLY includes links with `reviewStatus === 'accepted'` or `'human_reviewed'`.
All other statuses are filtered out before ranking.

### 2. Standards-Context Boost/Penalty

| Context State | Score Modifier |
|---------------|----------------|
| `complete` | +0.05 |
| `partial` | 0 |
| `missing` (standard accepted anyway) | -0.15 |
| `not_required` | 0 |
| `needs_human_review` | -0.20 |

### 3. Node Specificity Scoring

Use `link.nodeSpecificity` or `link.relationship` to weight direct references higher:

| Relationship | Weight Multiplier |
|--------------|-------------------|
| `is_primary_reference_for` | 1.3x |
| `defines`, `governs` | 1.2x |
| `explains`, `supports` | 1.1x |
| `provides_example`, `provides_historical_context` | 1.0x |
| `is_supplementary_reference_for` | 0.9x |

### 4. Recency Scoring (Where Meaningful)

Only apply recency bonus to:
- Standards (if edition/year known)
- Technical reports
- Government guidance

Do NOT apply recency to:
- Books without edition
- Historical sources
- General web pages (too volatile)

### 5. Source Rights Penalty

| Rights Status | Penalty |
|---------------|---------|
| `public` | 0 |
| `open_access` | 0 |
| `licensed` | -0.05 |
| `excerpt_limited` | -0.10 |
| `protected_content` | -0.15 |
| `unknown` | -0.08 |

### 6. Domain Fit Scoring

If the resource's `sourceFamilyId` or `jurisdiction` aligns with the node's taxonomy domain, apply a small boost (+0.03).

Example:
- Node: "Philippine National Building Code" → boost Philippine-law sources
- Node: "ASCE 7 Wind Load" → boost ASCE/IBC-adopted sources

## Ranking Algorithm (Proposed)

```
function rankForSidebar(nodeId, links, resources, options) {
  const eligible = links
    .filter(l => l.nodeId === nodeId)
    .filter(l => ['accepted', 'human_reviewed'].includes(l.reviewStatus))
    .map(l => ({
      link: l,
      resource: resources.find(r => r.id === l.resourceId),
      baseScore: displayScore(resource, link),
      contextModifier: standardContextModifier(link),
      specificityBoost: relationshipSpecificityBoost(link),
      rightsPenalty: rightsPenalty(resource),
      domainBoost: domainFitBoost(nodeId, resource),
    }));

  eligible.forEach(e => {
    e.finalScore = Math.max(0, Math.min(1,
      e.baseScore
      + e.contextModifier
      + e.specificityBoost
      - e.rightsPenalty
      + e.domainBoost
    ));
  });

  return eligible
    .sort((a, b) => b.finalScore - a.finalScore)
    .slice(0, options.limit || 8);
}
```

## Tie-Breaking Rules

1. Higher `verificationStatus` wins
2. Local file verified wins over URL
3. More complete citation context wins
4. Earlier `lastCheckedAt` (more recently verified) wins
5. Alphabetical by title

## No-Dump Safeguards

- Hard limit: 8 resources in learner view
- If fewer than 3 accepted links exist, show what exists with "Limited evidence" warning
- If zero accepted links exist, show "No verified sources for this node" message
- Never show candidates, needs_review, or rejected links to learners
