# Phase 5 Fire/Egress Rationale Review

Date: 2026-05-03T02:45:00+08:00

## Edges Reviewed

| Edge | Type | Rationale (truncated) |
|------|------|----------------------|
| VTN-DOM-0000056→0000058 | CONSTRAINS | "Fire protection requirements constrain egress design, including exit capacity, travel distance, door swing direction, and smoke-proof enclosure criteria. General domain-synthesis only; not a code-compliance, AHJ, or numerical claim." |
| VTN-DOM-0000058→0000056 | REQUIRES | "Egress design requires fire protection input to ensure exit routes remain tenable during fire events and meet code-mandated protection levels. General domain-synthesis only; not a code-compliance, AHJ, or numerical claim." |

## Code-Like Wording Identified

| Phrase | Location | Assessment |
|--------|----------|------------|
| "exit capacity" | CONSTRAINS rationale | **Domain-synthesis reference** — describes a design consideration, not a numerical capacity claim |
| "travel distance" | CONSTRAINS rationale | **Domain-synthesis reference** — describes a design dimension, not a specific distance value |
| "door swing direction" | CONSTRAINS rationale | **Domain-synthesis reference** — describes a design attribute, not a code-mandated direction |
| "smoke-proof enclosure criteria" | CONSTRAINS rationale | **Domain-synthesis reference** — describes a design strategy, not a specific standard criterion |
| "code-mandated protection levels" | REQUIRES rationale | **Softened by caveat** — the phrase appears but is explicitly disclaimed |

## Caveat Analysis

Both rationales end with:
> "General domain-synthesis only; not a code-compliance, AHJ, or numerical claim."

This caveat is present and explicit. However, the task notes that even caveated code-like wording can be misread.

## Classification

| Edge | Classification | Action |
|------|---------------|--------|
| Fire Protection CONSTRAINS Egress | **Safe with caveat** — wording could be softer | Queue for future metadata repair |
| Egress REQUIRES Fire Protection | **Safe with caveat** — "code-mandated" is the riskiest phrase | Queue for future metadata repair |

## Recommended Rationale Rewording (for future metadata repair)

**CONSTRAINS** (proposed):
> "Fire protection objectives influence egress design considerations such as exit configuration, route tenability, and enclosure strategies. General domain-synthesis only; not a code-compliance, AHJ, or numerical claim."

**REQUIRES** (proposed):
> "Egress planning relies on fire protection guidance to maintain safe evacuation conditions during fire events. General domain-synthesis only; not a code-compliance, AHJ, or numerical claim."

## Decision

**No registry mutation in this task.**

Rationale:
1. Both edges already have explicit caveats.
2. The code-like phrases are design-domain references, not numerical/standard assertions.
3. Updating 2 edge rationales would require a transaction manifest and registry mutation.
4. The risk of the current wording is low (caveated, no numerical values, no standard citations).
5. Queued for future metadata-only rationale repair if a maintenance window opens.

## Other Fire-Related Edges Inspected

No other admitted edges involving Fire Protection or Egress were found in the active registry.
