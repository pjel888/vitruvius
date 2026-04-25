---
task: aec-mepfs-backbone
phase: legal-and-steward-admission
created: 2026-04-25
author: CODEX
status: PREPARED-PENDING-HUMAN-SIGNOFF
---

# Legal And Steward Admission Record

## Purpose

Separate AI-prepared evidence from human/steward/legal decisions for the
AEC-MEPFS Backbone.

AI systems may prepare evidence, draft recommendations, and validate candidate
files. They may not self-approve canonical taxonomy, source rights, legal
clearance, jurisdiction precedence, or canonical source admission.

## Decision Boundary

| Decision | AI can prepare | Human/legal authority required | Current status |
|---|---|---|---|
| Predicate registry admission | candidate rows, validator reports, duplicate/vague-edge checks | named steward approval | pending |
| Source-rights registry admission | source rows, URL evidence, conservative allowed-use class | named source steward and legal/licensing reviewer for any escalation | pending |
| Legal/licensing clearance | evidence summary and no-ingest defaults | legal/licensing reviewer | pending |
| Source currentness | official URL reachability and exception list | source steward/currentness reviewer | evidence collected; decision pending |
| Canonical source admission | admission checklist and blocked packet | steward plus required reviewer | pending |
| Runtime implementation approval | impact map and bounded packet | architecture steward plus required reviewers | pending |

## Conservative AI Decision

Until a human/legal reviewer records otherwise:

- all protected standards remain `reference_only`
- all source text, tables, figures, clauses, data templates, and local dataset
  caches remain blocked
- metadata crosswalk rows may remain candidates only
- public-law or government-source rows may be cited for source-family planning
  only, not extracted into canonical legal overlays
- no source row is `cleared_for_declared_use`
- no source row is `content_ingest`

## Named Steward Status

Philip Lewis is already recorded as accountable readiness steward and source
owner in `governance-editorial-control-pack.md`.

That owner assignment closes the ownerless planning gap. It does not close:

- independent second review
- discipline review
- legal/licensing review
- Philippines jurisdiction/code review
- admission-time currentness review

## Human Decision Checklist

Before runtime implementation, the following rows need explicit decisions:

| Decision ID | Required decision | Minimum evidence | Decision state |
|---|---|---|---|
| `S7-DEC-001` | Accept/reject 12 predicate registry candidates for runtime registry staging | S6 validation report and predicate registry candidate | pending human steward |
| `S7-DEC-002` | Accept/reject 29 source-rights registry candidates as planning registry rows | S6 validation report and S7 currentness report | pending source steward |
| `S7-DEC-003` | Confirm that no protected source is cleared beyond reference/crosswalk use | legal/source pack and source currentness report | pending legal/licensing reviewer |
| `S7-DEC-004` | Accept/reject manual-review exception rows | `source-currentness-evidence-pack.md` | pending source/currentness reviewer |
| `S7-DEC-005` | Authorize or reject first canonical source admission | `canonical-source-admission-packet.md` | pending steward plus legal/currentness gates |
| `S7-DEC-006` | Authorize or reject first runtime implementation slice | `runtime-root-implementation-packet.md` | pending architecture steward and impact review |

## Prohibited Shortcut

Do not treat this file, a chat instruction, or an AI-generated commit as legal
clearance or canonical admission. Admission requires a reviewer decision entry
with reviewer identity, date, evidence path, and exact allowed use.
