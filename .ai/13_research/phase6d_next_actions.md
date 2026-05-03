# Phase 6D Next Actions

Date: 2026-05-03T05:15:00+08:00

## Immediate Next Action

**Loop 6B — Node Sidebar Resource Ranking API**

Implement learner-facing sidebar resource ranking:
1. `GET /node/:id/resources` returns ranked, accepted-only resources (hard limit 8).
2. Apply standards-context modifiers to displayScore.
3. Return warning flags for incomplete context.
4. Update `NodeInspector` Sources tab to consume ranked API.
5. Add "Limited evidence" empty state.

## Deferred Actions

- **Loop 6C:** Reviewer source-custody queue enhancements (local file admission, rights display, unified triage).
- **Loop 6E:** External URL/book/PDF metadata candidate workflow.
- **Loop 6F:** Evidence-path regression tests.

## No-Go Items

- Do not promote ASCE 7 or ACI 318 without real edition/section/context.
- Do not auto-link the 25 indexed local files.
- Do not mutate graph topology.
- Do not process P0 Concrete/Reinforced Concrete duplicates.
