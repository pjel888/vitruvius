# Phase 6 Standards-Context Policy Review

Date: 2026-05-03T03:45:00+08:00

## Current Behavior Verification

### Existing Validation Rules

From `api/resourceLayer/validation.ts`:

1. **Placeholder rejection**: Values like "tbd", "latest", "current", "unknown", "generic", "placeholder", "sample", "varies", "n/a" are rejected as standards context.
2. **ASCE promotion blocker**: `isAcceptedLink(link) && sourceFamilyIncludes(resource, 'asce') && !hasCitationContext(link) && !hasStructuredMissingContextJustification(resource, link)` → blocker
3. **ACI promotion blocker**: Same pattern for ACI source family.
4. **Accepted missing context tracking**: Accepted standard links without edition or citation context are counted as `standardsAcceptedMissingContext`.

### Current Standards State

| Standard | Resource ID | Link Status | Context State |
|----------|-------------|-------------|---------------|
| ASCE 7 | res-asce-7-official-landing | needs_review (2 links) | Missing edition, version, publicationYear |
| ACI 318 | res-aci-318-building-code-portal | rejected (1 link) | Missing edition, version, publicationYear |

### Promotion Gate Verification

Current behavior confirmed:
- ✅ Missing standards context remains visible in review queue
- ✅ Placeholder values are rejected
- ✅ Accepted/promoted links require truthful context
- ✅ Reviewer, rationale, and `sourceOfContext` are required for context decisions
- ✅ No fake completion values are accepted

### Known Safe Holdings

- ASCE 7 links remain `needs_review` because edition/version/scope are unknown.
- ACI 318 link is `rejected` because it is too broad without section-specific support.
- No "latest edition" or "current code" guesses are present.

## Policy for Phase 6

### 1. No Invention Rule

- Do not invent edition numbers.
- Do not invent publication years.
- Do not invent adoption statuses.
- Do not guess jurisdictions.
- If context is unknown, record it as unknown with justification.

### 2. Justified Missing Context

A standard link MAY be accepted with incomplete context IF:
- The reviewer records a truthful `standardContextJustification`
- The justification explains WHY context is missing (e.g., "landing page only; full standard requires purchase")
- The justification does not claim the missing context is unimportant
- The resource is clearly marked as "context incomplete" in the UI

### 3. Context Completion Levels

| Level | Required Fields | Sidebar Display |
|-------|-----------------|-----------------|
| `complete` | edition + jurisdiction + scope + citation context | ✅ Full confidence |
| `partial` | edition OR jurisdiction OR scope | ⚠️ Show with caveat |
| `needs_human_review` | Any standard link without review | ⚠️ Reviewer only |
| `justified_missing` | Justification recorded + reviewer | ⚠️ Show with explicit caveat |
| `missing` | No context, no justification | ❌ Block from promotion |

### 4. ASCE/ACI Specific Policy

- ASCE 7 links MUST NOT be promoted without:
  - Edition (e.g., "ASCE 7-22")
  - Minimum design load chapter/section reference OR explicit justification
  - Jurisdiction/applicability note
- ACI 318 links MUST NOT be promoted without:
  - Edition (e.g., "ACI 318-19")
  - Chapter/section-specific reference OR explicit justification
  - Jurisdiction/applicability note

### 5. UI Behavior

- Standards with incomplete context show "Context incomplete — not a compliance claim" badge.
- Standards with `justified_missing` show "Limited context — see reviewer note" badge.
- No standard is displayed as "current" or "latest" unless the edition field explicitly contains that text (which is discouraged).

## Implementation Queue

- Loop 6D: Harden standards-context enforcement in validation and UI.
- No schema changes needed; use existing `StandardReviewContext` and `standardContextJustification` fields.
