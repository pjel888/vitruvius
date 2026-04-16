---
task: duplicate-canonical-source-id-remediation
phase: 05
created: 2026-04-16
author: PLANNER
supersedes: null
status: ACCEPTED
---

# 2026-04-16 Duplicate Canonical Source ID Remediation Plan

## Executive Summary
Resolve the remaining duplicate canonical source ID by retaining the live pipeline-backed IRR source page, folding the richer lineage/content from the duplicate page into it, removing the duplicate draft source page, and revalidating graph integrity plus impacted tests/docs.

## Audit / Evidence Basis
- `.ai/02_audits/2026-04-16_backend-and-api-audit.md`
- `.ai/02_audits/2026-04-16_targeted-stabilization-reaudit.md`
- `.ai/05_logs/2026-04-16_audit-pass-2-fix-validation.md`

## Problem Statement
Two canonical source pages in `003_Canonical-Knowledge-Layer/shared/sources/` both declare the same ID `irr-implementing-rules-and-regulations-of-the-national-building-code`. PASS 2 fixed detection only, so `build-graph` now fails loudly but the underlying collision still blocks a green graph integrity pass.

## Scope
### In Scope
- `003_Canonical-Knowledge-Layer/shared/sources/pd-1096-irr.md`
- `003_Canonical-Knowledge-Layer/shared/sources/implementing-rules-and-regulations-of-the-national-building-code.md`
- `.ai/10_state/datasets.json`
- targeted docs/log/state updates needed to reflect the remediation
- targeted graph/query tests or fixtures if impacted

### Out of Scope
- wider graph/query feature changes
- raw-layer corpus edits
- new canonical ID generation rules
- relationship extraction logic changes unrelated to this duplicate

## Proposed Fix
1. Retain `implementing-rules-and-regulations-of-the-national-building-code.md` as the authoritative live page because it is the pipeline-backed path already referenced by the dataset registry and canonicalize outputs.
2. Fold the richer lineage/content from `pd-1096-irr.md` into the retained live page so no source-lineage scope is lost.
3. Confirm file-path registries that still point at the live IRR source already reference `implementing-rules-and-regulations-of-the-national-building-code.md` (`.ai/10_state/datasets.json`), so no registry migration is required.
4. Remove the duplicate live source page `pd-1096-irr.md` from the canonical source directory.
5. Re-run `build-graph` and targeted tests to confirm the duplicate-node integrity error is cleared.
6. Update validation/state/docs/logs to reflect that the blocking duplicate-ID caveat is resolved.

## Safety / Truth Notes
- This plan does **not** change the retained canonical ID. It removes the duplicate page that reused that same ID.
- Because the canonical ID remains stable, relationship records and graph edges that already reference the ID should continue to resolve.
- The fix should be validated against any file-path registries that previously referenced the removed file.

## Plan Critique
- Risk: deleting the wrong file would silently reduce source lineage or break live path references. Mitigation: retain the already-referenced live path `implementing-rules-and-regulations-of-the-national-building-code.md`, then fold the broader lineage from `pd-1096-irr.md` into it before deletion.
- Risk: there may be hidden filename-level references outside graph code. Mitigation: grep file-path references before deletion and update the known dataset registry.
- Risk: this could expose additional graph issues after the duplicate-node blocker is removed. Mitigation: run `build-graph` and inspect the full integrity report after the fix.

## Execution Checklist
- [x] Confirmed the retained live page should remain `implementing-rules-and-regulations-of-the-national-building-code.md`; `pd-1096-irr.md` was the duplicate live page
- [x] No file-path registry migration was needed because `.ai/10_state/datasets.json` already pointed at the retained page
- [x] Removed the duplicate live source page after folding its richer lineage/content into the retained page
- [x] Re-ran `build-graph`; duplicate-node integrity error cleared
- [x] Re-ran targeted graph/query tests and validation
- [x] Updated validation/state/docs to remove the resolved duplicate-ID caveat
