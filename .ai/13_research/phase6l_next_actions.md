# Phase 6L Next Actions

**Date:** 2026-05-03
**Status:** Planning Complete — No Implementation

---

## What Was Planned

1. **Promotion apply philosophy** — Two apply modes (resource-only, resource+links), verification philosophy, learner exposure rules
2. **Promotion apply gate design** — 9 gates (A-I) covering candidate status, metadata integrity, source truth, rights, standards, node-link, display, transaction, audit
3. **Future Resource record shape** — Base fields + promotion provenance + safe defaults + forbidden fields
4. **Future NodeResourceLink shape** — Base fields + link promotion provenance + safe defaults + multi-link rules
5. **Promotion apply API plan** — 4 future routes (apply-preview, apply, rollback-preview, rollback)
6. **Transaction/rollback model** — Transaction manifest requirements, rollback strategies, audit preservation
7. **Promotion apply UI plan** — Apply preview panel, mode selector, gate checklist, warning panels, safe wording
8. **Test plan** — 21 API tests, 10 UI tests for future implementation
9. **Stop conditions** — 38 hard stop conditions, 4 warning conditions

## What Was NOT Implemented

- No promotion apply route
- No resource creation
- No nodeResourceLink creation
- No graph/canonical mutation
- No external verification
- No learner exposure
- No production registry mutation

## Recommended Implementation Sequence

### Phase 6M: Resource-Only Promotion Apply
- Lower blast radius
- No graph node dependency
- Creates Resource in `resources.json` only
- Transaction-backed with rollback
- Requires all gates A-E, G-I

### Phase 6N: Resource + NodeResourceLink Promotion Apply
- Higher blast radius
- Requires node existence validation
- Creates Resource + NodeResourceLinks
- Links default to `needs_review`
- Requires all gates A-I

### Phase 6O+: Link Acceptance Workflow
- Separate from promotion apply
- Reviews promoted links individually
- Can accept links to make them learner-eligible
- Independent of resource promotion

## Next Safe Phase

**Phase 6M audit** — Independent audit of the resource-only promotion apply plan before any implementation.

## Standing Constraints

- ASCE 7 and ACI 318 remain blocked
- No fake metadata
- No auto-promotion
- No auto-linking
- No learner exposure without explicit verification
- Promotion apply requires explicit project-owner steward authorization
