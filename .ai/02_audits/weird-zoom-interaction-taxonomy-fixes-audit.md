---
task: weird-zoom-interaction-taxonomy-fixes
phase: 04
author: AUDITOR
created: 2026-04-30
supersedes: null
status: ACCEPTED
---

# Audit

The requested work is consistent with the active AEC-MEPFS file-backed Explorer milestone if changes stay local, metadata-only, and rights-safe. The primary risks are unintended selection loss, movement of unrelated nodes, route-scope widening, and accidental disturbance of existing uncommitted enrichment work.

Required controls:
- Preserve existing uncommitted work.
- Add targeted tests before or with fixes.
- Keep API expansion bounded and file-backed.
- Do not perform live graph promotion, KG rebuild/reload/reset, raw-source writes, or protected payload admission.
