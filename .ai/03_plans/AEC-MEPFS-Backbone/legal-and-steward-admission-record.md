---
task: aec-mepfs-backbone
phase: legal-and-steward-admission
created: 2026-04-25
author: CODEX
status: OWNER-DIRECTIVE-RECORDED-FOR-SHADOW-STAGING
---

# Legal And Steward Admission Record

## Purpose

Separate AI-prepared evidence from human/steward/legal decisions for the
AEC-MEPFS Backbone.

AI systems may prepare evidence, draft recommendations, and validate candidate
files. They may not self-approve canonical taxonomy, source rights, legal
clearance, jurisdiction precedence, or canonical source admission.

On 2026-04-25T15:39:12Z, a project-owner directive was captured in the S8 human
inbox. That directive accepts the bounded no-ingest, metadata/reference,
shadow-only posture below. It is not independent legal advice and it does not
clear protected content ingest.

## Decision Boundary

| Decision | AI can prepare | Human/legal authority required | Current status |
|---|---|---|---|
| Predicate registry admission | candidate rows, validator reports, duplicate/vague-edge checks | named steward approval | accepted for first-slice shadow staging only |
| Source-rights registry admission | source rows, URL evidence, conservative allowed-use class | named source steward and legal/licensing reviewer for any escalation | accepted for metadata/reference shadow staging only |
| Legal/licensing clearance | evidence summary and no-ingest defaults | legal/licensing reviewer | no-ingest posture accepted; content ingest still blocked |
| Source currentness | official URL reachability and exception list | source steward/currentness reviewer | accepted for declared reference/metadata use only |
| Canonical source admission | admission checklist and blocked packet | steward plus required reviewer | zero-content metadata staging accepted; content admission remains blocked |
| Runtime implementation approval | impact map and bounded packet | architecture steward plus required reviewers | first additive shadow-only implementation packet implemented |

## Conservative AI Decision

Unless a later reviewer records a broader allowed use:

- all protected standards remain `reference_only`
- all source text, tables, figures, clauses, data templates, and local dataset
  caches remain blocked
- metadata crosswalk rows may be used for first-slice shadow staging only
- public-law or government-source rows may be cited for source-family planning
  only, not extracted into canonical legal overlays
- no source row is cleared beyond declared reference/metadata use
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

## Recorded Decision Checklist

Before runtime implementation, the following rows need explicit decisions:

| Decision ID | Required decision | Minimum evidence | Decision state |
|---|---|---|---|
| `S7-DEC-001` | Accept/reject 12 predicate registry candidates for runtime registry staging | S6 validation report and predicate registry candidate | approved for first-slice shadow staging |
| `S7-DEC-002` | Accept/reject 29 source-rights registry candidates as planning registry rows | S6 validation report and S7/S8 currentness reports | approved for metadata/reference shadow staging |
| `S7-DEC-003` | Confirm that no protected source is cleared beyond reference/crosswalk use | legal/source pack and source currentness report | approved as no-ingest posture; content ingest blocked |
| `S7-DEC-004` | Accept/reject manual-review exception rows | `source-currentness-evidence-pack.md` | approved for declared reference/metadata use only |
| `S7-DEC-005` | Authorize or reject first canonical source admission | `canonical-source-admission-packet.md` | approved for zero-content metadata staging only |
| `S7-DEC-006` | Authorize or reject first runtime implementation slice | `runtime-root-implementation-packet.md` and `first-shadow-only-implementation-packet.md` | approved and implemented for first additive shadow-only packet |

## Prohibited Shortcut

Do not treat this file, a chat instruction, or an AI-generated commit as legal
clearance for protected content ingest or primary graph admission. The recorded
S8 directive is accepted only because the allowed use is explicitly bounded to
no-ingest, metadata/reference, shadow-only work with reviewer identity, date,
evidence path, and exact use captured in the inbox and acceptance record.
